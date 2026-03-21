#!/usr/bin/env python3
"""
modules/report_generator.py
============================
Auto-generates a structured penetration test report from LazyOwn session data.

Sources read (all optional — missing files are skipped gracefully):
  sessions/policy_facts.json    FactStore structured data (hosts, services, vulns)
  sessions/events.jsonl         Event timeline
  sessions/objectives.jsonl     Attack objectives with status
  sessions/credentials.txt      Captured credentials
  sessions/plan.txt             VulnBot/LLM attack plan
  sessions/sessionLazyOwn.json  Session state snapshot

Output:
  sessions/report_<YYYYMMDD_HHMMSS>.md

Usage:
    from modules.report_generator import ReportGenerator

    rg   = ReportGenerator()
    path = rg.generate()
    print(f"Report: {path}")

    # CLI:
    python3 modules/report_generator.py [--sessions PATH] [--output PATH] [--quiet]
"""
from __future__ import annotations

import json
import logging
import os
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

log = logging.getLogger("report_generator")

_BASE_DIR     = Path(__file__).parent.parent
_SESSIONS_DIR = _BASE_DIR / "sessions"


class ReportGenerator:
    """
    Reads session artefacts and produces a Markdown pentest report.

    Parameters
    ----------
    sessions_dir : path to the sessions/ directory (default: <project>/sessions/)
    """

    def __init__(self, sessions_dir: str | Path = _SESSIONS_DIR) -> None:
        self.sdir = Path(sessions_dir)

    # ── Public API ────────────────────────────────────────────────────────────

    def generate(self, output_path: Optional[str | Path] = None) -> Path:
        """
        Generate the report and write it to *output_path*.

        Returns the path of the written file.
        """
        if output_path is None:
            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = self.sdir / f"report_{ts}.md"
        out = Path(output_path)
        out.parent.mkdir(parents=True, exist_ok=True)

        sections = [
            self._header(),
            self._section_scope(),
            self._section_findings(),
            self._section_credentials(),
            self._section_timeline(),
            self._section_objectives(),
            self._section_plan(),
            self._section_recommendations(),
            self._footer(),
        ]
        report = "\n\n".join(s for s in sections if s and s.strip())
        out.write_text(report, encoding="utf-8")
        log.info("Report written to %s", out)
        return out

    # ── Sections ──────────────────────────────────────────────────────────────

    def _header(self) -> str:
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        facts = self._load_facts()
        hosts = list(facts.get("hosts", {}).keys()) if facts else []
        scope = ", ".join(hosts) if hosts else "unknown"
        return (
            "# Penetration Test Report\n\n"
            f"**Generated:** {now}  \n"
            f"**Framework:** LazyOwn RedTeam Suite  \n"
            f"**Scope:** {scope}  \n"
            f"**Classification:** CONFIDENTIAL\n\n"
            "---"
        )

    def _section_scope(self) -> str:
        facts = self._load_facts()
        if not facts:
            return "## 1. Scope & Discovery\n\n_No scan data available._"

        hosts = facts.get("hosts", {})
        lines = [
            "## 1. Scope & Discovery",
            "",
            f"**Hosts discovered:** {len(hosts)}",
            "",
            "| Host | OS | Open Services |",
            "|------|----|---------------|",
        ]
        for ip, info in hosts.items():
            services = info.get("services", {})
            if isinstance(services, dict):
                svc_list = [f"{port}/{info_s.get('name', '?')}" for port, info_s in services.items()]
            else:
                svc_list = [f"{s.get('port')}/{s.get('name','?')}" for s in (services or [])]
            os_hint = info.get("os_hint", info.get("os", "unknown"))
            lines.append(f"| {ip} | {os_hint} | {', '.join(svc_list) or 'none'} |")
        return "\n".join(lines)

    def _section_findings(self) -> str:
        facts = self._load_facts()
        if not facts:
            return ""

        vulns: List[dict] = []
        for ip, info in facts.get("hosts", {}).items():
            for v in info.get("vulnerabilities", []):
                vulns.append({"host": ip, **v})

        if not vulns:
            return "## 2. Findings\n\n_No vulnerabilities recorded._"

        lines = ["## 2. Findings", ""]
        for i, v in enumerate(vulns, 1):
            severity = v.get("severity", "INFO").upper()
            title    = v.get("title", v.get("name", f"Finding {i}"))
            desc     = v.get("description", v.get("detail", "No description."))
            evidence = v.get("evidence", v.get("output", ""))
            lines += [
                f"### 2.{i} {title}",
                f"**Severity:** {severity}  ",
                f"**Host:** {v.get('host', 'N/A')}  ",
                f"**Description:** {desc}",
            ]
            if evidence:
                lines.append(f"\n```\n{str(evidence)[:400]}\n```")
            lines.append("")
        return "\n".join(lines)

    def _section_credentials(self) -> str:
        cred_file = self.sdir / "credentials.txt"
        if not cred_file.exists():
            return ""
        creds = cred_file.read_text(encoding="utf-8", errors="replace").strip()
        if not creds:
            return ""
        count = len([l for l in creds.splitlines() if l.strip()])
        return (
            "## 3. Credentials Captured\n\n"
            f"**Total:** {count}\n\n"
            "```\n" + creds + "\n```"
        )

    def _section_timeline(self) -> str:
        events = self._load_jsonl(self.sdir / "events.jsonl")
        if not events:
            return ""

        lines = [
            "## 4. Timeline",
            "",
            "| Timestamp | Event Type | Detail |",
            "|-----------|------------|--------|",
        ]
        for ev in events[-60:]:
            ts     = str(ev.get("timestamp", ev.get("ts", "")))[:19]
            etype  = ev.get("type", ev.get("event_type", ""))
            detail = str(ev.get("data", ev.get("detail", ev.get("message", ""))))[:100]
            detail = detail.replace("|", "/")
            lines.append(f"| {ts} | {etype} | {detail} |")
        return "\n".join(lines)

    def _section_objectives(self) -> str:
        objs = self._load_jsonl(self.sdir / "objectives.jsonl")
        if not objs:
            return ""

        done    = [o for o in objs if o.get("status") in ("done", "completed")]
        pending = [o for o in objs if o.get("status") not in ("done", "completed")]

        lines = [
            "## 5. Objectives",
            "",
            f"**Completed:** {len(done)} / {len(objs)}",
            "",
        ]
        if done:
            lines.append("**Completed:**")
            for o in done:
                lines.append(f"- [x] {o.get('title', o.get('description', ''))}")
        if pending:
            lines.append("\n**Pending:**")
            for o in pending:
                lines.append(f"- [ ] {o.get('title', o.get('description', ''))}")
        return "\n".join(lines)

    def _section_plan(self) -> str:
        plan_file = self.sdir / "plan.txt"
        if not plan_file.exists():
            return ""
        plan = plan_file.read_text(encoding="utf-8", errors="replace").strip()
        if not plan:
            return ""
        return "## 6. Attack Plan\n\n```\n" + plan[:4000] + "\n```"

    def _section_recommendations(self) -> str:
        facts = self._load_facts()
        lines = ["## 7. Recommendations", ""]

        if not facts:
            lines.append("_Complete the engagement to generate recommendations._")
            return "\n".join(lines)

        SERVICE_RECS: Dict[str, str] = {
            "http":  "Perform web application assessment: directory brute-force, auth bypass, injection, misconfigurations.",
            "https": "Perform web application assessment over TLS: cert validity, HSTS, injection, auth bypass.",
            "smb":   "Test for null session, EternalBlue (MS17-010), SMB relay, credential brute-force.",
            "ssh":   "Check for outdated version vulnerabilities, user enumeration, brute-force, weak keys.",
            "ftp":   "Test anonymous login, brute-force, cleartext credential sniffing.",
            "ldap":  "Enumerate domain objects, AS-REP roast, Kerberoast, ACL abuse.",
            "ldaps": "Enumerate domain objects over LDAPS, AS-REP roast, Kerberoast, ACL abuse.",
            "mssql": "Test sa account, xp_cmdshell, credential stuffing, UNC path injection.",
            "mysql": "Test for blank root password, file read/write via LOAD DATA INFILE.",
            "rdp":   "Test BlueKeep (CVE-2019-0708), NLA bypass, credential brute-force.",
            "winrm": "Test credential brute-force; if credentials known, attempt lateral movement.",
        }

        added = False
        for ip, info in facts.get("hosts", {}).items():
            services = info.get("services", {})
            if isinstance(services, dict):
                svc_items = [(port, s.get("name", "")) for port, s in services.items()]
            else:
                svc_items = [(s.get("port", "?"), s.get("name", "")) for s in (services or [])]

            for port, name in svc_items:
                name_l = name.lower().split("/")[0].strip()
                rec = SERVICE_RECS.get(name_l)
                if rec:
                    lines.append(f"- **{ip}:{port}** (`{name_l}`): {rec}")
                    added = True

        if not added:
            lines.append("_No service-specific recommendations generated from current fact data._")
        return "\n".join(lines)

    def _footer(self) -> str:
        return (
            "---\n\n"
            "_This report was auto-generated by LazyOwn. "
            "Review and validate all findings before submission._"
        )

    # ── Data loaders ──────────────────────────────────────────────────────────

    def _load_facts(self) -> Dict[str, Any]:
        for fname in ("policy_facts.json", "facts.json"):
            p = self.sdir / fname
            if p.exists():
                try:
                    raw = json.loads(p.read_text(encoding="utf-8"))
                    # Normalise: some fact stores use top-level hosts dict, others wrap it
                    if "hosts" in raw and isinstance(raw["hosts"], dict):
                        return raw
                    # Treat the whole dict as hosts only if all values are dicts (host records)
                    host_like = {k: v for k, v in raw.items() if isinstance(v, dict)}
                    if host_like:
                        return {"hosts": host_like}
                    return {}
                except Exception as exc:
                    log.warning("Could not load %s: %s", p, exc)
        return {}

    def _load_jsonl(self, path: Path) -> List[Dict]:
        if not path.exists():
            return []
        results = []
        for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                results.append(json.loads(line))
            except Exception:
                pass
        return results


# ── CLI ───────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import argparse
    import sys

    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")

    p = argparse.ArgumentParser(description="LazyOwn Report Generator")
    p.add_argument("--sessions", default=str(_SESSIONS_DIR),
                   help="Path to sessions directory")
    p.add_argument("--output",   default=None,
                   help="Output file path (default: sessions/report_<ts>.md)")
    p.add_argument("--quiet",    action="store_true")
    args = p.parse_args()

    if args.quiet:
        logging.disable(logging.WARNING)

    rg  = ReportGenerator(sessions_dir=args.sessions)
    out = rg.generate(output_path=args.output)
    print(out)
