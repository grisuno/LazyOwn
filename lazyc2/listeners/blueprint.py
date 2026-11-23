"""REST blueprint for C2 listener management.

Exposes the operator listener CRUD API. Every route requires operator
authentication; the manager handle is read from
``current_app.config["listener_manager"]`` so the blueprint never imports
the monolith.
"""

from __future__ import annotations

from flask import Blueprint, current_app, jsonify, request

from lazyc2.security.auth import requires_auth

listeners_bp = Blueprint("listeners", __name__)


def _manager():
    """Return the listener manager bound to the running app."""
    return current_app.config["listener_manager"]


@listeners_bp.route("/api/listeners", methods=["GET"])
@requires_auth
def api_listeners():
    """List all configured C2 listeners and their runtime status."""
    return jsonify({"listeners": _manager().status()})


@listeners_bp.route("/api/listeners", methods=["POST"])
@requires_auth
def api_listeners_create():
    """Create a new listener."""
    data = request.get_json(silent=True) or {}
    port = data.get("port")
    if not port or not isinstance(port, int):
        return jsonify({"status": "error", "message": "port (int) is required"}), 400
    ssl_flag = data.get("ssl", False)
    listener_id = data.get("id")
    listener = _manager().add(port=port, ssl=ssl_flag, listener_id=listener_id)
    if data.get("start", True):
        _manager().start(listener.id)
    return jsonify({"status": "ok", "listener": listener.to_dict()})


@listeners_bp.route("/api/listeners/<listener_id>/start", methods=["POST"])
@requires_auth
def api_listeners_start(listener_id):
    """Start an existing listener."""
    ok = _manager().start(listener_id)
    return jsonify({"status": "ok" if ok else "error"})


@listeners_bp.route("/api/listeners/<listener_id>/stop", methods=["POST"])
@requires_auth
def api_listeners_stop(listener_id):
    """Stop a running listener."""
    ok = _manager().stop(listener_id)
    return jsonify({"status": "ok" if ok else "error"})


@listeners_bp.route("/api/listeners/<listener_id>", methods=["DELETE"])
@requires_auth
def api_listeners_delete(listener_id):
    """Remove a listener configuration."""
    ok = _manager().remove(listener_id)
    return jsonify({"status": "ok" if ok else "error"})
