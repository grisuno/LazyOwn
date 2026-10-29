"""Tests for modules.lazyshortener — keyless URL shortener bridge.

Covers:
    - Provider inventory
    - URL validation guard (scheme, metacharacters)
    - Shortening round-trip with mocked HTTP
    - Provider error and transport failure paths
"""

from __future__ import annotations

import pytest
import requests


@pytest.fixture
def shortener():
    from modules import lazyshortener

    return lazyshortener


class _FakeResponse:
    def __init__(self, text: str, status: int = 200):
        self.text = text
        self.status_code = status

    def raise_for_status(self) -> None:
        if self.status_code >= 400:
            raise requests.HTTPError(f"status {self.status_code}")


class TestLazyShortener:
    def test_providers(self, shortener):
        assert "isgd" in shortener.providers()
        assert "vgd" in shortener.providers()

    def test_unknown_provider(self, shortener):
        result = shortener.shorten("https://example.com", provider="nope")
        assert result["ok"] is False
        assert "unknown provider" in result["error"]

    def test_rejects_invalid_url(self, shortener):
        result = shortener.shorten("not-a-url")
        assert result["ok"] is False
        assert "url rejected" in result["error"]

    def test_rejects_metacharacters(self, shortener):
        result = shortener.shorten("https://example.com/a;rm|")
        assert result["ok"] is False
        assert "url rejected" in result["error"]

    def test_shorten_success(self, shortener, monkeypatch):
        captured = {}

        def fake_get(endpoint, params=None, **kwargs):
            captured["endpoint"] = endpoint
            captured["params"] = params
            return _FakeResponse("https://is.gd/abc123")

        monkeypatch.setattr(shortener.requests, "get", fake_get)
        result = shortener.shorten("https://example.com/login")
        assert result["ok"] is True
        assert result["short_url"] == "https://is.gd/abc123"
        assert captured["params"]["url"] == "https://example.com/login"
        assert captured["params"]["format"] == "simple"

    def test_provider_error_message(self, shortener, monkeypatch):
        monkeypatch.setattr(shortener.requests, "get", lambda *a, **k: _FakeResponse("Error: invalid URL", 200))
        result = shortener.shorten("https://example.com")
        assert result["ok"] is False
        assert "Error" in result["error"]

    def test_transport_failure(self, shortener, monkeypatch):
        def raising(*args, **kwargs):
            raise requests.ConnectionError("no network")

        monkeypatch.setattr(shortener.requests, "get", raising)
        result = shortener.shorten("https://example.com")
        assert result["ok"] is False
        assert "request failed" in result["error"]
