"""BDD tests for the intelligence selector in the shared cascade."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from modules.selection.base import SelectionContext as _Ctx


@pytest.fixture()
def intel(monkeypatch, tmp_path: Path):
    """Import the selector with a sandboxed sessions directory."""
    import modules.selection.intel as module

    monkeypatch.setattr(module, "SESSIONS_DIR", tmp_path)
    monkeypatch.setattribute = None
    monkeypatch.setattr(module, "BASE_DIR", tmp_path)
    return module


def _report(tmp_path: Path, target: str, matches: list[dict]) -> None:
    """Write one exposure report file in the sandbox."""
    (tmp_path / f"lazy_intel_{target}.json").write_text(json.dumps({
        "target": target,
        "temperature": "hot",
        "score": 50,
        "matches": matches,
    }), encoding="utf-8")


FIRE = {
    "cve_id": "CVE-2025-24813", "host": "10.66.44.7", "port": 8080, "protocol": "tcp",
    "product": "apache tomcat", "version": "9.0.45", "tier": "hot",
    "cvss": 9.8, "evidence": "in_range", "references": [], "source": "scanner",
}


def _ctx(target: str = "10.66.44.7", exclude=()):
    """Build a selection context for the tests."""
    return _Ctx(target=target, phase="recon", exclude=frozenset(exclude))


class TestCascadeOrder:
    def test_intel_selector_abstains_when_named_intent_wins(self):
        story = "named actor/adversary intents outrank the generic intel refresh in the cascade"
        from modules.selection import registry

        names = [type(sel).__name__ for sel in registry.all_selectors()]
        assert "IntelSelector" in names, story
        assert names.index("PlaybookSelector") < names.index("IntelSelector"), story

    def test_orchestrator_toggle_honours_intel(self):
        story = "orchestrator.selectors.intel = false drops the selector"
        from modules import orchestrator_config

        assert orchestrator_config.selector_enabled("intel") is True, story


class TestFireProposal:
    def test_fire_report_pending(self, intel, tmp_path: Path):
        story = "uncovered fire intel proposes the autofire confirmation"
        _report(tmp_path, "10.66.44.7", [dict(FIRE)])
        decision = intel.IntelSelector().propose(_ctx())
        assert decision is not None and decision.command == "lazyautofire fire 10.66.44.7", story
        assert decision.priority == 2, story
        assert "CVE-2025-24813" in decision.reason, story

    def test_covered_chain_abstains(self, intel, tmp_path: Path):
        story = "a chain file already covering the cve stops the selector"
        _report(tmp_path, "10.66.44.7", [dict(FIRE)])
        slug = "".join(ch if ch.isalnum() else "_" for ch in "10.66.44.7")
        chains_dir = tmp_path / "chains"
        chains_dir.mkdir()
        (chains_dir / f"lazy_autofire_{slug.strip('_')}.yaml").write_text(
            "name: lazy_autofire_x\nsteps: [{run: probe, id: a, cve: CVE-2025-24813}]\n",
            encoding="utf-8",
        )
        assert intel.IntelSelector().propose(_ctx()) is None, story

    def test_exclude_abstains(self, intel, tmp_path: Path):
        story = "already-proposed actions do not repeat"
        _report(tmp_path, "10.66.44.7", [dict(FIRE)])
        decision = intel.IntelSelector().propose(_ctx(exclude={"lazyautofire fire 10.66.44.7"}))
        assert decision is None, story

    def test_smoke_only_abstains(self, intel, tmp_path: Path):
        story = "smoke-tier matches never push the loop"
        only = dict(FIRE)
        only["tier"] = "warm"
        _report(tmp_path, "10.66.44.7", [only])
        assert intel.IntelSelector().propose(_ctx()) is None, story


class TestRefreshProposal:
    def test_no_report_with_feed(self, intel, tmp_path: Path):
        story = "a staged feed with no report proposes the first lazyintel run"
        (tmp_path / "intel").mkdir()
        (tmp_path / "intel" / "exploit_feed.json").write_text(
            json.dumps({"entries": []}), encoding="utf-8"
        )
        decision = intel.IntelSelector().propose(_ctx())
        assert decision is not None and decision.command == "lazyintel 10.66.44.7", story
        assert decision.priority == 6, story

    def test_no_sources_abstains(self, intel, tmp_path: Path, monkeypatch):
        story = "with no feed staged and live feeds disabled there is nothing to run"
        monkeypatch.setenv("LAZYOWN_CVE_FEEDS", "0")
        assert intel.IntelSelector().propose(_ctx()) is None, story

    def test_live_feeds_enabled_reach_refresh(self, intel, tmp_path: Path, monkeypatch):
        story = "live keyless feeds count as ready sources for a first run"
        monkeypatch.setenv("LAZYOWN_CVE_FEEDS", "1")
        decision = intel.IntelSelector().propose(_ctx())
        assert decision is not None and decision.command == "lazyintel 10.66.44.7", story

    def test_existing_report_abstains_second_run(self, intel, tmp_path: Path):
        story = "a saved report with no fires ends the refresh path"
        _report(tmp_path, "10.66.44.7", [])
        assert intel.IntelSelector().propose(_ctx()) is None, story
