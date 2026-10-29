"""Tests for modules.lazypoophish — loop phishing fallback.

Covers:
    - fallback_ready gating from access tokens (monkeypatched)
    - run_fallback happy path with mocked campaign launch + shortener
    - Offline artefact and short URL persistence
    - Invalid mode and launch failure paths
"""

from __future__ import annotations

import json
from pathlib import Path
from types import SimpleNamespace

import pytest


@pytest.fixture
def poophish():
    from modules import lazypoophish

    return lazypoophish


@pytest.fixture
def cleared_sessions(tmp_path, monkeypatch):
    monkeypatch.setattr("modules.lazypoophish.SESSIONS_DIR", tmp_path)
    return tmp_path


def _fake_orchestrator(monkeypatch, campaign_dir: Path, campaign_id: str):
    def fake_launch(target_domain, template="microsoft_365_login", mode="credential_harvest", targets_file=""):
        campaign_dir.mkdir(parents=True, exist_ok=True)
        (campaign_dir / "campaign.json").write_text(
            json.dumps(
                {
                    "campaign_id": campaign_id,
                    "target_domain": target_domain,
                    "phishing_url": f"http://10.0.0.1:8888/phish/{campaign_id}",
                }
            ),
            encoding="utf-8",
        )
        return campaign_id

    monkeypatch.setattr(
        "modules.phishing_orchestrator.PhishingOrchestrator.get_instance",
        classmethod(lambda cls: SimpleNamespace(launch=fake_launch)),
    )


class TestFallbackReady:
    def test_ready_when_access_none(self, poophish, monkeypatch):
        monkeypatch.setattr("modules.chain_tokens.build_tokens", lambda target, params: {"access": "none"})
        assert poophish.fallback_ready("10.0.0.1") is True

    def test_not_ready_with_access(self, poophish, monkeypatch):
        monkeypatch.setattr("modules.chain_tokens.build_tokens", lambda target, params: {"access": "user"})
        assert poophish.fallback_ready("10.0.0.1") is False

    def test_ready_when_tokens_fail(self, poophish, monkeypatch):
        def raising(*args, **kwargs):
            raise RuntimeError("facts down")

        monkeypatch.setattr("modules.chain_tokens.build_tokens", raising)
        assert poophish.fallback_ready("10.0.0.1") is True


class TestRunFallback:
    def test_invalid_mode(self, poophish, cleared_sessions):
        result = poophish.run_fallback("10.0.0.1", mode="nope")
        assert result["ok"] is False
        assert "invalid mode" in result["error"]

    def test_launch_failure(self, poophish, cleared_sessions, monkeypatch):
        monkeypatch.setattr(
            "modules.phishing_orchestrator.PhishingOrchestrator.get_instance",
            classmethod(lambda cls: SimpleNamespace(launch=lambda *a, **k: "")),
        )
        result = poophish.run_fallback("10.0.0.1")
        assert result["ok"] is False
        assert "campaign" in result["error"]

    def test_short_url_and_artifact(self, poophish, cleared_sessions, monkeypatch):
        campaign_id = "abc123456789"
        campaign_dir = cleared_sessions / f"phishing_{campaign_id}"

        def fake_shorten(url, provider="isgd", **kwargs):
            return {"ok": True, "short_url": "https://is.gd/x1", "provider": provider, "error": ""}

        _fake_orchestrator(monkeypatch, campaign_dir, campaign_id)
        monkeypatch.setattr("modules.lazyshortener.shorten", fake_shorten)
        result = poophish.run_fallback("10.0.0.1", {"domain": "corp.local"})
        assert result["ok"] is True
        assert result["short_url"] == "https://is.gd/x1"
        artefact = Path(result["artifact"])
        assert artefact.exists()
        data = json.loads(artefact.read_text(encoding="utf-8"))
        assert data["campaign_id"] == campaign_id
        assert data["phishing_short_url"] == "https://is.gd/x1"
        assert (
            "is.gd" not in (campaign_dir / "campaign.json").read_text(encoding="utf-8")
            or json.loads((campaign_dir / "campaign.json").read_text(encoding="utf-8")).get("phishing_short_url")
            == "https://is.gd/x1"
        )

    def test_no_shorten_keeps_raw_url(self, poophish, cleared_sessions, monkeypatch):
        campaign_id = "def456123456"
        campaign_dir = cleared_sessions / f"phishing_{campaign_id}"
        _fake_orchestrator(monkeypatch, campaign_dir, campaign_id)

        def forbidden(*args, **kwargs):
            raise AssertionError("shortener must not run with shorten=False")

        monkeypatch.setattr("modules.lazyshortener.shorten", forbidden)
        result = poophish.run_fallback("10.0.0.1", shorten=False)
        assert result["ok"] is True
        assert result["short_url"] == ""
        artefact = json.loads(Path(result["artifact"]).read_text(encoding="utf-8"))
        assert artefact["phishing_short_url"] == ""
