"""Trusted proxy resolver for the LazyOwn C2 web layer.

Contract: this module decides what the real client IP is, taking the
``X-Forwarded-For`` chain into account only when the operator has
declared one or more trusted reverse proxies in front of the C2.

Invariants:

1. When ``trusted_count == 0`` the resolver ignores
   ``X-Forwarded-For`` entirely and returns ``remote_addr``.
2. When ``trusted_count > 0`` the chain is parsed right-to-left; the
   rightmost ``trusted_count`` entries are considered proxy hops and
   discarded, and the leftmost remaining address is returned.
3. When the chain is shorter than ``trusted_count`` the resolver falls
   back to ``remote_addr`` rather than trusting a spoofed header.
4. ``is_operator(ip)`` does an exact-string comparison against the
   configured allowlist.

Config keys owned:

- ``c2_trusted_proxy_count`` (int, default ``0``)
- ``c2_operator_ip_allowlist`` (CSV string, default ``"127.0.0.1,{lhost}"``)
"""

from __future__ import annotations

from typing import Iterable


class TrustedProxyResolver:
    """Resolve the real client IP from Flask's ``request`` data.

    Args:
        trusted_count: Number of trusted reverse proxies in front of
            the C2. Set to ``0`` to disable header parsing.
        operator_allowlist: Iterable of operator IPs eligible for
            operator-only routes.
    """

    __slots__ = ("_trusted_count", "_operator_allowlist")

    def __init__(
        self,
        trusted_count: int,
        operator_allowlist: Iterable[str],
    ) -> None:
        if trusted_count < 0:
            raise ValueError("trusted_count must be >= 0")
        self._trusted_count = int(trusted_count)
        self._operator_allowlist = frozenset(ip.strip() for ip in operator_allowlist if ip)

    @property
    def trusted_count(self) -> int:
        """Return the configured number of trusted proxy hops."""
        return self._trusted_count

    def client_ip(
        self,
        remote_addr: str | None,
        x_forwarded_for: str | None = None,
    ) -> str:
        """Return the resolved client IP.

        Args:
            remote_addr: Flask's ``request.remote_addr``.
            x_forwarded_for: The ``X-Forwarded-For`` header value or
                ``None`` if missing.

        Returns:
            The resolved IP string. Never empty.
        """
        fallback = remote_addr or "0.0.0.0"
        if self._trusted_count <= 0 or not x_forwarded_for:
            return fallback
        parts = [segment.strip() for segment in x_forwarded_for.split(",") if segment.strip()]
        if len(parts) <= self._trusted_count:
            return fallback
        return parts[0]

    def is_operator(self, ip: str | None) -> bool:
        """Return ``True`` when ``ip`` is in the operator allowlist.

        Args:
            ip: The IP string to test, typically the value returned by
                :meth:`client_ip`.

        Returns:
            ``True`` for an exact-string match against the allowlist.
        """
        if not ip:
            return False
        return ip in self._operator_allowlist


__all__ = ["TrustedProxyResolver"]
