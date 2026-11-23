"""Authentication primitives for the C2 operator surface.

Single home for Basic-auth verification and the route decorators shared by
the monolith routes and the extracted blueprints. Boot credentials live in
module state set at startup via :func:`set_boot_credentials`; the RBAC
store is consulted first when available and the boot pair is the fallback.
"""

from __future__ import annotations

import hmac
import logging
from functools import wraps

from flask import Response, request
from flask_login import current_user

_log = logging.getLogger(__name__)

_BOOT_USERNAME = ""
_BOOT_PASSWORD = ""

_RBAC_MODULE = None
_RBAC_CHECKED = False


def set_boot_credentials(username: str, password: str) -> None:
    """Store the boot operator pair used as the Basic-auth fallback.

    Args:
        username: Operator username resolved at boot.
        password: Operator password resolved at boot.
    """
    global _BOOT_USERNAME, _BOOT_PASSWORD
    _BOOT_USERNAME = str(username or "")
    _BOOT_PASSWORD = str(password or "")


def boot_credentials() -> tuple[str, str]:
    """Return the stored boot operator pair."""
    return _BOOT_USERNAME, _BOOT_PASSWORD


def _rbac():
    """Return the lazy RBAC module when importable, else None."""
    global _RBAC_MODULE, _RBAC_CHECKED
    if not _RBAC_CHECKED:
        _RBAC_CHECKED = True
        try:
            from modules import lazy_rbac as _module

            _RBAC_MODULE = _module
        except ImportError:
            _log.warning("[rbac] lazy_rbac.py not available; RBAC disabled")
    return _RBAC_MODULE


def _matches_boot(username: str, password: str) -> bool:
    """Time-safe compare of the request pair against the boot pair."""
    return hmac.compare_digest(username, _BOOT_USERNAME) and hmac.compare_digest(password, _BOOT_PASSWORD)


def check_auth(username: str, password: str) -> bool:
    """Verify credentials. Checks the RBAC store first, falls back to boot creds.

    Args:
        username: Supplied operator username.
        password: Supplied operator password.

    Returns:
        True when the pair authenticates.
    """
    if not username or not password:
        return False
    module = _rbac()
    if module is not None:
        try:
            from werkzeug.security import check_password_hash

            store = module.get_rbac_store()
            user = store.find_by_username(username)
            if user and check_password_hash(user.password_hash, password):
                return True
        except Exception as exc:
            _log.debug("[auth] rbac lookup failed: %s", exc)
    return _matches_boot(username, password)


def authenticate():
    """Build the Basic-auth challenge response."""
    return Response(
        "Invalid credentials. Please provide valid username and password.\n",
        401,
        {"WWW-Authenticate": 'Basic realm="Login Required"'},
    )


def requires_auth_or_session(f):
    """Require Basic auth credentials or a valid Flask-Login session.

    Used on endpoints driven both by the CLI (HTTP Basic credentials) and
    by the GUI dashboard where the operator already authenticated through
    ``/login``. Either channel satisfies the gate.
    """

    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if auth and check_auth(auth.username, auth.password):
            return f(*args, **kwargs)
        if current_user.is_authenticated:
            return f(*args, **kwargs)
        return authenticate()

    return decorated


def requires_auth(f):
    """Require valid HTTP Basic credentials."""

    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)

    return decorated


__all__ = [
    "authenticate",
    "boot_credentials",
    "check_auth",
    "requires_auth",
    "requires_auth_or_session",
    "set_boot_credentials",
]
