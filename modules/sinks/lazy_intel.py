"""Lazy intel sink: mirror exploit-intelligence matches into the stores.

Every ``lazy_intel`` outcome event (one per exposure report, from
``modules.lazy_exposure.publish_report``) lands the bounded matches as

- WorldModel vulnerabilities with a CVE id so the ``/intel`` and
  ``/graphattack`` pages (which fuse ``sessions/world_model.json``)
  show the intelligence on the host finding nodes, and
- ``modules.db`` workspace vuln rows (with cve, severity, references)
  so ``lazysearch``, ``db vulns`` and every SQLite consumer see it
  without re-running the matcher.

Prevents duplicate rows: a host/cve pair already in either store is
skipped. Sink is best-effort by contract; never raises.
"""

from __future__ import annotations

from modules.lazy_heat import SEVERITY_FROM_HEAT
from modules.outcome_bus import OutcomeEvent
from modules.world_model import get_world_model

_INTEL_KIND = "lazy_intel"
_MAX_VULNS_PER_EVENT = 8
_MAX_DESCRIPTION = 240


def apply(event: OutcomeEvent) -> bool:
    """Mirror one lazy_intel event into the world model and the database.

    Args:
        event: Outcome bus event of kind ``lazy_intel``.

    Returns:
        True when at least one store accepted a write; False otherwise.
    """
    if str(event.kind or "") != _INTEL_KIND:
        return False
    host = event.host_value
    if not host:
        return False
    matches = (event.metadata or {}).get("matches") or []
    if not isinstance(matches, list):
        return False
    temperature = str((event.metadata or {}).get("temperature") or "")
    severity = str(event.severity or "medium")
    stored = 0
    for row in matches[:_MAX_VULNS_PER_EVENT]:
        if not isinstance(row, dict) or not str(row.get("cve_id") or ""):
            continue
        if _world_mirror(host, row, temperature, severity):
            stored += 1
        if _db_mirror(host, row):
            stored += 1
    return stored > 0


def _world_mirror(host: str, row: dict, temperature: str, severity: str) -> bool:
    """Add one CVE finding to the world model when not already present.

    Args:
        host: Target address.
        row: Compact match row (cve_id, product, version, reference).
        temperature: Report temperature for the note context.
        severity: Event severity label.

    Returns:
        True when a new vulnerability was stored.
    """
    cve = str(row.get("cve_id") or "")
    try:
        world = get_world_model()
        known_cves = {getattr(entry, "cve", "") for entry in world._vulns}
        if cve in known_cves:
            return False
        title = f"{row.get('product', 'service')} match ({temperature})".strip()
        world.add_vulnerability(title, host=host, cve=cve, severity=severity.upper())
        detail = (
            f"lazy_intel {cve} product={row.get('product')} version={row.get('version')} "
            f"port={row.get('port')} evidence={row.get('evidence')}"
        )
        world.add_note(host, detail[:_MAX_DESCRIPTION])
        return True
    except Exception:
        return False


def _db_mirror(host: str, row: dict) -> bool:
    """Mirror one match into the workspace database, deduped by (host, cve).

    Args:
        host: Target address.
        row: Compact match row.

    Returns:
        True when a new vuln row was inserted.
    """
    cve = str(row.get("cve_id") or "")
    try:
        from modules.db import get_db

        db = get_db()
        workspace_id = db.default_workspace()
        host_lookup = {item.get("address"): item for item in db.host_list(workspace_id)}
        entry = host_lookup.get(host)
        host_id = entry.get("id") if entry else db.host_add(workspace_id, host, state="scanned")
        rows = db.vuln_list(workspace_id)
        known_pairs = {(int(v.get("host_id") or 0), str(v.get("name") or "")) for v in rows}
        if (int(host_id), cve) in known_pairs:
            return False
        db.vuln_add(
            host_id,
            name=cve,
            severity=SEVERITY_FROM_HEAT.get(str(row.get("tier")), "medium"),
            description=f"lazy_intel {cve} on {row.get('product')} {row.get('version')} (port {row.get('port')})",
            refs="|".join(str(link)[:120] for link in (row.get("references") or [])[:2]),
        )
        return True
    except Exception:
        return False


__all__ = ["apply"]
