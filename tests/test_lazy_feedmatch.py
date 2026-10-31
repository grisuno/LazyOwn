"""BDD tests for the lazy feed schema and hard-evidence version matching."""

from __future__ import annotations

import json

import pytest

from modules import lazy_feedmatch
from modules.lazy_feedmatch import (
    EVIDENCE_IN_RANGE,
    EVIDENCE_UNBOUNDED,
    FeedEntry,
    Sighting,
    bind_sighting,
    is_os_sighting,
    load_feed,
    parse_feed,
    parse_version,
    product_token,
    unversioned_leads,
    version_in_ranges,
)
from modules.lazy_heat import compare_versions

FEED_ROWS = [
    {
        "cve_id": "CVE-2025-1001",
        "product": "apache tomcat",
        "cvss": 9.8,
        "kev": True,
        "ranges": [{"introduced": "10.0.0", "fixed": "10.0.20"}],
    },
    {
        "cve_id": "CVE-2025-1002",
        "product": "openssh",
        "cvss": 7.5,
        "public_exploit": True,
        "ranges": [{"introduced": "8.0", "last_affected": "9.9.1"}],
    },
    {
        "cve_id": "CVE-2025-1003",
        "product": "redis",
        "kev": True,
    },
]


class TestParseVersion:
    def test_plain_numbers(self):
        story = "numeric dotted versions parse and compare correctly"
        assert parse_version("1.2.3") < parse_version("1.2.10"), story

    def test_ignored_epoch(self):
        story = "an epoch prefix is stripped so upstream bounds keep applying"
        assert parse_version("1:9.6p1") == parse_version("9.6"), story

    def test_pre_release_ordering(self):
        story = "a pre-release sorts before its final release"
        assert compare_versions(parse_version("2.0-beta9"), parse_version("2.0")) < 0, story

    def test_garbage_returns_none(self):
        story = "no digits yields nothing to compare"
        assert parse_version("banana") is None, story
        assert parse_version("") is None, story


class TestProductTokens:
    def test_os_sightings_never_match(self):
        story = "operating system fingerprints are rejected by the binding policy, not by tokens"
        assert is_os_sighting("Ubuntu Linux"), story
        assert is_os_sighting("Windows Server 2019"), story
        feed = parse_feed([{"cve_id": "CVE-2025-7777", "product": "windows", "kev": True}])
        assert bind_sighting(Sighting(host="t", port=1, product="Windows Server 2019", version="10"), feed) == [], story

    def test_generic_filler_never_binds(self):
        story = "scanner filler labels produce no advisory binding"
        assert product_token("tcpwrapped") == "tcpwrapped", story
        feed = parse_feed([{"cve_id": "CVE-2025-7778", "product": "tcpwrapped", "kev": True}])
        assert bind_sighting(Sighting(host="t", port=1, product="tcpwrapped", version="0.1"), feed) == [], story

    def test_version_suffix_split(self):
        story = "product plus version naming still resolves to the base token"
        assert product_token("openssl 3.0.2") == "openssl", story

    def test_http_daemon_words_stripped(self):
        story = "daemon and server words are stripped so a cve naming the product matches"
        assert product_token("OpenSSH server") == "openssh", story


class TestRanges:
    def test_in_range(self):
        story = "a version inside a bounded range is affected"
        ranges = [{"introduced": "10.0.0", "fixed": "10.0.20"}]
        assert version_in_ranges(parse_version("10.0.2"), ranges) is True, story

    def test_fixed_bound_excludes(self):
        story = "the fixed version itself is not affected"
        ranges = [{"introduced": "10.0.0", "fixed": "10.0.20"}]
        assert version_in_ranges(parse_version("10.0.20"), ranges) is False, story

    def test_unbounded_is_none(self):
        story = "no bounded keys means the version cannot be tested"
        assert version_in_ranges(parse_version("10.0.2"), []) is None, story


class TestBindSighting:
    @pytest.fixture()
    def feed(self):
        return parse_feed(FEED_ROWS)

    def test_hard_evidence_in_range(self, feed):
        story = "tomcat 10.0.2 binds with in-range evidence and fire heat"
        result = bind_sighting(Sighting(host="t", port=8080, product="tomcat", version="10.0.2"), feed)
        assert [b.evidence for b in result] == [EVIDENCE_IN_RANGE], story
        assert result[0].tier == "hot", story
        assert result[0].cve_id == "CVE-2025-1001", story

    def test_fixed_version_not_affected(self, feed):
        story = "tomcat 10.0.20 produces no match"
        result = bind_sighting(Sighting(host="t", port=8080, product="tomcat", version="10.0.20"), feed)
        assert result == [], story

    def test_unbounded_kev_review(self, feed):
        story = "an unbounded kev advisory stays a review candidate, never affected"
        result = bind_sighting(Sighting(host="t", port=6379, product="redis", version="7.4.1"), feed)
        assert len(result) == 1, story
        assert result[0].evidence == EVIDENCE_UNBOUNDED, story
        assert result[0].tier == "cold", story

    def test_name_only_never_binds(self, feed):
        story = "a product without a version binds nothing, regardless of heat"
        result = bind_sighting(Sighting(host="t", port=22, product="openssh", version=""), feed)
        assert result == [], story

    def test_out_of_range_version_binds_nothing(self, feed):
        story = "a version past every bound of its advisory is not affected"
        result = bind_sighting(Sighting(host="t", port=22, product="openssh", version="10.9.9"), feed)
        assert result == [], story

    def test_unversioned_leads(self, feed):
        story = "products without versions come back as leads, and a product versioned elsewhere is dropped"
        rows = [
            Sighting(host="t", port=80, product="nginx", version=""),
            Sighting(host="t", port=5432, product="postgresql", version=""),
            Sighting(host="t", port=443, product="nginx", version="1.27.0"),
        ]
        leads = unversioned_leads(rows)
        assert [lead.product for lead in leads] == ["postgresql"], story


class TestLoadFeed:
    def test_lazy_schema(self, tmp_path):
        story = "entries under the lazy schema load verbatim"
        path = tmp_path / "exploit_feed.json"
        path.write_text(json.dumps({"entries": FEED_ROWS}), encoding="utf-8")
        rows = load_feed(path)
        assert [row["cve_id"] for row in rows] == ["CVE-2025-1001", "CVE-2025-1002", "CVE-2025-1003"], story

    def test_kev_dump_mapping(self, tmp_path):
        story = "a cisa KEV dump maps vendored product rows onto the schema"
        path = tmp_path / "kev.json"
        path.write_text(json.dumps({"vulnerabilities": [
            {"cveID": "CVE-2025-7775", "vendorProject": "F5", "product": "BIG-IP", "cisaExploitAdd": "2025-08-01"}
        ]}), encoding="utf-8")
        rows = load_feed(path)
        assert rows[0]["cve_id"] == "CVE-2025-7775" and rows[0]["kev"] is True, story
        assert rows[0]["product"], story

    def test_missing_file_is_silent(self, tmp_path):
        story = "a missing feed degrades to an empty row list"
        assert load_feed(tmp_path / "nope.json") == [], story

    def test_parse_feed_drops_malformed(self):
        story = "rows without a name or product are dropped and deduped"
        feed = parse_feed([{"cve_id": "x", "product": ""}, *FEED_ROWS, FEED_ROWS[0]])
        assert len(feed) == 3, story
        assert isinstance(feed[0], FeedEntry), story


class TestLiveBindings:
    def test_live_bindings_offline_contract(self):
        story = "with feeds gated off, the live path stays safe and never raises"
        import os

        old = os.environ.get("LAZYOWN_CVE_FEEDS")
        os.environ["LAZYOWN_CVE_FEEDS"] = "0"
        try:
            binding = lazy_feedmatch.live_bindings(
                lazy_feedmatch.Sighting(host="10.66.44.9", port=22, product="openssh", version="9.6p1"),
                allow_network=False,
            )
        finally:
            if old is None:
                os.environ.pop("LAZYOWN_CVE_FEEDS", None)
            else:
                os.environ["LAZYOWN_CVE_FEEDS"] = old
        assert isinstance(binding, list), story
        assert all(item.evidence in (lazy_feedmatch.EVIDENCE_IN_RANGE, lazy_feedmatch.EVIDENCE_UNBOUNDED) for item in binding), story

    def test_live_bindings_source_passthrough(self):
        story = "live bindings keep the sighting source (scanner vs host)"
        import os

        old = os.environ.get("LAZYOWN_CVE_FEEDS")
        os.environ["LAZYOWN_CVE_FEEDS"] = "0"
        try:
            binding = lazy_feedmatch.live_bindings(
                lazy_feedmatch.Sighting(host="10.66.44.9", port=0, product="openssh", version="9.6p1", source="host"),
                allow_network=False,
            )
        finally:
            if old is None:
                os.environ.pop("LAZYOWN_CVE_FEEDS", None)
            else:
                os.environ["LAZYOWN_CVE_FEEDS"] = old
        assert all(item.source == "host" for item in binding), story
