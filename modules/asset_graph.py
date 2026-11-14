"""Campaign scope coverage query for the autonomous loop.

The dual-graph asset store that used to live here retired with the
ad-hoc engine: production reads and writes assets through
``modules.lazy_loop.AssetGraph``. What remains is the single
db-backed coverage query consumed by the autonomous daemon.
"""

from __future__ import annotations


def coverage_for(db: object, workspace_id: int, scope: list[str]) -> dict:
    """Report tested scope assets versus total scope from the campaign db.

    The scope is the explicit target list (never inferred). An address
    counts as tested when present in the workspace hosts.

    Args:
        db: Campaign database exposing ``host_list``.
        workspace_id: Workspace whose hosts define the tested set.
        scope: Explicit target addresses (never inferred).

    Returns:
        Mapping with ``scope``, ``total``, ``tested``, ``untested``
        and the tested/total ``ratio``.
    """
    wanted = [str(a).strip().lower() for a in (scope or []) if str(a).strip()]
    try:
        held = {str(h.get("address", "")).lower() for h in db.host_list(int(workspace_id))}
    except Exception:
        held = set()
    tested = sorted(a for a in wanted if a in held)
    total = len(wanted)
    return {"scope": sorted(wanted), "total": total, "tested": tested,
            "untested": sorted(a for a in wanted if a not in held),
            "ratio": (len(tested) / total) if total else 0.0}


__all__ = ["coverage_for"]
