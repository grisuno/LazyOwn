"""Lazy checks doctrine: version-aware interpretation of read-only retests.

Every scenario states Given, When, Then. Observed versions re-read
through the stored OSV range flip the verdict between ``reaffirmed``
and ``version_changed``; a check that never reproduces stays
``inconclusive`` and never lowers a hardened finding.
"""

from __future__ import annotations

import json
from pathlib import Path

from modules.lazy_cve_feed import convert_osv_ranges, range_for_cve
from modules.lazy_checks import (
    INCONCLUSIVE,
    REAFFIRMED,
    VERSION_CHANGED,
    extract_cve,
    extract_version,
    interpret_checks,
)

_RANGE = {"type": "ECOSYSTEM", "introduced": "7.0", "fixed": "8.9"}


def test_extract_version_tolerates_patch_tails_and_rejects_ips():
    """Given banner evidence, When extracting, Then patch tails survive and IPs read nothing."""
    assert extract_version("OpenSSH_9.9p1 Ubuntu-3") == "9.9p1"
    assert extract_version("nginx/1.18.0") == "1.18.0"
    assert extract_version("openssl 1.0.2k") == "1.0.2k"
    assert extract_version("probe 10.0.0.9:22 open") == ""
    assert extract_version("nothing here") == ""


def test_extract_cve_uppercases():
    """Given a lowercase cve string, When extracting, Then it normalizes."""
    assert extract_cve("issue cve-2024-10099 matters") == "CVE-2024-10099"
    assert extract_cve("no cve here") == ""


def test_interpret_reaffirms_when_observed_version_in_range():
    """Given observed version inside the range, When interpreting, Then verdict reaffirms."""
    result = interpret_checks(
        [{"kind": "banner_probe", "verdict": "hit", "evidence": "OpenSSH_8.4p1"}],
        cve="CVE-2024-1",
        stored_version="8.4",
        ranges=_RANGE,
    )
    assert result["verdict"] == REAFFIRMED
    assert result["observed_version"] == "8.4p1"


def test_interpret_flags_version_changed():
    """Given observed version beyond the fixed bound, When interpreting, Then verdict flips."""
    result = interpret_checks(
        [{"kind": "banner_probe", "verdict": "hit", "evidence": "OpenSSH_9.9p1 Ubuntu-3"}],
        cve="CVE-2024-1",
        stored_version="8.4",
        ranges=_RANGE,
    )
    assert result["verdict"] == VERSION_CHANGED


def test_interpret_without_version_or_range_stays_inconclusive_on_miss():
    """Given a non-reproducing miss and no range signal, When interpreting, Then no lowering."""
    result = interpret_checks(
        [{"kind": "nmap_sv", "verdict": "miss", "evidence": "host down"}],
        cve="CVE-2024-1",
        stored_version="8.4",
        ranges=_RANGE,
    )
    assert result["verdict"] == INCONCLUSIVE


def test_convert_osv_ranges_and_range_for_cve(tmp_path: Path, monkeypatch):
    """Given an offline OSV cache, When asking the range, Then the first matching entry lands."""
    import modules.lazy_cve_feed as feed

    advisory = {
        "id": "OSV-2024-0001",
        "aliases": ["CVE-2024-1337"],
        "affected": [
            {
                "package": {"name": "openssh"},
                "ranges": [
                    {
                        "type": "ECOSYSTEM",
                        "events": [
                            {"introduced": "7.0"},
                            {"fixed": "8.9"},
                        ],
                    }
                ],
            }
        ],
    }
    monkeypatch.setattr(feed, "_cache_path", lambda name: tmp_path / name, raising=False)
    (tmp_path / "osv_openssh.json").write_text(json.dumps({"vulns": [advisory]}), encoding="utf-8")
    ranges = convert_osv_ranges(advisory["affected"][0])
    assert ranges == [{"type": "ECOSYSTEM", "introduced": "7.0", "fixed": "8.9", "lastAffected": ""}]
    assert range_for_cve("CVE-2024-1337", allow_network=False) == ranges[0]
    assert range_for_cve("CVE-0000-0000", allow_network=False) == {}
