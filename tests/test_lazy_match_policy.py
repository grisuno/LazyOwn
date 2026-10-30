"""Match policy contract: strands, standing and audited closures.

Every scenario states Given, When, Then. Version-bounded evidence is a
match; versionless or unbounded evidence is a lead or capped unknown;
OS sightings stay leads; closures persist their reason and standing
rows survive overwrites.
"""

from __future__ import annotations

from pathlib import Path

from modules.lazy_match_policy import (
    LEAD,
    MATCH,
    UNKNOWN_SCORE_CAP,
    VERSION_UNKNOWN,
    MatchStore,
    has_standing,
    is_os_sighting,
    strand_from_sighting,
)


def test_versioned_range_match():
    """Given a version inside a range, When stranding, Then it is a match."""
    sighting = {"product": "openssh", "version": "8.4", "ranges": {"type": "ECOSYSTEM", "introduced": "7.0", "fixed": "8.9"}}
    assert strand_from_sighting(sighting) == MATCH


def test_out_of_range_versions_stay_leads_not_matches():
    """Given a version past the fixed bound, When stranding, Then it is a lead."""
    sighting = {"product": "openssh", "version": "9.9", "ranges": {"type": "ECOSYSTEM", "introduced": "7.0", "fixed": "8.9"}}
    assert strand_from_sighting(sighting) == LEAD


def test_versionless_and_os_are_leads():
    """Given no version or an OS banner, When stranding, Then nothing claims a version."""
    assert strand_from_sighting({"product": "openssh"}) == LEAD
    assert strand_from_sighting({"product": "Linux telnetd", "version": "3.0"}) == LEAD
    assert is_os_sighting("Linux telnetd", "cpe:/o:linux:linux_kernel") is True


def test_unbounded_kev_is_version_unknown():
    """Given KEV with no bound, When stranding, Then it is a capped unknown."""
    assert strand_from_sighting({"product": "x", "version": "1.0", "kev_nobound": True}) == VERSION_UNKNOWN


def test_store_upgrades_strands_and_dedupes(tmp_path: Path):
    """Given lead then match, When upserting, Then the strand upgrades and sightings grow."""
    store = MatchStore(tmp_path)
    row = store.upsert({"cve": "CVE-1", "product": "ssh", "host": "10.0.0.9"}, {"product": "ssh"})
    assert row["strand"] == LEAD
    row2 = store.upsert(
        {"cve": "CVE-1", "product": "ssh", "host": "10.0.0.9"},
        {"product": "ssh", "version": "8.4", "ranges": {"introduced": "7.0", "fixed": "8.9"}},
    )
    assert row2["strand"] == MATCH
    assert len(store.rows()) == 1
    key = MatchStore._key({"cve": "CVE-1", "product": "ssh", "host": "10.0.0.9"})
    assert store.rows()[key]["strand"] == MATCH


def test_closure_persists_reason(tmp_path: Path):
    """Given a closed row, When queried, Then the reason survives."""
    store = MatchStore(tmp_path)
    store.upsert({"cve": "CVE-2", "product": "smb", "host": "h"}, {"product": "smb"})
    closed = store.close({"cve": "CVE-2", "product": "smb", "host": "h"}, "wrong product appear")
    assert closed["reason"] == "wrong product appear"
    assert store.closed_reason({"cve": "CVE-2", "product": "smb", "host": "h"}) == "wrong product appear"
    assert store.closed_reason({"cve": "CVE-404", "product": "no", "host": "x"}) == ""


def test_standing_blocks_auto_merge():
    """Given a human-touched row, When querying standing, Then it blocks automation."""
    assert has_standing({"timeline": [{"kind": "manual-validation"}]}) is True
    assert has_standing({"evidence": [{"kind": "remediation-claim"}]}) is True
    assert has_standing({"timeline": [{"kind": "sighting"}], "standing": True}) is True
    assert has_standing({"timeline": [{"kind": "sighting"}]}) is False


def test_unknown_score_cap_constant():
    """Given the doctrine, When capping, Then unknowns cost almost nothing."""
    assert UNKNOWN_SCORE_CAP == 2
