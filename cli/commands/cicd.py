"""CI/CD Enumeration command set.

Phase 02/03 — commands for enumerating CI/CD platforms, scanning build logs
for secrets, and abusing pipeline misconfigurations.
"""

from __future__ import annotations

import json
import os

import cmd2

from cli.commands._base import LazyOwnCommandSet
from utils import (
    GREEN,
    RED,
    RESET,
    YELLOW,
    print_error,
    print_msg,
    print_succ,
    print_warn,
)

CICD_CATEGORY = "20. CI/CD Pipeline Attacks"


class CICDCommandSet(LazyOwnCommandSet):
    """CI/CD pipeline enumeration and attack commands."""

    phase = "recon"
    category = CICD_CATEGORY

    @cmd2.with_category(CICD_CATEGORY)
    def do_cicd_scan(self, line=""):
        """Scan CI/CD platform for security misconfigurations.

        Usage: cicd_scan --url <platform_url> [--type jenkins|gitlab|github|azure|bitbucket]

        Enumerates:
        - Exposed API endpoints
        - Credential stores
        - Pipeline configurations with potential secret leakage
        - Unauthenticated access vectors
        """
        import shlex
        args = shlex.split(line) if line else []

        url = self._extract(args, "--url")
        platform_type = self._extract(args, "--type") or ""

        if not url:
            rhost = self.params.get("rhost", "")
            if rhost:
                url = input(f"Platform URL (default: http://{rhost}:8080): ") or f"http://{rhost}:8080"
            else:
                print_error("Usage: cicd_scan --url <platform_url> [--type jenkins|gitlab|github|azure]")
                return

        try:
            from modules.cicd_enumerator import CICDEnumerator
        except ImportError as exc:
            print_error(f"CI/CD module not available: {exc}")
            return

        enumerator = CICDEnumerator(target_url=url)
        findings = enumerator.scan()

        if platform_type:
            findings = [f for f in findings if platform_type.lower() in f.platform.lower()]

        findings_file = enumerator.export_findings()
        matrix_file = enumerator.generate_ci_attack_matrix()

        crit = [f for f in findings if f.severity == "critical"]
        high = [f for f in findings if f.severity == "high"]

        print_msg(f"\n{GREEN}CI/CD Scan Results for {url}{RESET}")
        print_msg(f"  Total findings: {len(findings)}")
        print_msg(f"  {RED}Critical: {len(crit)}{RESET}")
        print_msg(f"  {YELLOW}High: {len(high)}{RESET}")

        if crit:
            print_msg(f"\n{RED}Critical findings:{RESET}")
            for f in crit:
                print_msg(f"  {RED}[{f.platform}]{RESET} {f.finding_type} — {f.url}")

        if high:
            print_msg(f"\n{YELLOW}High severity findings:{RESET}")
            for f in high:
                print_msg(f"  {YELLOW}[{f.platform}]{RESET} {f.finding_type} — {f.url}")

        print_succ(f"\nFindings: {findings_file}")
        print_succ(f"Attack matrix: {matrix_file}")

    @cmd2.with_category(CICD_CATEGORY)
    def do_cicd_secrets(self, line=""):
        """Scan build log for leaked secrets.

        Usage: cicd_secrets [--file <path>] [--input <text>]

        Scans provided text or file for common secret patterns:
        passwords, API keys, tokens, SSH keys, AWS keys, database
        connection strings, and package registry tokens.
        """
        import shlex
        args = shlex.split(line) if line else []

        try:
            from modules.cicd_enumerator import CICDEnumerator
        except ImportError as exc:
            print_error(f"CI/CD module not available: {exc}")
            return

        input_text = self._extract(args, "--input") or ""
        file_path = self._extract(args, "--file")

        if file_path and os.path.exists(file_path):
            with open(file_path) as f:
                input_text = f.read()
            print_msg(f"Scanning {file_path} ({len(input_text)} chars)")

        if not input_text:
            print_error("Usage: cicd_secrets --file <path_to_build_log>")
            print_error("       cicd_secrets --input '<text_to_scan>'")
            return

        enumerator = CICDEnumerator()
        secrets = enumerator.scan_build_log(input_text, source=file_path or "stdin")

        if secrets:
            print_msg(f"\n{RED}Found {len(secrets)} potential secrets:{RESET}")
            for s in secrets:
                print_msg(f"  [{s['type']}] {s['category']} — {s['evidence']}")
        else:
            print_msg("No obvious secrets detected.")

    @cmd2.with_category(CICD_CATEGORY)
    def do_jenkins_enum(self, line=""):
        """Enumerate a Jenkins instance.

        Usage: jenkins_enum --url <jenkins_url>

        Checks for: Script Console access, credential store exposure,
        unauthenticated API, build agent enumeration, console output
        with potential secret leakage.
        """
        import shlex
        args = shlex.split(line) if line else []

        url = self._extract(args, "--url") or self.params.get("url", "")

        if not url:
            print_error("Usage: jenkins_enum --url <http://jenkins.example.com:8080>")
            return

        endpoints = [
            ("/api/json", "API Status"),
            ("/script", "Script Console"),
            ("/credentials/store/system/domain/_/api/json", "Credential Store API"),
            ("/computer/api/json", "Agent List"),
            ("/job/", "Job List"),
            ("/asynchPeople/api/json", "User List"),
            ("/pluginManager/api/json", "Plugin List"),
            ("/userContent/", "User Content"),
            ("/manage/", "Manage Jenkins"),
            ("/configureSecurity/", "Security Config"),
        ]

        print_msg(f"Enumerating Jenkins: {url}")
        for path, name in endpoints:
            full_url = f"{url.rstrip('/')}{path}"
            print_msg(f"  [{name}] {full_url}")
            self.cmd(f"curl -sk -o /dev/null -w '%{{http_code}}' '{full_url}' 2>/dev/null || echo 'unreachable'")

        output_dir = self.params.get("sessions_dir", "sessions")
        os.makedirs(output_dir, exist_ok=True)
        self.cmd(f"python3 modules/jenkins-cli/jenkins-cli.py -s {url} -g -o {output_dir}/jenkins_config.xml 2>/dev/null || echo ''")

    @cmd2.with_category(CICD_CATEGORY)
    def do_gitlab_enum(self, line=""):
        """Enumerate a GitLab instance.

        Usage: gitlab_enum --url <gitlab_url>

        Checks for: Public projects, API accessibility, CI lint API,
        runner enumeration, GraphQL API, version disclosure.
        """
        import shlex
        args = shlex.split(line) if line else []

        url = self._extract(args, "--url") or self.params.get("url", "")

        if not url:
            print_error("Usage: gitlab_enum --url <https://gitlab.example.com>")
            return

        base = url.rstrip("/")

        endpoints = [
            ("/api/v4/version", "Version"),
            ("/api/v4/projects?visibility=public&per_page=100", "Public Projects"),
            ("/api/v4/groups?per_page=100", "Groups"),
            ("/api/v4/users?per_page=100", "Users"),
            ("/explore", "Explore Page"),
            ("/help", "Help Page"),
            ("/api/v4/runners", "Runners"),
        ]

        print_msg(f"Enumerating GitLab: {url}")
        for path, name in endpoints:
            full_url = f"{base}{path}"
            print_msg(f"  [{name}] {full_url}")
            self.cmd(f"curl -sk -o /dev/null -w '%{{http_code}}' '{full_url}' 2>/dev/null || echo 'unreachable'")

        print_msg("\nChecking for .gitlab-ci.yml exposure:")
        ci_endpoints = [
            f"{base}/.gitlab-ci.yml",
            f"{base}/api/v4/ci/lint",
        ]
        for ep in ci_endpoints:
            print_msg(f"  {ep}")
            self.cmd(f"curl -sk '{ep}' 2>/dev/null | head -20")

    @cmd2.with_category(CICD_CATEGORY)
    def do_mfa_bypass(self, line=""):
        """Enumerate and test MFA bypass techniques.

        Usage: mfa_bypass --domain <target.com> [--idp <okta|azure|duo>]

        Analyzes target MFA posture and recommends bypass techniques:
        - Session cookie theft and replay
        - Push notification bombing/fatigue
        - Legacy protocol enumeration (IMAP/POP3/SMTP)
        - Conditional Access policy gaps
        - SAML assertion forging
        - Device code phishing templates
        """
        import shlex
        args = shlex.split(line) if line else []

        domain = self._extract(args, "--domain") or self.params.get("domain", "")
        idp_type = self._extract(args, "--idp") or ""

        if not domain:
            print_error("Usage: mfa_bypass --domain <target.com> [--idp <okta|azure|duo>]")
            return

        try:
            from modules.mfa_bypass import MFABypassEngine, MFATarget, MFA_TECHNIQUES
        except ImportError as exc:
            print_error(f"MFA bypass module not available: {exc}")
            return

        target = MFATarget(domain=domain, idp_type=idp_type)
        engine = MFABypassEngine()

        techniques = engine.enumerate_techniques(target)
        templates = engine.generate_phishing_templates(target)

        print_msg(f"\n{YELLOW}MFA Bypass Analysis for {domain}{RESET}")
        print_msg(f"IDP Type: {idp_type or 'auto-detect'}")
        print_msg(f"\n{YELLOW}Viable techniques ({len(techniques)}):{RESET}")
        for t in techniques:
            print_msg(f"  {GREEN}{t['name']}{RESET} [{', '.join(t['target_protocols'][:3])}]")
            print_msg(f"    {t['description']}")
            print_msg(f"    Tools: {', '.join(t['tools'][:3])}")

        if templates:
            print_msg(f"\n{YELLOW}Phishing templates ({len(templates)}):{RESET}")
            for t in templates:
                print_msg(f"  {GREEN}{t['name']}{RESET} ({t['type']})")
                print_msg(f"    {t['description']}")

        ca_scan = engine.mfa_conditional_access_scan(domain)
        print_msg(f"\n{YELLOW}Conditional Access scan commands:{RESET}")
        for tool, cmd in ca_scan.get("tools", {}).items():
            print_msg(f"  {tool}: {cmd}")

        report = engine.export_report()
        print_succ(f"\nMFA bypass report: {report}")

    @staticmethod
    def _extract(args: list[str], flag: str) -> str | None:
        try:
            idx = args.index(flag)
            return args[idx + 1]
        except (ValueError, IndexError):
            return None


__all__ = ["CICDCommandSet"]
