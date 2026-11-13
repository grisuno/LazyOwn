"""End-to-end CSRF token flow for the LazyOwn C2 web layer.

Contract: this module wires :class:`lazyc2.security.csrf.CSRFPolicy` into a
Flask application so every authenticated browser session receives a token
and every mutating request must echo it back. Non-browser clients (the CLI
driving the C2 over HTTP Basic) are exempt because a cross-site page cannot
attach the operator's Basic credentials.

Flow:

1. ``before_request`` primes a stable per-session key inside the signed
   Flask session and issues (or reuses) the token bound to that key.
2. ``after_request`` attaches two cookies: the policy cookie (session key,
   read back server-side by the gate, ``HttpOnly``) and a readable token
   cookie the browser JavaScript echoes as the policy header. Both carry
   ``Secure`` whenever ``secure_fn()`` reports TLS (or the request itself
   arrived over HTTPS), and ``SameSite=Strict`` always.
3. A context processor exposes the token to templates for hidden form
   fields (``<input type="hidden" name="xsrf_token" value="{{ csrf_token }}">``).

The pure token policy stays in :mod:`lazyc2.security.csrf`; only Flask
wiring lives here.
"""

from __future__ import annotations

import secrets
from collections.abc import Callable
from functools import wraps
from typing import Any

from flask import Flask, Request, g, jsonify, request, session
from flask_login import current_user

from lazyc2.security.csrf import CSRFPolicy

SESSION_KEY = "csrf_key"
_TOKEN_COOKIE = "LAZY_CSRF_TOKEN"
_HEADER_FALLBACK = "X-Session-Id"


def ensure_session_key(session: dict[str, Any]) -> str:
    """Return the per-session CSRF key, creating it on first use.

    Args:
        session: Flask session mapping.

    Returns:
        A stable per-session key indexing the token store.
    """
    key = session.get(SESSION_KEY)
    if not key:
        key = secrets.token_urlsafe(16)
        session[SESSION_KEY] = key
    return str(key)


def request_session_id(policy: CSRFPolicy, request: Request, session: dict[str, Any]) -> str:
    """Derive the token-store key for the incoming request.

    Lookup order: the policy cookie (sent automatically by the browser),
    the Flask session key, then the legacy ``X-Session-Id`` header.

    Args:
        policy: Active :class:`~lazyc2.security.csrf.CSRFPolicy`.
        request: Flask request.
        session: Flask session mapping.

    Returns:
        The session id string (possibly empty).
    """
    cookie_value = request.cookies.get(policy.cookie_name)
    if cookie_value:
        return cookie_value
    session_key = session.get(SESSION_KEY)
    if session_key:
        return str(session_key)
    return request.headers.get(_HEADER_FALLBACK, "")


def make_csrf_protect(
    policy: CSRFPolicy,
    enabled_fn: Callable[[], bool],
    basic_authenticated_fn: Callable[[], bool] | None = None,
) -> Callable[..., Any]:
    """Build the ``csrf_protect`` decorator bound to ``policy``.

    Args:
        policy: Active :class:`~lazyc2.security.csrf.CSRFPolicy`.
        enabled_fn: Callable returning whether the gate is enabled.
        basic_authenticated_fn: Callable returning ``True`` when the
            request already authenticated over HTTP Basic. Non-browser
            channels are exempt from CSRF.

    Returns:
        A decorator enforcing the per-session CSRF token on mutations.
    """

    def csrf_protect(view):
        @wraps(view)
        def wrapper(*args, **kwargs):
            if not enabled_fn():
                return view(*args, **kwargs)
            if basic_authenticated_fn is not None and basic_authenticated_fn():
                return view(*args, **kwargs)
            session_id = request_session_id(policy, request, session)
            if not policy.check_request(session_id, request):
                return jsonify({"error": "csrf token missing or invalid"}), 403
            return view(*args, **kwargs)

        return wrapper

    return csrf_protect


def register_csrf_flow(
    app: Flask,
    policy: CSRFPolicy,
    enabled_fn: Callable[[], bool],
    secure_fn: Callable[[], bool] | None = None,
) -> None:
    """Wire token issuance, delivery cookies and template globals.

    Args:
        app: Flask application.
        policy: Active :class:`~lazyc2.security.csrf.CSRFPolicy`.
        enabled_fn: Callable returning whether the gate is enabled.
        secure_fn: Optional callable reporting whether the listener runs
            with TLS. When it returns True (or the request itself arrived
            over HTTPS), both CSRF cookies carry the ``Secure`` flag.
            Defaults to per-request ``request.is_secure`` detection.

    Returns:
        None.
    """

    def _cookie_secure() -> bool:
        """Return True when CSRF cookies must carry the Secure flag."""
        try:
            if secure_fn is not None and secure_fn():
                return True
        except Exception:
            pass
        return bool(request.is_secure)

    @app.before_request
    def _prepare_csrf_token():
        g.csrf_token = ""
        if not enabled_fn():
            return None
        if not getattr(current_user, "is_authenticated", False):
            return None
        if policy.is_exempt(request.path):
            return None
        key = ensure_session_key(session)
        g.csrf_key = key
        g.csrf_token = policy.issue(key)
        return None

    @app.after_request
    def _attach_csrf_cookies(response):
        key = getattr(g, "csrf_key", "")
        token = getattr(g, "csrf_token", "")
        secure = _cookie_secure()
        if key:
            # Session-key cookie: server-side index only, never read by JS.
            response.set_cookie(
                policy.cookie_name,
                key,
                httponly=True,
                secure=secure,
                samesite="Strict",
                path="/",
            )
        if token:
            # Token cookie: intentionally JS-readable (double-submit echo).
            response.set_cookie(
                _TOKEN_COOKIE,
                token,
                httponly=False,
                secure=secure,
                samesite="Strict",
                path="/",
            )
        return response

    @app.context_processor
    def _inject_csrf_token():
        return {"csrf_token": getattr(g, "csrf_token", "")}


def token_cookie_name() -> str:
    """Return the readable cookie name carrying the CSRF token."""
    return _TOKEN_COOKIE


__all__ = [
    "SESSION_KEY",
    "ensure_session_key",
    "make_csrf_protect",
    "register_csrf_flow",
    "request_session_id",
    "token_cookie_name",
]
