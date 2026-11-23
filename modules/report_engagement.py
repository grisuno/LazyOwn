"""Engagement report sources — autonomous loops, beacons and audit trails.

Read-only collectors over ``sessions/lazy/`` artefacts so the report
pipeline (and the standalone loop trace) can navigate what the autonomous
engine actually did: every loop task, every executed command, the judge
and opsec verdicts, beacon sessions and findings.

>>> from modules.report_engagement import collect_loop_runs
>>> runs = collect_loop_runs()
>>> runs and runs[0].task_id
'...'
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

BASE_DIR = Path(__file__).resolve().parent.parent
LAZY_DIR = BASE_DIR / "sessions" / "lazy"
SESSIONS_DIR = BASE_DIR / "sessions"
FINDINGS_SUBDIR = "findings"
MAX_AUDIT_ROWS = 5000
MAX_OUTPUT_TAIL = 240

STATUS_DONE = "done"
STATUS_PAUSED = "paused"


@dataclass
class LoopRunSummary:
    """One autonomous loop task with execution counters."""

    task_id: str
    goal: str
    status: str
    target: str
    commands: int = 0
    commands_ok: int = 0
    rounds: int = 0
    detection_avg: float = 0.0
    blocked: int = 0
    first_ts: float = 0.0
    last_ts: float = 0.0
    findings: int = 0
    reproduced: int = 0
    steps: list[str] = field(default_factory=list)

    @property
    def ok_rate(self) -> float:
        """Fraction of executed commands that succeeded."""
        if not self.commands:
            return 0.0
        return self.commands_ok / self.commands

    @property
    def duration_sec(self) -> float:
        """Wall-clock span of the run in seconds."""
        return max(self.last_ts - self.first_ts, 0.0)

    def as_dict(self) -> dict[str, Any]:
        """Return the JSON-serialisable summary."""
        return {
            "task_id": self.task_id,
            "goal": self.goal,
            "status": self.status,
            "target": self.target,
            "commands": self.commands,
            "commands_ok": self.commands_ok,
            "ok_rate": round(self.ok_rate, 3),
            "rounds": self.rounds,
            "detection_avg": round(self.detection_avg, 3),
            "blocked": self.blocked,
            "duration_sec": round(self.duration_sec, 1),
            "findings": self.findings,
            "reproduced": self.reproduced,
        }


def _read_jsonl(path: Path, limit: int = MAX_AUDIT_ROWS) -> list[dict[str, Any]]:
    """Read a jsonl file defensively.

    Args:
        path: File to read.
        limit: Maximum rows returned.

    Returns:
        List of decoded dicts; corrupt lines skipped.
    """
    if not path.exists():
        return []
    rows: list[dict[str, Any]] = []
    try:
        for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                row = json.loads(line)
            except ValueError:
                continue
            if isinstance(row, dict):
                rows.append(row)
            if len(rows) >= limit:
                break
    except OSError:
        return []
    return rows


def _task_registry() -> dict[str, dict[str, Any]]:
    """Load the loop task registry.

    Returns:
        Mapping task id -> task record from ``sessions/lazy/tasks.json``.
    """
    path = LAZY_DIR / "tasks.json"
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}
    tasks = data.get("tasks")
    return tasks if isinstance(tasks, dict) else {}


def _progress_signals(task_id: str) -> dict[str, Any]:
    """Read per-round progress signals for one task.

    Args:
        task_id: Loop task identifier.

    Returns:
        Mapping with ``rounds``, ``findings`` and ``reproduced`` counters.
    """
    path = LAZY_DIR / FINDINGS_SUBDIR / f"progress_{task_id}.json"
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {"rounds": 0, "findings": 0, "reproduced": 0}
    rounds_log = data.get("log") or []
    findings = 0
    reproduced = 0
    for row in rounds_log:
        signals = row.get("signals") or {}
        findings = max(findings, int(signals.get("findings", 0) or 0))
        reproduced = max(reproduced, int(signals.get("reproduced", 0) or 0))
    return {"rounds": len(rounds_log), "findings": findings, "reproduced": reproduced}


def collect_loop_runs(sessions_dir: Path | None = None) -> list[LoopRunSummary]:
    """Summarize every autonomous loop run from the audit trail.

    Args:
        sessions_dir: Override for the ``sessions/lazy`` directory.

    Returns:
        Summaries sorted by task id; tasks without an audit trail are
        skipped.
    """
    lazy_dir = sessions_dir or LAZY_DIR
    registry = _task_registry()
    runs: list[LoopRunSummary] = []
    for path in sorted(lazy_dir.glob("audit_*.jsonl")):
        task_id = path.stem.replace("audit_", "", 1)
        record = registry.get(task_id) or {}
        summary = LoopRunSummary(
            task_id=task_id,
            goal=str(record.get("goal") or ""),
            status=str(record.get("status") or "unknown"),
            target="",
        )
        detection_values: list[float] = []
        first = 0.0
        last = 0.0
        for row in _read_jsonl(path):
            kind = str(row.get("kind", ""))
            ts = float(row.get("ts", 0.0) or 0.0)
            if ts:
                first = first or ts
                last = max(last, ts)
            if kind == "run_start":
                summary.goal = summary.goal or str(row.get("goal", ""))
                summary.target = summary.target or str(row.get("target", ""))
                summary.rounds = max(summary.rounds, int(row.get("rounds", 0) or 0))
            elif kind == "command":
                summary.commands += 1
                if bool(row.get("ok")):
                    summary.commands_ok += 1
                if str(row.get("judge_action", "")) == "deny" or str(row.get("opsec_gate", "")) == "deny":
                    summary.blocked += 1
                prob = row.get("detection_prob")
                if isinstance(prob, (int, float)):
                    detection_values.append(float(prob))
                step = str(row.get("step", ""))[:80]
                if step and len(summary.steps) < 20 and step not in summary.steps:
                    summary.steps.append(step)
        signals = _progress_signals(task_id)
        summary.rounds = max(summary.rounds, signals["rounds"])
        summary.findings = signals["findings"]
        summary.reproduced = signals["reproduced"]
        summary.detection_avg = sum(detection_values) / len(detection_values) if detection_values else 0.0
        summary.first_ts = first
        summary.last_ts = last
        runs.append(summary)
    return runs


def collect_audit_rows(task_id: str, kind: str = "", limit: int = MAX_AUDIT_ROWS) -> list[dict[str, Any]]:
    """Read one task's audit trail.

    Args:
        task_id: Loop task identifier.
        kind: Filter by row kind (``command``, ``run_start``, ...).
        limit: Maximum rows.

    Returns:
        Decoded audit rows, most useful first (chronological).
    """
    rows = _read_jsonl(LAZY_DIR / f"audit_{task_id}.jsonl", limit=limit)
    if kind:
        rows = [row for row in rows if str(row.get("kind", "")) == kind]
    return rows


def collect_conversation(task_id: str, intent_id: int | str = "") -> dict[str, Any]:
    """Read the worker conversation log for one task/intent.

    Args:
        task_id: Loop task identifier.
        intent_id: Optional intent filter.

    Returns:
        Mapping with ``messages`` per intent; empty when missing.
    """
    path = LAZY_DIR / f"convo_{task_id}.json"
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}
    intents = data.get("intents")
    if not isinstance(intents, dict):
        return {}
    if intent_id and str(intent_id) in intents:
        return {"intents": {str(intent_id): intents[str(intent_id)]}}
    return data


def collect_traffic(task_id: str, limit: int = MAX_AUDIT_ROWS) -> list[dict[str, Any]]:
    """Read the captured proxy traffic for one task.

    Args:
        task_id: Loop task identifier.
        limit: Maximum rows.

    Returns:
        Traffic rows with ``command`` and truncated ``output``.
    """
    rows = _read_jsonl(LAZY_DIR / f"traffic_{task_id}.jsonl", limit=limit)
    for row in rows:
        output = row.get("output")
        if isinstance(output, str) and len(output) > MAX_OUTPUT_TAIL:
            row["output"] = output[:MAX_OUTPUT_TAIL] + "..."
    return rows


def collect_beacon_sessions() -> list[dict[str, Any]]:
    """Summarize recorded beacon sessions.

    Returns:
        One row per beacon history file: client id, record count, first
        and last record timestamps.
    """
    sessions: list[dict[str, Any]] = []
    for path in sorted(SESSIONS_DIR.glob("*.records.jsonl")):
        rows = _read_jsonl(path)
        if not rows:
            continue
        last = rows[-1]
        sessions.append(
            {
                "client_id": path.stem.replace(".records", ""),
                "records": len(rows),
                "hostname": str(last.get("hostname", "")),
                "ips": str(last.get("ips", "")),
                "user": str(last.get("user", "")),
                "last_command": str(last.get("command", ""))[:MAX_OUTPUT_TAIL],
                "last_output": str(last.get("output", ""))[:MAX_OUTPUT_TAIL],
            }
        )
    return sessions


def aggregate_metrics(runs: list[LoopRunSummary]) -> dict[str, Any]:
    """Compute engagement-level metrics over loop runs.

    Args:
        runs: Loop run summaries.

    Returns:
        Mapping with totals, success rate and average detection
        probability across all executed commands.
    """
    total_commands = sum(run.commands for run in runs)
    total_ok = sum(run.commands_ok for run in runs)
    weighted_detection = (
        sum(run.detection_avg * run.commands for run in runs if run.commands) / total_commands
        if total_commands
        else 0.0
    )
    phases = sorted({step for run in runs for step in run.steps})
    return {
        "runs": len(runs),
        "tasks_done": sum(1 for run in runs if run.status == STATUS_DONE),
        "tasks_paused": sum(1 for run in runs if run.status == STATUS_PAUSED),
        "commands": total_commands,
        "commands_ok": total_ok,
        "ok_rate": round(total_ok / total_commands, 3) if total_commands else 0.0,
        "blocked": sum(run.blocked for run in runs),
        "detection_avg": round(weighted_detection, 3),
        "findings": sum(run.findings for run in runs),
        "reproduced": sum(run.reproduced for run in runs),
        "phases": phases,
    }


def render_loops_html(runs: list[LoopRunSummary], metrics: dict[str, Any]) -> str:
    """Render the loops section for the engagement report.

    Args:
        runs: Loop run summaries.
        metrics: Aggregated engagement metrics.

    Returns:
        HTML fragment with the metrics table and per-run cards.
    """
    rows = "".join(
        "<tr>"
        f"<td>{run.task_id}</td>"
        f"<td>{run.goal[:60]}</td>"
        f"<td>{run.target or '-'}</td>"
        f"<td>{run.status}</td>"
        f"<td>{run.rounds}</td>"
        f"<td>{run.commands}</td>"
        f"<td>{run.ok_rate:.0%}</td>"
        f"<td>{run.detection_avg:.2f}</td>"
        f"<td>{run.findings}</td>"
        "</tr>"
        for run in runs
    )
    return (
        "<h2>Autonomous loop activity</h2>"
        "<table class='metrics'><tr><th>Runs</th><th>Done</th><th>Commands</th>"
        "<th>Success</th><th>Blocked</th><th>Avg detection</th><th>Findings</th></tr>"
        "<tr>"
        f"<td>{metrics['runs']}</td><td>{metrics['tasks_done']}</td><td>{metrics['commands']}</td>"
        f"<td>{metrics['ok_rate']:.0%}</td><td>{metrics['blocked']}</td>"
        f"<td>{metrics['detection_avg']:.2f}</td><td>{metrics['findings']}</td>"
        "</tr></table>"
        "<table><tr><th>Task</th><th>Goal</th><th>Target</th><th>Status</th>"
        "<th>Rounds</th><th>Commands</th><th>OK rate</th><th>Det. avg</th><th>Findings</th></tr>"
        f"{rows}</table>"
    )


def render_beacons_html(sessions: list[dict[str, Any]]) -> str:
    """Render the beacon section for the engagement report.

    Args:
        sessions: Beacon session summaries.

    Returns:
        HTML fragment; empty string when there are no sessions.
    """
    if not sessions:
        return ""
    rows = "".join(
        "<tr>"
        f"<td>{session['client_id']}</td>"
        f"<td>{session['hostname']}</td>"
        f"<td>{session['ips']}</td>"
        f"<td>{session['user']}</td>"
        f"<td>{session['records']}</td>"
        f"<td>{session['last_command'][:100]}</td>"
        "</tr>"
        for session in sessions
    )
    return (
        "<h2>Beacon sessions</h2>"
        "<table><tr><th>Client</th><th>Hostname</th><th>IPs</th><th>User</th>"
        "<th>Records</th><th>Last command</th></tr>" + rows + "</table>"
    )


def iso_from_ts(ts: float) -> str:
    """Format a unix timestamp as ISO 8601 UTC.

    Args:
        ts: Unix timestamp.

    Returns:
        ISO string; empty for zero timestamps.
    """
    if not ts:
        return ""
    return datetime.fromtimestamp(ts, tz=UTC).isoformat()
