"""Campaign REST blueprint for the phishing domain.

Lifted verbatim from the C2 monolith: campaign list/create, tracking
pixel, report, LLM orchestration, multi-vector campaign creation and
landing-page serving. Monolith-owned helpers (``load_yaml_safely``,
``clean_json``) are imported lazily inside the call sites to keep the
package importable without booting the monolith; storage paths come from
:mod:`lazyc2.phishing.paths` and credentials/session layout are injected
through :func:`init_campaigns_bp`.
"""

from __future__ import annotations

import csv
import json
import logging
import os
import re
import secrets
import sqlite3
import time
import uuid
from collections.abc import Callable
from datetime import UTC, datetime
from urllib.parse import urlparse

import yagmail
import yaml
from flask import (
    Blueprint,
    abort,
    flash,
    jsonify,
    redirect,
    render_template,
    request,
    url_for,
)
from flask_login import current_user, login_required

from lazyc2.phishing.paths import CAMPAIGNS_DIR, DB_PATH, TEMPLATES_DIR
from lazyc2.phishing.short_urls_store import load_short_urls, save_short_urls
from modules.llm_orchestrator import complete_with_fallback

_log = logging.getLogger(__name__)

phishing_bp = Blueprint("phishing", __name__, template_folder="templates/phishing")

_gmail_address = ""
_gmail_app_password = ""


def _default_sessions_dir() -> str:
    return os.path.join(os.getcwd(), "sessions")


_sessions_dir_fn: Callable[[], str] = _default_sessions_dir


def init_campaigns_bp(
    gmail_address: str,
    gmail_app_password: str,
    sessions_dir_fn: Callable[[], str],
) -> None:
    """Bind SMTP credentials and the session-directory provider.

    Args:
        gmail_address: SMTP account for campaign email delivery.
        gmail_app_password: SMTP password for the account.
        sessions_dir_fn: Callable returning the active sessions directory
            (tenant-switchable at runtime).
    """
    global _gmail_address, _gmail_app_password, _sessions_dir_fn
    _gmail_address = str(gmail_address or "")
    _gmail_app_password = str(gmail_app_password or "")
    _sessions_dir_fn = sessions_dir_fn


def _load_yaml(file_path):
    """Delegate to the monolith YAML loader (validated, path-confined)."""
    from lazyc2 import load_yaml_safely

    return load_yaml_safely(file_path)


def _clean_json(text):
    """Delegate to the monolith JSON cleaner."""
    from lazyc2 import clean_json

    return clean_json(text)


@phishing_bp.route("/phishing/campaigns", methods=["GET"])
@login_required
def list_campaigns():
    """List persisted campaigns."""
    campaigns = []
    for filename in os.listdir(CAMPAIGNS_DIR):
        if filename.endswith(".yaml"):
            campaign = _load_yaml(os.path.join(CAMPAIGNS_DIR, filename))
            if campaign:
                campaign["id"] = filename.replace(".yaml", "")
                campaigns.append(campaign)
    return render_template("phishing/campaigns.html", campaigns=campaigns)


@phishing_bp.route("/phishing/campaigns/new", methods=["GET", "POST"])
@login_required
def create_campaign():
    """Create and optionally launch a single-vector email campaign."""
    if request.method == "POST":
        data = request.form
        campaign_id = str(uuid.uuid4())

        if not data.get("name") or not data.get("template") or not data.get("recipients"):
            flash("Name, template, and recipients are required.", "error")
            return redirect(url_for("phishing.create_campaign"))

        beacon_url = data.get("beacon_url", "")
        if not beacon_url:
            _log.warning("Campaign %s created with empty beacon_url", campaign_id)
            short_url = secrets.token_urlsafe(6)
            short_urls = load_short_urls()
            short_urls[short_url] = {
                "original_url": f"http://{request.host}/track/{short_url}",
                "active": True,
                "created_at": datetime.now().isoformat(),
            }
            save_short_urls(short_urls)
            beacon_url = f"http://{request.host}/{short_url}"

        campaign = {
            "name": data["name"],
            "template": data["template"],
            "recipients": [r.strip() for r in data["recipients"].split(",")],
            "beacon_url": beacon_url,
            "created_at": datetime.now(UTC).isoformat(),
        }
        try:
            with open(os.path.join(CAMPAIGNS_DIR, f"{campaign_id}.yaml"), "w") as f:
                yaml.safe_dump(campaign, f)
            _log.info("Campaign %s saved successfully", campaign_id)
        except Exception as e:
            _log.error("Error saving campaign %s: %s", campaign_id, e)
            flash("Failed to save campaign.", "error")
            return redirect(url_for("phishing.create_campaign"))

        try:
            template_file = os.path.join(TEMPLATES_DIR, f"{campaign['template']}.yaml")
            template = _load_yaml(template_file)
            if not template:
                flash("Invalid email template.", "error")
                return redirect(url_for("phishing.create_campaign"))

            with yagmail.SMTP(_gmail_address, _gmail_app_password) as yag:
                for recipient in campaign["recipients"]:
                    tracking_url = url_for(
                        "phishing.track_pixel", campaign_id=campaign_id, email=recipient, _external=True
                    )
                    html_body = template["body"].format(
                        name=recipient.split("@")[0],
                        beacon_url=campaign["beacon_url"],
                        tracking_pixel=f'<img src="{tracking_url}" width="1" height="1" alt="" />',
                    )
                    yag.send(to=recipient, subject=template["subject"], contents=html_body)
                    _log.info("Sent email to %s for campaign %s", recipient, campaign_id)

                    conn = sqlite3.connect(DB_PATH)
                    conn.execute(
                        "INSERT INTO tracking VALUES (?, ?, ?, ?, ?)",
                        (campaign_id, recipient, "sent", request.remote_addr, datetime.now().isoformat()),
                    )
                    conn.commit()
                    conn.close()

            flash(f"Campaign {campaign['name']} sent to {len(campaign['recipients'])} recipients.", "success")
            return redirect(url_for("phishing.list_campaigns"))
        except Exception as e:
            _log.error("Error sending campaign %s: %s", campaign_id, e)
            flash("Failed to send campaign emails.", "error")
            return redirect(url_for("phishing.create_campaign"))
    templates = [f.replace(".yaml", "") for f in os.listdir(TEMPLATES_DIR) if f.endswith(".yaml")]
    return render_template("phishing/new_campaign.html", templates=templates)


@phishing_bp.route("/phishing/<campaign_id>/track/<email>")
def track_pixel(campaign_id, email):
    """Tracking pixel that registers email opens."""
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        "INSERT INTO tracking VALUES (?, ?, ?, ?, ?)",
        (
            campaign_id,
            email,
            "opened",
            request.remote_addr,
            datetime.now(UTC).replace(tzinfo=None).isoformat(),
        ),
    )
    conn.commit()
    conn.close()

    with open(os.path.join(os.getcwd(), "static", "images", "pixel.png"), "rb") as f:
        return f.read(), 200, {"Content-Type": "image/png"}


@phishing_bp.route("/phishing/<campaign_id>/report")
@login_required
def campaign_report(campaign_id):
    """Render the interaction report for one campaign."""
    campaign_file = os.path.join(CAMPAIGNS_DIR, f"{campaign_id}.yaml")
    campaign = _load_yaml(campaign_file)
    if not campaign:
        abort(404)
    campaign["id"] = campaign_id

    short_urls = load_short_urls()
    beacon_url = campaign.get("beacon_url", "") if "vectors" not in campaign else ""
    beacon_short_url = urlparse(beacon_url).path.lstrip("/") if beacon_url else ""

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT event, COUNT(*) FROM tracking WHERE campaign_id = ? GROUP BY event", (campaign_id,))
    stats = {row[0]: row[1] for row in cursor.fetchall()}
    cursor.execute(
        "SELECT email, event, ip, timestamp FROM tracking WHERE campaign_id = ? ORDER BY timestamp DESC",
        (campaign_id,),
    )
    events = [{"email": row[0], "event": row[1], "ip": row[2], "timestamp": row[3]} for row in cursor.fetchall()]
    cursor.execute(
        "SELECT email, event_type, ip, user_agent, timestamp, behavior_data FROM behavioral_tracking "
        "WHERE campaign_id = ? OR short_url = ? ORDER BY timestamp DESC",
        (campaign_id, beacon_short_url),
    )
    behavioral_events = [
        {
            "email": row[0],
            "event_type": row[1],
            "ip": row[2],
            "user_agent": row[3],
            "timestamp": row[4],
            "behavior_data": row[5],
        }
        for row in cursor.fetchall()
    ]
    cursor.execute(
        "SELECT email, event_type, ip, timestamp FROM multivector_tracking WHERE campaign_id = ? ORDER BY timestamp DESC",
        (campaign_id,),
    )
    multivector_events = [
        {"email": row[0], "event_type": row[1], "ip": row[2], "timestamp": row[3]} for row in cursor.fetchall()
    ]
    conn.close()

    download_events = []
    execution_events = []
    if beacon_short_url:
        download_events = parse_access_log_for_short_url(beacon_short_url)
        stats["downloaded"] = len(download_events)
        stats["interactions"] = len(behavioral_events) + len(multivector_events)
        original_url = short_urls.get(beacon_short_url, {}).get("original_url", "Unknown")
        for event in download_events:
            event["original_url"] = original_url
        implante = short_urls.get(beacon_short_url, {}).get("original_url", "").split("/")[-1].replace(".exe", "")
        if implante:
            implant_config = load_implant_config(implante)
            if implant_config.get("name") == implante:
                execution_events = parse_execution_log(implante)
                stats["executed"] = len(execution_events)

    if "vectors" in campaign:
        for _vector_type, vector_data in campaign["vectors"].items():
            vector_beacon_url = vector_data.get("beacon_url", "")
            if vector_beacon_url:
                vector_short_url = urlparse(vector_beacon_url).path.lstrip("/")
                download_events.extend(parse_access_log_for_short_url(vector_short_url))
                stats["downloaded"] = len(download_events)

    behavioral_analysis = analyze_behavioral_data(behavioral_events)
    return render_template(
        "phishing/report.html",
        campaign=campaign,
        stats=stats,
        events=events,
        download_events=download_events,
        execution_events=execution_events,
        behavioral_analysis=behavioral_analysis,
        multivector_events=multivector_events,
    )


@phishing_bp.route("/phishing/<campaign_id>/orchestrate", methods=["GET", "POST"])
@login_required
def orchestrate_campaign(campaign_id):
    """Adapt one campaign using the orchestrator LLM chain."""
    campaign_file = os.path.join(CAMPAIGNS_DIR, f"{campaign_id}.yaml")
    campaign = _load_yaml(campaign_file)
    if not campaign:
        abort(404)
    campaign["id"] = campaign_id

    if request.method == "GET":
        return render_template("phishing/orchestrate_campaign.html", campaign=campaign)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT email, event_type, ip, timestamp FROM multivector_tracking WHERE campaign_id = ?",
        (campaign_id,),
    )
    events = [{"email": row[0], "event_type": row[1], "ip": row[2], "timestamp": row[3]} for row in cursor.fetchall()]
    conn.close()

    adaptations = analyze_campaign_progress(campaign_id, events)
    short_urls = load_short_urls()
    new_short_url = adaptations.get("short_url", secrets.token_urlsafe(6))
    vector_beacon_url = (
        campaign.get("beacon_url", "")
        if "vectors" not in campaign
        else campaign["vectors"].get("email", {}).get("beacon_url", "")
    )
    short_urls[new_short_url] = {
        "original_url": adaptations.get("payload", vector_beacon_url),
        "active": True,
        "created_at": datetime.now().isoformat(),
    }
    save_short_urls(short_urls)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO multivector_tracking (campaign_id, email, event_type, ip, timestamp) VALUES (?, ?, ?, ?, ?)",
        (campaign_id, "unknown", adaptations["vector"], request.remote_addr, datetime.now().isoformat()),
    )
    conn.commit()
    conn.close()

    return jsonify({"status": "adapted", "vector": adaptations["vector"], "short_url": new_short_url})


@phishing_bp.route("/phishing/create_multivector_campaign", methods=["GET", "POST"])
@login_required
def create_multivector_campaign():
    """Create a multi-vector campaign from operator-supplied YAML."""
    if request.method == "GET":
        token = secrets.token_urlsafe(32)
        expiry = int(time.time()) + 3600

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS auth_tokens (user_id INTEGER, token TEXT, expiry INTEGER)")
        cursor.execute(
            "INSERT INTO auth_tokens (user_id, token, expiry) VALUES (?, ?, ?)",
            (current_user.id, token, expiry),
        )
        conn.commit()
        conn.close()

        return render_template("phishing/create_multivector_campaign.html", auth_token=token)

    if request.method == "POST":
        yaml_input = request.form.get("yaml_input")
        auth_token = request.form.get("auth_token")

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT expiry FROM auth_tokens WHERE user_id = ? AND token = ?", (current_user.id, auth_token))
        result = cursor.fetchone()
        conn.close()

        if not result or result[0] < int(time.time()):
            flash("Invalid or expired authentication token.", "error")
            return redirect(url_for("phishing.create_multivector_campaign"))

        if not yaml_input:
            flash("YAML input is required.", "error")
            return redirect(url_for("phishing.create_multivector_campaign"))

        try:
            data = yaml.safe_load(yaml_input)
            if not data or not data.get("name") or not data.get("vectors"):
                flash("Campaign name and vectors are required.", "error")
                return redirect(url_for("phishing.create_multivector_campaign"))
        except yaml.YAMLError as e:
            _log.error("Invalid YAML input: %s", e)
            flash("Invalid YAML format. Check your syntax and try again.", "error")
            return redirect(url_for("phishing.create_multivector_campaign"))

        campaign_id = str(uuid.uuid4())
        campaign = {
            "id": campaign_id,
            "name": data["name"],
            "vectors": data.get("vectors", {}),
            "created_at": datetime.now().isoformat(),
        }
        try:
            with open(os.path.join(CAMPAIGNS_DIR, f"{campaign_id}.yaml"), "w") as f:
                yaml.safe_dump(campaign, f)
            _log.info("Created multi-vector campaign: %s", campaign_id)
        except Exception as e:
            _log.error("Error saving campaign %s: %s", campaign_id, e)
            flash("Failed to save campaign.", "error")
            return redirect(url_for("phishing.create_multivector_campaign"))

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        short_urls = load_short_urls()

        if "email" in campaign["vectors"]:
            email_vector = campaign["vectors"]["email"]
            template_file = os.path.join(TEMPLATES_DIR, f"{email_vector.get('template', '')}.yaml")
            template = _load_yaml(template_file)
            if not template:
                flash("Invalid email template.", "error")
                return redirect(url_for("phishing.create_multivector_campaign"))
            beacon_url = email_vector.get("beacon_url", "")
            if not beacon_url:
                short_url = secrets.token_urlsafe(6)
                short_urls[short_url] = {
                    "original_url": f"http://{request.host}/track/{short_url}",
                    "active": True,
                    "created_at": datetime.now().isoformat(),
                }
                beacon_url = f"http://{request.host}/{short_url}"
                campaign["vectors"]["email"]["beacon_url"] = beacon_url
            with yagmail.SMTP(_gmail_address, _gmail_app_password) as yag:
                for recipient in email_vector.get("recipients", []):
                    tracking_url = url_for(
                        "phishing.track_pixel", campaign_id=campaign_id, email=recipient, _external=True
                    )
                    html_body = template["body"].format(
                        name=recipient.split("@")[0],
                        beacon_url=beacon_url,
                        tracking_pixel=f'<img src="{tracking_url}" width="1" height="1" alt="" />',
                    )
                    yag.send(to=recipient, subject=template["subject"], contents=html_body)
                    cursor.execute(
                        "INSERT INTO multivector_tracking (campaign_id, email, event_type, ip, timestamp) "
                        "VALUES (?, ?, ?, ?, ?)",
                        (campaign_id, recipient, "email_sent", request.remote_addr, datetime.now().isoformat()),
                    )

        if "sms" in campaign["vectors"]:
            sms_vector = campaign["vectors"]["sms"]
            sms_beacon_url = sms_vector.get("beacon_url", "")
            if not sms_beacon_url:
                short_url = secrets.token_urlsafe(6)
                short_urls[short_url] = {
                    "original_url": f"http://{request.host}/track/{short_url}",
                    "active": True,
                    "created_at": datetime.now().isoformat(),
                }
                sms_beacon_url = f"http://{request.host}/{short_url}"
                campaign["vectors"]["sms"]["beacon_url"] = sms_beacon_url
            message = sms_vector.get("message", "")
            for recipient in sms_vector.get("recipients", []):
                try:
                    formatted_message = message.format(beacon_url=sms_beacon_url)
                    _log.info("Sent SMS to %s with message: %s", recipient, formatted_message)
                    cursor.execute(
                        "INSERT INTO multivector_tracking (campaign_id, email, event_type, ip, timestamp) "
                        "VALUES (?, ?, ?, ?, ?)",
                        (campaign_id, recipient, "sms_sent", request.remote_addr, datetime.now().isoformat()),
                    )
                except Exception as e:
                    _log.error("Error sending SMS to %s: %s", recipient, e)

        if "landing_page" in campaign["vectors"]:
            landing_vector = campaign["vectors"]["landing_page"]
            landing_beacon_url = landing_vector.get("beacon_url", "")
            if not landing_beacon_url:
                short_url = secrets.token_urlsafe(6)
                short_urls[short_url] = {
                    "original_url": f"http://{request.host}/track/{short_url}",
                    "active": True,
                    "created_at": datetime.now().isoformat(),
                }
                landing_beacon_url = f"http://{request.host}/{short_url}"
                campaign["vectors"]["landing_page"]["beacon_url"] = landing_beacon_url

            template_name = landing_vector.get("template", "")
            if template_name:
                cursor.execute(
                    "INSERT INTO multivector_tracking (campaign_id, email, event_type, ip, timestamp) "
                    "VALUES (?, ?, ?, ?, ?)",
                    (campaign_id, "unknown", "landing_page_created", request.remote_addr, datetime.now().isoformat()),
                )
        save_short_urls(short_urls)
        conn.commit()
        conn.close()

        with open(os.path.join(CAMPAIGNS_DIR, f"{campaign_id}.yaml"), "w") as f:
            yaml.safe_dump(campaign, f)

        return jsonify({"campaign_id": campaign_id, "message": "Multi-vector campaign created successfully"}), 200


@phishing_bp.route("/phishing/landing/<campaign_id>/<short_url>")
def serve_landing_page(campaign_id, short_url):
    """Serve the configured landing page for one campaign vector."""
    campaign_file = os.path.join(CAMPAIGNS_DIR, f"{campaign_id}.yaml")
    campaign = _load_yaml(campaign_file)
    if not campaign or "landing_page" not in campaign.get("vectors", {}):
        abort(404)
    short_urls = load_short_urls()
    if short_url not in short_urls or not short_urls[short_url]["active"]:
        abort(404)
    template_name = campaign["vectors"]["landing_page"].get("template", "")
    if not template_name:
        abort(404)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO multivector_tracking (campaign_id, email, event_type, ip, timestamp) VALUES (?, ?, ?, ?, ?)",
        (campaign_id, "unknown", "landing_page_visit", request.remote_addr, datetime.now().isoformat()),
    )
    conn.commit()
    conn.close()
    return render_template(
        f"phishing/landing_pages/{template_name}.html", beacon_url=short_urls[short_url]["original_url"]
    )


_BEHAVIOR_SYSTEM_PROMPT = (
    "You are a phishing simulation risk analyzer. Reply with a single integer risk score from 0 to 100."
)


def _behavioral_risk_prompt(event):
    """Render the risk-scoring prompt for one behavioral event.

    Args:
        event: Behavioral event mapping with event metadata.

    Returns:
        Prompt text asking for a single integer risk score.
    """
    return f"""
        Analyze the following user interaction:
        - Event: {event["event_type"]}
        - IP: {event["ip"]}
        - User Agent: {event["user_agent"]}
        - Behavior Data: {event["behavior_data"]}
        - Timestamp: {event["timestamp"]}
        Determine a risk score (0-100) based on suspicious behavior (e.g., rapid clicks, unusual IPs).
        """


def analyze_behavioral_data(behavioral_events):
    """Analyze behavioral events using the orchestrator LLM chain.

    The lazy_orchestrator failover chain serves each risk score, so a
    missing Groq key or an exhausted quota degrades to the next chain
    member instead of disabling the analysis.

    Args:
        behavioral_events: Behavioral event mappings from the tracking DB.

    Returns:
        Per-event risk scores; empty when no chain member answers.
    """
    analysis_results = []
    for event in behavioral_events:
        result = complete_with_fallback(
            _behavioral_risk_prompt(event),
            system=_BEHAVIOR_SYSTEM_PROMPT,
            max_tokens=100,
        )
        if not result.ok:
            return analysis_results if analysis_results else []
        risk_score = int(result.text.strip()) if result.text.strip().isdigit() else 50
        analysis_results.append({"email": event["email"], "event_type": event["event_type"], "risk_score": risk_score})
    return analysis_results


_CAMPAIGN_SYSTEM_PROMPT = (
    "You are an AI assistant analyzing an ethical phishing campaign simulation. "
    "Reply only with the requested JSON object."
)


def _campaign_adaptation_prompt(campaign_id, events):
    """Render the adaptation prompt for a campaign progress check.

    Args:
        campaign_id: Campaign identifier.
        events: Tracked interaction events.

    Returns:
        Prompt text asking for a JSON adaptation object.
    """
    return f"""
    You are an AI assistant analyzing a ethic phishing campaign simulation. Given the campaign ID {campaign_id} with events: {json.dumps(events)}.
    Suggest adaptations (e.g., change vector, payload, URL) to improve success rate.
    **Important**: Return your response as a valid JSON object with the following structure:
    ```json
    Return JSON: ```json{{ "vector": str, "payload": str, "short_url": str }}```
    """


def analyze_campaign_progress(campaign_id, events):
    """Analyze campaign progress using the orchestrator LLM chain.

    The lazy_orchestrator failover chain proposes the adaptation, so a
    missing Groq key or an exhausted quota degrades to the next chain
    member instead of disabling the orchestration route.

    Args:
        campaign_id: Campaign identifier.
        events: Tracked interaction events.

    Returns:
        Adaptation mapping with vector, payload and short_url keys;
        empty when no chain member answers with valid JSON.
    """
    result = complete_with_fallback(
        _campaign_adaptation_prompt(campaign_id, events),
        system=_CAMPAIGN_SYSTEM_PROMPT,
        max_tokens=200,
    )
    if not result.ok:
        return {}
    candidate = _clean_json(result.text.strip())
    if not candidate:
        candidate = result.text.strip()
    try:
        parsed = json.loads(candidate)
    except (json.JSONDecodeError, ValueError):
        return {}
    return parsed if isinstance(parsed, dict) else {}


_ACCESS_LOG_PATTERN = re.compile(
    r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3}) - INFO - Short URL (.+?) accessed by (.+?) with (.+)"
)


def parse_access_log_for_short_url(short_url):
    """Parse access.log for entries matching the given short URL."""
    download_events = []
    try:
        with open("sessions/access.log", "r") as f:
            for line in f:
                match = _ACCESS_LOG_PATTERN.match(line.strip())
                if match and match.group(2) == short_url:
                    timestamp, matched_url, ip, user_agent = match.groups()
                    download_events.append(
                        {"short_url": matched_url, "ip": ip, "user_agent": user_agent, "timestamp": timestamp}
                    )
    except FileNotFoundError:
        _log.error("access.log not found")
    except Exception:
        _log.error("Error parsing access.log: %s", "")
    return download_events


def parse_execution_log(implante):
    """Parse the execution log for one implant, returning execution events."""
    execution_events = []
    log_file = os.path.join(_sessions_dir_fn(), f"{implante}.log")
    if not os.path.exists(log_file):
        _log.warning("Execution log not found: %s", log_file)
        return execution_events
    with open(log_file, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            execution_events.append(
                {
                    "client_id": row["client_id"],
                    "os": row["os"],
                    "pid": row["pid"],
                    "hostname": row["hostname"],
                    "ips": row["ips"],
                    "user": row["user"],
                    "command": row["command"],
                    "output": row["output"].strip(),
                    "timestamp": datetime.now().isoformat(),
                }
            )
    return execution_events


def load_implant_config(implante):
    """Load one implant configuration from the sessions directory."""
    config_file = os.path.join(_sessions_dir_fn(), f"implant_config_{implante}.json")
    if not os.path.exists(config_file):
        _log.warning("Implant config not found: %s", config_file)
        return {}
    with open(config_file, "r") as f:
        return json.load(f)
