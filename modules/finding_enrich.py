"""Idempotent enrichment of a finding's evidence before it is reported.

A finding accrues traffic evidences one bind at a time, in whatever order the
loop happened to prove them: duplicates creep in when the same exchange is
bound twice, and the strongest proof can sit below weaker supporting rows. This
module canonicalises that set once, deterministically, so a report always shows
the proof first and never twice.

The pass is pure and idempotent: it ranks evidences by role, collapses repeated
digests onto their strongest role, and derives a content-only enrichment digest
from the result. Running it again over an already-enriched finding yields the
same ordering and the same digest, so it is safe to call on every bind without
ever compounding. Nothing here imports the loop runtime, keeping it cycle-free
and testable in isolation.
"""

from __future__ import annotations

import hashlib
from typing import Any

_ROLE_RANK = {
    "proof": 0,
    "verification": 1,
    "baseline": 2,
    "supporting": 3,
    "response": 3,
    "request": 3,
}
_WEAKEST_RANK = max(_ROLE_RANK.values()) + 1
_ENRICH_DIGEST_WIDTH = 16


def _role_rank(role: str) -> int:
    """Return the sort rank of an evidence role, weakest for the unknown."""
    return _ROLE_RANK.get(str(role or "").lower(), _WEAKEST_RANK)


def _stronger(left: str, right: str) -> str:
    """Return the stronger of two roles for duplicate-digest collapsing."""
    return left if _role_rank(left) <= _role_rank(right) else right


def enrich_refs(refs: list[dict[str, Any]]) -> dict[str, Any]:
    """Canonicalise evidence refs into a stable, deduplicated ordering.

    Duplicate digests are collapsed onto their strongest role, then every
    surviving ref is ordered by role strength with the digest as a stable
    tie-break, so the same inputs in any order produce one identical result.

    Args:
        refs: Evidence refs as stored on a finding, each carrying at least a
            ``digest`` and optionally ``role``, ``note`` and ``ts``.

    Returns:
        A result dict with the canonical ``refs`` list, the ``digest`` of that
        canonical form, a ``count`` of distinct evidences and ``roles``, a
        role-to-count tally.
    """
    collapsed: dict[str, dict[str, Any]] = {}
    for ref in refs or []:
        if not isinstance(ref, dict):
            continue
        digest = str(ref.get("digest", "")).strip()
        if not digest:
            continue
        role = str(ref.get("role", "supporting") or "supporting").lower()
        note = str(ref.get("note", ""))[:300]
        ts = float(ref.get("ts", 0.0) or 0.0)
        existing = collapsed.get(digest)
        if existing is None:
            collapsed[digest] = {"digest": digest, "role": role, "note": note, "ts": ts}
            continue
        existing["role"] = _stronger(existing["role"], role)
        if not existing["note"] and note:
            existing["note"] = note
        existing["ts"] = min(existing["ts"], ts) if existing["ts"] and ts else (existing["ts"] or ts)
    ordered = sorted(collapsed.values(), key=lambda r: (_role_rank(r["role"]), r["digest"]))
    roles: dict[str, int] = {}
    for ref in ordered:
        roles[ref["role"]] = roles.get(ref["role"], 0) + 1
    return {
        "refs": ordered,
        "digest": _enrichment_digest(ordered),
        "count": len(ordered),
        "roles": roles,
    }


def _enrichment_digest(ordered: list[dict[str, Any]]) -> str:
    """Return a content-only digest of the canonical refs for idempotency."""
    material = "|".join(f"{r['digest']}:{r['role']}" for r in ordered)
    return hashlib.sha256(material.encode("utf-8", errors="replace")).hexdigest()[:_ENRICH_DIGEST_WIDTH]


def enrich_finding(traffic_log: Any, finding_id: int, graph: Any) -> dict[str, Any]:
    """Enrich one finding's stored evidence in place, idempotently.

    The finding's evidence refs are canonicalised and written back only when
    the enrichment digest changes, so a finding already in canonical form is
    never rewritten and its ``evidence_version`` never churns.

    Args:
        traffic_log: The :class:`~modules.lazy_loop.TrafficLog` owning the refs.
        finding_id: The finding node id to enrich.
        graph: The exploration graph holding the finding.

    Returns:
        A result dict with ``ok``, and either the enrichment summary (``digest``,
        ``count``, ``roles``, ``changed``) or an ``error``.
    """
    if graph is None:
        return {"ok": False, "error": "no graph"}
    node = graph.get(int(finding_id))
    if node is None or getattr(node, "kind", "") != "finding":
        return {"ok": False, "error": f"unknown finding: {finding_id}"}
    current = node.meta.get("traffic_refs", [])
    normalized = traffic_log._normalize_refs(current)
    result = enrich_refs(normalized)
    before_order = [(r.get("digest"), r.get("role")) for r in normalized]
    after_order = [(r["digest"], r["role"]) for r in result["refs"]]
    refs_changed = before_order != after_order
    before_full = [(r.get("digest"), r.get("role"), r.get("note", "")) for r in normalized]
    after_full = [(r["digest"], r["role"], r["note"]) for r in result["refs"]]
    meta_changed = before_full != after_full
    marker_stale = str(node.meta.get("enrichment_digest", "")) != result["digest"]
    if refs_changed or meta_changed:
        node.meta["traffic_refs"] = result["refs"]
    if refs_changed or meta_changed or marker_stale:
        node.meta["enrichment_digest"] = result["digest"]
        if refs_changed:
            node.meta["evidence_version"] = int(node.meta.get("evidence_version", 1)) + 1
        graph._persist()
    return {
        "ok": True,
        "digest": result["digest"],
        "count": result["count"],
        "roles": result["roles"],
        "changed": refs_changed,
    }


__all__ = ["enrich_finding", "enrich_refs"]
