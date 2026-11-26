"""Session-token gate: bearer tokens issued by the C2 backend.

Estorides-parity auth layer on top of the existing Basic-auth gate. The
backend mints one random session token at boot (memory-only, never
written next to ``.c2_credentials.txt``), operators exchange valid
credentials for it once via ``POST /api/auth/token``, and every gated
request must present it. A compromised credentials file alone is no
longer enough: the token rotates on every C2 restart and expires after
``TOKEN_TTL_SECONDS``.

Extraction order (first match wins):
``Authorization: Bearer <token>``, ``X-LazyOwn-Token``, the
``lazyown_c2_session`` cookie, and ``?token=`` on GET requests only
(SSE/EventSource cannot set headers; the value leaks into access logs,
so the caller is warned).
"""

from __future__ import annotations

import hmac
import logging
import os
import secrets
import time
from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Any

from flask import g, jsonify, request

log = logging.getLogger(__name__)

TOKEN_TTL_SECONDS = 12 * 60 * 60
TOKEN_LENGTH_BYTES = 32
AUTH_COOKIE = "lazyown_c2_session"
AUTH_ALT_HEADER = "X-LazyOwn-Token"
AUTH_HEADER = "Authorization"
_BEARER_PREFIX = "bearer "
_MISSING_TOKEN_BODY = {"error": "unauthorized: operator token required"}


def _token_bytes(length: int = TOKEN_LENGTH_BYTES) -> str:
    """Return a random hex token.

    Args:
        length: Entropy in bytes before hex encoding.

    Returns:
        Hex-encoded random string.
    """
    return secrets.token_hex(length)


@dataclass
class SessionTokenGate:
    """Single shared bearer token with TTL, compared in constant time.

    Attributes:
        token: The active hex token, or ``None`` when the gate is off.
        ttl_seconds: Lifetime of the token.
        issued_at: Monotonic clock value at issue time.
    """

    token: str | None = None
    ttl_seconds: int = TOKEN_TTL_SECONDS
    issued_at: float = field(default_factory=time.monotonic)

    @property
    def enabled(self) -> bool:
        """Whether the gate enforces tokens.

        Returns:
            True when a token is configured.
        """
        return self.token is not None

    @property
    def expired(self) -> bool:
        """Whether the token lifetime has elapsed.

        Returns:
            True when the token is missing or past its TTL.
        """
        if self.token is None:
            return True
        return (time.monotonic() - self.issued_at) >= self.ttl_seconds

    def check(self, presented: str | None) -> bool:
        """Compare a presented token in constant time.

        Args:
            presented: Token supplied by the caller, or ``None``.

        Returns:
            True when it matches the active token and is not expired.
        """
        if not self.enabled or self.expired:
            return False
        if not presented:
            return False
        return hmac.compare_digest(presented, self.token or "")

    def rotate(self) -> str:
        """Mint a fresh token and reset the TTL clock.

        Returns:
            The new hex token.
        """
        self.token = _token_bytes()
        self.issued_at = time.monotonic()
        return self.token

    def expires_at_epoch(self) -> float:
        """Absolute expiry for clients.

        Returns:
            Unix timestamp after which the token stops working.
        """
        import time as _time

        return _time.time() + max(self.ttl_seconds - (time.monotonic() - self.issued_at), 0)

    def issue_session_cookie_kwargs(self, secure: bool = False) -> dict[str, Any]:
        """Keyword arguments for ``set_cookie`` installing the session.

        Args:
            secure: Force the ``Secure`` attribute (HTTPS-only deployments).

        Returns:
            Cookie kwargs mirroring the estorides session policy.
        """
        return {
            "max_age": self.ttl_seconds,
            "httponly": True,
            "samesite": "Lax",
            "secure": secure or os.environ.get("LAZYOWN_FORCE_HTTPS") == "1",
            "path": "/",
        }


def extract_token() -> str | None:
    """Pull the operator token from the current request.

    Returns:
        The token string, or ``None`` when absent.
    """
    header = request.headers.get(AUTH_HEADER, "")
    if header.lower().startswith(_BEARER_PREFIX):
        candidate = header[len(_BEARER_PREFIX) :].strip()
        if candidate:
            return candidate
    alt = request.headers.get(AUTH_ALT_HEADER, "").strip()
    if alt:
        return alt
    cookie = request.cookies.get(AUTH_COOKIE, "").strip()
    if cookie:
        return cookie
    if request.method == "GET":
        query_token = request.args.get("token", "").strip()
        if query_token:
            log.warning("token accepted via query param (leaks into access logs); prefer the Authorization header")
            return query_token
    return None


def install_token_gate(
    app: Any,
    gate: SessionTokenGate,
    is_exempt: Callable[[], bool],
) -> SessionTokenGate:
    """Attach the gate to the Flask app via a ``before_request`` hook.

    Args:
        app: Flask application receiving the hook.
        gate: The configured token gate.
        is_exempt: Callable returning True when the current request is
            exempt (beacon transports, login flow, static assets...).

    Returns:
        The installed gate.

    Raises:
        ValueError: When the gate is disabled.
    """
    if not gate.enabled:
        raise ValueError("install_token_gate requires an enabled gate")

    @app.before_request
    def _enforce_session_token():  # noqa: ANN202
        if is_exempt():
            return None
        if gate.check(extract_token()):
            g.session_token_authenticated = True
            return None
        response = jsonify(_MISSING_TOKEN_BODY)
        response.status_code = 401
        response.headers["WWW-Authenticate"] = 'Bearer realm="lazyown-c2"'
        return response

    app.extensions["lazyown_token_gate"] = gate
    log.info("token gate ENABLED (session token required; expires every %ds)", gate.ttl_seconds)
    return gate


__all__ = [
    "AUTH_ALT_HEADER",
    "AUTH_COOKIE",
    "AUTH_HEADER",
    "TOKEN_LENGTH_BYTES",
    "TOKEN_TTL_SECONDS",
    "SessionTokenGate",
    "extract_token",
    "install_token_gate",
]
