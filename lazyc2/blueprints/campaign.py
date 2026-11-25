"""Campaign Explorer blueprint — navigable index over ``sessions/``.

Serves the ``/campaign`` page and its JSON API over the read-only
:mod:`modules.session_index` contract. Every route requires an operator
session, every artefact path is resolved through
:meth:`modules.session_index.SessionIndex.resolve_safe` (fail-closed on
traversal), and the file viewer answers ``text/plain`` so loot is never
rendered as markup. The view never writes: actions are left to the
operator shell and the scope guard.
"""

from __future__ import annotations

import json

from flask import Blueprint, Response, abort, current_app, jsonify, render_template, request

from lazyc2.blueprints.session_auth import require_operator_session

campaign_bp = Blueprint("campaign", __name__)

require_operator_session(campaign_bp)

DEFAULT_QUERY_LIMIT = 100


def _payload_entries() -> list[str]:
    """Return the authorized scope entries from ``payload.json``."""
    try:
        with open("payload.json", encoding="utf-8") as fh:
            payload = json.load(fh)
    except (OSError, json.JSONDecodeError):
        return []
    entries = payload.get("scope")
    if isinstance(entries, list):
        return [str(entry) for entry in entries if str(entry).strip()]
    return []


def _campaign_label() -> str:
    """Return the campaign label shown in the header."""
    try:
        with open("payload.json", encoding="utf-8") as fh:
            payload = json.load(fh)
    except (OSError, json.JSONDecodeError):
        return ""
    return str(payload.get("domain") or payload.get("rhost") or "campaign")


def _index():
    """Build the session index bound to the configured sessions root."""
    from modules.session_index import SessionIndex

    return SessionIndex(current_app.config.get("SESSIONS_DIR", "sessions"))


@campaign_bp.route("/campaign", methods=["GET"])
def campaign_page():
    """Render the Campaign Explorer page."""
    return render_template("campaign.html", campaign=_campaign_label())


@campaign_bp.route("/api/campaign/overview", methods=["GET"])
def api_overview():
    """Return the full campaign snapshot: host cards, frontier, totals."""
    from cli.scope_guard import target_in_scope

    entries = _payload_entries()
    data = _index().overview(lambda target: target_in_scope(target, entries))
    data["campaign"] = _campaign_label()
    data["scope"] = {"entries": entries}
    return jsonify(data), 200


@campaign_bp.route("/api/campaign/host/<ip>", methods=["GET"])
def api_host(ip: str):
    """Return one host card plus its artefacts."""
    from cli.scope_guard import target_in_scope

    index = _index()
    entries = _payload_entries()
    card = next((c for c in index.host_cards() if c["ip"] == ip), None)
    if card is None:
        return jsonify({"error": "host not found"}), 404
    artifacts = [
        {"rel": a.rel, "kind": a.kind, "size": a.size, "age_seconds": a.age_seconds, "stale": a.stale}
        for a in index.artifacts_for_host(ip)
    ]
    card["in_scope"] = target_in_scope(ip, entries)
    card["artifacts_list"] = artifacts
    return jsonify(card), 200


@campaign_bp.route("/api/campaign/file", methods=["GET"])
def api_file():
    """Serve one artefact as plain text with a hard traversal guard."""
    rel = request.args.get("path", "")
    index = _index()
    try:
        index.resolve_safe(rel)
    except (PermissionError, ValueError):
        abort(403)
    data = index.read(rel)
    if not data.get("exists"):
        abort(404)
    content = data.get("content", "")
    if data.get("binary"):
        content = f"[binary artifact, {data.get('size', 0)} bytes - not rendered]"
    if data.get("truncated"):
        content += "\n[truncated]"
    response = Response(content, mimetype="text/plain")
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["Content-Security-Policy"] = "default-src 'none'"
    return response


@campaign_bp.route("/api/campaign/search", methods=["GET"])
def api_search():
    """Run a regex search across the indexed artefacts."""
    query = request.args.get("q", "").strip()
    if not query:
        return jsonify({"error": "q required"}), 400
    result = _index().search(query, max_matches=DEFAULT_QUERY_LIMIT)
    return jsonify(result), 200


__all__ = ["campaign_bp"]
