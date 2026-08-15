"""API blueprint for the LazyOwn C2 server.

Provides REST endpoints for health checks, command execution, output
retrieval, and dashboard data. Registered under the ``/api`` prefix.

Every endpoint that mutates state or reads sensitive data requires
tenant-bound API authorization via ``core.api_authz.require_api_auth``.
"""

from __future__ import annotations


import time
from dataclasses import dataclass
from typing import Any

from flask import Blueprint, current_app, g, jsonify

api_bp = Blueprint("api", __name__, url_prefix="/api")


@dataclass
class HealthConfig:
    """Configuration for the health-check subsystem."""

    required_components: tuple[str, ...] = (
        "database",
        "listeners",
        "beacons",
    )
    degraded_threshold_beacons: int = 0


def _health_status(config: HealthConfig | None = None) -> dict[str, Any]:
    """Collect health metrics for all critical subsystems.

    Args:
        config: Optional health-check configuration.

    Returns:
        A dict with ``status``, ``timestamp``, ``uptime``, and
        per-component status entries.
    """
    if config is None:
        config = HealthConfig()

    started = getattr(current_app, "start_time", time.time())
    result: dict[str, Any] = {
        "status": "healthy",
        "timestamp": time.time(),
        "uptime_seconds": round(time.time() - started, 2),
        "components": {},
    }

    try:
        db = current_app.config.get("lazyown_db")
        if db is not None:
            db.conn.execute("SELECT 1")
            result["components"]["database"] = "ok"
        else:
            result["components"]["database"] = "unavailable"
    except Exception as exc:
        result["components"]["database"] = f"error: {exc}"

    beacon_count = 0
    try:
        lm = current_app.config.get("listener_manager")
        if lm is not None:
            listeners = getattr(lm, "listeners", {})
            result["components"]["listeners"] = {
                "count": len(listeners),
                "active": [n for n, l in listeners.items() if _listener_alive(l)],
            }
            beacon_count = getattr(lm, "beacon_count", 0)
            result["components"]["beacons"] = beacon_count
        else:
            result["components"]["listeners"] = "unavailable"
            result["components"]["beacons"] = "unavailable"
    except Exception as exc:
        result["components"]["listeners"] = f"error: {exc}"
        result["components"]["beacons"] = "unavailable"

    if beacon_count <= config.degraded_threshold_beacons:
        result["status"] = "degraded"

    for comp in config.required_components:
        comp_status = result["components"].get(comp, "unavailable")
        if isinstance(comp_status, str) and comp_status != "ok":
            result["status"] = "unhealthy"
            break

    return result


def _listener_alive(listener: Any) -> bool:
    """Check whether a listener instance is alive."""
    try:
        return getattr(listener, "is_alive", lambda: False)()
    except Exception:
        return False


@api_bp.route("/health", methods=["GET"])
def health():
    """Health-check endpoint returning subsystem status.

    Returns:
        200 with JSON containing status of database, listeners,
        beacons, uptime, and an overall ``status`` field
        (``healthy``, ``degraded``, or ``unhealthy``).
    """
    return jsonify(_health_status())


@api_bp.route("/ping", methods=["GET"])
def ping():
    """Lightweight liveness probe.

    Returns:
        200 with ``{"status": "ok"}``.
    """
    return jsonify({"status": "ok"})


def require_api_auth_with_store(view):
    """Protect a view with the app-scoped API key store.

    Resolves the store from the Flask app config at request time so the
    route stays decoupled from application construction order.

    Args:
        view: The Flask view function to protect.

    Returns:
        The view wrapped by :func:`core.api_authz.require_api_auth`.
    """
    from functools import wraps

    from core.api_authz import ApiAuthzConfig, ApiKeyStore, require_api_auth

    @wraps(view)
    def guarded(*args, **kwargs):
        store = current_app.config.get("lazyown_api_key_store")
        if store is None:
            store = ApiKeyStore(config=ApiAuthzConfig())
        return require_api_auth(store=store)(view)(*args, **kwargs)

    return guarded


@api_bp.route("/health/tenant", methods=["GET"])
@require_api_auth_with_store
def health_tenant():
    """Health-check scoped to the current authenticated tenant.

    Requires a valid API key bound to a tenant. Returns tenant-scoped
    metrics in addition to the standard health data.

    Returns:
        200 with health data plus ``tenant_id`` and tenant-scoped
        beacon/listener counts. 401 when the API key is missing or
        invalid, 403 when the key is not tenant-scoped.
    """
    tenant_id = getattr(g, "api_tenant_id", "unknown")
    base = _health_status()
    base["tenant_id"] = tenant_id
    return jsonify(base)
