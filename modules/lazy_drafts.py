"""Injected objective drafts: close the lazy_drafts handoff loop.

``modules.lazy_bridge.push_objective_to_lazy`` writes task drafts under
``sessions/lazy_drafts/`` whenever an objective reaches the cross-engine
sync, but nothing read them back: Hermes/MCP-injected objectives vanished
from the loop's task board. This module is the read side. One function,
``drain``: every ``pending`` draft becomes a queued loop task (goal +
scope pre-seeded) and the draft is marked ``imported`` so one injection
never spawns two tasks, even across loop restarts.
"""

from __future__ import annotations

import datetime
import json
from pathlib import Path

from modules.lazy_loop import BASE_DIR

DRAFTS_SUBDIR = "lazy_drafts"
_STATUS_PENDING = "pending"
_STATUS_IMPORTED = "imported"
_MAX_DRAFTS = 20
_MAX_GOAL_CHARS = 500


def _drafts_dir() -> Path:
    """Return the drafts directory, creating it when missing."""
    path = Path(BASE_DIR) / "sessions" / DRAFTS_SUBDIR
    path.mkdir(parents=True, exist_ok=True)
    return path


def drain(engine) -> list[str]:
    """Import every pending draft into the loop task board.

    Args:
        engine: LazyLoopEngine owning ``create_task``/``ensure_target``.

    Returns:
        The imported task ids (queued for admission, not run).
    """
    directory = _drafts_dir()
    imported: list[str] = []
    try:
        paths = sorted(directory.glob("task_*.json"))
    except OSError:
        return imported
    for path in paths[:_MAX_DRAFTS]:
        try:
            record = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        if not isinstance(record, dict) or str(record.get("status", "")) != _STATUS_PENDING:
            continue
        goal = str(record.get("goal", "") or "").strip()[:_MAX_GOAL_CHARS]
        if not goal:
            continue
        try:
            summary = engine.create_task(goal)
        except Exception:
            continue
        task_id = str(summary.get("task_id", "") or "")
        if not task_id:
            continue
        for item in (record.get("scope") or [])[:10]:
            if not isinstance(item, dict):
                continue
            value = str(item.get("value", "") or "").strip()
            if value:
                try:
                    engine.ensure_target(task_id, value, "lazy_draft import")
                except Exception:
                    continue
        record["status"] = _STATUS_IMPORTED
        record["imported_task_id"] = task_id
        stamp = datetime.datetime.now(datetime.UTC).isoformat()
        record["updated"] = stamp
        try:
            path.write_text(json.dumps(record, ensure_ascii=False, indent=2), encoding="utf-8")
        except OSError:
            continue
        imported.append(task_id)
    if imported:
        try:
            from modules.lazy_loop import ActivityLog

            ActivityLog("engine").emit("drafts", "drain", f"imported {len(imported)} lazy_draft task(s)")
        except Exception:
            pass
    return imported


__all__ = ["drain"]
