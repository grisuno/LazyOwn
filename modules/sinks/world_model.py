"""World-model sink: hosts, services, vulnerabilities and credentials."""

from __future__ import annotations

from modules.obs_parser import Finding, FindingType
from modules.outcome_bus import OutcomeEvent
from modules.world_model import get_world_model

_FINDING_KINDS = frozenset({"finding", "exploit", "shell"})


def apply(event: OutcomeEvent) -> bool:
    """Write one outcome into the world model.

    Args:
        event: Outcome to persist.

    Returns:
        True when the model accepted the write.
    """
    host = event.host_value
    if not host:
        return False
    world = get_world_model()
    world.add_host(host)
    findings: list[Finding] = []
    if event.cve:
        findings.append(
            Finding(
                type=FindingType.CVE,
                value=event.cve,
                host=host,
                confidence=max(0.0, min(1.0, float(event.confidence or 0.0))),
            )
        )
    if event.shell:
        findings.append(
            Finding(
                type=FindingType.CREDENTIAL,
                value=f"shell:{event.source or event.kind}",
                host=host,
                confidence=1.0,
                metadata={"mitre_id": event.mitre_id},
            )
        )
    if findings:
        world.update_from_findings(findings)
    if event.port and event.service:
        try:
            world.add_service(
                host,
                int(str(event.port)),
                name=event.service,
                version=str(event.metadata.get("version", "") or ""),
                protocol=event.protocol or "tcp",
            )
        except (TypeError, ValueError):
            pass
    if event.title and event.kind in _FINDING_KINDS:
        world.add_vulnerability(
            event.title,
            host=host,
            cve=event.cve,
            severity=str(event.severity or "unknown").upper(),
        )
    note = event.description or event.banner
    if note:
        world.add_note(host, f"[{event.source or event.kind}] {note[:1000]}")
    return True
