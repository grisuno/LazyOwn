"""CSRF protection policy for the LazyOwn C2 web layer.

Contract: this module issues per-session tokens that the client must echo
back on every mutating request, except for a configured allowlist of
exempt paths (login, logout, beacon endpoints).

Invariants:

1. Tokens are 32 URL-safe bytes (43 characters base64-encoded) generated
   with :func:`secrets.token_urlsafe`.
2. The token store is keyed by session id, so the same session always
   receives the same token until it is rotated.
3. Validation is constant-time to defeat timing oracles.
4. The exempt set is configurable; ``/login`` and ``/logout`` are always
   exempt by default, and ``/api/beacon/`` is exempt because implants
   cannot parse HTML to read a token.
5. ``GET``, ``HEAD``, ``OPTIONS``, and ``TRACE`` requests are treated as
   safe and bypass the check.

Config keys owned:

- ``c2_csrf_enabled`` (bool, default ``True``)
- ``c2_csrf_exempt_paths`` (CSV string, default
  ``"/login,/logout,/register,/api/beacon"``)
- ``c2_csrf_header`` (string, default ``"X-XSRF-TOKEN"``)
"""

from __future__ import annotations

import hmac
import secrets
from typing import Mapping


_SAFE_METHODS = frozenset({"GET", "HEAD", "OPTIONS", "TRACE"})

_DEFAULT_EXEMPT_PATHS: tuple[str, ...] = (
    "/login",
    "/logout",
    "/register",
    "/api/beacon",
)

_DEFAULT_HEADER = "X-XSRF-TOKEN"
_DEFAULT_FORM_FIELD = "xsrf_token"
_DEFAULT_COOKIE = "XSRF-TOKEN"


class CSRFPolicy:
    """Per-session CSRF token issuer and validator.

    Args:
        header: HTTP header name carrying the token from the client.
        form_field: Form field name used as a fallback for older clients.
        cookie_name: Cookie name used to seed the client-side read.
        exempt_paths: Tuple of path prefixes that bypass the check.
        secret: Optional pre-shared secret. When ``None`` a fresh
            ``secrets.token_urlsafe(32)`` is generated at construction.
    """

    __slots__ = (
        "_header",
        "_form_field",
        "_cookie_name",
        "_exempt_paths",
        "_secret",
        "_store",
    )

    def __init__(
        self,
        header: str = _DEFAULT_HEADER,
        form_field: str = _DEFAULT_FORM_FIELD,
        cookie_name: str = _DEFAULT_COOKIE,
        exempt_paths: tuple[str, ...] = _DEFAULT_EXEMPT_PATHS,
        secret: str | None = None,
    ) -> None:
        self._header = header
        self._form_field = form_field
        self._cookie_name = cookie_name
        self._exempt_paths = tuple(exempt_paths)
        self._secret = secret or secrets.token_urlsafe(32)
        self._store: dict[str, str] = {}

    @property
    def header(self) -> str:
        """Return the HTTP header name carrying the token."""
        return self._header

    @property
    def cookie_name(self) -> str:
        """Return the cookie name that should hold the readable token."""
        return self._cookie_name

    def issue(self, session_id: str) -> str:
        """Return the token bound to ``session_id``.

        Args:
            session_id: The Flask session id; must be a non-empty string.

        Returns:
            A URL-safe token string, stable for the same session id.
        """
        if not session_id:
            raise ValueError("session_id is required")
        token = self._store.get(session_id)
        if token is None:
            token = secrets.token_urlsafe(32)
            self._store[session_id] = token
        return token

    def rotate(self, session_id: str) -> str:
        """Force a fresh token for ``session_id``.

        Args:
            session_id: The session id to rotate.

        Returns:
            The new token.
        """
        if not session_id:
            raise ValueError("session_id is required")
        token = secrets.token_urlsafe(32)
        self._store[session_id] = token
        return token

    def forget(self, session_id: str) -> None:
        """Drop the token bound to ``session_id`` (e.g. on logout)."""
        self._store.pop(session_id, None)

    def validate(self, session_id: str, candidate: str | None) -> bool:
        """Return ``True`` iff ``candidate`` matches the stored token.

        Args:
            session_id: The session id to look up.
            candidate: The token echoed back by the client.

        Returns:
            ``True`` when the constant-time comparison succeeds.
        """
        if not session_id or not candidate:
            return False
        stored = self._store.get(session_id)
        if stored is None:
            return False
        return hmac.compare_digest(stored, candidate)

    def is_exempt(self, path: str) -> bool:
        """Return ``True`` if ``path`` is in the exempt set.

        Args:
            path: The request path (e.g. ``"/login"``).

        Returns:
            ``True`` when any exempt prefix is a prefix of ``path``.
        """
        if not path:
            return False
        for prefix in self._exempt_paths:
            if path == prefix or path.startswith(prefix.rstrip("/") + "/") or path.startswith(prefix):
                return True
        return False

    def extract_token(self, request: object) -> str | None:
        """Return the token from a Flask-shaped request.

        Args:
            request: An object exposing ``headers`` and ``form`` mappings.

        Returns:
            The token string or ``None`` if absent.
        """
        headers: Mapping[str, str] = getattr(request, "headers", {}) or {}
        form: Mapping[str, str] = getattr(request, "form", {}) or {}
        header_value = headers.get(self._header)
        if header_value:
            return header_value
        form_value = form.get(self._form_field)
        if form_value:
            return form_value
        return None

    def check_request(self, session_id: str, request: object) -> bool:
        """Run the full CSRF gate against a request.

        Args:
            session_id: The session id derived from the request cookie.
            request: A Flask-shaped request.

        Returns:
            ``True`` when the request should be allowed, ``False`` otherwise.
        """
        method = (getattr(request, "method", "GET") or "GET").upper()
        path = getattr(request, "path", "/") or "/"
        if method in _SAFE_METHODS:
            return True
        if self.is_exempt(path):
            return True
        candidate = self.extract_token(request)
        return self.validate(session_id, candidate)


__all__ = ["CSRFPolicy"]
