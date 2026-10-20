"""chain_distill - crystallise one autonomous-loop trace into a chain YAML.

The loop keeps everything it does: the exploration graph
(``sessions/<dir>/exp_<task>.json``) and the append-only execution stream
(``sessions/<dir>/traffic_<task>.jsonl``). This module reads both and
emits a validated, reusable chain file under ``chains/`` so the next run
of the same goal is deterministic and free instead of LLM-priced.

Join contract (real on-disk formats):

- traffic row: ``{ts, kind: bash|http|note, command, output, preview,
  truncated, bytes, digest, template, meta:{worker, intent}}`` where
  ``digest`` is the sha12 of the command line and ``meta.intent`` is the
  claiming intent node id;
- graph node: ``{node_id, kind: goal|intent|fact, text, state, priority,
  created, updated, meta}`` plus ``edges`` (spawns/yields) and
  ``anchors``. The goal text carries the target the task was scoped to.

Policy v1: keep rows that produced output and carry no known failure
signature; drop silent probes and dead ends with their reason; dedupe by
digest and by rendered command; tokenise the task target as ``{target}``;
attach per-step lineage (intent id + digest) in ``description``. Scan
steps get the canonical ``skip_if_exists`` guard on the nmap XML
artefact. Verbs that have a manifest (:mod:`modules.verb_manifest`)
inherit its phase and exploit-classification, so a distilled chain can
be audited for cost/noise before it ever runs.

Output is validated with :func:`modules.chain_registry.validate_chain`
before writing; a distilled file that cannot validate is never written.
Generated chains start ``enabled: false`` and belong to the operator.
"""

from __future__ import annotations

import json
import logging
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Union

from modules.chain_registry import validate_chain

try:
    import yaml
except ImportError:  # pragma: no cover
    yaml = None  # type: ignore

log = logging.getLogger("chain_distill")

REPO_ROOT = Path(__file__).resolve().parent.parent
SESSIONS_DIR = REPO_ROOT / "sessions"
CHAINS_DIR = REPO_ROOT / "chains"
MAX_RUN_CHARS = 2000
_MAX_STEPS = 120

_FAILURE_MARKERS: tuple[str, ...] = (
    "connection refused",
    "could not connect",
    "failed to connect",
    "no route to host",
    "connection reset",
    "connection timed out",
    "unreachable",
    "name or service not known",
    "command not found",
    "invalid option",
    "permission denied",
    "authentication failed",
)
_HOST_TOKEN_RE = re.compile(r"(?<![\w.])(?:(?:\d{1,3}\.){3}\d{1,3}|(?:[\w-]+\.)+[A-Za-z]{2,10})(?![\w.])")
_GOAL_TARGET_RE = re.compile(r"\bon\s+((?:\d{1,3}\.){3}\d{1,3}|(?:[\w-]+\.)+[A-Za-z]{2,10})\b")
_PROSE_LIMIT_WORDS = 14


def _slug(text: str) -> str:
    """Reduce arbitrary text to a YAML-name-safe slug.

    Args:
        text: Raw text.

    Returns:
        Slug bound to ``[a-z0-9_]`` for chain naming.
    """
    slug = re.sub(r"[^a-z0-9_]+", "_", (text or "").strip().lower()).strip("_")
    return slug or "target"


def locate_traces(task: str, sessions_dir: Path | str | None = None) -> tuple[Union[Path, None], Union[Path, None]]:
    """Find the exp/traffic pair of one loop task under sessions/.

    Args:
        task: Task id (``tNNNN``) or an explicit ``exp_*.json`` path.
        sessions_dir: Override the repository sessions root.

    Returns:
        ``(exp_path, traffic_path)``: each element None when absent.
    """
    task = str(task or "").strip()
    root = Path(sessions_dir or SESSIONS_DIR)
    if not task:
        return None, None
    if "/" in task or task.endswith(".json"):
        exp = Path(task)
        if exp.is_file():
            return exp, exp.with_name(f"traffic_{exp.stem.replace('exp_', '')}.jsonl")
        return None, None
    exp_name = f"exp_{task}.json"
    traffic_name = f"traffic_{task}.jsonl"
    exp_hits: list[Path] = []
    traffic_hits: list[Path] = []
    for directory in sorted(root.iterdir()):
        if not directory.is_dir():
            continue
        candidate = directory / exp_name
        if candidate.is_file():
            exp_hits.append(candidate)
        candidate = directory / traffic_name
        if candidate.is_file():
            traffic_hits.append(candidate)
    exp_path = exp_hits[0] if exp_hits else None
    traffic_path: Union[Path, None] = None
    if exp_path is not None:
        traffic_path = next((path for path in traffic_hits if path.parent == exp_path.parent), None)
    if traffic_path is None:
        traffic_path = traffic_hits[0] if len(traffic_hits) == 1 else None
    if len(exp_hits) > 1:
        log.warning("exp trace for %s in %d directories; using %s", task, len(exp_hits), exp_path)
    return exp_path, traffic_path


def _load_traffic(path: Union[Path, None]) -> list[dict]:
    """Read traffic rows in append order, deduped by digest.

    Args:
        path: ``traffic_*.jsonl`` path.

    Returns:
        First-seen rows per digest; malformed lines are skipped.
    """
    if path is None or not path.is_file():
        return []
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return []
    rows: list[dict] = []
    seen: set[str] = set()
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            row = json.loads(line)
        except ValueError:
            continue
        if not isinstance(row, dict):
            continue
        digest = str(row.get("digest", "")) or f"cmd{len(rows)}"
        if digest in seen:
            continue
        seen.add(digest)
        row["digest"] = digest
        rows.append(row)
    return rows


def _load_graph(path: Union[Path, None]) -> dict[str, Any]:
    """Read the exploration graph into a tolerant shape.

    Args:
        path: ``exp_*.json`` path.

    Returns:
        ``{"goal": str, "intents": {id: text}}`` with safe defaults.
    """
    if path is None or not path.is_file():
        return {"goal": "", "intents": {}}
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {"goal": "", "intents": {}}
    goal = ""
    intents: dict[str, str] = {}
    for node in raw.get("nodes") or []:
        kind = str(node.get("kind", ""))
        if kind == "goal" and not goal:
            goal = str(node.get("text", "") or "")
        elif kind == "intent":
            intents[str(node.get("node_id", ""))] = str(node.get("text", "") or "")
    return {"goal": goal, "intents": intents}


def _is_prose(command: str) -> bool:
    """Reject planner commentary that was logged as a command line.

    Args:
        command: Raw first field of a traffic row.

    Returns:
        True when the line reads as English prose, not a shell verb.
    """
    fields = (command or "").strip().split()
    if len(fields) > _PROSE_LIMIT_WORDS:
        return True
    return ". " in (command or "") or "This command" in (command or "")[:24]


def _is_failed(row: dict) -> bool:
    """Classify one exchange as a dead end.

    Args:
        row: Traffic row.

    Returns:
        True when output is empty or carries a failure signature.
    """
    output = str(row.get("output", "") or "")
    if not output.strip():
        return True
    lowered = output.lower()
    return any(marker in lowered for marker in _FAILURE_MARKERS)


def _command_verb(command: str) -> str:
    """Return the leading shell verb of one command line.

    Args:
        command: Raw command line.

    Returns:
        Lower-case leading token (``sudo`` and ``auto`` wrapper aware),
        else ``run``.
    """
    fields = (command or "").strip().split(":")[0].split()
    if not fields:
        return "run"
    if fields[0].lower() == "sudo" and len(fields) > 1:
        fields = fields[1:]
    if fields[0].lower() == "auto" and len(fields) > 1:
        fields = fields[1:]
    return fields[0].lower()


def _phase_for(command: str, manifest_phase: str) -> str:
    """Resolve the kill-chain phase from manifest, command index, bridge.

    Args:
        command: Raw command line.
        manifest_phase: Phase declared in the verb manifest (may be '').

    Returns:
        Phase string; ``enum`` as last resort.
    """
    if manifest_phase:
        return manifest_phase
    verb = _command_verb(command)
    try:
        import json as jsonlib
        from pathlib import Path as PathLib

        index_path = PathLib(__file__).parent.parent / "cli" / "command_index.json"
        index = jsonlib.loads(index_path.read_text(encoding="utf-8"))
        for entry in index.get("commands", []):
            if entry.get("name") == f"do_{verb}" and entry.get("phase", "uncategorized") != "uncategorized":
                return str(entry["phase"])
    except Exception:  # noqa: BLE001 - phase resolution must never hard-fail
        pass
    try:
        from modules.lazy_cli_bridge import phase_for

        phase = phase_for(verb)
        if phase and phase != "other":
            return str(phase)
    except Exception:  # noqa: BLE001
        pass
    return "enum"


def _infer_target(rows: list[dict], graph: dict[str, Any]) -> str:
    """Pick the task target: the goal text wins, then command frequency.

    Args:
        rows: Traffic rows.
        graph: Loaded graph shape (goal, intents).

    Returns:
        Target string, or '' when the trace carries no scoping signal.
    """
    goal = str(graph.get("goal", "") or "")
    candidates = [
        host
        for host in _HOST_TOKEN_RE.findall(goal)
        if host.lower() != "127.0.0.1" and not host.lower().endswith("example.com")
    ]
    if candidates:
        return candidates[0]
    counts: dict[str, int] = {}
    for row in rows:
        for host in _HOST_TOKEN_RE.findall(str(row.get("command", "") or "")):
            counts[host] = counts.get(host, 0) + 1
    best, hits = "", 0
    for host, count in counts.items():
        if host == "127.0.0.1" and len(counts) > 1:
            continue
        if count > hits:
            best, hits = host, count
    return best


@dataclass
class StepDecision:
    """One trace row and whether it becomes a chain step.

    Args:
        command: Raw command line from the trace.
        digest: Trace digest (lineage).
        intent_id: Claiming intent node id (0 when none).
        intent_text: Intent text of the claiming node.
        kept: True when the row becomes a step.
        reason: Why the row was kept or dropped.
    """

    command: str
    digest: str
    intent_id: int
    intent_text: str = ""
    kept: bool = False
    reason: str = ""


@dataclass
class DistillReport:
    """Full account of one distillation for operator review.

    Args:
        task: Task id distilled.
        exp_path: Graph artefact used.
        traffic_path: Traffic artefact used.
        goal: Goal text of the trace.
        target: Inferred ``{target}`` token (empty when unknown).
        steps: Kept and dropped decisions in trace order.
        row_count: Raw rows read (post digest-dedupe).
        chain_name: Built chain name (empty when build failed).
        path: Written chain path (None on dry-run / validation failure).
        errors: Registry validation errors.
    """

    task: str = ""
    exp_path: str = ""
    traffic_path: str = ""
    goal: str = ""
    target: str = ""
    steps: list[StepDecision] = field(default_factory=list)
    row_count: int = 0
    chain_name: str = ""
    path: str | None = None
    errors: list[str] = field(default_factory=list)

    @property
    def kept(self) -> int:
        """Count decisions turned into steps."""
        return sum(1 for item in self.steps if item.kept)

    @property
    def dropped(self) -> int:
        """Count decisions rejected with a reason."""
        return sum(1 for item in self.steps if not item.kept)

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-serializable report."""
        return {
            "task": self.task,
            "exp_path": self.exp_path,
            "traffic_path": self.traffic_path,
            "goal": self.goal,
            "target": self.target,
            "row_count": self.row_count,
            "kept": self.kept,
            "dropped": self.dropped,
            "chain_name": self.chain_name,
            "path": self.path,
            "errors": list(self.errors),
            "steps": [
                {
                    "command": item.command,
                    "digest": item.digest,
                    "intent": item.intent_id,
                    "intent_text": item.intent_text,
                    "kept": item.kept,
                    "reason": item.reason,
                }
                for item in self.steps
            ],
        }

    def render(self, verbose: bool = False) -> list[str]:
        """Return printable report lines.

        Args:
            verbose: Also list dropped rows.

        Returns:
            Lines for the CLI printer.
        """
        lines = [
            f"task      : {self.task}",
            f"goal      : {self.goal[:120]}",
            f"exp trace : {self.exp_path or '-'}",
            f"traffic   : {self.traffic_path or '-'}",
            f"rows      : {self.row_count}  kept={self.kept} dropped={self.dropped}",
            f"target    : {self.target or '?'}",
            f"chain     : {self.chain_name or '-'}",
            f"path      : {self.path or '(not written)'}",
        ]
        for error in self.errors:
            lines.append(f"error     : {error}")
        lines.append("")
        lines.append(f"{'#':<3} {'status':<6} {'intent':<26} command")
        for index, item in enumerate(self.steps, start=1):
            if verbose or item.kept:
                status = "kept" if item.kept else "DROP"
                note = "" if (item.kept or not item.reason) else f"  [{item.reason}]"
                lines.append(f"{index:<3} {status:<6} {item.intent_text[:26]:<26} {item.command[:72]}{note}")
        return lines


def build_chain_data(
    task: str,
    rows: list[dict],
    graph: dict[str, Any],
    manifests: dict[str, Any] | None = None,
) -> tuple[dict[str, Any], list[StepDecision]]:
    """Turn deduped traffic rows and graph context into chain YAML data.

    Args:
        task: Task id for naming.
        rows: Dedupe traffic rows (first-seen digests).
        graph: Loaded graph shape (goal, intents).
        manifests: Verb manifests keyed by verb (phase inheritance).

    Returns:
        ``(chain_data, decisions)`` with one decision per row.
    """
    target = _infer_target(rows, graph)
    decisions: list[StepDecision] = []
    steps: list[dict[str, Any]] = []
    intents = graph.get("intents") or {}
    seen_lines: set[str] = set()
    id_counts: dict[str, int] = {}

    def note(row: dict, kept: bool, reason: str = "") -> None:
        """Record one keep/drop decision for the report."""
        meta = row.get("meta") or {}
        raw_intent = int(meta.get("intent", 0) or 0)
        decisions.append(
            StepDecision(
                command=str(row.get("command", "") or ""),
                digest=str(row.get("digest", "")),
                intent_id=raw_intent,
                intent_text=str(intents.get(str(raw_intent), "")),
                kept=kept,
                reason=reason,
            )
        )

    for row in rows:
        command = str(row.get("command", "") or "").strip()
        if not command:
            note(row, False, "empty command")
            continue
        if row.get("kind", "bash") not in ("bash", ""):
            note(row, False, f"kind={row.get('kind')} not distillable")
            continue
        if _is_prose(command):
            note(row, False, "prose, not a command line")
            continue
        if _is_failed(row):
            note(row, False, "silent or failure signature")
            continue
        if target:
            command = re.sub(rf"(?<![\w.]){re.escape(target)}(?![\w.])", "{target}", command)
        if command in seen_lines:
            note(row, False, "duplicate rendered command")
            continue
        seen_lines.add(command)
        verb = _command_verb(command)
        manifest = (manifests or {}).get(verb)
        phase = _phase_for(command, manifest.phase if manifest else "")
        base_id = f"{_slug(phase)[:18]}_{_slug(verb)[:20]}"
        id_counts[base_id] = id_counts.get(base_id, 0) + 1
        step_id = base_id if id_counts[base_id] == 1 else f"{base_id}_{id_counts[base_id]}"
        lineage = (
            f"[intent {row.get('meta', {}).get('intent', '')} digest {row.get('digest', '')}]"
            if row.get("digest")
            else ""
        )
        steps.append(
            {
                "id": step_id[:63],
                "phase": phase,
                "description": f"{command[:140]} {lineage}".strip()[:MAX_RUN_CHARS],
                "run": command[:MAX_RUN_CHARS],
                "continue_on_error": phase != "exploit",
            }
        )
        if verb in ("nmap", "lazynmap"):
            steps[-1]["skip_if_exists"] = "sessions/scan_{target}.nmap.xml"
        note(row, True)

    goal_text = str(graph.get("goal", "") or "")
    name = f"distill_{_slug(task)[:16]}_{_slug(goal_text or target or 'trace')[:36]}"
    if target:
        defaults: dict[str, str] = {"target": target}
    else:
        defaults = {}

    data: dict[str, Any] = {
        "name": name[:63],
        "version": 2,
        "description": (
            f"Distilled from exp_{task}.json + traffic_{task}.jsonl; "
            f"goal: {goal_text[:140]}; starts disabled; operator owns this file."
        ),
        "enabled": False,
        "tags": ["distill"],
        "platforms": ["linux", "windows"],
        "defaults": defaults,
        "steps": steps[:_MAX_STEPS],
        "total_timeout": 0,
    }
    if not data["steps"]:
        data["steps"] = [{"id": "empty", "run": "assign target {target}"}]
    return data, decisions


def distill(
    task: str,
    sessions_dir: Path | str | None = None,
    write: bool = False,
    chains_dir: Path | str | None = None,
) -> DistillReport:
    """Distill one loop task into a validated chain YAML.

    Args:
        task: Task id (``tNNNN``).
        sessions_dir: Sessions root override.
        write: Persist ``chains/<name>.yaml`` when True and valid.
        chains_dir: Chains directory override (tests).

    Returns:
        The DistillReport; ``path`` set only after a successful write.
    """
    from modules.verb_manifest import manifests as loaded_manifests

    manifests = loaded_manifests()
    exp_path, traffic_path = locate_traces(task, sessions_dir)
    rows = _load_traffic(traffic_path)
    graph = _load_graph(exp_path)
    data, decisions = build_chain_data(task, rows, graph, manifests)
    report = DistillReport(
        task=task,
        exp_path=str(exp_path or ""),
        traffic_path=str(traffic_path or ""),
        goal=str(graph.get("goal", "")),
        target=str(data.get("defaults", {}).get("target", "")),
        steps=decisions,
        row_count=len(rows),
        chain_name=str(data.get("name", "")),
    )
    if not traffic_path and not exp_path:
        report.errors.append("no trace found for task")
        return report
    errors = validate_chain(data, filename=str(data["name"]), chains_dir=chains_dir)
    if errors:
        report.errors = errors
        return report
    if not write:
        return report
    if yaml is None:
        report.errors = ["PyYAML not available"]
        return report
    base = Path(chains_dir or CHAINS_DIR)
    base.mkdir(parents=True, exist_ok=True)
    path = base / f"{data['name']}.yaml"
    try:
        path.write_text(yaml.safe_dump(data, sort_keys=False, allow_unicode=True), encoding="utf-8")
    except OSError as exc:
        report.errors = [f"cannot write {path}: {exc}"]
        return report
    report.path = str(path)
    return report
