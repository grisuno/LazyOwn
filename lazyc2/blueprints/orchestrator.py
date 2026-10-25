"""Orchestrator REST + web panel for the LazyOwn C2 dashboard.

Exposes the autonomous-loop administration contract over HTTP so a
remote operator or the web panel sees the same truth as the shell and
the Textual console:

- ``GET /api/v1/orchestrator/status`` — world model, kill chain, verbs,
  triggers and stage view in one call;
- ``GET /api/v1/orchestrator/world`` — raw world model + kill chain;
- ``GET /api/v1/orchestrator/verbs`` — verb catalog with optional search;
- ``POST /api/v1/orchestrator/verbs/toggle`` — flip one catalog verb;
- ``POST /api/v1/orchestrator/stages/toggle`` — flip one loop stage;
- ``GET/POST /api/v1/orchestrator/triggers`` — list / add triggers;
- ``GET /api/v1/orchestrator/triggers/seed`` — re-merge the YAML seeds;
- ``DELETE /api/v1/orchestrator/triggers/<id>`` — remove one trigger.

X-API-Key guards every route (same store as the rest of ``/api/v1``).
The panel route reuses the dashboard session login instead.

Design (SOLID): Single Responsibility — HTTP adaptation only, no domain
logic; Open/Closed — new layers append one helper; Dependency Inversion
— domain contracts are imported lazily at call time so partial installs
degrade to JSON errors instead of crashing the whole service.
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any

from flask import Blueprint, current_app, jsonify, render_template, request

from lazyc2.blueprints.api import require_api_auth_with_store

try:
    from flask_login import current_user, login_required
except ImportError:  # pragma: no cover - scaled-down installs
    current_user = None
    login_required = Any

orchestrator_bp = Blueprint(
    "orchestrator",
    __name__,
    url_prefix="/api/v1/orchestrator",
    template_folder="../templates",
)

logger = logging.getLogger("lazyc2.blueprints.orchestrator")

_TOGGLE_NAME_MAX = 64

BODY_NAME_REQUIRED = "verb name required"


def _error(message: str, status: int) -> tuple[Any, int]:
    """Build the standard JSON error tuple."""
    return jsonify({"error": message}), status


def _namespaced_path(name: str) -> Path:
    """Return ``name`` relative to the sandboxed sessions directory."""
    return Path(current_app.config.get("SESSIONS_DIR", "sessions")) / name


def _world_snapshot() -> dict[str, Any]:
    """Collect the world model + kill chain snapshot in a safe dict."""
    world: dict[str, Any] = {}
    try:
        from modules import world_model as world_model_module
        from modules.world_model import get_world_model

        hosts = dict(get_world_model().get_hosts_summary())
        model = get_world_model()
        world = {
            "hosts": [
                {"ip": ip, "state": str(getattr(state, "value", state))} for ip, state in hosts.items()
            ],
            "phase": str(getattr(model.get_phase(), "value", model.get_phase())),
            "vault_path": str(world_model_module._DEFAULT_PATH),
        }
    except Exception as exc:
        logger.debug("orchestrator world snapshot failed: %s", exc)
        world = {"error": "world model unavailable"}
    return world


def _status_payload() -> dict[str, Any]:
    """Wire the status sections through lazy domain imports."""
    from modules import trigger_policy
    from modules.orchestrator_config import stages
    from modules.verb_catalog import stats

    return {
        "world": _world_snapshot(),
        "verbs": stats(),
        "triggers": trigger_policy.export_store(),
        "stage_names": sorted(stages()),
    }


@orchestrator_bp.route("/status", methods=["GET"])
@require_api_auth_with_store
def status():  # noqa: A001 - Flask route name
    """One-call awareness: world model, verbs, triggers and stages."""
    return jsonify(_status_payload())


@orchestrator_bp.route("/world", methods=["GET"])
@require_api_auth_with_store
def world():  # noqa: A001 - Flask route name
    """Return the raw world-model + kill chain snapshot."""
    live = _world_snapshot()
    try:
        from modules.killchain import KillChain

        live["killchain"] = KillChain.current_phase()
    except Exception as exc:
        logger.debug("killchain snapshot failed: %s", exc)
    return jsonify(live)


@orchestrator_bp.route("/verbs", methods=["GET"])
@require_api_auth_with_store
def verbs():  # noqa: A001 - Flask route name
    """Verb catalog view with optional search filtering."""
    from modules.verb_catalog import entries, search

    query = str(request.args.get("query") or "").strip()
    if query:
        rows = search(query.replace("do_", ""), limit=50)
    else:
        rows = list(entries().values())[:200]
    state = str(request.args.get("state") or "").strip()
    if state in ("on", "off"):
        wanted = state == "on"
        rows = [row for row in rows if bool(row["enabled"]) == wanted]
    return jsonify({"verbs": rows})


def _read_body_name() -> str:
    """Extract and validate the toggle body payload."""
    data = request.get_json(silent=True) or {}
    return str(data.get("name") or "").strip()[:_TOGGLE_NAME_MAX]


@orchestrator_bp.route("/verbs/toggle", methods=["POST"])
@require_api_auth_with_store
def verbs_toggle():  # noqa: A001 - Flask route name
    """Flip one loop verb between enabled and disabled."""
    from modules import verb_catalog

    name = _read_body_name()
    if not name:
        return _error(BODY_NAME_REQUIRED, 400)
    current = verb_catalog.catalog_enabled(name)
    if not isinstance(current, bool):
        return _error("unknown shell command", 404)
    entry = verb_catalog.set_enabled(name, not current)
    entry["name"] = name
    return jsonify(entry)


@orchestrator_bp.route("/stages/toggle", methods=["POST"])
@require_api_auth_with_store
def stages_toggle():  # noqa: A001 - Flask route name
    """Flip one autonomous-loop stage between enabled and disabled."""
    from modules.orchestrator_config import set_stage, stage_enabled

    name = _read_body_name()
    if not name:
        return _error("stage name required", 400)
    if stage_enabled(name) is None or name not in stage_names():
        return _error("unknown stage", 404)
    before = stage_enabled(name)
    set_stage(name, not before)
    return jsonify({"name": name, "enabled": not before})


def stage_names() -> set[str]:
    """Return the known stage names (fallback builtins included)."""
    from modules.orchestrator_config import FALLBACK_STAGES, stages

    try:
        known = set(stages())
    except Exception:
        known = {}
    return set(known) | set(FALLBACK_STAGES)


@orchestrator_bp.route("/triggers", methods=["GET"])
@require_api_auth_with_store
def triggers():  # noqa: A001 - Flask route name
    """List the scheduler triggers pinned in the store."""
    from modules import trigger_policy

    return jsonify({"triggers": trigger_policy.export_store()})


@orchestrator_bp.route("/triggers", methods=["POST"])
@require_api_auth_with_store
def triggers_add():  # noqa: A001 - Flask route name
    """Register one scheduler trigger from the JSON body."""
    from modules.loop_triggers import TRIGGER_KINDS, TriggerStore
    from modules.trigger_policy import TRIGGER_POLICY

    data = request.get_json(silent=True) or {}
    kind = str(data.get("kind") or "").strip()
    arg = str(data.get("arg") or "")[: TRIGGER_POLICY.arg_max_chars]
    try:
        every = float(data.get("every_sec", 0.0) or 0.0)
    except (TypeError, ValueError):
        return _error("every_sec must be numeric", 400)
    if kind not in TRIGGER_KINDS:
        return _error(f"kind must be one of {TRIGGER_KINDS}", 400)
    item = TriggerStore("").add(kind, arg=arg, every_sec=every)
    return jsonify(item)


@orchestrator_bp.route("/triggers/seed", methods=["GET"])
@require_api_auth_with_store
def triggers_seed():  # noqa: A001 - Flask route name
    """Re-merge the declarative YAML seeds into the store once."""
    from modules import trigger_policy

    return jsonify(trigger_policy.seed_store())


@orchestrator_bp.route("/triggers/<int:trigger_id>", methods=["DELETE"])
@require_api_auth_with_store
def triggers_delete(trigger_id: int):  # noqa: A001 - Flask route name
    """Remove one scheduler trigger by id."""
    from modules.loop_triggers import TriggerStore

    if not TriggerStore("").remove(trigger_id):
        return _error("unknown trigger", 404)
    return jsonify({"removed": trigger_id})


@orchestrator_bp.route("/panel", methods=["GET"])
@login_required
def panel():  # noqa: A001 - Flask route name
    """Dashboard panel mirroring the orchestrator console state."""
    try:
        from modules import trigger_policy
        from modules.verb_catalog import stats

        payload = {
            "verbs": stats(),
            "triggers": trigger_policy.export_store(),
            "world": _world_snapshot(),
            "user": str(getattr(current_user, "username", "")),
        }
    except Exception as exc:
        logger.debug("panel render failed: %s", exc)
        payload = {"error": "orchestrator state unavailable"}
    return render_template("orchestrator_panel.html", **payload)


@orchestrator_bp.route("/panel.json", methods=["GET"])
@require_api_auth_with_store
def panel_json():  # noqa: A001 - Flask route name
    """JSON mirror of the panel payload for automation."""
    from modules import trigger_policy
    from modules.verb_catalog import stats

    return jsonify(
        {
            "verbs": stats(),
            "triggers": trigger_policy.export_store(),
            "world": _world_snapshot(),
        }
    )
