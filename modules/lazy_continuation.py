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
        updated: ISO timestamp of the last write.
    """

    target: str
    task_id: str = ""
    goal: str = ""
    status: str = ""
    settlement: str = ""
    findings: list[str] = field(default_factory=list)
    next_steps: list[str] = field(default_factory=list)
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
        updated=str(data.get("updated", "") or ""),
    )


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


__all__ = ["ContinuationRecord", "load", "recall_candidates", "record_path", "save"]
