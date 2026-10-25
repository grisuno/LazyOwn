"""Regression tests for the Socket.IO origin allowlist.

The original wire-up broke xterm.js because flask-socketio does an exact
match between the request ``Origin`` header and the ``cors_allowed_origins``
list. The browser sends ``https://127.0.0.1:5000`` (with port) but the
list only had ``https://127.0.0.1`` (no port), so the WebSocket upgrade
was rejected with HTTP 400.

This test ensures the policy returns the allowlist expanded with the
common C2 ports for the configured lhost so the upgrade succeeds.
"""

from __future__ import annotations

import pytest

from lazyc2.security.cors import CorsPolicy


class TestOriginsForSocketIO:
    """Verify the list fed to ``SocketIO(cors_allowed_origins=...)``."""

    def test_dev_empty_includes_lhost_with_common_ports(self) -> None:
        policy = CorsPolicy(env="DEV", lhost="127.0.0.1", allowed_origins="")
        origins = policy.origins_for_socketio()
        assert "https://127.0.0.1" in origins
        assert any(o.startswith("https://127.0.0.1:") for o in origins)

    def test_dev_empty_includes_http_and_https(self) -> None:
        policy = CorsPolicy(env="DEV", lhost="127.0.0.1", allowed_origins="")
        origins = policy.origins_for_socketio()
        assert any(o.startswith("http://127.0.0.1") for o in origins)
        assert any(o.startswith("https://127.0.0.1") for o in origins)

    def test_dev_empty_includes_localhost_alias(self) -> None:
        policy = CorsPolicy(env="DEV", lhost="127.0.0.1", allowed_origins="")
        origins = policy.origins_for_socketio()
        assert any("localhost" in o for o in origins)

    def test_explicit_origins_kept_with_port_appended(self) -> None:
        policy = CorsPolicy(
            env="PROD",
            lhost="c2.example",
            allowed_origins="https://c2.example",
            c2_port=5000,
        )
        origins = policy.origins_for_socketio()
        assert "https://c2.example" in origins
        assert "https://c2.example:5000" in origins

    def test_explicit_origins_deduped(self) -> None:
        policy = CorsPolicy(
            env="PROD",
            lhost="c2.example",
            allowed_origins="https://c2.example:5000,https://c2.example",
            c2_port=5000,
        )
        origins = policy.origins_for_socketio()
        assert origins.count("https://c2.example:5000") == 1

    def test_prod_raises_when_empty(self) -> None:
        with pytest.raises(Exception):
            CorsPolicy(env="PROD", lhost="c2.example", allowed_origins="").origins_for_socketio()

    def test_wildcard_rejected(self) -> None:
        with pytest.raises(Exception):
            CorsPolicy(env="PROD", lhost="c2.example", allowed_origins="*").origins_for_socketio()
