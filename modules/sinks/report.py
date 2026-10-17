"""Report sink: refresh the operator session report."""

from __future__ import annotations

from modules.c2_surfaces import refresh_session_report
from modules.outcome_bus import OutcomeEvent


def apply(event: OutcomeEvent) -> bool:
    """Refresh the session report for terminal or explicit report outcomes.

    Args:
        event: Outcome to report.

    Returns:
        True when the report command succeeded.
    """
    explicit = bool(event.metadata.get("refresh_report"))
    if event.kind not in ("report", "chain") and not explicit:
        return False
    return bool(refresh_session_report())
