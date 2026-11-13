"""Operator audit trail for autonomous loop runs.

One question drives this module: what exactly did the loop do, when,
who triggered it, with what confidence, and with what outcome? The
engine already persists fragments (activity, traffic, guard audits,
findings) but no single timeline exists, so a finished run is a sea of
logs the operator cannot navigate.

This module owns one append-only JSONL timeline per task:
``sessions/lazy/audit_<task>.jsonl``. Every executed command lands as a
``command`` event carrying:

- when: wall-clock ``ts`` plus the offset from run start;
- what: the full command and the module/verb that runs it;
- who and why: worker name, intent id, guard verdict (allow/ask/deny),
  judge source and reason, opsec gate and detection probability —
  supplied by the worker through a thread-local step context;
- outcome: ok/failed, duration and a bounded output tail.

The runner (``modules.lazy_runner``) starts the audit, emits
``run_start``/``preflight``/``verdict``/``run_end`` lifecycle events and
hooks the executor so every executed command is recorded exactly once.
Rendering (``render``) merges the audit timeline with guard decisions
(``guard_audit_<task>.jsonl``) and engine lifecycle activity
(``activity_<task>.jsonl``) so ``loop_audit`` can navigate the campaign
timeline from start to end. Never raises on I/O; a lost audit row must
never kill a step that already ran.
"""

from __future__ import annotations

import json
import threading
import time
from contextlib import contextmanager
from pathlib import Path

from core.parsers import strip_ansi

BASE_DIR = Path(__file__).resolve().parent.parent
SESSIONS_DIR = BASE_DIR / "sessions"
AUDIT_DIR = SESSIONS_DIR / "lazy"
AUDIT_MAX_RECORDS = 5000
AUDIT_COMMAND_LIMIT = 200
AUDIT_OUTPUT_TAIL_LIMIT = 400
AUDIT_STEP_TEXT_LIMIT = 200
TIMELINE_ACTIVITY_KINDS = frozenset(
    {"engine", "planner", "verdict", "finalizer", "wake", "progress", "digest", "round", "archive"}
)

_LOCAL = threading.local()
_REGISTRY: dict[str, LoopAudit] = {}
_REGISTRY_LOCK = threading.Lock()


def _clean(text: str, limit: int) -> str:
    """Collapse text to one bounded single line."""
    return " ".join(str(text or "").split())[:limit]


def _first_token(command: str) -> str:
    """Return the module/verb token that runs a command."""
    parts = str(command or "").split()
    if not parts:
        return ""
    if parts[0] == "custom" and len(parts) > 2 and parts[1] == "tool":
        return f"custom:{parts[2]}"
    return parts[0]


def _output_tail(output: str) -> str:
    """Return the bounded, ANSI-stripped tail of one command output."""
    text = strip_ansi(str(output or "")).strip()
    if len(text) <= AUDIT_OUTPUT_TAIL_LIMIT:
        return _clean(text, AUDIT_OUTPUT_TAIL_LIMIT)
    return _clean(text[-AUDIT_OUTPUT_TAIL_LIMIT:], AUDIT_OUTPUT_TAIL_LIMIT)


@contextmanager
def step_context(task_id: str = "", **fields):
    """Annotate every command executed inside the block with step context.

    The worker wraps its execution path so the single ``command`` event
    recorded by the executor also carries who ran the step (worker,
    intent), why it was allowed (judge verdict, source, reason) and what
    it cost in opsec terms (gate, detection probability).

    Args:
        task_id: Task the step belongs to.
        **fields: Enrichment fields merged into the command event.
    """
    previous_fields = getattr(_LOCAL, "fields", None)
    previous_task = getattr(_LOCAL, "task_id", "")
    try:
        _LOCAL.fields = dict(fields or {})
        _LOCAL.task_id = str(task_id or "")
        yield
    finally:
        _LOCAL.fields = previous_fields
        _LOCAL.task_id = previous_task


def _consume_context() -> dict:
    """Read the current thread-local step context without clearing it."""
    fields = getattr(_LOCAL, "fields", None)
    return dict(fields) if isinstance(fields, dict) else {}


def audit_path(task_id: str) -> Path:
    """Return the audit file path for one task."""
    return AUDIT_DIR / f"audit_{task_id}.jsonl"


class LoopAudit:
    """Append-only per-task audit timeline (one JSON object per line).

    Args:
        task_id: Task identifier the timeline belongs to.
        path: File override (tests); defaults to
            ``sessions/lazy/audit_<task>.jsonl``.
    """

    def __init__(self, task_id: str, path: Path | None = None) -> None:
        """Bind the audit file and start the run clock."""
        self.task_id = str(task_id or "")
        self._path = Path(path) if path is not None else audit_path(self.task_id)
        self._lock = threading.Lock()
        self._start = time.time()

    @property
    def path(self) -> Path:
        """Return the timeline file path."""
        return self._path

    def record(self, kind: str, **fields) -> dict | None:
        """Append one event and enforce the file cap.

        Args:
            kind: Event family (``command``, ``blocked``, ``run_start``, ...).
            **fields: Event payload; long text fields are bounded.

        Returns:
            The stored event mapping, or None when the write failed.
        """
        event = {
            "ts": round(time.time(), 3),
            "offset": round(max(0.0, time.time() - self._start), 3),
            "task": self.task_id,
            "kind": str(kind or ""),
        }
        event.update(fields)
        self._append(event)
        return event

    def run_start(self, goal: str = "", target: str = "", rounds: int = 0, workers: int = 0, mode: str = "", profile: str = "") -> dict | None:
        """Record the loop lifecycle start."""
        self._start = time.time()
        return self.record(
            "run_start",
            goal=_clean(goal, 300),
            target=str(target or ""),
            rounds=int(rounds or 0),
            workers=int(workers or 0),
            mode=str(mode or ""),
            profile=str(profile or ""),
        )

    def preflight(self, outcome: dict) -> dict | None:
        """Record the target preflight verdict."""
        return self.record(
            "preflight",
            ok=bool((outcome or {}).get("ok")),
            reason=_clean((outcome or {}).get("reason", ""), 300),
            open_ports=list((outcome or {}).get("open_ports") or []),
            lab=dict((outcome or {}).get("lab") or {}),
        )

    def blocked(self, source: str, reason: str, command: str = "", worker: str = "", intent: int = 0) -> dict | None:
        """Record a command that never ran because a gate blocked it."""
        return self.record(
            "blocked",
            source=str(source or ""),
            reason=_clean(reason, 300),
            command=_clean(command, AUDIT_COMMAND_LIMIT),
            worker=str(worker or ""),
            intent=int(intent or 0),
        )

    def verdict(self, verdict: dict) -> dict | None:
        """Record the independent goal-evaluation verdict."""
        data = verdict if isinstance(verdict, dict) else {}
        return self.record(
            "verdict",
            verdict=str(data.get("verdict", "")),
            status=str(data.get("status", "")),
            coverage_pct=float(data.get("coverage_pct", 0.0) or 0.0),
            facts=int(data.get("facts", 0) or 0),
            findings=int(data.get("findings", 0) or 0),
            confirmed=int(data.get("confirmed", 0) or 0),
            completion_reason=_clean(data.get("completion_reason", ""), 200),
        )

    def run_end(self, status: str = "", rounds: int = 0, verdict: dict | None = None, error: str = "") -> dict | None:
        """Record the loop lifecycle end with the final engine status."""
        data = verdict if isinstance(verdict, dict) else {}
        return self.record(
            "run_end",
            status=str(status or ""),
            rounds=int(rounds or 0),
            verdict=str(data.get("verdict", "")),
            findings=int(data.get("findings", 0) or 0),
            confirmed=int(data.get("confirmed", 0) or 0),
            error=_clean(error, 300),
        )

    def record_command(self, command: str, output: str, duration: float, ok: bool | None = None, task_id: str = "") -> dict | None:
        """Record one executed command with its trigger context.

        Called by the loop executor for every command it dispatches. The
        thread-local step context (when the caller wrapped the step) is
        consumed and merged, so the event carries the full trigger
        picture in a single row.

        Args:
            command: The command string as executed.
            output: Raw command output (bounded tail is stored).
            duration: Execution seconds.
            ok: Success override; derived from the output prefix when None.
            task_id: Task override when the audit handle is task-less.

        Returns:
            The stored event mapping, or None when the write failed.
        """
        context = _consume_context()
        resolved = self
        owner = str(task_id or context.get("task_id", "") or self.task_id)
        if owner and owner != self.task_id:
            resolved = audit_for(owner) or self
        outcome_text = strip_ansi(str(output or ""))
        if ok is None:
            ok = not outcome_text.lstrip().startswith(("execution failed:", "skipped:"))
        event = {
            "command": _clean(command, AUDIT_COMMAND_LIMIT),
            "module": _first_token(command),
            "ok": bool(ok),
            "duration": round(max(0.0, float(duration or 0.0)), 3),
            "output_tail": _output_tail(outcome_text),
        }
        for key in (
            "worker",
            "intent",
            "tool_use_id",
            "judge_action",
            "judge_source",
            "judge_reason",
            "opsec_gate",
            "detection_prob",
            "step",
        ):
            value = context.get(key)
            if value in (None, ""):
                continue
            if key in ("intent",):
                try:
                    value = int(value)
                except (TypeError, ValueError):
                    continue
            elif key in ("judge_reason", "step"):
                value = _clean(value, AUDIT_STEP_TEXT_LIMIT if key == "step" else 300)
            event[key] = value
        return resolved.record("command", **event)

    def _append(self, event: dict) -> bool:
        """Append one event and enforce the cap. Never raises."""
        try:
            self._path.parent.mkdir(parents=True, exist_ok=True)
            try:
                self._path.chmod(0o600)
            except OSError:
                pass
            with self._lock, open(self._path, "a", encoding="utf-8") as handle:
                handle.write(json.dumps(event, ensure_ascii=False) + "\n")
            self._trim()
            return True
        except OSError:
            return False

    def _trim(self) -> None:
        """Rewrite the file keeping only the newest rows."""
        rows = self._read(self._path)
        if len(rows) <= AUDIT_MAX_RECORDS:
            return
        try:
            tmp = self._path.with_suffix(".tmp")
            with open(tmp, "w", encoding="utf-8") as handle:
                for row in rows[-AUDIT_MAX_RECORDS:]:
                    handle.write(json.dumps(row, ensure_ascii=False) + "\n")
            tmp.replace(self._path)
        except OSError:
            pass

    @staticmethod
    def _read(path: Path) -> list[dict]:
        """Read one audit file tolerating missing files and broken lines."""
        try:
            lines = Path(path).read_text(encoding="utf-8", errors="replace").splitlines()
        except OSError:
            return []
        rows: list[dict] = []
        for line in lines:
            try:
                data = json.loads(line)
            except ValueError:
                continue
            if isinstance(data, dict):
                rows.append(data)
        return rows


def start(task_id: str) -> LoopAudit | None:
    """Create and register the audit for one task.

    Args:
        task_id: Task identifier.

    Returns:
        The active audit handle, or None for an empty task id.
    """
    clean = str(task_id or "").strip()
    if not clean:
        return None
    audit = LoopAudit(clean)
    with _REGISTRY_LOCK:
        _REGISTRY[clean] = audit
    return audit


def audit_for(task_id: str) -> LoopAudit | None:
    """Return the active audit for one task, or None when not started.

    Args:
        task_id: Task identifier.
    """
    clean = str(task_id or "").strip()
    with _REGISTRY_LOCK:
        return _REGISTRY.get(clean)


def stop(task_id: str) -> None:
    """Forget the registered audit for one task."""
    with _REGISTRY_LOCK:
        _REGISTRY.pop(str(task_id or "").strip(), None)


def _read_jsonl(path: Path) -> list[dict]:
    """Read one JSONL file tolerating missing files and broken lines."""
    return LoopAudit._read(path)


def guard_rows(task_id: str) -> list[dict]:
    """Return guard decisions recorded for one task."""
    return _read_jsonl(AUDIT_DIR / f"guard_audit_{task_id}.jsonl")


def activity_rows(task_id: str) -> list[dict]:
    """Return engine activity rows for one task."""
    return _read_jsonl(AUDIT_DIR / f"activity_{task_id}.jsonl")


def _ts(row: dict) -> float:
    """Best-effort wall-clock timestamp of one timeline row."""
    try:
        return float(row.get("ts", 0.0) or 0.0)
    except (TypeError, ValueError):
        return 0.0


def _timeline_event(audit_row: dict, start_ts: float) -> dict:
    """Normalize one audit row into a render event."""
    ts = _ts(audit_row)
    return {
        "ts": ts,
        "offset": max(0.0, ts - start_ts) if start_ts else float(audit_row.get("offset", 0.0) or 0.0),
        "kind": str(audit_row.get("kind", "")),
        "row": audit_row,
    }


def _guard_event(row: dict, start_ts: float) -> dict:
    """Normalize one guard decision into a render event."""
    ts = _ts(row)
    action = str(row.get("action", ""))
    return {
        "ts": ts,
        "offset": max(0.0, ts - start_ts) if start_ts else 0.0,
        "kind": "guard_" + (action or "audit"),
        "row": row,
    }


def _activity_event(row: dict, start_ts: float) -> dict | None:
    """Normalize one activity row into a render event when in scope."""
    kind = str(row.get("kind", ""))
    if kind not in TIMELINE_ACTIVITY_KINDS:
        return None
    ts = _ts(row)
    return {
        "ts": ts,
        "offset": max(0.0, ts - start_ts) if start_ts else 0.0,
        "kind": f"activity_{kind}",
        "row": row,
    }


def timeline(task_id: str, audit: LoopAudit | None = None) -> list[dict]:
    """Merge audit, guard and lifecycle rows into one timeline.

    Args:
        task_id: Task identifier.
        audit: Audit handle override; resolved from the registry when None.

    Returns:
        Events sorted oldest first, each with ``ts``, ``offset``, ``kind``
        and the raw ``row``.
    """
    handle = audit or audit_for(task_id) or LoopAudit(str(task_id))
    path = handle.path if handle.path.exists() else audit_path(task_id)
    rows = _read_jsonl(path)
    start_ts = _ts(rows[0]) if rows else 0.0
    events = [_timeline_event(row, start_ts) for row in rows]
    events.extend(_guard_event(row, start_ts) for row in guard_rows(task_id))
    for row in activity_rows(task_id):
        event = _activity_event(row, start_ts)
        if event:
            events.append(event)
    return sorted(events, key=lambda item: (item["ts"], 0 if item["kind"].startswith("activity") else 1))


def _fmt_offset(offset: float) -> str:
    """Render one timeline offset."""
    return f"+{offset:07.1f}s"


def _render_event(event: dict) -> str:
    """Render one timeline event to an operator line."""
    row = event.get("row") or {}
    kind = event["kind"]
    offset = _fmt_offset(event["offset"])
    if kind == "command":
        marker = "CMD " if row.get("ok") else "FAIL"
        worker = str(row.get("worker", "") or "-")
        parts = [
            f"{offset} {marker} {worker:<8}",
            str(row.get("command", "")),
            f"({row.get('duration', 0)}s)",
        ]
        context = []
        if row.get("judge_action"):
            context.append(f"judge={row['judge_action']}" + (f"/{row['judge_source']}" if row.get("judge_source") else ""))
        if row.get("opsec_gate"):
            context.append(f"opsec={row['opsec_gate']}")
        if row.get("detection_prob") not in (None, ""):
            context.append(f"detect={row['detection_prob']}")
        if context:
            parts.append("[" + " ".join(context) + "]")
        if row.get("output_tail"):
            parts.append(f"-> {_clean(row['output_tail'], 120)}")
        return " ".join(parts)
    if kind == "blocked":
        return (
            f"{offset} DENY {str(row.get('worker', '') or '-'): <8}"
            f"{str(row.get('command', ''))} ({str(row.get('source', ''))}: {str(row.get('reason', ''))})"
        )
    if kind == "run_start":
        return f"{offset} RUN  START   rounds<={row.get('rounds', 0)} workers={row.get('workers', 0)} target={row.get('target', '')} goal={str(row.get('goal', ''))[:120]}"
    if kind == "preflight":
        marker = "OK  " if row.get("ok") else "DOWN"
        ports = ",".join(str(p) for p in row.get("open_ports", [])[:8])
        detail = f" ports={ports}" if ports else ""
        return f"{offset} PREFLIGHT {marker} {str(row.get('reason', ''))[:160]}{detail}"
    if kind == "verdict":
        return (
            f"{offset} VERDICT    {row.get('verdict', '')} status={row.get('status', '')} "
            f"coverage={row.get('coverage_pct', 0)}% findings={row.get('findings', 0)} "
            f"confirmed={row.get('confirmed', 0)} ({str(row.get('completion_reason', ''))})"
        )
    if kind == "run_end":
        return (
            f"{offset} RUN  END     status={row.get('status', '')} rounds={row.get('rounds', 0)} "
            f"verdict={row.get('verdict', '')} findings={row.get('findings', 0)}"
            + (f" error={row.get('error', '')}" if row.get("error") else "")
        )
    if kind.startswith("guard_"):
        tool = str(row.get("tool", ""))
        reason = _clean(row.get("reason", ""), 140)
        command = _clean(row.get("command", ""), AUDIT_COMMAND_LIMIT)
        return f"{offset} {kind.upper()} {tool:<8}{command} ({reason})"
    if kind.startswith("activity_"):
        inner = kind.split("_", 1)[1]
        who = str(row.get("worker", "") or row.get("source", "") or "-")
        return f"{offset} ENG  {inner:<8}{who:<8}{_clean(row.get('text', ''), 160)}"
    return f"{offset} {kind.upper()} {_clean(json.dumps(row, ensure_ascii=False), 200)}"


def render(task_id: str, limit: int = 100, audit: LoopAudit | None = None) -> str:
    """Render the merged campaign timeline for one task.

    Args:
        task_id: Task identifier.
        limit: Maximum events to show (most recent tail).
        audit: Audit handle override.

    Returns:
        Multi-line timeline string; empty when nothing was recorded.
    """
    events = timeline(task_id, audit=audit)
    if not events:
        return ""
    shown = events[-max(1, int(limit)) :]
    header = f"loop audit {task_id} — {len(events)} events (showing {len(shown)}, oldest first)"
    lines = [header, "-" * len(header)]
    lines.extend(_render_event(event) for event in shown)
    return "\n".join(lines)


def list_runs(limit: int = 20) -> list[dict]:
    """Summarize every recorded loop run, newest first.

    Returns:
        One summary dict per audit file: task, started, duration,
        events, commands, ok/failed command counts and the final
        run_end status when present.
    """
    summaries: list[dict] = []
    try:
        paths = sorted(AUDIT_DIR.glob("audit_*.jsonl"), key=lambda p: p.stat().st_mtime, reverse=True)
    except OSError:
        return []
    for path in paths[: max(1, int(limit))]:
        rows = _read_jsonl(path)
        if not rows:
            continue
        commands = [row for row in rows if row.get("kind") == "command"]
        run_end = next((row for row in reversed(rows) if row.get("kind") == "run_end"), {})
        verdict = next((row for row in reversed(rows) if row.get("kind") == "verdict"), {})
        summaries.append(
            {
                "task": str(rows[0].get("task", path.stem.replace("audit_", ""))),
                "started": _ts(rows[0]),
                "events": len(rows),
                "commands": len(commands),
                "ok": sum(1 for row in commands if row.get("ok")),
                "failed": sum(1 for row in commands if not row.get("ok")),
                "status": str(run_end.get("status", "")),
                "verdict": str(verdict.get("verdict", "") or run_end.get("verdict", "")),
                "duration": round(max(0.0, _ts(rows[-1]) - _ts(rows[0])), 1),
                "path": str(path),
            }
        )
    return summaries


def render_summary(summaries: list[dict]) -> str:
    """Render ``list_runs`` summaries as an operator table."""
    if not summaries:
        return "no loop audits recorded yet (runs record under sessions/lazy/audit_<task>.jsonl)"
    lines = ["TASK     STARTED             DUR(s)  EVENTS  CMD(ok/fail)  STATUS     VERDICT"]
    for item in summaries:
        started = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(item["started"])) if item["started"] else "-"
        lines.append(
            f"{item['task']:<8} {started:<19} {item['duration']:<7} {item['events']:<7} "
            f"{item['ok']}/{item['failed']:<12} {item['status'] or '-':<10} {item['verdict'] or '-'}"
        )
    return "\n".join(lines)


__all__ = [
    "AUDIT_DIR",
    "AUDIT_MAX_RECORDS",
    "LoopAudit",
    "activity_rows",
    "audit_for",
    "audit_path",
    "guard_rows",
    "list_runs",
    "render",
    "render_summary",
    "start",
    "step_context",
    "stop",
    "timeline",
]
