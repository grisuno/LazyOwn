"""Tests for ``ChainSelector`` in ``skills/autonomous_daemon.py``.

The selector bridges the autonomous loop to the vetted ``chains/`` library:

* it only fires in strategic phases and only on a concrete match;
* it proposes ``apt_chain <name> <target>`` through the routable shell verb;
* it honours the declared platform of a chain;
* it excludes lab/gym chains unless explicitly allowed;
* it proposes each (chain, target) pair at most once;
* it is inert (returns ``None``) when the master switch is off, so the
  cascade falls through to the other selectors with no side effect.

Every scenario states Given, When, Then. The chain registry is injected by
monkeypatching ``scan_all`` so no YAML files are read.
"""

from __future__ import annotations

import sys
from pathlib import Path

_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(_ROOT))
sys.path.insert(0, str(_ROOT / "skills"))

import skills.autonomous_daemon as auto  # noqa: E402
from skills.autonomous_daemon import ChainSelector  # noqa: E402


def _rows() -> list[dict]:
    """Return a small registry fixture covering the match dimensions."""
    return [
        {"name": "apt_web_http", "enabled": True, "valid": True, "tags": ["web", "http"], "platforms": ["linux"]},
        {"name": "apt_ad_coerce", "enabled": True, "valid": True, "tags": ["ad", "credentials"], "platforms": ["windows"]},
        {"name": "apt_ad_lab", "enabled": True, "valid": True, "tags": ["ad-lab", "samba", "gym"], "platforms": ["linux"]},
        {"name": "apt_disabled", "enabled": False, "valid": True, "tags": ["http"], "platforms": ["linux"]},
        {"name": "apt_invalid", "enabled": True, "valid": False, "tags": ["http"], "platforms": ["linux"]},
        {"name": "apt_untagged", "enabled": True, "valid": True, "tags": [], "platforms": []},
    ]


def _selector(monkeypatch, rows=None) -> ChainSelector:
    """Build a ChainSelector with an injected registry and defaults forced on."""
    import modules.chain_match as chain_match

    monkeypatch.setattr("modules.chain_registry.scan_all", lambda *a, **k: list(_rows() if rows is None else rows))
    monkeypatch.setattr(auto, "CHAIN_SELECTOR_ENABLED", True, raising=False)
    monkeypatch.setattr(auto, "CHAIN_SELECTOR_ALLOW_LAB", False, raising=False)
    monkeypatch.setattr(auto, "CHAIN_SELECTOR_TTL_S", 0.0, raising=False)
    chain_match.reset_cache()
    return ChainSelector()


def test_non_strategic_phase_returns_none(monkeypatch):
    """Given a recon phase, When selecting, Then no chain is proposed."""
    sel = _selector(monkeypatch)
    assert sel.select("10.0.0.9", "recon", {"services": ["http"], "os_hint": "linux"}) is None


def test_service_match_proposes_apt_chain(monkeypatch):
    """Given an http service on linux, When in exploit phase, Then the web chain runs."""
    sel = _selector(monkeypatch)
    decision = sel.select("10.0.0.9", "exploit", {"services": ["http"], "os_hint": "linux"})
    assert decision is not None
    assert decision.command == "apt_chain apt_web_http 10.0.0.9"
    assert decision.source == "chain"
    assert decision.priority == 3
    assert "http" in decision.reason


def test_platform_mismatch_excludes_chain(monkeypatch):
    """Given a windows-only chain, When the target is linux, Then it is not proposed."""
    sel = _selector(monkeypatch)
    decision = sel.select("10.0.0.9", "cred", {"services": ["ldap"], "os_hint": "linux"})
    assert decision is None


def test_platform_match_for_windows_ad(monkeypatch):
    """Given an ldap service on windows, When in cred phase, Then the AD chain runs."""
    sel = _selector(monkeypatch)
    decision = sel.select("10.0.0.9", "cred", {"services": ["ldap"], "os_hint": "windows"})
    assert decision is not None
    assert decision.command == "apt_chain apt_ad_coerce 10.0.0.9"


def test_lab_chains_excluded_when_flag_off(monkeypatch):
    """Given a samba service, When lab chains are disallowed, Then the gym chain is skipped."""
    sel = _selector(monkeypatch)
    decision = sel.select("10.0.0.9", "lateral", {"services": ["microsoft-ds"], "os_hint": "linux"})
    assert decision is None


def test_lab_chains_allowed_when_flag_set(monkeypatch):
    """Given the lab flag, When a samba service is seen, Then the gym chain is proposed."""
    import modules.chain_match as chain_match

    sel = _selector(monkeypatch)
    monkeypatch.setattr(auto, "CHAIN_SELECTOR_ALLOW_LAB", True, raising=False)
    chain_match.reset_cache()
    decision = sel.select("10.0.0.9", "lateral", {"services": ["microsoft-ds"], "os_hint": "linux"})
    assert decision is not None
    assert decision.command == "apt_chain apt_ad_lab 10.0.0.9"


def test_no_match_returns_none(monkeypatch):
    """Given an unrelated service, When nothing scores, Then the cascade falls through."""
    sel = _selector(monkeypatch)
    assert sel.select("10.0.0.9", "exploit", {"services": ["gopher"], "os_hint": "linux"}) is None


def test_each_pair_proposed_once(monkeypatch):
    """Given one match, When selecting twice, Then the same chain is not re-proposed."""
    sel = _selector(monkeypatch)
    ctx = {"services": ["http"], "os_hint": "linux"}
    first = sel.select("10.0.0.9", "exploit", ctx)
    second = sel.select("10.0.0.9", "exploit", ctx)
    assert first is not None
    assert second is None


def test_master_switch_off_is_inert(monkeypatch):
    """Given the switch off, When selecting a clear match, Then nothing is proposed."""
    sel = _selector(monkeypatch)
    monkeypatch.setattr(auto, "CHAIN_SELECTOR_ENABLED", False, raising=False)
    assert sel.select("10.0.0.9", "exploit", {"services": ["http"], "os_hint": "linux"}) is None


def test_disabled_and_invalid_chains_ignored(monkeypatch):
    """Given disabled/invalid http chains, When selecting, Then only the valid one is used."""
    rows = [
        {"name": "apt_disabled", "enabled": False, "valid": True, "tags": ["http"], "platforms": ["linux"]},
        {"name": "apt_invalid", "enabled": True, "valid": False, "tags": ["http"], "platforms": ["linux"]},
    ]
    sel = _selector(monkeypatch, rows=rows)
    assert sel.select("10.0.0.9", "exploit", {"services": ["http"], "os_hint": "linux"}) is None
