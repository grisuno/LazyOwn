"""Phishing blueprint for the LazyOwn C2 server.

Short URL management, phishing campaign tracking, behavioural
logging, and file-serving endpoints.

Registered under no prefix (the short URL redirect endpoint must
live at ``/`` so it can capture arbitrary paths).
"""

from __future__ import annotations

import logging
import os
import secrets
from datetime import datetime
from urllib.parse import urlparse

from flask import (
    Blueprint,
    abort,
    current_app,
    jsonify,
    redirect,
    render_template,
    request,
    send_file,
    send_from_directory,
)
from werkzeug.utils import secure_filename

from modules.security_sanitizers import SessionPathResolver
from lazyc2.extensions.short_urls import (
    is_valid_url,
    load_short_urls,
    save_short_urls,
)

redirect_bp = Blueprint("redirect", __name__)


def _get_config(key: str, default=None):
    """Read a value from the Flask app config (set by app factory)."""
    return current_app.config.get(key, default)


@redirect_bp.route("/create_short_url", methods=["POST"])
def create_short_url():
    """Create one or more short URLs for a single original URL.

    Request JSON:
        ``original_url`` (str, required): Target URL or file path.
        ``custom_short_url`` (str, optional): Custom short code.
        ``count`` (int, optional): Number of short URLs to create
            (default 1).

    Returns:
        200 with the list of generated short codes, or 400 on
        validation failure.
    """
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "No data provided"}), 400
    original_url = data.get("original_url")
    custom_short_url = data.get("custom_short_url")
    count = data.get("count", 1)
    if not original_url:
        return jsonify({"error": "Original URL is required"}), 400
    if not is_valid_url(original_url):
        return jsonify({"error": "Invalid URL or file path."}), 400
    short_urls = load_short_urls()
    generated = []
    for _ in range(count):
        short_code = custom_short_url if custom_short_url and not generated else secrets.token_urlsafe(6)
        if short_code in short_urls:
            continue
        short_urls[short_code] = {
            "original_url": original_url,
            "active": True,
            "created_at": datetime.now().isoformat(),
        }
        generated.append(short_code)
    save_short_urls(short_urls)
    return jsonify({"short_urls": generated})


@redirect_bp.route("/track/<short_url>")
def track_interaction(short_url):
    """Serve a tracking page and log behavioural data.

    Logs client IP, user-agent, and optional behaviour data to the
    C2 database. Renders ``tracking_page.html`` for real-user
    simulation.
    """
    import sqlite3

    short_urls = load_short_urls()
    if short_url not in short_urls or not short_urls[short_url]["active"]:
        abort(404)
    db_path = _get_config("DB_PATH", "sessions/c2.db")
    client_ip = request.remote_addr
    user_agent = request.headers.get("User-Agent")
    behavior_data = request.args.get("behavior", "{}")
    email = request.args.get("email", "unknown")
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO behavioral_tracking "
            "(campaign_id, short_url, email, event_type, ip, user_agent, timestamp, behavior_data) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            ("unknown", short_url, email, "click", client_ip, user_agent, datetime.now().isoformat(), behavior_data),
        )
        conn.commit()
        conn.close()
    except Exception:
        logging.exception("Failed to log tracking event")
    return render_template("tracking_page.html", short_url=short_url, original_url=short_urls[short_url]["original_url"])


@redirect_bp.route("/update_short_url/<short_url>", methods=["PUT"])
def update_short_url(short_url):
    """Update an existing short URL's target or active status.

    Request JSON (at least one):
        ``original_url`` (str): New target URL.
        ``active`` (bool): Enable or disable the short URL.
    """
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "No data provided"}), 400
    new_url = data.get("original_url")
    active = data.get("active")
    if new_url and not is_valid_url(new_url):
        return jsonify({"error": "Invalid URL format"}), 400
    short_urls = load_short_urls()
    if short_url not in short_urls:
        return jsonify({"error": "Short URL not found"}), 404
    if new_url:
        short_urls[short_url]["original_url"] = new_url
    if active is not None:
        short_urls[short_url]["active"] = active
    save_short_urls(short_urls)
    return jsonify({"message": "Updated successfully"})


@redirect_bp.route("/<short_url>")
def redirect_to_file(short_url):
    """Resolve a short URL and redirect (or serve a local file).

    If the original URL points to a local file under the sessions
    directory the file is served directly; otherwise an HTTP
    redirect is issued.
    """
    short_urls = load_short_urls()
    if short_url not in short_urls or not short_urls[short_url]["active"]:
        abort(404)
    original_url = short_urls[short_url]["original_url"]
    parsed = urlparse(original_url)
    if parsed.scheme == "file" or not parsed.scheme:
        file_path = parsed.path if parsed.scheme == "file" else original_url
        file_path = os.path.abspath(file_path)
        if os.path.exists(file_path) and os.path.isfile(file_path):
            return send_file(file_path)
        abort(404)
    return redirect(original_url)


@redirect_bp.route("/webserver-report")
@redirect_bp.route("/webserver-report/<path:filename>")
def webserver_report(filename="index2.html"):
    """Serve nmap HTML report assets from the sessions directory.

    Path validation is enforced through :class:`SessionPathResolver`.
    """
    sessions_dir = _get_config("SESSIONS_DIR", "sessions")
    security_cfg = _get_config("_security_config")
    resolver = SessionPathResolver(sessions_dir, security_cfg)
    resolved = resolver.resolve(filename)
    if resolved is None:
        abort(403)
    absolute, relative = resolved
    if not os.path.isfile(absolute):
        abort(404)
    return send_from_directory(resolver.base_dir, relative)


@redirect_bp.route("/s/<filename>")
def download_files(filename):
    """Serve a session file by name with path-traversal protection.

    Enforces strict basename containment, secure filename sanitisation,
    realpath containment, and an extension allowlist.
    """
    access_denied = "Access denied or invalid file"
    if not filename or "/" in filename or "\\" in filename or "\x00" in filename:
        abort(403, description=access_denied)
    if filename in (".", ".."):
        abort(403, description=access_denied)
    sanitized = secure_filename(filename)
    if not sanitized or sanitized != filename:
        abort(403, description=access_denied)
    if os.path.basename(sanitized) != sanitized:
        abort(403, description=access_denied)

    sessions_dir = _get_config("SESSIONS_DIR", "sessions")
    allowed_extensions = _get_config("ALLOWED_EXTENSIONS", {"txt", "enc", "exe"})
    sessions_real = os.path.realpath(sessions_dir)
    candidate_real = os.path.realpath(os.path.join(sessions_real, sanitized))
    try:
        if os.path.commonpath([sessions_real, candidate_real]) != sessions_real:
            abort(403, description=access_denied)
    except ValueError:
        abort(403, description=access_denied)

    ext = sanitized.rsplit(".", 1)[-1].lower() if "." in sanitized else ""
    is_allowed = ext in allowed_extensions
    is_existing = os.path.isfile(candidate_real)
    short_urls = load_short_urls()
    for data in short_urls.values():
        if not data.get("active", False):
            continue
        parsed = urlparse(data["original_url"])
        orig_name = os.path.basename(parsed.path)
        if sanitized == orig_name and is_existing:
            return send_from_directory(sessions_real, sanitized)
    if is_existing and is_allowed:
        return send_from_directory(sessions_real, sanitized)
    abort(403, description=access_denied)
