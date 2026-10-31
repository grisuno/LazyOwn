"""BDD tests for the lazy exposure report engine."""

from __future__ import annotations

import json

from modules import lazy_feedmatch
from modules.lazy_exposure import (
    generate_report,
    probe_checks,
    publish_report,
    save_report,
    score_report,
)

ENTRIES = [
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
        "cvss": 5.0,
        "ranges": [{"last_affected": "9.9.1"}],
    },
    {"cve_id": "CVE-2025-1003", "product": "redis", "kev": True, "cvss": 9.1},
]

SIGHTINGS = [
    {"ip": "10.0.0.9", "state": "scanned", "services": {
        "8080": {"port": 8080, "name": "tomcat", "version": "10.0.2", "protocol": "tcp"},
        "22": {"port": 22, "name": "openssh", "version": "9.9", "protocol": "tcp"},
        "6379": {"port": 6379, "name": "redis", "version": "7.4.1", "protocol": "tcp"},
    }},
]


class TestGenerateReport:
    def test_in_range_matches_ranked(self):
        story = "bounded matches come back ranked hottest first with evidence states"
        report = generate_report("10.0.0.9", ENTRIES, sightings=SIGHTINGS)
        ids = [row["cve_id"] for row in report["matches"]]
        assert ids[0] == "CVE-2025-1001", story
        assert report["matches"][0]["evidence"] == "in_range", story
        assert report["temperature"] == "hot", story

    def test_unbounded_kev_is_review_not_match(self):
        story = "the unbounded kev redis entry lands in the review queue at ice"
        report = generate_report("10.0.0.9", ENTRIES, sightings=SIGHTINGS)
        assert any(row["cve_id"] == "CVE-2025-1003" for row in report["version_unknown"]), story
        assert all(row["cve_id"] != "CVE-2025-1003" for row in report["matches"]), story

    def test_leads_for_unversioned(self):
        from modules.lazy_feedmatch import Sighting

        rows = [Sighting(host="10.0.0.9", port=80, product="nginx", version="")]
        report = generate_report("10.0.0.9", ENTRIES, sightings=rows)
        story = "products without versions never bind, so only leads remain"
        assert report["matches"] == [], story
        assert [lead["product"] for lead in report["leads"]] == ["nginx"], story

    def test_score_breakdown(self):
        story = "the score sums its audited detail lines, the fire match is on the board and it stays within 100"
        report = generate_report("10.0.0.9", ENTRIES, sightings=SIGHTINGS)
        assert report["score"] == sum(item["points"] for item in report["score_detail"]), story
        assert report["score"] <= 100, story
        assert any("CVE-2025-1001" in item["label"] for item in report["score_detail"]), story

    def test_checks_render_for_bounded(self):
        story = "only bounded matches get rendered read-only checks, capped"
        report = generate_report("10.0.0.9", ENTRIES, sightings=SIGHTINGS)
        checks = report["checks"]
        assert checks, story
        assert all(check["cve_id"] != "CVE-2025-1003" for check in checks), story
        assert all("nmap -Pn" in check["command"] for check in checks), story

    def test_feed_fingerprint_recorded(self):
        story = "the report records feed provenance"
        report = generate_report("10.0.0.9", ENTRIES, sightings=SIGHTINGS)
        assert report["feed"], story

    def test_save_report_atomic(self, tmp_path):
        story = "save_report writes the artifact and never leaves a tmp file"
        report = generate_report("10.0.0.9", ENTRIES, sightings=SIGHTINGS)
        out = tmp_path / "lazy_intel_10.0.0.9.json"
        path = save_report(report, out)
        assert path is not None and out.exists(), story
        assert json.loads(out.read_text(encoding="utf-8"))["target"] == "10.0.0.9", story
        assert not list(tmp_path.glob("*.tmp")), story

    def test_save_report_survives_bad_path(self, tmp_path):
        story = "a directory target path degrades to None and never raises"
        report = generate_report("10.0.0.9", ENTRIES, sightings=SIGHTINGS)
        assert save_report(report, tmp_path) is None, story


class TestPublish:
    def test_publish_event(self):
        story = "publish_report fans out one lazy_intel event"
        report = generate_report("10.0.0.9", ENTRIES, sightings=SIGHTINGS)
        report["score"] = 82
        report["temperature"] = "hot"
        results = publish_report(report)
        assert results.get("event_bus") is True, story

    def test_score_report_caps(self):
        story = "unknown review items count at most 2 points and surface is capped at 10"
        entries = [
            {"cve_id": "CVE-2025-1001", "product": "tomcat", "tier": "hot",
             "cvss": 9.8, "evidence": "in_range", "version": "10.0.2", "port": 8080,
             "protocol": "tcp", "host": "t", "references": []},
            {"cve_id": "CVE-2025-9001", "product": "x", "tier": "cold", "cvss": 0, "evidence": "unbounded_kev",
             "version": "1", "port": 1, "protocol": "tcp", "host": "t", "references": []},
        ] * 5
        bounded_unknown = entries[1:6]
        score, detail = score_report(entries[:1], bounded_unknown, services=40)
        assert any(item["points"] == 2 for item in detail), story
        assert any(item["points"] == 10 for item in detail), story
        assert score <= 100, story

    def test_probe_checks_sorted_and_capped(self):
        story = "probe_checks contracts to MAX_CHECKS with ranges from the feed"
        feed = lazy_feedmatch.parse_feed(ENTRIES)
        from modules.lazy_exposure import MAX_CHECKS

        matches = [row for row in generate_report("10.0.0.9", ENTRIES, sightings=SIGHTINGS)["matches"]]
        rendered = probe_checks(matches[: MAX_CHECKS + 2], feed)
        assert len(rendered) <= MAX_CHECKS, story
