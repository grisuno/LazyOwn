"""Tests for the auto_loop phishing fallback wiring in modules.lazy_runner.

Covers:
    - ``--fallback-phish`` flag parsing
    - Fallback skipped when foothold already exists
    - Fallback invoked and appended to the loop result
"""

from __future__ import annotations

import pytest


@pytest.fixture
def runner():
    from modules import lazy_runner

    return lazy_runner


class TestFlagParsing:
    def test_fallback_phish_flag(self, runner):
        config = runner.parse_loop_line("--fallback-phish --target 10.0.0.1 engage")
        assert config.phishing_fallback is True

    def test_default_off(self, runner):
        config = runner.parse_loop_line("--target 10.0.0.1 engage")
        assert config.phishing_fallback is False


class TestMaybePhishingFallback:
    def test_no_flag_noop(self, runner):
        result = {"task_id": "t1"}
        config = runner.LoopRunConfig(target="10.0.0.1")
        assert runner._maybe_phishing_fallback(result, config, {}) is result

    def test_skipped_when_foothold(self, runner, monkeypatch):

        captured = {}

        def fake_run_fallback(*args, **kwargs):
            captured["ran"] = True
            return {}

        monkeypatch.setattr("modules.lazypoophish.fallback_ready", lambda target: False)
        monkeypatch.setattr("modules.lazypoophish.run_fallback", fake_run_fallback)
        config = runner.LoopRunConfig(target="10.0.0.1", phishing_fallback=True)
        result = runner._maybe_phishing_fallback({"task_id": "t1"}, config, {})
        assert result["fallback"]["skipped"] == "foothold already present"
        assert captured == {}

    def test_invoked_when_no_access(self, runner, monkeypatch):
        monkeypatch.setattr("modules.lazypoophish.fallback_ready", lambda target: True)
        monkeypatch.setattr(
            "modules.lazypoophish.run_fallback",
            lambda target, params: {
                "ok": True,
                "campaign_id": "fed123456789",
                "short_url": "https://is.gd/xx",
                "artifact": "sessions/p.json",
                "error": "",
            },
        )
        config = runner.LoopRunConfig(target="10.0.0.1", phishing_fallback=True)
        result = runner._maybe_phishing_fallback({"task_id": "t1"}, config, {})
        assert result["fallback"]["campaign_id"] == "fed123456789"

    def test_no_target_noop(self, runner, monkeypatch):
        monkeypatch.setattr("modules.lazypoophish.fallback_ready", lambda target: True)
        config = runner.LoopRunConfig(phishing_fallback=True)
        result = runner._maybe_phishing_fallback({"task_id": "t1"}, config, {})
        assert "fallback" not in result

    def test_never_raises(self, runner, monkeypatch):

        def raising(*args, **kwargs):
            raise RuntimeError("boom")

        monkeypatch.setattr("modules.lazypoophish.fallback_ready", raising)
        config = runner.LoopRunConfig(target="10.0.0.1", phishing_fallback=True)
        result = runner._maybe_phishing_fallback({"task_id": "t1"}, config, {})
        assert "fallback" not in result
