"""Tests for idempotent enrichment of a finding's evidence.

Enrichment must collapse duplicate digests onto their strongest role, order
evidences proof-first with a stable tie-break, and derive a content-only digest
so a second pass over an already-canonical finding changes nothing and never
churns the evidence version.
"""

from __future__ import annotations

import types

from modules import finding_enrich
from modules.lazy_loop import TrafficLog


def _ref(digest, role="supporting", note="", ts=1.0):
    return {"digest": digest, "role": role, "note": note, "ts": ts}


def test_enrich_orders_proof_first():
    result = finding_enrich.enrich_refs([_ref("b", "supporting"), _ref("a", "proof")])
    assert [r["digest"] for r in result["refs"]] == ["a", "b"]
    assert result["refs"][0]["role"] == "proof"


def test_enrich_collapses_duplicate_onto_strongest_role():
    result = finding_enrich.enrich_refs([_ref("a", "supporting"), _ref("a", "proof")])
    assert result["count"] == 1
    assert result["refs"][0]["role"] == "proof"


def test_enrich_is_order_independent():
    first = finding_enrich.enrich_refs([_ref("a", "proof"), _ref("b", "baseline")])
    second = finding_enrich.enrich_refs([_ref("b", "baseline"), _ref("a", "proof")])
    assert first["digest"] == second["digest"]
    assert [r["digest"] for r in first["refs"]] == [r["digest"] for r in second["refs"]]


def test_enrich_digest_is_stable_and_sized():
    result = finding_enrich.enrich_refs([_ref("a", "proof")])
    assert len(result["digest"]) == 16
    assert finding_enrich.enrich_refs(result["refs"])["digest"] == result["digest"]


def test_enrich_ignores_empty_and_malformed():
    result = finding_enrich.enrich_refs([_ref(""), "legacy", {"role": "proof"}, _ref("a")])
    assert result["count"] == 1 and result["refs"][0]["digest"] == "a"


def test_enrich_empty_input():
    result = finding_enrich.enrich_refs([])
    assert result["count"] == 0 and result["refs"] == [] and result["digest"]


def _graph_with(meta):
    finding = types.SimpleNamespace(kind="finding", meta=meta)
    persisted = {"n": 0}

    def _persist():
        persisted["n"] += 1

    graph = types.SimpleNamespace(get=lambda _id: finding, _persist=_persist, _persisted=persisted)
    return graph, finding


def test_enrich_finding_canonicalises_and_bumps_version():
    graph, finding = _graph_with(
        {"traffic_refs": [_ref("b", "supporting"), _ref("a", "proof")], "evidence_version": 1}
    )
    result = finding_enrich.enrich_finding(TrafficLog("t"), 1, graph)
    assert result["ok"] and result["changed"] is True
    assert [r["digest"] for r in finding.meta["traffic_refs"]] == ["a", "b"]
    assert finding.meta["evidence_version"] == 2


def test_enrich_finding_is_idempotent():
    graph, finding = _graph_with({"traffic_refs": [_ref("a", "proof"), _ref("b", "baseline")]})
    traffic = TrafficLog("t")
    finding_enrich.enrich_finding(traffic, 1, graph)
    before = graph._persisted["n"]
    second = finding_enrich.enrich_finding(traffic, 1, graph)
    assert second["changed"] is False
    assert graph._persisted["n"] == before


def test_enrich_finding_unknown():
    graph = types.SimpleNamespace(get=lambda _id: None, _persist=lambda: None)
    assert finding_enrich.enrich_finding(TrafficLog("t"), 9, graph)["ok"] is False
    assert finding_enrich.enrich_finding(TrafficLog("t"), 9, None)["ok"] is False


def test_enrich_finding_preserves_note_through_collapse():
    graph, finding = _graph_with(
        {"traffic_refs": [_ref("a", "proof", note=""), _ref("a", "supporting", note="cred dump confirmed")]}
    )
    result = finding_enrich.enrich_finding(TrafficLog("t"), 1, graph)
    assert result["count"] == 1
    assert finding.meta["traffic_refs"][0]["role"] == "proof"
    assert finding.meta["traffic_refs"][0]["note"] == "cred dump confirmed"
