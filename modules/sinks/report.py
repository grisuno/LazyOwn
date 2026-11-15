"""Report sink: refresh the session report and emit report artifacts."""

from __future__ import annotations

from modules.outcome_bus import OutcomeEvent


def apply(event: OutcomeEvent) -> bool:
    """Regenerate the engagement report for terminal or explicit outcomes.

    Refreshes the legacy session report JSON rendered by ``/report`` and,
    when ``auto_report_on_finish`` is enabled, writes the client-ready
    report artifacts. Generation is throttled and never raises.

    Args:
        event: Outcome to report.

    Returns:
        True when the session report was refreshed.
    """
    explicit = bool(event.metadata.get("refresh_report"))
    if event.kind not in ("report", "chain") and not explicit:
        return False
    from modules.report_autogen import generate_campaign_report

    outcome = generate_campaign_report(reason=f"outcome:{event.kind}")
    return bool(outcome.get("session_refreshed"))
