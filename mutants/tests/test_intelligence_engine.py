"""Tests for IntelligenceEngine — collection, analysis, intelligence, dissemination."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from modules.intelligence_engine import (
    CollectedFact,
    IntelligenceAssessment,
    IntelligenceConfig,
    IntelligenceEngine,
)


@pytest.fixture
def engine():
    return IntelligenceEngine()


@pytest.fixture
def nmap_xml(tmp_path):
    xml = tmp_path / "sessions" / "scan_10.0.0.1.nmap.xml"
    xml.parent.mkdir(parents=True, exist_ok=True)
    xml.write_text("""<?xml version="1.0"?>
<!DOCTYPE nmaprun>
<nmaprun scanner="nmap">
<host>
  <address addr="10.0.0.1" addrtype="ipv4"/>
  <address addr="10.0.0.2" addrtype="ipv4"/>
  <hostnames><hostname name="target.corp.local" type="user"/></hostnames>
  <ports>
    <port protocol="tcp" portid="22"><state state="open"/><service name="ssh" product="OpenSSH" version="8.9p1"/></port>
    <port protocol="tcp" portid="80"><state state="open"/><service name="http" product="Apache httpd" version="2.4.49"/></port>
    <port protocol="tcp" portid="443"><state state="closed"/></port>
  </ports>
  <os><osmatch name="Linux 5.15" accuracy="98"/></os>
</host>
</nmaprun>""")
    return xml


class TestCollection:
    def test_collect_from_scan_services(self, engine, nmap_xml):
        engine._config = IntelligenceConfig(sessions_dir=nmap_xml.parent)
        facts = engine.collect_from_scan("10.0.0.1")
        assert len(facts) >= 2
        services = [f for f in facts if f.fact_type == "service"]
        assert len(services) == 2
        ssh = next(f for f in services if f.value == "ssh")
        assert ssh.port == 22
        assert ssh.metadata["product"] == "OpenSSH"

    def test_collect_from_scan_os(self, engine, nmap_xml):
        engine._config = IntelligenceConfig(sessions_dir=nmap_xml.parent)
        facts = engine.collect_from_scan("10.0.0.1")
        os_facts = [f for f in facts if f.fact_type == "os"]
        assert len(os_facts) == 1
        assert "linux" in os_facts[0].value

    def test_collect_from_scan_domain(self, engine, nmap_xml):
        engine._config = IntelligenceConfig(sessions_dir=nmap_xml.parent)
        facts = engine.collect_from_scan("10.0.0.1")
        domains = [f for f in facts if f.fact_type == "domain"]
        assert len(domains) == 1
        assert domains[0].value == "target.corp.local"

    def test_collect_from_scan_hosts(self, engine, nmap_xml):
        engine._config = IntelligenceConfig(sessions_dir=nmap_xml.parent)
        facts = engine.collect_from_scan("10.0.0.1")
        hosts = [f for f in facts if f.fact_type == "host"]
        assert any("10.0.0.2" in h.value for h in hosts)

    def test_collect_from_scan_missing_xml(self, engine):
        engine._config = IntelligenceConfig(sessions_dir=Path("/nonexistent"))
        facts = engine.collect_from_scan("10.0.0.99")
        assert facts == []

    def test_collect_from_tool_parses_creds(self, engine):
        facts = engine.collect_from_tool(
            "[+] admin:P@ssw0rd!", tool="crackmapexec", host="10.0.0.1"
        )
        creds = [f for f in facts if f.fact_type == "credential"]
        assert len(creds) >= 1

    def test_collect_from_tool_filters_placeholders(self, engine):
        facts = engine.collect_from_tool(
            "admin:CHANGE_ME please update", tool="manual", host="10.0.0.1"
        )
        creds = [f for f in facts if f.fact_type == "credential"]
        assert len(creds) == 0

    def test_collect_from_factstore(self, engine, tmp_path):
        facts_path = tmp_path / "policy_facts.json"
        facts_path.write_text(json.dumps({
            "hosts": {"10.1.1.1": {"services": [
                {"port": 22, "name": "ssh", "version": "OpenSSH", "protocol": "tcp"}
            ]}},
            "credentials": [{"value": "admin:realpass", "host": "10.1.1.1"}],
        }))
        engine._config = IntelligenceConfig(sessions_dir=tmp_path)
        facts = engine.collect_from_factstore()
        assert len(facts) >= 2


class TestAnalysis:
    def test_analyze_produces_assessments(self, engine, nmap_xml):
        engine._config = IntelligenceConfig(sessions_dir=nmap_xml.parent)
        engine.collect_from_scan("10.0.0.1")
        assessments = engine.analyze()
        assert len(assessments) >= 1

    def test_analyze_maps_apache_cve(self, engine):
        engine._facts = [
            CollectedFact(source="nmap", fact_type="service", value="http",
                          host="10.0.0.1", port=80, confidence=0.95,
                          metadata={"product": "Apache httpd", "version": "2.4.49",
                                    "full_version": "Apache httpd 2.4.49"}),
        ]
        assessments = engine.analyze()
        apache = [a for a in assessments if "CVE-2021-41773" in a.recommendation]
        assert len(apache) >= 1

    def test_analyze_correlates_creds_to_hosts(self, engine):
        engine._facts = [
            CollectedFact(source="nmap", fact_type="host", value="10.0.0.1",
                          host="10.0.0.1", confidence=1.0),
            CollectedFact(source="nmap", fact_type="host", value="10.0.0.2",
                          host="10.0.0.1", confidence=1.0),
            CollectedFact(source="crackmapexec", fact_type="credential",
                          value="admin:pass", host="10.0.0.1", confidence=0.9),
        ]
        assessments = engine.analyze()
        reuse = [a for a in assessments if a.category == "credential_reuse_opportunity"]
        assert len(reuse) >= 1

    def test_analyze_ranks_targets(self, engine):
        engine._facts = [
            CollectedFact(source="nmap", fact_type="service", value="ssh",
                          host="10.0.0.1", port=22, confidence=0.95),
            CollectedFact(source="nmap", fact_type="service", value="http",
                          host="10.0.0.1", port=80, confidence=0.95),
            CollectedFact(source="nuclei", fact_type="vulnerability", value="CVE-2021-41773",
                          host="10.0.0.1", confidence=0.8),
            CollectedFact(source="crackmapexec", fact_type="credential",
                          value="admin:pass", host="10.0.0.1", confidence=0.9),
        ]
        assessments = engine.analyze()
        rankings = [a for a in assessments if a.category == "target_priority"]
        assert len(rankings) >= 1


class TestIntelligenceProduction:
    def test_produce_intelligence_grades_assessments(self, engine):
        engine._assessments = [
            IntelligenceAssessment(
                subject="test", category="vulnerable_service",
                confidence=0.1, severity="LOW",
            ),
            IntelligenceAssessment(
                subject="test2", category="vulnerable_service",
                confidence=0.9, severity="HIGH",
            ),
        ]
        engine.produce_intelligence()


class TestCounterIntelligence:
    def test_credential_exposure_detected(self, engine):
        engine._facts = [
            CollectedFact(source="crackmapexec", fact_type="credential",
                          value="admin:P@ssw0rd", host="10.0.0.1"),
        ]
        findings = engine.produce_counter_intelligence()
        cred_exposures = [c for c in findings if c.finding_type == "credential_exposure"]
        assert len(cred_exposures) >= 1
        assert "SIEM" in cred_exposures[0].detectable_by

    def test_high_scan_volume_detected(self, engine):
        engine._facts = [
            CollectedFact(source="nmap", fact_type="service", value=f"svc{i}",
                          host="10.0.0.1", port=i) for i in range(15)
        ]
        findings = engine.produce_counter_intelligence()
        scans = [c for c in findings if c.finding_type == "high_scan_volume"]
        assert len(scans) >= 1


class TestFullCycle:
    def test_run_full_cycle_returns_summary(self, engine, nmap_xml):
        engine._config = IntelligenceConfig(sessions_dir=nmap_xml.parent)
        result = engine.run_full_cycle("10.0.0.1")
        assert result["facts_ingested"] > 0
        assert result["assessments_count"] > 0

    def test_get_intel_report_structured(self, engine, nmap_xml):
        engine._config = IntelligenceConfig(sessions_dir=nmap_xml.parent)
        engine.run_full_cycle("10.0.0.1")
        report = engine.get_intel_report()
        assert "summary" in report
        assert "facts_by_type" in report
        assert "assessments" in report
        assert "counter_intel" in report


class TestPlaceholderFiltering:
    def test_is_placeholder_detects_change_me(self, engine):
        assert engine._is_placeholder("CHANGE_ME:password")
        assert engine._is_placeholder("admin:CHANGEME")

    def test_is_placeholder_rejects_real_values(self, engine):
        assert not engine._is_placeholder("admin:realpass123")
        assert not engine._is_placeholder("j.fleischman:J0elTHEM4n1990!")
