"""TDD tests for the CORS policy contract.

Contract: ``lazyc2.security.cors.CorsPolicy.resolve_origins(config)`` returns the
allowlist of origins the C2 web layer is willing to serve.

Invariants under test:

1. Wildcard ``*`` is rejected outright (never expose Socket.IO to every origin).
2. In ``PROD`` an empty allowlist raises ``CorsConfigError``.
3. In ``DEV`` an empty allowlist falls back to ``https://{lhost}``.
4. CSV strings are split, trimmed, and empty entries skipped.
5. ``"*"`` entries inside a CSV are dropped, not propagated.
6. ``is_allowed(origin)`` accepts exact matches and denies everything else.
7. ``is_allowed`` tolerates a missing port when comparing hostnames.
"""

from __future__ import annotations

import pytest

from lazyc2.security.cors import CorsConfigError, CorsPolicy


class TestResolveOrigins:
    """Verify origin allowlist derivation from configuration."""

    def test_wildcard_is_rejected(self) -> None:
        with pytest.raises(CorsConfigError):
            CorsPolicy(env="PROD", lhost="10.0.0.1", allowed_origins="*").resolve_origins()

    def test_wildcard_in_csv_is_dropped(self) -> None:
        policy = CorsPolicy(
            env="PROD",
            lhost="10.0.0.1",
            allowed_origins="https://a.example,*,https://b.example",
        )
        origins = policy.resolve_origins()
        assert "*" not in origins
        assert "https://a.example" in origins
        assert "https://b.example" in origins

    def test_prod_empty_allowlist_raises(self) -> None:
        with pytest.raises(CorsConfigError):
            CorsPolicy(env="PROD", lhost="10.0.0.1", allowed_origins="").resolve_origins()

    def test_dev_empty_allowlist_falls_back_to_lhost(self) -> None:
        policy = CorsPolicy(env="DEV", lhost="127.0.0.1", allowed_origins="")
        origins = policy.resolve_origins()
        assert "https://127.0.0.1" in origins
        assert "http://127.0.0.1" in origins

    def test_csv_is_split_and_trimmed(self) -> None:
        policy = CorsPolicy(
            env="PROD",
            lhost="10.0.0.1",
            allowed_origins="  https://a.example , https://b.example  ",
        )
        origins = policy.resolve_origins()
        assert origins == ["https://a.example", "https://b.example"]

    def test_list_input_is_preserved(self) -> None:
        policy = CorsPolicy(
            env="PROD",
            lhost="10.0.0.1",
            allowed_origins=["https://a.example", "https://b.example"],
        )
        assert policy.resolve_origins() == ["https://a.example", "https://b.example"]

    def test_empty_entries_in_csv_are_skipped(self) -> None:
        policy = CorsPolicy(
            env="PROD",
            lhost="10.0.0.1",
            allowed_origins="https://a.example,,https://b.example",
        )
        assert policy.resolve_origins() == ["https://a.example", "https://b.example"]


class TestIsAllowed:
    """Verify the runtime origin check."""

    def test_exact_match_is_allowed(self) -> None:
        policy = CorsPolicy(env="PROD", lhost="10.0.0.1", allowed_origins="https://c2.example")
        assert policy.is_allowed("https://c2.example") is True

    def test_non_matching_origin_is_denied(self) -> None:
        policy = CorsPolicy(env="PROD", lhost="10.0.0.1", allowed_origins="https://c2.example")
        assert policy.is_allowed("https://evil.example") is False

    def test_empty_origin_is_denied(self) -> None:
        policy = CorsPolicy(env="PROD", lhost="10.0.0.1", allowed_origins="https://c2.example")
        assert policy.is_allowed("") is False

    def test_hostname_match_ignores_port(self) -> None:
        policy = CorsPolicy(
            env="PROD",
            lhost="10.0.0.1",
            allowed_origins="https://c2.example:8443",
        )
        assert policy.is_allowed("https://c2.example:9000") is True

    def test_scheme_mismatch_is_denied(self) -> None:
        policy = CorsPolicy(env="PROD", lhost="10.0.0.1", allowed_origins="https://c2.example")
        assert policy.is_allowed("http://c2.example") is False


class TestFlaskSocketIOIntegration:
    """Verify the integration helper used by ``lazyc2.py``."""

    def test_origins_for_socketio(self) -> None:
        policy = CorsPolicy(
            env="PROD",
            lhost="10.0.0.1",
            allowed_origins="https://c2.example",
        )
        origins = policy.origins_for_socketio()
        assert "https://c2.example" in origins
        assert any(o.startswith("https://c2.example:") for o in origins)

    def test_origins_for_socketio_dev_fallback(self) -> None:
        policy = CorsPolicy(env="DEV", lhost="127.0.0.1", allowed_origins="")
        origins = policy.origins_for_socketio()
        assert "https://127.0.0.1" in origins
        assert any(o.startswith("https://127.0.0.1:") for o in origins)
