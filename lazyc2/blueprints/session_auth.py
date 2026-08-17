"""Session-based authentication gate for operator dashboard blueprints.

Some dashboard blueprints (tasks, addons, notes) were previously
protected only by the decoy IP check, so any request arriving from the
operator IP could read operator data without a login session. This
module closes that gap with a single reusable guard: every route on a
guarded blueprint requires an authenticated Flask-Login session, and
unauthenticated requests are redirected to the login page.

Implant-facing blueprints (beacons, phishing redirects, health APIs)
must NOT use this gate.
"""

from __future__ import annotations

from flask import Blueprint, redirect, url_for
from flask_login import current_user


def require_operator_session(
    blueprint: Blueprint,
    login_endpoint: str = "login",
) -> None:
    """Register a ``before_request`` guard on a blueprint.

    All routes on the guarded blueprint serve operator-only content, so
    the guard treats every method the same way. The per-view decoy and
    CSRF layers keep running after the session check.

    Args:
        blueprint: The Flask blueprint to protect.
        login_endpoint: Endpoint name the login redirect targets.
    """
    @blueprint.before_request
    def _guard():
        if current_user.is_authenticated:
            return None
        return redirect(url_for(login_endpoint))


__all__ = ["require_operator_session"]
