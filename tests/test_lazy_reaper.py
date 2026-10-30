"""Reaper contract: orphan running tasks are harvested with proof of death.

Every scenario states Given, When, Then. Only ``running`` tasks with a
heartbeat older than the window expire; fresh beats, queued, paused
past-rows and unknown fields never count as evidence. Failures in the
store shrink the scan instead of closing anything.
"""

from __future__ import annotations

from typing import Any

from modules.lazy_reaper import DEFAULT_STALE_SECONDS, reap


class _FakeStore:
    """Task-store stub with the reaper's needed surface."""

    def __init__(self, rows: list[dict[str, Any]]) -> None:
        """Bind rows mutably."""
        self.rows = rows

    def list(self):
        """Return task rows."""
        return list(self.rows)

    def get(self, task_id: str) -> dict | None:
        """Return the row by id."""
        for row in self.rows:
            if row.get("task_id") == task_id:
                return row
        return None

    def set_status(self, task_id: str, status: str) -> bool:
        """Stamp the status in place."""
        row = self.get(task_id)
        if row is None:
            return False
        row["status"] = status
        return True

    def _persist(self) -> None:
        """Persist (noop for the stub)."""
        return None


def _row(task_id: str, status: str, beat: float) -> dict[str, Any]:
    """Build one task row shape."""
    return {
        "task_id": task_id,
        "status": status,
        "runtime": {"last_beat": beat, "workers": 1},
    }


def test_stale_running_task_expires():
    """Given a beat older than the window, When reaping, Then the row expires once."""
    store = _FakeStore([_row("t0001", "running", 0.0)])
    counts = reap(store, now=DEFAULT_STALE_SECONDS + 60.0)
    assert counts == {"examined": 1, "expired": 1, "kept": 0}
    assert store.rows[0]["status"] == "timeout"
    assert store.rows[0]["runtime"]["abort_cause"] == "timeout"


def test_fresh_heartbeat_and_other_statuses_kept():
    """Given fresh/paused/queued rows, When reaping, Then nothing expires."""
    reference = 10000.0
    store = _FakeStore(
        [
            _row("t0001", "running", reference - 60.0),
            _row("t0002", "running", reference - DEFAULT_STALE_SECONDS - 99999.0),
            _row("t0003", "queued", 0.0),
            _row("t0004", "paused", 0.0),
        ]
    )
    store.rows[1]["runtime"]["last_beat"] = reference - DEFAULT_STALE_SECONDS - 10.0
    counts = reap(store, now=reference)
    assert counts["expired"] == 1 and counts["kept"] == 1
    assert store.rows[0]["status"] == "running"
    assert store.rows[2]["status"] == "queued"
    assert store.rows[3]["status"] == "paused"


def test_missing_beat_is_insufficient_evidence():
    """Given a running row with no beat, When reaping, Then it is kept, never harvested."""
    store = _FakeStore([_row("t0001", "running", 0.0)])
    del store.rows[0]["runtime"]
    counts = reap(store, now=999999.0)
    assert counts == {"examined": 1, "expired": 0, "kept": 1}


def test_unusable_store_reports_zero():
    """Given a store that crashes, When reaping, Then the summary degrades to zero."""

    class Broken:
        """Store raising on list()."""

        def list(self):
            """Raise to simulate a corrupt store."""
            raise RuntimeError("corrupt store")

    counts = reap(Broken(), now=999999.0)
    assert counts == {"examined": 0, "expired": 0, "kept": 0}
