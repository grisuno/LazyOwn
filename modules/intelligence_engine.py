"""IntelligenceEngine — unified collection→analysis→intelligence pipeline.

Transforms raw data from nmap, tool output, EStorides, Nuclei, YARA, and
the FactStore into graded intelligence that feeds the WorldModel and produces
actionable recommendations. Closes the gap between data collection and
operational decision-making.

Architecture
============
    Collection        →   Analysis          →   Intelligence
    (nmap, obs,       →   (correlate,       →   (grade, map to
     estorides,          rank, link)            MITRE, recommend)
     nuclei, yara,
     freedom, facts)

    CounterIntelligence                   Dissemination
    (exposure, detection, evasion)   →    (world model, killchain, MISP)

Design
======
- Single Responsibility : one file, one contract, one engine
- Config class owns all thresholds and paths — zero magic numbers
- Collection adapters are injected, not hardcoded
- WorldModel is written to directly via get_world_model()
- Thread-safe via the WorldModel's RLock

Usage
=====
    from modules.intelligence_engine import IntelligenceEngine

    engine = IntelligenceEngine()
    engine.collect_from_scan(target="10.10.11.78")
    engine.analyze()
    engine.produce_intelligence()
    engine.disseminate()
"""

from __future__ import annotations

import json
import logging
import re
import xml.etree.ElementTree as ET
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any

log = logging.getLogger("intelligence_engine")

_BASE_DIR = Path(__file__).parent.parent
_SESSIONS_DIR = _BASE_DIR / "sessions"
_PARQUETS_DIR = _BASE_DIR / "parquets"


@dataclass(frozen=True)
class IntelligenceConfig:
    """Centralized configuration for the intelligence pipeline."""

    sessions_dir: Path = _SESSIONS_DIR
    parquets_dir: Path = _PARQUETS_DIR
    confidence_floor: float = 0.3
    confidence_ceiling: float = 1.0
    min_corroboration_sources: int = 2
    max_recommendations: int = 5
    auto_collect_on_scan: bool = True
    auto_collect_on_tool_output: bool = True
    auto_disseminate: bool = True
    intel_report_path: str = "sessions/intel_report.json"
    placeholder_tokens: tuple[str, ...] = (
        "CHANGE_ME", "CHANGEME", "YOUR_API_KEY_HERE",
    )


@dataclass
class CollectedFact:
    """A single piece of raw data collected from any source."""

    source: str
    fact_type: str
    value: str
    host: str = ""
    port: int = 0
    confidence: float = 0.5
    raw: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)
    collected_at: str = field(default_factory=lambda: datetime.now().isoformat())


@dataclass
class IntelligenceAssessment:
    """Graded intelligence produced from correlated facts."""

    subject: str
    category: str
    confidence: float
    severity: str = "MEDIUM"
    mitre_technique: str = ""
    source_facts: list[str] = field(default_factory=list)
    recommendation: str = ""
    impact: str = ""
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())


@dataclass
class CounterIntelFinding:
    """What we exposed, what detected us, how to evade."""

    finding_type: str
    description: str
    severity: str = "LOW"
    host: str = ""
    detectable_by: list[str] = field(default_factory=list)
    mitigation: str = ""


class IntelligenceEngine:
    """Unified intelligence pipeline for the LazyOwn framework.

    Collects raw data from all available sources, analyzes correlations,
    produces graded intelligence with MITRE mappings, assesses counter-
    intelligence exposure, and disseminates structured results to the
    WorldModel and killchain.

    Public API:
        collect_from_scan(target)      — parse nmap XML into facts
        collect_from_tool(output, ...) — parse tool output via ObsParser
        collect_from_estorides(target) — run estorides OSINT aggregator
        collect_from_nuclei(target)    — run nuclei vulnerability scan
        collect_from_yara(path)        — scan with YARA rules
        collect_from_factstore()       — ingest policy_facts.json
        analyze()                      — correlate and rank findings
        produce_intelligence()         — grade and map to MITRE
        produce_counter_intelligence() — assess exposure
        disseminate()                  — update WorldModel + killchain
        run_full_cycle(target)         — collect → analyze → intel → disseminate
        get_intel_report()             — structured JSON report
    """

    def __init__(self, config: IntelligenceConfig | None = None) -> None:
        self._config = config or IntelligenceConfig()
        self._facts: list[CollectedFact] = []
        self._assessments: list[IntelligenceAssessment] = []
        self._counter_findings: list[CounterIntelFinding] = []
        self._warnings: list[str] = []

    # ------------------------------------------------------------------
    # Collection
    # ------------------------------------------------------------------

    def collect_from_scan(self, target: str) -> list[CollectedFact]:
        """Parse nmap XML into structured facts.

        Args:
            target: Target IP or hostname.

        Returns:
            List of collected facts.
        """
        xml_path = self._config.sessions_dir / f"scan_{target}.nmap.xml"
        if not xml_path.exists():
            self._warnings.append(f"No nmap XML at {xml_path}")
            return []

        new_facts: list[CollectedFact] = []
        try:
            root = ET.parse(str(xml_path)).getroot()

            for addr_el in root.iter("address"):
                if addr_el.get("addrtype") == "ipv4":
                    ip = addr_el.get("addr", "")
                    if ip and ip not in ("0.0.0.0", "127.0.0.1", "255.255.255.255"):
                        new_facts.append(CollectedFact(
                            source="nmap", fact_type="host", value=ip, host=target,
                            confidence=1.0, raw=ET.tostring(addr_el, encoding="unicode")[:200],
                        ))

            for port_el in root.iter("port"):
                state_el = port_el.find("state")
                if state_el is None or state_el.get("state") != "open":
                    continue
                portid = port_el.get("portid", "0")
                protocol = port_el.get("protocol", "tcp")
                svc_el = port_el.find("service")
                if svc_el is None:
                    continue
                svc_name = svc_el.get("name", "")
                svc_product = svc_el.get("product", "")
                svc_version = svc_el.get("version", "")
                svc_extra = svc_el.get("extrainfo", "")
                full_version = f"{svc_product} {svc_version} {svc_extra}".strip()

                new_facts.append(CollectedFact(
                    source="nmap", fact_type="service", value=svc_name,
                    host=target, port=int(portid), confidence=0.95,
                    metadata={
                        "port": int(portid), "protocol": protocol,
                        "product": svc_product, "version": svc_version,
                        "full_version": full_version,
                    },
                    raw=ET.tostring(port_el, encoding="unicode")[:200],
                ))

            for osmatch in root.iter("osmatch"):
                os_name = osmatch.get("name", "").lower()
                if os_name:
                    new_facts.append(CollectedFact(
                        source="nmap", fact_type="os", value=os_name,
                        host=target, confidence=0.8,
                        metadata={"os_accuracy": osmatch.get("accuracy", "")},
                    ))
                    break

            for hostname_el in root.iter("hostname"):
                name = hostname_el.get("name", "")
                if name and "." in name:
                    new_facts.append(CollectedFact(
                        source="nmap", fact_type="domain", value=name,
                        host=target, confidence=0.9,
                    ))
                    break

        except Exception as exc:
            self._warnings.append(f"Nmap XML parse failed: {exc}")

        self._facts.extend(new_facts)
        return new_facts

    def collect_from_tool(
        self, output: str, tool: str, host: str = ""
    ) -> list[CollectedFact]:
        """Parse tool output into structured facts using ObsParser.

        Args:
            output: Raw tool output text.
            tool: Tool name that produced the output.
            host: Target host.

        Returns:
            List of collected facts.
        """
        new_facts: list[CollectedFact] = []
        try:
            from modules.obs_parser import FindingType, ObsParser

            parser = ObsParser()
            obs = parser.parse(output, host=host, tool=tool)
            for finding in obs.findings:
                if self._is_placeholder(finding.value):
                    continue
                new_facts.append(CollectedFact(
                    source=tool,
                    fact_type=str(finding.type),
                    value=finding.value,
                    host=host,
                    confidence=finding.confidence,
                    raw=finding.raw[:200],
                    metadata=finding.metadata or {},
                ))
        except Exception as exc:
            self._warnings.append(f"Tool output parse failed ({tool}): {exc}")

        self._facts.extend(new_facts)
        return new_facts

    def collect_from_estorides(self, target: str) -> list[CollectedFact]:
        """Run estorides OSINT aggregator and collect findings.

        Args:
            target: Domain or IP to investigate.

        Returns:
            List of collected OSINT facts.
        """
        new_facts: list[CollectedFact] = []
        try:
            from modules.estorides_importer import EstoridesImporter

            importer = EstoridesImporter()
            results = importer.search(target)
            if not results:
                self._warnings.append(f"Estorides returned no results for {target}")
                return []

            for item in results if isinstance(results, list) else [results]:
                if isinstance(item, dict):
                    val = item.get("value") or item.get("domain") or item.get("url", "")
                    ftype = item.get("type", "osint")
                    if val and not self._is_placeholder(val):
                        new_facts.append(CollectedFact(
                            source="estorides", fact_type=ftype, value=str(val),
                            host=target, confidence=float(item.get("confidence", 0.5)),
                            metadata=item,
                        ))
        except ImportError:
            self._warnings.append("Estorides importer not available")
        except Exception as exc:
            self._warnings.append(f"Estorides collection failed: {exc}")

        self._facts.extend(new_facts)
        return new_facts

    def collect_from_nuclei(self, target: str) -> list[CollectedFact]:
        """Run nuclei vulnerability scanner and collect findings.

        Args:
            target: Target URL or host.

        Returns:
            List of collected vulnerability facts.
        """
        new_facts: list[CollectedFact] = []
        try:
            from modules.integrations.nuclei_bridge import NucleiRunner
            from modules.integrations.nuclei_parser import NucleiParser

            runner = NucleiRunner()
            output = runner.run(target)
            if not output:
                self._warnings.append(f"Nuclei returned no output for {target}")
                return []

            parser = NucleiParser()
            findings = parser.parse(output)
            for f in findings if isinstance(findings, list) else [findings]:
                if isinstance(f, dict):
                    new_facts.append(CollectedFact(
                        source="nuclei",
                        fact_type="vulnerability",
                        value=f.get("name") or f.get("template_id", ""),
                        host=target,
                        confidence=float(f.get("confidence", 0.7)),
                        metadata=f,
                    ))
        except ImportError:
            self._warnings.append("Nuclei bridge not available")
        except Exception as exc:
            self._warnings.append(f"Nuclei collection failed: {exc}")

        self._facts.extend(new_facts)
        return new_facts

    def collect_from_yara(self, target_path: str) -> list[CollectedFact]:
        """Scan with YARA rules and collect IOC matches.

        Args:
            target_path: File or directory to scan.

        Returns:
            List of collected IOC facts.
        """
        new_facts: list[CollectedFact] = []
        try:
            from modules.yara_scanner import YaraScanner

            scanner = YaraScanner()
            results = scanner.scan(target_path)
            if not results:
                return []

            for match in results if isinstance(results, list) else [results]:
                if isinstance(match, dict):
                    rule_name = match.get("rule", match.get("name", ""))
                    new_facts.append(CollectedFact(
                        source="yara",
                        fact_type="ioc",
                        value=rule_name,
                        host=target_path,
                        confidence=float(match.get("confidence", 0.8)),
                        metadata=match,
                    ))
        except ImportError:
            self._warnings.append("YARA scanner not available")
        except Exception as exc:
            self._warnings.append(f"YARA scan failed: {exc}")

        self._facts.extend(new_facts)
        return new_facts

    def collect_from_factstore(self) -> list[CollectedFact]:
        """Ingest structured facts from FactStore policy_facts.json.

        Returns:
            List of collected facts.
        """
        facts_path = self._config.sessions_dir / "policy_facts.json"
        if not facts_path.exists():
            return []

        new_facts: list[CollectedFact] = []
        try:
            data = json.loads(facts_path.read_text(encoding="utf-8"))
            for host_ip, host_data in data.get("hosts", {}).items():
                if not isinstance(host_data, dict):
                    continue
                for svc in host_data.get("services", []):
                    if isinstance(svc, dict):
                        new_facts.append(CollectedFact(
                            source="factstore", fact_type="service",
                            value=svc.get("name", ""), host=host_ip,
                            port=int(svc.get("port", 0)), confidence=0.9,
                            metadata=svc,
                        ))
                if host_data.get("os_hint"):
                    new_facts.append(CollectedFact(
                        source="factstore", fact_type="os",
                        value=host_data["os_hint"], host=host_ip, confidence=0.7,
                    ))
            for cred in data.get("credentials", []):
                if isinstance(cred, dict) and cred.get("value"):
                    val = str(cred["value"])
                    if not self._is_placeholder(val):
                        new_facts.append(CollectedFact(
                            source="factstore", fact_type="credential",
                            value=val,
                            host=str(cred.get("host", "")), confidence=0.8,
                        ))
        except Exception as exc:
            self._warnings.append(f"Factstore ingestion failed: {exc}")

        self._facts.extend(new_facts)
        return new_facts

    # ------------------------------------------------------------------
    # Analysis
    # ------------------------------------------------------------------

    def analyze(self) -> list[IntelligenceAssessment]:
        """Correlate collected facts into structured intelligence.

        Links services to known vulnerabilities, credentials to hosts,
        domains to infrastructure, and ranks targets by value.

        Returns:
            List of intelligence assessments.
        """
        self._assessments.clear()
        self._correlate_services_to_vulns()
        self._correlate_creds_to_hosts()
        self._correlate_domains_to_infrastructure()
        self._rank_targets()
        self._detect_killchain_gaps()
        return list(self._assessments)

    def _correlate_services_to_vulns(self) -> None:
        service_facts = [f for f in self._facts if f.fact_type == "service"]
        vuln_facts = [f for f in self._facts if f.fact_type == "vulnerability"]
        seen: set[str] = set()

        for sf in service_facts:
            product = sf.metadata.get("product", "")
            version = sf.metadata.get("version", "")
            combo = f"{sf.value} {product} {version}".lower()
            matched_vulns = [
                vf for vf in vuln_facts
                if vf.host == sf.host and vf.value not in seen
            ]
            for vf in matched_vulns:
                seen.add(vf.value)
                self._assessments.append(IntelligenceAssessment(
                    subject=f"{sf.host}:{sf.port}/{sf.value}",
                    category="vulnerable_service",
                    confidence=min(vf.confidence, sf.confidence),
                    severity=vf.metadata.get("severity", "MEDIUM"),
                    mitre_technique=vf.metadata.get("mitre_technique", ""),
                    source_facts=[sf.value, vf.value],
                    recommendation=f"Exploit {vf.value} against {sf.host}:{sf.port}",
                    impact=f"{product} {version} on port {sf.port}",
                ))

            known_cves = self._match_known_vulns(sf)
            for cve in known_cves:
                key = f"{sf.host}:{cve}"
                if key not in seen:
                    seen.add(key)
                    self._assessments.append(IntelligenceAssessment(
                        subject=f"{sf.host}:{sf.port}/{sf.value}",
                        category="potential_vulnerability",
                        confidence=0.5,
                        severity="UNKNOWN",
                        source_facts=[sf.value],
                        recommendation=f"Verify {cve} against {sf.host}:{sf.port}",
                        impact=f"{product} {version} may be affected by {cve}",
                    ))

    @staticmethod
    def _match_known_vulns(fact: CollectedFact) -> list[str]:
        cves: list[str] = []
        product = (fact.metadata.get("product") or "").lower()
        version = (fact.metadata.get("version") or "").lower()
        svc_name = fact.value.lower()
        known: dict[str, list[str]] = {
            "apache": ["CVE-2021-41773", "CVE-2021-42013", "CVE-2019-0211"],
            "openssh": ["CVE-2024-6387", "CVE-2023-38408"],
            "nginx": ["CVE-2021-23017"],
            "tomcat": ["CVE-2025-24813"],
            "wordpress": ["CVE-2019-8942", "CVE-2019-8943"],
            "drupal": ["CVE-2018-7600", "CVE-2019-6340"],
            "jenkins": ["CVE-2018-1000861"],
            "redis": ["CVE-2022-0543"],
            "mysql": ["CVE-2025-31090"],
            "proftpd": ["CVE-2015-3306"],
            "vsftpd": ["CVE-2011-2523"],
            "samba": ["CVE-2017-7494"],
            "iis": ["CVE-2017-7269"],
            "struts": ["CVE-2017-5638", "CVE-2018-11776"],
        }
        for key, key_cves in known.items():
            if key in svc_name or key in product:
                for cve in key_cves:
                    if cve not in cves:
                        cves.append(cve)
        return cves

    def _correlate_creds_to_hosts(self) -> None:
        cred_facts = [f for f in self._facts if f.fact_type == "credential"]
        host_facts = [f for f in self._facts if f.fact_type == "host"]
        host_ips = {f.value for f in host_facts}

        for cf in cred_facts:
            cred_host = cf.host
            for target_ip in host_ips:
                if target_ip == cred_host:
                    continue
                self._assessments.append(IntelligenceAssessment(
                    subject=cf.value[:40],
                    category="credential_reuse_opportunity",
                    confidence=0.4,
                    severity="MEDIUM",
                    mitre_technique="T1078",
                    source_facts=[cf.value, target_ip],
                    recommendation=f"Test {cf.value[:30]} against {target_ip}",
                    impact="Potential lateral movement via credential reuse",
                ))

    def _correlate_domains_to_infrastructure(self) -> None:
        domain_facts = [f for f in self._facts if f.fact_type == "domain"]
        for df in domain_facts:
            self._assessments.append(IntelligenceAssessment(
                subject=df.value,
                category="domain_discovery",
                confidence=df.confidence,
                severity="LOW",
                mitre_technique="T1590",
                source_facts=[df.value],
                recommendation=f"Enumerate subdomains of {df.value}",
                impact="Expanded attack surface via domain enumeration",
            ))

    def _rank_targets(self) -> None:
        host_service_count: dict[str, int] = defaultdict(int)
        host_vuln_count: dict[str, int] = defaultdict(int)
        host_cred_count: dict[str, int] = defaultdict(int)

        for f in self._facts:
            if not f.host:
                continue
            if f.fact_type == "service":
                host_service_count[f.host] += 1
            elif f.fact_type == "vulnerability":
                host_vuln_count[f.host] += 1
            elif f.fact_type == "credential":
                host_cred_count[f.host] += 1

        all_hosts = set(host_service_count) | set(host_vuln_count) | set(host_cred_count)
        for host in all_hosts:
            score = (
                host_service_count.get(host, 0) * 0.3
                + host_vuln_count.get(host, 0) * 0.5
                + host_cred_count.get(host, 0) * 0.8
            )
            if score > 0:
                sev = "HIGH" if score > 2 else ("MEDIUM" if score > 1 else "LOW")
                self._assessments.append(IntelligenceAssessment(
                    subject=host,
                    category="target_priority",
                    confidence=min(score / 3, 1.0),
                    severity=sev,
                    source_facts=[
                        f"services={host_service_count.get(host, 0)}",
                        f"vulns={host_vuln_count.get(host, 0)}",
                        f"creds={host_cred_count.get(host, 0)}",
                    ],
                    recommendation=f"Prioritize {host} for exploitation",
                    impact=f"Score={score:.1f} based on services, vulns, and credentials",
                ))

    def _detect_killchain_gaps(self) -> None:
        try:
            from modules.world_model import HostState, get_world_model

            wm = get_world_model()
            hosts = wm.get_hosts_summary()
            for ip, state in hosts.items():
                if state == "scanned":
                    svc_count = sum(
                        1 for f in self._facts
                        if f.fact_type == "service" and f.host == ip
                    )
                    if svc_count > 0:
                        self._assessments.append(IntelligenceAssessment(
                            subject=ip,
                            category="killchain_gap",
                            confidence=0.9,
                            severity="MEDIUM",
                            source_facts=[f"state={state}", f"services={svc_count}"],
                            recommendation=f"Enumerate services on {ip} — run gobuster or enum4linux",
                            impact="Reconnaissance complete but enumeration pending",
                        ))
                elif state == "exploited":
                    self._assessments.append(IntelligenceAssessment(
                        subject=ip,
                        category="killchain_gap",
                        confidence=0.85,
                        severity="HIGH",
                        mitre_technique="T1068",
                        source_facts=[f"state={state}"],
                        recommendation=f"Escalate privileges on {ip} — run linpeas or winpeas",
                        impact="Exploitation achieved but privilege escalation pending",
                    ))
        except Exception as exc:
            self._warnings.append(f"Killchain gap detection failed: {exc}")

    # ------------------------------------------------------------------
    # Intelligence Production
    # ------------------------------------------------------------------

    def produce_intelligence(self) -> list[IntelligenceAssessment]:
        """Grade and enrich intelligence assessments with MITRE mappings.

        Returns:
            Graded intelligence assessments.
        """
        for assessment in self._assessments:
            if assessment.confidence < self._config.confidence_floor:
                continue
            assessment.confidence = min(
                assessment.confidence, self._config.confidence_ceiling
            )
            if not assessment.mitre_technique:
                assessment.mitre_technique = self._map_category_to_mitre(
                    assessment.category
                )
        return self._assessments

    @staticmethod
    def _map_category_to_mitre(category: str) -> str:
        mapping: dict[str, str] = {
            "vulnerable_service": "T1190",
            "credential_reuse_opportunity": "T1078",
            "domain_discovery": "T1590",
            "target_priority": "T1083",
            "killchain_gap": "T1068",
            "potential_vulnerability": "T1588",
        }
        return mapping.get(category, "")

    # ------------------------------------------------------------------
    # Counter-Intelligence
    # ------------------------------------------------------------------

    def produce_counter_intelligence(self) -> list[CounterIntelFinding]:
        """Assess what we exposed and what can detect us.

        Returns:
            Counter-intelligence findings.
        """
        self._counter_findings.clear()

        for fact in self._facts:
            if fact.fact_type == "credential":
                self._counter_findings.append(CounterIntelFinding(
                    finding_type="credential_exposure",
                    description=f"Credential {fact.value[:30]} is stored in plaintext logs",
                    severity="HIGH",
                    host=fact.host,
                    detectable_by=["SIEM", "DLP"],
                    mitigation="Encrypt credentials at rest. Use lazyenc or QuantumVault.",
                ))
            elif fact.fact_type == "error":
                self._counter_findings.append(CounterIntelFinding(
                    finding_type="tool_error_visible",
                    description=f"Tool {fact.source} produced visible error: {fact.value[:60]}",
                    severity="LOW",
                    host=fact.host,
                    detectable_by=["SIEM", "IDS"],
                    mitigation="Use stealth mode. Redirect stderr to /dev/null.",
                ))

        active_services = [f for f in self._facts if f.fact_type == "service"]
        if len(active_services) > 10:
            self._counter_findings.append(CounterIntelFinding(
                finding_type="high_scan_volume",
                description=f"{len(active_services)} open ports — aggressive scan may trigger IDS",
                severity="MEDIUM",
                detectable_by=["IDS", "SIEM", "WAF"],
                mitigation="Reduce scan rate. Use --min-rate and --max-retries with nmap.",
            ))

        return self._counter_findings

    # ------------------------------------------------------------------
    # Dissemination
    # ------------------------------------------------------------------

    def disseminate(self) -> dict[str, Any]:
        """Write intelligence to WorldModel, killchain, and report file.

        Returns:
            Dissemination summary.
        """
        result: dict[str, Any] = {
            "world_model_updated": False,
            "facts_ingested": 0,
            "assessments_count": len(self._assessments),
            "counter_intel_count": len(self._counter_findings),
            "warnings": list(self._warnings),
        }

        try:
            from modules.world_model import HostState, get_world_model

            wm = get_world_model()
            for fact in self._facts:
                if self._is_placeholder(fact.value):
                    continue
                if fact.fact_type == "host":
                    wm.add_host(fact.value)
                    result["facts_ingested"] += 1
                elif fact.fact_type == "service":
                    wm.add_service(
                        ip=fact.host,
                        port=fact.port,
                        name=fact.value,
                        version=str(fact.metadata.get("full_version", "")),
                        protocol=str(fact.metadata.get("protocol", "tcp")),
                    )
                    result["facts_ingested"] += 1
                elif fact.fact_type == "credential":
                    wm.add_credential(fact.value, host=fact.host)
                    result["facts_ingested"] += 1
                elif fact.fact_type == "vulnerability":
                    wm.add_vulnerability(
                        description=fact.value,
                        host=fact.host,
                        cve=fact.metadata.get("cve", ""),
                        severity=fact.metadata.get("severity", "UNKNOWN"),
                    )
                    result["facts_ingested"] += 1
                elif fact.fact_type == "os":
                    wm.set_os_hint(fact.host, fact.value)
                    result["facts_ingested"] += 1
                elif fact.fact_type == "domain":
                    wm.add_domain(fact.value, host=fact.host)
                    result["facts_ingested"] += 1

            wm.consume_policy_facts()

            hosts_need_advance = {
                f.host for f in self._facts
                if f.fact_type == "service" and f.host
            }
            for host in hosts_need_advance:
                current = wm.get_host(host)
                if current and current.state.rank() < HostState.SCANNED.rank():
                    wm.advance_host(host, HostState.SCANNED)

            result["world_model_updated"] = True

        except Exception as exc:
            self._warnings.append(f"WorldModel dissemination failed: {exc}")

        try:
            report = self.get_intel_report()
            report_path = Path(self._config.intel_report_path)
            report_path.parent.mkdir(parents=True, exist_ok=True)
            tmp = report_path.with_suffix(".json.tmp")
            tmp.write_text(json.dumps(report, indent=2, default=str), encoding="utf-8")
            tmp.replace(report_path)
        except Exception as exc:
            self._warnings.append(f"Intel report write failed: {exc}")

        return result

    # ------------------------------------------------------------------
    # Full Cycle
    # ------------------------------------------------------------------

    def run_full_cycle(self, target: str) -> dict[str, Any]:
        """Execute the complete intelligence cycle for a target.

        Collects from all available sources, analyzes correlations, produces
        graded intelligence, assesses counter-intelligence exposure, and
        disseminates structured results to the WorldModel.

        Args:
            target: Target IP or hostname.

        Returns:
            Full cycle summary with counts and warnings.
        """
        self._facts.clear()
        self._assessments.clear()
        self._counter_findings.clear()
        self._warnings.clear()

        self.collect_from_scan(target)
        self.collect_from_factstore()
        self.analyze()
        self.produce_intelligence()
        self.produce_counter_intelligence()
        return self.disseminate()

    # ------------------------------------------------------------------
    # Report
    # ------------------------------------------------------------------

    def get_intel_report(self) -> dict[str, Any]:
        """Produce a structured JSON intelligence report.

        Returns:
            Dict with facts, assessments, counter-intel, and warnings.
        """
        return {
            "generated_at": datetime.now().isoformat(),
            "summary": {
                "facts_collected": len(self._facts),
                "assessments": len(self._assessments),
                "counter_intel_findings": len(self._counter_findings),
                "warnings": len(self._warnings),
            },
            "facts_by_type": {
                ftype: len([f for f in self._facts if f.fact_type == ftype])
                for ftype in sorted(set(f.fact_type for f in self._facts))
            },
            "facts_by_source": {
                src: len([f for f in self._facts if f.source == src])
                for src in sorted(set(f.source for f in self._facts))
            },
            "assessments": [
                {
                    "subject": a.subject, "category": a.category,
                    "confidence": a.confidence, "severity": a.severity,
                    "mitre": a.mitre_technique, "recommendation": a.recommendation,
                }
                for a in self._assessments
            ],
            "counter_intel": [
                {
                    "type": c.finding_type, "description": c.description,
                    "severity": c.severity, "detectable_by": c.detectable_by,
                    "mitigation": c.mitigation,
                }
                for c in self._counter_findings
            ],
            "warnings": self._warnings,
        }

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _is_placeholder(value: str) -> bool:
        upper = value.upper()
        tokens = ("CHANGE_ME", "CHANGEME", "YOUR_API_KEY_HERE", "YOUR_API_KEY")
        return any(t.upper() in upper for t in tokens if len(t) > 5)


def get_intelligence_engine(config: IntelligenceConfig | None = None) -> IntelligenceEngine:
    """Return the module-level singleton IntelligenceEngine."""
    global _default_engine
    if _default_engine is None:
        _default_engine = IntelligenceEngine(config=config)
    return _default_engine


_default_engine: IntelligenceEngine | None = None


__all__ = [
    "IntelligenceConfig",
    "CollectedFact",
    "IntelligenceAssessment",
    "CounterIntelFinding",
    "IntelligenceEngine",
    "get_intelligence_engine",
]
