"""API blueprint for the LazyOwn C2 server.

Provides REST endpoints for command execution, output retrieval, and
dashboard data. Registered under the ``/api`` prefix.
"""

from __future__ import annotations

from flask import Blueprint, jsonify, request

api_bp = Blueprint("api", __name__, url_prefix="/api")


@api_bp.route("/ping", methods=["GET"])
def ping():
    """Health-check endpoint.

    Returns:
        200 with ``{"status": "ok"}``.
    """
    return jsonify({"status": "ok"})
