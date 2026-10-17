"""Campaign database sink: opt-in host and vulnerability mirror."""

from __future__ import annotations

from modules.db import get_db
from modules.outcome_bus import OutcomeEvent


def apply(event: OutcomeEvent) -> bool:
    """Mirror one outcome into the campaign database.

    The sink is opt-in: it never runs unless the event names it or an
    operator enables it, so routine loop traffic does not open SQLite.

    Args:
        event: Outcome to mirror.

    Returns:
        True when a host or vulnerability row was written.
    """
    host = event.host_value
    if not host:
        return False
    title = event.title or event.cve
    if not title:
        return False
    try:
        database = get_db()
        workspace = database.default_workspace(str(event.metadata.get("workspace", "default") or "default"))
        host_id = database.host_add(workspace, host, hostname=host)
        database.vuln_add(
            host_id,
            title[:200],
            severity=str(event.severity or "unknown").lower(),
            description=(event.description or title)[:2000],
            refs=event.cve or event.mitre_id,
        )
    except Exception:
        return False
    return True
