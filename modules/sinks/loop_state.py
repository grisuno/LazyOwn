"""Loop state sink: durable SQLite mirror of every outcome event.

The sink appends every outcome to the shared engine event log
(:mod:`modules.loop.event_store`), raises a ``foothold`` worker
message whenever an event reports confirmed shell access, so sibling
workers see the foothold on their next prompt context refresh, and
plants the outcome into LazyHebb (:mod:`modules.lazy_hebb`) so later
planning rounds recall it with zero inference.
"""

from __future__ import annotations

from modules.loop.event_store import record_outcome
from modules.outcome_bus import OutcomeEvent


def apply(event: OutcomeEvent) -> bool:
    """Mirror one outcome into the SQLite event store and LazyHebb.

    Args:
        event: Outcome to persist.

    Returns:
        True when a row was appended, False when nothing was stored.
    """
    try:
        payload = event.to_dict()
    except Exception:
        return False
    stored = False
    try:
        row_id = record_outcome(payload)
        stored = row_id > 0
    except Exception:
        stored = False
    try:
        from modules import orchestrator_config
        from modules.lazy_hebb import remember_outcome

        if stored and orchestrator_config.hebb_config().get("record_outcomes"):
            remember_outcome(payload)
    except Exception:
        pass
    return stored
