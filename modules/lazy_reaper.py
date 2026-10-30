"""Reaper: expire lazy-loop tasks whose process proves dead.

Lazy re-brand of the broker-verified orphan pattern: a stuck ``running``
row is only harvested when the liveness signal it owns (its heartbeat)
is provably stale — the reaper never closes on absence of evidence. A
heartbeat inside the window, an old-but-paused or queued row stays
untouched; rows that expire get one idempotent terminal stamp and an
abort cause so the retry surfaces can re-enter them deliberately.

State: the operator's own task store (``sessions/lazy/tasks.json``);
audit trail lands in ``sessions/lazy/reaper.jsonl``, bounded per file.
"""

from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Any

REAPER_LOG_FILENAME = "reaper.jsonl"
DEFAULT_STALE_SECONDS = 45 * 60.0
_MAX_LOG_ENTRIES = 2000

_VALID_EXPIRE_STATUSES = ("running",)
_TERMINAL_STATUS = "timeout"
_ABORT_CAUSE = "timeout"


def reap(
    store: Any,
    log_path: str | Path | None = None,
    now: float | None = None,
    stale_seconds: float = DEFAULT_STALE_SECONDS,
) -> dict[str, int]:
    """Expire tasks whose heartbeat is provably stale.

    Args:
        store: Task store object with ``list()`` rows and
            ``set_status(task_id, status)``; pass the engine store.
        log_path: Audit trail file; defaults under the lazy store dir.
        now: Reference epoch; defaults to current time.
        stale_seconds: Heartbeat age that proves death.

    Returns:
        ``{"examined", "expired", "kept"}`` counts. Store failures are
        fail-soft: an unusable store reports ``examined=0`` and nothing
        changes.
    """
    reference = float(now if now is not None else time.time())
    examined = expired_count = kept = 0
    try:
        rows = [row for row in (store.list() or []) if isinstance(row, dict)]
    except Exception:
        rows = []
    for row in rows:
        task_id = str(row.get("task_id", "") or "")
        status = str(row.get("status", "") or "")
        if not task_id or status not in _VALID_EXPIRE_STATUSES:
            continue
        examined += 1
        runtime = row.get("runtime", {}) or {}
        raw_beat = runtime.get("last_beat")
        if raw_beat is None or str(raw_beat).strip() == "":
            kept += 1
            continue
        try:
            last_beat = float(raw_beat)
        except (TypeError, ValueError):
            kept += 1
            continue
        if last_beat < 0:
            kept += 1
            continue
        age = reference - last_beat
        if age < stale_seconds:
            kept += 1
            continue
        stamped = _expire(store, task_id)
        if stamped:
            expired_count += 1
            _log(
                log_path,
                {"ts": time.time(), "task_id": task_id, "age": round(age, 1),
                 "action": "expired", "status": _TERMINAL_STATUS},
            )
        else:
            kept += 1
    return {"examined": examined, "expired": expired_count, "kept": kept}


def _expire(store: Any, task_id: str) -> bool:
    """Stamp one task as terminally outdated.

    Args:
        store: Task store.
        task_id: Task to expire.

    Returns:
        True when the store accepted the stamp.
    """
    try:
        if not store.set_status(task_id, _TERMINAL_STATUS):
            return False
        record = store.get(task_id) or {}
        runtime = record.setdefault("runtime", {})
        runtime["abort_cause"] = _ABORT_CAUSE
        runtime["abort_detail"] = "reaper expired a running task with stale heartbeat"
        store._persist()
        return True
    except Exception:
        return False


def _log(log_path: str | Path | None, row: dict[str, Any]) -> None:
    """Append one bounded audit row."""
    try:
        path = Path(str(log_path or "")) if log_path else None
        if path is None:
            try:
                from modules.lazy_loop import _store_path

                path = Path(str(_store_path(REAPER_LOG_FILENAME)))
            except Exception:
                return
        path.parent.mkdir(parents=True, exist_ok=True)
        entries: list[dict[str, Any]] = []
        try:
            if path.is_file():
                existing = json.loads(path.read_text(encoding="utf-8"))
                if isinstance(existing, list):
                    entries = [entry for entry in existing if isinstance(entry, dict)]
        except Exception:
            entries = []
        entries = [*entries, row][-_MAX_LOG_ENTRIES:]
        path.write_text(json.dumps(entries), encoding="utf-8")
    except Exception:
        pass


REPO_OUTPUT = REAPER_LOG_FILENAME
__all__ = ["DEFAULT_STALE_SECONDS", "REAPER_LOG_FILENAME", "reap"]
