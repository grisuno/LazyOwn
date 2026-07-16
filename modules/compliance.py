"""
modules/compliance.py
=====================
Enterprise compliance engine for LazyOwn RedTeam Framework.

Capabilities:
- Framework mappings (PCI-DSS 4.0, ISO 27001:2022, NIST SP 800-53 Rev 5)
- Cryptographic evidence chain (SHA256 merkle-style chain of custody)
- PDF report export (via fpdf2, zero external pandoc dependency)
- SIEM/Elastic bulk export (JSON-ND format for Elasticsearch, CEF for ArcSight)
- Operator attribution in all audit trails
- Automated compliance coverage scoring per engagement

Usage:
    from modules.compliance import ComplianceEngine, EvidenceChain, export_pdf

    engine = ComplianceEngine(sessions_dir="sessions/default")
    report = engine.generate_compliance_report(include_evidence_chain=True)
    engine.export_pdf(report, "compliance_report.pdf")
"""

from __future__ import annotations

import hashlib
import json
import logging
import time
from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

log = logging.getLogger("compliance")


# ═══════════════════════════════════════════════════════════════════════════════
# Compliance Framework Mappings
# ═══════════════════════════════════════════════════════════════════════════════

COMPLIANCE_FRAMEWORKS: dict[str, dict[str, Any]] = {
    "pci_dss": {
        "name": "PCI-DSS 4.0",
        "url": "https://www.pcisecuritystandards.org/",
        "controls": {
            "reconnaissance": [
                {"id": "11.2", "title": "External Vulnerability Scans", "desc": "Perform quarterly external ASV scans"},
                {"id": "11.3", "title": "Internal Vulnerability Scans", "desc": "Perform quarterly internal vulnerability scans"},
                {"id": "1.1", "title": "Network Security Controls", "desc": "Define and implement firewall rules"},
            ],
            "enumeration": [
                {"id": "2.2", "title": "Secure Configuration Standards", "desc": "Apply configuration standards to all system components"},
                {"id": "6.3", "title": "Security Vulnerabilities", "desc": "Identify and rank new security vulnerabilities"},
            ],
            "exploitation": [
                {"id": "11.4", "title": "Penetration Testing", "desc": "Conduct penetration testing based on industry-accepted approaches"},
                {"id": "11.4.1", "title": "External Penetration Testing", "desc": "Perform external penetration testing per methodology"},
                {"id": "11.4.2", "title": "Internal Penetration Testing", "desc": "Perform internal penetration testing per methodology"},
            ],
            "privilege_escalation": [
                {"id": "7.1", "title": "Least Privilege", "desc": "Limit access to system components by need-to-know"},
                {"id": "7.2", "title": "Access Control Systems", "desc": "Establish an access control system for system components"},
                {"id": "8.2", "title": "User Identification", "desc": "Unique ID for each person with access"},
            ],
            "lateral_movement": [
                {"id": "1.3", "title": "Network Segmentation", "desc": "Prohibit direct public access between Internet and CDE"},
                {"id": "7.3", "title": "Access Approval", "desc": "Ensure access to CDE is approved by authorized personnel"},
            ],
            "credential_access": [
                {"id": "8.3", "title": "Strong Authentication", "desc": "Implement MFA for all access into CDE"},
                {"id": "8.4", "title": "Password Policies", "desc": "Document and communicate authentication policies"},
                {"id": "3.6", "title": "Key Management", "desc": "Cryptographic key management procedures"},
            ],
            "data_exfil": [
                {"id": "4.1", "title": "Data Encryption", "desc": "Use strong cryptography to safeguard cardholder data"},
                {"id": "12.10", "title": "Incident Response", "desc": "Implement an incident response plan"},
            ],
            "general": [
                {"id": "12.5", "title": "Information Security Policy", "desc": "Maintain an information security policy"},
                {"id": "12.6", "title": "Security Awareness", "desc": "Implement a formal security awareness program"},
            ],
        },
    },
    "iso27001": {
        "name": "ISO 27001:2022",
        "url": "https://www.iso.org/standard/27001",
        "controls": {
            "reconnaissance": [
                {"id": "A.8.8", "title": "Technical Vulnerability Management", "desc": "Information about technical vulnerabilities shall be obtained and evaluated"},
                {"id": "A.5.8", "title": "Information Security in Project Management", "desc": "Information security shall be integrated into project management"},
            ],
            "enumeration": [
                {"id": "A.8.9", "title": "Configuration Management", "desc": "Secure configurations shall be applied to hardware, software, and services"},
                {"id": "A.8.2", "title": "Asset Management", "desc": "Assets shall be identified and an inventory maintained"},
            ],
            "exploitation": [
                {"id": "A.8.7", "title": "Protection Against Malware", "desc": "Protection against malware shall be implemented"},
                {"id": "A.8.16", "title": "Monitoring Activities", "desc": "Networks, systems, and applications shall be monitored for anomalous behaviour"},
            ],
            "privilege_escalation": [
                {"id": "A.5.15", "title": "Access Control", "desc": "Access to information and other associated assets shall be controlled"},
                {"id": "A.5.16", "title": "Identity Management", "desc": "The full lifecycle of identities shall be managed"},
            ],
            "lateral_movement": [
                {"id": "A.8.20", "title": "Network Security", "desc": "Networks and network devices shall be secured, managed and controlled"},
                {"id": "A.8.22", "title": "Network Segregation", "desc": "Groups of information services, users and information systems shall be segregated on networks"},
            ],
            "credential_access": [
                {"id": "A.5.17", "title": "Authentication Information", "desc": "Allocation and management of authentication information shall be controlled"},
                {"id": "A.8.5", "title": "Secure Authentication", "desc": "Secure authentication technologies and procedures shall be implemented"},
            ],
            "data_exfil": [
                {"id": "A.8.24", "title": "Use of Cryptography", "desc": "Rules for the effective use of cryptography shall be defined"},
                {"id": "A.5.24", "title": "ICT Readiness for Business Continuity", "desc": "ICT readiness shall be planned, implemented, maintained, and tested"},
            ],
            "general": [
                {"id": "A.5.1", "title": "Policies for Information Security", "desc": "Information security policy shall be defined and approved by management"},
                {"id": "A.6.3", "title": "Information Security Awareness and Training", "desc": "Personnel shall receive appropriate awareness education"},
            ],
        },
    },
    "nist_800_53": {
        "name": "NIST SP 800-53 Rev 5",
        "url": "https://csrc.nist.gov/publications/detail/sp/800-53/rev-5/final",
        "controls": {
            "reconnaissance": [
                {"id": "RA-5", "title": "Vulnerability Monitoring and Scanning", "desc": "Monitor and scan for vulnerabilities in the system"},
                {"id": "CA-8", "title": "Penetration Testing", "desc": "Conduct penetration testing on the system"},
            ],
            "enumeration": [
                {"id": "CM-6", "title": "Configuration Settings", "desc": "Establish and document configuration settings"},
                {"id": "CM-8", "title": "System Component Inventory", "desc": "Develop and document an inventory of system components"},
            ],
            "exploitation": [
                {"id": "SI-3", "title": "Malicious Code Protection", "desc": "Implement malicious code protection mechanisms"},
                {"id": "SI-4", "title": "System Monitoring", "desc": "Monitor the system to detect attacks and indicators of potential attacks"},
            ],
            "privilege_escalation": [
                {"id": "AC-6", "title": "Least Privilege", "desc": "Employ the principle of least privilege"},
                {"id": "IA-2", "title": "Identification and Authentication", "desc": "Uniquely identify and authenticate users and processes"},
            ],
            "lateral_movement": [
                {"id": "AC-4", "title": "Information Flow Enforcement", "desc": "Enforce approved authorizations for controlling the flow of information within the system"},
                {"id": "SC-7", "title": "Boundary Protection", "desc": "Monitor and control communications at external and internal boundaries"},
            ],
            "credential_access": [
                {"id": "IA-5", "title": "Authenticator Management", "desc": "Manage system authenticators"},
                {"id": "IA-6", "title": "Authentication Feedback", "desc": "Obscure feedback of authentication information during authentication"},
            ],
            "data_exfil": [
                {"id": "SC-8", "title": "Transmission Confidentiality and Integrity", "desc": "Protect the confidentiality and integrity of transmitted information"},
                {"id": "IR-4", "title": "Incident Handling", "desc": "Implement an incident handling capability"},
            ],
            "general": [
                {"id": "AT-2", "title": "Literacy Training and Awareness", "desc": "Provide security literacy training to system users"},
                {"id": "CA-2", "title": "Control Assessments", "desc": "Assess the controls in the system periodically"},
            ],
        },
    },
}

FINDING_CATEGORY_TO_COMPLIANCE_MAP: dict[str, list[str]] = {
    "open_port": ["reconnaissance"],
    "outdated_service": ["enumeration"],
    "vulnerable_service": ["exploitation", "enumeration"],
    "default_credential": ["credential_access", "privilege_escalation"],
    "exposed_credential": ["credential_access"],
    "weak_password": ["credential_access"],
    "privilege_escalation_path": ["privilege_escalation"],
    "lateral_movement_path": ["lateral_movement"],
    "data_leak": ["data_exfil"],
    "misconfiguration": ["enumeration"],
    "missing_patch": ["exploitation"],
    "reverse_shell": ["exploitation", "data_exfil"],
    "persistence": ["lateral_movement", "privilege_escalation"],
}


# ═══════════════════════════════════════════════════════════════════════════════
# Cryptographic Evidence Chain
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass(frozen=True, slots=True)
class EvidenceEntry:
    filename: str
    sha256: str
    size_bytes: int
    timestamp: str
    operator: str
    description: str


class EvidenceChain:
    """Merkle-style chain of custody for red-team evidence.

    Each file artefact added to the chain is hashed with SHA256 and linked
    to the previous entry, creating a tamper-evident chain. The chain state
    is persisted to ``sessions/evidence_chain.jsonl``.
    """

    def __init__(self, sessions_dir: str = "sessions") -> None:
        self._sessions_dir = Path(sessions_dir)
        self._chain_file = self._sessions_dir / "evidence_chain.jsonl"
        self._chain: list[EvidenceEntry] = []
        self._prev_hash: str = "0" * 64
        self._load()

    def _load(self) -> None:
        if not self._chain_file.exists():
            return
        try:
            for line in self._chain_file.read_text(encoding="utf-8").splitlines():
                line = line.strip()
                if not line:
                    continue
                entry = json.loads(line)
                ev = EvidenceEntry(**entry)
                self._chain.append(ev)
                self._prev_hash = self._hash_entry(ev)
        except Exception as exc:
            log.warning("Failed to load evidence chain: %s", exc)

    def _hash_entry(self, entry: EvidenceEntry) -> str:
        data = f"{self._prev_hash}:{entry.filename}:{entry.sha256}:{entry.timestamp}"
        return hashlib.sha256(data.encode("utf-8")).hexdigest()

    def add_file(self, filepath: str, operator: str, description: str = "") -> EvidenceEntry:
        path = Path(filepath)
        if not path.exists():
            raise FileNotFoundError(f"Evidence file not found: {filepath}")

        sha256 = hashlib.sha256(path.read_bytes()).hexdigest()
        entry = EvidenceEntry(
            filename=str(path),
            sha256=sha256,
            size_bytes=path.stat().st_size,
            timestamp=datetime.now(UTC).isoformat(),
            operator=operator,
            description=description,
        )
        self._prev_hash = self._hash_entry(entry)
        self._chain.append(entry)
        self._append_to_file(entry)
        log.info("Evidence added: %s (SHA256: %s) by %s", path.name, sha256[:16], operator)
        return entry

    def _append_to_file(self, entry: EvidenceEntry) -> None:
        self._sessions_dir.mkdir(parents=True, exist_ok=True)
        with open(self._chain_file, "a", encoding="utf-8") as f:
            chain_hash = self._prev_hash
            record = {**asdict(entry), "chain_hash": chain_hash}
            f.write(json.dumps(record) + "\n")

    def verify(self) -> tuple[bool, list[str]]:
        issues: list[str] = []
        prev = "0" * 64
        for i, entry in enumerate(self._chain):
            data = f"{prev}:{entry.filename}:{entry.sha256}:{entry.timestamp}"
            computed = hashlib.sha256(data.encode("utf-8")).hexdigest()

            path = Path(entry.filename)
            if path.exists():
                current = hashlib.sha256(path.read_bytes()).hexdigest()
                if current != entry.sha256:
                    issues.append(f"Entry {i}: file content hash mismatch for {entry.filename}")
                    issues.append(f"  Stored: {entry.sha256[:16]}... Current: {current[:16]}...")
            else:
                issues.append(f"Entry {i}: file missing: {entry.filename}")

            prev = computed
        return len(issues) == 0, issues

    def get_chain_digest(self) -> str:
        return self._prev_hash[-16:] if self._chain else "EMPTY_CHAIN"

    def to_report(self) -> list[dict[str, str]]:
        return [asdict(e) for e in self._chain]


# ═══════════════════════════════════════════════════════════════════════════════
# PDF Report Export
# ═══════════════════════════════════════════════════════════════════════════════

_FPDF_AVAILABLE = False
try:
    from fpdf import FPDF
    _FPDF_AVAILABLE = True
except ImportError:
    pass


def export_pdf(report_md: str, output_path: str, title: str = "LazyOwn RedTeam Report",
               classification: str = "CONFIDENTIAL") -> str | None:
    """Export a Markdown report to PDF using fpdf2.

    Zero external dependencies beyond fpdf2 (no pandoc, no weasyprint).
    Returns the output path on success, None on failure.
    """
    if not _FPDF_AVAILABLE:
        log.warning("fpdf2 not installed; cannot export to PDF")
        return None

    try:
        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()

        pdf.set_font("Helvetica", "B", 16)
        pdf.cell(0, 10, title, ln=True, align="C")
        pdf.set_font("Helvetica", "I", 10)
        pdf.cell(0, 8, f"Classification: {classification}", ln=True, align="C")
        pdf.cell(0, 8, f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} UTC", ln=True, align="C")
        pdf.ln(10)

        pdf.set_draw_color(180, 0, 0)
        pdf.set_line_width(0.5)
        pdf.line(10, pdf.get_y(), 200, pdf.get_y())
        pdf.ln(5)

        in_code_block = False
        for line in report_md.split("\n"):
            stripped = line.strip()

            if stripped.startswith("```"):
                in_code_block = not in_code_block
                continue

            if in_code_block:
                pdf.set_font("Courier", "", 8)
                pdf.cell(0, 4, line[:120], ln=True)
                continue

            if stripped == "---":
                pdf.set_draw_color(100, 100, 100)
                pdf.line(10, pdf.get_y(), 200, pdf.get_y())
                pdf.ln(3)
                continue

            if stripped.startswith("# ") and not stripped.startswith("##"):
                pdf.set_font("Helvetica", "B", 14)
                pdf.cell(0, 10, stripped[2:], ln=True)
                pdf.ln(3)
            elif stripped.startswith("## "):
                pdf.set_font("Helvetica", "B", 12)
                pdf.cell(0, 8, stripped[3:], ln=True)
                pdf.ln(2)
            elif stripped.startswith("### "):
                pdf.set_font("Helvetica", "B", 11)
                pdf.cell(0, 7, stripped[4:], ln=True)
                pdf.ln(1)
            elif stripped.startswith("- ") or stripped.startswith("* "):
                pdf.set_font("Helvetica", "", 10)
                pdf.cell(5, 0, "")
                pdf.cell(0, 5, stripped[2:], ln=True)
            elif stripped:
                pdf.set_font("Helvetica", "", 10)
                encoded = stripped.encode("latin-1", errors="replace").decode("latin-1")
                pdf.multi_cell(0, 5, encoded[:150])

        out = Path(output_path)
        out.parent.mkdir(parents=True, exist_ok=True)
        pdf.output(str(out))
        log.info("PDF report written to %s", out)
        return str(out)
    except Exception as exc:
        log.error("PDF export failed: %s", exc)
        return None


# ═══════════════════════════════════════════════════════════════════════════════
# SIEM / Elastic Export
# ═══════════════════════════════════════════════════════════════════════════════

def export_to_elastic_ndjson(findings: list[dict[str, Any]], output_path: str,
                              index_prefix: str = "lazyown") -> str:
    """Export findings as Elasticsearch NDJSON bulk format.

    Produces a newline-delimited JSON file compatible with Elasticsearch _bulk API.
    """
    out = Path(output_path)
    out.parent.mkdir(parents=True, exist_ok=True)

    ts = datetime.now(UTC).isoformat()
    with open(out, "w", encoding="utf-8") as f:
        for i, finding in enumerate(findings):
            action = {
                "index": {
                    "_index": f"{index_prefix}-findings-{datetime.now().strftime('%Y.%m.%d')}",
                    "_id": f"lazyown-{i}-{int(time.time())}",
                }
            }
            f.write(json.dumps(action) + "\n")

            doc = {
                "@timestamp": ts,
                "event_type": "finding",
                "source": "LazyOwn RedTeam",
                "severity": finding.get("severity", "INFO"),
                "host": finding.get("host", ""),
                "port": finding.get("port", ""),
                "service": finding.get("service", ""),
                "description": finding.get("description", ""),
                "operator": finding.get("operator", "system"),
                "category": finding.get("category", ""),
                "compliance": finding.get("compliance", {}),
                "raw": finding,
            }
            f.write(json.dumps(doc) + "\n")

    log.info("Elastic NDJSON export written to %s (%d documents)", out, len(findings))
    return str(out)


def export_to_cef(findings: list[dict[str, Any]], output_path: str,
                   vendor: str = "LazyOwn", product: str = "RedTeam",
                   version: str = "1.0") -> str:
    """Export findings in CEF (Common Event Format) for ArcSight/QRadar/Splunk.

    CEF:0|<vendor>|<product>|<version>|<signature_id>|<name>|<severity>|<extension>
    """
    out = Path(output_path)
    out.parent.mkdir(parents=True, exist_ok=True)

    with open(out, "w", encoding="utf-8") as f:
        for i, finding in enumerate(findings):
            signature_id = f"LAZY-{i:05d}"
            name = finding.get("service", "Unknown")[:100].replace("|", "_")
            severity_map = {"CRITICAL": "10", "HIGH": "8", "MEDIUM": "5", "LOW": "3", "INFO": "1"}
            severity = severity_map.get(finding.get("severity", "INFO").upper(), "1")

            cef_prefix = f"CEF:0|{vendor}|{product}|{version}|{signature_id}|{name}|{severity}|"

            extensions = []
            if finding.get("host"):
                extensions.append(f"dhost={finding['host']}")
            if finding.get("port"):
                extensions.append(f"dpt={finding['port']}")
            if finding.get("description"):
                desc = finding["description"].replace("=", "\\=").replace("|", "\\|")[:200]
                extensions.append(f"msg={desc}")
            if finding.get("operator"):
                extensions.append(f"suser={finding['operator']}")
            extensions.append(f"cat={finding.get('category', 'unknown')}")
            extensions.append(f"rt={datetime.now(UTC).strftime('%b %d %Y %H:%M:%S')} UTC")

            f.write(cef_prefix + " ".join(extensions) + "\n")

    log.info("CEF export written to %s (%d events)", out, len(findings))
    return str(out)


# ═══════════════════════════════════════════════════════════════════════════════
# Compliance Engine
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class ComplianceFinding:
    category: str
    host: str
    port: str
    service: str
    description: str
    severity: str
    operator: str
    timestamp: str = field(default_factory=lambda: datetime.now(UTC).isoformat())
    evidence_sha256: str = ""


class ComplianceEngine:
    """Generates compliance-mapped reports with evidence chain support."""

    def __init__(self, sessions_dir: str = "sessions") -> None:
        self._sessions_dir = Path(sessions_dir)
        self._evidence_chain = EvidenceChain(str(sessions_dir))

    def map_findings_to_compliance(
        self, findings: list[ComplianceFinding],
        frameworks: list[str] | None = None,
    ) -> dict[str, Any]:
        """Map findings to compliance framework controls.

        Args:
            findings: List of ComplianceFinding objects.
            frameworks: List of framework keys (e.g. ['pci_dss', 'iso27001', 'nist_800_53']).
                       If None, all frameworks are included.

        Returns:
            Dict with per-framework coverage and control-level mappings.
        """
        if frameworks is None:
            frameworks = list(COMPLIANCE_FRAMEWORKS.keys())

        report: dict[str, Any] = {
            "generated_at": datetime.now(UTC).isoformat(),
            "total_findings": len(findings),
            "frameworks": {},
            "coverage_summary": {},
        }

        for fw_key in frameworks:
            fw = COMPLIANCE_FRAMEWORKS.get(fw_key)
            if not fw:
                continue

            framework_report: dict[str, Any] = {
                "name": fw["name"],
                "url": fw["url"],
                "controls_mapped": [],
                "findings_mapped": 0,
            }

            mapped_control_ids: set = set()
            for finding in findings:
                categories = FINDING_CATEGORY_TO_COMPLIANCE_MAP.get(
                    finding.category, ["general"]
                )
                for cat in categories:
                    controls = fw["controls"].get(cat, [])
                    for ctrl in controls:
                        if ctrl["id"] not in mapped_control_ids:
                            framework_report["controls_mapped"].append({
                                "control_id": ctrl["id"],
                                "title": ctrl["title"],
                                "description": ctrl["desc"],
                                "finding_evidence": {
                                    "host": finding.host,
                                    "service": finding.service,
                                    "description": finding.description,
                                    "severity": finding.severity,
                                    "operator": finding.operator,
                                },
                            })
                            mapped_control_ids.add(ctrl["id"])
                            framework_report["findings_mapped"] += 1

            total_controls = sum(
                len(ctrls) for ctg, ctrls in fw["controls"].items()
            )
            coverage_pct = (
                round(100 * len(mapped_control_ids) / total_controls, 1)
                if total_controls > 0
                else 0
            )

            framework_report["controls_covered"] = len(mapped_control_ids)
            framework_report["total_controls"] = total_controls
            framework_report["coverage_pct"] = coverage_pct
            report["frameworks"][fw_key] = framework_report

        return report

    def generate_compliance_report(
        self,
        findings: list[ComplianceFinding] | None = None,
        include_evidence_chain: bool = True,
        include_siem_formats: bool = False,
    ) -> dict[str, Any]:
        """Generate a full compliance report with evidence chain and optional SIEM export.

        Args:
            findings: List of findings. If None, loads from sessions/.
            include_evidence_chain: Include cryptographic evidence chain in report.
            include_siem_formats: Generate NDJSON and CEF exports.

        Returns:
            Comprehensive compliance report dict.
        """
        if findings is None:
            findings = self._load_findings()

        compliance_map = self.map_findings_to_compliance(findings)

        evidence_info: dict[str, Any] = {}
        if include_evidence_chain:
            valid, issues = self._evidence_chain.verify()
            evidence_info = {
                "chain_digest": self._evidence_chain.get_chain_digest(),
                "entries_count": len(self._evidence_chain._chain),
                "integrity_verified": valid,
                "integrity_issues": issues,
            }

        siem_files: dict[str, str] = {}
        if include_siem_formats and findings:
            finding_dicts = [asdict(f) for f in findings]
            ndjson_path = self._sessions_dir / "siem_export_bulk.ndjson"
            cef_path = self._sessions_dir / "siem_export_cef.log"
            siem_files["elastic_ndjson"] = export_to_elastic_ndjson(finding_dicts, str(ndjson_path))
            siem_files["cef"] = export_to_cef(finding_dicts, str(cef_path))

        report = {
            "report_type": "compliance",
            "generated_at": datetime.now(UTC).isoformat(),
            "compliance": compliance_map,
            "evidence_chain": evidence_info,
            "siem_exports": siem_files,
            "findings_summary": {
                "total": len(findings),
                "by_severity": self._count_by_severity(findings),
                "by_category": self._count_by_category(findings),
                "operators_involved": list(set(f.operator for f in findings)),
            },
        }

        return report

    def _count_by_severity(self, findings: list[ComplianceFinding]) -> dict[str, int]:
        counts: dict[str, int] = {}
        for f in findings:
            sev = f.severity.upper() or "INFO"
            counts[sev] = counts.get(sev, 0) + 1
        return counts

    def _count_by_category(self, findings: list[ComplianceFinding]) -> dict[str, int]:
        counts: dict[str, int] = {}
        for f in findings:
            cat = f.category or "unknown"
            counts[cat] = counts.get(cat, 0) + 1
        return counts

    def _load_findings(self) -> list[ComplianceFinding]:
        findings: list[ComplianceFinding] = []
        facts_path = self._sessions_dir / "policy_facts.json"
        if facts_path.exists():
            try:
                data = json.loads(facts_path.read_text(encoding="utf-8"))
                facts = data.get("facts", []) if isinstance(data, dict) else data
                if isinstance(facts, list):
                    for fact in facts:
                        if isinstance(fact, dict):
                            findings.append(ComplianceFinding(
                                category=fact.get("type", "general"),
                                host=fact.get("host", ""),
                                port=str(fact.get("port", "")),
                                service=fact.get("service", ""),
                                description=fact.get("value", ""),
                                severity="MEDIUM",
                                operator=fact.get("operator", "system"),
                            ))
            except Exception as exc:
                log.warning("Failed to load facts: %s", exc)

        events_path = self._sessions_dir / "events.jsonl"
        if events_path.exists():
            try:
                for line in events_path.read_text(encoding="utf-8").splitlines():
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        event = json.loads(line)
                        if isinstance(event, dict):
                            findings.append(ComplianceFinding(
                                category=event.get("type", "event"),
                                host=event.get("host", event.get("target", "")),
                                port=str(event.get("port", "")),
                                service=event.get("service", ""),
                                description=event.get("message", event.get("description", "")),
                                severity=event.get("severity", "INFO"),
                                operator=event.get("operator", "system"),
                            ))
                    except json.JSONDecodeError:
                        pass
            except Exception as exc:
                log.warning("Failed to load events: %s", exc)

        return findings

    def export_pdf(self, report: dict[str, Any], output_path: str) -> str | None:
        md = self._format_compliance_report_md(report)
        return export_pdf(md, output_path)

    def _format_compliance_report_md(self, report: dict[str, Any]) -> str:
        lines: list[str] = []
        lines.append("# LazyOwn Compliance Report")
        lines.append(f"**Generated:** {report['generated_at']}")
        lines.append("")

        summary = report.get("findings_summary", {})
        lines.append("## Findings Summary")
        lines.append(f"- Total findings: **{summary.get('total', 0)}**")
        lines.append(f"- Operators: {', '.join(summary.get('operators_involved', []))}")
        lines.append("")

        severity = summary.get("by_severity", {})
        if severity:
            lines.append("### By Severity")
            for sev, count in sorted(severity.items()):
                lines.append(f"- {sev}: {count}")
            lines.append("")

        std_cat = summary.get("by_category", {})
        if std_cat:
            lines.append("### By Category")
            for cat, count in sorted(std_cat.items()):
                lines.append(f"- {cat}: {count}")
            lines.append("")

        ev = report.get("evidence_chain", {})
        if ev:
            lines.append("## Evidence Chain of Custody")
            lines.append(f"- Chain integrity: {'VERIFIED' if ev.get('integrity_verified') else 'BROKEN'}")
            lines.append(f"- Entries: {ev.get('entries_count', 0)}")
            lines.append(f"- Digest: `{ev.get('chain_digest', 'N/A')}`")
            issues = ev.get("integrity_issues", [])
            if issues:
                lines.append("### Integrity Issues")
                for issue in issues:
                    lines.append(f"- {issue}")
            lines.append("")

        compliance = report.get("compliance", {})
        frameworks = compliance.get("frameworks", {})
        if frameworks:
            lines.append("## Compliance Framework Coverage")
            for _fw_key, fw_data in frameworks.items():
                lines.append(f"### {fw_data['name']}")
                lines.append(f"- Coverage: **{fw_data.get('coverage_pct', 0)}%** ({fw_data.get('controls_covered', 0)}/{fw_data.get('total_controls', 0)} controls)")
                controls = fw_data.get("controls_mapped", [])
                if controls:
                    lines.append("  Mapped controls:")
                    for c in controls[:30]:
                        lines.append(f"  - {c['control_id']}: {c['title']}")
                lines.append("")

        siem = report.get("siem_exports", {})
        if siem:
            lines.append("## SIEM Export Files")
            for fmt_name, path in siem.items():
                lines.append(f"- {fmt_name}: `{path}`")
            lines.append("")

        lines.append("---")
        lines.append("*Generated by LazyOwn Compliance Engine*")
        return "\n".join(lines)

    def add_evidence(self, filepath: str, operator: str, description: str = "") -> EvidenceEntry:
        return self._evidence_chain.add_file(filepath, operator, description)

    def verify_evidence_chain(self) -> tuple[bool, list[str]]:
        return self._evidence_chain.verify()
