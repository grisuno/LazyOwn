"""Enhanced reporting commands — professional multi-format reports with
MITRE ATT&CK coverage matrix, timeline visualization, and compliance mapping.

Unifies the three existing report generators (professional_report.py,
report_generator.py, cli/commands/reporting.py) into a single pipeline
with consistent output formats.
"""

from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from pathlib import Path

import cmd2

from cli.commands._base import LazyOwnCommandSet
from modules.db import LazyOwnDB
from utils import (
    miscellaneous_category,
    print_error,
    print_msg,
    print_warn,
    reporting_category,
)

BASE_DIR = Path(__file__).resolve().parent.parent.parent
SESSIONS_DIR = BASE_DIR / "sessions"
REPORTS_DIR = SESSIONS_DIR / "reports"


def _render_mitre_matrix_html(coverage_data: dict, techniques: list[dict]) -> str:
    """Render a MITRE ATT&CK coverage matrix as an HTML table."""
    if not techniques:
        return "<p>No MITRE ATT&CK techniques recorded for this engagement.</p>"

    tactics_order = [
        "reconnaissance", "resource-development", "initial-access",
        "execution", "persistence", "privilege-escalation",
        "defense-evasion", "credential-access", "discovery",
        "lateral-movement", "collection", "command-and-control",
        "exfiltration", "impact",
    ]

    tactics_present: dict[str, list[dict]] = {}
    for t in techniques:
        tactic = t.get("tactic", "unknown")
        tactics_present.setdefault(tactic, []).append(t)

    rows = []
    for tactic in tactics_order:
        if tactic not in tactics_present:
            continue
        for tech in tactics_present[tactic]:
            tid = tech.get("technique_id", "")
            name = tech.get("name", tid)
            status = tech.get("status", "untested")
            status_class = {
                "tested": "status-tested",
                "failed": "status-failed",
                "blocked": "status-blocked",
                "ready": "status-ready",
                "queued": "status-queued",
            }.get(status, "status-untested")
            rows.append(
                f"<tr>"
                f"<td>{tactic.upper().replace('-', ' ')}</td>"
                f"<td>{tid}</td>"
                f"<td>{name}</td>"
                f"<td class='{status_class}'>{status.upper()}</td>"
                f"</tr>"
            )

    if not rows:
        return "<p>No MITRE ATT&CK techniques recorded for this engagement.</p>"

    return (
        f"<h2>MITRE ATT&CK Coverage</h2>\n"
        f"<p>Techniques tested or available for this engagement:</p>\n"
        f"<table class='mitre-matrix'>\n"
        f"<thead><tr><th>Tactic</th><th>ID</th><th>Technique</th><th>Status</th></tr></thead>\n"
        f"<tbody>\n"
        + "\n".join(rows)
        + f"\n</tbody>\n</table>"
    )


class EnhancedReportCommandSet(LazyOwnCommandSet):
    """Professional report generation with MITRE ATT&CK matrix, compliance,
    and multi-format output."""

    phase = "report"
    category = "11. Reporting"

    def _collect_all_findings(self) -> list[dict]:
        """Collect findings from DB and sessions into a unified list."""
        findings: list[dict] = []
        seen: set[str] = set()

        try:
            db = LazyOwnDB()
            db_vulns = db.vuln_list()
            for v in db_vulns:
                key = v.get("cve_id") or v.get("name", str(v))
                if key and key not in seen:
                    seen.add(key)
                    findings.append({
                        "title": v.get("name", "Unknown"),
                        "severity": v.get("severity", "medium"),
                        "description": v.get("description", ""),
                        "cve_id": v.get("cve_id", ""),
                        "cvss_score": v.get("cvss_score"),
                        "affected_hosts": [v.get("host", "target")],
                        "remediation": v.get("remediation", ""),
                        "source": "db",
                    })
        except Exception:
            pass

        try:
            wm_path = SESSIONS_DIR / "world_model.json"
            if wm_path.exists():
                wm = json.loads(wm_path.read_text(encoding="utf-8"))
                for vuln in wm.get("vulnerabilities", []):
                    cve = vuln.get("cve", vuln.get("id", ""))
                    if cve and cve not in seen:
                        seen.add(cve)
                        findings.append({
                            "title": vuln.get("name", vuln.get("description", cve)),
                            "severity": vuln.get("severity", "medium"),
                            "description": vuln.get("description", ""),
                            "cve_id": cve,
                            "cvss_score": vuln.get("cvss"),
                            "affected_hosts": [wm.get("target", "target")],
                            "remediation": "",
                            "source": "world_model",
                        })
        except Exception:
            pass

        return findings

    def _collect_ttp_coverage(self) -> tuple[dict, list[dict]]:
        """Collect MITRE ATT&CK TTP coverage data."""
        techniques: list[dict] = []
        try:
            from modules.ttp_coverage import TTPCoverage
            coverage = TTPCoverage()
            coverage.rebuild_from_operations()
            rows = coverage.matrix().splitlines() if hasattr(coverage, "matrix") else []
            for row in rows:
                parts = row.split()
                if len(parts) >= 2:
                    techniques.append({
                        "technique_id": parts[0],
                        "name": " ".join(parts[1:]),
                        "tactic": "",
                        "status": "tested",
                    })
        except Exception:
            pass

        coverage_dict: dict = {"total": len(techniques)}
        for t in techniques:
            tid = t["technique_id"]
            if tid not in coverage_dict:
                coverage_dict[tid] = t

        return coverage_dict, techniques

    def _collect_timeline(self) -> list[dict]:
        """Collect event timeline from sessions."""
        events: list[dict] = []
        events_path = SESSIONS_DIR / "events.jsonl"
        if events_path.exists():
            try:
                for line in events_path.read_text(encoding="utf-8").splitlines():
                    if line.strip():
                        events.append(json.loads(line))
            except Exception:
                pass
        return sorted(events, key=lambda e: str(e.get("timestamp", "")))

    @cmd2.with_category(reporting_category)
    def do_gen_report(self, line):
        """Generate enhanced professional penetration test reports.

        Usage:
            gen_report generate [name]         — full report (HTML + MD + JSON)
            gen_report mitre                    — MITRE ATT&CK coverage matrix
            gen_report findings                 — vulnerability findings summary
            gen_report timeline                 — engagement event timeline

        Formats:
            HTML  — Dark-mode professional report with MITRE matrix
            MD    — Markdown for git/notes
            JSON  — Machine-readable for automation

        Examples:
            gen_report generate
            gen_report generate htb_machine
            gen_report mitre
            gen_report findings
            gen_report timeline
        """
        args = line.strip().split()
        if not args:
            print_msg("Usage: gen_report [generate|mitre|findings|timeline] [name]")
            print_msg("Try: gen_report generate")
            return

        action = args[0].lower()
        name = args[1] if len(args) > 1 else ""

        if action == "generate":
            self._report_generate(name)
        elif action == "mitre":
            self._report_mitre()
        elif action == "findings":
            self._report_findings()
        elif action == "timeline":
            self._report_timeline()
        else:
            print_error(f"Unknown action: {action}. Use generate, mitre, findings, or timeline.")

    def _report_generate(self, name: str):
        """Generate a unified multi-format report."""
        REPORTS_DIR.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
        safe_name = (name or "engagement").replace(" ", "_")
        base_name = f"report_{safe_name}_{timestamp}"

        findings = self._collect_all_findings()
        coverage_dict, techniques = self._collect_ttp_coverage()
        timeline = self._collect_timeline()

        severity_order = {"critical": 0, "high": 1, "medium": 2, "low": 3, "info": 4}
        findings.sort(key=lambda f: severity_order.get(f.get("severity", "info"), 99))

        target = self.params.get("rhost", "unknown")
        operator = getattr(self._resolve_shell(), "operator_name", "LazyOwn")

        print_msg(f"Generating report for target: {target}")
        print_msg(f"  Findings: {len(findings)}")
        print_msg(f"  MITRE techniques: {len(techniques)}")
        print_msg(f"  Timeline events: {len(timeline)}")

        findings_html = ""
        for f_data in findings:
            sev = f_data.get("severity", "medium").upper()
            findings_html += (
                f"<div class='finding finding-{f_data.get('severity', 'medium')}'>"
                f"<h3>[{sev}] {f_data.get('title', 'Untitled')}</h3>"
            )
            if f_data.get("cve_id"):
                findings_html += f"<p class='cve'>CVE: {f_data['cve_id']}</p>"
            if f_data.get("cvss_score"):
                findings_html += f"<p class='cvss'>CVSS: {f_data['cvss_score']}</p>"
            if f_data.get("description"):
                findings_html += f"<p>{f_data['description']}</p>"
            if f_data.get("remediation"):
                findings_html += f"<p class='remediation'><strong>Remediation:</strong> {f_data['remediation']}</p>"
            findings_html += "</div>\n"

        mitre_html = _render_mitre_matrix_html(coverage_dict, techniques)

        severity_counts: dict[str, int] = {}
        for f_data in findings:
            sev = f_data.get("severity", "info")
            severity_counts[sev] = severity_counts.get(sev, 0) + 1
        summary_rows = ""
        for sev, count in severity_counts.items():
            summary_rows += f"<tr><td>{sev.upper()}</td><td>{count}</td></tr>\n"

        timeline_html = ""
        for ev in timeline[-20:]:
            ts = ev.get("timestamp", "")
            etype = ev.get("type", ev.get("event", "?"))
            msg = ev.get("message", ev.get("description", str(ev)))
            timeline_html += (
                f"<tr><td>{ts}</td><td>{etype}</td><td>{str(msg)[:120]}</td></tr>\n"
            )

        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>LazyOwn Red Team Report — {target}</title>
<style>
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: #0d1117; color: #c9d1d9; line-height: 1.6; padding: 2rem; }}
.container {{ max-width: 1100px; margin: 0 auto; }}
h1 {{ color: #58a6ff; font-size: 2rem; margin-bottom: 0.5rem; }}
h2 {{ color: #58a6ff; font-size: 1.5rem; margin-top: 2rem; margin-bottom: 1rem; border-bottom: 1px solid #30363d; padding-bottom: 0.5rem; }}
.meta {{ color: #8b949e; font-size: 0.9rem; margin-bottom: 2rem; }}
.finding {{ background: #161b22; border-left: 4px solid #30363d; padding: 1rem; margin-bottom: 1rem; border-radius: 0 6px 6px 0; }}
.finding-critical {{ border-left-color: #ff7b72; }}
.finding-high {{ border-left-color: #ffa657; }}
.finding-medium {{ border-left-color: #d29922; }}
.finding-low {{ border-left-color: #58a6ff; }}
.finding h3 {{ margin-bottom: 0.5rem; }}
.cve {{ color: #8b949e; font-size: 0.85rem; }}
.cvss {{ color: #f85149; font-weight: bold; }}
.remediation {{ color: #7ee787; margin-top: 0.5rem; }}
table {{ width: 100%; border-collapse: collapse; margin: 1rem 0; }}
th, td {{ padding: 0.5rem; text-align: left; border-bottom: 1px solid #21262d; }}
th {{ background: #161b22; color: #8b949e; font-weight: 600; text-transform: uppercase; font-size: 0.8rem; }}
.status-tested {{ color: #7ee787; }}
.status-failed {{ color: #f85149; }}
.status-blocked {{ color: #d29922; }}
.status-ready {{ color: #58a6ff; }}
.status-queued {{ color: #8b949e; }}
</style>
</head>
<body>
<div class="container">
<h1>LazyOwn Red Team Report</h1>
<div class="meta">
<p>Target: {target}</p>
<p>Report generated: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}</p>
<p>Operator: {operator}</p>
<p>Findings: {len(findings)} | Techniques: {len(techniques)} | Events: {len(timeline)}</p>
</div>

<h2>Executive Summary</h2>
<div class="finding">
<p>This report documents the findings of a penetration test conducted against {target}.
{len(findings)} vulnerabilities were identified across {len(severity_counts)} severity levels.
The assessment included reconnaissance, service enumeration, vulnerability scanning, exploitation
attempts, and privilege escalation analysis.</p>
</div>

<h2>Findings Summary</h2>
<table>
<thead><tr><th>Severity</th><th>Count</th></tr></thead>
<tbody>{summary_rows}</tbody>
</table>

<h2>Detailed Findings</h2>
{findings_html or '<p>No vulnerabilities found. The target may be well-hardened or the scan was incomplete.</p>'}

{mitre_html}

<h2>Engagement Timeline</h2>
{('<table><thead><tr><th>Timestamp</th><th>Event</th><th>Details</th></tr></thead><tbody>' + timeline_html + '</tbody></table>') if timeline_html else '<p>No timeline events recorded.</p>'}

<h2>Recommendations</h2>
<div class="finding">
<p>Based on the findings above, we recommend the following prioritized actions:</p>
<ol>
<li>Patch all identified CVEs to the latest vendor-recommended versions.</li>
<li>Disable or restrict unnecessary services exposed to the network.</li>
<li>Implement network segmentation to limit lateral movement paths.</li>
<li>Enforce strong password policies and multi-factor authentication.</li>
<li>Enable logging and monitoring to detect intrusion attempts.</li>
</ol>
</div>

<p style="color: #30363d; margin-top: 3rem; text-align: center; font-size: 0.8rem;">
Generated by LazyOwn Red Team Framework | This report is confidential.
</p>
</div>
</body>
</html>"""

        html_path = REPORTS_DIR / f"{base_name}.html"
        html_path.write_text(html, encoding="utf-8")
        print_msg(f"  HTML report: {html_path}")

        json_report = {
            "metadata": {
                "target": target,
                "operator": operator,
                "generated_at": datetime.now(timezone.utc).isoformat(),
                "finding_count": len(findings),
                "technique_count": len(techniques),
            },
            "findings": findings,
            "mitre_techniques": techniques,
            "timeline": timeline,
        }
        json_path = REPORTS_DIR / f"{base_name}.json"
        json_path.write_text(json.dumps(json_report, indent=2, default=str), encoding="utf-8")
        print_msg(f"  JSON report: {json_path}")

        md_lines = [
            f"# LazyOwn Red Team Report — {target}",
            "",
            f"**Generated:** {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}",
            f"**Operator:** {operator}",
            f"**Findings:** {len(findings)} | **MITRE Techniques:** {len(techniques)}",
            "",
            "## Findings Summary",
            "",
        ]
        for sev, count in severity_counts.items():
            md_lines.append(f"- **{sev.upper()}**: {count}")
        md_lines.append("")

        if findings:
            md_lines.append("## Detailed Findings")
            md_lines.append("")
            for f_data in findings:
                md_lines.append(f"### [{f_data.get('severity', '?').upper()}] {f_data.get('title', 'Untitled')}")
                if f_data.get("cve_id"):
                    md_lines.append(f"**CVE:** {f_data['cve_id']}")
                if f_data.get("description"):
                    md_lines.append(f"\n{f_data['description']}\n")
                if f_data.get("remediation"):
                    md_lines.append(f"**Remediation:** {f_data['remediation']}\n")
                md_lines.append("")

        md_path = REPORTS_DIR / f"{base_name}.md"
        md_path.write_text("\n".join(md_lines), encoding="utf-8")
        print_msg(f"  Markdown report: {md_path}")

        print_msg(f"\nReports saved to: {REPORTS_DIR}/")
        print_msg(f"  {base_name}.html")
        print_msg(f"  {base_name}.json")
        print_msg(f"  {base_name}.md")

    def _report_mitre(self):
        """Display the MITRE ATT&CK coverage matrix."""
        _, techniques = self._collect_ttp_coverage()

        if not techniques:
            print_msg("No MITRE ATT&CK techniques recorded.")
            print_msg("Run operations first to populate TTP coverage.")
            return

        print_msg("\nMITRE ATT&CK Coverage Matrix:\n")

        tactics: dict[str, list[dict]] = {}
        for t in techniques:
            tactic = t.get("tactic", "unknown")
            tactics.setdefault(tactic, []).append(t)

        for tactic, techs in sorted(tactics.items()):
            print_msg(f"  {tactic.upper().replace('-', ' ')}:")
            for tech in techs:
                tid = tech.get("technique_id", "")
                name = tech.get("name", tid)
                status = tech.get("status", "untested")
                print_msg(f"    {tid:<12} {name:<40} [{status}]")
            print_msg("")
        print_msg(f"  Total techniques: {len(techniques)}")

    def _report_findings(self):
        """Display a summary of all vulnerability findings."""
        findings = self._collect_all_findings()

        if not findings:
            print_msg("No vulnerability findings recorded.")
            print_msg("Run: lazynmap && auto_populate && hunt")
            return

        severity_order = {"critical": 0, "high": 1, "medium": 2, "low": 3, "info": 4}
        findings.sort(key=lambda f: severity_order.get(f.get("severity", "info"), 99))

        counts: dict[str, int] = {}
        for f_data in findings:
            sev = f_data.get("severity", "info")
            counts[sev] = counts.get(sev, 0) + 1

        print_msg(f"\nVulnerability Findings ({len(findings)} total):\n")
        print_msg(f"  CRITICAL: {counts.get('critical', 0)}")
        print_msg(f"  HIGH:     {counts.get('high', 0)}")
        print_msg(f"  MEDIUM:   {counts.get('medium', 0)}")
        print_msg(f"  LOW:      {counts.get('low', 0)}")
        print_msg(f"  INFO:     {counts.get('info', 0)}")
        print_msg("")

        for f_data in findings[:30]:
            sev = f_data.get("severity", "?").upper()
            title = f_data.get("title", "?")[:70]
            cve = f" [{f_data['cve_id']}]" if f_data.get("cve_id") else ""
            print_msg(f"  [{sev:<8}] {title}{cve}")

        if len(findings) > 30:
            print_msg(f"\n  ... and {len(findings) - 30} more.")
            print_msg("  Use: report generate for the full report.")

    def _report_timeline(self):
        """Display the engagement event timeline."""
        timeline = self._collect_timeline()

        if not timeline:
            print_msg("No timeline events recorded.")
            print_msg("Events are logged automatically during 'engage' and 'orchestrate' operations.")
            return

        print_msg(f"\nEngagement Timeline ({len(timeline)} events):\n")
        for ev in timeline[-50:]:
            ts = ev.get("timestamp", "")
            etype = ev.get("type", ev.get("event", "?"))
            msg = str(ev.get("message", ev.get("description", "")))[:100]
            print_msg(f"  {ts:<22} [{etype:<16}] {msg}")
        print_msg("")
