"""Cloud attack commands — Azure AD/Entra ID, AWS, GCP, Kubernetes, cross-cloud, SaaS.

Provides:
    entra_attack            — Entra ID device code phishing, OAuth consent, managed identity
    aws_privesc             — AWS IAM enumeration, Lambda backdoors, STS role chaining
    gcp_privesc             — GCP service account impersonation, Cloud Functions, GCS
    k8s_attack              — Kubernetes RBAC enum, pod escape, etcd, Helm Tiller
    cross_cloud             — Cross-cloud federation attacks (SAML/OIDC bridging)
    saas_enum               — SaaS platform enumeration (M365, Google Workspace, Salesforce, Slack)
"""

from __future__ import annotations

import cmd2

from cli.commands._base import LazyOwnCommandSet


class CloudAttackCommandSet(LazyOwnCommandSet):
    """Cloud and SaaS attack operations."""

    phase = "enumeration"
    category = "06. Cloud Attacks"

    def do_entra_attack(self, line: str) -> None:
        """Microsoft Entra ID / Azure AD attack operations.

Usage: entra_attack <method> [options]

Methods:
    device_code   — Initiate device code phishing flow
    consent_grant — Generate OAuth consent grant phishing URL
    spn_cred_theft — Service principal credential theft plan
    managed_identity — Managed identity abuse from compromised VM/container
    connect_sync  — Entra Connect Sync abuse (on-prem ↔ cloud)
    ca_bypass     — Conditional Access bypass techniques
    tenant_enum   — Enumerate tenant via Graph API

Examples:
    entra_attack device_code
    entra_attack consent_grant
    entra_attack tenant_enum
"""
        from modules.entra_id_attacks import EntraIDAttackEngine

        engine = EntraIDAttackEngine()

        if not line.strip():
            self._cmd.poutput(f"\n[ Entra ID Attack Methods ]")
            for method in ["device_code", "consent_grant", "spn_cred_theft", "managed_identity", "connect_sync", "ca_bypass"]:
                self._cmd.poutput(f"    {method}")
            self._cmd.poutput(f"\nUsage: entra_attack <method>")
            return

        method = line.strip().split()[0].lower()

        if method == "device_code":
            result = engine.device_code_phish()
            self._cmd.poutput(f"\n[ Device Code Phishing ]")
            self._cmd.poutput(f"    User Code      : {result.get('user_code', 'N/A')}")
            self._cmd.poutput(f"    Verification   : {result.get('verification_uri', '')}")
            self._cmd.poutput(f"    Expires in     : {result.get('expires_in', 900)}s")
            self._cmd.poutput(f"    Poll interval  : {result.get('interval', 5)}s")
            self._cmd.poutput(f"\n    Send the user to: {result.get('verification_uri', '')}")
            self._cmd.poutput(f"    Enter the code : {result.get('user_code', '')}")

        elif method == "consent_grant":
            result = engine.oauth_consent_grant()
            self._cmd.poutput(f"\n[ OAuth Consent Grant Phishing ]")
            self._cmd.poutput(f"    Scopes requested:")
            for scope in result.get('scopes', []):
                self._cmd.poutput(f"        - {scope}")
            self._cmd.poutput(f"\n    Consent URL ({len(result['consent_url'])} chars):")
            self._cmd.poutput(f"        {result['consent_url'][:200]}...")

        elif method == "spn_cred_theft":
            result = engine.service_principal_credential_theft()
            self._cmd.poutput(f"\n[ Service Principal Credential Theft ]")
            self._cmd.poutput(f"    Requirements:")
            for req in result['requirements']:
                self._cmd.poutput(f"        - {req}")
            self._cmd.poutput(f"\n    Attack Steps:")
            for step in result['steps']:
                self._cmd.poutput(f"        {step}")

        elif method == "managed_identity":
            result = engine.managed_identity_abuse()
            self._cmd.poutput(f"\n[ Managed Identity Abuse ]")
            self._cmd.poutput(f"    IMDS Endpoints:")
            for name, url in result['imds_endpoints'].items():
                self._cmd.poutput(f"        {name}: {url}")
            self._cmd.poutput(f"\n    Curl Commands:")
            for cmd in result['curl_commands']:
                self._cmd.poutput(f"        $ {cmd}")

        elif method == "connect_sync":
            result = engine.entra_connect_sync_abuse()
            self._cmd.poutput(f"\n[ Entra Connect Sync Abuse ]")
            for path in result['attack_paths']:
                self._cmd.poutput(f"\n    {path['direction']}: {path['description']}")
                for step in path['steps'][:3]:
                    self._cmd.poutput(f"        {step}")

        elif method == "ca_bypass":
            result = engine.conditional_access_bypass()
            self._cmd.poutput(f"\n[ Conditional Access Bypass Techniques ]")
            for tech in result['techniques']:
                self._cmd.poutput(f"\n    [{tech['name']}]")
                self._cmd.poutput(f"        {tech['description']}")

        elif method == "tenant_enum":
            result = engine.enumerate_tenant()
            self._cmd.poutput(f"\n[ Tenant Enumeration via Graph API ]")
            for name, endpoint in result['graph_endpoints'].items():
                self._cmd.poutput(f"    GET {endpoint}")

        else:
            self._cmd.perror(f"Unknown method: {method}")

    def do_aws_privesc(self, line: str) -> None:
        """AWS privilege escalation and enumeration.

Usage: aws_privesc <method>

Methods:
    iam_enum        — Enumerate IAM permissions and privesc paths
    lambda_backdoor — Backdoor a Lambda function for role credential theft
    sts_chain       — Enumerate STS AssumeRole privesc chains
    ec2_data        — Extract EC2 instance user data and metadata
    s3_enum         — Enumerate S3 buckets and permissions
    cf_drift        — CloudFormation drift exploitation
    ssm_abuse       — SSM session abuse for EC2 shell access

Examples:
    aws_privesc iam_enum
    aws_privesc lambda_backdoor
"""
        from modules.aws_attacks import AWSAttackEngine, AWS_PRIVESC_METHODS

        engine = AWSAttackEngine()

        if not line.strip():
            self._cmd.poutput(f"\n[ AWS Privesc Methods — {len(AWS_PRIVESC_METHODS)} total ]")
            for m in AWS_PRIVESC_METHODS[:10]:
                self._cmd.poutput(f"    {m}")
            self._cmd.poutput(f"\nUsage: aws_privesc <method>")
            return

        method = line.strip().split()[0].lower()

        if method == "iam_enum":
            result = engine.enumerate_iam_permissions()
            self._cmd.poutput(f"\n[ IAM Permission Enumeration ]")
            self._cmd.poutput(f"\n[ Quick Commands ]")
            for cmd in result.get('commands', [])[:5]:
                self._cmd.poutput(f"    $ {cmd}")
            self._cmd.poutput(f"\n[ Privesc Checks ]")
            for perm, desc in result.get('privesc_check', {}).items():
                self._cmd.poutput(f"    {perm:50s} → {desc}")

        elif method == "lambda_backdoor":
            result = engine.lambda_backdoor()
            self._cmd.poutput(f"\n[ Lambda Backdoor ]")
            for req in result.get('requirements', []):
                self._cmd.poutput(f"    Requires: {req}")
            self._cmd.poutput(f"\n    Backdoor code (Python):")
            self._cmd.poutput(f"        {result.get('backdoor_code', '')[:200]}")

        elif method == "sts_chain":
            result = engine.sts_role_chain()
            self._cmd.poutput(f"\n[ STS Role Chaining ]")
            for cmd in result.get('commands', [])[:4]:
                self._cmd.poutput(f"    $ {cmd}")
            self._cmd.poutput(f"\n    Example chain: {result.get('chain_example', '')}")

        elif method == "ec2_data":
            result = engine.ec2_user_data_exfil()
            self._cmd.poutput(f"\n[ EC2 User Data Exfiltration ]")
            self._cmd.poutput(f"\n[ IMDSv1 Commands ]")
            for cmd in result.get('imdsv1_commands', []):
                self._cmd.poutput(f"    $ {cmd}")
            self._cmd.poutput(f"\n[ IMDSv2 Commands ]")
            for cmd in result.get('imdsv2_commands', []):
                self._cmd.poutput(f"    $ {cmd}")

        elif method == "s3_enum":
            result = engine.s3_enumeration()
            self._cmd.poutput(f"\n[ S3 Enumeration ]")
            for cmd in result.get('commands', [])[:3]:
                self._cmd.poutput(f"    $ {cmd}")
            self._cmd.poutput(f"\n[ Sensitive Patterns ]")
            for pattern in result.get('sensitive_patterns', [])[:5]:
                self._cmd.poutput(f"    {pattern}")

        elif method == "cf_drift":
            result = engine.cloudformation_drift()
            self._cmd.poutput(f"\n[ CloudFormation Drift ]")
            for cmd in result.get('commands', [])[:3]:
                self._cmd.poutput(f"    $ {cmd}")

        elif method == "ssm_abuse":
            result = engine.ec2_ssm_session_abuse()
            self._cmd.poutput(f"\n[ SSM Session Abuse ]")
            for cmd in result.get('commands', [])[:3]:
                self._cmd.poutput(f"    $ {cmd}")

        else:
            self._cmd.perror(f"Unknown method: {method}")

    def do_gcp_privesc(self, line: str) -> None:
        """GCP privilege escalation and enumeration.

Usage: gcp_privesc <method>

Methods:
    iam_enum        — Enumerate GCP IAM policies
    sa_impersonate  — Service account impersonation attack
    cloud_function  — Cloud Functions backdoor
    metadata_exfil  — Compute Engine metadata exfiltration
    gcs_enum        — Cloud Storage bucket enumeration
    cloudbuild      — Cloud Build abuse
    org_escalation  — Organization-level escalation paths

Examples:
    gcp_privesc iam_enum
    gcp_privesc metadata_exfil
"""
        from modules.gcp_attacks import GCPAttackEngine

        engine = GCPAttackEngine()

        if not line.strip():
            self._cmd.poutput(f"\n[ GCP Privesc Methods ]")
            for method in ["iam_enum", "sa_impersonate", "cloud_function", "metadata_exfil", "gcs_enum", "cloudbuild", "org_escalation"]:
                self._cmd.poutput(f"    {method}")
            self._cmd.poutput(f"\nUsage: gcp_privesc <method>")
            return

        method = line.strip().split()[0].lower()

        if method == "iam_enum":
            result = engine.enumerate_iam_policy()
            self._cmd.poutput(f"\n[ GCP IAM Enumeration ]")
            for cmd in result.get('commands', [])[:5]:
                self._cmd.poutput(f"    $ {cmd}")
            self._cmd.poutput(f"\n[ Sensitive Roles ]")
            for role in result.get('sensitive_roles', [])[:5]:
                self._cmd.poutput(f"    {role}")

        elif method == "sa_impersonate":
            result = engine.service_account_impersonation()
            self._cmd.poutput(f"\n[ Service Account Impersonation ]")
            for cmd in result.get('commands', [])[:3]:
                self._cmd.poutput(f"    $ {cmd}")

        elif method == "cloud_function":
            result = engine.cloud_functions_backdoor()
            self._cmd.poutput(f"\n[ Cloud Functions Backdoor ]")
            for cmd in result.get('commands', [])[:3]:
                self._cmd.poutput(f"    $ {cmd}")

        elif method == "metadata_exfil":
            result = engine.compute_engine_metadata_exfil()
            self._cmd.poutput(f"\n[ Compute Engine Metadata Exfiltration ]")
            for cmd in result.get('commands', [])[:5]:
                self._cmd.poutput(f"    $ {cmd}")

        elif method == "gcs_enum":
            result = engine.gcs_enumeration()
            self._cmd.poutput(f"\n[ GCS Enumeration ]")
            for cmd in result.get('commands', [])[:4]:
                self._cmd.poutput(f"    $ {cmd}")

        elif method == "cloudbuild":
            result = engine.cloudbuild_abuse()
            self._cmd.poutput(f"\n[ Cloud Build Abuse ]")
            for cmd in result.get('commands', [])[:2]:
                self._cmd.poutput(f"    $ {cmd}")

        elif method == "org_escalation":
            result = engine.organization_escalation()
            self._cmd.poutput(f"\n[ Organization Escalation ]")
            for path in result.get('paths', []):
                self._cmd.poutput(f"\n    [{path['name']}] {path['description']}")

        else:
            self._cmd.perror(f"Unknown method: {method}")

    def do_k8s_attack(self, line: str) -> None:
        """Kubernetes attack — RBAC enumeration, pod escape, etcd, persistence.

Usage: k8s_attack <method>

Methods:
    rbac_enum       — Enumerate RBAC permissions
    pod_escape      — Privileged pod escape plan (hostPID, hostPath, docker socket)
    token_theft     — Service account token theft across namespaces
    kubelet_abuse   — Kubelet anonymous auth abuse
    etcd            — etcd database exploitation
    helm            — Helm Tiller abuse (v2+v3)
    persistence     — K8s persistence techniques

Examples:
    k8s_attack rbac_enum
    k8s_attack pod_escape
    k8s_attack persistence
"""
        from modules.k8s_attacks import K8SAttackEngine, K8sConfig

        config = K8sConfig(namespace=self.params.get("domain", "default"))
        engine = K8SAttackEngine(config=config)

        if not line.strip():
            self._cmd.poutput(f"\n[ K8s Attack Methods ]")
            for method in ["rbac_enum", "pod_escape", "token_theft", "kubelet_abuse", "etcd", "helm", "persistence"]:
                self._cmd.poutput(f"    {method}")
            self._cmd.poutput(f"\nUsage: k8s_attack <method>")
            return

        method = line.strip().split()[0].lower()

        if method == "rbac_enum":
            result = engine.enumerate_rbac()
            self._cmd.poutput(f"\n[ K8s RBAC Enumeration ]")
            for cmd in result.get('commands', [])[:5]:
                self._cmd.poutput(f"    $ {cmd}")
            self._cmd.poutput(f"\n[ Privesc Checks ]")
            for perm, desc in result.get('privesc_checks', {}).items():
                self._cmd.poutput(f"    {perm:45s} → {desc}")

        elif method == "pod_escape":
            result = engine.privileged_pod_escape()
            self._cmd.poutput(f"\n[ Privileged Pod Escape ]")
            self._cmd.poutput(f"    Requirements: {', '.join(result.get('requirements', []))}")
            self._cmd.poutput(f"\n    Escape commands (inside pod):")
            for cmd in result.get('commands', [])[4:8]:
                self._cmd.poutput(f"        $ {cmd}")

        elif method == "token_theft":
            result = engine.service_account_token_theft()
            self._cmd.poutput(f"\n[ SA Token Theft ]")
            for cmd in result.get('commands', [])[:3]:
                self._cmd.poutput(f"    $ {cmd}")

        elif method == "kubelet_abuse":
            result = engine.kubelet_anonymous_auth_abuse()
            self._cmd.poutput(f"\n[ Kubelet Anonymous Auth Abuse ]")
            for cmd in result.get('commands', [])[:4]:
                self._cmd.poutput(f"    $ {cmd}")

        elif method == "etcd":
            result = engine.etcd_access_exploitation()
            self._cmd.poutput(f"\n[ etcd Exploitation ]")
            for cmd in result.get('commands', [])[:3]:
                self._cmd.poutput(f"    $ {cmd}")

        elif method == "helm":
            result = engine.helm_tiller_abuse()
            self._cmd.poutput(f"\n[ Helm Tiller Abuse ]")
            self._cmd.poutput(f"\n    v2 Tiller (port {result['tiller_v2']['port']}):")
            for cmd in result['tiller_v2']['commands']:
                self._cmd.poutput(f"        $ {cmd}")

        elif method == "persistence":
            result = engine.persistence_techniques()
            self._cmd.poutput(f"\n[ K8s Persistence Techniques ]")
            for tech in result.get('techniques', []):
                self._cmd.poutput(f"\n    [{tech['name']}] {tech['description']}")
                self._cmd.poutput(f"        API: {tech['api_resource']}")

        else:
            self._cmd.perror(f"Unknown method: {method}")

    def do_cross_cloud(self, line: str) -> None:
        """Cross-cloud identity federation attacks.

Usage: cross_cloud <method>

Methods:
    azure_to_aws   — Azure AD SAML → AWS role assumption
    gcp_to_azure   — GCP OIDC → Azure AD token exchange
    aws_to_gcp     — AWS OIDC → GCP workload identity federation
    imds_harvest   — Multi-cloud IMDS metadata harvesting (6 providers)
    detect_federation — Detect cross-cloud federation configurations

Examples:
    cross_cloud azure_to_aws
    cross_cloud imds_harvest
    cross_cloud detect_federation
"""
        from modules.cross_cloud import CrossCloudAttackEngine

        engine = CrossCloudAttackEngine()

        if not line.strip():
            self._cmd.poutput(f"\n[ Cross-Cloud Attacks ]")
            for method in ["azure_to_aws", "gcp_to_azure", "aws_to_gcp", "imds_harvest", "detect_federation"]:
                self._cmd.poutput(f"    {method}")
            self._cmd.poutput(f"\nUsage: cross_cloud <method>")
            return

        method = line.strip().split()[0].lower()

        if method == "azure_to_aws":
            result = engine.azure_saml_to_aws()
            self._cmd.poutput(f"\n[ Azure AD SAML → AWS ]")
            self._cmd.poutput(f"    Attack Path: {result['attack_path']}")
            for step in result.get('steps', []):
                self._cmd.poutput(f"        {step}")
            self._cmd.poutput(f"\n    Commands:")
            for cmd in result.get('commands', []):
                self._cmd.poutput(f"        $ {cmd}")

        elif method == "gcp_to_azure":
            result = engine.gcp_oidc_to_azure()
            self._cmd.poutput(f"\n[ GCP OIDC → Azure ]")
            self._cmd.poutput(f"    Attack Path: {result['attack_path']}")
            for step in result.get('steps', []):
                self._cmd.poutput(f"        {step}")
            self._cmd.poutput(f"\n    Commands:")
            for cmd in result.get('commands', []):
                self._cmd.poutput(f"        $ {cmd}")

        elif method == "aws_to_gcp":
            result = engine.aws_oidc_to_gcp()
            self._cmd.poutput(f"\n[ AWS OIDC → GCP ]")
            self._cmd.poutput(f"    Attack Path: {result['attack_path']}")
            for step in result.get('steps', []):
                self._cmd.poutput(f"        {step}")
            self._cmd.poutput(f"\n    Commands:")
            for cmd in result.get('commands', []):
                self._cmd.poutput(f"        $ {cmd}")

        elif method == "imds_harvest":
            result = engine.multi_cloud_imds_harvesting()
            self._cmd.poutput(f"\n[ Multi-Cloud IMDS Harvesting ]")
            for provider, cmds in result.items():
                if provider == "attack_type":
                    continue
                self._cmd.poutput(f"\n    [{provider}]")
                for cmd in cmds[:2]:
                    self._cmd.poutput(f"        $ {cmd}")

        elif method == "detect_federation":
            result = engine.detect_cross_cloud_federation()
            self._cmd.poutput(f"\n[ Cross-Cloud Federation Detection ]")
            for cloud, cmds in result.items():
                if cloud == "attack_type":
                    continue
                self._cmd.poutput(f"\n    [{cloud}]")
                for cmd in cmds:
                    self._cmd.poutput(f"        $ {cmd}")

        else:
            self._cmd.perror(f"Unknown method: {method}")

    def do_saas_enum(self, line: str) -> None:
        """Enumerate SaaS platforms — M365, Google Workspace, Salesforce, Slack, ServiceNow.

Usage: saas_enum <platform>

Platforms: m365, google_workspace, salesforce, servicenow, slack, all

Examples:
    saas_enum m365
    saas_enum slack
    saas_enum all
"""
        from modules.saas_attacks import SaaSAttackEngine, SaaSEnumerationTools

        if not line.strip():
            self._cmd.poutput(f"\n[ SaaS Platforms ]")
            for p in ["m365", "google_workspace", "salesforce", "servicenow", "slack"]:
                self._cmd.poutput(f"    {p}")
            self._cmd.poutput(f"\nUsage: saas_enum <platform>")
            return

        platform = line.strip().split()[0].lower()

        if platform == "m365":
            data = SaaSEnumerationTools.microsoft365_commands()
            self._cmd.poutput(f"\n[ Microsoft 365 Enumeration ]")
            for category, cmds in data.items():
                self._cmd.poutput(f"\n    [{category}]")
                for cmd in cmds[:2]:
                    self._cmd.poutput(f"        $ {cmd}")

        elif platform == "google_workspace":
            data = SaaSEnumerationTools.google_workspace_commands()
            self._cmd.poutput(f"\n[ Google Workspace Enumeration ]")
            for category, cmds in data.items():
                self._cmd.poutput(f"\n    [{category}]")
                for cmd in cmds[:2]:
                    self._cmd.poutput(f"        $ {cmd}")

        elif platform == "salesforce":
            data = SaaSEnumerationTools.salesforce_commands()
            self._cmd.poutput(f"\n[ Salesforce Enumeration ]")
            for category, cmds in data.items():
                self._cmd.poutput(f"\n    [{category}]")
                for cmd in cmds[:2]:
                    self._cmd.poutput(f"        $ {cmd}")

        elif platform == "servicenow":
            data = SaaSEnumerationTools.servicenow_commands()
            self._cmd.poutput(f"\n[ ServiceNow Enumeration ]")
            for category, cmds in data.items():
                self._cmd.poutput(f"\n    [{category}]")
                for cmd in cmds[:2]:
                    self._cmd.poutput(f"        $ {cmd}")

        elif platform == "slack":
            eng = SaaSAttackEngine()
            result = eng.slack_data_mining()
            self._cmd.poutput(f"\n[ Slack Data Mining ]")
            self._cmd.poutput(f"\n    Search terms:")
            for term in result.get('search_terms', [])[:10]:
                self._cmd.poutput(f"        {term}")
            self._cmd.poutput(f"\n    API Endpoints:")
            for endpoint in result.get('api_endpoints', [])[:3]:
                self._cmd.poutput(f"        GET {endpoint}")

        elif platform == "all":
            engine = SaaSAttackEngine()
            result = engine.enumerate_all()
            self._cmd.poutput(f"\n[ All SaaS Platforms ]")
            for plat, cmds in result.items():
                self._cmd.poutput(f"\n    [{plat}]")
                for category, commands in cmds.items():
                    self._cmd.poutput(f"        {category}: {len(commands)} commands available")
            self._cmd.poutput(f"")

        else:
            self._cmd.perror(f"Unknown platform: {platform}")
