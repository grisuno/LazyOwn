"""Phase 1 data-gap closure: SDD + TDD + BDD tests.

Covers four critical gaps:
    1. service_version findings now populate structured add_service() via metadata
    2. domain / email / error findings are consumed instead of dropped
    3. GraphTopologySignal feeds pivot_candidates into RecommendationEngine
    4. AutonomousExploitEngine retries exploits with newly-captured credentials
"""

from __future__ import annotations

import json
import tempfile
from pathlib import Path

import pytest

from modules.obs_parser import (
    Finding,
    FindingType,
    ObsParser,
    _EmailExtractor,
    _ServiceVersionExtractor,
)
from modules.world_model import (
    DomainEntry,
    EmailEntry,
    HostState,
    VulnerabilityEntry,
    WorldModel,
)

BASE_DIR = Path(__file__).resolve().parent.parent


@pytest.fixture
def parser():
    return ObsParser()


@pytest.fixture
def world_model():
    with tempfile.TemporaryDirectory() as d:
        path = Path(d) / "test_world_model.json"
        wm = WorldModel(path=str(path))
        yield wm
        wm.reset()


def _make_finding(ftype: str, value: str, host: str = "", metadata: dict | None = None):
    return Finding(type=ftype, value=value, host=host, metadata=metadata or {})


# ─── GAP-1: Finding.metadata + ServiceVersionExtractor ──────────────────────


class TestFindingMetadata:
    def test_finding_has_metadata_default_empty(self):
        f = Finding(type=FindingType.IP, value="10.0.0.1")
        assert f.metadata == {}

    def test_finding_accepts_metadata(self):
        f = Finding(type=FindingType.SERVICE_VERSION, value="http Apache",
                    host="10.0.0.1", metadata={"port": 80, "protocol": "tcp"})
        assert f.metadata["port"] == 80
        assert f.metadata["protocol"] == "tcp"


class TestServiceVersionExtractor:
    def test_port_and_protocol_in_metadata(self):
        ext = _ServiceVersionExtractor()
        findings = ext.extract(
            "22/tcp open ssh OpenSSH 8.9p1", host="10.0.0.1"
        )
        assert len(findings) == 1
        assert findings[0].metadata["port"] == 22
        assert findings[0].metadata["protocol"] == "tcp"
        assert findings[0].value == "ssh OpenSSH 8.9p1"

    def test_multiple_services_extracted(self):
        ext = _ServiceVersionExtractor()
        text = (
            "80/tcp  open  http Apache 2.4.49\n"
            "443/tcp open  https\n"
            "3306/tcp open mysql 5.7.42\n"
        )
        findings = ext.extract(text, host="10.0.0.1")
        assert len(findings) == 3
        ports = {f.metadata["port"] for f in findings}
        assert ports == {80, 443, 3306}
        protocols = {f.metadata["protocol"] for f in findings}
        assert protocols == {"tcp"}

    def test_udp_service_captured(self):
        ext = _ServiceVersionExtractor()
        findings = ext.extract(
            "161/udp open snmp SNMPv1", host="10.0.0.1"
        )
        assert len(findings) == 1
        assert findings[0].metadata["port"] == 161
        assert findings[0].metadata["protocol"] == "udp"
        assert "snmp" in findings[0].value.lower()


# ─── GAP-1: EmailExtractor ─────────────────────────────────────────────────


class TestEmailExtractor:
    def test_extracts_single_email(self):
        ext = _EmailExtractor()
        findings = ext.extract(
            "Contact: admin@domain.com for support", host="10.0.0.1"
        )
        assert len(findings) == 1
        assert findings[0].value == "admin@domain.com"
        assert findings[0].type == FindingType.EMAIL

    def test_extracts_multiple_emails(self):
        ext = _EmailExtractor()
        findings = ext.extract(
            "From: alice@corp.com To: bob@corp.com, carol@corp.com",
            host="10.0.0.1",
        )
        assert len(findings) == 3

    def test_deduplicates_emails(self):
        ext = _EmailExtractor()
        findings = ext.extract(
            "admin@test.com repeated admin@test.com", host="10.0.0.1"
        )
        assert len(findings) == 1

    def test_ignores_non_email(self):
        ext = _EmailExtractor()
        findings = ext.extract("no email here just text", host="10.0.0.1")
        assert len(findings) == 0


class TestObsParserIncludesEmailExtractor:
    def test_parser_extracts_emails_from_output(self, parser):
        obs = parser.parse(
            "Info: root@company.com is the admin\n"
            "80/tcp  open  http\n",
            host="10.0.0.1",
            tool="recon",
        )
        emails = obs.by_type(FindingType.EMAIL)
        assert len(emails) >= 1
        assert emails[0].value == "root@company.com"

    def test_parser_still_extracts_service_versions_with_metadata(self, parser):
        obs = parser.parse(
            "22/tcp open ssh OpenSSH 9.2\n"
            "80/tcp open http nginx 1.24.0\n",
            host="10.0.0.1",
            tool="nmap",
        )
        svcs = obs.by_type(FindingType.SERVICE_VERSION)
        assert len(svcs) == 2
        for f in svcs:
            assert "port" in f.metadata
            assert "protocol" in f.metadata
            assert f.metadata["port"] > 0


# ─── GAP-2: EmailEntry, DomainEntry ────────────────────────────────────────


class TestEmailAndDomainEntries:
    def test_email_entry_defaults(self):
        e = EmailEntry(address="test@corp.com")
        assert e.address == "test@corp.com"
        assert e.host == ""
        assert e.context == ""

    def test_domain_entry_defaults(self):
        d = DomainEntry(domain="corp.com")
        assert d.domain == "corp.com"
        assert d.host == ""


# ─── GAP-2: add_email / add_domain ─────────────────────────────────────────


class TestWorldModelEmailDomain:
    def test_add_email_stores_and_deduplicates(self, world_model):
        world_model.add_email("admin@corp.com", host="10.0.0.1")
        world_model.add_email("admin@corp.com", host="10.0.0.1")
        assert len(world_model._emails) == 1
        assert world_model._emails[0].address == "admin@corp.com"

    def test_add_domain_stores_and_adds_note(self, world_model):
        world_model.add_host("10.0.0.1")
        world_model.add_domain("corp.com", host="10.0.0.1")
        assert len(world_model._domains) == 1
        assert world_model._domains[0].domain == "corp.com"
        host = world_model.get_host("10.0.0.1")
        assert any("domain: corp.com" in n for n in host.notes)

    def test_add_domain_without_host(self, world_model):
        world_model.add_domain("external.org")
        assert len(world_model._domains) == 1
        assert world_model._domains[0].host == ""


# ─── GAP-2: update_from_findings handlers ──────────────────────────────────


class TestUpdateFromFindings:
    def test_service_version_calls_add_service(self, world_model):
        findings = [
            _make_finding("service_version", "http Apache 2.4.49",
                         host="10.0.0.1",
                         metadata={"port": 80, "protocol": "tcp"}),
        ]
        world_model.update_from_findings(findings)
        host = world_model.get_host("10.0.0.1")
        assert host is not None
        svc = host.services.get(80)
        assert svc is not None
        assert svc.name == "http"
        assert "Apache" in svc.version

    def test_service_version_no_longer_adds_note(self, world_model):
        findings = [
            _make_finding("service_version", "ssh OpenSSH 8.9",
                         host="10.0.0.1",
                         metadata={"port": 22, "protocol": "tcp"}),
        ]
        world_model.update_from_findings(findings)
        host = world_model.get_host("10.0.0.1")
        service_notes = [n for n in host.notes if n.startswith("service:")]
        assert len(service_notes) == 0
        svc = host.services.get(22)
        assert svc is not None
        assert svc.name == "ssh"

    def test_domain_finding_calls_add_domain(self, world_model):
        findings = [
            _make_finding("domain", "corp.local", host="10.0.0.1"),
        ]
        world_model.update_from_findings(findings)
        assert len(world_model._domains) >= 1
        assert any(d.domain == "corp.local" for d in world_model._domains)

    def test_email_finding_calls_add_email(self, world_model):
        findings = [
            _make_finding("email", "admin@corp.local", host="10.0.0.1"),
        ]
        world_model.update_from_findings(findings)
        assert len(world_model._emails) >= 1
        assert any(e.address == "admin@corp.local" for e in world_model._emails)

    def test_error_finding_adds_note(self, world_model):
        findings = [
            _make_finding("error", "connection refused", host="10.0.0.1"),
        ]
        world_model.update_from_findings(findings)
        host = world_model.get_host("10.0.0.1")
        assert host is not None
        assert any("error:" in n for n in host.notes)

    def test_error_finding_no_host_uses_sentinel(self, world_model):
        findings = [
            _make_finding("error", "timeout", host=""),
        ]
        world_model.update_from_findings(findings)
        sentinel = world_model.get_host("0.0.0.0")
        assert sentinel is not None
        assert any("global_error:" in n for n in sentinel.notes)


# ─── GAP-2: consume_policy_facts ───────────────────────────────────────────


class TestConsumePolicyFacts:
    def test_consume_empty_file_returns_zero(self, world_model, tmp_path):
        facts_path = tmp_path / "empty_facts.json"
        facts_path.write_text("{}")
        ingested = world_model.consume_policy_facts(facts_path)
        assert ingested == 0

    def test_consume_ingests_hosts_and_services(self, world_model, tmp_path):
        facts = {
            "hosts": {
                "10.10.10.1": {
                    "services": [
                        {"port": 80, "name": "http", "version": "nginx", "protocol": "tcp"},
                        {"port": 443, "name": "https", "version": "nginx", "protocol": "tcp"},
                    ],
                    "os_hint": "linux",
                },
                "10.10.10.2": {
                    "services": [{"port": 22, "name": "ssh", "version": "OpenSSH", "protocol": "tcp"}],
                },
            },
            "credentials": [
                {"value": "admin:password123", "host": "10.10.10.1", "service": "http"},
            ],
            "vulnerabilities": [
                {"description": "SQLi on /api", "host": "10.10.10.1", "cve": "CVE-2024-0001", "severity": "HIGH"},
            ],
            "domains": [
                {"domain": "corp.internal", "host": "10.10.10.1"},
            ],
            "emails": [
                {"address": "admin@corp.internal", "host": "10.10.10.1"},
            ],
        }
        facts_path = tmp_path / "test_facts.json"
        facts_path.write_text(json.dumps(facts))
        ingested = world_model.consume_policy_facts(facts_path)
        assert ingested > 0

        hosts = world_model.get_hosts_summary()
        assert "10.10.10.1" in hosts
        assert "10.10.10.2" in hosts

        host1 = world_model.get_host("10.10.10.1")
        assert host1.services[80].name == "http"
        assert host1.services[443].name == "https"
        assert host1.os_hint == "linux"

        assert len(world_model._creds) >= 1
        assert len(world_model._vulns) >= 1
        assert len(world_model._domains) >= 1
        assert len(world_model._emails) >= 1

    def test_consume_nonexistent_file_returns_zero(self, world_model):
        ingested = world_model.consume_policy_facts("/nonexistent/path/facts.json")
        assert ingested == 0

    def test_consume_malformed_json_returns_zero(self, world_model, tmp_path):
        bad_path = tmp_path / "bad_facts.json"
        bad_path.write_text("not valid json")
        ingested = world_model.consume_policy_facts(bad_path)
        assert ingested == 0


# ─── GAP-2: persistence round-trip ─────────────────────────────────────────


class TestWorldModelPersistence:
    def test_emails_and_domains_survive_roundtrip(self, world_model):
        world_model.add_host("10.0.0.1")
        world_model.add_email("admin@test.com", host="10.0.0.1")
        world_model.add_domain("test.com", host="10.0.0.1")
        world_model.add_domain("other.org")

        wm2 = WorldModel(path=world_model._path)
        try:
            assert len(wm2._emails) == 1
            assert wm2._emails[0].address == "admin@test.com"
            assert len(wm2._domains) == 2
            domain_names = {d.domain for d in wm2._domains}
            assert domain_names == {"test.com", "other.org"}
        finally:
            wm2.reset()

    def test_reset_clears_emails_and_domains(self, world_model):
        world_model.add_email("test@corp.com")
        world_model.add_domain("corp.com")
        world_model.reset()
        assert len(world_model._emails) == 0
        assert len(world_model._domains) == 0

    def test_snapshot_includes_emails_and_domains(self, world_model):
        world_model.add_email("a@b.com")
        world_model.add_domain("b.com")
        snap = world_model.snapshot()
        assert "emails" in snap
        assert "domains" in snap
        assert len(snap["emails"]) == 1
        assert len(snap["domains"]) == 1

    def test_to_context_string_has_email_domain_counts(self, world_model):
        world_model.add_email("a@b.com")
        world_model.add_domain("b.com")
        ctx = world_model.to_context_string()
        assert "Emails: 1" in ctx
        assert "Domains: 1" in ctx


# ─── GAP-3: GraphTopologySignal ────────────────────────────────────────────


class TestGraphTopologySignal:
    def test_returns_empty_on_nonexistent_world_model(self):
        from cli.recommendation_signals import (
            GraphTopologySignal,
            RecommendationContext,
        )
        signal = GraphTopologySignal(sessions_dir="/nonexistent")
        ctx = RecommendationContext(
            target="10.0.0.1", payload={}, recent_commands=[], phase="lateral", limit=5
        )
        proposals = signal.propose(ctx)
        assert proposals == []

    def test_produces_lateral_proposals_from_host_nodes(self, tmp_path):
        from cli.recommendation_signals import (
            GraphTopologySignal,
            KIND_COMMAND,
            RecommendationContext,
        )
        sessions = tmp_path / "sessions"
        sessions.mkdir()
        wm_data = {
            "pivot_candidates": [
                {
                    "node": "host:10.10.10.5",
                    "centrality": 0.85,
                    "out_degree": 3,
                    "in_degree": 2,
                    "neighbors": ["host:10.10.10.1", "host:10.10.10.2", "host:10.10.10.3"],
                },
                {
                    "node": "cred:adm::passwor",
                    "centrality": 0.6,
                    "out_degree": 4,
                    "in_degree": 1,
                    "neighbors": ["host:10.10.10.1", "host:10.10.10.2"],
                },
            ],
        }
        (sessions / "world_model.json").write_text(json.dumps(wm_data))
        signal = GraphTopologySignal(sessions_dir=str(sessions))
        ctx = RecommendationContext(
            target="10.10.10.1", payload={}, recent_commands=[], phase="lateral", limit=5
        )
        proposals = signal.propose(ctx)
        assert len(proposals) >= 1
        host_proposal = next((p for p in proposals if "10.10.10.5" in p.action), None)
        assert host_proposal is not None
        assert host_proposal.kind == KIND_COMMAND
        assert host_proposal.category == "lateral"

    def test_produces_credential_spray_proposals(self, tmp_path):
        from cli.recommendation_signals import (
            GraphTopologySignal,
            RecommendationContext,
        )
        sessions = tmp_path / "sessions"
        sessions.mkdir()
        wm_data = {
            "pivot_candidates": [
                {
                    "node": "cred:admin:pass",
                    "centrality": 0.75,
                    "out_degree": 5,
                    "in_degree": 1,
                    "neighbors": ["host:10.10.10.1", "host:10.10.10.2"],
                },
            ],
        }
        (sessions / "world_model.json").write_text(json.dumps(wm_data))
        signal = GraphTopologySignal(sessions_dir=str(sessions))
        ctx = RecommendationContext(
            target="10.10.10.1", payload={}, recent_commands=[], phase="lateral", limit=5
        )
        proposals = signal.propose(ctx)
        cred_proposal = next((p for p in proposals if p.action == "credential_spray"), None)
        assert cred_proposal is not None
        assert cred_proposal.category == "lateral"

    def test_computes_centrality_from_graph_when_no_candidates(self, tmp_path):
        from cli.recommendation_signals import (
            GraphTopologySignal,
            RecommendationContext,
        )
        sessions = tmp_path / "sessions"
        sessions.mkdir()
        wm_data = {
            "network_graph": {
                "nodes": ["host:10.10.10.1", "host:10.10.10.2", "host:10.10.10.3",
                          "service:smb", "cred:adm:pass"],
                "relations": [
                    {"source": "host:10.10.10.1", "target": "service:smb", "relation": "runs_service"},
                    {"source": "host:10.10.10.1", "target": "cred:adm:pass", "relation": "exposes_credential"},
                    {"source": "cred:adm:pass", "target": "host:10.10.10.2", "relation": "may_authenticate_to"},
                    {"source": "cred:adm:pass", "target": "host:10.10.10.3", "relation": "may_authenticate_to"},
                ],
            },
        }
        (sessions / "world_model.json").write_text(json.dumps(wm_data))
        signal = GraphTopologySignal(sessions_dir=str(sessions))
        ctx = RecommendationContext(
            target="10.10.10.1", payload={}, recent_commands=[], phase="lateral", limit=5
        )
        proposals = signal.propose(ctx)
        assert len(proposals) >= 1

    def test_signals_are_wired_in_build_default_engine(self, tmp_path):
        from cli.recommendation_signals import build_default_engine
        sessions = tmp_path / "sessions"
        sessions.mkdir()
        engine = build_default_engine(payload={}, sessions_dir=str(sessions))
        signal_names = {s.name for s in engine._signals}
        assert "topology" in signal_names


# ─── GAP-4: credential-aware retry ─────────────────────────────────────────


class TestCredentialAwareRetry:
    def test_retry_with_no_open_ports_returns_empty(self):
        from modules.autonomous_exploit_engine import (
            AutonomousExploitEngine,
        )
        engine = AutonomousExploitEngine()
        engine._results = []
        results = engine.retry_with_credentials("255.255.255.255")
        assert results == []

    def test_credential_aware_rank_boosts_brute_force(self):
        from modules.autonomous_exploit_engine import (
            AutonomousExploitEngine,
            ExploitCandidate,
            TargetProfile,
        )
        engine = AutonomousExploitEngine()
        profile = TargetProfile(
            ip="10.0.0.1",
            open_ports=(22,),
            services=({"port": "22", "name": "ssh", "product": "OpenSSH", "version": "8.9"},),
        )

        baseline = engine.rank_exploits(profile)
        ssh_base = next(
            (c for c in baseline if c.strategy == "brute_force"), None
        )
        assert ssh_base is not None
        base_conf = ssh_base.confidence

        creds = [{"username": "admin", "password": "secret"}]
        boosted = engine._credential_aware_rank(profile, creds)
        ssh_boosted = next(
            (c for c in boosted if c.strategy == "brute_force"), None
        )
        assert ssh_boosted is not None
        assert ssh_boosted.confidence > base_conf
        assert ssh_boosted.confidence == 1.0

    def test_credential_aware_rank_boosts_credential_reuse(self):
        from modules.autonomous_exploit_engine import (
            AutonomousExploitEngine,
            ExploitCandidate,
            TargetProfile,
        )
        engine = AutonomousExploitEngine()
        profile = TargetProfile(
            ip="10.0.0.1",
            open_ports=(5985,),
            services=({"port": "5985", "name": "winrm", "product": "", "version": ""},),
        )
        creds = [{"username": "admin", "password": "pass"}]
        candidates = engine._credential_aware_rank(profile, creds)
        winrm = next((c for c in candidates if "winrm" in c.service), None)
        assert winrm is not None

    def test_credential_aware_rank_handles_empty_creds(self):
        from modules.autonomous_exploit_engine import (
            AutonomousExploitEngine,
            TargetProfile,
        )
        engine = AutonomousExploitEngine()
        profile = TargetProfile(
            ip="10.0.0.1",
            open_ports=(22,),
            services=({"port": "22", "name": "ssh", "product": "OpenSSH", "version": "8.9"},),
        )
        candidates = engine._credential_aware_rank(profile, [])
        assert len(candidates) >= 0


# ─── Integration: full data-flow test ──────────────────────────────────────


class TestFullDataFlow:
    def test_recon_to_world_model_to_recommendation(self, world_model, parser):
        nmap_output = (
            "22/tcp open ssh OpenSSH 8.9p1 Ubuntu-3ubuntu0.6\n"
            "80/tcp open http Apache httpd 2.4.52\n"
            "Contact: admin@victim.corp\n"
        )
        obs = parser.parse(nmap_output, host="10.10.11.78", tool="nmap")

        world_model.update_from_findings(obs.findings)

        host = world_model.get_host("10.10.11.78")
        assert host is not None
        assert 22 in host.services
        assert 80 in host.services
        assert host.services[22].name == "ssh"
        assert host.services[80].name == "http"

        assert len(world_model._emails) >= 1

        assert host.state.rank() >= HostState.SCANNED.rank()
