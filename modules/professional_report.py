"""Professional Red Team Report Generator.

Produces client-ready pentest/red-team reports in HTML, PDF, and Markdown
formats. Reads from the world model, session data, and credential stores to
auto-generate structured findings with CVSS scores, evidence, and
remediation recommendations.

Architecture:
    DataCollector -> FindingClassifier -> RiskScorer -> ReportAssembler -> OutputWriter

Output formats:
    HTML  — standalone responsive page with collapsible sections and dark mode.
    PDF   — via wkhtmltopdf (if available) or weasyprint.
    MD    — markdown for further editing or wiki integration.
    JSON  — machine-readable findings for API/CI integration.

Security:
    No credentials in rendered reports by default — only usernames and hashes
    are included if ``include_credentials`` is explicitly set.

Usage:
    from modules.professional_report import RedTeamReportGenerator
    gen = RedTeamReportGenerator()
    gen.generate(output_dir="reports/")
"""

from __future__ import annotations

import json
import os
import subprocess
import textwrap
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

BASE_DIR = Path(__file__).resolve().parent.parent
SESSIONS_DIR = BASE_DIR / "sessions"
PAYLOAD_PATH = BASE_DIR / "payload.json"

REPORT_STYLES = """
:root {
    --bg: #0d1117; --fg: #c9d1d9; --accent: #58a6ff;
    --border: #30363d; --critical: #f85149; --high: #d29922;
    --medium: #58a6ff; --low: #3fb950; --info: #8b949e;
}
* { box-sizing: border-box; margin: 0; padding: 0; }
body { font-family: 'Segoe UI', system-ui, sans-serif; background: var(--bg); color: var(--fg); line-height: 1.6; }
.container { max-width: 1100px; margin: 0 auto; padding: 2rem; }
h1 { font-size: 2rem; border-bottom: 2px solid var(--accent); padding-bottom: .5rem; margin-bottom: 1rem; }
h2 { font-size: 1.5rem; margin: 2rem 0 1rem; color: var(--accent); }
h3 { margin: 1rem 0 .5rem; }
.header-meta { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 0.5rem; margin-bottom: 2rem; }
.meta-item { background: #161b22; border: 1px solid var(--border); border-radius: 6px; padding: 0.75rem; }
.meta-label { font-size: 0.75rem; color: var(--info); text-transform: uppercase; }
.meta-value { font-size: 1rem; font-weight: 600; }
.finding { background: #161b22; border: 1px solid var(--border); border-radius: 8px; margin-bottom: 1rem; overflow: hidden; }
.finding-header { display: flex; justify-content: space-between; align-items: center; padding: 1rem; cursor: pointer; }
.finding-header:hover { background: #1c2128; }
.finding-title { font-weight: 600; flex: 1; }
.severity { padding: 0.25rem 0.75rem; border-radius: 12px; font-size: 0.75rem; font-weight: 700; text-transform: uppercase; margin-left: 1rem; }
.severity.critical { background: #490202; color: var(--critical); }
.severity.high { background: #341a00; color: var(--high); }
.severity.medium { background: #04260f; color: var(--medium); }
.severity.low { background: #0d2818; color: var(--low); }
.severity.info { background: #1a2233; color: var(--info); }
.finding-body { padding: 0 1rem 1rem; display: none; }
.finding-body.open { display: block; }
.evidence { background: #0d1117; border: 1px solid var(--border); border-radius: 4px; padding: 0.75rem; margin: 0.5rem 0; font-family: monospace; font-size: 0.85rem; white-space: pre-wrap; overflow-x: auto; }
.remediation { background: #04260f; border-left: 4px solid var(--low); padding: 0.75rem; margin: 0.5rem 0; border-radius: 4px; }
.summary-cards { display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 1rem; margin-bottom: 2rem; }
.summary-card { background: #161b22; border: 1px solid var(--border); border-radius: 8px; padding: 1rem; text-align: center; }
.summary-card .count { font-size: 2.5rem; font-weight: 700; }
.summary-card .label { font-size: 0.8rem; color: var(--info); text-transform: uppercase; margin-top: 0.25rem; }
.timeline { border-left: 2px solid var(--border); padding-left: 1.5rem; margin: 1rem 0; }
.timeline-item { position: relative; margin-bottom: 1rem; padding-bottom: 0.5rem; }
.timeline-item::before { content: ''; position: absolute; left: -1.7rem; top: 0.4rem; width: 10px; height: 10px; background: var(--accent); border-radius: 50%; }
.timeline-time { font-size: 0.75rem; color: var(--info); }
code { background: #1c2128; padding: 0.15rem 0.4rem; border-radius: 3px; font-size: 0.85rem; }
table { width: 100%; border-collapse: collapse; margin: 1rem 0; }
th, td { padding: 0.5rem 0.75rem; text-align: left; border-bottom: 1px solid var(--border); }
th { color: var(--accent); font-size: 0.8rem; text-transform: uppercase; }
@media print { body { background: #fff; color: #000; } .finding { break-inside: avoid; } }
"""


@dataclass
class ReportFinding:
    """A single security finding for the report."""

    title: str
    severity: str
    description: str
    evidence: str = ""
    remediation: str = ""
    cvss_score: float = 0.0
    cve_id: str = ""
    affected_hosts: list[str] = field(default_factory=list)
    references: list[str] = field(default_factory=list)


@dataclass
class ReportMetadata:
    """Report header metadata."""

    client: str = "REDACTED"
    engagement_type: str = "External Penetration Test"
    start_date: str = ""
    end_date: str = ""
    testers: list[str] = field(default_factory=list)
    scope: list[str] = field(default_factory=list)
    executive_summary: str = ""


class RedTeamReportGenerator:
    """Generate professional red team reports from session data.

    Public methods:
        collect_data() -> dict
        classify_findings(data) -> list[ReportFinding]
        generate(output_dir, format) -> str
    """

    SEVERITY_ORDER = {"critical": 0, "high": 1, "medium": 2, "low": 3, "info": 4}

    REMEDIATION_TEMPLATES: dict[str, str] = {
        "default_credentials": (
            "Change all default credentials immediately. Implement a password "
            "policy requiring minimum 14 characters with complexity requirements. "
            "Enable account lockout after 5 failed attempts."
        ),
        "weak_password": (
            "Enforce strong password policies across all accounts. Require "
            "minimum 14 characters, uppercase, lowercase, numbers, and special "
            "characters. Implement MFA where possible."
        ),
        "unpatched_service": (
            "Apply vendor security patches immediately. Implement a regular "
            "patch management cycle with vulnerability scanning. Subscribe to "
            "vendor security advisories."
        ),
        "smb_signing_disabled": (
            "Enable SMB signing across all Windows systems via Group Policy. "
            "This prevents NTLM relay attacks and SMB man-in-the-middle."
        ),
        "ldap_signing": (
            "Enable LDAP signing and channel binding to prevent relay attacks. "
            "Configure via Group Policy: Network security: LDAP client signing "
            "requirements."
        ),
        "null_session": (
            "Disable anonymous SMB/NetBIOS access. Configure RestrictAnonymous=1 "
            "in the registry. Block ports 139/445 at the perimeter firewall."
        ),
        "kerberoasting": (
            "Use managed service accounts (MSAs/gMSAs) with long complex passwords. "
            "Audit SPNs regularly. Monitor Event ID 4769 for unusual TGS requests."
        ),
        "asrep_roasting": (
            "Disable Kerberos pre-authentication requirement only when absolutely "
            "necessary. Audit accounts with DONT_REQUIRE_PREAUTH flag."
        ),
        "exposed_service": (
            "Restrict exposed services to required IP ranges only. Implement "
            "network segmentation and zero-trust architecture. Use a VPN or "
            "bastion host for administrative access."
        ),
        "insecure_protocol": (
            "Disable legacy protocols (FTP, Telnet, SMBv1, HTTP where HTTPS is "
            "available). Migrate to encrypted alternatives with modern cipher suites."
        ),
    }

    def __init__(self, include_credentials: bool = False) -> None:
        self._include_creds = include_credentials
        self._findings: list[ReportFinding] = []
        self._metadata = ReportMetadata()
        self._world_model: dict[str, Any] = {}

    def collect_data(self) -> dict[str, Any]:
        """Collect all available engagement data from sessions directory.

        Returns:
            Dict with world_model, scan_data, credentials, sessions, timeline.
        """
        data: dict[str, Any] = {
            "world_model": self._load_json("world_model.json"),
            "credentials": [],
            "sessions": [],
            "scan_files": [],
            "timeline": [],
        }

        for cred_file in sorted(SESSIONS_DIR.glob("credentials*.txt")):
            try:
                content = cred_file.read_text(errors="replace")
                data["credentials"].extend(
                    line.strip() for line in content.split("\n") if line.strip()
                )
            except OSError:
                continue

        for session_file in sorted(SESSIONS_DIR.glob("session_*.json")):
            session_data = self._load_json(session_file.name)
            if session_data:
                data["sessions"].append(session_data)

        for scan_file in sorted(SESSIONS_DIR.glob("scan_*.nmap")):
            data["scan_files"].append(str(scan_file))

        data["hosts"] = self._world_model.get("targets", [])
        if not data["hosts"] and isinstance(self._world_model, dict):
            if "rhost" in self._world_model:
                data["hosts"].append(self._world_model)

        data["vulnerabilities"] = self._world_model.get("vulnerabilities", [])

        return data

    def classify_findings(self, data: dict[str, Any]) -> list[ReportFinding]:
        """Classify collected data into structured findings.

        Args:
            data: Data dict from collect_data().

        Returns:
            List of classified ReportFinding objects.
        """
        findings: list[ReportFinding] = []

        services_data = data.get("world_model", {}).get("services", [])
        hosts = data.get("hosts", [])

        if isinstance(hosts, dict):
            hosts = [hosts]

        findings.extend(self._classify_services(services_data, hosts))
        findings.extend(self._classify_vulnerabilities(data.get("vulnerabilities", []), hosts))
        findings.extend(self._classify_credentials(data.get("credentials", []), hosts))
        findings.extend(self._classify_sessions(data.get("sessions", []), hosts))

        findings.sort(
            key=lambda f: self.SEVERITY_ORDER.get(f.severity.lower(), 99)
        )

        self._findings = findings
        return findings

    def generate(
        self,
        output_dir: str = "reports",
        output_format: str = "html",
        client_name: str = "",
        engagement_type: str = "",
    ) -> str:
        """Generate the report in the specified format.

        Args:
            output_dir: Directory to write the report.
            output_format: One of html, pdf, md, json.
            client_name: Client name for the header.
            engagement_type: Engagement type string.

        Returns:
            Path to the generated report.
        """
        data = self.collect_data()
        self.classify_findings(data)

        self._metadata = ReportMetadata(
            client=client_name or "REDACTED",
            engagement_type=engagement_type or "External Penetration Test",
            start_date=datetime.now(timezone.utc).strftime("%Y-%m-%d"),
            end_date=datetime.now(timezone.utc).strftime("%Y-%m-%d"),
            scope=self._extract_scope(data),
        )

        out_path = Path(output_dir)
        out_path.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        if output_format == "html":
            return self._generate_html(out_path, timestamp)
        if output_format == "md":
            return self._generate_markdown(out_path, timestamp)
        if output_format == "json":
            return self._generate_json(out_path, timestamp)
        if output_format == "pdf":
            html_path = self._generate_html(out_path, timestamp)
            return self._html_to_pdf(html_path)

        return ""

    def _generate_html(self, out_path: Path, timestamp: str) -> str:
        """Generate an HTML report.

        Args:
            out_path: Output directory path.
            timestamp: Timestamp string for filename.

        Returns:
            Path to the generated HTML file.
        """
        filename = f"lazyown_report_{timestamp}.html"
        filepath = out_path / filename

        severity_counts = {"critical": 0, "high": 0, "medium": 0, "low": 0, "info": 0}
        for f in self._findings:
            sev = f.severity.lower()
            if sev in severity_counts:
                severity_counts[sev] += 1

        summary_cards = ""
        colors = {"critical": "var(--critical)", "high": "var(--high)",
                   "medium": "var(--medium)", "low": "var(--low)", "info": "var(--info)"}
        for sev, count in severity_counts.items():
            if count > 0:
                summary_cards += (
                    f'<div class="summary-card">'
                    f'<div class="count" style="color:{colors.get(sev, "var(--info)")}">{count}</div>'
                    f'<div class="label">{sev.upper()}</div>'
                    f'</div>'
                )

        findings_html = ""
        for idx, finding in enumerate(self._findings):
            cvss_html = ""
            if finding.cvss_score > 0:
                cvss_html = f'<div style="margin-top:0.5rem;"><strong>CVSS:</strong> {finding.cvss_score}</div>'

            cve_html = ""
            if finding.cve_id:
                cve_html = f'<div><strong>CVE:</strong> {finding.cve_id}</div>'

            hosts_html = ""
            if finding.affected_hosts:
                hosts_html = f'<div><strong>Affected Hosts:</strong> {", ".join(finding.affected_hosts)}</div>'

            refs_html = ""
            if finding.references:
                refs = "<br>".join(finding.references)
                refs_html = f'<div style="margin-top:0.5rem;"><strong>References:</strong><br>{refs}</div>'

            evidence_block = ""
            if finding.evidence:
                evidence_escaped = finding.evidence.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
                evidence_block = f'<div class="evidence">{evidence_escaped}</div>'

            remediation_block = ""
            if finding.remediation:
                remediation_block = f'<div class="remediation"><strong>Remediation:</strong> {finding.remediation}</div>'

            findings_html += f"""
            <div class="finding">
                <div class="finding-header" onclick="this.nextElementSibling.classList.toggle('open')">
                    <span class="finding-title">{finding.title}</span>
                    <span class="severity {finding.severity.lower()}">{finding.severity}</span>
                </div>
                <div class="finding-body">
                    <p>{finding.description}</p>
                    {cvss_html}
                    {cve_html}
                    {hosts_html}
                    {evidence_block}
                    {remediation_block}
                    {refs_html}
                </div>
            </div>"""

        executive_summary = ""
        if self._findings:
            criticals = severity_counts["critical"]
            highs = severity_counts["high"]
            exec_lines = [
                f"This penetration test identified {len(self._findings)} security findings "
                f"across the target environment.",
            ]
            if criticals > 0:
                exec_lines.append(
                    f"<strong>{criticals} Critical</strong> findings require "
                    f"immediate remediation."
                )
            if highs > 0:
                exec_lines.append(
                    f"<strong>{highs} High</strong> severity issues were discovered "
                    f"that pose significant risk to the organization."
                )
            exec_lines.append(
                "Detailed findings with evidence and remediation guidance are "
                "provided below. We recommend addressing Critical and High "
                "findings within 30 days."
            )
            executive_summary = "".join(f"<p>{line}</p>" for line in exec_lines)

        scope_html = "<br>".join(self._metadata.scope) if self._metadata.scope else "Not specified"
        testers_html = ", ".join(self._metadata.testers) if self._metadata.testers else "LazyOwn Red Team"

        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Red Team Engagement Report — {self._metadata.client}</title>
<style>{REPORT_STYLES}</style>
</head>
<body>
<div class="container">

<h1>Red Team Engagement Report</h1>

<div class="header-meta">
    <div class="meta-item"><div class="meta-label">Client</div><div class="meta-value">{self._metadata.client}</div></div>
    <div class="meta-item"><div class="meta-label">Engagement Type</div><div class="meta-value">{self._metadata.engagement_type}</div></div>
    <div class="meta-item"><div class="meta-label">Date</div><div class="meta-value">{self._metadata.start_date}</div></div>
    <div class="meta-item"><div class="meta-label">Classification</div><div class="meta-value">CONFIDENTIAL</div></div>
    <div class="meta-item"><div class="meta-label">Testers</div><div class="meta-value">{testers_html}</div></div>
    <div class="meta-item"><div class="meta-label">Scope</div><div class="meta-value">{scope_html}</div></div>
</div>

<h2>Executive Summary</h2>
{executive_summary}

<h2>Finding Summary</h2>
<div class="summary-cards">{summary_cards}</div>

<h2>Detailed Findings</h2>
{findings_html}

<p style="margin-top:3rem; color:var(--info); text-align:center; font-size:0.8rem;">
    Generated by LazyOwn Red Team Framework &mdash; {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} UTC
</p>

</div>
</body>
</html>"""

        filepath.write_text(html)
        return str(filepath)

    def _generate_markdown(self, out_path: Path, timestamp: str) -> str:
        """Generate a Markdown report.

        Args:
            out_path: Output directory path.
            timestamp: Timestamp string.

        Returns:
            Path to the generated MD file.
        """
        filename = f"lazyown_report_{timestamp}.md"
        filepath = out_path / filename

        lines: list[str] = [
            f"# Red Team Engagement Report — {self._metadata.client}",
            "",
            f"**Engagement Type:** {self._metadata.engagement_type}",
            f"**Date:** {self._metadata.start_date}",
            f"**Classification:** CONFIDENTIAL",
            "",
            "---",
            "",
            "## Executive Summary",
            "",
        ]

        for finding in self._findings:
            lines.extend([
                f"### {finding.title}",
                f"",
                f"**Severity:** {finding.severity.upper()}",
                f"",
                finding.description,
                f"",
            ])
            if finding.cvss_score:
                lines.append(f"**CVSS Score:** {finding.cvss_score}")
                lines.append("")
            if finding.cve_id:
                lines.append(f"**CVE:** {finding.cve_id}")
                lines.append("")
            if finding.evidence:
                lines.append("**Evidence:**")
                lines.append("```")
                lines.append(finding.evidence[:2000])
                lines.append("```")
                lines.append("")
            if finding.remediation:
                lines.append(f"**Remediation:** {finding.remediation}")
                lines.append("")

        lines.extend([
            "---",
            f"*Generated by LazyOwn Red Team Framework — {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} UTC*",
        ])

        filepath.write_text("\n".join(lines))
        return str(filepath)

    def _generate_json(self, out_path: Path, timestamp: str) -> str:
        """Generate a JSON report.

        Args:
            out_path: Output directory path.
            timestamp: Timestamp string.

        Returns:
            Path to the generated JSON file.
        """
        filename = f"lazyown_report_{timestamp}.json"
        filepath = out_path / filename

        data = {
            "metadata": {
                "client": self._metadata.client,
                "engagement_type": self._metadata.engagement_type,
                "date": self._metadata.start_date,
                "generated": datetime.now().isoformat(),
            },
            "findings": [
                {
                    "title": f.title,
                    "severity": f.severity,
                    "description": f.description,
                    "evidence": f.evidence[:2000] if f.evidence else "",
                    "remediation": f.remediation,
                    "cvss_score": f.cvss_score,
                    "cve_id": f.cve_id,
                    "affected_hosts": f.affected_hosts,
                    "references": f.references,
                }
                for f in self._findings
            ],
        }

        filepath.write_text(json.dumps(data, indent=2))
        return str(filepath)

    def _html_to_pdf(self, html_path: str) -> str:
        """Convert HTML report to PDF.

        Args:
            html_path: Path to HTML file.

        Returns:
            Path to the generated PDF file.
        """
        pdf_path = html_path.replace(".html", ".pdf")
        converters = ["wkhtmltopdf", "weasyprint"]

        for converter in converters:
            try:
                if converter == "wkhtmltopdf":
                    subprocess.run(
                        ["wkhtmltopdf", "--quiet", html_path, pdf_path],
                        check=True, timeout=60,
                    )
                    return pdf_path
                if converter == "weasyprint":
                    subprocess.run(
                        ["weasyprint", html_path, pdf_path],
                        check=True, timeout=60,
                    )
                    return pdf_path
            except (subprocess.CalledProcessError, FileNotFoundError, Exception):
                continue

        return html_path

    def _classify_services(
        self,
        services: list[dict[str, Any]],
        hosts: list[dict[str, Any]],
    ) -> list[ReportFinding]:
        """Classify service data into findings.

        Args:
            services: List of service dicts from world model.
            hosts: List of host dicts.

        Returns:
            List of ReportFinding objects from services.
        """
        findings: list[ReportFinding] = []
        host_ips = [h.get("ip", h.get("address", "")) for h in hosts if isinstance(h, dict)]

        insecure_ports = {
            21: "FTP — cleartext authentication",
            23: "Telnet — cleartext authentication",
            25: "SMTP — potential open relay",
            139: "NetBIOS — legacy protocol",
            445: "SMB — potential null session",
            3306: "MySQL default port",
            3389: "RDP — exposed remote desktop",
        }

        for svc in services:
            port = int(svc.get("port", 0))
            protocol = svc.get("protocol", "tcp")
            name = svc.get("name", "")
            product = svc.get("product", "")

            if port in insecure_ports:
                findings.append(
                    ReportFinding(
                        title=f"Insecure Service: {name or port}/{protocol} on port {port}",
                        severity="medium",
                        description=(
                            f"The service {name or product or 'unknown'} is exposed "
                            f"on port {port}/{protocol}. {insecure_ports.get(port, '')} "
                            f"This increases the attack surface and may allow unauthorized "
                            f"access or information disclosure."
                        ),
                        evidence=f"Port: {port}/{protocol}\nService: {name}\nProduct: {product}",
                        remediation=self.REMEDIATION_TEMPLATES.get(
                            "insecure_protocol",
                            "Restrict access and disable legacy protocols.",
                        ),
                        affected_hosts=list(host_ips) if host_ips else ["unknown"],
                    )
                )

        return findings

    def _classify_vulnerabilities(
        self,
        vulns: list[dict[str, Any]],
        hosts: list[dict[str, Any]],
    ) -> list[ReportFinding]:
        """Classify vulnerability data into findings.

        Args:
            vulns: List of vulnerability dicts.
            hosts: List of host dicts.

        Returns:
            List of ReportFinding objects from vulns.
        """
        findings: list[ReportFinding] = []
        host_ips = [h.get("ip", h.get("address", "")) for h in hosts if isinstance(h, dict)]

        for vuln in vulns:
            title = vuln.get("title", vuln.get("name", "Unknown Vulnerability"))
            severity = vuln.get("severity", "medium")
            description = vuln.get("description", "No description available.")
            cve_id = vuln.get("cve", vuln.get("cve_id", ""))

            findings.append(
                ReportFinding(
                    title=title,
                    severity=severity.lower(),
                    description=description,
                    cve_id=cve_id,
                    evidence=json.dumps(vuln, indent=2),
                    remediation=self.REMEDIATION_TEMPLATES.get(
                        "unpatched_service",
                        "Apply vendor security patches.",
                    ),
                    cvss_score=float(vuln.get("cvss", 0)),
                    affected_hosts=list(host_ips) if host_ips else ["unknown"],
                    references=vuln.get("references", []),
                )
            )

        return findings

    def _classify_credentials(
        self,
        credentials: list[str],
        hosts: list[dict[str, Any]],
    ) -> list[ReportFinding]:
        """Classify credential data into findings.

        Args:
            credentials: List of credential lines.
            hosts: List of host dicts.

        Returns:
            List of ReportFinding objects from credentials.
        """
        findings: list[ReportFinding] = []
        host_ips = [h.get("ip", h.get("address", "")) for h in hosts if isinstance(h, dict)]

        if not credentials:
            return findings

        weak_creds_found = False
        default_creds_found = False
        weak_patterns = [
            "admin:admin", "root:root", "administrator:", "guest:",
            "password", "123456", "qwerty", "welcome", "letmein",
        ]

        for line in credentials:
            line_lower = line.lower()
            for pattern in weak_patterns:
                if pattern in line_lower:
                    weak_creds_found = True
                    break
            if "default" in line_lower:
                default_creds_found = True

        if weak_creds_found:
            findings.append(
                ReportFinding(
                    title="Weak Credentials Discovered",
                    severity="critical",
                    description=(
                        "Weak or default credentials were discovered during the "
                        "engagement. These credentials can be used by attackers to "
                        "gain unauthorized access to systems and services."
                    ),
                    evidence="\n".join(credentials[:20]) if self._include_creds else "[Redacted]",
                    remediation=self.REMEDIATION_TEMPLATES["weak_password"],
                    affected_hosts=list(host_ips) if host_ips else ["unknown"],
                )
            )

        if default_creds_found:
            findings.append(
                ReportFinding(
                    title="Default Credentials in Use",
                    severity="high",
                    description=(
                        "Default credentials are still configured on one or more "
                        "systems. These are publicly known and trivially exploitable."
                    ),
                    evidence="[Redacted — default credentials confirmed]",
                    remediation=self.REMEDIATION_TEMPLATES["default_credentials"],
                    affected_hosts=list(host_ips) if host_ips else ["unknown"],
                )
            )

        return findings

    def _classify_sessions(
        self,
        sessions: list[dict[str, Any]],
        hosts: list[dict[str, Any]],
    ) -> list[ReportFinding]:
        """Classify session data into findings.

        Args:
            sessions: List of session dicts.
            hosts: List of host dicts.

        Returns:
            List of ReportFinding objects from sessions.
        """
        findings: list[ReportFinding] = []
        host_ips = [h.get("ip", h.get("address", "")) for h in hosts if isinstance(h, dict)]

        if not sessions:
            return findings

        privilege_sessions = [
            s for s in sessions
            if s.get("method") in ("psexec", "wmiexec", "pth")
            or s.get("admin", False)
        ]

        if privilege_sessions:
            findings.append(
                ReportFinding(
                    title="Privileged Access Achieved",
                    severity="critical",
                    description=(
                        f"The engagement team successfully obtained privileged access "
                        f"to {len(privilege_sessions)} systems. This demonstrates that "
                        f"an attacker could achieve domain compromise given the current "
                        f"security posture."
                    ),
                    evidence=f"Sessions obtained: {len(privilege_sessions)}",
                    remediation=(
                        "Implement the Principle of Least Privilege. Segment the "
                        "network. Enable credential guard. Monitor for unusual "
                        "authentication patterns."
                    ),
                    affected_hosts=list(host_ips) if host_ips else ["unknown"],
                )
            )

        return findings

    def _load_json(self, filename: str) -> dict[str, Any]:
        """Safely load a JSON file from sessions.

        Args:
            filename: Filename relative to sessions dir.

        Returns:
            Parsed dict or empty dict.
        """
        path = SESSIONS_DIR / filename
        if not path.exists():
            return {}
        try:
            return json.loads(path.read_text())
        except (json.JSONDecodeError, OSError):
            return {}

    def _extract_scope(self, data: dict[str, Any]) -> list[str]:
        """Extract scope from engagement data.

        Args:
            data: Engagement data dict.

        Returns:
            List of scope strings.
        """
        scope: list[str] = []
        hosts = data.get("hosts", [])
        if isinstance(hosts, list):
            for h in hosts:
                if isinstance(h, dict):
                    ip = h.get("ip", h.get("address", ""))
                    if ip:
                        scope.append(ip)
        return scope


__all__ = [
    "RedTeamReportGenerator",
    "ReportFinding",
    "ReportMetadata",
]
