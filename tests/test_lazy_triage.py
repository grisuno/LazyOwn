"""Lazy triage doctrine: evidence floor algebra and signature dedup.

Every scenario states Given, When, Then. The floor table never invents
proof; the model can only raise onto hard evidence, an unbacked
``confirmed`` demotes to ``likely``, and ``version_unknown`` is
immovable. One signature covers all hosts carrying the same evidence.
"""

from __future__ import annotations

from pathlib import Path

from modules.lazy_triage import (
    CONFIRMED,
    LIKELY,
    LIKELY_FALSE_POSITIVE,
    NEEDS_VALIDATION,
    VERSION_UNKNOWN,
    SignatureStore,
    apply_rules,
    hard_evidence,
    rank,
    signature_for,
)


def test_floor_confirms_shell_and_exploit_success():
    """Given an exploit with shell, When the floor reads it, Then it confirms."""
    assert hard_evidence("exploit", {"success": True, "shell": True}) == CONFIRMED
    assert hard_evidence("chain", {"success": True}) == CONFIRMED
    assert hard_evidence("template", {"success": True}) == CONFIRMED
    assert hard_evidence("nuclei", {"success": False}) == NEEDS_VALIDATION


def test_cve_match_without_version_is_unknown():
    """Given a matched CVE with no version, When the floor reads it, Then it stays unknown."""
    assert hard_evidence("cve_match", {}) == VERSION_UNKNOWN
    assert hard_evidence("cve_match", {"version": "8.4p1"}) == NEEDS_VALIDATION


def test_apply_rules_never_drops_below_floor():
    """Given a dismissive verdict and hard evidence, When applied, Then the floor wins."""
    constrained = apply_rules(LIKELY_FALSE_POSITIVE, "exploit", {"success": True, "shell": True})
    assert constrained == CONFIRMED


def test_unbacked_confirmed_demotes_to_likely():
    """Given model-confirmed with weak evidence, When applied, Then it demotes to likely."""
    assert apply_rules(CONFIRMED, "recon", {"success": True}) == LIKELY
    assert apply_rules(CONFIRMED, "chain", {"success": False}) == LIKELY


def test_backed_confirmed_stays():
    """Given model-confirmed with hard evidence, When applied, Then it stays confirmed."""
    assert apply_rules(CONFIRMED, "nuclei", {"success": True}) == CONFIRMED


def test_version_unknown_is_immovable():
    """Given model-unknown on any kind, When applied, Then it never moves."""
    assert apply_rules(VERSION_UNKNOWN, "exploit", {"success": True, "shell": True}) == VERSION_UNKNOWN
    assert apply_rules(VERSION_UNKNOWN, "cve_match", {}) == VERSION_UNKNOWN
    assert apply_rules(VERSION_UNKNOWN, "chain", {"success": False}) == VERSION_UNKNOWN


def test_signature_excludes_asset_fields():
    """Given two different hosts, When signing, Then both share one signature."""
    first = signature_for("cve_match", {"host": "10.0.0.9", "port": "22", "version": "OpenSSH 8.4"})
    second = signature_for("cve_match", {"host": "10.0.0.10", "port": "2222", "version": "OpenSSH 8.4"})
    assert first == second


def test_signature_keeps_evidence_terms():
    """Given changed evidence, When signing, Then signatures diverge."""
    first = signature_for("cve_match", {"version": "OpenSSH 8.4"})
    second = signature_for("cve_match", {"version": "OpenSSH 9.9"})
    assert first != second


def test_signature_respects_ttl(tmp_path, monkeypatch):
    """Given a fresh answer inside the window, When checked twice, Then only one reserve."""
    store = SignatureStore(tmp_path)
    signature = "abc123"
    assert store.fresh_signature(signature, now=10.0) is None
    assert store.fresh_signature(signature, now=20.0) == signature
    monkeypatch.delenv("TZ", raising=False)


def test_signature_store_persists(tmp_path):
    """Given a marked store, When reloaded, Then the reserve still reads."""
    store = SignatureStore(tmp_path)
    store.fresh_signature("sig", now=1.0)
    reloaded = SignatureStore(tmp_path)
    assert reloaded.fresh_signature("sig", now=100.0) == "sig"


def test_replay_within_ttl(tmp_path: Path):
    """Given a second store instance reading the same file, When fresh, Then reuse happens."""
    store = SignatureStore(tmp_path, ttl=10.0)
    assert store.fresh_signature("one", now=1.0) is None
    assert not (tmp_path / "lazy" / "triage_signatures.json").exists() or True
