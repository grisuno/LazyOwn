"""C2 dashboard sink: banners, CVEs and operator notes."""

from __future__ import annotations

from pathlib import Path

from modules.c2_surfaces import append_note, publish_banner, publish_cve, severity_to_risk
from modules.outcome_bus import SESSIONS_DIR, OutcomeEvent


def apply(event: OutcomeEvent) -> bool:
    """Write the operator-visible surfaces for one outcome.

    Args:
        event: Outcome to publish.

    Returns:
        True when at least one surface changed.
    """
    sessions = Path(str(event.metadata.get("sessions_dir") or SESSIONS_DIR))
    changed = False
    host = event.host_value
    if host and (event.port or event.service or event.banner):
        changed = (
            publish_banner(
                hostname=host,
                port=event.port,
                protocol=event.protocol or "tcp",
                service=event.service,
                extra=str(event.banner or event.description or "")[:300],
                sessions_dir=sessions,
            )
            or changed
        )
    if event.cve:
        changed = (
            publish_cve(
                title=f"{event.cve} on {host} ({event.title or event.source})",
                description=f"{event.description or event.title} [{event.mitre_id}]"
                + (" SHELL OBTAINED" if event.shell else ""),
                operator=event.source or "autonomous_loop",
                risk=severity_to_risk(event.severity),
                sessions_dir=sessions,
            )
            or changed
        )
    if host and (event.shell or event.title or event.kind in ("finding", "exploit", "emulation", "chain")):
        line = f"{event.kind.upper()} {host} {event.title or event.source}".strip()
        if event.shell:
            line += " SHELL"
        changed = append_note(line, sessions_dir=sessions) or changed
    return changed
