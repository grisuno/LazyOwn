"""Nuclei JSON output parser — feeds scan results into DB, WorldModel, and recommender.

Parses nuclei ``-json`` / ``-jsonl`` output and enriches the LazyOwn
campaign database (``modules/db.py``) and WorldModel
(``modules/world_model.py``) with discovered vulnerabilities.

Design (SOLID):
- Single Responsibility: NucleiParser only parses nuclei output.
- Open/Closed: new finding types via Finding subclass.
- Liskov: any DB interface can replace LazyOwnDB.
- Interface Segregation: parse(), import_findings(), enrich_world_model().
- Dependency Inversion: depends on abstract DB interface, not concrete SQLite.

Usage:
    from modules.integrations.nuclei_parser import NucleiParser

    parser = NucleiParser()
    findings = parser.parse_file("sessions/nuclei_10.10.11.5.json")
    imported = parser.import_to_db(findings, rhost="10.10.11.5")
    parser.enrich_world_model(findings, rhost="10.10.11.5")
"""

from __future__ import annotations

import json
import logging
import re
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any

log = logging.getLogger("nuclei_parser")

SEVERITY_MAP: dict[str, int] = {
    "critical": 10,
    "high": 7,
    "medium": 5,
    "low": 3,
    "info": 1,
    "unknown": 0,
}

MITRE_TACTICS: dict[str, str] = {
    "sqli": "TA0006 — Credential Access",
    "xss": "TA0001 — Initial Access",
    "ssrf": "TA0001 — Initial Access",
    "rce": "TA0002 — Execution",
    "lfi": "TA0006 — Credential Access",
    "idor": "TA0005 — Defense Evasion",
    "auth-bypass": "TA0005 — Defense Evasion",
    "exposure": "TA0043 — Reconnaissance",
    "misconfig": "TA0043 — Reconnaissance",
    "default-login": "TA0006 — Credential Access",
    "takeover": "TA0040 — Impact",
    "csrf": "TA0001 — Initial Access",
    "open-redirect": "TA0043 — Reconnaissance",
    "traversal": "TA0006 — Credential Access",
}

EXPLOIT_PROBABILITY: dict[str, float] = {
    "critical": 0.90,
    "high": 0.70,
    "medium": 0.40,
    "low": 0.15,
    "info": 0.05,
    "unknown": 0.10,
}


@dataclass
class NucleiFinding:
    template_id: str
    name: str
    severity: str
    matched_at: str
    host: str
    matched: str = ""
    description: str = ""
    cve_id: str = ""
    cvss_score: float = 0.0
    curl_command: str = ""
    tags: list[str] = field(default_factory=list)
    references: list[str] = field(default_factory=list)
    raw: dict[str, Any] = field(default_factory=dict)

    @property
    def mitre_tactic(self) -> str:
        for tag_name in self.tags:
            for tactic_key, tactic_label in MITRE_TACTICS.items():
                if tactic_key in tag_name.lower():
                    return tactic_label
        return "TA0043 — Reconnaissance"

    @property
    def exploit_probability(self) -> float:
        return EXPLOIT_PROBABILITY.get(self.severity.lower(), 0.05)


class NucleiParser:
    """Parses nuclei JSON/JSONL output and imports into LazyOwn.

    Supports both single-line JSON objects per finding (``-jsonl``)
    and arrays of JSON objects (``-json``).

    Attributes:
        sessions_dir: Base sessions directory for output files.
    """

    def __init__(self, sessions_dir: str | Path | None = None) -> None:
        if sessions_dir:
            self._sessions = Path(sessions_dir)
        else:
            self._sessions = Path(__file__).parent.parent.parent / "sessions"

    def parse_text(self, text: str) -> list[NucleiFinding]:
        """Parse raw nuclei text output (table format).

        Args:
            text: Raw text from nuclei stdout.

        Returns:
            List of parsed NucleiFinding objects.
        """
        findings: list[NucleiFinding] = []
        for line in text.splitlines():
            line = line.strip()
            if not line or line.startswith("[INF]") or line.startswith("[WRN]"):
                continue
            finding = self._parse_line(line)
            if finding:
                findings.append(finding)
        return findings

    def parse_json(self, json_text: str) -> list[NucleiFinding]:
        """Parse nuclei JSON output (``-jsonl`` or ``-json`` format).

        Supports both newline-delimited JSON (JSONL) and JSON arrays.

        Args:
            json_text: JSON or JSONL formatted nuclei output.

        Returns:
            List of parsed NucleiFinding objects.
        """
        findings: list[NucleiFinding] = []
        text = json_text.strip()
        if not text:
            return findings

        if text.startswith("["):
            try:
                array = json.loads(text)
                for obj in array:
                    finding = self._parse_json_obj(obj)
                    if finding:
                        findings.append(finding)
                return findings
            except json.JSONDecodeError:
                pass

        for line in text.splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
                finding = self._parse_json_obj(obj)
                if finding:
                    findings.append(finding)
            except json.JSONDecodeError:
                finding = self._parse_line(line)
                if finding:
                    findings.append(finding)

        return findings

    def parse_file(self, filepath: str | Path) -> list[NucleiFinding]:
        """Parse nuclei output from a file (auto-detects format).

        Args:
            filepath: Path to nuclei output file.

        Returns:
            List of parsed NucleiFinding objects.
        """
        path = Path(filepath)
        if not path.exists():
            log.warning("Nuclei output file not found: %s", filepath)
            return []

        text = path.read_text(encoding="utf-8", errors="replace")
        if text.strip().startswith("{") or text.strip().startswith("["):
            return self.parse_json(text)
        return self.parse_text(text)

    def import_to_db(
        self,
        findings: list[NucleiFinding],
        rhost: str = "",
        workspace_name: str = "default",
    ) -> int:
        """Import parsed findings into the LazyOwnDB vulnerabilities table.

        Args:
            findings: Parsed NucleiFinding list.
            rhost: Target IP for host association.
            workspace_name: DB workspace to use.

        Returns:
            Number of vulnerabilities imported.
        """
        from modules.db import LazyOwnDB
        db = LazyOwnDB()
        ws = db.workspace_get(workspace_name)
        if ws is None:
            ws_id = db.workspace_create(workspace_name)
        else:
            ws_id = ws["id"]

        host_id: int | None = None
        if rhost:
            hosts = db.host_search(address=rhost, workspace_id=ws_id)
            if hosts:
                host_id = hosts[0]["id"]

        service_id = None
        if host_id:
            try:
                svc = db.service_search(host_id=host_id)
                if svc:
                    service_id = svc[0]["id"]
            except Exception:
                pass

        imported = 0
        seen: set[str] = set()
        for finding in findings:
            key = f"{finding.template_id}:{finding.matched_at}"
            if key in seen:
                continue
            seen.add(key)

            refs = ", ".join(finding.references[:5]) if finding.references else finding.cve_id
            description = finding.description or finding.name

            db.vuln_add(
                host_id=host_id,
                service_id=service_id,
                name=finding.name,
                severity=finding.severity,
                description=description,
                refs=refs,
                exploit_available=int(finding.exploit_probability > 0.5),
                matched_by=f"nuclei:{finding.template_id}",
            )
            imported += 1

        log.info("Imported %d nuclei findings into DB workspace '%s'", imported, workspace_name)
        return imported

    def enrich_world_model(
        self,
        findings: list[NucleiFinding],
        rhost: str = "",
    ) -> int:
        """Feed parsed findings into the WorldModel for autonomous decision-making.

        Args:
            findings: Parsed NucleiFinding list.
            rhost: Target IP.

        Returns:
            Number of findings added to the world model.
        """
        try:
            from modules.world_model import VulnerabilityEntry, WorldModel
            wm = WorldModel()
            added = 0
            for finding in findings:
                v = VulnerabilityEntry(
                    name=finding.name,
                    severity=finding.severity,
                    cve=finding.cve_id,
                    host=rhost or finding.host,
                    description=finding.description,
                    exploit_available=finding.exploit_probability > 0.5,
                    cvss_score=finding.cvss_score,
                    source=f"nuclei:{finding.template_id}",
                )
                wm.add_vulnerability(v)
                added += 1
            log.info("Enriched world model with %d nuclei findings", added)
            return added
        except ImportError:
            log.debug("WorldModel not available for nuclei enrichment")
            return 0

    def generate_recommendations(
        self,
        findings: list[NucleiFinding],
        rhost: str = "",
    ) -> list[dict[str, Any]]:
        """Generate actionable LazyOwn command recommendations from findings.

        Args:
            findings: Parsed NucleiFinding list.
            rhost: Target IP for command placeholders.

        Returns:
            List of recommendation dicts with command, confidence, and reason.
        """
        recommendations: list[dict[str, Any]] = []
        seen_templates: set[str] = set()

        for finding in sorted(findings, key=lambda f: SEVERITY_MAP.get(f.severity, 0), reverse=True):
            if finding.template_id in seen_templates:
                continue
            seen_templates.add(finding.template_id)

            rec = self._recommend_for_finding(finding, rhost)
            if rec:
                recommendations.append(rec)

        return recommendations

    def scan_and_import(
        self,
        target: str,
        templates: list | None = None,
        services: list[str] | None = None,
        cves: list[str] | None = None,
        workspace_name: str = "default",
    ) -> dict[str, Any]:
        """Run nuclei scan against target, parse output, and import to DB/WorldModel.

        This is the high-level entry point: run + parse + import + recommend
        in a single call.

        Args:
            target: Host to scan.
            templates: Specific nuclei templates to run (auto-selects if None).
            services: Service names to match templates against.
            cves: CVE IDs to match templates against.
            workspace_name: DB workspace.

        Returns:
            Dict with keys: findings (list), imported (int), recommendations (list).
        """
        from modules.integrations.nuclei_bridge import (
            LocalTemplateIndex,
            NucleiRunner,
            get_bridge,
        )

        idx = LocalTemplateIndex()
        if templates is None:
            svc_list = services or []
            cve_list = cves or []
            templates = idx.select(svc_list, cve_list)

        if not templates:
            return {"findings": [], "imported": 0, "recommendations": []}

        runner = NucleiRunner()
        cmd = runner._build_command(target, templates, self._sessions)
        cmd.extend(["-jsonl"])

        import subprocess
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
            output = result.stdout or ""
        except subprocess.TimeoutExpired:
            output = ""
        except (FileNotFoundError, OSError) as exc:
            log.warning("nuclei execution failed: %s", exc)
            output = ""

        findings = self.parse_json(output) if output else []
        imported = self.import_to_db(findings, rhost=target, workspace_name=workspace_name)
        self.enrich_world_model(findings, rhost=target)
        recs = self.generate_recommendations(findings, rhost=target)

        outcome: dict[str, Any] = {
            "findings": [self._finding_to_dict(f) for f in findings],
            "imported": imported,
            "recommendations": recs,
            "summary": self._summarize(findings),
        }
        return outcome

    def _parse_line(self, line: str) -> NucleiFinding | None:
        pattern = re.compile(
            r"\[(?P<severity>\w+)\]\s+"
            r"(?P<template>[\w\-]+)\s+"
            r"(?P<name>[^\[]+?)\s*"
            r"\[(?P<url>[^\]]+)\]"
        )
        match = pattern.search(line)
        if not match:
            return None

        return NucleiFinding(
            template_id=match.group("template"),
            name=match.group("name").strip(),
            severity=match.group("severity").lower(),
            matched_at=match.group("url").strip(),
            host="",
        )

    def _parse_json_obj(self, obj: dict[str, Any]) -> NucleiFinding | None:
        template_id = obj.get("template-id", obj.get("templateID", ""))
        if not template_id:
            return None

        info = obj.get("info", {})
        severity = (info.get("severity") or obj.get("severity", "info")).lower()

        matched = obj.get("matched-at", obj.get("matched", ""))
        host = obj.get("host", obj.get("ip", ""))

        name = info.get("name", template_id)
        description = info.get("description", "")
        cvss_metrics = info.get("classification", {}).get("cvss-metrics", "")
        cvss_match = re.search(r"[\d.]+", cvss_metrics) if cvss_metrics else None
        cvss_score = float(cvss_match.group(0)) if cvss_match else 0.0

        tags = info.get("tags", [])
        if isinstance(tags, str):
            tags = [t.strip() for t in tags.split(",")]

        cve_id = ""
        raw_classification = info.get("classification", {})
        if isinstance(raw_classification, dict):
            raw_cve = raw_classification.get("cve-id") or raw_classification.get("cveID")
        else:
            raw_cve = None
        if raw_cve:
            cve_id = raw_cve[0] if isinstance(raw_cve, list) else str(raw_cve)
        if not cve_id and "cve" in template_id.lower():
            cve_match = re.search(r"CVE-\d{4}-\d+", template_id, re.IGNORECASE)
            if cve_match:
                cve_id = cve_match.group(0).upper()

        refs = info.get("reference", [])
        if isinstance(refs, str):
            refs = [refs]

        curl = obj.get("curl-command", obj.get("curl_command", ""))

        return NucleiFinding(
            template_id=template_id,
            name=name,
            severity=severity,
            matched_at=matched,
            host=host,
            matched=matched,
            description=description,
            cve_id=cve_id,
            cvss_score=cvss_score,
            curl_command=curl,
            tags=tags,
            references=refs,
            raw=obj,
        )

    def _recommend_for_finding(
        self,
        finding: NucleiFinding,
        rhost: str,
    ) -> dict[str, Any] | None:
        sev_score = SEVERITY_MAP.get(finding.severity, 0)
        if sev_score < 3:
            return None

        target = rhost or finding.host
        commands: list[str] = []

        if finding.cve_id:
            commands.append(f"ss {finding.cve_id}")
            commands.append(f"searchsploit {finding.cve_id}")
        if sev_score >= 5:
            commands.append(f"lazynuclei {target}")

        for tag in finding.tags:
            if "sqli" in tag.lower():
                commands.append(f"sqlmap -u {finding.matched_at}")
            elif "xss" in tag.lower() or "rce" in tag.lower():
                commands.append(f"exploit {finding.cve_id or finding.template_id}")

        if not commands:
            return None

        return {
            "command": commands[0],
            "all_commands": commands,
            "confidence": EXPLOIT_PROBABILITY.get(finding.severity, 0.3),
            "reason": f"{finding.severity.upper()} {finding.name}: {finding.matched_at}",
            "mitre_tactic": finding.mitre_tactic,
        }

    @staticmethod
    def _finding_to_dict(finding: NucleiFinding) -> dict[str, Any]:
        return {
            "template_id": finding.template_id,
            "name": finding.name,
            "severity": finding.severity,
            "matched_at": finding.matched_at,
            "cve_id": finding.cve_id,
            "cvss_score": finding.cvss_score,
            "mitre_tactic": finding.mitre_tactic,
            "exploit_probability": finding.exploit_probability,
        }

    @staticmethod
    def _summarize(findings: list[NucleiFinding]) -> dict[str, Any]:
        by_severity: dict[str, int] = {}
        for f in findings:
            by_severity[f.severity] = by_severity.get(f.severity, 0) + 1
        cve_findings = [f for f in findings if f.cve_id]
        exploitable = [f for f in findings if f.exploit_probability >= 0.5]
        return {
            "total": len(findings),
            "by_severity": by_severity,
            "with_cve": len(cve_findings),
            "likely_exploitable": len(exploitable),
            "top_critical": [f.template_id for f in findings if f.severity == "critical"][:5],
        }


__all__ = [
    "NucleiParser",
    "NucleiFinding",
    "SEVERITY_MAP",
    "MITRE_TACTICS",
    "EXPLOIT_PROBABILITY",
]
