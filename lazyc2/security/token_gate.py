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
TICKET_TTL_SECONDS = 60
MAX_OUTSTANDING_TICKETS = 100
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
class _IssuedToken:
    """One operator's live token.

    Attributes:
        token: Hex token value.
        issued_at: Monotonic clock value at issue time.
    """

    token: str
    issued_at: float = field(default_factory=time.monotonic)


@dataclass
class SessionTokenGate:
    """Single shared bearer token plus per-operator tokens and tickets.

    The primary token rotates at boot; operator tokens let each operator
    hold an independent credential that revokes individually, and SSE
    tickets are one-time short-lived values for clients that cannot set
    headers. All comparisons are constant time.

    Attributes:
        token: The active primary hex token, or ``None`` when off.
        ttl_seconds: Lifetime of the primary token.
        issued_at: Monotonic clock value at issue time.
    """

    token: str | None = None
    ttl_seconds: int = TOKEN_TTL_SECONDS
    issued_at: float = field(default_factory=time.monotonic)
    ticket_ttl_seconds: int = TICKET_TTL_SECONDS
    _operator_tokens: dict[str, _IssuedToken] = field(default_factory=dict)
    _tickets: dict[str, float] = field(default_factory=dict)

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

        Accepts the primary token, any live operator token, or an unused
        ticket within its TTL (which is then consumed).

        Args:
            presented: Token supplied by the caller, or ``None``.

        Returns:
            True when it matches an accepted token and is not expired.
        """
        if not presented:
            return False
        if not self.enabled or self.expired:
            return False
        if hmac.compare_digest(presented, self.token or ""):
            return True
        if self._check_operator_token(presented):
            return True
        return self._consume_ticket(presented)

    def _check_operator_token(self, presented: str) -> bool:
        """Return True when ``presented`` matches a live operator token.

        Args:
            presented: Candidate token value.

        Returns:
            True when an operator token matches and is within its TTL.
        """
        now = time.monotonic()
        for issued in self._operator_tokens.values():
            if (now - issued.issued_at) < self.ttl_seconds and hmac.compare_digest(presented, issued.token):
                return True
        return False

    def issue_for_operator(self, operator: str) -> str:
        """Mint an independent token for one operator.

        Args:
            operator: Stable operator name owning the token.

        Returns:
            The new hex token.

        Raises:
            ValueError: When the operator name is blank.
        """
        name = str(operator or "").strip()
        if not name:
            raise ValueError("operator name is required")
        issued = _IssuedToken(token=_token_bytes())
        self._operator_tokens[name] = issued
        return issued.token

    def revoke_operator(self, operator: str) -> int:
        """Revoke one operator's token.

        Args:
            operator: Operator name to revoke.

        Returns:
            1 when a token was removed, 0 when the name had none.
        """
        return 1 if self._operator_tokens.pop(str(operator or "").strip(), None) is not None else 0

    def issue_ticket(self) -> str:
        """Mint a one-time short-lived ticket (SSE handshake).

        Returns:
            The new hex ticket.
        """
        if len(self._tickets) >= MAX_OUTSTANDING_TICKETS:
            oldest = min(self._tickets, key=self._tickets.get, default=None)
            if oldest is not None:
                self._tickets.pop(oldest, None)
        ticket = _token_bytes()
        self._tickets[ticket] = time.monotonic()
        return ticket

    def _consume_ticket(self, presented: str) -> bool:
        """Redeem a ticket exactly once within its TTL.

        Args:
            presented: Candidate ticket value.

        Returns:
            True when the ticket was live and is now consumed.
        """
        now = time.monotonic()
        for ticket, issued_at in list(self._tickets.items()):
            if (now - issued_at) >= self.ticket_ttl_seconds:
                self._tickets.pop(ticket, None)
                continue
            if hmac.compare_digest(presented, ticket):
                self._tickets.pop(ticket, None)
                return True
        return False

    def rotate(self) -> str:
        """Mint a fresh token and reset the TTL clock.

        A rotation is a global logout: operator tokens and outstanding
        tickets are cleared with the primary token.

        Returns:
            The new hex token.
        """
        self.token = _token_bytes()
        self.issued_at = time.monotonic()
        self._operator_tokens.clear()
        self._tickets.clear()
        return self.token

    def expires_at_epoch(self) -> float:
        """Absolute expiry for clients.

        Returns:
            Unix timestamp after which the token stops working.
        """
        import time as _time

        return _time.time() + max(self.ttl_seconds - (time.monotonic() - self.issued_at), 0)

    def issue_session_cookie_kwargs(self, secure: bool | None = None) -> dict[str, Any]:
        """Keyword arguments for ``set_cookie`` installing the session.

        Args:
            secure: Force the ``Secure`` attribute; ``None`` auto-detects
                from the current request's scheme (HTTPS deployments get
                ``Secure`` without configuration).

        Returns:
            Cookie kwargs mirroring the estorides session policy.
        """
        if secure is None:
            try:
                secure = request.is_secure
            except RuntimeError:
                secure = False
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
