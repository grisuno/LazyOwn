"""Campaign database sink: non-blocking host and vulnerability mirror.

The sink offloads every write to the single-writer queue in
:mod:`modules.db_writer` so routine autonomous-loop traffic never opens
SQLite on the hot path. Because the write is enqueued and applied on a
dedicated writer thread, this sink is safe to run by default.
"""

from __future__ import annotations

from modules.db import LazyOwnDB
from modules.db_writer import submit_write
from modules.outcome_bus import OutcomeEvent


def apply(event: OutcomeEvent) -> bool:
    """Enqueue one outcome mirror into the campaign database.

    The host and vulnerability write is deferred to the single-writer
    queue; this function returns as soon as the operation is accepted and
    never blocks the caller on SQLite I/O.

    Args:
        event: Outcome to mirror.

    Returns:
        True when a mirror operation was enqueued, False when the event
        carries no host or title, or the write queue rejected it.
    """
    host = event.host_value
    if not host:
        return False
    title = event.title or event.cve
    if not title:
        return False
    workspace_name = str(event.metadata.get("workspace", "default") or "default")
    name = title[:200]
    severity = str(event.severity or "unknown").lower()
    description = (event.description or title)[:2000]
    refs = event.cve or event.mitre_id

    def _write(database: LazyOwnDB) -> None:
        workspace = database.default_workspace(workspace_name)
        host_id = database.host_add(workspace, host, hostname=host)
        database.vuln_add(
            host_id,
            name,
            severity=severity,
            description=description,
            refs=refs,
        )

    return submit_write(_write)
