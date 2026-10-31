"""Objective queue plumbing: the autonomous loop's read side of the objective store.

``skills.lazyown_objective`` owns the JSONL store and ``modules.sinks.objectives``
appends proven-outcome follow-ups; until now the LazyLoopEngine never consumed
either (the objectives file was write-only for the loop). This module closes
that gap with one small contract the planner and the wrap-up round both call:

pending_objectives   -> planner wake candidates
mark_started         -> objective claimed by one task this round
settle               -> wrap-up completes or requeues the objective

Parsing is tolerant: malformed or foreign lines are skipped, never fatal, so
campaign state cannot wedge the planner. State transitions rewrite only the
touched records and keep every other line byte-compatible.
"""

from __future__ import annotations

import datetime
import json
import os
import re
from dataclasses import dataclass
from pathlib import Path

_LAZYOWN_DIR = Path(os.environ.get("LAZYOWN_DIR", str(Path(__file__).resolve().parent.parent)))
_SESSIONS_DIR = _LAZYOWN_DIR / "sessions"
_OBJECTIVES_FILE = _SESSIONS_DIR / "objectives.jsonl"

_PRIORITY_RANK = {"critical": 9, "high": 8, "medium": 7, "low": 6}
_MAX_ITEMS = 64


@dataclass(frozen=True)
class ObjectiveCandidate:
    """One pending objective shaped for planner consumption.

    Attributes:
        objective_id: Store id (8-char hex or ``outcome_`` digest).
        text: Objective text actionable as an intent.
        priority: Loop priority; critical outranks generic candidates.
    """

    objective_id: str
    text: str
    priority: int


def _objectives_path() -> Path:
    """Return the objective JSONL path honouring the active sessions directory.

    Resolves the loop's live ``SESSIONS_DIR`` at call time so the store the
    planner reads is always the one the running engine writes to; this keeps
    the objective queue aligned when the sessions directory is redirected
    (tests, isolated campaigns). Falls back to the import-time default when
    the loop module is unavailable.
    """
    try:
        from modules.lazy_loop import SESSIONS_DIR as _loop_sessions

        return Path(_loop_sessions) / "objectives.jsonl"
    except Exception:
        return _OBJECTIVES_FILE


def _load_records(path: Path) -> list[dict]:
    """Return every parseable JSONL record with a usable id and text."""
    records: list[dict] = []
    try:
        raw = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return records
    for line in raw.splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            item = json.loads(line)
        except json.JSONDecodeError:
            continue
        if not isinstance(item, dict):
            continue
        objective_id = str(item.get("id", "") or "").strip()
        text = str(item.get("text", "") or "").strip()
        if not objective_id or not text:
            continue
        records.append(item)
    return records


def _save_records(path: Path, records: list[dict]) -> bool:
    """Atomically rewrite the store from the mutated record list."""
    if not records:
        return False
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        tmp = path.with_suffix(".tmp")
        tmp.write_text("\n".join(json.dumps(record, ensure_ascii=False) for record in records) + "\n", encoding="utf-8")
        tmp.replace(path)
        return True
    except OSError:
        return False


def pending_objectives(limit: int = 2, target: str = "") -> list[ObjectiveCandidate]:
    """Return pending objectives shaped as planner candidates.

    Objectives whose recorded ``context.target`` names a different host than
    the one under test are skipped so one loop never drags another target's
    work in; objectives without a recorded target are global and always
    considered. Oldest first within the same priority.

    Args:
        limit: Maximum candidates returned.
        target: Host the task is scoped to (blank when unknown).

    Returns:
        Priority-ordered :class:`ObjectiveCandidate` list.
    """
    if int(limit or 0) <= 0:
        return []
    records = _load_records(_objectives_path())
    host = str(target or "").strip()
    wanted = [item for item in records if str(item.get("status", "")) == "pending"][:_MAX_ITEMS]
    wanted.sort(
        key=lambda item: (
            -int(item.get("priority_rank", _PRIORITY_RANK.get(str(item.get("priority", "")).lower(), 6)) or 6),
            str(item.get("updated_at", "") or item.get("created_at", "") or ""),
        )
    )
    out: list[ObjectiveCandidate] = []
    for item in wanted:
        context = item.get("context") if isinstance(item.get("context"), dict) else {}
        bound_host = str((context or {}).get("target", "") or "").strip()
        if host and bound_host and bound_host != host:
            continue
        text = str(item.get("text", "")).strip()
        if not text:
            continue
        rank = _PRIORITY_RANK.get(str(item.get("priority", "")).lower(), 6)
        out.append(
            ObjectiveCandidate(
                objective_id=str(item["id"]),
                text=text[:300],
                priority=rank,
            )
        )
        if len(out) >= int(limit):
            break
    return out


def _update_status(objective_id: str, status: str, notes: str) -> bool:
    """Flip one objective's status in place and persist the store."""
    path = _objectives_path()
    records = _load_records(path)
    found = False
    stamp = datetime.datetime.now(datetime.UTC).isoformat()
    for record in records:
        if str(record.get("id", "")) != objective_id:
            continue
        if str(record.get("status", "")) == status:
            continue
        record["status"] = status
        record.setdefault("updated_at", stamp)
        if notes:
            previous = str(record.get("notes", "") or "")
            record["notes"] = (f"{notes}; {previous}" if previous else notes)[:500]
        record["updated_at"] = stamp
        found = True
        break
    if not found:
        return False
    return _save_records(path, records)


def mark_started(objective_id: str, task_id: str = "") -> bool:
    """Mark an objective ``in_progress`` when a task claims it.

    Args:
        objective_id: Store id to claim.
        task_id: Claiming loop task for the audit note.

    Returns:
        True when the status flipped; False when already claimed or absent.
    """
    if not objective_id:
        return False
    note = f"claimed by {task_id}" if task_id else "claimed by auto_loop"
    try:
        return _update_status(objective_id, "in_progress", note)
    except Exception:
        return False


def settle(objective_id: str, task_id: str = "", success: bool = False) -> str:
    """Complete a done objective or requeue an unfinished one.

    Wrap-up handler: when the task proved the objective (its intent reached
    ``done``) the objective marks ``done``; otherwise it returns to
    ``pending`` so a later task can attempt it again.

    Args:
        objective_id: Store id to settle.
        task_id: Settling loop task for the audit note.
        success: True when the owning intent completed successfully.

    Returns:
        The new status (``done`` or ``pending``), empty when not found.
    """
    if not objective_id:
        return ""
    new_status = "done" if success else "pending"
    note = f"settled by {task_id}" if task_id else "settled by auto_loop"
    path = _objectives_path()
    records = _load_records(path)
    for record in records:
        if str(record.get("id", "")) != objective_id:
            continue
        previous = str(record.get("status", ""))
        if previous == new_status and not success:
            return new_status
        record["status"] = new_status
        stamp = datetime.datetime.now(datetime.UTC).isoformat()
        record["updated_at"] = stamp
        appended = f"{note}"
        old_notes = str(record.get("notes", "") or "")
        record["notes"] = (f"{appended}; {old_notes}" if old_notes else appended)[:500]
        if _save_records(path, records):
            return new_status
        return ""
    return ""


def objective_ids_from_text(text: str) -> str:
    """Extract the objective id embedded in an intent summary prefix.

    Args:
        text: Intent text like ``objective ab12cd34: enumerate shares``.

    Returns:
        The id token, or empty when the text is not objective-tagged.
    """
    match = re.match(r"^objective\s+([0-9a-z_]{4,64}):", (text or "").strip())
    return match.group(1) if match else ""


__all__ = [
    "ObjectiveCandidate",
    "mark_started",
    "objective_ids_from_text",
    "pending_objectives",
    "settle",
]
