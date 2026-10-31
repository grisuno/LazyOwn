"""BDD tests for the lazy_autofire intelligence-to-chain closure."""

from __future__ import annotations

import json
from pathlib import Path

import yaml

from modules import lazy_autofire


def _clean_report(*cves: tuple[str, int, str], tier: str = "hot") -> dict:
    """Clean report builder without comprehension contortions."""
    matches = [
        {
            "cve_id": cve_id, "host": "10.66.44.7", "port": port, "protocol": "tcp",
            "product": product, "version": "1.0", "tier": tier,
            "cvss": 9.8, "evidence": "in_range", "references": [], "source": "scanner",
        }
        for cve_id, port, product in cves
    ]
    return {
        "target": "10.66.44.7",
        "temperature": tier,
        "score": 50,
        "matches": matches,
        "version_unknown": [],
        "leads": [],
        "checks": [],
        "notes": [],
        "score_detail": [],
    }


class TestConsiderReport:
    def test_unarmed_proposes(self, tmp_path):
        story = "without arming, the chain data is a proposal and nothing is written"
        result = lazy_autofire.consider_report(
            _clean_report(("CVE-2025-1001", 8080, "tomcat"), ("CVE-2025-1002", 8081, "tomcat")),
            chains_dir=tmp_path, now=1000.0,
        )
        assert result["action"] == "proposed", story
        assert result["path"] is None, story
        assert result["chain"]["name"].startswith("lazy_autofire_"), story
        assert not list(tmp_path.rglob("*.yaml")), story

    def test_armed_writes_validated_chain(self, tmp_path):
        story = "armed autofire writes the chain through the real validator"
        result = lazy_autofire.consider_report(
            _clean_report(("CVE-2025-1001", 8080, "tomcat")),
            chains_dir=tmp_path, state_path=tmp_path / "state.json", armed=True, now=1000.0,
        )
        assert result["action"] == "generated", story
        data = yaml.safe_load(Path(result["path"]).read_text(encoding="utf-8"))
        assert data["name"], story
        probe = next(step for step in data["steps"] if step["id"].startswith("probe_"))
        assert "nmap -Pn" in probe["run"], story
        assert probe.get("verify") == "tomcat", story
        closes = data["steps"][-1]["run"].startswith("lazyintel"), story

    def test_step_cap(self, tmp_path):
        story = "at most MAX_FIRE_STEPS probe steps are generated"
        triple = _clean_report(("CVE-2025-9001", 1, "a"), ("CVE-2025-9002", 2, "b"),
                               ("CVE-2025-9003", 3, "c"), ("CVE-2025-9004", 4, "d"))
        result = lazy_autofire.consider_report(triple, chains_dir=tmp_path, state_path=tmp_path / "state.json", armed=True, now=1000.0)
        data = yaml.safe_load(Path(result["path"]).read_text(encoding="utf-8"))
        probes = [step for step in data["steps"] if step["id"].startswith("probe_")]
        assert len(probes) == lazy_autofire.MAX_FIRE_STEPS, story
        assert result["cves"] == ["CVE-2025-9001", "CVE-2025-9002", "CVE-2025-9003"], story

    def test_smoke_tier_never_fires(self, tmp_path):
        story = "smoke matches generate nothing"
        result = lazy_autofire.consider_report(
            _clean_report(("CVE-2025-1001", 8080, "tomcat"), tier="warm"),
            chains_dir=tmp_path, state_path=tmp_path / "state.json", armed=True, now=1000.0,
        )
        assert result["action"] == "skipped", story
        assert "no fire-tier" in result["reason"], story

    def test_cooldown_blocks_regeneration(self, tmp_path):
        story = "a generated cve cools down before a second chain may exist"
        report = _clean_report(("CVE-2025-1001", 8080, "tomcat"))
        lazy_autofire.consider_report(report, chains_dir=tmp_path, state_path=tmp_path / "state.json", armed=True, now=1000.0)
        second = lazy_autofire.consider_report(report, chains_dir=tmp_path, state_path=tmp_path / "state.json", armed=True, now=1100.0)
        assert second["action"] == "skipped", story
        later = lazy_autofire.consider_report(report, chains_dir=tmp_path, state_path=tmp_path / "state.json", armed=True, now=1000.0 + lazy_autofire.COOLDOWN_SECONDS + 1)
        assert later["action"] == "skipped" and "already covered" in later["reason"], story

    def test_state_persisted(self, tmp_path):
        story = "the cooldown state survives a reload"
        report = _clean_report(("CVE-2025-1001", 8080, "tomcat"))
        lazy_autofire.consider_report(report, chains_dir=tmp_path, state_path=tmp_path / "state.json", armed=True, now=1000.0)
        data = json.loads((tmp_path / "state.json").read_text(encoding="utf-8"))
        assert any("CVE-2025-1001" in key for key in data["cooldown"]), story


class TestHelpers:
    def test_autofire_armed_contract(self):
        story = "arming requires an explicit true"
        assert lazy_autofire.autofire_armed({"autofire": True}) is True, story
        assert lazy_autofire.autofire_armed({"autofire": "true"}) is False, story
        assert lazy_autofire.autofire_armed({}) is False, story

    def test_status_surface(self, tmp_path):
        story = "status sums the cooldown entries"
        report = _clean_report(("CVE-2025-1001", 8080, "tomcat"))
        lazy_autofire.consider_report(report, chains_dir=tmp_path, state_path=tmp_path / "state.json", armed=True, now=1000.0)
        view = lazy_autofire.status({"autofire": True}, state_path=tmp_path / "state.json")
        assert view["armed"] is True and view["cooldown"] == 1, story

    def test_sweep_prunes_expired(self, tmp_path):
        story = "sweep drops expired entries and keeps fresh ones"
        report = _clean_report(("CVE-2025-1001", 8080, "tomcat"))
        lazy_autofire.consider_report(report, chains_dir=tmp_path, state_path=tmp_path / "state.json", armed=True, now=1000.0)
        pruned = lazy_autofire.sweep_state(tmp_path / "state.json", now=1000.0 + lazy_autofire.COOLDOWN_SECONDS)
        assert pruned == 1, story

    def test_fire_from_missing_report(self, tmp_path):
        story = "a missing saved report skips loudly"
        result = lazy_autofire.fire_from_file("nope-host", chains_dir=tmp_path)
        assert result["action"] == "skipped" and "no saved report" in result["reason"], story
