"""Tests for modules/detection_feed.py."""
from __future__ import annotations

import json

from modules.detection_feed import (
    _CATEGORY_MAP,
    _DEFAULT_PROBABILITY,
    DetectionFeed,
)


class TestDetectionFeedInit:
    def test_default_init(self, tmp_path):
        feed = DetectionFeed(cache_dir=tmp_path)
        assert feed._cache_dir == tmp_path
        assert "sigmahq" in feed._sources

    def test_custom_sources(self, tmp_path):
        sources = {"custom": "https://example.com/rules"}
        feed = DetectionFeed(cache_dir=tmp_path, sources=sources)
        assert "custom" in feed._sources
        assert "sigmahq" not in feed._sources


class TestSigmaParsing:
    def test_extract_log_source(self, tmp_path):
        feed = DetectionFeed(cache_dir=tmp_path)
        doc = {"logsource": {"product": "windows", "service": "security"}}
        assert feed._extract_log_source(doc) == "windows/security"

    def test_extract_log_source_minimal(self, tmp_path):
        feed = DetectionFeed(cache_dir=tmp_path)
        doc = {"logsource": {"product": "linux"}}
        assert feed._extract_log_source(doc) == "linux"

    def test_extract_mitre(self, tmp_path):
        feed = DetectionFeed(cache_dir=tmp_path)
        doc = {"tags": ["attack.t1059", "T1059.001"]}
        assert feed._extract_mitre(doc) == "T1059.001"

    def test_extract_mitre_none(self, tmp_path):
        feed = DetectionFeed(cache_dir=tmp_path)
        doc = {"tags": ["attack.t1059"]}
        assert feed._extract_mitre(doc) == "T0000"

    def test_extract_keywords(self, tmp_path):
        feed = DetectionFeed(cache_dir=tmp_path)
        doc = {
            "detection": {
                "selection": {
                    "CommandLine|contains": ["mimikatz", "sekurlsa"],
                },
            },
        }
        keywords = feed._extract_keywords(doc)
        assert "mimikatz" in keywords
        assert "sekurlsa" in keywords

    def test_extract_categories(self, tmp_path):
        feed = DetectionFeed(cache_dir=tmp_path)
        doc = {"tags": ["attack.credential_access", "attack.t1003"]}
        cats = feed._extract_categories(doc)
        assert "credential" in cats


class TestCaching:
    def test_cache_and_load(self, tmp_path):
        from modules.detection_oracle import SigmaRule
        feed = DetectionFeed(cache_dir=tmp_path)
        rules = [
            SigmaRule(
                rule_id="TEST-001",
                name="Test Rule",
                log_source="windows/security",
                mitre_technique="T1003",
                base_probability=0.8,
                keywords=("mimikatz", "sekurlsa"),
                category_tags=("credential",),
            ),
        ]
        feed._cache_rules(rules, "test_source")
        loaded = feed.load_cached_rules("test_source")
        assert len(loaded) == 1
        assert loaded[0].rule_id == "TEST-001"
        assert loaded[0].name == "Test Rule"

    def test_load_cached_missing(self, tmp_path):
        feed = DetectionFeed(cache_dir=tmp_path)
        loaded = feed.load_cached_rules("nonexistent")
        assert len(loaded) == 0


class TestFeedbackAdjustment:
    def test_adjust_from_feedback_no_file(self, tmp_path):
        feed = DetectionFeed(cache_dir=tmp_path)
        result = feed.adjust_from_feedback(tmp_path / "nonexistent.jsonl")
        assert result == 0

    def test_adjust_from_feedback(self, tmp_path):
        fb_file = tmp_path / "feedback.jsonl"
        fb_file.write_text(json.dumps({
            "rule_id": "LAZ-001",
            "detected": True,
            "actual": True,
        }) + "\n")
        feed = DetectionFeed(cache_dir=tmp_path)
        result = feed.adjust_from_feedback(fb_file)
        assert result == 1


class TestCategoryMap:
    def test_category_mappings(self):
        assert _CATEGORY_MAP["credential_access"] == "credential"
        assert _CATEGORY_MAP["lateral_movement"] == "lateral"
        assert _CATEGORY_MAP["privilege_escalation"] == "privesc"
        assert _CATEGORY_MAP["execution"] == "exploit"
        assert _CATEGORY_MAP["collection"] == "exfil"

    def test_default_probability(self):
        assert _DEFAULT_PROBABILITY == 0.50
