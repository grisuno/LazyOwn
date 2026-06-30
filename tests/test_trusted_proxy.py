"""TDD tests for the trusted proxy resolver contract.

Contract: ``lazyc2.security.trusted_proxy.TrustedProxyResolver.client_ip``
returns the real client IP, ignoring spoofed ``X-Forwarded-For`` entries
when no trusted proxy count is configured.

Invariants:

1. ``trusted_count=0``: always returns ``remote_addr`` and ignores
   ``X-Forwarded-For`` entirely.
2. ``trusted_count=N``: parses ``X-Forwarded-For`` right-to-left, skipping
   the rightmost N entries, and returns the leftmost untrusted address.
3. Missing or empty ``X-Forwarded-For`` falls back to ``remote_addr``.
4. ``is_operator(remote_addr)`` matches the configured operator allowlist.
"""

from __future__ import annotations

import pytest

from lazyc2.security.trusted_proxy import TrustedProxyResolver


class TestNoProxy:
    """Without a trusted proxy, X-Forwarded-For is ignored."""

    def test_remote_addr_returned(self) -> None:
        resolver = TrustedProxyResolver(
            trusted_count=0,
            operator_allowlist=("127.0.0.1",),
        )
        assert resolver.client_ip(
            remote_addr="127.0.0.1",
            x_forwarded_for="6.6.6.6",
        ) == "127.0.0.1"

    def test_no_header_falls_back_to_remote(self) -> None:
        resolver = TrustedProxyResolver(trusted_count=0, operator_allowlist=("127.0.0.1",))
        assert resolver.client_ip(remote_addr="10.0.0.5") == "10.0.0.5"


class TestTrustedProxy:
    """With a trusted proxy, X-Forwarded-For is parsed."""

    def test_single_proxy_returns_leftmost(self) -> None:
        resolver = TrustedProxyResolver(
            trusted_count=1,
            operator_allowlist=("127.0.0.1",),
        )
        assert (
            resolver.client_ip(
                remote_addr="10.0.0.1",
                x_forwarded_for="6.6.6.6, 10.0.0.1",
            )
            == "6.6.6.6"
        )

    def test_two_proxies_returns_leftmost(self) -> None:
        resolver = TrustedProxyResolver(
            trusted_count=2,
            operator_allowlist=("127.0.0.1",),
        )
        assert (
            resolver.client_ip(
                remote_addr="10.0.0.1",
                x_forwarded_for="6.6.6.6, 10.0.0.2, 10.0.0.1",
            )
            == "6.6.6.6"
        )

    def test_insufficient_chain_falls_back(self) -> None:
        resolver = TrustedProxyResolver(
            trusted_count=2,
            operator_allowlist=("127.0.0.1",),
        )
        assert (
            resolver.client_ip(
                remote_addr="10.0.0.1",
                x_forwarded_for="6.6.6.6",
            )
            == "10.0.0.1"
        )

    def test_empty_header_falls_back(self) -> None:
        resolver = TrustedProxyResolver(
            trusted_count=1,
            operator_allowlist=("127.0.0.1",),
        )
        assert (
            resolver.client_ip(
                remote_addr="10.0.0.1",
                x_forwarded_for="",
            )
            == "10.0.0.1"
        )


class TestIsOperator:
    """Verify operator allowlist checks."""

    def test_match(self) -> None:
        resolver = TrustedProxyResolver(
            trusted_count=0,
            operator_allowlist=("127.0.0.1", "10.0.0.5"),
        )
        assert resolver.is_operator("10.0.0.5") is True

    def test_no_match(self) -> None:
        resolver = TrustedProxyResolver(
            trusted_count=0,
            operator_allowlist=("127.0.0.1",),
        )
        assert resolver.is_operator("6.6.6.6") is False
