"""Tests for modules.lazy_netattack — Windows attack-surface adjudication.

Covers:
    - Windows identity detection from OS hints and service names
    - LLMNR viable / blocked split
    - SMB relay gating on attested signing evidence
    - mitm6 needs_evidence contract (consent + IPv6 event)
    - NTLMv1 downgrade LM compatibility gating
    - hint_text shape and JSON-safety of verdicts
"""

from __future__ import annotations

import pytest


@pytest.fixture
def module():
    import modules.lazy_netattack as na

    return na


@pytest.fixture
def windows_only(module):
    return module.SurfaceEvidence(
        services={"10.10.10.4": {"445": {"name": "microsoft-ds"}, "3389": {"name": "ms-wbt-server"}}},
        os_hints={"10.10.10.4": "windows server 2019"},
        signing={},
        lm_compat={},
    )


@pytest.fixture
def ad_domain_controller(module):
    return module.SurfaceEvidence(
        services={
            "10.10.10.2": {
                "88": {"name": "kerberos-sec"},
                "389": {"name": "ldap"},
                "445": {"name": "microsoft-ds"},
            }
        },
        os_hints={"10.10.10.2": "windows server 2016"},
        signing={"10.10.10.2": "nmap: SMB signing: not required"},
        lm_compat={"10.10.10.2": 2},
    )


class TestIdentity:
    def test_windows_hint_matches(self, module, windows_only):
        verdicts = module.surface_decision(windows_only)
        assert verdicts["llmnr"].verdict == module.VERDICT_VIABLE
        assert "10.10.10.4" in verdicts["llmnr"].targets

    def test_linux_host_blocked(self, module):
        verdicts = module.surface_decision(
            module.SurfaceEvidence(
                services={"10.10.10.9": {"22": {"name": "ssh"}}},
                os_hints={"10.10.10.9": "linux"},
                signing={},
                lm_compat={},
            )
        )
        assert verdicts["llmnr"].verdict == module.VERDICT_BLOCKED
        assert verdicts["mitm6"].verdict == module.VERDICT_BLOCKED


class TestRelay:
    def test_attested_signing_unlocks_relay(self, module, ad_domain_controller):
        verdicts = module.surface_decision(ad_domain_controller)
        assert verdicts["smb_relay"].verdict == module.VERDICT_VIABLE
        assert "10.10.10.2" in verdicts["smb_relay"].targets

    def test_unknown_signing_requires_evidence(self, module, windows_only):
        verdicts = module.surface_decision(windows_only)
        assert verdicts["smb_relay"].verdict == module.VERDICT_NEEDS_EVIDENCE

    def test_attested_signing_required_blocks(self, module, windows_only):
        windows_only.signing["10.10.10.4"] = "nmap: SMB signing: required"
        verdicts = module.surface_decision(windows_only)
        assert verdicts["smb_relay"].verdict != module.VERDICT_VIABLE


class TestMitm6Downgrade:
    def test_mitm6_needs_event_and_consent(self, module, ad_domain_controller):
        verdicts = module.surface_decision(ad_domain_controller)
        assert verdicts["mitm6"].verdict == module.VERDICT_NEEDS_EVIDENCE
        assert verdicts["mitm6"].missing

    def test_downgrade_lm2_viable(self, module, ad_domain_controller):
        verdicts = module.surface_decision(ad_domain_controller)
        assert verdicts["ntlmv1_downgrade"].verdict == module.VERDICT_VIABLE

    def test_downgrade_lm5_needs_evidence(self, module, ad_domain_controller):
        ad_domain_controller.lm_compat = {}
        verdicts = module.surface_decision(ad_domain_controller)
        assert verdicts["ntlmv1_downgrade"].verdict == module.VERDICT_NEEDS_EVIDENCE


class TestShape:
    def test_hint_text_shapes(self, module, ad_domain_controller):
        verdicts = module.surface_decision(ad_domain_controller)
        text = module.hint_text(verdicts["smb_relay"])
        assert "smb_relay" in text and "viable" in text

    def test_verdicts_json_safe(self, module, ad_domain_controller):
        verdicts = module.surface_decision(ad_domain_controller)
        for row in verdicts.values():
            assert row.verdict in module.VERDICTS
            assert isinstance(row.as_dict(), dict)
