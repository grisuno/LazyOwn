"""Gym blueprint — Red Team Gym lab lifecycle for the dashboard.

Exposes the operator endpoints that launch, inspect and stop the
framework's training gyms (Metasploitable2, AD lab, Juice Shop, ...)
backed by :mod:`modules.lab_runtime`. The viz.js node graph reads
``/api/gym/nodes`` to draw every running gym as its own node, and the
node context menu drives ``/api/gym/stop`` so a gym can be torn down
with one click from the graph.

Every route requires an authenticated operator session and every
mutating route enforces the same CSRF policy as the rest of the C2
(the shared :class:`lazyc2.security.csrf.CSRFPolicy` instance is read
from ``app.config``), so this blueprint adds no new auth surface.
"""

from __future__ import annotations

import re
from functools import wraps

from flask import Blueprint, current_app, jsonify, request, session

from lazyc2.blueprints.session_auth import require_operator_session

gym_bp = Blueprint("gym", __name__)

require_operator_session(gym_bp)

_SCENARIO_RE = re.compile(r"^[a-z0-9][a-z0-9_-]{0,48}$")
GYM_NODE_PREFIX = "gym-"


def _csrf_guard(view):
    """Enforce the app-wide CSRF policy on one blueprint view.

    The shared policy instance is stashed in ``app.config`` by the main
    application module; when it is absent the view runs unwrapped so a
    misconfigured boot degrades instead of erroring.

    Args:
        view: The Flask view to wrap.

    Returns:
        The wrapped view.
    """

    @wraps(view)
    def wrapper(*args, **kwargs):
        policy = current_app.config.get("LAZYOWN_CSRF_POLICY")
        enabled_fn = current_app.config.get("LAZYOWN_CSRF_ENABLED_FN")
        if policy is None or enabled_fn is None or not enabled_fn():
            return view(*args, **kwargs)
        from lazyc2.security.csrf_flow import request_session_id

        session_id = request_session_id(policy, request, session)
        if not policy.check_request(session_id, request):
            return jsonify({"error": "csrf token missing or invalid"}), 403
        return view(*args, **kwargs)

    return wrapper


def _scenario_from_payload(data: object) -> str:
    """Return a validated scenario key from a JSON body, empty when invalid."""
    if not isinstance(data, dict):
        return ""
    scenario = str(data.get("scenario", "") or "").strip().lower()
    if not _SCENARIO_RE.match(scenario):
        return ""
    return scenario


def _scenario_allowed(scenario: str) -> bool:
    """Return whether the scenario exists in the lab catalogue."""
    try:
        from modules.lab_runtime import LAB_SCENARIOS

        return scenario in LAB_SCENARIOS
    except Exception:
        return False


def _scenario_row(name: str, info: dict) -> dict:
    """Return one viz-ready scenario row with live status."""
    running = False
    ip = ""
    container = ""
    try:
        from modules.lab_runtime import container_ip, container_name, running_containers

        name_full = container_name(name)
        container = name_full
        running = name_full in running_containers()
        if running:
            ip = container_ip(name_full)
    except Exception:
        running = False
    return {
        "scenario": name,
        "description": str(info.get("description", "")),
        "difficulty": str(info.get("difficulty", "")),
        "running": running,
        "container": container,
        "ip": ip,
        "ports": dict(info.get("ports", {}) or {}),
        "node_id": f"{GYM_NODE_PREFIX}{name}",
    }


@gym_bp.route("/api/gym/scenarios", methods=["GET"])
def api_gym_scenarios():
    """List every gym scenario with its live container status."""
    try:
        from modules.lab_runtime import LAB_SCENARIOS

        rows = [_scenario_row(name, info) for name, info in sorted(LAB_SCENARIOS.items())]
        return jsonify({"scenarios": rows}), 200
    except Exception:
        current_app.logger.exception("api_gym_scenarios failed")
        return jsonify({"error": "gym scenarios unavailable"}), 500


@gym_bp.route("/api/gym/nodes", methods=["GET"])
def api_gym_nodes():
    """Return the running gym nodes for the viz.js graph.

    Every running gym container becomes one node carrying its scenario,
    container IP and mapped ports, so the operator can auto_loop the gym
    IP straight from the graph.
    """
    try:
        from modules.lab_runtime import LAB_SCENARIOS, container_ip, container_name, running_containers

        running = set(running_containers())
        nodes = []
        for name, info in sorted(LAB_SCENARIOS.items()):
            name_full = container_name(name)
            if name_full not in running:
                continue
            nodes.append(
                {
                    "node_id": f"{GYM_NODE_PREFIX}{name}",
                    "scenario": name,
                    "ip": container_ip(name_full),
                    "description": str(info.get("description", "")),
                    "ports": dict(info.get("ports", {}) or {}),
                }
            )
        return jsonify({"nodes": nodes}), 200
    except Exception:
        current_app.logger.exception("api_gym_nodes failed")
        return jsonify({"error": "gym nodes unavailable"}), 500


@gym_bp.route("/api/gym/start", methods=["POST"])
@_csrf_guard
def api_gym_start():
    """Start one gym scenario container.

    Body: ``{"scenario": "metasploitable"}``. Returns the container IP
    and mapped ports so the dashboard can point the next auto_loop at
    the gym target.
    """
    try:
        scenario = _scenario_from_payload(request.get_json(silent=True))
        if not scenario or not _scenario_allowed(scenario):
            return jsonify({"error": "unknown scenario"}), 400
        from modules.lab_runtime import LAB_SCENARIOS, start

        result = dict(start(scenario) or {})
        if not result.get("success"):
            return (
                jsonify({"error": str(result.get("error", "gym start failed"))[:300]}),
                502,
            )
        row = _scenario_row(scenario, dict(LAB_SCENARIOS.get(scenario, {})))
        row.update({key: result[key] for key in ("success", "already", "container", "ip", "ports") if key in result})
        return jsonify(row), 201
    except Exception:
        current_app.logger.exception("api_gym_start failed")
        return jsonify({"error": "gym start failed"}), 500


@gym_bp.route("/api/gym/stop", methods=["POST"])
@_csrf_guard
def api_gym_stop():
    """Stop one gym scenario container.

    Body: ``{"scenario": "metasploitable"}`` or ``{"all": true}`` to
    tear down every running gym container.
    """
    try:
        data = request.get_json(silent=True) or {}
        if isinstance(data, dict) and bool(data.get("all")):
            from modules.lab_runtime import stop_all

            return jsonify(stop_all() or {"stopped": [], "failed": {}}), 200
        scenario = _scenario_from_payload(data)
        if not scenario or not _scenario_allowed(scenario):
            return jsonify({"error": "unknown scenario"}), 400
        from modules.lab_runtime import stop

        result = dict(stop(scenario) or {})
        status = 200 if result.get("success") else 409
        return jsonify(result), status
    except Exception:
        current_app.logger.exception("api_gym_stop failed")
        return jsonify({"error": "gym stop failed"}), 500


__all__ = ["GYM_NODE_PREFIX", "gym_bp"]
