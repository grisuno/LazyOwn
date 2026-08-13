"""Flask application factory for the LazyOwn C2 server.

Consolidates app creation, security policy initialisation, extension wiring,
and blueprint registration. Call :func:`create_app` to get a fully-wired
:class:`Flask` instance instead of relying on the monolithic ``lazyc2.py``
module-level globals.

Usage::

    from lazyc2.app_factory import create_app
    app = create_app()
    app.run()
"""

from __future__ import annotations

import json
import os
import uuid
from pathlib import Path
from typing import Any

from flask import Flask
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_login import LoginManager
from flask_socketio import SocketIO

from lazyc2.blueprints import api_bp, redirect_bp
from lazyc2.extensions import short_urls as short_urls_ext


def _load_payload_config() -> dict[str, Any]:
    """Load ``payload.json`` and return its contents."""
    try:
        with open("payload.json") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def _load_or_create_secret_key(sessions_dir: str = "sessions") -> str:
    """Resolve the Flask secret key from env or disk."""
    env_key = os.environ.get("LAZYOWN_SECRET_KEY")
    if env_key:
        return env_key
    try:
        from lazyc2.security.services import SecretKeyManager
        os.makedirs(sessions_dir, exist_ok=True)
        return SecretKeyManager(Path(sessions_dir)).get_or_create()
    except Exception:
        return uuid.uuid4().hex


def _make_security_config(payload: dict[str, Any]) -> object:
    """Build a simple namespace-style config object from payload settings."""
    from types import SimpleNamespace

    cfg = SimpleNamespace()
    cfg.enable_c2_debug = payload.get("enable_c2_debug", False)
    cfg.generic_command_error_message = "An error occurred"
    cfg.c2_daily_limit = payload.get("c2_daily_limit", "1000 per day")
    cfg.c2_hour_limit = payload.get("c2_hour_limit", "200 per hour")
    cfg.c2_max_upload_size_mb = int(payload.get("c2_max_upload_size_mb", 10) or 10)
    cfg.secret_key = _load_or_create_secret_key()
    return cfg


def create_app() -> Flask:
    """Create and return a fully configured C2 Flask application.

    Returns:
        A :class:`Flask` instance ready to run or serve via WSGI.
    """
    _root = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    app = Flask(__name__, static_folder="static", root_path=_root)

    payload = _load_payload_config()
    security = _make_security_config(payload)

    app.secret_key = security.secret_key + str(uuid.uuid4())
    app.config["SECRET_KEY"] = app.secret_key
    app.config["SESSION_COOKIE_SECURE"] = True
    app.config["SESSION_COOKIE_HTTPONLY"] = True
    app.config["REMEMBER_COOKIE_SECURE"] = True
    app.config["SESSION_COOKIE_SAMESITE"] = "Lax"
    app.config["PROPAGATE_EXCEPTIONS"] = False
    app.config["TRAP_HTTP_EXCEPTIONS"] = True
    app.config["fd"] = None
    app.config["child_pid"] = None

    upload_size = security.c2_max_upload_size_mb * 1024 * 1024
    app.config["MAX_CONTENT_LENGTH"] = upload_size
    app.config["UPLOAD_FOLDER"] = "sessions/uploads"

    # Rate limiter
    limiter = Limiter(
        app=app,
        key_func=get_remote_address,
        default_limits=[security.c2_daily_limit, security.c2_hour_limit],
    )

    # SocketIO
    socketio = SocketIO(
        app,
        cors_allowed_origins="*",
        async_mode="threading",
        transports=["websocket"],
    )

    # Login manager
    login_manager = LoginManager(app)
    login_manager.login_view = "login"

    # ── Shared config for blueprints ──────────────────────────────────────
    app.config["_security_config"] = security
    app.config["SESSIONS_DIR"] = "sessions"
    app.config["DB_PATH"] = "sessions/c2.db"
    app.config["ALLOWED_EXTENSIONS"] = {"txt", "enc", "exe"}

    # ── Extensions ────────────────────────────────────────────────────────
    short_urls_ext.configure("sessions/phishing")

    # ── Blueprints ────────────────────────────────────────────────────────
    app.register_blueprint(api_bp, url_prefix="/api")
    app.register_blueprint(redirect_bp)

    # ── Error handlers ────────────────────────────────────────────────────
    @app.errorhandler(404)
    def _handle_404(_error):
        return {"error": "not found"}, 404

    @app.errorhandler(405)
    def _handle_405(_error):
        return {"error": "method not allowed"}, 405

    @app.errorhandler(Exception)
    def _handle_exception(error):
        if getattr(security, "enable_c2_debug", False):
            app.logger.exception("[c2] unhandled exception: %s", error)
        return {"error": "internal server error"}, 500

    # ── Security headers ──────────────────────────────────────────────────
    @app.after_request
    def _add_security_headers(response):
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "SAMEORIGIN"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        return response

    return app
