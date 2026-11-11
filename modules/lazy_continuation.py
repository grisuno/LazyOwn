"""Task continuation records: campaign memory that survives loop restarts.

A finished loop task writes its settlement context to a per-target
continuation record under ``sessions/continuations/<target>.json``: goal,
terminal status, the wrap-up settlement text, confirmed findings and the
open next steps. The next task bound to the same target reads it back as
planner wake candidates, so a restarted loop (operator restart, daemon
recycle, C2 loop respawn) continues where the previous run stopped
instead of re-running the same recon.

This is the campaign blackboard pattern: the record is a working summary,
not a verified fact — proven findings still live in the graph, world
model and finding lifecycle; the continuation only steers the next task
toward the unfinished work.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_DIR = REPO_ROOT / "sessions" / "continuations"

_MAX_RECORDS = 40
_MAX_TEXT_CHARS = 2000
_MAX_NEXT_STEPS = 6
_MAX_CREDENTIALS = 10
_MAX_DEVIATIONS = 6
_SLUG_SAFE = re.compile(r"[^a-z0-9_.-]+")


@dataclass
class ContinuationRecord:
    """One target's campaign continuation state.

    Attributes:
        target: Host the record is bound to (slug key).
        task_id: Loop task that last wrote the record.
        goal: Goal of that task.
        status: Terminal status of that task.
        settlement: Wrap-up settlement text.
        findings: Confirmed finding texts.
        next_steps: Unfinished work the next task should try.
        credentials: Reusable ``user:pass`` or hash hints for the successor.
        deviations: Planned-versus-actual notes the successor must honor.
        updated: ISO timestamp of the last write.
    """

    target: str
    task_id: str = ""
    goal: str = ""
    status: str = ""
    settlement: str = ""
    findings: list[str] = field(default_factory=list)
    next_steps: list[str] = field(default_factory=list)
    credentials: list[str] = field(default_factory=list)
    deviations: list[str] = field(default_factory=list)
    updated: str = ""


def _dir() -> Path:
    """Return the continuations directory, creating it when missing."""
    directory = DEFAULT_DIR
    directory.mkdir(parents=True, exist_ok=True)
    return directory


def _slug(target: str) -> str:
    """Return the filesystem-safe key for one target."""
    cleaned = _SLUG_SAFE.sub("_", str(target or "").strip().lower()).strip("_") or "unknown"
    return cleaned[:120]


def record_path(target: str) -> Path:
    """Return the continuation record path for one target.

    Args:
        target: Host address or scope name.

    Returns:
        The JSON record path (may not exist yet).
    """
    return _dir() / f"{_slug(target)}.json"


def save(
    target: str,
    task_id: str = "",
    goal: str = "",
    status: str = "",
    settlement: str = "",
    findings: list[str] | None = None,
    next_steps: list[str] | None = None,
    credentials: list[str] | None = None,
    deviations: list[str] | None = None,
) -> bool:
    """Write one target's continuation record atomically.

    Args:
        target: Host the record belongs to.
        task_id: Loop task writing the record.
        goal: Task goal text.
        status: Terminal task status.
        settlement: Wrap-up settlement summary.
        findings: Confirmed finding texts.
        next_steps: Unfinished next steps for the follow-up task.
        credentials: Reusable ``user:pass`` or hash hints for the successor.
        deviations: Planned-versus-actual notes for the successor.

    Returns:
        True when persisted; False on I/O failure.
    """
    if not str(target or "").strip():
        return False
    import datetime

    payload = {
        "target": str(target).strip(),
        "task_id": str(task_id or ""),
        "goal": str(goal or "")[:_MAX_TEXT_CHARS],
        "status": str(status or ""),
        "settlement": str(settlement or "")[:_MAX_TEXT_CHARS],
        "findings": [str(item)[:400] for item in (findings or [])][:10],
        "next_steps": [str(item)[:400] for item in (next_steps or []) if str(item).strip()][
            :_MAX_NEXT_STEPS
        ],
        "credentials": [str(item)[:200] for item in (credentials or []) if str(item).strip()][:_MAX_CREDENTIALS],
        "deviations": [str(item)[:400] for item in (deviations or []) if str(item).strip()][:_MAX_DEVIATIONS],
        "updated": datetime.datetime.now(datetime.UTC).isoformat(),
    }
    path = record_path(target)
    try:
        tmp = path.with_suffix(".tmp")
        tmp.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
        tmp.replace(path)
        return True
    except OSError:
        return False


def load(target: str) -> ContinuationRecord | None:
    """Read one target's continuation record.

    Args:
        target: Host address.

    Returns:
        The :class:`ContinuationRecord`, or None when absent/unreadable.
    """
    try:
        data = json.loads(record_path(target).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None
    if not isinstance(data, dict):
        return None
    return ContinuationRecord(
        target=str(data.get("target", "") or target),
        task_id=str(data.get("task_id", "") or ""),
        goal=str(data.get("goal", "") or ""),
        status=str(data.get("status", "") or ""),
        settlement=str(data.get("settlement", "") or ""),
        findings=[str(item) for item in (data.get("findings") or [])][:10],
        next_steps=[str(item) for item in (data.get("next_steps") or [])][:_MAX_NEXT_STEPS],
        credentials=[str(item) for item in (data.get("credentials") or [])][:_MAX_CREDENTIALS],
        deviations=[str(item) for item in (data.get("deviations") or [])][:_MAX_DEVIATIONS],
        updated=str(data.get("updated", "") or ""),
    )


def handover_brief(target: str) -> str:
    """Render a target's continuation record as a successor-ready playbook.

    sapper-v2 has a saturating worker leave a written playbook for its
    replacement. This renders the same handover from the persisted record:
    goal, terminal status, the wrap-up settlement, confirmed findings, the
    open next steps and any reusable credentials, so a fresh worker resumes
    with knowledge instead of a cold graph.

    Args:
        target: Host whose record is rendered.

    Returns:
        A formatted multi-line brief, or an empty string when no record
        exists for the target.
    """
    record = load(target)
    if record is None:
        return ""
    lines = [
        f"# Handover for {record.target}",
        f"goal: {record.goal or '(none)'}",
        f"last status: {record.status or '(unknown)'} (task {record.task_id or '-'})",
    ]
    if record.settlement:
        lines.append(f"settlement: {record.settlement}")
    if record.findings:
        lines.append("confirmed findings:")
        lines.extend(f"  - {item}" for item in record.findings)
    if record.next_steps:
        lines.append("next steps:")
        lines.extend(f"  - {item}" for item in record.next_steps)
    if record.credentials:
        lines.append("reusable credentials:")
        lines.extend(f"  - {item}" for item in record.credentials)
    if record.deviations:
        lines.append("deviations the plan took (honor them, do not re-derive):")
        lines.extend(f"  - {item}" for item in record.deviations)
    return "\n".join(lines)


def recall_candidates(target: str, limit: int = 3) -> list[tuple[str, str]]:
    """Return ``(intent_summary, reason)`` wake candidates for one target.

    Args:
        target: Host the next task is scoped to.
        limit: Maximum candidates returned.

    Returns:
        Continuation wake candidates built from the record's next steps
        and open findings; empty when no record exists.
    """
    record = load(target)
    if record is None:
        return []
    out: list[tuple[str, str]] = []
    for step in record.next_steps:
        text = str(step).strip()
        if not text:
            continue
        out.append(
            (
                f"continuation: {text[:300]}",
                f"prior task {record.task_id} ({record.status}) left this open",
            )
        )
        if len(out) >= max(1, int(limit)):
            break
    return out


__all__ = ["ContinuationRecord", "handover_brief", "load", "recall_candidates", "record_path", "save"]
