"""CORS origin allowlist policy for the LazyOwn C2 web layer.

Contract: this module owns the single source of truth for which origins the
C2 web layer and its Socket.IO transport are willing to serve.

Invariants:

1. The wildcard ``"*"`` is never permitted; an empty allowlist is allowed
   only when ``env != "PROD"`` and falls back to ``https://{lhost}``.
2. CSV strings are split on comma, trimmed, and empty tokens skipped.
3. ``"*"`` tokens inside a CSV are silently dropped (defence in depth).
4. ``is_allowed(origin)`` matches by ``scheme://hostname[:port]`` so the
   port may differ between the configured origin and the request.
5. ``origins_for_socketio()`` returns the allowlist expanded with the
   configured ``c2_port`` and the common C2 ports so flask-socketio's
   exact-match check on the ``Origin`` header passes for the xterm.js
   and beacon clients.
6. The policy is intentionally immutable: ``resolve_origins()`` can be
   called repeatedly and returns a fresh list each time.

Config keys owned:

- ``env`` (string, default ``"DEV"``)
- ``lhost`` (string, used for the dev fallback)
- ``c2_port`` (int, used to expand the socketio allowlist)
- ``c2_allowed_origins`` (string CSV or list of strings, default ``""``)
"""

from __future__ import annotations

from typing import Iterable
from urllib.parse import urlsplit


_DEFAULT_SOCKETIO_PORTS: tuple[int, ...] = (
    443,
    5000,
    5001,
    8000,
    8080,
    8443,
    8888,
    9000,
)


class CorsConfigError(ValueError):
    """Raised when the CORS configuration is invalid for the current env."""


class CorsPolicy:
    """Immutable CORS allowlist derived from the LazyOwn runtime config.

    Args:
        env: Runtime environment tag, usually ``"PROD"`` or ``"DEV"``.
        lhost: Loopback or operator-side address used for the dev fallback.
        allowed_origins: Either a CSV string or a sequence of origins.
        c2_port: Optional C2 port used to expand the Socket.IO allowlist.
        extra_socketio_ports: Optional additional ports to include in the
            Socket.IO expansion. Defaults to the common C2 ports.
    """

    __slots__ = (
        "_env",
        "_lhost",
        "_raw_origins",
        "_c2_port",
        "_extra_socketio_ports",
    )

    def __init__(
        self,
        env: str,
        lhost: str,
        allowed_origins: str | Iterable[str] | None,
        c2_port: int | None = None,
        extra_socketio_ports: Iterable[int] | None = None,
    ) -> None:
        self._env = (env or "DEV").upper()
        self._lhost = lhost or ""
        self._raw_origins = allowed_origins
        self._c2_port = int(c2_port) if c2_port else None
        self._extra_socketio_ports = tuple(extra_socketio_ports) if extra_socketio_ports else ()

    @property
    def env(self) -> str:
        """Return the normalized environment tag (``"PROD"`` or ``"DEV"``)."""
        return self._env

    def resolve_origins(self) -> list[str]:
        """Return the validated allowlist of origins for the current env.

        Returns:
            A list of origins such as ``["https://c2.example"]``.

        Raises:
            CorsConfigError: when ``env`` is ``"PROD"`` and the resolved
                allowlist is empty.
        """
        candidates = self._collect_candidates()
        cleaned = self._clean(candidates)
        if not cleaned and self._env == "PROD":
            raise CorsConfigError(
                "c2_allowed_origins must be configured in PROD; "
                "set it in payload.json (CSV or list of full origin URLs)."
            )
        if not cleaned:
            cleaned = self._dev_fallback()
        return list(cleaned)

    def origins_for_socketio(self) -> list[str]:
        """Return the allowlist to feed ``flask_socketio.SocketIO``.

        ``flask_socketio`` does an exact match between the request
        ``Origin`` header and the list passed as ``cors_allowed_origins``.
        The browser typically sends the full origin including the port
        (e.g. ``https://127.0.0.1:5000``), so this method expands the
        policy with the configured ``c2_port`` and the common C2 ports
        so the WebSocket upgrade succeeds.

        Returns:
            A deduplicated list of origins with explicit ports.
        """
        base = self.resolve_origins()
        expanded: list[str] = []
        for origin in base:
            expanded.append(origin)
            host = _host_of(origin)
            if not host:
                continue
            for port in self._socketio_ports():
                candidate = f"{_scheme_of(origin)}://{host}:{port}"
                if candidate not in expanded:
                    expanded.append(candidate)
        return expanded

    def is_allowed(self, origin: str | None) -> bool:
        """Return ``True`` if ``origin`` matches any allowed entry.

        Args:
            origin: The ``Origin`` header from the incoming request.

        Returns:
            ``True`` when the origin is in the allowlist (port-insensitive),
            ``False`` otherwise.
        """
        if not origin:
            return False
        try:
            allowed = self.resolve_origins()
        except CorsConfigError:
            return False
        for entry in allowed:
            if _origin_matches(entry, origin):
                return True
        return False

    def _socketio_ports(self) -> tuple[int, ...]:
        ports: list[int] = list(self._extra_socketio_ports)
        if self._c2_port and self._c2_port not in ports:
            ports.append(self._c2_port)
        for port in _DEFAULT_SOCKETIO_PORTS:
            if port not in ports:
                ports.append(port)
        return tuple(ports)

    def _collect_candidates(self) -> list[str]:
        raw = self._raw_origins
        if raw is None or raw == "":
            return []
        if isinstance(raw, str):
            return [token for token in raw.split(",")]
        return list(raw)

    @staticmethod
    def _clean(candidates: Iterable[str]) -> list[str]:
        seen: list[str] = []
        for token in candidates:
            value = token.strip()
            if not value or value == "*":
                continue
            if value not in seen:
                seen.append(value)
        return seen

    def _dev_fallback_origins(self) -> list[str]:
        host = self._lhost.strip() or "127.0.0.1"
        aliases = [host]
        if host == "127.0.0.1" and "localhost" not in aliases:
            aliases.append("localhost")
        return [f"http://{alias}" for alias in aliases] + [
            f"https://{alias}" for alias in aliases
        ]

    def _dev_fallback(self) -> list[str]:
        return list(self._dev_fallback_origins())


def _origin_matches(allowed: str, candidate: str) -> bool:
    """Return ``True`` if ``candidate`` matches ``allowed`` ignoring port.

    Args:
        allowed: A configured origin like ``"https://c2.example:8443"``.
        candidate: The ``Origin`` header value to check.

    Returns:
        ``True`` when scheme and hostname match, regardless of port.
    """
    try:
        a = urlsplit(allowed)
        c = urlsplit(candidate)
    except ValueError:
        return False
    if not a.scheme or not a.hostname:
        return False
    if a.scheme.lower() != c.scheme.lower():
        return False
    if a.hostname.lower() != (c.hostname or "").lower():
        return False
    return True


def _scheme_of(origin: str) -> str:
    try:
        return urlsplit(origin).scheme or "https"
    except ValueError:
        return "https"


def _host_of(origin: str) -> str:
    try:
        return urlsplit(origin).hostname or ""
    except ValueError:
        return ""


__all__ = ["CorsConfigError", "CorsPolicy"]
