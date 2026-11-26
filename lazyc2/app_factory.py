"""Flask application factory for the LazyOwn C2 server.

Consolidates app creation, security policy initialisation, extension wiring,
and blueprint registration. This factory is the canonical boot path: it mounts
the same blueprint surface as the frozen ``lazyc2.py`` monolith and keeps
security parity with it (CSRF flow, CORS allowlist, CSP header, stable secret
key, HTTPS redirect).

Usage::

    from lazyc2.app_factory import create_app
    app = create_app()
    app.run()
"""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

from flask import Flask
from flask import request as _flask_request
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_login import LoginManager
from flask_socketio import SocketIO

from lazyc2.blueprints import api_v1_bp, register_blueprints
from lazyc2.blueprints.orchestrator import orchestrator_bp
from lazyc2.extensions import short_urls as short_urls_ext
from lazyc2.security.constants import CONTENT_SECURITY_POLICY
from lazyc2.security.cors import CorsPolicy
from lazyc2.security.csrf import CSRFPolicy
from lazyc2.security.csrf_flow import register_csrf_flow
from lazyc2.security.https_redirect import HTTPSRedirect

_CSRF_EXEMPT_PATHS = ("/login", "/logout", "/register", "/api/beacon")


def _load_payload_config() -> dict[str, Any]:
    """Load ``payload.json`` and return its contents."""
    try:
        with open("payload.json") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def _build_api_key_store(payload: dict[str, Any]) -> object:
    """Build the tenant-scoped API key store from payload configuration.

    Args:
        payload: ``payload.json`` contents. ``api_keys_path`` overrides
            the default store location when present.

    Returns:
        A configured :class:`core.api_authz.ApiKeyStore`.
    """
    from core.api_authz import ApiAuthzConfig, ApiKeyStore

    config = ApiAuthzConfig()
    override = str(payload.get("api_keys_path") or "").strip()
    if override:
        config.api_keys_path = override
    return ApiKeyStore(config=config)


def _load_or_create_secret_key(sessions_dir: str = "sessions") -> str:
    """Resolve the Flask secret key from env or disk, failing closed.

    Args:
        sessions_dir: Directory holding the persisted key file.

    Returns:
        The hex-encoded secret key string.

    Raises:
        RuntimeError: when no ``LAZYOWN_SECRET_KEY`` is set and the
            persistent key manager cannot provide a key. A silently
            randomised key would invalidate sessions on every restart
            and hide a broken boot, so it is never used.
    """
    env_key = os.environ.get("LAZYOWN_SECRET_KEY")
    if env_key:
        return env_key
    from lazyc2.security.services import SecretKeyManager

    os.makedirs(sessions_dir, exist_ok=True)
    key = SecretKeyManager(Path(sessions_dir)).get_or_create()
    if not key:
        raise RuntimeError(
            f"no C2 secret key available: set LAZYOWN_SECRET_KEY or ensure {sessions_dir}/.secret_key is writable"
        )
    return key


def _tls_deployed(payload: dict[str, Any]) -> bool:
    """Return True when the listener is expected to serve TLS."""
    return bool(payload.get("c2_https_redirect", False)) or (os.path.isfile("cert.pem") and os.path.isfile("key.pem"))


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
    cfg.tls_deployed = _tls_deployed(payload)
    return cfg


def _build_cors_policy(payload: dict[str, Any]) -> CorsPolicy:
    """Build the shared CORS allowlist policy from payload settings.

    Args:
        payload: ``payload.json`` contents.

    Returns:
        A :class:`lazyc2.security.cors.CorsPolicy`. The wildcard origin is
        never permitted; the policy owns the single source of truth for
        web and Socket.IO origins.
    """
    return CorsPolicy(
        env=str(payload.get("env", "DEV") or "DEV").upper(),
        lhost=str(payload.get("lhost", "127.0.0.1") or "127.0.0.1"),
        allowed_origins=payload.get("c2_allowed_origins", "") or "",
        c2_port=int(payload.get("c2_port", 5000) or 5000),
    )


def _build_csrf_stack(payload: dict[str, Any]) -> tuple[CSRFPolicy, Any, Any]:
    """Build the CSRF policy plus its enable and secure callables.

    Args:
        payload: ``payload.json`` contents.

    Returns:
        ``(policy, enabled_fn, secure_fn)`` mirroring the monolith wiring.
    """
    policy = CSRFPolicy(exempt_paths=_CSRF_EXEMPT_PATHS)
    enabled = bool(payload.get("c2_csrf_enabled", True))

    def _enabled() -> bool:
        """Report whether the CSRF gate is switched on."""
        return enabled

    def _secure() -> bool:
        """Report whether the listener serves TLS."""
        return _tls_deployed(payload)

    return policy, _enabled, _secure


def create_app() -> Flask:
    """Create and return a fully configured C2 Flask application.

    Returns:
        A :class:`Flask` instance ready to run or serve via WSGI.
    """
    _root = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    app = Flask(__name__, static_folder="static", root_path=_root)

    payload = _load_payload_config()
    security = _make_security_config(payload)
    cors_policy = _build_cors_policy(payload)
    csrf_policy, csrf_enabled, csrf_secure = _build_csrf_stack(payload)
    https_redirect = HTTPSRedirect(
        env=str(payload.get("env", "DEV") or "DEV").upper(),
        enabled=bool(payload.get("c2_https_redirect", True)),
    )

    app.secret_key = security.secret_key
    app.config["SECRET_KEY"] = app.secret_key
    app.config["SESSION_COOKIE_SECURE"] = security.tls_deployed
    app.config["SESSION_COOKIE_HTTPONLY"] = True
    app.config["REMEMBER_COOKIE_SECURE"] = security.tls_deployed
    app.config["SESSION_COOKIE_SAMESITE"] = "Lax"
    app.config["PROPAGATE_EXCEPTIONS"] = False
    app.config["TRAP_HTTP_EXCEPTIONS"] = True
    app.config["fd"] = None
    app.config["child_pid"] = None

    register_csrf_flow(app, csrf_policy, csrf_enabled, secure_fn=csrf_secure)
    app.config["LAZYOWN_CSRF_POLICY"] = csrf_policy
    app.config["LAZYOWN_CSRF_ENABLED_FN"] = csrf_enabled

    upload_size = security.c2_max_upload_size_mb * 1024 * 1024
    app.config["MAX_CONTENT_LENGTH"] = upload_size
    app.config["UPLOAD_FOLDER"] = "sessions/uploads"

    limiter = Limiter(
        app=app,
        key_func=get_remote_address,
        default_limits=[security.c2_daily_limit, security.c2_hour_limit],
    )

    socketio = SocketIO(
        app,
        cors_allowed_origins=cors_policy.origins_for_socketio(),
        async_mode="threading",
        transports=["websocket"],
    )
    app.config["LAZYOWN_SOCKETIO"] = socketio

    login_manager = LoginManager(app)
    login_manager.login_view = "login"

    @login_manager.user_loader
    def _factory_load_user(user_id):
        """Resolve one RBAC user so the blueprint session auth works."""
        from flask_login import UserMixin

        class _FactoryUser(UserMixin):
            def __init__(self, data: dict) -> None:
                self.id = str(data.get("id", ""))
                self.username = str(data.get("username", ""))
                self.role = str(data.get("role", "operator"))

        try:
            from modules.lazy_rbac import get_rbac_store

            rbac_user = get_rbac_store().find_by_id(int(user_id))
        except Exception:
            return None
        return _FactoryUser(rbac_user.to_dict()) if rbac_user else None

    app.config["_security_config"] = security
    app.config["SESSIONS_DIR"] = "sessions"
    app.config["DB_PATH"] = "sessions/c2.db"
    app.config["ALLOWED_EXTENSIONS"] = {"txt", "enc", "exe"}
    app.config["lazyown_api_key_store"] = _build_api_key_store(payload)

    short_urls_ext.configure("sessions/phishing")

    register_blueprints(app, limiter=limiter)
    app.register_blueprint(orchestrator_bp)
    app.register_blueprint(api_v1_bp, url_prefix="/api/v1")

    @app.before_request
    def _enforce_https_redirect():
        """Force HTTP -> HTTPS when the policy says so."""
        return https_redirect.evaluate(_flask_request)

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

    @app.after_request
    def _add_security_headers(response):
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "SAMEORIGIN"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["Content-Security-Policy"] = CONTENT_SECURITY_POLICY
        return response

    return app
