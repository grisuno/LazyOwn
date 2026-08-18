"""Tests for new reactive engine matchers."""
from __future__ import annotations

from modules.reactive_engine import (
    DataOfInterestMatcher,
    LateralOpportunityMatcher,
    ReactiveEngine,
)


class TestLateralOpportunityMatcher:
    def test_kerberos_ticket(self):
        m = LateralOpportunityMatcher()
        signals = m.match("Found kerberos ticket for krbtgt", {})
        assert len(signals) >= 1
        assert any(s.value == "kerberos_ticket" for s in signals)

    def test_rdp_session(self):
        m = LateralOpportunityMatcher()
        signals = m.match("RDP session active on target", {})
        assert any(s.value == "rdp_session" for s in signals)

    def test_smb_admin_share(self):
        m = LateralOpportunityMatcher()
        signals = m.match("\\\\server\\admin$ share accessible", {})
        assert any(s.value == "smb_admin_share" for s in signals)

    def test_winrm_access(self):
        m = LateralOpportunityMatcher()
        signals = m.match("winrm service detected", {})
        assert any(s.value == "winrm_access" for s in signals)

    def test_ssh_key(self):
        m = LateralOpportunityMatcher()
        signals = m.match("ssh key found in authorized_keys", {})
        assert any(s.value == "ssh_key" for s in signals)

    def test_wmi_access(self):
        m = LateralOpportunityMatcher()
        signals = m.match("wmi enabled on remote host", {})
        assert any(s.value == "wmi_access" for s in signals)

    def test_domain_admin(self):
        m = LateralOpportunityMatcher()
        signals = m.match("domain admin group found", {})
        assert any(s.value == "domain_admin" for s in signals)

    def test_no_match(self):
        m = LateralOpportunityMatcher()
        signals = m.match("no lateral opportunities here", {})
        assert len(signals) == 0

    def test_confidence(self):
        m = LateralOpportunityMatcher()
        signals = m.match("kerberos ticket found", {})
        for s in signals:
            assert s.confidence == 0.75


class TestDataOfInterestMatcher:
    def test_pii_email(self):
        m = DataOfInterestMatcher()
        signals = m.match("Contact: user@example.com", {})
        assert any("pii:" in s.value for s in signals)

    def test_pii_ssn(self):
        m = DataOfInterestMatcher()
        signals = m.match("SSN: 123-45-6789", {})
        assert any("pii:" in s.value for s in signals)

    def test_pii_credit_card(self):
        m = DataOfInterestMatcher()
        signals = m.match("Card: 4111111111111111", {})
        assert any("pii:" in s.value for s in signals)

    def test_secret_api_key(self):
        m = DataOfInterestMatcher()
        signals = m.match("api_key=AKIAIOSFODNN7EXAMPLE", {})
        assert any("secret:" in s.value for s in signals)

    def test_secret_aws_key(self):
        m = DataOfInterestMatcher()
        signals = m.match("aws_secret_access_key=wJalrXUtnFEMI/K7MDENG", {})
        assert any("secret:" in s.value for s in signals)

    def test_secret_private_key(self):
        m = DataOfInterestMatcher()
        signals = m.match("-----BEGIN RSA PRIVATE KEY-----", {})
        assert any("secret:" in s.value for s in signals)

    def test_file_pattern_env(self):
        m = DataOfInterestMatcher()
        signals = m.match("Found .env file with secrets", {})
        assert any("file:" in s.value for s in signals)

    def test_file_pattern_config(self):
        m = DataOfInterestMatcher()
        signals = m.match("config.json contains credentials", {})
        assert any("file:" in s.value for s in signals)

    def test_no_match(self):
        m = DataOfInterestMatcher()
        signals = m.match("no interesting data here", {})
        assert len(signals) == 0

    def test_confidence_levels(self):
        m = DataOfInterestMatcher()
        signals = m.match("api_key=secret123 user@test.com .env", {})
        for s in signals:
            if "secret:" in s.value:
                assert s.confidence == 0.90
            elif "pii:" in s.value:
                assert s.confidence == 0.85
            elif "file:" in s.value:
                assert s.confidence == 0.70


class TestReactiveEngineIntegration:
    def _make_engine(self, matchers):
        """Create a ReactiveEngine with mocked advisors to avoid ChromaDB loading."""
        from unittest.mock import MagicMock
        return ReactiveEngine(
            matchers=matchers,
            evasion=MagicMock(),
            privesc=MagicMock(),
            parquet=MagicMock(),
            semantic=MagicMock(),
        )

    def test_lateral_signals_produce_decisions(self):
        engine = self._make_engine([LateralOpportunityMatcher()])
        engine._evasion.suggest.return_value = []
        engine._privesc.suggest.return_value = []
        engine._semantic.suggest.return_value = []
        output = "Found kerberos ticket and RDP session"
        decisions = engine.analyse(output, "test", "linux", {"known_hosts": []})
        lateral_decisions = [
            d for d in decisions
            if any(s.kind == "lateral_opportunity" for s in d.signals)
        ]
        assert len(lateral_decisions) >= 1
        for d in lateral_decisions:
            assert d.action == "run_command"
            assert d.mitre_tactic == "T1570"
            assert d.priority == 2

    def test_data_signals_produce_decisions(self):
        engine = self._make_engine([DataOfInterestMatcher()])
        engine._evasion.suggest.return_value = []
        engine._privesc.suggest.return_value = []
        engine._semantic.suggest.return_value = []
        output = "Found api_key=secret123 user@test.com"
        decisions = engine.analyse(output, "test", "linux", {"known_hosts": []})
        data_decisions = [
            d for d in decisions
            if any(s.kind == "data_of_interest" for s in d.signals)
        ]
        assert len(data_decisions) >= 1
        for d in data_decisions:
            assert d.action == "run_command"
            assert d.command == "exfil"
            assert d.mitre_tactic == "T1030"
            assert d.priority == 1

    def test_decisions_sorted_by_priority(self):
        engine = self._make_engine([LateralOpportunityMatcher(), DataOfInterestMatcher()])
        engine._evasion.suggest.return_value = []
        engine._privesc.suggest.return_value = []
        engine._semantic.suggest.return_value = []
        output = "api_key=secret123 kerberos ticket"
        decisions = engine.analyse(output, "test", "linux", {"known_hosts": []})
        priorities = [d.priority for d in decisions]
        assert priorities == sorted(priorities)
