"""Lazy autonomous loop for LazyOwn.

Double-graph engine without external services.

Semantics:
    AssetGraph is global shared truth, ExplorationGraph is per-task,
    anchors join them, Planner is the sole intent generator emitting
    0..N intents per wakeup, each Worker claims exactly ONE intent and
    writes facts back, Guard gates every tool call, Enrich completes
    DNS/HTTP asynchronously, Traffic records every execution, Retester
    replays findings to a verdict, cold compaction folds stale nodes.

Persistence:
    JSON files under ``sessions/lazy/`` so every state survives
    restarts and stays inspectable from the CLI. Legacy ``sessions/lazy/``
    files are migrated automatically on first use.

Usage:
    from modules.lazy_loop import LazyLoopEngine
    engine = LazyLoopEngine()
    task = engine.create_task("gain initial access on 10.10.11.5")
    engine.run(task.task_id)
"""

from __future__ import annotations

import hashlib
import json
import re
import socket
import threading
import time
import urllib.request
from dataclasses import asdict, dataclass, field
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
STORE_DIR = BASE_DIR / "sessions" / "lazy"

EXPLORATION_NODE_KINDS = ("goal", "intent", "fact", "finding", "hint", "constraint")
EXPLORATION_TERMINAL_STATES = ("done", "blocked", "exhausted", "stopped")
EXPLORATION_ACTIVE_STATES = ("pending", "open", "running")
INTENT_OPEN_STATES = ("pending", "open")
ASSET_KINDS = ("root_domain", "subdomain", "ip", "cidr", "url", "service", "app", "endpoint",
               "cred", "fingerprint")
TASK_STATUSES = ("queued", "running", "paused", "done", "failed", "timeout", "exhausted")
EDGE_KINDS = ("spawns", "derived_from", "yields", "proves", "anchors")
CONSTRAINT_TYPES = ("allow", "deny")
RETEST_VERDICTS = ("reproduced", "fixed", "inconclusive")
RETEST_LEGACY = {"reproducible": "reproduced", "unconfirmed": "inconclusive"}
SEVERITIES = ("critical", "high", "medium", "low", "info")
SEV_RANK = {"critical": 0, "high": 1, "medium": 2, "low": 3, "info": 4, "": 5}
FINDING_STATUSES = ("pending", "in_progress", "confirmed", "resolved", "fixed",
                    "false_positive", "ignored", "duplicate", "risk_accepted")
TRIGGER_KINDS = ("interval", "finding", "goal", "timeout", "toolcall", "hint")
GUARD_ACTIONS = ("allow", "ask", "deny")
TRAFFIC_KINDS = ("bash", "http", "note")
DEFAULT_MAX_ROUNDS = 10
DEFAULT_WORKERS = 3
DEFAULT_DEBOUNCE_SEC = 0.5
DEFAULT_COLD_THRESHOLD = 50
DEFAULT_PRIORITY = 5
MAX_PRIORITY = 10
MAX_INTENTS_PER_ROUND = 4
MAX_FACTS_PAGE = 100
MAX_WORKER_STEPS = 6
RETEST_MAX_ATTEMPTS = 2
ABORT_CAUSES = ("shutdown", "goal_met", "paused", "killed", "timeout", "budget", "user")
DEFAULT_MAX_TOOLCALLS = 200
DEFAULT_MAX_FINDINGS = 50
INTERCEPT_TIMEOUT_SEC = 30.0
TRAFFIC_INLINE_CUTOFF = 256 * 1024
TRAFFIC_PREVIEW = 8192
TOOL_DEFAULTS: dict[str, dict] = {
    "nmap": {"cmd": "nmap -sV --top-ports 100 {target}", "kind": "recon",
             "desc": "Service/version discovery on top ports"},
    "nmap_full": {"cmd": "nmap -sV -p- --min-rate 500 {target}", "kind": "recon",
                  "desc": "Full-port service sweep (slow, noisy)"},
    "curl_head": {"cmd": "curl -sSI --max-time 15 http://{target}", "kind": "recon",
                  "desc": "HTTP header probe"},
    "curl_get": {"cmd": "curl -sS -m 20 http://{target}", "kind": "recon",
                 "desc": "HTTP body fetch"},
    "dig": {"cmd": "dig +short {target}", "kind": "recon",
            "desc": "DNS resolution"},
    "host": {"cmd": "host {target}", "kind": "recon",
             "desc": "DNS lookup"},
    "whatweb": {"cmd": "whatweb http://{target}", "kind": "fingerprint",
                "desc": "Web fingerprint"},
    "nikto": {"cmd": "nikto -h http://{target}", "kind": "vuln",
              "desc": "Web vuln scan"},
}


def _now() -> float:
    """Return current epoch seconds."""
    return time.time()


def _store_path(name: str) -> Path:
    """Return JSON store path, ensuring the directory exists."""
    STORE_DIR.mkdir(parents=True, exist_ok=True)
    return STORE_DIR / name


def _load_json(path: Path, default: dict) -> dict:
    """Load JSON mapping from path or return default copy."""
    try:
        if path.exists():
            return json.loads(path.read_text())
    except Exception:
        pass
    return json.loads(json.dumps(default))


def _save_json(path: Path, payload: dict) -> None:
    """Atomically persist payload to path."""
    tmp = path.with_suffix(".tmp")
    tmp.write_text(json.dumps(payload, indent=2, ensure_ascii=False))
    tmp.replace(path)


def _slug(value: str) -> str:
    """Normalize value into a dedupe key fragment."""
    return re.sub(r"[^a-z0-9]+", "-", (value or "").strip().lower()).strip("-")


def _traffic_template(command: str) -> str:
    """Group exchanges by URL-template like the traffic proxy index."""
    text = (command or "").strip()[:300]
    text = re.sub(r"\b(?:\d{1,3}\.){3}\d{1,3}\b", "{host}", text)
    text = re.sub(r"\b[0-9a-f]{8}-[0-9a-f\-\.]{4,}\b", "{id}", text, flags=re.IGNORECASE)
    text = re.sub(r"(?<=/)\d+(?=[/\s]|$)", "{id}", text)
    text = re.sub(r"[0-9]{4,}", "{n}", text)
    return text[:200]


@dataclass
class ExplorationNode:
    """Single node of the per-task exploration graph."""

    node_id: int
    kind: str
    text: str
    state: str = "pending"
    priority: int = DEFAULT_PRIORITY
    created: float = field(default_factory=_now)
    updated: float = field(default_factory=_now)
    meta: dict = field(default_factory=dict)


@dataclass
class ExplorationEdge:
    """Directed edge between exploration nodes."""

    src: int
    dst: int
    kind: str


@dataclass
class AssetNode:
    """Single node of the global asset graph."""

    asset_id: int
    kind: str
    value: str
    parent_id: int = 0
    dedupe_key: str = ""
    tested: bool = False
    created: float = field(default_factory=_now)
    meta: dict = field(default_factory=dict)


@dataclass
class LazyTask:
    """Lifecycle record for one autonomous engagement."""

    task_id: str
    goal: str
    description: str = ""
    status: str = "running"
    created: float = field(default_factory=_now)
    updated: float = field(default_factory=_now)


class AssetGraph:
    """Global shared asset truth across tasks."""

    def __init__(self) -> None:
        """Load persisted assets or start empty."""
        self._path = _store_path("assets.json")
        raw = _load_json(self._path, {"seq": 0, "nodes": []})
        self._seq = int(raw.get("seq", 0))
        self.nodes: dict[int, AssetNode] = {}
        for item in raw.get("nodes", []):
            try:
                node = AssetNode(**{k: v for k, v in item.items() if k in AssetNode.__dataclass_fields__})
                self.nodes[node.asset_id] = node
            except TypeError:
                continue
        self._lock = threading.Lock()

    def _persist(self) -> None:
        """Persist current assets to disk."""
        _save_json(self._path, {"seq": self._seq, "nodes": [asdict(n) for n in self.nodes.values()]})

    def dedupe_key(self, kind: str, value: str, parent_id: int = 0) -> str:
        """Compute program-owned dedupe key for an asset."""
        return f"{kind}:{parent_id}:{_slug(value)}"

    def insert(self, kind: str, value: str, parent_id: int = 0, meta: dict | None = None) -> AssetNode:
        """Insert asset or return existing node with same dedupe key."""
        if kind not in ASSET_KINDS:
            raise ValueError(f"unknown asset kind: {kind}")
        value = (value or "").strip()
        if not value:
            raise ValueError("asset value is required")
        verdict = AssetGate().evaluate(value)
        if not verdict["allowed"]:
            raise ValueError(verdict["reason"])
        key = self.dedupe_key(kind, value, parent_id)
        with self._lock:
            for node in self.nodes.values():
                if node.dedupe_key == key:
                    return node
            self._seq += 1
            node = AssetNode(asset_id=self._seq, kind=kind, value=value,
                             parent_id=parent_id, dedupe_key=key, meta=dict(meta or {}))
            self.nodes[node.asset_id] = node
            self._persist()
            return node

    def get(self, asset_id: int) -> AssetNode | None:
        """Return asset by id or None."""
        return self.nodes.get(int(asset_id))

    def list(self, kind: str = "") -> list[AssetNode]:
        """List assets optionally filtered by kind."""
        items = list(self.nodes.values())
        if kind:
            items = [n for n in items if n.kind == kind]
        return sorted(items, key=lambda n: n.asset_id)

    def mark_tested(self, asset_id: int) -> bool:
        """Flag asset as tested by a worker intent."""
        with self._lock:
            node = self.nodes.get(int(asset_id))
            if node is None:
                return False
            node.tested = True
            self._persist()
            return True

    def coverage(self, scope: list[dict] | None = None) -> dict:
        """Compute tested/total coverage, optionally scoped."""
        items = list(self.nodes.values())
        if scope:
            wanted = {(s.get("kind"), s.get("value")) for s in scope if s.get("value")}
            items = [n for n in items if (n.kind, n.value) in wanted]
        total = len(items)
        tested = sum(1 for n in items if n.tested)
        by_type: dict[str, dict[str, int]] = {}
        for node in items:
            bucket = by_type.setdefault(node.kind, {"total": 0, "tested": 0})
            bucket["total"] += 1
            bucket["tested"] += int(node.tested)
        pct = round(100.0 * tested / total, 1) if total else 0.0
        return {"total": total, "tested": tested, "pct": pct, "by_type": by_type}

    def untested(self, limit: int = 20) -> list[AssetNode]:
        """Return oldest untested assets up to limit."""
        items = [n for n in self.nodes.values() if not n.tested]
        return sorted(items, key=lambda n: n.asset_id)[: max(1, limit)]

    def coverage_for(self, graph=None, scope: list[dict] | None = None) -> dict:
        """Compute task-scoped coverage like the planner graph_overview.

        Tested means anchored to a terminal intent of THIS task, not the
        global flag polluted by other tasks on the same target.
        """
        items = list(self.nodes.values())
        if scope:
            wanted = [(str(s.get("kind", "")).lower(), str(s.get("value", "")).lower())
                      for s in scope if s.get("value")]
            scoped = []
            for node in items:
                for kind, value in wanted:
                    if value and value in node.value.lower():
                        scoped.append(node)
                        break
                    if kind == "cidr" and node.kind == "ip" and value:
                        scoped.append(node)
                        break
            items = scoped
        tested_ids: set[int] = set()
        if graph is not None:
            try:
                for node in graph.list("intent"):
                    if node.state in EXPLORATION_TERMINAL_STATES:
                        tested_ids.update(graph.anchors_for(node.node_id))
            except Exception:
                tested_ids = set()
        total = len(items)
        tested = sum(1 for n in items if n.asset_id in tested_ids)
        by_type: dict[str, dict[str, int]] = {}
        for node in items:
            bucket = by_type.setdefault(node.kind, {"total": 0, "tested": 0})
            bucket["total"] += 1
            bucket["tested"] += int(node.asset_id in tested_ids)
        pct = round(100.0 * tested / total, 1) if total else 0.0
        return {"total": total, "tested": tested, "pct": pct, "by_type": by_type}

    def untested_for(self, graph=None, scope: list[dict] | None = None,
                     limit: int = 20) -> list[AssetNode]:
        """Return scope-filtered assets not yet covered by this task.

        Lazy list_untested_assets is per-task: global tested flag from
        other tasks must not starve a new task on the same target.
        An asset counts as covered only when this task already anchored
        it to a terminal intent.
        """
        scope = scope or []
        covered: set[int] = set()
        if graph is not None:
            try:
                for node in graph.list("intent"):
                    if node.state in EXPLORATION_TERMINAL_STATES:
                        covered.update(graph.anchors_for(node.node_id))
            except Exception:
                covered = set()
        items = [n for n in self.nodes.values() if n.asset_id not in covered]
        if scope:
            wanted = [(str(s.get("kind", "")).lower(), str(s.get("value", "")).lower())
                      for s in scope if s.get("value")]
            filtered = []
            for node in items:
                for kind, value in wanted:
                    if value and value in node.value.lower():
                        filtered.append(node)
                        break
                    if kind == "cidr" and node.kind == "ip" and value:
                        filtered.append(node)
                        break
            items = filtered
        items.sort(key=lambda n: (n.tested, n.asset_id))
        return items[: max(1, limit)]


class ExplorationGraph:
    """Per-task exploration graph with anchors into the asset graph."""

    def __init__(self, task_id: str) -> None:
        """Load task graph or start empty."""
        self.task_id = task_id
        self._path = _store_path(f"exp_{task_id}.json")
        raw = _load_json(self._path, {"seq": 0, "nodes": [], "edges": [], "anchors": []})
        self._seq = int(raw.get("seq", 0))
        self.nodes: dict[int, ExplorationNode] = {}
        for item in raw.get("nodes", []):
            try:
                node = ExplorationNode(**{k: v for k, v in item.items() if k in ExplorationNode.__dataclass_fields__})
                self.nodes[node.node_id] = node
            except TypeError:
                continue
        self.edges: list[ExplorationEdge] = []
        for item in raw.get("edges", []):
            try:
                self.edges.append(ExplorationEdge(src=int(item["src"]), dst=int(item["dst"]), kind=str(item["kind"])))
            except (KeyError, ValueError, TypeError):
                continue
        self.anchors: list[dict] = [a for a in raw.get("anchors", []) if isinstance(a, dict)]
        self._lock = threading.Lock()

    def _persist(self) -> None:
        """Persist task graph to disk."""
        _save_json(self._path, {
            "seq": self._seq,
            "nodes": [asdict(n) for n in self.nodes.values()],
            "edges": [asdict(e) for e in self.edges],
            "anchors": self.anchors,
        })

    def add_node(self, kind: str, text: str, state: str = "pending",
                 priority: int = DEFAULT_PRIORITY, meta: dict | None = None) -> ExplorationNode:
        """Append node and return it."""
        if kind not in EXPLORATION_NODE_KINDS:
            raise ValueError(f"unknown node kind: {kind}")
        text = (text or "").strip()
        if not text:
            raise ValueError("node text is required")
        with self._lock:
            self._seq += 1
            node = ExplorationNode(node_id=self._seq, kind=kind, text=text,
                                   state=state, priority=max(0, min(MAX_PRIORITY, int(priority))),
                                   meta=dict(meta or {}))
            self.nodes[node.node_id] = node
            self._persist()
            return node

    def get(self, node_id: int) -> ExplorationNode | None:
        """Return node by id or None."""
        return self.nodes.get(int(node_id))

    def set_state(self, node_id: int, state: str) -> bool:
        """Transition node state and persist."""
        with self._lock:
            node = self.nodes.get(int(node_id))
            if node is None:
                return False
            node.state = state
            node.updated = _now()
            self._persist()
            return True

    def add_edge(self, src: int, dst: int, kind: str) -> bool:
        """Link two existing nodes."""
        if kind not in EDGE_KINDS:
            raise ValueError(f"unknown edge kind: {kind}")
        with self._lock:
            if src not in self.nodes or dst not in self.nodes:
                return False
            if any(e.src == src and e.dst == dst and e.kind == kind for e in self.edges):
                return True
            self.edges.append(ExplorationEdge(src=src, dst=dst, kind=kind))
            self._persist()
            return True

    def anchor(self, node_id: int, asset_id: int) -> bool:
        """Anchor exploration node to a concrete asset."""
        with self._lock:
            if node_id not in self.nodes:
                return False
            if any(a.get("node_id") == node_id and a.get("asset_id") == asset_id for a in self.anchors):
                return True
            self.anchors.append({"node_id": node_id, "asset_id": int(asset_id), "ts": _now()})
            self._persist()
            return True

    def anchors_for(self, node_id: int) -> list[int]:
        """Return asset ids anchored to node."""
        return [int(a["asset_id"]) for a in self.anchors if a.get("node_id") == int(node_id)]

    def anchored_nodes(self, asset_id: int) -> list[int]:
        """Return exploration node ids anchored to asset."""
        return [int(a["node_id"]) for a in self.anchors if a.get("asset_id") == int(asset_id)]

    def list(self, kind: str = "", state: str = "") -> list[ExplorationNode]:
        """List nodes optionally filtered by kind/state."""
        items = list(self.nodes.values())
        if kind:
            items = [n for n in items if n.kind == kind]
        if state:
            items = [n for n in items if n.state == state]
        return sorted(items, key=lambda n: n.node_id)

    def children(self, node_id: int, kind: str = "") -> list[int]:
        """Return destination ids of outgoing edges."""
        out = [e.dst for e in self.edges if e.src == int(node_id)]
        if kind:
            out = [i for i in out if any(e.dst == i and e.kind == kind for e in self.edges)]
        return out

    def overview(self) -> dict:
        """Return planner-facing state summary like graph overview."""
        goals = [{"id": n.node_id, "state": n.state, "text": n.text[:400]} for n in self.list("goal")]
        intents = [{"id": n.node_id, "state": n.state, "text": n.text[:300], "priority": n.priority}
                   for n in self.list("intent")]
        facts = len(self.list("fact"))
        findings = len(self.list("finding"))
        hints = [{"id": n.node_id, "state": n.state, "text": n.text[:300]} for n in self.list("hint")]
        pending = [i for i in intents if i["state"] in ("pending", "open")]
        return {"goals": goals, "intents": intents, "pending": pending,
                "facts": facts, "findings": findings, "hints": hints,
                "nodes": len(self.nodes), "edges": len(self.edges), "anchors": len(self.anchors)}

    def reload(self) -> None:
        """Reload graph from disk, discarding in-memory state."""
        raw = _load_json(self._path, {"seq": 0, "nodes": [], "edges": [], "anchors": []})
        with self._lock:
            self._seq = int(raw.get("seq", 0))
            self.nodes = {}
            for item in raw.get("nodes", []):
                try:
                    node = ExplorationNode(**{k: v for k, v in item.items()
                                              if k in ExplorationNode.__dataclass_fields__})
                    self.nodes[node.node_id] = node
                except TypeError:
                    continue
            self.edges = []
            for item in raw.get("edges", []):
                try:
                    self.edges.append(ExplorationEdge(src=int(item["src"]),
                                                      dst=int(item["dst"]),
                                                      kind=str(item["kind"])))
                except (KeyError, ValueError, TypeError):
                    continue
            self.anchors = [a for a in raw.get("anchors", []) if isinstance(a, dict)]

    def compare_and_claim(self, node_id: int) -> bool:
        """CAS claim: reload, verify still open, then mark running. Cross-process safe."""
        lock_path = self._path.with_suffix(".lock")
        try:
            import fcntl as _fcntl
            with lock_path.open("w") as lock:
                try:
                    _fcntl.flock(lock.fileno(), _fcntl.LOCK_EX)
                except OSError:
                    pass
                self.reload()
                node = self.nodes.get(int(node_id))
                if node is None or node.kind != "intent":
                    return False
                if node.state not in INTENT_OPEN_STATES:
                    return False
                node.state = "running"
                node.updated = _now()
                self._persist()
                return True
        except OSError:
            self.reload()
            node = self.nodes.get(int(node_id))
            if node is None or node.state not in INTENT_OPEN_STATES:
                return False
            return self.set_state(node.node_id, "running")

    def finding_signature(self, text: str) -> str:
        """Normalize finding text into dedupe signature."""
        norm = re.sub(r"[^a-z0-9]+", " ", (text or "").lower())
        norm = re.sub(r"\s+", " ", norm).strip()
        return hashlib.sha256(norm.encode()).hexdigest()[:16]

    def has_finding(self, text: str) -> ExplorationNode | None:
        """Return existing finding with same signature or None."""
        sig = self.finding_signature(text)
        for node in self.list("finding"):
            if self.finding_signature(node.text) == sig:
                return node
            if str(node.meta.get("sig", "")) == sig and sig:
                return node
        return None

    def node_detail(self, node_id: int) -> dict:
        """Full node view: text, state, meta, edges, anchors, trace tail."""
        node = self.get(int(node_id))
        if node is None:
            raise KeyError(f"unknown node: {node_id}")
        return {"id": node.node_id, "kind": node.kind, "state": node.state,
                "text": node.text, "priority": node.priority, "meta": dict(node.meta),
                "children": self.children(node.node_id),
                "anchors": self.anchors_for(node.node_id)}

    def list_facts(self, query: str = "", limit: int = 50, hot_full: bool = False) -> list[ExplorationNode]:
        """Keyword-filtered facts like list_facts.

        Hot facts are never truncated when ``hot_full`` is set: the full
        hot set returns regardless of ``limit`` (cold views stay capped).
        """
        items = self.list("fact")
        if query:
            needle = query.lower()
            items = [n for n in items if needle in n.text.lower()]
        if hot_full:
            return [n for n in items if not n.meta.get("cold")
                    and n.state != "exhausted" and not n.meta.get("cold_digest")]
        return items[-max(1, limit):]

    def record_fact(self, text: str, evidence: str = "", confidence: str = "observed",
                    intent_id: int = 0, asset_ids: list[int] | None = None) -> ExplorationNode:
        """Worker fact write like recordFact: deduped, anchored, done."""
        node = self.add_node("fact", text[:600], state="done",
                             meta={"evidence": (evidence or "")[:1500],
                                   "confidence": confidence, "intent": int(intent_id)})
        if intent_id:
            self.add_edge(int(intent_id), node.node_id, "yields")
        for asset_id in asset_ids or []:
            self.anchor(node.node_id, int(asset_id))
        return node


class Frontier:
    """Pending-intent queue; workers claim exactly one intent each."""

    def __init__(self, graph: ExplorationGraph) -> None:
        """Bind frontier to a task graph."""
        self.graph = graph
        self._lock = threading.Lock()

    def pending(self) -> list[ExplorationNode]:
        """Return pending intents ordered by priority then id."""
        items = [n for n in self.graph.list("intent") if n.state in INTENT_OPEN_STATES]
        return sorted(items, key=lambda n: (-n.priority, n.node_id))

    def claim_next(self) -> ExplorationNode | None:
        """Atomically claim highest-priority pending intent (cross-process CAS)."""
        with self._lock:
            self.graph.reload()
            items = self.pending()
            if not items:
                return None
            node = items[0]
            if self.graph.compare_and_claim(node.node_id):
                self.graph.reload()
                claimed = self.graph.get(node.node_id)
                return claimed or node
            return None

    def release(self, node_id: int, state: str = "pending") -> bool:
        """Return a running intent to a new state."""
        return self.graph.set_state(int(node_id), state)


class ActivityLog:
    """Per-step worker/planner trace, backing trace exchange."""

    def __init__(self, task_id: str) -> None:
        """Bind log to task."""
        self.task_id = task_id
        self._path = _store_path(f"activity_{task_id}.jsonl")

    def emit(self, worker: str, kind: str, text: str, intent_id: int = 0) -> dict:
        """Append one activity record and return it."""
        record = {"ts": _now(), "task": self.task_id, "worker": worker,
                  "kind": kind, "text": text[:4000], "intent_id": int(intent_id)}
        with self._path.open("a") as handle:
            handle.write(json.dumps(record, ensure_ascii=False) + "\n")
        return record

    def read(self, limit: int = 200) -> list[dict]:
        """Return most recent records up to limit."""
        try:
            lines = self._path.read_text().splitlines()
        except OSError:
            return []
        out = []
        for line in lines[-max(1, limit):]:
            try:
                out.append(json.loads(line))
            except ValueError:
                continue
        return out

    def for_intent(self, intent_id: int) -> list[dict]:
        """Return records for one intent."""
        return [r for r in self.read(2000) if int(r.get("intent_id", 0)) == int(intent_id)]

    def search(self, query: str, exclude_intent: int = 0) -> list[dict]:
        """Search worker traces by keyword, excluding one intent like the planner."""
        needle = (query or "").lower()
        if not needle:
            return []
        hits = []
        for record in self.read(2000):
            if exclude_intent and int(record.get("intent_id", 0)) == int(exclude_intent):
                continue
            if needle in str(record.get("text", "")).lower():
                hits.append(record)
        return hits[:50]


class TrafficLog:
    """Append-only record of every tool execution like the Lazy MITM proxy."""

    def __init__(self, task_id: str = "") -> None:
        """Bind log to task or global stream."""
        name = f"traffic_{task_id}.jsonl" if task_id else "traffic.jsonl"
        self._path = _store_path(name)

    def record(self, kind: str, command: str, output: str = "", meta: dict | None = None) -> dict:
        """Append one traffic record and return it."""
        digest = hashlib.sha256((command or "").encode()).hexdigest()[:12]
        body = (output or "")
        truncated = len(body) > TRAFFIC_INLINE_CUTOFF
        stored = body[:TRAFFIC_INLINE_CUTOFF]
        record = {"ts": _now(), "kind": kind if kind in TRAFFIC_KINDS else "bash",
                  "command": (command or "")[:2000], "output": stored[:4000],
                  "preview": stored[:TRAFFIC_PREVIEW],
                  "truncated": truncated, "bytes": len(body),
                  "digest": digest, "template": _traffic_template(command or ""),
                  "meta": dict(meta or {})}
        with self._path.open("a") as handle:
            handle.write(json.dumps(record, ensure_ascii=False) + "\n")
        return record

    def read(self, limit: int = 100) -> list[dict]:
        """Return most recent traffic records."""
        try:
            lines = self._path.read_text().splitlines()
        except OSError:
            return []
        out = []
        for line in lines[-max(1, limit):]:
            try:
                out.append(json.loads(line))
            except ValueError:
                continue
        return out

    def search(self, query: str, limit: int = 50) -> list[dict]:
        """Full-text search over command/output like traffic_search."""
        needle = (query or "").lower()
        if not needle:
            return []
        return [r for r in self.read(2000)
                if needle in str(r.get("command", "")).lower()
                or needle in str(r.get("output", "")).lower()][: max(1, limit)]

    def get(self, digest: str) -> dict | None:
        """Fetch one exchange by digest like traffic_get."""
        for record in self.read(2000):
            if record.get("digest") == digest:
                return record
        return None

    def templates(self, limit: int = 50) -> list[dict]:
        """Group exchanges by URL-template with counts like the proxy index."""
        groups: dict[str, int] = {}
        for record in self.read(2000):
            key = str(record.get("template") or record.get("command", ""))[:200]
            groups[key] = groups.get(key, 0) + 1
        ranked = sorted(groups.items(), key=lambda kv: -kv[1])[: max(1, limit)]
        return [{"template": key, "count": count} for key, count in ranked]

    def by_template(self, template: str, limit: int = 50) -> list[dict]:
        """Return exchanges matching one template substring."""
        needle = (template or "").lower()
        return [r for r in self.read(2000)
                if needle in str(r.get("template", "")).lower()][: max(1, limit)]

    def bind(self, finding_id: int, digest: str, graph=None) -> bool:
        """Attach traffic digest to a finding like bind_finding_traffic."""
        if graph is None:
            return False
        node = graph.get(int(finding_id))
        if node is None or node.kind != "finding":
            return False
        refs = node.meta.setdefault("traffic_refs", [])
        if digest not in refs:
            refs.append(digest)
        graph._persist()
        return True

    def export(self, path: str, limit: int = 500) -> str:
        """Dump recent exchanges to a JSON file like traffic archive export."""
        dest = Path(path)
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(json.dumps(self.read(limit), indent=2, ensure_ascii=False))
        return str(dest)

    def archive(self, label: str = "") -> str:
        """Snapshot traffic stream into sessions/lazy/traffic_archive_*."""
        dest = _store_path(f"traffic_archive_{self._path.stem}_{label or int(_now())}.json")
        dest.write_text(json.dumps(self.read(2000), indent=2, ensure_ascii=False))
        return str(dest)

    def clear(self) -> int:
        """Drop the traffic stream, returning the discarded record count."""
        count = len(self.read(2000))
        try:
            self._path.write_text("")
        except OSError:
            return 0
        return count


class Guard:
    """Safety boundary: audit log plus user-configured intercept rules."""

    def __init__(self, task_id: str = "") -> None:
        """Load rules and audit trail."""
        suffix = f"_{task_id}" if task_id else ""
        self._rules_path = _store_path(f"guard_rules{suffix}.json")
        self._audit_path = _store_path(f"guard_audit{suffix}.jsonl")
        raw = _load_json(self._rules_path, {"rules": [
            {"pattern": r"rm\s+-rf\s+/( |$)", "action": "deny", "reason": "destructive root wipe"},
            {"pattern": r"mkfs|dd\s+.*of=/dev/", "action": "deny", "reason": "disk destruction"},
            {"pattern": r"curl.*\|\s*(sh|bash)", "action": "ask", "reason": "remote code execution pipe"},
            {"pattern": r"exfil|upload.*http", "action": "ask", "reason": "possible exfiltration"},
        ]})
        self.rules: list[dict] = raw.get("rules", [])

    def _persist(self) -> None:
        """Persist rule set."""
        _save_json(self._rules_path, {"rules": self.rules})

    def add_rule(self, pattern: str, action: str, reason: str = "", priority: int = 0) -> dict:
        """Register an intercept rule; higher priority evaluates first."""
        if action not in GUARD_ACTIONS:
            raise ValueError(f"action must be one of {GUARD_ACTIONS}")
        re.compile(pattern)
        rule = {"pattern": pattern, "action": action, "reason": reason or pattern,
                "priority": int(priority)}
        self.rules.append(rule)
        self.rules.sort(key=lambda r: -int(r.get("priority", 0)))
        self._persist()
        return rule

    def remove_rule(self, pattern: str) -> bool:
        """Delete rules matching pattern exactly."""
        before = len(self.rules)
        self.rules = [r for r in self.rules if r.get("pattern") != pattern]
        if len(self.rules) != before:
            self._persist()
            return True
        return False

    def check(self, tool: str, command: str) -> dict:
        """Evaluate tool call and audit it, returning allow/ask/deny."""
        decision: dict = {"tool": tool, "action": "allow", "reason": "", "command": command[:500]}
        for rule in self.rules:
            try:
                if re.search(rule.get("pattern", ""), command or ""):
                    decision = {"tool": tool, "action": rule.get("action", "allow"),
                                "reason": rule.get("reason", ""), "command": command[:500]}
                    break
            except re.error:
                continue
        with self._audit_path.open("a") as handle:
            handle.write(json.dumps({"ts": _now(), **decision}, ensure_ascii=False) + "\n")
        return decision

    def audit(self, limit: int = 100) -> list[dict]:
        """Return recent audit entries."""
        try:
            lines = self._audit_path.read_text().splitlines()
        except OSError:
            return []
        out = []
        for line in lines[-max(1, limit):]:
            try:
                out.append(json.loads(line))
            except ValueError:
                continue
        return out

    def stats(self) -> dict:
        """Attribution counters over the audit trail."""
        counts = {"allow": 0, "ask": 0, "deny": 0}
        for entry in self.audit(limit=2000):
            action = str(entry.get("action", ""))
            if action in counts:
                counts[action] += 1
        return counts


ASSET_GATE_KINDS = ("exact_domain", "exact_ip", "exact_url",
                    "fuzzy_domain", "fuzzy_ip", "fuzzy_url", "cidr")


def _asset_candidates(target: str) -> tuple[list[str], list[str], list[str]]:
    """Split a target into domain/ip/url candidate lists for gate matching."""
    text = (target or "").strip()
    domains, ips, urls = [], [], []
    if not text:
        return domains, ips, urls
    if text.lower().startswith("http"):
        urls.append(text)
        host = re.sub(r"^https?://", "", text).split("/")[0].split(":")[0].strip()
        if re.match(r"^(?:\d+\.)+\d+$", host or ""):
            ips.append(host)
        elif host:
            domains.append(host.lower())
        return domains, ips, urls
    if re.match(r"^(?:\d{1,3}\.){3}\d{1,3}(?:/\d{1,2})?$", text):
        ips.append(text.split("/")[0])
        return domains, ips, urls
    domains.append(text.lower())
    return domains, ips, urls


def _match_gate_rule(rule: dict, target: str) -> bool:
    """Return True when one enabled gate rule hits the target asset."""
    import ipaddress as _ip

    pattern = str(rule.get("pattern", "") or "").strip()
    if not pattern or not rule.get("enabled", True):
        return False
    kind = str(rule.get("kind", ""))
    domains, ips, urls = _asset_candidates(target)
    if kind == "exact_domain":
        return any(d == pattern.lower() for d in domains)
    if kind == "exact_ip":
        return any(ip == pattern for ip in ips)
    if kind == "exact_url":
        return any(u == pattern for u in urls)
    if kind == "fuzzy_domain":
        return any(pattern.lower() in d for d in domains if d)
    if kind == "fuzzy_ip":
        return any(pattern in ip for ip in ips if ip)
    if kind == "fuzzy_url":
        return any(pattern.lower() in u.lower() for u in urls if u)
    if kind == "cidr":
        try:
            net = _ip.ip_network(pattern, strict=False)
        except ValueError:
            return False
        for ip in ips:
            try:
                if _ip.ip_address(ip) in net:
                    return True
            except ValueError:
                continue
    return False


class AssetGate:
    """Target-asset gate: global blocklist + per-task block/allow lists.

    Enforcement order: global block hit denies; task block hit denies;
    non-empty task allow-list without hit denies (closed whitelist);
    otherwise allows. Checked on asset insert, intent inject and every
    worker target before tools run.
    """

    def __init__(self, task_id: str = "") -> None:
        """Bind global list plus optional per-task lists."""
        self.task_id = task_id
        self._global_path = _store_path("asset_gate.json")
        suffix = f"_{task_id}" if task_id else ""
        self._task_path = _store_path(f"asset_gate{suffix}.json") if task_id else None

    def _load_global(self) -> list[dict]:
        """Return global block rules."""
        return list(_load_json(self._global_path, {"block": []}).get("block", []))

    def _load_task(self) -> dict:
        """Return per-task block/allow payload."""
        if self._task_path is None:
            return {"block": [], "allow": []}
        payload = _load_json(self._task_path, {"block": [], "allow": []})
        return {"block": list(payload.get("block", [])),
                "allow": list(payload.get("allow", []))}

    def _save_global(self, block: list[dict]) -> None:
        """Persist global block rules."""
        _save_json(self._global_path, {"block": block})

    def _save_task(self, payload: dict) -> None:
        """Persist per-task block/allow rules."""
        if self._task_path is not None:
            _save_json(self._task_path, payload)

    def add(self, kind: str, pattern: str, note: str = "",
            action: str = "block") -> dict:
        """Register a block (global or task) or allow (task only) rule."""
        if kind not in ASSET_GATE_KINDS:
            raise ValueError(f"kind must be one of {ASSET_GATE_KINDS}")
        if action not in ("block", "allow"):
            raise ValueError("action must be block|allow")
        if action == "allow" and not self.task_id:
            raise ValueError("allow rules require a task (pass --task T)")
        if action == "block" and not self.task_id:
            block = self._load_global()
            rule = {"id": len(block) + 1, "enabled": True, "kind": kind,
                    "pattern": pattern[:300], "note": note[:200]}
            block.append(rule)
            self._save_global(block)
            return rule
        payload = self._load_task()
        bucket = payload["allow"] if action == "allow" else payload["block"]
        rule = {"id": len(bucket) + 1, "enabled": True, "kind": kind,
                "pattern": pattern[:300], "note": note[:200]}
        bucket.append(rule)
        self._save_task(payload)
        return rule

    def remove(self, rule_id: int, action: str = "block") -> bool:
        """Delete a rule by id; returns True when something was removed."""
        if action == "block" and not self.task_id:
            block = self._load_global()
            kept = [r for r in block if int(r.get("id", 0)) != int(rule_id)]
            if len(kept) != len(block):
                self._save_global(kept)
                return True
            return False
        payload = self._load_task()
        bucket = payload["allow"] if action == "allow" else payload["block"]
        kept = [r for r in bucket if int(r.get("id", 0)) != int(rule_id)]
        if len(kept) != len(bucket):
            payload[action] = kept
            self._save_task(payload)
            return True
        return False

    def list(self) -> dict:
        """Return global block plus per-task block/allow rules."""
        return {"global_block": self._load_global(), **self._load_task()}

    def evaluate(self, target: str) -> dict:
        """Gate one target: allowed flag plus human-readable reason."""
        for rule in self._load_global():
            if _match_gate_rule(rule, target):
                return {"allowed": False,
                        "reason": f"asset gate [global:{rule['kind']}:{rule['pattern']}]"}
        task = self._load_task()
        for rule in task["block"]:
            if _match_gate_rule(rule, target):
                return {"allowed": False,
                        "reason": f"asset gate [task:{rule['kind']}:{rule['pattern']}]"}
        if any(r.get("enabled", True) for r in task["allow"]):
            if not any(_match_gate_rule(r, target) for r in task["allow"]):
                return {"allowed": False,
                        "reason": "asset gate: outside task allow-list"}
        return {"allowed": True, "reason": ""}


class Budget:
    """Three-level budget: rounds, toolcalls, findings, task deadline."""

    def __init__(self, store=None) -> None:
        """Bind budget counters to task store."""
        self._store = store

    def limits(self, task_id: str) -> dict:
        """Return effective limits for task."""
        record = (self._store.get(task_id) or {}) if self._store else {}
        budget = record.get("budget", {}) or {}
        return {
            "max_rounds": int(budget.get("max_rounds", DEFAULT_MAX_ROUNDS)),
            "max_toolcalls": int(budget.get("max_toolcalls", DEFAULT_MAX_TOOLCALLS)),
            "max_findings": int(budget.get("max_findings", DEFAULT_MAX_FINDINGS)),
            "timeout_sec": float(budget.get("timeout_sec", 0.0)),
        }

    def set_limits(self, task_id: str, **kwargs) -> dict:
        """Persist budget limits for task."""
        if self._store is None:
            return {}
        record = self._store.get(task_id) or {}
        budget = record.setdefault("budget", {})
        for key in ("max_rounds", "max_toolcalls", "max_findings", "timeout_sec"):
            if key in kwargs and kwargs[key] is not None:
                budget[key] = kwargs[key]
        record["updated"] = _now()
        self._store._persist()
        return self.limits(task_id)

    def usage(self, task_id: str) -> dict:
        """Return consumed toolcalls/findings/rounds."""
        record = (self._store.get(task_id) or {}) if self._store else {}
        used = record.get("used", {}) or {}
        return {
            "toolcalls": int(used.get("toolcalls", 0)),
            "findings": int(used.get("findings", 0)),
            "rounds": int(used.get("rounds", 0)),
        }

    def record_toolcall(self, task_id: str, intent_id: int = 0) -> None:
        """Count one executed tool call."""
        if self._store is None:
            return
        record = self._store.get(task_id)
        if record is None:
            return
        used = record.setdefault("used", {})
        used["toolcalls"] = int(used.get("toolcalls", 0)) + 1
        record["updated"] = _now()
        self._store._persist()

    def record_round(self, task_id: str) -> None:
        """Count one orchestrator round."""
        if self._store is None:
            return
        record = self._store.get(task_id)
        if record is None:
            return
        used = record.setdefault("used", {})
        used["rounds"] = int(used.get("rounds", 0)) + 1
        findings = 0
        try:
            findings = len(ExplorationGraph(task_id).list("finding"))
        except Exception:
            findings = 0
        used["findings"] = findings
        record["updated"] = _now()
        self._store._persist()

    def check(self, task_id: str) -> dict:
        """Return ok/exceeded decision with reason."""
        limits = self.limits(task_id)
        used = self.usage(task_id)
        if self._store is not None and self._store.expired(task_id):
            return {"ok": False, "reason": "task deadline exceeded"}
        if used["toolcalls"] >= limits["max_toolcalls"]:
            return {"ok": False, "reason": f"toolcall budget {used['toolcalls']}/{limits['max_toolcalls']}"}
        if used["findings"] >= limits["max_findings"]:
            return {"ok": False, "reason": f"finding budget {used['findings']}/{limits['max_findings']}"}
        return {"ok": True, "reason": "", "used": used, "limits": limits}


class RuntimeTracker:
    """Observable runtime: abort cause, workers, heartbeat, watermarks."""

    def __init__(self, store=None) -> None:
        """Bind runtime to task store."""
        self._store = store

    def heartbeat(self, task_id: str) -> dict:
        """Return live runtime snapshot."""
        record = (self._store.get(task_id) or {}) if self._store else {}
        runtime = record.get("runtime", {}) or {}
        budget = Budget(self._store)
        return {
            "task_id": task_id,
            "status": record.get("status", "unknown"),
            "abort_cause": runtime.get("abort_cause", ""),
            "workers": int(runtime.get("workers", 0)),
            "started": float(runtime.get("started", 0.0) or 0.0),
            "last_beat": float(runtime.get("last_beat", 0.0) or 0.0),
            "deadline": float(record.get("deadline", 0.0) or 0.0),
            "budget": budget.limits(task_id),
            "used": budget.usage(task_id),
            "watermark": int((record.get("sched", {}) or {}).get("last_trigger", 0)),
        }

    def beat(self, task_id: str, workers: int = 0) -> None:
        """Stamp heartbeat."""
        if self._store is None:
            return
        record = self._store.get(task_id)
        if record is None:
            return
        runtime = record.setdefault("runtime", {})
        if not runtime.get("started"):
            runtime["started"] = _now()
        runtime["last_beat"] = _now()
        runtime["workers"] = int(workers)
        record["updated"] = _now()
        self._store._persist()

    def abort(self, task_id: str, cause: str, detail: str = "") -> bool:
        """Stamp abort cause like typed AbortCause."""
        if cause not in ABORT_CAUSES:
            raise ValueError(f"cause must be one of {ABORT_CAUSES}")
        if self._store is None:
            return False
        record = self._store.get(task_id)
        if record is None:
            return False
        runtime = record.setdefault("runtime", {})
        runtime["abort_cause"] = cause
        runtime["abort_detail"] = detail[:500]
        runtime["last_beat"] = _now()
        self._store._persist()
        return True

    def note_trigger(self, task_id: str, trigger_id: int) -> None:
        """Advance scheduler watermark so restarts never re-fire."""
        if self._store is None:
            return
        record = self._store.get(task_id)
        if record is None:
            return
        sched = record.setdefault("sched", {})
        sched["last_trigger"] = max(int(sched.get("last_trigger", 0)), int(trigger_id))
        self._store._persist()


class InterceptQueue:
    """Pending ask-queue with decide + timeout, priority ordered."""

    def __init__(self, task_id: str = "") -> None:
        """Bind queue to task."""
        self.task_id = task_id
        suffix = f"_{task_id}" if task_id else ""
        self._path = _store_path(f"intercept{suffix}.json")

    def _load(self) -> dict:
        """Load queue payload."""
        return _load_json(self._path, {"seq": 0, "items": []})

    def _save(self, payload: dict) -> None:
        """Persist queue payload."""
        _save_json(self._path, payload)

    def request(self, tool: str, command: str, reason: str = "") -> dict:
        """Enqueue one ask decision and return pending entry."""
        payload = self._load()
        seq = int(payload.get("seq", 0)) + 1
        payload["seq"] = seq
        item = {"id": seq, "tool": tool, "command": command[:2000],
                "reason": reason[:500], "state": "pending", "ts": _now()}
        payload.setdefault("items", []).append(item)
        self._save(payload)
        return item

    def pending(self) -> list[dict]:
        """Return pending entries ordered by id."""
        return sorted([i for i in self._load().get("items", [])
                       if i.get("state") == "pending"], key=lambda i: i["id"])

    def decide(self, item_id: int, verdict: str) -> bool:
        """Approve or deny one pending entry."""
        if verdict not in ("approved", "denied"):
            raise ValueError("verdict must be approved|denied")
        payload = self._load()
        for item in payload.get("items", []):
            if int(item.get("id", 0)) == int(item_id) and item.get("state") == "pending":
                item["state"] = verdict
                item["decided"] = _now()
                self._save(payload)
                return True
        return False

    def wait(self, item_id: int, timeout_sec: float = INTERCEPT_TIMEOUT_SEC) -> str:
        """Block until decided or timeout; timeout denies safely."""
        deadline = _now() + max(0.0, float(timeout_sec))
        while _now() < deadline:
            for item in self._load().get("items", []):
                if int(item.get("id", 0)) == int(item_id):
                    if item.get("state") in ("approved", "denied"):
                        return str(item["state"])
            time.sleep(0.2)
        payload = self._load()
        for item in payload.get("items", []):
            if int(item.get("id", 0)) == int(item_id) and item.get("state") == "pending":
                item["state"] = "denied"
                item["decided"] = _now()
                item["reason"] = (item.get("reason", "") + " [timeout->deny]")[:500]
                self._save(payload)
                break
        return "denied"


class TodoStore:
    """Per-task shared planner scratchpad for serial exploit chains."""

    def __init__(self, task_id: str) -> None:
        """Load persisted todos."""
        self.task_id = task_id
        self._path = _store_path(f"todos_{task_id}.json")
        raw = _load_json(self._path, {"items": []})
        self.items: list[dict] = raw.get("items", [])

    def _persist(self) -> None:
        """Persist todo list."""
        _save_json(self._path, {"items": self.items})

    def add(self, text: str) -> dict:
        """Append a serial step and return it."""
        item = {"id": len(self.items) + 1, "text": text.strip(), "state": "pending", "ts": _now()}
        self.items.append(item)
        self._persist()
        return item

    def complete(self, item_id: int) -> bool:
        """Mark step done."""
        for item in self.items:
            if int(item.get("id", 0)) == int(item_id):
                item["state"] = "done"
                self._persist()
                return True
        return False

    def next_pending(self) -> dict | None:
        """Return first pending step."""
        for item in self.items:
            if item.get("state") == "pending":
                return item
        return None

    def as_list(self) -> list[dict]:
        """Return all steps."""
        return list(self.items)


class TaskStore:
    """Registry of tasks, goals, constraints, hints, scope, findings."""

    def __init__(self) -> None:
        """Load task registry."""
        self._path = _store_path("tasks.json")
        self._raw = _load_json(self._path, {"seq": 0, "tasks": {}})

    def _persist(self) -> None:
        """Persist registry."""
        _save_json(self._path, self._raw)

    def create(self, goal: str, description: str = "") -> LazyTask:
        """Create task record and return it."""
        seq = int(self._raw.get("seq", 0)) + 1
        self._raw["seq"] = seq
        task_id = f"t{seq:04d}"
        task = LazyTask(task_id=task_id, goal=goal.strip(), description=description.strip())
        tasks = self._raw.setdefault("tasks", {})
        tasks[task_id] = {**asdict(task), "constraints": [], "scope": [], "steer": {}, "killed": []}
        self._persist()
        return task

    def get(self, task_id: str) -> dict | None:
        """Return raw task record or None."""
        return self._raw.get("tasks", {}).get(task_id)

    def list(self) -> list[dict]:
        """Return all task records."""
        return sorted(self._raw.get("tasks", {}).values(), key=lambda t: t.get("task_id", ""))

    def set_status(self, task_id: str, status: str) -> bool:
        """Update task status."""
        record = self.get(task_id)
        if record is None:
            return False
        if status not in TASK_STATUSES:
            raise ValueError(f"unknown status: {status}")
        record["status"] = status
        record["updated"] = _now()
        self._persist()
        return True

    def pause(self, task_id: str) -> bool:
        """Pause planner and workers like the planner Engine.Pause."""
        return self.set_status(task_id, "paused")

    def resume(self, task_id: str) -> bool:
        """Resume a paused task back to running like the planner resumeTask."""
        record = self.get(task_id)
        if record is None:
            return False
        if record.get("status") not in ("paused", "queued", "exhausted"):
            return True
        return self.set_status(task_id, "running")

    def delete(self, task_id: str) -> bool:
        """Remove task record; per-task graph files are cleaned by caller."""
        tasks = self._raw.get("tasks", {})
        if task_id not in tasks:
            return False
        del tasks[task_id]
        self._persist()
        return True

    def set_deadline(self, task_id: str, timeout_sec: float) -> bool:
        """Stamp absolute deadline like the planner deadline coordinator."""
        record = self.get(task_id)
        if record is None:
            return False
        record["deadline"] = _now() + max(0.0, float(timeout_sec)) if timeout_sec else 0.0
        record["updated"] = _now()
        self._persist()
        return True

    def expired(self, task_id: str) -> bool:
        """Report whether task deadline passed."""
        record = self.get(task_id) or {}
        deadline = float(record.get("deadline", 0.0) or 0.0)
        return bool(deadline) and _now() >= deadline

    def add_constraint(self, task_id: str, ctype: str, text: str) -> dict:
        """Register allow/deny operation constraint like the planner set_constraints."""
        if ctype not in CONSTRAINT_TYPES:
            raise ValueError(f"type must be one of {CONSTRAINT_TYPES}")
        record = self.get(task_id)
        if record is None:
            raise KeyError(f"unknown task: {task_id}")
        item = {"type": ctype, "text": text.strip(), "ts": _now()}
        record.setdefault("constraints", []).append(item)
        record["updated"] = _now()
        self._persist()
        return item

    def add_scope(self, task_id: str, kind: str, value: str, reason: str = "") -> dict:
        """Register authorized asset scope like the planner add_task_scope."""
        record = self.get(task_id)
        if record is None:
            raise KeyError(f"unknown task: {task_id}")
        item = {"kind": kind.strip(), "value": value.strip(), "reason": reason.strip(), "ts": _now()}
        record.setdefault("scope", []).append(item)
        record["updated"] = _now()
        self._persist()
        return item

    def steer(self, task_id: str, intent_id: int, message: str) -> bool:
        """Attach mid-run correction to a running intent like steer_work."""
        record = self.get(task_id)
        if record is None:
            return False
        record.setdefault("steer", {})[str(int(intent_id))] = {"msg": message, "ts": _now()}
        self._persist()
        return True

    def kill(self, task_id: str, intent_id: int) -> bool:
        """Flag a running intent for termination like kill_work."""
        record = self.get(task_id)
        if record is None:
            return False
        killed = record.setdefault("killed", [])
        if int(intent_id) not in killed:
            killed.append(int(intent_id))
        self._persist()
        return True

    def steer_for(self, task_id: str, intent_id: int) -> str:
        """Return pending steer message for intent if any."""
        record = self.get(task_id) or {}
        return str((record.get("steer", {}).get(str(int(intent_id)), {}) or {}).get("msg", ""))

    def killed(self, task_id: str, intent_id: int) -> bool:
        """Report whether intent was flagged for termination."""
        record = self.get(task_id) or {}
        return int(intent_id) in (record.get("killed", []) or [])


def extract_scope_items(goal_text: str, description: str = "") -> list[dict]:
    """Lift explicit asset scope from goal like the planner goalsScopeTail.

    Minimal-range principle: only what the operator literally named.
    Bare IP/CIDR wins over domains; full hostname wins over root domain.
    """
    text = f"{goal_text or ''} {description or ''}"
    items: list[dict] = []
    seen: set[tuple[str, str]] = set()
    for match in re.finditer(r"\b(?:\d{1,3}\.){3}\d{1,3}(?:/\d{1,2})?\b", text):
        value = match.group(0)
        kind = "cidr" if "/" in value else "ip"
        if (kind, value) not in seen:
            seen.add((kind, value))
            items.append({"kind": kind, "value": value, "reason": "explicit in goal"})
    for match in re.finditer(r"https?://([A-Za-z0-9.-]+)(?::\d+)?(?:/\S*)?", text):
        host = match.group(1).lower().strip(".")
        if host and ("root_domain", host) not in seen and ("subdomain", host) not in seen:
            kind = "root_domain" if host.count(".") == 1 else "subdomain"
            seen.add((kind, host))
            items.append({"kind": kind, "value": host, "reason": "explicit URL host in goal"})
    for match in re.finditer(r"\b(?:[A-Za-z0-9-]+\.)+(?:[a-z]{2,})\b", text.lower()):
        host = match.group(0).strip(".")
        if host and (("root_domain", host) not in seen) and (("subdomain", host) not in seen):
            if re.match(r"^(?:\d+\.)+\d+$", host):
                continue
            kind = "root_domain" if host.count(".") == 1 else "subdomain"
            seen.add((kind, host))
            items.append({"kind": kind, "value": host, "reason": "explicit hostname in goal"})
    return items[:5]


def extract_constraint_items(goal_text: str, description: str = "") -> list[dict]:
    """Lift explicit allow/deny operation bounds like the planner goals decomposer."""
    text = f"{goal_text or ''} {description or ''}".lower()
    items: list[dict] = []
    deny_marks = ("do not scan", "don't scan", "no port scan", "without port scan",
                  "no brute", "forbid", "prohibit", "passive only", "do not exploit",
                  "don't exploit", "no exploitation", "out of scope")
    allow_marks = ("only test", "only scan", "limited to", "in scope", "authorized")
    if any(mark in text for mark in deny_marks):
        items.append({"type": "deny", "text": "operator-limited operation from goal text"})
    for mark in allow_marks:
        if mark in text:
            items.append({"type": "allow", "text": f"operator scope bound: {mark}"})
            break
    return items


def load_intel_scores() -> dict:
    """Return host exposure scores from sessions/intel_summary.json.

    Written by the intel fusion view on every graph fetch; empty when
    the operator never opened IntelGraph. Never raises.
    """
    try:
        payload = _load_json(STORE_DIR.parent / "intel_summary.json", {})
        return {str(r.get("host", "")): float(r.get("score", 0.0))
                for r in payload.get("top_exposed", []) if r.get("host")}
    except Exception:
        return {}


def resolve_target(task_id: str, store=None, graph=None) -> str:
    """Resolve concrete target for worker commands from scope, assets, goal."""
    try:
        record = (store.get(task_id) or {}) if store is not None else {}
    except Exception:
        record = {}
    for item in record.get("scope", []) or []:
        value = str(item.get("value", "")).strip()
        if value:
            return value.split("/")[0]
    if graph is not None:
        try:
            for node in graph.list("goal"):
                for item in extract_scope_items(node.text):
                    return str(item["value"]).split("/")[0]
        except Exception:
            pass
    goal = str(record.get("goal", ""))
    for item in extract_scope_items(goal):
        return str(item["value"]).split("/")[0]
    return ""


def decompose_goals(goal_text: str, description: str = "") -> list[dict]:
    """Split goal text into verifiable objectives like the planner DecomposeGoals."""
    chunks = [c.strip(" .") for c in re.split(r"[;\n]+|\s+and\s+", goal_text or "") if c.strip()]
    if not chunks:
        chunks = [(goal_text or "assess target").strip()]
    try:
        from modules.lazy_loop import LlmPool as _Pool
        pool = _Pool()
        if pool.members() and len(chunks) == 1 and len(chunks[0]) > 20:
            hint = pool.complete(
                f"Split this pentest goal into short verifiable objectives, one per line, "
                f"no bullets:\n{(goal_text or '')[:800]}", max_tokens=300) or ""
            lines = [re.sub(r"^[\d\-\*\.\#\)\s]+", "", ln).strip()
                     for ln in hint.splitlines() if ln.strip()]
            lines = [ln for ln in lines if len(ln) > 3][:5]
            if len(lines) >= 2:
                chunks = lines
    except Exception:
        pass
    specs = []
    for chunk in chunks[:5]:
        vulnclass = ""
        lowered = chunk.lower()
        for candidate in ("sqli", "xss", "rce", "lfi", "ssrf", "idor", "privesc", "persistence"):
            if candidate in lowered:
                vulnclass = candidate
                break
        specs.append({"text": chunk[:300], "vulnclass": vulnclass})
    _ = description
    return specs


def enrich_asset(value: str) -> dict:
    """Synchronously enrich one asset with DNS and HTTP like the planner enrich."""
    result: dict = {"value": value, "dns": [], "http": {}}
    host = re.sub(r"^https?://", "", value or "").split("/")[0].split(":")[0].strip()
    if host:
        try:
            _, _, addresses = socket.gethostbyname_ex(host)
            result["dns"] = addresses[:8]
        except OSError:
            result["dns"] = []
        try:
            request = urllib.request.Request(f"http://{host}", method="HEAD")
            with urllib.request.urlopen(request, timeout=8) as response:
                result["http"] = {"status": response.status,
                                  "server": response.headers.get("Server", ""),
                                  "title": response.headers.get("X-Powered-By", "")}
        except Exception:
            result["http"] = {}
    return result


class Planner:
    """Sole intent generator, woken on every graph change like the planner planner."""

    def __init__(self, task_id: str, assets: AssetGraph, graph: ExplorationGraph,
                 activity: ActivityLog, store: TaskStore) -> None:
        """Bind planner to task collaborators."""
        self.task_id = task_id
        self.assets = assets
        self.graph = graph
        self.activity = activity
        self.store = store
        self.todos = TodoStore(task_id)

    def _constraints(self) -> list[dict]:
        """Return task constraints."""
        record = self.store.get(self.task_id) or {}
        return list(record.get("constraints", []))

    def _denied(self, text: str) -> str:
        """Return matching deny constraint text or empty string."""
        lowered = (text or "").lower()
        for item in self._constraints():
            if item.get("type") == "deny" and item.get("text", "").lower() in lowered:
                return str(item.get("text"))
        return ""

    def plan(self, triggers: list[dict] | None = None) -> list[ExplorationNode]:
        """Emit 0..N intents from current situation; most wakeups emit zero.

        Faithful to Lazy planner: stall-guard forces at least one intent
        when goals are unmet and nothing is open/running; goalless tasks
        never enter the planner; deny constraints block candidates.
        """
        record = self.store.get(self.task_id) or {}
        if record.get("status") == "paused":
            return []
        if self.store.expired(self.task_id):
            self.store.set_status(self.task_id, "timeout")
            return []
        goals = self.graph.list("goal")
        if goals and all(g.state == "done" for g in goals):
            return []
        if not goals:
            intents = self.graph.list("intent")
            active = [n for n in intents if n.state in ("pending", "open", "running")]
            if not active:
                self.store.set_status(self.task_id, "done")
            return []
        existing = {n.text for n in self.graph.list("intent")}
        created: list[ExplorationNode] = []
        candidates = self._candidates()
        candidates.extend(self._llm_candidates(existing))
        for summary, asset_ids, parents, priority in candidates:
            if summary in existing:
                continue
            denied = self._denied(summary)
            if denied:
                self.activity.emit("planner", "skip",
                                   f"blocked by deny constraint '{denied}': {summary}")
                continue
            node = self.graph.add_node("intent", summary, priority=priority)
            origin = self._origin_fact()
            self.graph.add_edge(origin, node.node_id, "spawns")
            for parent in parents:
                self.graph.add_edge(parent, node.node_id, "derived_from")
            for asset_id in asset_ids:
                self.graph.anchor(node.node_id, asset_id)
            created.append(node)
            self.activity.emit("planner", "intent", f"#{node.node_id} {summary}", intent_id=node.node_id)
            if len(created) >= MAX_INTENTS_PER_ROUND:
                break
        if triggers:
            brief = "; ".join(str(t.get("kind", t)) for t in triggers[:5])[:300]
            self.activity.emit("planner", "trigger", f"round fired by: {brief}")
        if not created:
            active = [n for n in self.graph.list("intent")
                      if n.state in ("pending", "open", "running")]
            if active:
                return []
            stall = self._stall_intent(existing)
            if stall is not None:
                summary, asset_ids, parents, priority = stall
                node = self.graph.add_node("intent", summary, priority=priority)
                origin = self._origin_fact()
                self.graph.add_edge(origin, node.node_id, "spawns")
                for parent in parents:
                    self.graph.add_edge(parent, node.node_id, "derived_from")
                for asset_id in asset_ids:
                    self.graph.anchor(node.node_id, asset_id)
                self.activity.emit("planner", "intent",
                                   f"stall-guard #{node.node_id} {summary}",
                                   intent_id=node.node_id)
                created.append(node)
        return created

    def _origin_fact(self) -> int:
        """Return origin fact id, creating it once."""
        facts = self.graph.list("fact")
        for node in facts:
            if node.meta.get("origin"):
                return node.node_id
        node = self.graph.add_node("fact", "task origin", state="done", meta={"origin": True})
        return node.node_id

    def _candidates(self) -> list[tuple[str, list[int], list[int], int]]:
        """Build candidate intents from serial todos, hints, coverage, findings."""
        out: list[tuple[str, list[int], list[int], int]] = []
        record = self.store.get(self.task_id) or {}
        scope = record.get("scope", []) or []
        step = self.todos.next_pending()
        if step:
            satisfied = any(step["text"][:30].lower() in n.text.lower()
                            for n in self.graph.list("fact") if n.state == "done")
            if satisfied:
                self.todos.complete(int(step["id"]))
                step = self.todos.next_pending()
            if step:
                facts = [n.node_id for n in self.graph.list("fact") if n.state == "done"][-3:]
                scoped = [a.asset_id for a in self.assets.untested_for(self.graph, scope, limit=2)]
                out.append((f"advance serial chain: {step['text']}", scoped, facts, 9))
                return out
        for hint in self.graph.list("hint", "pending"):
            out.append((f"steered probe: {hint.text}", self.graph.anchors_for(hint.node_id), [], 8))
            self.graph.set_state(hint.node_id, "done")
        for asset in self.assets.untested_for(self.graph, scope, limit=MAX_INTENTS_PER_ROUND):
            out.append((f"probe {asset.kind} {asset.value}", [asset.asset_id], [], 6))
        try:
            scores = load_intel_scores()
        except Exception:
            scores = {}
        if scores:
            boosted = []
            for summary, asset_ids, parents, priority in out:
                bonus = 0
                for asset_id in asset_ids:
                    asset = self.assets.get(asset_id)
                    if asset is not None and asset.value in scores:
                        bonus = max(bonus, min(4, int(scores[asset.value] / 10)))
                boosted.append((summary, asset_ids, parents, min(10, priority + bonus)))
            out = boosted
            self.activity.emit("planner", "intel",
                               f"exposure-ranked {len(out)} candidates from intel_summary")
        for finding in self.graph.list("finding")[-2:]:
            out.append((f"extend finding: {finding.text[:120]}", self.graph.anchors_for(finding.node_id),
                        [finding.node_id], 7))
        if not out and not self.graph.list("intent"):
            target = resolve_target(self.task_id, self.store, self.graph)
            out.append((f"baseline recon: enumerate {target or 'target surface'}",
                        [], [], DEFAULT_PRIORITY))
        try:
            from modules.auto_registry import propose_intents as _auto_intents
            from modules.finding_lifecycle import suppressed_values as _suppressed
            goal_text = str(record.get("goal", "") or "")
            auto_target = resolve_target(self.task_id, self.store, self.graph) or ""
            try:
                suppressed = set(_suppressed())
            except Exception:
                suppressed = set()
            if not any(val and val in auto_target for val in suppressed):
                finding_texts = tuple(
                    n.text for n in self.graph.list("finding")[-4:]
                    if not any(val and val in n.text for val in suppressed))
                for summary in _auto_intents(goal_text, auto_target, finding_texts):
                    out.append((summary, [], [], 7))
        except Exception:
            pass
        return out

    def _llm_candidates(self, existing: set[str]) -> list[tuple[str, list[int], list[int], int]]:
        """Ask the configured LLM chain for extra intents; empty without members."""
        try:
            from modules.lazy_loop import LlmPool as _Pool
            pool = _Pool()
            if not pool.members():
                return []
            record = self.store.get(self.task_id) or {}
            overview = json.dumps(self.graph.overview(), ensure_ascii=False)[:2000]
            prompt = (f"Goal: {(record.get('goal', ''))[:300]}\nOverview: {overview}\n"
                      f"Constraints: {constraint_block(record.get('constraints', []))[:400]}\n"
                      "Propose up to 3 next probe intents, one per line, no bullets.")
            reply = pool.complete(prompt, max_tokens=400) or ""
        except Exception:
            return []
        out: list[tuple[str, list[int], list[int], int]] = []
        for line in reply.splitlines():
            summary = re.sub(r"^[\d\-\*\.\#\)\s]+", "", line).strip()[:200]
            if len(summary) < 8 or summary in existing:
                continue
            if self._denied(summary):
                continue
            out.append((summary, [], [], 6))
            if len(out) >= 2:
                break
        if out:
            try:
                self.activity.emit("planner", "llm", f"LLM proposed {len(out)} intents")
            except Exception:
                pass
        return out

    def _stall_intent(self, existing: set[str]) -> tuple[str, list[int], list[int], int] | None:
        """Force one forward intent when exploration stalled like the planner.

        Fires only when goals are unmet and no intent is open/running.
        Prefers an untested scoped asset, else re-drives the most recent
        done intent with a new mechanism, else a scoped baseline probe.
        """
        record = self.store.get(self.task_id) or {}
        scope = record.get("scope", []) or []
        for asset in self.assets.untested_for(self.graph, scope, limit=4):
            summary = f"probe {asset.kind} {asset.value}"
            if summary not in existing:
                return summary, [asset.asset_id], [], 6
        done = [n for n in self.graph.list("intent") if n.state == "done"]
        if done:
            last = done[-1]
            summary = f"re-drive with new mechanism: {last.text[:120]}"
            if summary not in existing:
                return summary, self.graph.anchors_for(last.node_id), [last.node_id], 6
        target = resolve_target(self.task_id, self.store, self.graph) or "target"
        summary = f"baseline recon: enumerate {target}"
        if summary not in existing:
            return summary, [], [], DEFAULT_PRIORITY
        return None

    def _scope_allows(self, asset: AssetNode) -> bool:
        """Check asset against explicit task scope when present."""
        record = self.store.get(self.task_id) or {}
        scope = record.get("scope", []) or []
        if not scope:
            return True
        return any(s.get("value", "").lower() in asset.value.lower() for s in scope)


class Worker:
    """Executes exactly ONE claimed intent with real tools."""

    def __init__(self, name: str, task_id: str, assets: AssetGraph, graph: ExplorationGraph,
                 activity: ActivityLog, traffic: TrafficLog, guard: Guard, store: TaskStore) -> None:
        """Bind worker to task collaborators."""
        self.name = name
        self.task_id = task_id
        self.assets = assets
        self.graph = graph
        self.activity = activity
        self.traffic = traffic
        self.guard = guard
        self.store = store

    def _scope_allows_target(self, target: str) -> bool:
        """Enforce explicit scope: targets outside scope are blocked."""
        try:
            gate = AssetGate(self.task_id).evaluate(target or "")
            if not gate["allowed"]:
                self.activity.emit(self.name, "block",
                                   f"asset-gate: {target} {gate['reason']}",
                                   intent_id=0)
                return False
        except Exception:
            pass
        try:
            from modules.intercept import scope_blocked as _blocked
            if _blocked(target or ""):
                self.activity.emit(self.name, "block",
                                   f"scope-deny-global: {target} matches protected suffix",
                                   intent_id=0)
                return False
        except Exception:
            pass
        record = self.store.get(self.task_id) or {}
        scope = record.get("scope", []) or []
        if not scope:
            return True
        lowered = (target or "").lower()
        for item in scope:
            value = str(item.get("value", "")).lower()
            if value and (value in lowered or lowered in value):
                return True
            if item.get("kind") == "cidr" and value:
                return True
        return False

    def execute(self, intent: ExplorationNode, executor=None,
                timeout_sec: float = 0.0) -> dict:
        """Run one intent to completion and write facts back."""
        outcome: dict = {"intent_id": intent.node_id, "worker": self.name,
                         "facts": 0, "assets": 0, "findings": 0, "state": "done"}
        budget = Budget(self.store)
        steps = self._steps_for(intent)
        model_errors = 0
        transcripts: list[tuple[str, str]] = []
        intercept = InterceptQueue(self.task_id)
        deadline = (_now() + float(timeout_sec)) if timeout_sec else 0.0
        for index, command in enumerate(steps[:MAX_WORKER_STEPS], start=1):
            if deadline and _now() >= deadline:
                self.activity.emit(self.name, "timeout",
                                   f"intent #{intent.node_id} timed out at step {index}; settling partial",
                                   intent_id=intent.node_id)
                RuntimeTracker(self.store).abort(self.task_id, "timeout",
                                                 f"intent #{intent.node_id} step {index}")
                outcome["state"] = "stopped"
                break
            if (self.store.get(self.task_id) or {}).get("status") == "paused":
                self.graph.set_state(intent.node_id, "pending")
                self.activity.emit(self.name, "pause",
                                   f"intent #{intent.node_id} yielded on pause (cancel, re-queue)",
                                   intent_id=intent.node_id)
                RuntimeTracker(self.store).abort(self.task_id, "paused",
                                                 f"intent #{intent.node_id} step {index}")
                outcome["state"] = "stopped"
                return outcome
            if self.store.killed(self.task_id, intent.node_id):
                self.graph.set_state(intent.node_id, "stopped")
                self.activity.emit(self.name, "kill", f"intent #{intent.node_id} terminated",
                                   intent_id=intent.node_id)
                outcome["state"] = "stopped"
                return outcome
            if not budget.check(self.task_id)["ok"]:
                self.graph.set_state(intent.node_id, "pending")
                self.activity.emit(self.name, "budget",
                                   f"intent #{intent.node_id} yielded: "
                                   f"{budget.check(self.task_id)['reason']}",
                                   intent_id=intent.node_id)
                RuntimeTracker(self.store).abort(self.task_id, "budget",
                                                 budget.check(self.task_id)["reason"])
                outcome["state"] = "blocked"
                return outcome
            steer = self.store.steer_for(self.task_id, intent.node_id)
            if steer:
                self.activity.emit(self.name, "steer", f"course correction: {steer}",
                                   intent_id=intent.node_id)
            target = self._target_for(intent)
            if target and not self._scope_allows_target(target):
                self.activity.emit(self.name, "block",
                                   f"scope-enforce: target {target} outside authorized scope",
                                   intent_id=intent.node_id)
                outcome["state"] = "blocked"
                continue
            decision = self.guard.check("Bash", command)
            self.activity.emit(self.name, "tool", f"[{decision['action']}] {command[:200]}",
                               intent_id=intent.node_id)
            if decision["action"] == "deny":
                self.activity.emit(self.name, "block", decision.get("reason", "denied"),
                                   intent_id=intent.node_id)
                continue
            if decision["action"] == "ask" and not self._auto_approve(command):
                pending = intercept.request("Bash", command, decision.get("reason", "ask"))
                self.activity.emit(self.name, "intercept",
                                   f"ask #{pending['id']}: {command[:160]} "
                                   f"(decide via lazy_guard approve|deny)",
                                   intent_id=intent.node_id)
                verdict = intercept.wait(pending["id"], timeout_sec=2.0)
                if verdict != "approved":
                    self.activity.emit(self.name, "block",
                                       f"needs approval: {decision.get('reason', 'ask')}",
                                       intent_id=intent.node_id)
                    outcome["state"] = "blocked"
                    continue
            output = self._run(command, executor)
            budget.record_toolcall(self.task_id, intent.node_id)
            try:
                from modules.intercept import observe_post_tool as _observe
                verdict_post = _observe(output)
                if verdict_post in ("blocked", "error"):
                    self.activity.emit(self.name, verdict_post,
                                       f"post-tool {verdict_post}: {command[:120]}",
                                       intent_id=intent.node_id)
            except Exception:
                pass
            if output.startswith("execution failed:") and model_errors < 2:
                model_errors += 1
                self.activity.emit(self.name, "retry",
                                   f"transient failure, retry {model_errors}/2",
                                   intent_id=intent.node_id)
                time.sleep(1.0)
                output = self._run(command, executor)
                budget.record_toolcall(self.task_id, intent.node_id)
            self.traffic.record("bash", command, output, {"worker": self.name, "intent": intent.node_id})
            self.activity.emit(self.name, "result", output[:1500], intent_id=intent.node_id)
            transcripts.append((command, output))
        if outcome["state"] == "done" and not transcripts:
            outcome["state"] = "blocked"
        wrote = self._writeback(intent, transcripts)
        outcome["facts"] += wrote["facts"]
        outcome["assets"] += wrote["assets"]
        outcome["findings"] += wrote["findings"]
        if outcome["state"] == "done" and wrote["facts"] == 0 and wrote["findings"] == 0:
            outcome["state"] = "exhausted"
            self.activity.emit(self.name, "settle",
                               f"intent #{intent.node_id} explored but persisted nothing -> exhausted",
                               intent_id=intent.node_id)
        self.graph.set_state(intent.node_id, outcome["state"])
        for asset_id in self.graph.anchors_for(intent.node_id):
            self.assets.mark_tested(asset_id)
        return outcome

    def _target_for(self, intent: ExplorationNode) -> str:
        """Resolve concrete target for scope enforcement."""
        for asset_id in self.graph.anchors_for(intent.node_id):
            asset = self.assets.get(asset_id)
            if asset is not None:
                return str(asset.value)
        return resolve_target(self.task_id, self.store, self.graph)

    def _auto_approve(self, command: str) -> bool:
        """Auto-approve read-only probes, hold the rest for approval."""
        lowered = (command or "").lower()
        read_only = ("nmap", "curl", "dig", "host ", "whatweb", "nikto", "enum")
        if lowered.startswith(read_only):
            return True
        try:
            from modules.auto_registry import is_shell_verb as _is_auto_verb
        except Exception:
            return False
        return _is_auto_verb(lowered)

    def _run(self, command: str, executor) -> str:
        """Execute command through injected executor or LazyOwn runner."""
        try:
            if executor is not None:
                result = executor(command)
                return str(result or "")
            from core.process import run_command as _run_command
            return str(_run_command(command) or "")
        except Exception as exc:
            return f"execution failed: {exc}"

    def _steps_for(self, intent: ExplorationNode) -> list[str]:
        """Translate intent summary into real probe commands."""
        text = intent.text.lower()
        if text.startswith("auto "):
            from modules.auto_registry import steps_for as _auto_steps
            resolved = _auto_steps(intent.text, "")
            if resolved:
                return resolved
        targets = []
        for asset_id in self.graph.anchors_for(intent.node_id):
            asset = self.assets.get(asset_id)
            if asset is not None:
                targets.append(asset.value)
        target = targets[0] if targets else resolve_target(self.task_id, self.store, self.graph)
        target = (target or "").strip()
        if not target:
            return [f"echo no-target: cannot probe without scope; register scope first: {intent.text[:120]}"]
        host_flag = f" {target}"
        if "baseline recon" in text or "enumerate" in text:
            return [f"nmap -sV --top-ports 100{host_flag}".strip(),
                    f"curl -sSI --max-time 15 http://{target}".strip()]
        if "extend finding" in text:
            return [f"curl -sS -m 20 http://{target}".strip(),
                    f"nmap -sV -p- --min-rate 500{host_flag}".strip()]
        if "re-drive" in text or "serial chain" in text:
            return [f"nmap -sV -p 80,443,8080,8000,22,21,25,53,135,139,445,3306,3389 {target}".strip(),
                    f"curl -sS -m 20 -I http://{target}".strip()]
        from modules.auto_registry import steps_for as _auto_keyword_steps
        keyword_resolved = _auto_keyword_steps(intent.text, target)
        if keyword_resolved:
            return keyword_resolved
        return [f"nmap -sV -p 80,443,8080,8000,22,21,25,53,135,139,445,3306,3389 {target}".strip(),
                f"curl -sS -m 20 -I http://{target}".strip(),
                f"dig +short {target}".strip()]

    def _writeback(self, intent: ExplorationNode, transcripts: list[tuple[str, str]]) -> dict:
        """Write one aggregated fact plus assets/findings atomically with dedupe."""
        wrote = {"facts": 0, "assets": 0, "findings": 0}
        useful = [(cmd, (out or "").strip()) for cmd, out in transcripts
                  if (out or "").strip() and not (out or "").startswith("execution failed:")]
        if not useful:
            return wrote
        best_cmd, best_out = max(useful, key=lambda pair: len(pair[1]))
        evidence = f"{best_cmd} :: {best_out[:300]}"
        summary_bits = []
        for cmd, out in useful[:3]:
            first = next((ln.strip() for ln in out.splitlines() if ln.strip()), out[:120])
            summary_bits.append(f"{cmd[:60]} => {first[:120]}")
        fact_text = f"intent #{intent.node_id} [{intent.text[:100]}]: " + " | ".join(summary_bits)
        fact = self.graph.add_node("fact", f"{fact_text[:600]}",
                                   state="done", meta={"worker": self.name, "evidence": evidence[:500],
                                                       "confidence": "observed"})
        self.graph.add_edge(intent.node_id, fact.node_id, "yields")
        wrote["facts"] = 1
        seen_assets: set[tuple[str, str]] = set()
        for _, out in useful:
            for host in re.findall(r"\b(?:\d{1,3}\.){3}\d{1,3}\b", out)[:8]:
                if ("ip", host) not in seen_assets:
                    seen_assets.add(("ip", host))
                    try:
                        asset = self.assets.insert("ip", host)
                    except ValueError:
                        continue
                    self.graph.anchor(fact.node_id, asset.asset_id)
                    wrote["assets"] += 1
            for host in re.findall(r"\b(?:[a-z0-9-]+\.)+[a-z]{2,}\b", out.lower())[:8]:
                if ("subdomain", host) not in seen_assets:
                    seen_assets.add(("subdomain", host))
                    try:
                        asset = self.assets.insert("subdomain", host)
                    except ValueError:
                        continue
                    self.graph.anchor(fact.node_id, asset.asset_id)
                    wrote["assets"] += 1
            for match in re.findall(r"(\d+)/tcp\s+open\s+(\S+)?", out)[:8]:
                port = match[0]
                service = match[1] if len(match) > 1 else ""
                key = ("service", f"{port}/{service}")
                if key not in seen_assets:
                    seen_assets.add(key)
                    try:
                        asset = self.assets.insert("service", f"tcp/{port} {service}".strip())
                    except ValueError:
                        continue
                    self.graph.anchor(fact.node_id, asset.asset_id)
                    wrote["assets"] += 1
        lowered = " ".join(out for _, out in useful).lower()
        finding_marks = ("vulnerable", "cve-", "exploit", "ms17", "rce", "sqli", "lfi",
                         "unauthorized", "login:", "password:", "open tcp", "/tcp open")
        if any(mark in lowered for mark in finding_marks):
            poc = f"{best_cmd}\n{best_out[:800]}"
            text = f"possible issue via {best_cmd[:80]}: {best_out[:300]}"
            existing = self.graph.has_finding(text)
            if existing is not None:
                self.activity.emit(self.name, "dedupe",
                                   f"finding #{existing.node_id} already covers: {text[:120]}",
                                   intent_id=intent.node_id)
                self.graph.add_edge(intent.node_id, existing.node_id, "proves")
                try:
                    EvidenceStore(self.graph.task_id).add(existing.node_id, "poc", poc[:2000])
                except Exception:
                    pass
                return wrote
            finding = FindingService(self.graph.task_id, self.graph,
                                     self.activity, self.store).report(
                name=f"possible issue via {best_cmd[:80]}", summary=best_out[:400],
                poc=poc[:1500], intent_id=intent.node_id,
                asset_ids=self.graph.anchors_for(intent.node_id))
            self.graph.add_edge(intent.node_id, finding.node_id, "proves")
            for asset_id in self.graph.anchors_for(intent.node_id):
                self.graph.anchor(finding.node_id, asset_id)
            anchors = self.graph.anchors_for(fact.node_id)
            if anchors:
                self.graph.anchor(finding.node_id, anchors[0])
            try:
                EvidenceStore(self.graph.task_id).add(finding.node_id, "poc", poc[:2000])
            except Exception:
                pass
            wrote["findings"] = 1
        return wrote


class Retester:
    """Replay finding evidence to a verdict like the Lazy retester agent."""

    def __init__(self, graph: ExplorationGraph, activity: ActivityLog, traffic: TrafficLog) -> None:
        """Bind retester to task collaborators."""
        self.graph = graph
        self.activity = activity
        self.traffic = traffic

    def retest(self, finding_id: int, executor=None, note: str = "") -> dict:
        """Re-execute finding evidence to reproduced/fixed/inconclusive.

        Faithful to the reference retester: minimal targeted replay of the stored
        PoC, inconclusive when the environment blocks a decision (auth, WAF,
        unreachable, thin evidence) — one failed request never proves fixed.
        """
        finding = self.graph.get(int(finding_id))
        if finding is None or finding.kind != "finding":
            raise KeyError(f"unknown finding: {finding_id}")
        attempts = 0
        verdict = "inconclusive"
        evidence = ""
        poc = str(finding.meta.get("poc", "") or finding.text or "")[:300]
        blocked_marks = ("401", "403 forbidden", "waf", "blocked", "unreachable",
                         "connection refused", "no route", "timeout", "login required",
                         "unauthorized", "401", "captcha")
        for _ in range(RETEST_MAX_ATTEMPTS):
            attempts += 1
            command = (poc.splitlines() or [""])[0][:300] or f"curl -sS -m 20 -I {finding.text[:120]}"
            try:
                if executor is not None:
                    evidence = str(executor(command) or "")
                else:
                    from core.process import run_command as _run_command
                    evidence = str(_run_command(command) or "")
            except Exception as exc:
                evidence = f"retest failed: {exc}"
            self.traffic.record("bash", command, evidence, {"retest": finding_id})
            lowered = evidence.lower()
            if any(mark in lowered for mark in ("200", "vulnerable", "cve", "exploit", "open tcp")):
                verdict = "reproduced"
                break
            if any(mark in lowered for mark in ("404", "no longer", "patched", "remediated")):
                verdict = "fixed"
                break
            if any(mark in lowered for mark in blocked_marks) or not evidence.strip():
                verdict = "inconclusive"
                evidence += f"\n[blocked: {note or 'environment or evidence too thin to decide'}]"[:300]
                break
        finding.meta["retest"] = {"verdict": verdict, "attempts": attempts,
                                  "evidence": evidence[:1000], "note": note[:300]}
        if verdict == "reproduced":
            finding.state = "done"
        elif verdict == "fixed":
            finding.state = "done"
            finding.meta["status"] = "fixed"
        else:
            finding.state = "pending"
        finding.updated = _now()
        self.graph._persist()
        self.activity.emit("retester", "verdict", f"finding #{finding_id}: {verdict} ({attempts} attempts)")
        return {"finding_id": finding_id, "verdict": verdict, "attempts": attempts}

    def retest_context(self, finding_id: int) -> dict:
        """Return finding + PoC + assets + constraints like get_finding_retest_context."""
        finding = self.graph.get(int(finding_id))
        if finding is None or finding.kind != "finding":
            raise KeyError(f"unknown finding: {finding_id}")
        return {"finding_id": finding_id, "text": finding.text,
                "meta": dict(finding.meta),
                "anchors": self.graph.anchors_for(finding.node_id),
                "evidence": EvidenceStore(self.graph.task_id).for_finding(int(finding_id))}


class ColdCompactor:
    """Fold stale exploration nodes into digests like the planner coldgraph."""

    def __init__(self, graph: ExplorationGraph, activity: ActivityLog) -> None:
        """Bind compactor to task graph."""
        self.graph = graph
        self.activity = activity

    def compact(self, threshold: int = DEFAULT_COLD_THRESHOLD, mode: str = "minor") -> dict:
        """Fold cold facts into digests like coldgraph minor/major.

        minor appends only not-yet-covered cold facts; major re-derives the
        whole grouping and reuses unchanged digest bodies (signature check).
        """
        done_facts = [n for n in self.graph.list("fact", "done") if not n.meta.get("cold")]
        if mode == "major":
            candidates = [n for n in self.graph.list("fact") if not n.meta.get("cold_digest")]
        else:
            candidates = done_facts
        if len(candidates) <= threshold:
            return {"compacted": 0, "digest_id": 0, "mode": mode}
        stale = candidates[: len(candidates) - threshold]
        groups: dict[str, list] = {}
        for node in stale:
            sig = hashlib.sha256(node.text[:60].encode()).hexdigest()[:8]
            groups.setdefault(sig, []).append(node)
        digest_ids: list[int] = []
        for sig, members in groups.items():
            if len(members) < 2 and mode == "minor":
                continue
            body = "cold digest: " + " | ".join(n.text[:80] for n in members[:10])
            digest = self.graph.add_node("fact", body[:500], state="done",
                                         meta={"cold_digest": True, "mode": mode,
                                               "members": [n.node_id for n in members],
                                               "sig": sig})
            digest_ids.append(digest.node_id)
            for node in members:
                if node.state not in ("pending", "open", "running"):
                    node.meta["cold"] = True
                    node.state = "exhausted"
        self.graph._persist()
        self.activity.emit("compactor", "digest",
                           f"{mode}: folded {len(stale)} cold facts into {len(digest_ids)} digests")
        return {"compacted": len(stale), "digest_id": digest_ids[0] if digest_ids else 0,
                "digests": digest_ids, "mode": mode}

    def expand(self, digest_id: int) -> list[int]:
        """Restore digest members like expandDigest."""
        digest = self.graph.get(int(digest_id))
        if digest is None or not digest.meta.get("cold_digest"):
            raise KeyError(f"unknown digest: {digest_id}")
        revived = []
        for member_id in digest.meta.get("members", []) or []:
            node = self.graph.get(int(member_id))
            if node is not None and node.state == "exhausted":
                node.state = "done"
                node.meta.pop("cold", None)
                revived.append(node.node_id)
        self.graph._persist()
        self.activity.emit("compactor", "expand",
                           f"digest #{digest_id}: revived {len(revived)} members")
        return revived

    def unfolded(self, limit: int = 60) -> dict:
        """Return cold facts unfolded up to cap with a truncated flag.

        Restores the un-nerfed view: the operator sees real cold members
        (not just digest counts); ``truncated`` tells whether the cap hid
        the tail.
        """
        cold = [n for n in self.graph.list("fact")
                if n.meta.get("cold") or n.state == "exhausted"]
        cold.sort(key=lambda n: n.node_id)
        shown = cold[: max(1, limit)]
        return {"facts": [{"id": n.node_id, "text": n.text[:200],
                           "state": n.state} for n in shown],
                "total": len(cold), "truncated": len(cold) > len(shown)}

    def digest_overview(self) -> dict:
        """Digest index: every digest with expandable members + body preview.

        ``expandable`` lists digests that still hold exhausted members
        (revivable via expand); ``covered`` counts cold facts already
        folded under a digest (lineage coverage).
        """
        digests = [n for n in self.graph.list("fact") if n.meta.get("cold_digest")]
        covered: set[int] = set()
        for digest in digests:
            covered.update(int(m) for m in digest.meta.get("members", []) or [])
        expandable = []
        for digest in digests:
            alive = [int(m) for m in digest.meta.get("members", []) or []
                     if (self.graph.get(int(m)) or digest).state == "exhausted"]
            if alive:
                expandable.append(digest.node_id)
        return {"digests": [{"id": n.node_id, "mode": n.meta.get("mode", ""),
                             "members": list(n.meta.get("members", []) or []),
                             "body": n.text[:200]} for n in digests],
                "expandable": expandable,
                "covered": len(covered)}


def constraint_block(constraints: list[dict]) -> str:
    """Render allow/deny bounds as highest-priority prompt block.

    Faithful to the reference constraint block: allow/deny grouped, out-of-scope
    targets are recorded as facts and skipped, never probed.
    """
    allow = [str(c.get("text", "")).strip() for c in constraints or []
             if c.get("type") == "allow" and str(c.get("text", "")).strip()]
    deny = [str(c.get("text", "")).strip() for c in constraints or []
            if c.get("type") != "allow" and str(c.get("text", "")).strip()]
    if not allow and not deny:
        return ""
    block = ("\n\n[OPERATION CONSTRAINTS — highest priority, override all exploration "
             "heuristics; self-check every intent and every action before acting]")
    if allow:
        block += "\nAllowed:\n" + "\n".join(f"- {t}" for t in allow)
    if deny:
        block += "\nDenied:\n" + "\n".join(f"- {t}" for t in deny)
    block += ("\n(New targets outside the allowed scope are NOT authorization: "
              "record an out-of-scope fact and skip, never derive intents or run tools.)")
    return block


def finding_severity(text: str, evidence: str = "") -> str:
    """Rank finding severity like the report renderer (critical first)."""
    blob = f"{text or ''} {evidence or ''}".lower()
    if any(m in blob for m in ("rce", "remote code", "cve-", "ms17", "unauthenticated")):
        return "critical" if any(m in blob for m in ("rce", "cve-", "ms17")) else "high"
    if any(m in blob for m in ("sqli", "ssrf", "lfi", "idor", "privesc", "exploit")):
        return "high"
    if any(m in blob for m in ("xss", "open tcp", "login:", "password:", "unauthorized")):
        return "medium"
    if any(m in blob for m in ("vulnerable", "exposed", "header")):
        return "low"
    return "info"


class FindingService:
    """Finding lifecycle: report/status/bind like finding_workflow."""

    def __init__(self, task_id: str, graph: ExplorationGraph,
                 activity: ActivityLog, store=None) -> None:
        """Bind service to task collaborators."""
        self.task_id = task_id
        self.graph = graph
        self.activity = activity
        self.store = store

    def report(self, name: str, summary: str = "", poc: str = "",
               severity: str = "", vulnclass: str = "",
               intent_id: int = 0, asset_ids: list[int] | None = None,
               traffic_refs: list[str] | None = None) -> ExplorationNode:
        """Register a finding with severity/evidence/dedupe like report_finding."""
        text = f"{name.strip()} :: {(summary or poc)[:400]}".strip(" :")
        if not text:
            raise ValueError("finding name is required")
        existing = self.graph.has_finding(text)
        if existing is not None:
            self.activity.emit("reporter", "dedupe",
                               f"finding #{existing.node_id} already covers: {text[:120]}",
                               intent_id=int(intent_id))
            return existing
        sev = (severity or "").lower() if severity in SEVERITIES else finding_severity(text, poc)
        node = self.graph.add_node(
            "finding", text[:600], state="pending",
            meta={"name": name[:200], "summary": summary[:1000],
                  "poc": poc[:2000], "severity": sev,
                  "vulnclass": (vulnclass or "")[:80], "status": "pending",
                  "sig": self.graph.finding_signature(text),
                  "traffic_refs": list(traffic_refs or [])})
        if intent_id:
            self.graph.add_edge(int(intent_id), node.node_id, "proves")
        for asset_id in asset_ids or []:
            self.graph.anchor(node.node_id, int(asset_id))
        self.activity.emit("reporter", "finding",
                           f"finding #{node.node_id} [{sev}] {name[:120]}",
                           intent_id=int(intent_id))
        Notifier(self.store).emit(self.task_id, "finding_created", {
            "finding_id": node.node_id, "name": name[:200], "severity": sev})
        return node

    def set_status(self, finding_id: int, status: str) -> bool:
        """Transition finding status like the workflow disposition."""
        if status not in FINDING_STATUSES:
            raise ValueError(f"status must be one of {FINDING_STATUSES}")
        node = self.graph.get(int(finding_id))
        if node is None or node.kind != "finding":
            return False
        node.meta["status"] = status
        node.state = "done" if status in ("confirmed", "resolved", "fixed") else node.state
        node.updated = _now()
        self.graph._persist()
        self.activity.emit("reporter", "status", f"finding #{finding_id} -> {status}")
        Notifier(self.store).emit(self.task_id, "finding_status_changed", {
            "finding_id": int(finding_id), "status": status})
        return True

    def ranked(self) -> list[ExplorationNode]:
        """Findings ordered critical-first like the Markdown renderer."""
        return sorted(self.graph.list("finding"),
                      key=lambda n: (SEV_RANK.get(str(n.meta.get("severity", "")), 5), n.node_id))


class EvidenceStore:
    """Durable PoC/evidence vault per task like evidence/store."""

    def __init__(self, task_id: str) -> None:
        """Bind vault to task."""
        self.task_id = task_id
        self._path = _store_path(f"evidence_{task_id}.json")

    def _load(self) -> dict:
        """Load vault payload."""
        return _load_json(self._path, {"seq": 0, "items": []})

    def add(self, finding_id: int, kind: str, body: str) -> dict:
        """Attach evidence to a finding and return the record."""
        payload = self._load()
        payload["seq"] = int(payload.get("seq", 0)) + 1
        text = (body or "")[:4000]
        item = {"id": payload["seq"], "finding_id": int(finding_id),
                "kind": kind[:40] or "note", "body": text, "ts": _now(),
                "sha256": hashlib.sha256(text.encode()).hexdigest()}
        payload.setdefault("items", []).append(item)
        _save_json(self._path, payload)
        return item

    def verify(self) -> list[int]:
        """Return ids whose body fails the sha256 integrity check."""
        bad = []
        for item in self._load().get("items", []):
            digest = hashlib.sha256(str(item.get("body", "")).encode()).hexdigest()
            if item.get("sha256") and digest != item.get("sha256"):
                bad.append(int(item.get("id", 0)))
        return bad

    def gc(self, valid_findings: set[int] | None = None) -> int:
        """Drop evidence for findings no longer present; returns removed."""
        payload = self._load()
        items = payload.get("items", [])
        if valid_findings is None:
            try:
                valid_findings = {n.node_id for n in
                                  ExplorationGraph(self.task_id).list("finding")}
            except Exception:
                return 0
        kept = [i for i in items if int(i.get("finding_id", 0)) in valid_findings]
        removed = len(items) - len(kept)
        if removed:
            payload["items"] = kept
            _save_json(self._path, payload)
        return removed

    def for_finding(self, finding_id: int) -> list[dict]:
        """Return evidence attached to one finding."""
        return [i for i in self._load().get("items", [])
                if int(i.get("finding_id", 0)) == int(finding_id)]

    def export(self, path: str) -> str:
        """Dump vault to a file for the report pipeline."""
        dest = Path(path)
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(json.dumps(self._load().get("items", []), indent=2, ensure_ascii=False))
        return str(dest)


class Notifier:
    """Finding event fan-out like notify/ (log + webhook, stateless)."""

    def __init__(self, store=None) -> None:
        """Bind optional channel config from task store."""
        self._store = store

    def channels(self) -> list[dict]:
        """Return configured channels (empty = log only)."""
        try:
            raw = _load_json(_store_path("notify_channels.json"), {"channels": []})
            return list(raw.get("channels", []))
        except Exception:
            return []

    def add_channel(self, kind: str, target: str, min_severity: str = "") -> dict:
        """Register a channel: log|webhook|file with severity floor."""
        if kind not in ("log", "webhook", "file"):
            raise ValueError("kind must be log|webhook|file")
        payload = _load_json(_store_path("notify_channels.json"), {"channels": []})
        item = {"kind": kind, "target": target[:500], "min_severity": min_severity or ""}
        payload.setdefault("channels", []).append(item)
        _save_json(_store_path("notify_channels.json"), payload)
        return item

    def emit(self, task_id: str, event: str, data: dict) -> int:
        """Fan out finding_created/status_changed; returns deliveries."""
        sev = str((data or {}).get("severity", "") or "")
        try:
            from modules.notify import mask_secrets as _mask
            safe_data = {k: (_mask(str(v)) if isinstance(v, str) else v)
                         for k, v in (data or {}).items()}
        except Exception:
            safe_data = dict(data or {})
        line = json.dumps({"ts": _now(), "task": task_id, "event": event, **safe_data},
                          ensure_ascii=False)
        with _store_path("notify.log").open("a") as handle:
            handle.write(line + "\n")
        delivered = 0
        for channel in self.channels():
            floor = str(channel.get("min_severity", "") or "")
            if floor and SEV_RANK.get(sev, 5) > SEV_RANK.get(floor, 5):
                continue
            try:
                if channel.get("kind") == "webhook" and channel.get("target"):
                    try:
                        from modules.notify import url_allowed as _allowed
                        ok, _reason = _allowed(str(channel["target"]))
                    except Exception:
                        ok, _reason = True, "ok"
                    if not ok:
                        continue
                    request = urllib.request.Request(
                        channel["target"], data=line.encode(),
                        headers={"Content-Type": "application/json"}, method="POST")
                    with urllib.request.urlopen(request, timeout=8):
                        pass
                elif channel.get("kind") == "file" and channel.get("target"):
                    dest = Path(str(channel["target"]))
                    dest.parent.mkdir(parents=True, exist_ok=True)
                    with dest.open("a") as handle:
                        handle.write(line + "\n")
                delivered += 1
            except Exception:
                continue
        return delivered


class TriggerStore:
    """Persistent event/interval triggers like server/scheduler (P3)."""

    def __init__(self, task_id: str = "") -> None:
        """Bind trigger table (global when task_id empty)."""
        name = f"triggers_{task_id}.json" if task_id else "triggers.json"
        self._path = _store_path(name)

    def _load(self) -> dict:
        """Load trigger payload."""
        return _load_json(self._path, {"seq": 0, "items": []})

    def add(self, kind: str, arg: str = "", every_sec: float = 0.0) -> dict:
        """Register a trigger; interval needs every_sec, events fire on new rows."""
        if kind not in TRIGGER_KINDS:
            raise ValueError(f"kind must be one of {TRIGGER_KINDS}")
        payload = self._load()
        payload["seq"] = int(payload.get("seq", 0)) + 1
        item = {"id": payload["seq"], "kind": kind, "arg": (arg or "")[:300],
                "every_sec": float(every_sec or 0.0), "last_fire": 0.0,
                "watermark": 0, "enabled": True}
        payload.setdefault("items", []).append(item)
        _save_json(self._path, payload)
        return item

    def remove(self, trigger_id: int) -> bool:
        """Delete a trigger."""
        payload = self._load()
        before = len(payload.get("items", []))
        payload["items"] = [i for i in payload["items"] if int(i.get("id", 0)) != int(trigger_id)]
        if len(payload["items"]) != before:
            _save_json(self._path, payload)
            return True
        return False

    def list(self) -> list[dict]:
        """Return all triggers."""
        return list(self._load().get("items", []))

    def due(self, task_id: str, graph: ExplorationGraph, activity: ActivityLog) -> list[dict]:
        """Evaluate triggers like the scheduler tick; fires at most once each."""
        payload = self._load()
        fired: list[dict] = []
        now = _now()
        for item in payload.get("items", []):
            if not item.get("enabled"):
                continue
            kind = item.get("kind")
            if kind == "interval":
                if now - float(item.get("last_fire", 0.0)) >= max(5.0, float(item.get("every_sec", 60.0))):
                    item["last_fire"] = now
                    fired.append({"kind": "interval", "id": item["id"]})
            elif kind == "finding":
                current = [n.node_id for n in graph.list("finding")]
                new = [i for i in current if i > int(item.get("watermark", 0))]
                if new:
                    item["watermark"] = max(new)
                    fired.append({"kind": "finding", "ids": new, "id": item["id"]})
            elif kind == "goal":
                met = [n.node_id for n in graph.list("goal", "done")]
                seen = set(item.get("fired_goals", []))
                new = [i for i in met if i not in seen]
                if new:
                    item["fired_goals"] = sorted(seen | set(new))
                    fired.append({"kind": "goal", "ids": new, "id": item["id"]})
            elif kind == "hint":
                pending = [n.node_id for n in graph.list("hint", "pending")]
                new = [i for i in pending if i > int(item.get("watermark", 0))]
                if new:
                    item["watermark"] = max(new)
                    fired.append({"kind": "hint", "ids": new, "id": item["id"]})
            elif kind == "toolcall":
                total = len(activity.read(2000))
                if total > int(item.get("watermark", 0)):
                    item["watermark"] = total
                    fired.append({"kind": "toolcall", "total": total, "id": item["id"]})
            elif kind == "timeout":
                fired.append({"kind": "timeout", "id": item["id"]})
        if fired:
            _save_json(self._path, payload)
        return fired


class LlmPool:
    """Optional LLM chain with failover + usage ledger like llmpool/llmrec.

    Members resolve through modules.llm_factory when configured; with no
    members the planner/worker keep the heuristic path (never a hard error).
    Failures trip a shared health registry with tiered backoff so a dead
    head member is skipped instead of retried every round.
    """

    DEFAULT_MEMBERS = (
        {"name": "groq-cloud", "model": "groq:llama-3.3-70b-versatile", "priority": 10},
        {"name": "ollama-local", "model": "ollama:deepseek-r1:1.5b", "priority": 5},
        {"name": "toposwarm-agent", "model": "toposwarm:router", "priority": 1},
    )

    def __init__(self) -> None:
        """Load member list and usage ledger paths."""
        self._path = _store_path("llm_pool.json")
        self._usage = _store_path("llm_usage.json")
        try:
            from modules.llm_pool import shared_registry as _shared
            self._health = _shared()
        except Exception:
            self._health = None

    def _seed_defaults(self) -> None:
        """Persist the 3 default legs once so operators can edit/remove them."""
        try:
            payload = _load_json(self._path, {"members": []})
            if payload.get("members"):
                return
            payload["members"] = [dict(spec) for spec in self.DEFAULT_MEMBERS]
            _save_json(self._path, payload)
        except Exception:
            pass

    def members(self) -> list[dict]:
        """Return configured chain in order, seeding defaults on first use."""
        self._seed_defaults()
        return list(_load_json(self._path, {"members": []}).get("members", []))

    def add_member(self, name: str, model: str = "", priority: int = 0) -> dict:
        """Append a chain member backed by llm_factory at call time."""
        payload = _load_json(self._path, {"members": []})
        item = {"name": name[:120], "model": (model or name)[:120], "priority": int(priority)}
        payload.setdefault("members", []).append(item)
        payload["members"].sort(key=lambda m: -int(m.get("priority", 0)))
        _save_json(self._path, payload)
        return item

    def remove_member(self, name: str) -> bool:
        """Drop a chain member."""
        payload = _load_json(self._path, {"members": []})
        before = len(payload.get("members", []))
        payload["members"] = [m for m in payload["members"] if m.get("name") != name]
        if len(payload["members"]) != before:
            _save_json(self._path, payload)
            return True
        return False

    def usage(self) -> dict:
        """Return per-member call ledger like llm_usage."""
        return _load_json(self._usage, {"calls": []})

    def _record(self, member: str, ok: bool, text: str = "") -> None:
        """Append one ledger row like llmrec capture."""
        payload = self.usage()
        payload.setdefault("calls", []).append(
            {"ts": _now(), "member": member, "ok": ok, "text": text[:500]})
        _save_json(self._usage, payload)

    def complete(self, prompt: str, max_tokens: int = 800) -> str:
        """Fail over across members; empty string when no backend answers."""
        if not (prompt or "").strip():
            return ""
        for member in self.members():
            name = str(member.get("name", "?"))
            if self._health is not None:
                try:
                    if not self._health.healthy(name):
                        continue
                except Exception:
                    pass
            try:
                from modules.llm_factory import complete as _complete
                text = str(_complete(str(member.get("model", "")),
                                     prompt[:6000], max_tokens=max_tokens) or "")
            except Exception as exc:
                self._record(name, False, str(exc)[:200])
                if self._health is not None:
                    try:
                        self._health.report_failure(name, str(exc)[:200])
                    except Exception:
                        pass
                continue
            if text.strip():
                self._record(name, True, text[:200])
                if self._health is not None:
                    try:
                        self._health.report_success(name)
                    except Exception:
                        pass
                return text
            self._record(name, False, "empty reply")
            if self._health is not None:
                try:
                    self._health.report_failure(name, "empty reply")
                except Exception:
                    pass
        return ""

    def health(self) -> dict:
        """Return per-member health state for lazy_llm health."""
        out = {}
        for member in self.members():
            name = str(member.get("name", "?"))
            try:
                out[name] = bool(self._health.healthy(name)) if self._health else True
            except Exception:
                out[name] = True
        return out


class ToolCatalog:
    """Per-agent tool bindings like agent/toolcatalog (DB-overridable)."""

    def __init__(self) -> None:
        """Load binding table."""
        self._path = _store_path("tool_catalog.json")

    def _load(self) -> dict:
        """Load catalog payload."""
        return _load_json(self._path, {"bindings": {
            "planner": ["graph", "facts", "findings", "node", "intent", "goal"],
            "worker": ["bash", "fact", "finding", "trace"],
            "reporter": ["finding", "traffic", "evidence"]}})

    def bindings(self, agent: str = "") -> dict:
        """Return bindings for one agent or the whole table."""
        table = self._load().get("bindings", {})
        return {agent: table.get(agent, [])} if agent else dict(table)

    def bind(self, agent: str, tool: str) -> list[str]:
        """Opt a tool into an agent lane."""
        payload = self._load()
        tools = payload.setdefault("bindings", {}).setdefault(agent, [])
        if tool not in tools:
            tools.append(tool)
        _save_json(self._path, payload)
        return list(tools)

    def unbind(self, agent: str, tool: str) -> list[str]:
        """Remove a tool from an agent lane."""
        payload = self._load()
        tools = payload.setdefault("bindings", {}).setdefault(agent, [])
        if tool in tools:
            tools.remove(tool)
        _save_json(self._path, payload)
        return list(tools)


class SideQuestions:
    """Bounded side-question Q&A over task context like sidequestion/."""

    BUDGET_CHARS = 6000

    def ask(self, task_id: str, question: str, pool: LlmPool | None = None) -> dict:
        """Answer from graph overview + recent trace within a char budget."""
        graph = ExplorationGraph(task_id)
        activity = ActivityLog(task_id)
        context = json.dumps(graph.overview(), ensure_ascii=False)[:3000]
        trace = "\n".join(str(r.get("text", ""))[:200] for r in activity.read(10))
        budget = f"{context}\n{trace}"[: self.BUDGET_CHARS]
        answer = ""
        if pool is not None:
            answer = pool.complete(f"Context:\n{budget}\n\nQuestion: {question[:500]}")
        if not answer:
            needle = (question or "").lower()
            hits = activity.search(question)[:3] if needle else []
            if hits:
                answer = " | ".join(str(h.get("text", ""))[:300] for h in hits)
            else:
                view = graph.overview()
                answer = (f"task {task_id}: {view.get('nodes', 0)} nodes, "
                          f"{view.get('facts', 0)} facts, {view.get('findings', 0)} findings; "
                          f"top intents: " + "; ".join(
                              i["text"][:80] for i in view.get("intents", [])[-3:]))
        ActivityLog(task_id).emit("sidequestion", "answer", f"Q: {question[:200]} A: {answer[:500]}")
        return {"question": question[:500], "answer": answer[:2000], "budget": len(budget)}


class CompanyScope:
    """Company asset-range registry like db/companies + company_scope."""

    def __init__(self) -> None:
        """Load company table."""
        self._path = _store_path("companies.json")

    def _load(self) -> dict:
        """Load company payload."""
        return _load_json(self._path, {"seq": 0, "items": []})

    def add(self, name: str, scope: str = "") -> dict:
        """Register a company with an optional scope pattern."""
        payload = self._load()
        payload["seq"] = int(payload.get("seq", 0)) + 1
        item = {"id": payload["seq"], "name": name[:200], "scope": (scope or "")[:300],
                "ts": _now()}
        payload.setdefault("items", []).append(item)
        _save_json(self._path, payload)
        return item

    def list(self) -> list[dict]:
        """Return companies with asset counts."""
        return list(self._load().get("items", []))

    def match(self, value: str) -> list[dict]:
        """Return companies whose scope substring hits the value."""
        lowered = (value or "").lower()
        return [c for c in self.list()
                if c.get("scope") and c["scope"].lower() in lowered]


class TaskArchive:
    """Task snapshot vault like task_archives: save/list/restore/stats."""

    def save(self, task_id: str) -> dict:
        """Snapshot task record + graph + activity tail into one archive."""
        from modules.lazy_loop import TaskStore as _Store
        store = _Store()
        record = store.get(task_id) or {}
        graph = ExplorationGraph(task_id)
        payload = {"task_id": task_id, "ts": _now(), "task": record,
                   "nodes": [asdict(n) for n in graph.nodes.values()],
                   "edges": [asdict(e) for e in graph.edges],
                   "anchors": list(graph.anchors),
                   "activity": ActivityLog(task_id).read(200),
                   "todos": TodoStore(task_id).as_list()}
        dest = _store_path(f"archive_{task_id}_{int(_now())}.json")
        dest.write_text(json.dumps(payload, indent=2, ensure_ascii=False))
        return {"path": str(dest), "nodes": len(payload["nodes"])}

    def list(self) -> list[dict]:
        """Return archive snapshots with task + node counts."""
        out = []
        try:
            paths = sorted(STORE_DIR.glob("archive_*.json"))
        except OSError:
            return []
        for path in paths[-50:]:
            try:
                payload = json.loads(path.read_text())
            except (OSError, ValueError):
                continue
            out.append({"path": str(path), "task_id": payload.get("task_id", ""),
                        "nodes": len(payload.get("nodes", [])),
                        "ts": payload.get("ts", 0.0)})
        return out

    def restore(self, path: str) -> str:
        """Restore one archive as a NEW task; returns the new task id."""
        from modules.lazy_loop import TaskStore as _Store
        payload = json.loads(Path(path).read_text())
        store = _Store()
        task = store.create(str((payload.get("task") or {}).get("goal", "restored")),
                            "restored from archive")
        graph = ExplorationGraph(task.task_id)
        for node in payload.get("nodes", []):
            try:
                graph.add_node(node.get("kind", "fact"), node.get("text", ""),
                               state=node.get("state", "done"),
                               priority=int(node.get("priority", DEFAULT_PRIORITY)),
                               meta=dict(node.get("meta", {})))
            except (ValueError, TypeError):
                continue
        ActivityLog(task.task_id).emit("engine", "archive", f"restored from {path}")
        return task.task_id

    def stats(self) -> dict:
        """Aggregate counts across archives like archive aggregate stats."""
        items = self.list()
        return {"archives": len(items), "nodes": sum(i.get("nodes", 0) for i in items)}


class TaskTemplate:
    """Named goal templates like task_templates: list/add/use/remove."""

    def __init__(self) -> None:
        """Bind template table."""
        self._path = _store_path("task_templates.json")

    def _load(self) -> dict:
        """Load template payload."""
        return _load_json(self._path, {"items": []})

    def list(self) -> list[dict]:
        """Return all templates."""
        return list(self._load().get("items", []))

    def add(self, name: str, goal: str) -> dict:
        """Register a template; names are unique (overwrite on clash)."""
        payload = self._load()
        items = [i for i in payload.get("items", []) if i.get("name") != name]
        item = {"name": name[:120], "goal": goal[:500], "ts": _now()}
        items.append(item)
        payload["items"] = items
        _save_json(self._path, payload)
        return item

    def remove(self, name: str) -> bool:
        """Delete a template by name."""
        payload = self._load()
        before = len(payload.get("items", []))
        payload["items"] = [i for i in payload["items"] if i.get("name") != name]
        if len(payload["items"]) != before:
            _save_json(self._path, payload)
            return True
        return False

    def get(self, name: str) -> dict | None:
        """Return one template by name or None."""
        for item in self.list():
            if item.get("name") == name:
                return item
        return None


class TaskCategory:
    """Per-task labels like task_categories: set/list."""

    def __init__(self, store=None) -> None:
        """Bind optional task store."""
        self._store = store
        self._path = _store_path("task_categories.json")

    def set(self, task_id: str, category: str) -> dict:
        """Label a task; returns the mapping."""
        payload = _load_json(self._path, {"map": {}})
        payload.setdefault("map", {})[task_id] = category[:80]
        _save_json(self._path, payload)
        return {"task_id": task_id, "category": category[:80]}

    def get(self, task_id: str) -> str:
        """Return the category for a task or empty string."""
        return str(_load_json(self._path, {"map": {}}).get("map", {}).get(task_id, ""))

    def list(self, category: str = "") -> list[dict]:
        """Return task->category rows, optionally filtered."""
        rows = [{"task_id": k, "category": v} for k, v in
                _load_json(self._path, {"map": {}}).get("map", {}).items()]
        if category:
            rows = [r for r in rows if r["category"] == category]
        return sorted(rows, key=lambda r: r["task_id"])


class TaskChat:
    """Persistent per-task conversation like conversation/: say/log/clear."""

    def say(self, task_id: str, text: str, pool=None) -> dict:
        """Append a human turn and answer from task context; returns both."""
        path = _store_path(f"chat_{task_id}.jsonl")
        question = (text or "").strip()[:1000]
        if not question:
            raise ValueError("message is required")
        with path.open("a") as handle:
            handle.write(json.dumps({"ts": _now(), "role": "human",
                                     "text": question}, ensure_ascii=False) + "\n")
        answer = ""
        if pool is not None:
            try:
                history = "\n".join(f"{r.get('role')}: {str(r.get('text', ''))[:200]}"
                                    for r in self.log(task_id, 6))
                view = ExplorationGraph(task_id).overview()
                answer = pool.complete(
                    f"Task {task_id} context: {json.dumps(view)[:1500]}\n"
                    f"History:\n{history}\nHuman: {question}\nAnswer briefly.")
            except Exception:
                answer = ""
        if not answer:
            view = ExplorationGraph(task_id).overview()
            answer = (f"task {task_id}: {view.get('facts', 0)} facts, "
                      f"{view.get('findings', 0)} findings; "
                      f"pending intents: {len(view.get('pending', []))}. "
                      f"Ask with lazy_ask for bounded Q&A or steer with lazy_hint.")
        with path.open("a") as handle:
            handle.write(json.dumps({"ts": _now(), "role": "assistant",
                                     "text": answer[:2000]}, ensure_ascii=False) + "\n")
        ActivityLog(task_id).emit("chat", "turn", f"Q: {question[:160]} A: {answer[:160]}")
        return {"question": question, "answer": answer[:2000]}

    def log(self, task_id: str, limit: int = 20) -> list[dict]:
        """Return recent conversation turns."""
        try:
            lines = _store_path(f"chat_{task_id}.jsonl").read_text().splitlines()
        except OSError:
            return []
        out = []
        for line in lines[-max(1, limit):]:
            try:
                out.append(json.loads(line))
            except ValueError:
                continue
        return out

    def clear(self, task_id: str) -> bool:
        """Drop the conversation log for a task."""
        try:
            _store_path(f"chat_{task_id}.jsonl").unlink()
            return True
        except OSError:
            return False


class LazyLoopEngine:
    """Single event-driven orchestrator: planner, workers, guard, enrich, retest.

    One human command (lazy_loop / auto_loop) invokes every operator-visible
    step internally: scope, asset, enrich, planner, frontier claim, worker
    tools, traffic, finding, retest, compaction, trace, report.
    """

    ORCHESTRATOR_CHAIN = (
        "lazy_task", "lazy_scope", "lazy_asset", "lazy_enrich",
        "lazy_planner", "lazy_frontier", "lazy_worker", "lazy_guard",
        "lazy_traffic", "lazy_finding", "lazy_retest", "lazy_compact",
        "lazy_trace", "lazy_report",
    )

    def __init__(self) -> None:
        """Load shared stores."""
        self.assets = AssetGraph()
        self.store = TaskStore()
        self.debounce_sec = DEFAULT_DEBOUNCE_SEC
        self.budget = Budget(self.store)
        self.runtime = RuntimeTracker(self.store)

    def ensure_target(self, task_id: str, target: str, reason: str = "") -> dict:
        """Register scope + asset for target like lazy_scope/lazy_asset."""
        target = (target or "").strip()
        if not target:
            return {}
        record = self.store.get(task_id) or {}
        kind = "ip"
        lowered = target.lower()
        if "/" in target and any(ch.isdigit() for ch in target):
            kind = "cidr"
        elif lowered.startswith("http"):
            kind = "url"
        elif "." in target and not any(ch.isdigit() for ch in target.replace(".", "")):
            kind = "subdomain"
        item = None
        if not any(s.get("value") == target for s in record.get("scope", [])):
            item = self.store.add_scope(task_id, kind, target, reason or "loop target")
        try:
            asset = self.assets.insert(kind if kind in
                                       ("ip", "cidr", "subdomain", "url") else "ip", target)
            asset_id = asset.asset_id
        except ValueError:
            asset_id = 0
        ActivityLog(task_id).emit("engine", "lazy_scope",
                                  f"scope [{kind}]: {target} (asset #{asset_id})")
        return {"scope": item, "asset_id": asset_id, "kind": kind}

    def orchestrate(self, goal: str = "", task_id: str = "", target: str = "",
                    max_rounds: int = DEFAULT_MAX_ROUNDS,
                    workers: int = DEFAULT_WORKERS,
                    timeout_sec: float = 0.0, executor=None) -> dict:
        """Single entry for lazy_loop + auto_loop: create, scope, run, report."""
        if task_id:
            record = self.store.get(task_id)
            if record is None:
                task_id = ""
        if not task_id:
            task_id = self.create_task(goal or f"engage {target or 'target'}")["task_id"]
        if target:
            self.ensure_target(task_id, target, "loop target")
        result = self.run(task_id, max_rounds=max_rounds, workers=workers,
                          executor=executor, timeout_sec=timeout_sec)
        result["chain"] = list(self.ORCHESTRATOR_CHAIN)
        return result

    def _parts(self, task_id: str) -> tuple[ExplorationGraph, ActivityLog, TrafficLog, Guard]:
        """Build per-task collaborators."""
        graph = ExplorationGraph(task_id)
        return graph, ActivityLog(task_id), TrafficLog(task_id), Guard(task_id)

    def create_task(self, goal: str, description: str = "") -> dict:
        """Create task, decompose goals, register scope, return summary."""
        task = self.store.create(goal, description)
        graph = ExplorationGraph(task.task_id)
        for spec in decompose_goals(goal, description):
            graph.add_node("goal", spec["text"], state="pending", meta={"vulnclass": spec["vulnclass"]})
        added = 0
        for item in extract_scope_items(goal, description):
            try:
                self.store.add_scope(task.task_id, item["kind"], item["value"], item["reason"])
                try:
                    self.assets.insert(item["kind"], item["value"])
                except ValueError:
                    pass
                added += 1
            except (KeyError, ValueError):
                continue
        for item in extract_constraint_items(goal, description):
            try:
                self.store.add_constraint(task.task_id, item["type"], item["text"])
            except (KeyError, ValueError):
                continue
        ActivityLog(task.task_id).emit("engine", "task",
                                       f"created: {goal[:200]} (scope={added})")
        return {"task_id": task.task_id, "goal": task.goal, "goals": len(graph.list("goal")),
                "scope": added}

    def add_hint(self, task_id: str, text: str) -> ExplorationNode:
        """Inject human steering hint read by the next planner round."""
        graph = ExplorationGraph(task_id)
        node = graph.add_node("hint", text)
        ActivityLog(task_id).emit("human", "hint", text)
        return node

    def add_intent(self, task_id: str, summary: str, asset_ids: list[int] | None = None,
                   parent_ids: list[int] | None = None, priority: int = DEFAULT_PRIORITY) -> ExplorationNode:
        """Directly inject high-priority intent like the planner main-agent add_intent."""
        for asset_id in asset_ids or []:
            asset = self.assets.get(int(asset_id))
            if asset is not None:
                verdict = AssetGate(task_id).evaluate(asset.value)
                if not verdict["allowed"]:
                    raise ValueError(verdict["reason"])
        graph = ExplorationGraph(task_id)
        node = graph.add_node("intent", summary, priority=priority)
        for parent in parent_ids or []:
            graph.add_edge(parent, node.node_id, "derived_from")
        for asset_id in asset_ids or []:
            graph.anchor(node.node_id, int(asset_id))
        ActivityLog(task_id).emit("human", "intent", f"injected #{node.node_id}: {summary}",
                                  intent_id=node.node_id)
        self.store.set_status(task_id, "running")
        return node

    def set_goals(self, task_id: str, specs: list[dict]) -> list[ExplorationNode]:
        """Replace/append decomposed objectives like set_goals; wakes the task."""
        graph = ExplorationGraph(task_id)
        created = []
        for spec in specs or []:
            text = str((spec or {}).get("text", "")).strip()
            if not text:
                continue
            node = graph.add_node("goal", text[:300], state="pending",
                                  meta={"vulnclass": str((spec or {}).get("vulnclass", ""))[:80]})
            created.append(node)
            ActivityLog(task_id).emit("planner", "goal", f"goal #{node.node_id}: {text[:160]}")
        if created:
            self.store.resume(task_id)
        return created

    def edit_goal(self, task_id: str, goal_id: int, text: str) -> bool:
        """Edit a goal node like the goals manager."""
        graph = ExplorationGraph(task_id)
        node = graph.get(int(goal_id))
        if node is None or node.kind != "goal" or not (text or "").strip():
            return False
        node.text = text.strip()[:300]
        node.updated = _now()
        graph._persist()
        ActivityLog(task_id).emit("planner", "goal", f"goal #{goal_id} edited")
        return True

    def delete_goal(self, task_id: str, goal_id: int) -> bool:
        """Delete a goal node; done tasks with no goals left stay done."""
        graph = ExplorationGraph(task_id)
        node = graph.get(int(goal_id))
        if node is None or node.kind != "goal":
            return False
        del graph.nodes[int(goal_id)]
        graph._persist()
        ActivityLog(task_id).emit("planner", "goal", f"goal #{goal_id} deleted")
        return True

    def goal_met(self, task_id: str, reason: str = "") -> bool:
        """Declare the whole task complete like goal_met (weighted, audited)."""
        graph = ExplorationGraph(task_id)
        for node in graph.list("goal"):
            graph.set_state(node.node_id, "done")
        self.store.set_status(task_id, "done")
        self.runtime.abort(task_id, "goal_met", reason[:300] or "operator declared complete")
        ActivityLog(task_id).emit("planner", "goal", f"goal_met: {reason[:200]}")
        return True

    def record_fact(self, task_id: str, text: str, evidence: str = "",
                    intent_id: int = 0) -> ExplorationNode:
        """Operator-visible fact write like recordFact."""
        graph = ExplorationGraph(task_id)
        node = graph.record_fact(text, evidence=evidence, intent_id=int(intent_id))
        ActivityLog(task_id).emit("human", "fact", text[:300], intent_id=int(intent_id))
        return node

    def run_round(self, task_id: str, workers: int = DEFAULT_WORKERS, executor=None) -> dict:
        """Run one orchestrated round invoking every subsystem in order.

        Single path, no parallel loops: scope-check, enrich, triggers/scheduler,
        planner (constraint-gated, LLM-assisted), frontier claim, worker tools
        (guard+intercept+traffic), finding report, retest, goals, compaction
        minor/major, evidence/traffic archive, notify fan-out.
        """
        record = self.store.get(task_id) or {}
        if record.get("status") == "paused":
            return {"task_id": task_id, "new_intents": 0, "executed": 0,
                    "results": [], "overview": ExplorationGraph(task_id).overview(),
                    "paused": True}
        if self.store.expired(task_id):
            self.store.set_status(task_id, "timeout")
            self.runtime.abort(task_id, "timeout", "task deadline exceeded")
            return {"task_id": task_id, "new_intents": 0, "executed": 0,
                    "results": [], "overview": ExplorationGraph(task_id).overview(),
                    "timeout": True}
        if not self.budget.check(task_id)["ok"]:
            self.runtime.abort(task_id, "budget", self.budget.check(task_id)["reason"])
            return {"task_id": task_id, "new_intents": 0, "executed": 0,
                    "results": [], "overview": ExplorationGraph(task_id).overview(),
                    "budget": self.budget.check(task_id)["reason"]}
        graph, activity, traffic, guard = self._parts(task_id)
        self.runtime.beat(task_id, workers)
        constraints = list((self.store.get(task_id) or {}).get("constraints", []))
        block = constraint_block(constraints)
        if block:
            activity.emit("planner", "constraints", block[:500])
        enriched = self._auto_enrich(task_id, graph, activity, limit=2)
        scheduler_hits = TriggerStore(task_id).due(task_id, graph, activity)
        triggers = self._drain_triggers(task_id, graph)
        for hit in scheduler_hits:
            triggers.append(hit)
            activity.emit("scheduler", "fire",
                          f"trigger #{hit.get('id')} kind={hit.get('kind')}")
        llm_hint = ""
        try:
            pool = LlmPool()
            if pool.members():
                llm_hint = pool.complete(
                    f"Task goal: {(record.get('goal', ''))[:500]}\n"
                    f"Overview: {json.dumps(graph.overview())[:2000]}\n"
                    "Suggest ONE next probe intent in one line.")[:300]
                if llm_hint:
                    activity.emit("planner", "llm", llm_hint[:300])
        except Exception:
            llm_hint = ""
        planner = Planner(task_id, self.assets, graph, activity, self.store)
        new_intents = planner.plan(triggers=triggers)
        frontier = Frontier(graph)
        claimed = []
        for _ in range(max(1, workers)):
            node = frontier.claim_next()
            if node is None:
                break
            claimed.append(node)
        results: list[dict] = []
        if claimed:
            import concurrent.futures as _futures
            budget = max(1, min(5, int(workers)))

            def _run_one(index_node) -> dict:
                index, node = index_node
                worker = Worker(f"worker-{index + 1}", task_id, self.assets, graph,
                                activity, traffic, guard, self.store)
                return worker.execute(node, executor=executor)

            with _futures.ThreadPoolExecutor(max_workers=budget) as pool:
                for outcome in pool.map(_run_one, enumerate(claimed)):
                    results.append(outcome)
            time.sleep(self.debounce_sec)
        else:
            time.sleep(self.debounce_sec)
        retested = self._auto_retest(task_id, graph, activity, traffic,
                                     executor=executor, limit=3)
        self._check_goals(task_id, graph, activity)
        compacted = ColdCompactor(graph, activity).compact()
        if int((self.budget.usage(task_id) or {}).get("rounds", 0)) % 4 == 3:
            try:
                compacted = ColdCompactor(graph, activity).compact(mode="major")
            except Exception:
                pass
        try:
            EvidenceStore(task_id).export(str(_store_path(f"evidence_{task_id}_snapshot.json")))
        except Exception:
            pass
        try:
            traffic.archive(label=f"{task_id}_round")
        except Exception:
            pass
        self.budget.record_round(task_id)
        ActivityLog(task_id).emit("engine", "round",
                                  f"new={len(new_intents)} executed={len(results)} "
                                  f"enriched={enriched} retested={retested} "
                                  f"compacted={compacted.get('compacted', 0)} "
                                  f"sched={len(scheduler_hits)} llm={'yes' if llm_hint else 'no'}")
        steps = ["lazy_scope", "lazy_asset", "lazy_enrich",
                 "lazy_planner", "lazy_frontier", "lazy_worker",
                 "lazy_guard", "lazy_traffic", "lazy_finding",
                 "lazy_retest", "lazy_compact", "lazy_trace"]
        return {"task_id": task_id, "new_intents": len(new_intents),
                "executed": len(results), "results": results,
                "enriched": enriched, "retested": retested,
                "scheduler": scheduler_hits, "steps": steps,
                "overview": ExplorationGraph(task_id).overview()}

    def _drain_triggers(self, task_id: str, graph: ExplorationGraph) -> list[dict]:
        """Build planner triggers from activity after scheduler watermark."""
        try:
            records = ActivityLog(task_id).read(50)
        except Exception:
            return []
        watermark = int(((self.store.get(task_id) or {}).get("sched", {}) or {}).get("last_trigger", 0))
        triggers: list[dict] = []
        for idx, record in enumerate(records[-10:]):
            kind = str(record.get("kind", ""))
            worker = str(record.get("worker", ""))
            trig_id = watermark + idx + 1
            if worker.startswith("worker-") and kind == "result":
                triggers.append({"kind": "done", "intent": record.get("intent_id", 0),
                                 "id": trig_id})
            elif kind == "verdict":
                triggers.append({"kind": "finding", "text": str(record.get("text", ""))[:200],
                                 "id": trig_id})
            elif worker == "human" and kind in ("hint", "intent", "goal"):
                triggers.append({"kind": "hint" if kind == "hint" else kind,
                                 "text": str(record.get("text", ""))[:200], "id": trig_id})
            elif kind == "enriched":
                triggers.append({"kind": "enriched", "text": str(record.get("text", ""))[:200],
                                 "id": trig_id})
        seen: set[str] = set()
        unique: list[dict] = []
        for item in triggers:
            key = f"{item.get('kind')}:{item.get('intent', '')}:{str(item.get('text', ''))[:60]}"
            if key not in seen:
                seen.add(key)
                unique.append(item)
        out = unique[-5:]
        if out:
            self.runtime.note_trigger(task_id, max(int(t.get("id", watermark)) for t in out))
        return out

    def _auto_enrich(self, task_id: str, graph: ExplorationGraph,
                     activity: ActivityLog, limit: int = 2) -> int:
        """Enrich untested scoped assets and record facts for the planner."""
        record = self.store.get(task_id) or {}
        scope = record.get("scope", []) or []
        if not scope:
            return 0
        try:
            cooldown = _load_json(_store_path("enrich_cooldown.json"), {"seen": {}}).get("seen", {})
        except Exception:
            cooldown = {}
        now = _now()
        fresh = {k: v for k, v in cooldown.items() if now - float(v or 0) < 300.0}
        done = 0
        for asset in self.assets.untested_for(graph, scope, limit=limit):
            if str(asset.asset_id) in fresh:
                continue
            try:
                result = enrich_asset(asset.value)
            except Exception:
                continue
            dns = result.get("dns", []) or []
            http = result.get("http", {}) or {}
            if not dns and not http:
                continue
            text = f"enrich {asset.kind} {asset.value}: dns={','.join(dns[:4])} http={http}"
            node = graph.add_node("fact", text[:600], state="done",
                                  meta={"enrich": True, "asset_id": asset.asset_id})
            graph.anchor(node.node_id, asset.asset_id)
            activity.emit("enricher", "enriched", text[:300], intent_id=0)
            fresh[str(asset.asset_id)] = now
            done += 1
        try:
            _save_json(_store_path("enrich_cooldown.json"), {"seen": fresh})
        except Exception:
            pass
        return done

    def _auto_retest(self, task_id: str, graph: ExplorationGraph, activity: ActivityLog,
                     traffic: TrafficLog, executor=None, limit: int = 3) -> int:
        """Automatically retest pending findings to a verdict."""
        done = 0
        retester = Retester(graph, activity, traffic)
        for node in graph.list("finding", "pending")[: max(1, limit)]:
            try:
                retester.retest(node.node_id, executor=executor)
                done += 1
            except (KeyError, ValueError):
                continue
        return done

    def run(self, task_id: str, max_rounds: int = DEFAULT_MAX_ROUNDS,
            workers: int = DEFAULT_WORKERS, executor=None,
            timeout_sec: float = 0.0) -> dict:
        """Drive rounds until goals met, frontier drains, or budget exhausts."""
        if timeout_sec:
            self.store.set_deadline(task_id, timeout_sec)
            self.budget.set_limits(task_id, timeout_sec=timeout_sec)
        self.budget.set_limits(task_id, max_rounds=max_rounds)
        self.runtime.beat(task_id, workers)
        rounds = []
        for _ in range(max(1, max_rounds)):
            if (self.store.get(task_id) or {}).get("status") == "paused":
                self.runtime.abort(task_id, "paused", "run loop yielded on pause")
                break
            if self.store.expired(task_id):
                self.store.set_status(task_id, "timeout")
                self.runtime.abort(task_id, "timeout", "task deadline exceeded")
                break
            if not self.budget.check(task_id)["ok"]:
                self.runtime.abort(task_id, "budget", self.budget.check(task_id)["reason"])
                break
            summary = self.run_round(task_id, workers=workers, executor=executor)
            rounds.append({"new_intents": summary["new_intents"], "executed": summary["executed"]})
            if self._goals_met(task_id):
                self.store.set_status(task_id, "done")
                self.runtime.abort(task_id, "goal_met", "every goal done")
                break
            if summary["new_intents"] == 0 and summary["executed"] == 0:
                if not self._goals_met(task_id):
                    continue
                self.store.set_status(task_id, "done")
                self.runtime.abort(task_id, "goal_met", "drained with goals met")
                break
        record = self.store.get(task_id) or {}
        if record.get("status") == "running" and not self._goals_met(task_id):
            self.store.set_status(task_id, "exhausted")
            record = self.store.get(task_id) or {}
        archived = ""
        if record.get("status") in ("done", "exhausted", "timeout"):
            try:
                archived = TaskArchive().save(task_id).get("path", "")
            except Exception:
                archived = ""
        return {"task_id": task_id, "status": record.get("status", "done"),
                "rounds": len(rounds), "detail": rounds, "archive": archived,
                "overview": ExplorationGraph(task_id).overview()}

    def prove_goal(self, task_id: str, goal_id: int, evidence_id: int, reason: str) -> bool:
        """Mark goal met with finding/fact evidence like the planner prove_goal.

        Refuses quantitative goals (coverage %, N flags) unless the
        overview actually satisfies them — never stamp early.
        """
        graph = ExplorationGraph(task_id)
        goal = graph.get(goal_id)
        evidence = graph.get(evidence_id)
        if goal is None or evidence is None or goal.kind != "goal":
            return False
        if evidence.kind not in ("finding", "fact"):
            return False
        lowered = goal.text.lower()
        if any(mark in lowered for mark in ("100%", "coverage", "all ports", "every")):
            record = self.store.get(task_id) or {}
            coverage = self.assets.coverage_for(graph, record.get("scope", []))
            if float(coverage.get("pct", 0.0)) < 100.0:
                ActivityLog(task_id).emit("planner", "skip",
                                          f"goal #{goal_id} quantitative bar unmet "
                                          f"({coverage.get('pct', 0)}%)")
                return False
        if not (reason or "").strip():
            return False
        graph.add_edge(evidence_id, goal_id, "proves")
        graph.set_state(goal_id, "done")
        ActivityLog(task_id).emit("planner", "goal", f"goal #{goal_id} proven by #{evidence_id}: {reason[:200]}")
        if self._goals_met(task_id):
            self.store.set_status(task_id, "done")
        else:
            self.store.resume(task_id)
        return True

    def _check_goals(self, task_id: str, graph: ExplorationGraph, activity: ActivityLog) -> None:
        """Auto-prove goals whose text appears in a finding."""
        for goal in graph.list("goal", "pending"):
            for finding in graph.list("finding"):
                if goal.text[:40].lower() in finding.text.lower():
                    self.prove_goal(task_id, goal.node_id, finding.node_id, "finding text entails goal")

    def _goals_met(self, task_id: str) -> bool:
        """Report whether every goal node is done."""
        graph = ExplorationGraph(task_id)
        goals = graph.list("goal")
        return bool(goals) and all(g.state == "done" for g in goals)

    def status(self, task_id: str) -> dict:
        """Return full inspectable state for one task."""
        record = self.store.get(task_id) or {}
        graph = ExplorationGraph(task_id)
        activity = ActivityLog(task_id)
        return {"task": record, "overview": graph.overview(),
                "coverage": self.assets.coverage_for(graph, record.get("scope", [])),
                "todos": TodoStore(task_id).as_list(),
                "recent": activity.read(10),
                "runtime": self.runtime.heartbeat(task_id),
                "budget": {"limits": self.budget.limits(task_id),
                           "used": self.budget.usage(task_id),
                           "check": self.budget.check(task_id)},
                "intercept_pending": len(InterceptQueue(task_id).pending())}

    def graph_overview(self, task_id: str) -> dict:
        """Return planner-facing overview plus coverage and scope."""
        record = self.store.get(task_id) or {}
        graph = ExplorationGraph(task_id)
        overview = graph.overview()
        overview["coverage"] = self.assets.coverage_for(graph, record.get("scope", []))
        overview["scope"] = record.get("scope", [])
        overview["constraints"] = record.get("constraints", [])
        overview["runtime"] = self.runtime.heartbeat(task_id)
        overview["budget"] = {"limits": self.budget.limits(task_id),
                              "used": self.budget.usage(task_id)}
        return overview


__all__ = ["LazyLoopEngine", "AssetGraph", "AssetGate", "ExplorationGraph", "Frontier", "Planner",
           "Worker", "Guard", "Retester", "TodoStore", "TaskStore", "ActivityLog",
           "TrafficLog", "ColdCompactor", "Budget", "RuntimeTracker", "InterceptQueue",
           "FindingService", "EvidenceStore", "Notifier", "TriggerStore", "LlmPool",
           "ToolCatalog", "SideQuestions", "CompanyScope", "TaskArchive",
           "TaskTemplate", "TaskCategory", "TaskChat",
           "TOOL_DEFAULTS", "decompose_goals", "enrich_asset", "constraint_block",
           "finding_severity", "extract_scope_items", "extract_constraint_items",
           "load_intel_scores", "resolve_target"]
