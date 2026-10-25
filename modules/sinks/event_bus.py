"""Unified event-bus sink: publish every outcome once."""

from __future__ import annotations

from modules.event_bus import publish_event
from modules.outcome_bus import OutcomeEvent, category_for_event, severity_for_event


def apply(event: OutcomeEvent) -> bool:
    """Publish one event to the unified bus.

    Args:
        event: Outcome to publish.

    Returns:
        True when the bus accepted the event.
    """
    try:
        publish_event(
            category=category_for_event(event.kind),
            event_type=event.kind,
            source=event.source or "outcome_bus",
            payload={
                "title": event.title,
                "description": event.description,
                "cve": event.cve,
                "mitre_id": event.mitre_id,
                "shell": event.shell,
                "success": event.success,
                "artifacts": list(event.artifacts),
                "metadata": dict(event.metadata),
            },
            severity=severity_for_event(event.severity),
            target=event.host_value,
            operator="autonomous_loop",
        )
    except Exception:
        return False
    return True
