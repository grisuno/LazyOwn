"""HTTPS redirect policy for the LazyOwn C2 web layer.

Contract: this module produces the response that a Flask ``before_request``
handler must return to force the client onto TLS in PROD, while leaving
DEV traffic alone.

Invariants:

1. ``is_secure=True`` requests always pass through.
2. ``is_secure=False`` + ``env="PROD"`` + ``enabled=True`` returns a
   301 redirect to the same URL with the scheme replaced by ``https``.
3. ``env="DEV"`` or ``enabled=False`` lets the request pass through.
4. The path, query string, and host header are preserved.
5. The redirect response is a small dataclass so the ``before_request``
   handler does not have to import Flask at import time.

Config keys owned:

- ``c2_https_redirect`` (bool, default ``True``)
- ``env`` (string, default ``"DEV"``)
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class RedirectResponse:
    """A 301 redirect reply compatible with Flask's ``before_request`` return.

    Attributes:
        status_code: HTTP status code, always 301.
        location: Target URL the client should follow.
    """

    status_code: int
    location: str


class HTTPSRedirect:
    """Decide whether a request should be upgraded to HTTPS.

    Args:
        env: Runtime environment tag, usually ``"PROD"`` or ``"DEV"``.
        enabled: When ``False``, the policy is a no-op.
    """

    __slots__ = ("_env", "_enabled")

    def __init__(self, env: str, enabled: bool) -> None:
        self._env = (env or "DEV").upper()
        self._enabled = bool(enabled)

    @property
    def enabled(self) -> bool:
        """Return ``True`` when the policy is active."""
        return self._enabled

    def evaluate(self, request: object) -> RedirectResponse | None:
        """Return a redirect response, or ``None`` if the request can pass.

        Args:
            request: A Flask-shaped request exposing ``is_secure``,
                ``host``, ``path``, and ``query_string`` attributes.

        Returns:
            A :class:`RedirectResponse` to be returned from
            ``before_request``; ``None`` if no redirect is required.
        """
        if not self._enabled or self._env != "PROD":
            return None
        is_secure = bool(getattr(request, "is_secure", False))
        if is_secure:
            return None
        host = getattr(request, "host", "") or ""
        path = getattr(request, "path", "/") or "/"
        query = getattr(request, "query_string", b"") or b""
        if isinstance(query, bytes):
            try:
                query = query.decode("utf-8", errors="replace")
            except Exception:
                query = ""
        location = f"https://{host}{path}"
        if query:
            location = f"{location}?{query}"
        return RedirectResponse(status_code=301, location=location)


__all__ = ["HTTPSRedirect", "RedirectResponse"]
