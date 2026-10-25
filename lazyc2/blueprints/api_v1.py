"""Versioned REST API (``/api/v1``) for the LazyOwn C2 server.

Programmatic interface for SIEM/SOAR integration, custom dashboards, and
CI/CD pipelines. Every endpoint except ``/health`` requires a tenant-bound
API key (``X-API-Key`` header, see ``core.api_authz``).

Endpoints:

- ``GET /api/v1/health`` — public service status.
- ``GET /api/v1/targets`` — hosts in scope from the campaign database.
- ``GET /api/v1/results`` — beacon task results, optionally per client.
- ``GET /api/v1/campaigns`` — autonomous campaign/objective status.
- ``GET /api/v1/webhooks`` — registered result webhooks.
- ``POST /api/v1/webhooks`` — register a result webhook URL.
- ``DELETE /api/v1/webhooks/<index>`` — remove a registered webhook.
"""

from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any

from flask import Blueprint, current_app, jsonify, request

from lazyc2.blueprints.api import _health_status, require_api_auth_with_store

api_v1_bp = Blueprint("api_v1", __name__, url_prefix="/api/v1")

logger = logging.getLogger("lazyc2.blueprints.api_v1")

WEBHOOKS_FILE = "api_webhooks.json"
OBJECTIVES_FILE = "objectives.jsonl"
WORLD_MODEL_FILE = "world_model.json"


def _sessions_dir() -> Path:
    """Return the sessions directory configured on the Flask app."""
    return Path(current_app.config.get("SESSIONS_DIR", "sessions"))


def _db() -> Any | None:
    """Return a campaign database handle, or ``None`` when unavailable."""
    db = current_app.config.get("lazyown_db")
    if db is not None:
        return db
    try:
        from modules.db import LazyOwnDB
    except ImportError:
        return None
    db_path = current_app.config.get("DB_PATH", str(_sessions_dir() / "c2.db"))
    try:
        return LazyOwnDB(db_path)
    except Exception as exc:
        logger.warning("api v1: cannot open campaign database: %s", exc)
        return None


def _error(message: str, status: int) -> tuple[Any, int]:
    return jsonify({"error": message}), status


@api_v1_bp.route("/health", methods=["GET"])
def health() -> Any:
    """Public service status (same payload as ``/api/health``).

    Returns:
        200 with subsystem status, uptime, and an overall status field.
    """
    return jsonify(_health_status())


@api_v1_bp.route("/targets", methods=["GET"])
@require_api_auth_with_store
def targets() -> Any:
    """List in-scope hosts from the campaign database.

    Query args:
        workspace: Workspace name (default ``"default"``).

    Returns:
        200 with the workspace name and its hosts (each with services).
        503 when the campaign database is unavailable.
    """
    db = _db()
    if db is None:
        return _error("campaign database unavailable", 503)
    workspace_name = request.args.get("workspace", "default")
    try:
        workspace = db.workspace_get(workspace_name)
        if workspace is None:
            return jsonify({"workspace": workspace_name, "hosts": []})
        hosts = db.host_list(workspace["id"])
        for host in hosts:
            try:
                host["services"] = db.service_list(host["id"])
            except Exception:
                host["services"] = []
    except Exception as exc:
        logger.warning("api v1 targets failed: %s", exc)
        return _error("failed to read targets", 500)
    return jsonify({"workspace": workspace_name, "hosts": hosts})


@api_v1_bp.route("/results", methods=["GET"])
@require_api_auth_with_store
def results() -> Any:
    """Return beacon task results.

    Query args:
        client_id: When given, only that beacon's history. Otherwise the
            latest record per known beacon plus the client id list.

    Returns:
        200 with records (oldest first per beacon).
    """
    from modules.beacon_history import BeaconHistoryConfig, read_records

    sessions = _sessions_dir()
    config = BeaconHistoryConfig(base_dir=sessions.parent)
    client_id = request.args.get("client_id", "")
    if client_id:
        return jsonify({"client_id": client_id, "records": read_records(client_id, config)})
    known: list[str] = []
    try:
        for path in sorted(sessions.glob("*.records.jsonl")):
            known.append(path.name[: -len(".records.jsonl")])
    except OSError as exc:
        logger.warning("api v1 results listing failed: %s", exc)
    latest = []
    for known_id in known:
        records = read_records(known_id, config)
        if records:
            latest.append({"client_id": known_id, "record": records[-1]})
    return jsonify({"clients": known, "latest": latest})


@api_v1_bp.route("/campaigns", methods=["GET"])
@require_api_auth_with_store
def campaigns() -> Any:
    """Report autonomous campaign status from operational state files.

    Returns:
        200 with the current kill-chain phase (world model, when present)
        and pending objective counts. State files are best-effort: missing
        files yield empty sections, never errors.
    """
    sessions = _sessions_dir()
    phase: str | None = None
    try:
        world_model = json.loads((sessions / WORLD_MODEL_FILE).read_text(encoding="utf-8"))
        phase = world_model.get("phase") or world_model.get("current_phase")
    except (OSError, ValueError):
        phase = None
    pending = 0
    objectives_path = sessions / OBJECTIVES_FILE
    try:
        if objectives_path.is_file():
            pending = sum(1 for line in objectives_path.read_text(encoding="utf-8").splitlines() if line.strip())
    except OSError:
        pending = 0
    return jsonify({"phase": phase, "pending_objectives": pending})


def _webhooks_path() -> Path:
    return _sessions_dir() / WEBHOOKS_FILE


def _read_webhooks() -> list[dict[str, Any]]:
    try:
        data = json.loads(_webhooks_path().read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return []
    return data if isinstance(data, list) else []


@api_v1_bp.route("/webhooks", methods=["GET"])
@require_api_auth_with_store
def webhooks_list() -> Any:
    """List registered result webhooks.

    Returns:
        200 with the webhook list (URL + event filter each).
    """
    return jsonify({"webhooks": _read_webhooks()})


@api_v1_bp.route("/webhooks", methods=["POST"])
@require_api_auth_with_store
def webhooks_register() -> Any:
    """Register a result webhook URL.

    Body (JSON): ``{"url": "https://...", "events": ["results"]}``.
    The URL must be http(s); anything else is rejected.

    Returns:
        201 with the stored entry and its index. 400 on bad input.
    """
    from core.safe_exec import validate_url

    payload = request.get_json(silent=True) or {}
    url = payload.get("url", "")
    events = payload.get("events", ["results"])
    if not isinstance(url, str) or not url:
        return _error("field 'url' is required", 400)
    try:
        clean_url = validate_url(url)
    except (ValueError, PermissionError):
        return _error("url must be a valid http(s) URL", 400)
    if not isinstance(events, list) or not all(isinstance(e, str) for e in events):
        return _error("field 'events' must be a list of strings", 400)
    hooks = _read_webhooks()
    entry = {"url": clean_url, "events": events}
    hooks.append(entry)
    try:
        path = _webhooks_path()
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(hooks, indent=2), encoding="utf-8")
    except OSError as exc:
        logger.warning("api v1 webhook store failed: %s", exc)
        return _error("failed to store webhook", 500)
    return jsonify({"index": len(hooks) - 1, "webhook": entry}), 201


@api_v1_bp.route("/webhooks/<int:index>", methods=["DELETE"])
@require_api_auth_with_store
def webhooks_delete(index: int) -> Any:
    """Remove a registered webhook by index.

    Returns:
        200 with the removed entry. 404 when the index does not exist.
    """
    hooks = _read_webhooks()
    if index < 0 or index >= len(hooks):
        return _error("webhook index not found", 404)
    removed = hooks.pop(index)
    try:
        _webhooks_path().write_text(json.dumps(hooks, indent=2), encoding="utf-8")
    except OSError as exc:
        logger.warning("api v1 webhook delete failed: %s", exc)
        return _error("failed to store webhook", 500)
    return jsonify({"removed": removed})
