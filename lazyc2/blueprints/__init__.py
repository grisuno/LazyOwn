"""Flask Blueprints for the LazyOwn C2.

Each blueprint owns a domain area of the C2 web interface. The
``register_blueprints`` helper is the single registration home so both
boot paths (the ``lazyc2.py`` monolith and
:func:`lazyc2.app_factory.create_app`) mount the same surface and the
monolith keeps no registration boilerplate.
"""

from typing import Any

from flask import Flask

from lazyc2.blueprints.addons import addons_bp
from lazyc2.blueprints.api import api_bp
from lazyc2.blueprints.api_v1 import api_v1_bp
from lazyc2.blueprints.auth import auth_bp
from lazyc2.blueprints.campaign import campaign_bp
from lazyc2.blueprints.gym import gym_bp
from lazyc2.blueprints.lazybox import lazybox_bp
from lazyc2.blueprints.loops import init_loops_bp, loops_bp
from lazyc2.blueprints.operations import operations_bp
from lazyc2.blueprints.phishing import redirect_bp
from lazyc2.listeners import listeners_bp

_BLUEPRINTS = (
    operations_bp,
    auth_bp,
    redirect_bp,
    api_bp,
    addons_bp,
    gym_bp,
    lazybox_bp,
    campaign_bp,
    loops_bp,
)


def register_blueprints(
    app: Flask,
    *,
    limiter: Any = None,
    loops_guard: Any = None,
) -> list[str]:
    """Register every domain blueprint on one application.

    Args:
        app: The Flask application to mount onto.
        limiter: Optional rate limiter forwarded to ``init_loops_bp``.
        loops_guard: Optional ``(view, needs_csrf)`` wrapper used to
            initialise the loops blueprint auth/CSRF wiring; the
            monolith passes its own guard.

    Returns:
        The list of successfully registered blueprint names.
    """
    init_loops_bp(limiter, guard=loops_guard)
    registered: list[str] = []
    for blueprint in (*_BLUEPRINTS, listeners_bp):
        try:
            app.register_blueprint(blueprint)
            registered.append(blueprint.name)
        except Exception:
            continue
    return registered


__all__ = [
    "addons_bp",
    "api_bp",
    "api_v1_bp",
    "auth_bp",
    "campaign_bp",
    "gym_bp",
    "init_loops_bp",
    "lazybox_bp",
    "loops_bp",
    "operations_bp",
    "redirect_bp",
    "register_blueprints",
]
