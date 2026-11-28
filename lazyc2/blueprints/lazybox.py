"""LazyBox blueprint — gym + gamification dashboard for the C2.

Serves the ``/lazybox`` page and its JSON API over the aggregation
contract in :mod:`modules.lazybox`. Every route requires an operator
session and every mutating route enforces the shared CSRF policy, so
this blueprint adds no new auth surface.
"""

from __future__ import annotations

from flask import Blueprint, jsonify, render_template, request

from lazyc2.blueprints.session_auth import require_operator_session
from lazyc2.security.csrf_flow import csrf_guard

lazybox_bp = Blueprint("lazybox", __name__)

require_operator_session(lazybox_bp)


@lazybox_bp.route("/lazybox", methods=["GET"])
def lazybox_page():
    """Render the LazyBox gym dashboard."""
    from modules.lazybox import BRAND

    return render_template("lazybox.html", brand=BRAND)


@lazybox_bp.route("/api/lazybox/catalogue", methods=["GET"])
def api_lazybox_catalogue():
    """Return the LazyBox catalogue snapshot."""
    from modules.lazybox import catalogue

    return jsonify(catalogue()), 200


@lazybox_bp.route("/api/lazybox/intel/<challenge_id>", methods=["GET"])
def api_lazybox_intel(challenge_id: str):
    """Return the intelligence cross for one challenge."""
    from modules.lazybox import challenge_intel

    result = challenge_intel(challenge_id)
    status = 200 if result.get("success") else 404
    return jsonify(result), status


@lazybox_bp.route("/api/lazybox/scoreboard", methods=["GET"])
def api_lazybox_scoreboard():
    """Return the gym leaderboard plus operator gamification state."""
    from modules.lazybox import scoreboard

    return jsonify(scoreboard()), 200


@lazybox_bp.route("/api/lazybox/challenge/start", methods=["POST"])
@csrf_guard
def api_lazybox_start():
    """Launch one gym challenge.

    Body: ``{"challenge_id": "first_blood_smb", "target": "", "spin_lab": true}``.
    """
    from modules.lazybox import start_challenge

    data = request.get_json(silent=True) or {}
    challenge_id = str(data.get("challenge_id", "") or "").strip()
    if not challenge_id:
        return jsonify({"error": "challenge_id required"}), 400
    target = str(data.get("target", "") or "").strip()
    spin_lab = bool(data.get("spin_lab", True))
    result = start_challenge(challenge_id, target=target, spin_lab=spin_lab)
    status = 201 if result.get("success") else 409
    return jsonify(result), status


@lazybox_bp.route("/api/lazybox/challenge/submit", methods=["POST"])
@csrf_guard
def api_lazybox_submit():
    """Submit one completed challenge for scoring.

    Body: ``{"techniques_used": ["T1110"], "success": true, "run_id": ""}``.
    """
    from modules.lazybox import submit_challenge

    data = request.get_json(silent=True) or {}
    techniques = data.get("techniques_used")
    if not isinstance(techniques, list):
        techniques = []
    result = submit_challenge(
        techniques_used=[str(t) for t in techniques],
        success=bool(data.get("success", True)),
        run_id=str(data.get("run_id", "") or ""),
    )
    status = 200 if result.get("success") else 409
    return jsonify(result), status


@lazybox_bp.route("/api/lazybox/challenge/stop", methods=["POST"])
@csrf_guard
def api_lazybox_stop():
    """Stop gym runs. Body: ``{"selector": "challenge_id|run_id|gym_name"}``."""
    from modules.lazybox import stop_challenges

    data = request.get_json(silent=True) or {}
    selector = str(data.get("selector", "") or "").strip()
    result = stop_challenges(selector)
    status = 200 if result.get("success") else 409
    return jsonify(result), status


__all__ = ["lazybox_bp"]
