"""Loop state sink: durable SQLite mirror of every outcome event.

The sink appends every outcome to the shared engine event log
(:mod:`modules.loop.event_store`) and raises a ``foothold`` worker
message whenever an event reports confirmed shell access, so sibling
workers see the foothold on their next prompt context refresh.
"""

from __future__ import annotations

from modules.loop.event_store import record_outcome
from modules.outcome_bus import OutcomeEvent


def apply(event: OutcomeEvent) -> bool:
    """Mirror one outcome into the SQLite event store.

    Args:
        event: Outcome to persist.

    Returns:
        True when a row was appended, False when nothing was stored.
    """
    try:
        payload = event.to_dict()
    except Exception:
        return False
    try:
        row_id = record_outcome(payload)
        return row_id > 0
    except Exception:
        return False
