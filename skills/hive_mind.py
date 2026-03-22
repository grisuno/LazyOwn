#!/usr/bin/env python3
"""
skills/hive_mind.py — LazyOwn Borg Hive Mind
==============================================
Multi-agent cognitive architecture where Claude (MCP) is the Queen/Mainframe
and Groq/Ollama agents are satellite drones executing in parallel.

Architecture
────────────
  HiveMemory      — Unified ChromaDB (semantic) + SQLite (episodic) + Parquet (long-term)
  QueenBrain      — Orchestrator: plan → delegate → synthesize (Claude is here via MCP)
  DronePool       — Parallel Groq/Ollama agents with specialised roles
  HiveBus         — In-memory message bus between queen and drones
  HiveMind        — Top-level coordinator, exposed as MCP tools

Memory layers
─────────────
  working    — current task context (dict in memory, shared via bus)
  episodic   — SQLite FTS5: events, commands, outcomes per session
  semantic   — ChromaDB vectors: similarity search across all agents
  longterm   — Parquet: compressed historical knowledge

Drone roles
───────────
  recon      — host/port/service discovery
  exploit    — vulnerability analysis and exploitation
  analyze    — log/output analysis, pattern detection
  cred       — credential hunting and cracking
  lateral    — lateral movement and pivoting
  report     — synthesis and documentation
  generic    — any goal (default)

MCP tools added to lazyown_mcp.py
──────────────────────────────────
  lazyown_hive_spawn     — spawn N drones for a goal (parallel)
  lazyown_hive_status    — hive-wide status + memory stats
  lazyown_hive_recall    — semantic recall from ChromaDB
  lazyown_hive_plan      — queen generates task decomposition
  lazyown_hive_result    — get aggregated drone results
  lazyown_hive_forget    — prune hive memory by topic/age

Usage
─────
  from hive_mind import get_hive
  hive = get_hive()
  run_ids = hive.queen.plan_and_dispatch("Enumerate AD on 10.10.11.78")
  status  = hive.status()
  result  = hive.collect(run_ids)

  python3 skills/hive_mind.py spawn "Enumerate SMB" --drones 3 --wait
  python3 skills/hive_mind.py status
  python3 skills/hive_mind.py recall "kerberos hash"
"""

from __future__ import annotations

import asyncio
import hashlib
import json
import logging
import os
import sys
import threading
import time
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Tuple

# ── Paths ──────────────────────────────────────────────────────────────────────
# Mirror lazyown_mcp.py: respect LAZYOWN_DIR env override for consistency.

SKILLS_DIR   = Path(__file__).parent
LAZYOWN_DIR  = Path(os.environ.get("LAZYOWN_DIR", str(SKILLS_DIR.parent)))
SESSIONS_DIR = LAZYOWN_DIR / "sessions"
PARQUETS_DIR = LAZYOWN_DIR / "parquets"
HIVE_DIR     = SESSIONS_DIR / "hive"
HIVE_DIR.mkdir(parents=True, exist_ok=True)

sys.path.insert(0, str(SKILLS_DIR))
sys.path.insert(0, str(LAZYOWN_DIR / "modules"))

log = logging.getLogger("hive_mind")

# ── Optional ChromaDB ──────────────────────────────────────────────────────────

try:
    import chromadb
    from chromadb.config import Settings as _ChromaSettings
    _CHROMA_OK = True
except ImportError:
    _CHROMA_OK = False

# ── Optional sentence-transformers (local embeddings) ─────────────────────────

try:
    from sentence_transformers import SentenceTransformer as _ST
    _EMBED_MODEL = _ST("all-MiniLM-L6-v2")
    _EMBED_OK    = True
except Exception:
    _EMBED_OK = False
    _EMBED_MODEL = None  # type: ignore[assignment]

# ── Optional numpy ────────────────────────────────────────────────────────────

try:
    import numpy as np
    _NUMPY_OK = True
except ImportError:
    _NUMPY_OK = False

# ─────────────────────────────────────────────────────────────────────────────
# SECTION 1 — HiveMemory  (ChromaDB + SQLite + Parquet)
# ─────────────────────────────────────────────────────────────────────────────


class HiveMemory:
    """
    Unified three-layer memory shared across all hive agents.

    Layer 1 — episodic  : SQLite, fast FTS5 keyword search
    Layer 2 — semantic  : ChromaDB, vector similarity (optional)
    Layer 3 — longterm  : Parquet files in parquets/ (read-only from here)
    """

    _DDL_STMTS = [
        """CREATE TABLE IF NOT EXISTS hive_events (
            rowid       INTEGER PRIMARY KEY AUTOINCREMENT,
            id          TEXT NOT NULL UNIQUE,
            agent_id    TEXT NOT NULL,
            role        TEXT NOT NULL DEFAULT 'generic',
            event_type  TEXT NOT NULL DEFAULT 'observation',
            content     TEXT NOT NULL,
            meta_json   TEXT NOT NULL DEFAULT '{}',
            ts          REAL NOT NULL,
            session_tag TEXT NOT NULL DEFAULT ''
        )""",
        "CREATE VIRTUAL TABLE IF NOT EXISTS hive_fts USING fts5(content, tokenize='porter ascii')",
        """CREATE TRIGGER IF NOT EXISTS hive_ai AFTER INSERT ON hive_events BEGIN
            INSERT INTO hive_fts(rowid, content) VALUES (new.rowid, new.content);
        END""",
    ]

    def __init__(self, db_path: Optional[Path] = None) -> None:
        import sqlite3
        self._db_path = db_path or (HIVE_DIR / "hive_memory.db")
        self._lock    = threading.RLock()
        self._conn    = self._connect()
        self._chroma  = self._init_chroma()

    def _connect(self):
        import sqlite3
        conn = sqlite3.connect(str(self._db_path), check_same_thread=False)
        conn.execute("PRAGMA journal_mode=WAL")
        for stmt in self._DDL_STMTS:
            try:
                conn.execute(stmt)
            except Exception:
                pass
        conn.commit()
        return conn

    def _init_chroma(self):
        if not _CHROMA_OK:
            return None
        try:
            client = chromadb.PersistentClient(
                path=str(HIVE_DIR / "chroma"),
            )
            return client.get_or_create_collection(
                name="hive_memory",
                metadata={"hnsw:space": "cosine"},
            )
        except Exception as exc:
            log.warning("ChromaDB init failed: %s", exc)
            return None

    # ── Write ──────────────────────────────────────────────────────────────────

    def store(
        self,
        content: str,
        agent_id: str = "queen",
        role: str = "generic",
        event_type: str = "observation",
        meta: Optional[Dict] = None,
        session_tag: str = "",
    ) -> str:
        """Store content in episodic + semantic layers. Returns event_id."""
        event_id   = uuid.uuid4().hex
        ts         = time.time()
        meta_json  = json.dumps(meta or {}, ensure_ascii=False)

        with self._lock:
            try:
                self._conn.execute(
                    """INSERT OR IGNORE INTO hive_events
                       (id, agent_id, role, event_type, content, meta_json, ts, session_tag)
                       VALUES (?,?,?,?,?,?,?,?)""",
                    (event_id, agent_id, role, event_type, content[:8000],
                     meta_json, ts, session_tag),
                )
                self._conn.commit()
            except Exception as exc:
                log.error("SQLite store error: %s", exc)
                return event_id

        # Vector store (async-safe — ChromaDB is thread-safe)
        if self._chroma is not None:
            try:
                embedding = self._embed(content)
                self._chroma.add(
                    ids=[event_id],
                    documents=[content[:2000]],
                    embeddings=[embedding] if embedding else None,
                    metadatas=[{
                        "agent_id":   agent_id,
                        "role":       role,
                        "event_type": event_type,
                        "ts":         str(ts),
                        "session":    session_tag,
                    }],
                )
            except Exception as exc:
                log.debug("ChromaDB store error: %s", exc)

        return event_id

    # ── Recall — episodic (FTS) ────────────────────────────────────────────────

    def recall_episodic(
        self,
        query: str,
        top_k: int = 10,
        role: Optional[str] = None,
        event_type: Optional[str] = None,
    ) -> List[Dict]:
        """Keyword search across hive episodic memory."""
        with self._lock:
            try:
                extra_filters: List[str] = []
                params: List[Any] = [query]
                if role:
                    extra_filters.append("e.role = ?")
                    params.append(role)
                if event_type:
                    extra_filters.append("e.event_type = ?")
                    params.append(event_type)
                params.append(top_k)
                extra_where = ("AND " + " AND ".join(extra_filters)) if extra_filters else ""
                sql = f"""
                    SELECT e.id, e.agent_id, e.role, e.event_type,
                           e.content, e.meta_json, e.ts
                    FROM hive_events e
                    JOIN hive_fts f ON f.rowid = e.rowid
                    WHERE hive_fts MATCH ? {extra_where}
                    ORDER BY rank LIMIT ?
                """
                cur = self._conn.execute(sql, params)
                rows = cur.fetchall()
                return [
                    {
                        "id": r[0], "agent_id": r[1], "role": r[2],
                        "event_type": r[3], "content": r[4][:500],
                        "meta": json.loads(r[5]), "ts": r[6],
                    }
                    for r in rows
                ]
            except Exception as exc:
                log.error("Recall episodic error: %s", exc)
                return []

    # ── Recall — semantic (ChromaDB) ──────────────────────────────────────────

    def recall_semantic(
        self,
        query: str,
        top_k: int = 8,
        where: Optional[Dict] = None,
    ) -> List[Dict]:
        """Vector similarity search in ChromaDB."""
        if self._chroma is None:
            return self.recall_episodic(query, top_k)
        try:
            embedding = self._embed(query)
            kw: Dict[str, Any] = {"n_results": top_k, "include": ["documents", "metadatas", "distances"]}
            if embedding:
                kw["query_embeddings"] = [embedding]
            else:
                kw["query_texts"] = [query]
            if where:
                kw["where"] = where
            res = self._chroma.query(**kw)
            docs   = res.get("documents",  [[]])[0]
            metas  = res.get("metadatas",  [[]])[0]
            dists  = res.get("distances",  [[]])[0]
            ids_   = res.get("ids",        [[]])[0]
            return [
                {
                    "id":         ids_[i],
                    "content":    docs[i],
                    "meta":       metas[i],
                    "similarity": round(1.0 - dists[i], 4),
                }
                for i in range(len(docs))
            ]
        except Exception as exc:
            log.debug("ChromaDB recall error: %s — falling back to FTS", exc)
            return self.recall_episodic(query, top_k)

    # ── Recall — long-term (Parquet) ──────────────────────────────────────────

    def recall_longterm(self, query: str, top_k: int = 10) -> List[Dict]:
        """Keyword search across Parquet knowledge files."""
        try:
            from lazyown_parquet_db import get_pdb
            pdb = get_pdb()
            if pdb is None:
                return []
            # Use query_knowledge for keyword search; query_session has no keyword param
            if hasattr(pdb, "query_knowledge"):
                rows = pdb.query_knowledge(keyword=query, limit=top_k)
            else:
                all_rows = pdb.query_session(limit=50)
                q_low = query.lower()
                rows = [r for r in all_rows
                        if q_low in str(r.get("command", "")).lower()
                        or q_low in str(r.get("outcome", "")).lower()][:top_k]
            return [
                {
                    "id":      r.get("id", ""),
                    "content": (
                        f"[{r.get('phase', r.get('category','?'))}] "
                        f"{r.get('command','?')} → {r.get('outcome','?')}"
                    ),
                    "meta":    {"phase": r.get("phase", r.get("category","")), "source": "parquet"},
                    "similarity": None,
                }
                for r in rows
            ]
        except Exception as exc:
            log.debug("Parquet recall error: %s", exc)
            return []

    # ── Unified recall (all layers) ───────────────────────────────────────────

    def recall(self, query: str, top_k: int = 10) -> List[Dict]:
        """
        Unified recall: semantic (ChromaDB) + episodic (SQLite) + longterm (Parquet).
        Deduplicates by content hash.
        """
        seen: set = set()
        results: List[Dict] = []

        for item in self.recall_semantic(query, top_k=top_k):
            key = hashlib.md5(item["content"][:200].encode()).hexdigest()
            if key not in seen:
                seen.add(key)
                item["layer"] = "semantic"
                results.append(item)

        for item in self.recall_longterm(query, top_k=top_k // 2 + 1):
            key = hashlib.md5(item["content"][:200].encode()).hexdigest()
            if key not in seen:
                seen.add(key)
                item["layer"] = "longterm"
                results.append(item)

        return results[:top_k]

    # ── Stats ──────────────────────────────────────────────────────────────────

    def stats(self) -> Dict[str, Any]:
        with self._lock:
            total = self._conn.execute("SELECT COUNT(*) FROM hive_events").fetchone()[0]
            agents = self._conn.execute(
                "SELECT COUNT(DISTINCT agent_id) FROM hive_events"
            ).fetchone()[0]
        chroma_count = 0
        if self._chroma is not None:
            try:
                chroma_count = self._chroma.count()
            except Exception:
                pass
        return {
            "episodic_events": total,
            "unique_agents":   agents,
            "chroma_vectors":  chroma_count,
            "chroma_enabled":  _CHROMA_OK,
            "embed_enabled":   _EMBED_OK,
        }

    # ── Forget ────────────────────────────────────────────────────────────────

    def forget(self, older_than_hours: float = 24.0, topic: str = "") -> int:
        """Prune old or topic-matched entries. Returns number pruned."""
        cutoff = time.time() - older_than_hours * 3600
        with self._lock:
            if topic:
                cur = self._conn.execute(
                    "DELETE FROM hive_events WHERE ts < ? AND content LIKE ?",
                    (cutoff, f"%{topic}%"),
                )
            else:
                cur = self._conn.execute(
                    "DELETE FROM hive_events WHERE ts < ?", (cutoff,)
                )
            self._conn.commit()
            return cur.rowcount

    # ── Internal: embeddings ──────────────────────────────────────────────────

    def _embed(self, text: str) -> Optional[List[float]]:
        if not _EMBED_OK or _EMBED_MODEL is None:
            return None
        try:
            vec = _EMBED_MODEL.encode(text[:512], show_progress_bar=False)
            if _NUMPY_OK:
                return vec.tolist()
            return list(vec)
        except Exception:
            return None


# ─────────────────────────────────────────────────────────────────────────────
# SECTION 2 — HiveBus  (message passing between queen and drones)
# ─────────────────────────────────────────────────────────────────────────────


@dataclass
class HiveMessage:
    """A message on the hive bus."""
    msg_id:    str = field(default_factory=lambda: uuid.uuid4().hex[:8])
    sender:    str = "queen"
    recipient: str = "*"          # "*" = broadcast
    kind:      str = "task"       # task | result | signal | heartbeat
    payload:   Dict = field(default_factory=dict)
    ts:        float = field(default_factory=time.time)


class HiveBus:
    """
    Simple thread-safe in-process message bus.
    Agents subscribe to their own mailbox (recipient == agent_id or "*").
    """

    def __init__(self) -> None:
        self._lock    = threading.Lock()
        self._mailbox: Dict[str, List[HiveMessage]] = {}   # recipient → [msgs]

    def publish(self, msg: HiveMessage) -> None:
        with self._lock:
            for recipient in (msg.recipient, "*"):
                self._mailbox.setdefault(recipient, []).append(msg)

    def receive(self, agent_id: str, max_msgs: int = 10) -> List[HiveMessage]:
        """Drain mailbox for agent_id (includes broadcast)."""
        with self._lock:
            direct    = self._mailbox.pop(agent_id, [])
            broadcast = self._mailbox.get("*", [])
            # Keep broadcast for others — only drain own direct
            combined = direct + broadcast
            return combined[:max_msgs]

    def ack_broadcast(self, agent_id: str, msg_id: str) -> None:
        """Mark a broadcast message as seen by agent_id (not implemented — simple bus)."""
        pass  # noqa: WPS420 — intentionally minimal

    def pending_count(self, agent_id: str) -> int:
        with self._lock:
            return len(self._mailbox.get(agent_id, [])) + len(self._mailbox.get("*", []))


# ─────────────────────────────────────────────────────────────────────────────
# SECTION 3 — DroneAgent  (satellite Groq/Ollama agent)
# ─────────────────────────────────────────────────────────────────────────────

# Role → system prompt focus
_ROLE_FOCUS: Dict[str, str] = {
    "recon":   "You specialise in host discovery, port scanning, and service fingerprinting.",
    "exploit": "You specialise in vulnerability analysis, CVE research, and exploitation.",
    "analyze": "You specialise in log analysis, output parsing, and pattern detection.",
    "cred":    "You specialise in credential hunting, hash cracking, and auth bypass.",
    "lateral": "You specialise in lateral movement, pivoting, and network traversal.",
    "report":  "You specialise in synthesising findings into structured, actionable reports.",
    "generic": "You are a general-purpose red-team assistant.",
}

# Role → preferred tool subset
_ROLE_TOOLS: Dict[str, List[str]] = {
    "recon":   ["run_command", "facts_show", "bridge_suggest", "rag_query", "cve_lookup",
                "parquet_context", "memory_search", "session_status"],
    "exploit": ["run_command", "cve_lookup", "searchsploit", "bridge_suggest",
                "atomic_search", "parquet_context", "reactive_suggest", "rag_query"],
    "analyze": ["run_command", "rag_query", "memory_search", "reactive_suggest",
                "threat_model", "facts_show", "parquet_context"],
    "cred":    ["run_command", "bridge_suggest", "memory_search", "parquet_context",
                "reactive_suggest", "facts_show", "session_status"],
    "lateral": ["run_command", "bridge_suggest", "session_status", "c2_status",
                "c2_command", "reactive_suggest", "parquet_context"],
    "report":  ["run_command", "rag_query", "threat_model", "facts_show",
                "parquet_context", "task_list", "memory_search"],
    "generic": [],   # all tools
}


@dataclass
class DroneState:
    drone_id:  str
    role:      str
    goal:      str
    backend:   str     # groq | ollama
    status:    str = "queued"   # queued|running|completed|failed
    result:    str = ""
    error:     str = ""
    started:   float = 0.0
    finished:  float = 0.0
    iterations: int = 0
    tokens_in:  int = 0
    tokens_out: int = 0


class DroneAgent:
    """
    A satellite agent running on Groq or Ollama.
    Reports back to hive memory on completion.
    """

    def __init__(
        self,
        drone_id: str,
        role: str,
        goal: str,
        backend: str,
        memory: HiveMemory,
        bus: HiveBus,
        max_iterations: int = 10,
        api_key: Optional[str] = None,
        model: Optional[str] = None,
    ) -> None:
        self.state    = DroneState(
            drone_id=drone_id, role=role, goal=goal, backend=backend,
        )
        self._memory  = memory
        self._bus     = bus
        self._max_it  = max_iterations
        self._api_key = api_key
        self._model   = model
        self._thread: Optional[threading.Thread] = None

    def start(self) -> None:
        self._thread = threading.Thread(
            target=self._run,
            name=f"drone-{self.state.drone_id}-{self.state.role}",
            daemon=True,
        )
        self._thread.start()

    def join(self, timeout: Optional[float] = None) -> None:
        if self._thread:
            self._thread.join(timeout=timeout)

    def _run(self) -> None:
        s = self.state
        s.status  = "running"
        s.started = time.time()

        # Announce to hive
        self._memory.store(
            content=f"[DRONE STARTED] role={s.role} goal={s.goal[:200]}",
            agent_id=s.drone_id,
            role=s.role,
            event_type="lifecycle",
        )

        try:
            from lazyown_llm import LLMBridge
            from lazyown_groq_agents import REGISTRY

            key = (
                self._api_key
                or self._load_payload_key()
                or os.environ.get("GROQ_API_KEY", "")
            )
            bridge = LLMBridge(backend=s.backend, model=self._model, api_key=key)

            # Register role-filtered tools
            tool_names = _ROLE_TOOLS.get(s.role) or list(REGISTRY.keys())
            for name in tool_names:
                if name in REGISTRY:
                    desc, params, func = REGISTRY[name]
                    bridge.register_tool(name, desc, params, func)

            # Build system prompt with hive context
            hive_ctx = self._build_hive_context()
            sys_prompt = self._build_system_prompt(list(bridge._tools.keys()), hive_ctx)

            answer = bridge.ask(
                goal=s.goal,
                max_iterations=self._max_it,
                system_prompt=sys_prompt,
            )
            s.result  = answer
            s.status  = "completed"

        except Exception as exc:
            s.error  = str(exc)
            s.status = "failed"
            answer   = f"[FAILED] {exc}"

        finally:
            s.finished = time.time()

        # Write result to hive memory
        self._memory.store(
            content=f"[DRONE RESULT] role={s.role} goal={s.goal[:100]}\n{answer[:2000]}",
            agent_id=s.drone_id,
            role=s.role,
            event_type="result",
            meta={"status": s.status, "duration_s": round(s.finished - s.started, 2)},
        )

        # Publish result on bus
        self._bus.publish(HiveMessage(
            sender=s.drone_id,
            recipient="queen",
            kind="result",
            payload={
                "drone_id": s.drone_id,
                "role":     s.role,
                "goal":     s.goal[:200],
                "status":   s.status,
                "result":   answer[:4000],
                "duration": round(s.finished - s.started, 2),
            },
        ))

    def _build_hive_context(self) -> str:
        """Pull relevant memories to seed this drone's context."""
        items = self._memory.recall(self.state.goal, top_k=5)
        if not items:
            return ""
        lines = ["=== Hive Memory Context ==="]
        for item in items:
            layer = item.get("layer", "?")
            lines.append(f"[{layer}] {item['content'][:300]}")
        return "\n".join(lines)

    def _build_system_prompt(self, tool_names: List[str], hive_ctx: str) -> str:
        role_focus = _ROLE_FOCUS.get(self.state.role, _ROLE_FOCUS["generic"])
        base = (
            f"You are a LazyOwn hive-mind drone. Role: {self.state.role.upper()}.\n"
            f"{role_focus}\n"
            "Rules:\n"
            "- Use ONLY real tool output — never fabricate results.\n"
            "- After each command, analyse the output with reactive_suggest.\n"
            "- Report ALL credentials, hostnames, and access levels you find.\n"
            "- Be concise and structured.\n"
            f"Available tools: {', '.join(tool_names)}.\n"
        )
        if hive_ctx:
            base += f"\n{hive_ctx}\n"
        return base

    @staticmethod
    def _load_payload_key() -> str:
        try:
            payload = json.loads((LAZYOWN_DIR / "payload.json").read_text())
            return payload.get("api_key", "") or payload.get("groq_api_key", "")
        except Exception:
            return ""


# ─────────────────────────────────────────────────────────────────────────────
# SECTION 4 — QueenBrain  (orchestrator — Claude's cognitive interface)
# ─────────────────────────────────────────────────────────────────────────────

# Task decomposition templates per objective type
_DECOMPOSITION_TEMPLATES: Dict[str, List[Dict]] = {
    "enum": [
        {"role": "recon",   "goal_suffix": "— host discovery and port scanning"},
        {"role": "analyze", "goal_suffix": "— service version fingerprinting"},
        {"role": "cred",    "goal_suffix": "— anonymous access and default credentials"},
    ],
    "exploit": [
        {"role": "recon",   "goal_suffix": "— confirm target services and versions"},
        {"role": "exploit", "goal_suffix": "— CVE research and exploit selection"},
        {"role": "analyze", "goal_suffix": "— post-exploit output analysis"},
    ],
    "ad": [
        {"role": "recon",   "goal_suffix": "— AD enumeration (users, groups, GPOs)"},
        {"role": "cred",    "goal_suffix": "— Kerberoasting and AS-REP roasting"},
        {"role": "lateral", "goal_suffix": "— lateral movement and privilege escalation"},
        {"role": "report",  "goal_suffix": "— synthesis of AD attack path"},
    ],
    "generic": [
        {"role": "recon",   "goal_suffix": ""},
        {"role": "analyze", "goal_suffix": ""},
        {"role": "report",  "goal_suffix": "— synthesis"},
    ],
}


def _classify_objective(goal: str) -> str:
    g = goal.lower()
    if any(k in g for k in ("ad ", "active directory", "kerberos", "ldap", "domain")):
        return "ad"
    if any(k in g for k in ("exploit", "cve", "rce", "lfi", "sqli", "shell")):
        return "exploit"
    if any(k in g for k in ("enum", "scan", "nmap", "discover", "service")):
        return "enum"
    return "generic"


class QueenBrain:
    """
    The queen orchestrates the hive:
      1. plan(goal)       — decompose into drone tasks
      2. dispatch(tasks)  — spawn drones in parallel
      3. collect(ids)     — wait and aggregate results
      4. synthesize(results) — final summary written to hive memory

    Claude Code IS the queen — this class is the programmatic shim that lets
    the MCP tools interact with the drone pool and hive memory.
    """

    def __init__(
        self,
        memory: HiveMemory,
        bus: HiveBus,
        pool: "DronePool",
    ) -> None:
        self._memory = memory
        self._bus    = bus
        self._pool   = pool

    def plan(self, goal: str, n_drones: int = 0) -> List[Dict]:
        """
        Decompose a high-level goal into per-drone task specs.
        Returns list of {role, goal} dicts.
        """
        obj_type = _classify_objective(goal)
        template = _DECOMPOSITION_TEMPLATES.get(obj_type, _DECOMPOSITION_TEMPLATES["generic"])

        tasks = []
        for spec in template:
            suffix = spec["goal_suffix"]
            task_goal = f"{goal} {suffix}".strip()
            tasks.append({"role": spec["role"], "goal": task_goal})

        # If caller wants more drones than template provides, pad with generic
        while n_drones and len(tasks) < n_drones:
            tasks.append({"role": "generic", "goal": goal})

        return tasks

    def dispatch(
        self,
        tasks: List[Dict],
        backend: str = "groq",
        api_key: Optional[str] = None,
        max_iterations: int = 10,
    ) -> List[str]:
        """Spawn one drone per task in parallel. Returns list of drone_ids."""
        drone_ids = []
        for task in tasks:
            drone_id = self._pool.spawn(
                role=task.get("role", "generic"),
                goal=task["goal"],
                backend=backend,
                api_key=api_key,
                max_iterations=max_iterations,
            )
            drone_ids.append(drone_id)

        self._memory.store(
            content=f"[QUEEN] Dispatched {len(drone_ids)} drones for: {tasks[0]['goal'][:120]}",
            agent_id="queen",
            event_type="dispatch",
            meta={"drone_ids": drone_ids, "task_count": len(tasks)},
        )
        return drone_ids

    def plan_and_dispatch(
        self,
        goal: str,
        n_drones: int = 0,
        backend: str = "groq",
        api_key: Optional[str] = None,
        max_iterations: int = 10,
    ) -> List[str]:
        """Convenience: plan + dispatch in one call."""
        tasks = self.plan(goal, n_drones=n_drones)
        return self.dispatch(tasks, backend=backend, api_key=api_key,
                             max_iterations=max_iterations)

    def collect(
        self,
        drone_ids: List[str],
        timeout: float = 300.0,
        poll_interval: float = 2.0,
    ) -> Dict[str, Any]:
        """
        Wait for all drones to finish (up to timeout seconds).
        Returns aggregated results dict.
        """
        deadline = time.time() + timeout
        while time.time() < deadline:
            states = [self._pool.get_state(did) for did in drone_ids]
            pending = [s for s in states if s and s.status in ("queued", "running")]
            if not pending:
                break
            time.sleep(poll_interval)

        results = {}
        for did in drone_ids:
            s = self._pool.get_state(did)
            if s:
                results[did] = {
                    "role":     s.role,
                    "status":   s.status,
                    "result":   s.result[:3000] if s.result else s.error,
                    "duration": round(s.finished - s.started, 2) if s.finished else 0,
                }
        return results

    def synthesize(self, drone_ids: List[str], original_goal: str) -> str:
        """
        Read hive memory results for these drones and produce a synthesis summary.
        Written back to hive memory by the queen.
        """
        results = self.collect(drone_ids, timeout=0)   # non-blocking snapshot
        lines   = [f"# Hive Synthesis: {original_goal[:100]}", ""]
        total_ok = sum(1 for r in results.values() if r["status"] == "completed")
        lines.append(f"**Drones:** {len(drone_ids)} | **Completed:** {total_ok}")
        lines.append("")
        for did, r in results.items():
            lines.append(f"## Drone {did} [{r['role']}] — {r['status']} ({r['duration']}s)")
            lines.append(r["result"])
            lines.append("")

        summary = "\n".join(lines)
        self._memory.store(
            content=summary[:6000],
            agent_id="queen",
            event_type="synthesis",
            meta={"drone_ids": drone_ids, "goal": original_goal[:200]},
        )
        return summary

    def read_bus(self) -> List[HiveMessage]:
        """Drain queen's mailbox from drone result messages."""
        return self._bus.receive("queen")


# ─────────────────────────────────────────────────────────────────────────────
# SECTION 5 — DronePool  (manages all live drone threads)
# ─────────────────────────────────────────────────────────────────────────────


class DronePool:
    """Registry of all spawned drones with their state and threads."""

    def __init__(self, memory: HiveMemory, bus: HiveBus) -> None:
        self._memory  = memory
        self._bus     = bus
        self._drones: Dict[str, DroneAgent] = {}
        self._lock    = threading.Lock()

    def spawn(
        self,
        role: str,
        goal: str,
        backend: str = "groq",
        api_key: Optional[str] = None,
        model: Optional[str] = None,
        max_iterations: int = 10,
    ) -> str:
        drone_id = f"{role[:4]}-{uuid.uuid4().hex[:6]}"
        drone    = DroneAgent(
            drone_id=drone_id,
            role=role,
            goal=goal,
            backend=backend,
            memory=self._memory,
            bus=self._bus,
            max_iterations=max_iterations,
            api_key=api_key,
            model=model,
        )
        with self._lock:
            self._drones[drone_id] = drone
        drone.start()
        return drone_id

    def get_state(self, drone_id: str) -> Optional[DroneState]:
        with self._lock:
            d = self._drones.get(drone_id)
        return d.state if d else None

    def list_all(self, limit: int = 30) -> List[Dict]:
        with self._lock:
            items = list(self._drones.values())
        items.sort(key=lambda d: d.state.started, reverse=True)
        return [
            {
                "drone_id": d.state.drone_id,
                "role":     d.state.role,
                "status":   d.state.status,
                "backend":  d.state.backend,
                "goal":     d.state.goal[:80],
                "duration": round(d.state.finished - d.state.started, 1)
                            if d.state.finished else None,
            }
            for d in items[:limit]
        ]

    def active_count(self) -> int:
        with self._lock:
            return sum(
                1 for d in self._drones.values()
                if d.state.status in ("queued", "running")
            )


# ─────────────────────────────────────────────────────────────────────────────
# SECTION 6 — HiveMind  (top-level singleton)
# ─────────────────────────────────────────────────────────────────────────────


class HiveMind:
    """
    Top-level hive coordinator.
    Singleton — use get_hive() to obtain the instance.
    """

    def __init__(self) -> None:
        self.memory = HiveMemory()
        self.bus    = HiveBus()
        self._pool  = DronePool(self.memory, self.bus)
        self.queen  = QueenBrain(self.memory, self.bus, self._pool)

    # ── Convenience methods (called from MCP tools) ───────────────────────────

    def spawn(
        self,
        goal: str,
        role: str = "generic",
        backend: str = "groq",
        api_key: Optional[str] = None,
        max_iterations: int = 10,
    ) -> str:
        """Spawn a single drone. Returns drone_id."""
        return self._pool.spawn(
            role=role, goal=goal, backend=backend,
            api_key=api_key, max_iterations=max_iterations,
        )

    def spawn_hive(
        self,
        goal: str,
        n_drones: int = 0,
        backend: str = "groq",
        api_key: Optional[str] = None,
        max_iterations: int = 10,
    ) -> List[str]:
        """Queen plans and dispatches multiple drones in parallel."""
        return self.queen.plan_and_dispatch(
            goal=goal, n_drones=n_drones, backend=backend,
            api_key=api_key, max_iterations=max_iterations,
        )

    def status(self) -> Dict[str, Any]:
        drone_list = self._pool.list_all()
        mem_stats  = self.memory.stats()
        bus_msgs   = self.bus.pending_count("queen")
        return {
            "active_drones":   self._pool.active_count(),
            "total_drones":    len(drone_list),
            "drones":          drone_list,
            "memory":          mem_stats,
            "queen_mailbox":   bus_msgs,
        }

    def recall(self, query: str, top_k: int = 10) -> List[Dict]:
        return self.memory.recall(query, top_k=top_k)

    def drone_result(self, drone_id: str) -> Dict[str, Any]:
        s = self._pool.get_state(drone_id)
        if s is None:
            return {"error": f"Drone '{drone_id}' not found"}
        return {
            "drone_id": s.drone_id,
            "role":     s.role,
            "status":   s.status,
            "result":   s.result,
            "error":    s.error,
            "duration": round(s.finished - s.started, 2) if s.finished else None,
        }

    def collect_and_synthesize(self, drone_ids: List[str], goal: str) -> str:
        return self.queen.synthesize(drone_ids, goal)

    def forget(self, older_than_hours: float = 24.0, topic: str = "") -> int:
        return self.memory.forget(older_than_hours=older_than_hours, topic=topic)


# ── Singleton ──────────────────────────────────────────────────────────────────

_hive_instance: Optional[HiveMind] = None
_hive_lock = threading.Lock()


def get_hive() -> HiveMind:
    global _hive_instance
    if _hive_instance is None:
        with _hive_lock:
            if _hive_instance is None:
                _hive_instance = HiveMind()
    return _hive_instance


# ─────────────────────────────────────────────────────────────────────────────
# SECTION 7 — MCP tool handlers (imported by lazyown_mcp.py)
# ─────────────────────────────────────────────────────────────────────────────


def mcp_hive_spawn(
    goal: str,
    role: str = "generic",
    n_drones: int = 1,
    backend: str = "groq",
    max_iterations: int = 10,
    api_key: str = "",
) -> str:
    """
    Spawn one or more hive drones for a goal.
    If n_drones > 1 or role == 'auto', queen plans and dispatches a full squad.
    """
    hive = get_hive()
    eff_key = api_key or None

    if n_drones > 1 or role == "auto":
        ids = hive.spawn_hive(
            goal=goal, n_drones=n_drones, backend=backend,
            api_key=eff_key, max_iterations=max_iterations,
        )
        return json.dumps({
            "spawned":   len(ids),
            "drone_ids": ids,
            "message":   f"Hive squad dispatched: {len(ids)} drones in parallel",
        }, indent=2)
    else:
        drone_id = hive.spawn(
            goal=goal, role=role, backend=backend,
            api_key=eff_key, max_iterations=max_iterations,
        )
        return json.dumps({
            "drone_id": drone_id,
            "role":     role,
            "backend":  backend,
            "message":  f"Drone {drone_id} spawned for role={role}",
        }, indent=2)


def mcp_hive_status() -> str:
    """Return full hive status: active drones, memory stats, queen mailbox."""
    return json.dumps(get_hive().status(), indent=2)


def mcp_hive_recall(query: str, top_k: int = 10) -> str:
    """Semantic + episodic + longterm recall from hive memory."""
    results = get_hive().recall(query, top_k=top_k)
    if not results:
        return f"No hive memories found for: {query!r}"
    lines = [f"Hive recall ({len(results)} results) for: {query!r}", ""]
    for i, r in enumerate(results, 1):
        layer = r.get("layer", "?")
        sim   = r.get("similarity")
        sim_s = f"  sim={sim:.3f}" if sim is not None else ""
        lines.append(f"{i}. [{layer}]{sim_s}  {r['content'][:300]}")
    return "\n".join(lines)


def mcp_hive_plan(goal: str, n_drones: int = 0) -> str:
    """Queen generates task decomposition without spawning drones."""
    tasks = get_hive().queen.plan(goal, n_drones=n_drones)
    lines = [f"Hive plan for: {goal[:100]}", f"({len(tasks)} tasks)", ""]
    for i, t in enumerate(tasks, 1):
        lines.append(f"  {i}. [{t['role']:8s}] {t['goal'][:100]}")
    return "\n".join(lines)


def mcp_hive_result(drone_id: str) -> str:
    """Get result from a specific drone."""
    r = get_hive().drone_result(drone_id)
    return json.dumps(r, indent=2)


def mcp_hive_collect(drone_ids_csv: str, goal: str = "") -> str:
    """
    Wait for drones to finish and return synthesized result.
    drone_ids_csv: comma-separated drone IDs.
    """
    ids = [x.strip() for x in drone_ids_csv.split(",") if x.strip()]
    if not ids:
        return "No drone IDs provided."
    return get_hive().collect_and_synthesize(ids, goal or f"Collected from {len(ids)} drones")


def mcp_hive_forget(older_than_hours: float = 24.0, topic: str = "") -> str:
    """Prune hive memory. Removes entries older than N hours, optionally filtered by topic."""
    pruned = get_hive().forget(older_than_hours=older_than_hours, topic=topic)
    return f"Pruned {pruned} hive memory entries (older_than={older_than_hours}h, topic={topic!r})"


# ─────────────────────────────────────────────────────────────────────────────
# SECTION 8 — CLI
# ─────────────────────────────────────────────────────────────────────────────


def _cli() -> None:  # noqa: C901
    import argparse

    parser = argparse.ArgumentParser(
        description="LazyOwn Hive Mind — multi-agent cognitive system",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    sub = parser.add_subparsers(dest="cmd")

    # spawn
    p_sp = sub.add_parser("spawn", help="Spawn drones for a goal")
    p_sp.add_argument("goal",      help="High-level goal")
    p_sp.add_argument("--role",    default="auto", help="Drone role (auto = queen plans)")
    p_sp.add_argument("--drones",  type=int, default=0, help="Number of drones (0 = template)")
    p_sp.add_argument("--backend", default="groq", choices=["groq", "ollama"])
    p_sp.add_argument("--max-iter",type=int, default=10)
    p_sp.add_argument("--wait",    action="store_true", help="Block until all done")
    p_sp.add_argument("--timeout", type=float, default=300.0)

    # status
    sub.add_parser("status", help="Show hive status")

    # recall
    p_rc = sub.add_parser("recall", help="Recall from hive memory")
    p_rc.add_argument("query")
    p_rc.add_argument("--top", type=int, default=10)

    # plan
    p_pl = sub.add_parser("plan", help="Show queen's task decomposition")
    p_pl.add_argument("goal")
    p_pl.add_argument("--drones", type=int, default=0)

    # result
    p_rs = sub.add_parser("result", help="Get drone result")
    p_rs.add_argument("drone_id")

    # forget
    p_fg = sub.add_parser("forget", help="Prune hive memory")
    p_fg.add_argument("--hours", type=float, default=24.0)
    p_fg.add_argument("--topic", default="")

    args = parser.parse_args()
    logging.basicConfig(level=logging.WARNING)

    if args.cmd == "spawn":
        role = args.role if args.role != "auto" else "generic"
        n    = args.drones or (1 if role != "generic" else 0)
        print(mcp_hive_spawn(
            goal=args.goal, role=role, n_drones=n if args.role == "auto" else 1,
            backend=args.backend, max_iterations=args.max_iter,
        ))
        if args.wait:
            hive    = get_hive()
            # Wait for active drones
            deadline = time.time() + args.timeout
            while hive._pool.active_count() > 0 and time.time() < deadline:
                time.sleep(2.0)
            print(json.dumps(hive.status(), indent=2))

    elif args.cmd == "status":
        print(mcp_hive_status())

    elif args.cmd == "recall":
        print(mcp_hive_recall(args.query, top_k=args.top))

    elif args.cmd == "plan":
        print(mcp_hive_plan(args.goal, n_drones=args.drones))

    elif args.cmd == "result":
        print(mcp_hive_result(args.drone_id))

    elif args.cmd == "forget":
        print(mcp_hive_forget(older_than_hours=args.hours, topic=args.topic))

    else:
        parser.print_help()


if __name__ == "__main__":
    _cli()
