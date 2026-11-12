"""Tests for the shared chain selector and its cascade master switch.

The chain selector bridges the autonomous loop to the vetted ``chains/``
library. It lives once in :mod:`modules.selection.chain` and is consumed by
both runtimes through :func:`modules.selection.registry.all_selectors`; the
daemon's former private wrapper was subsumed by ``UnifiedBrainSelector``.

The selector itself must:

* only fire in strategic phases and only on a concrete match;
* propose ``apt_chain <name> <target>`` through the routable shell verb;
* honour the declared platform of a chain;
* exclude lab/gym chains unless ``allow_lab`` is set;
* propose a (chain, target) pair at most once via the shared exclude set;
* ignore disabled and invalid chains.

The cascade assembly must honour ``AUTO_CHAIN_SELECTOR`` (default on): when
falsey the chain selector is dropped from the shared cascade for every
runtime. Every scenario states Given, When, Then. The chain registry is
injected by monkeypatching ``scan_all`` so no YAML files are read.
"""

from __future__ import annotations

import sys
from pathlib import Path

_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(_ROOT))

import modules.chain_match as chain_match  # noqa: E402
from modules.selection.base import SelectionContext  # noqa: E402
from modules.selection.chain import ChainSelector  # noqa: E402
from modules.selection.registry import all_selectors  # noqa: E402


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


def _bind_registry(monkeypatch, rows=None) -> None:
    """Inject the registry fixture and force a fresh match cache."""
    monkeypatch.setattr("modules.chain_registry.scan_all", lambda *a, **k: list(_rows() if rows is None else rows))
    chain_match.reset_cache()


def _ctx(target: str, phase: str, services, os_hint: str, exclude=frozenset()) -> SelectionContext:
    """Build a SelectionContext mirroring the loop's live snapshot."""
    return SelectionContext(
        target=target,
        phase=phase,
        os_hint=os_hint,
        services=tuple(services),
        exclude=frozenset(exclude),
    )


def test_non_strategic_phase_returns_none(monkeypatch):
    """Given a recon phase, When selecting, Then no chain is proposed."""
    _bind_registry(monkeypatch)
    sel = ChainSelector(allow_lab=False)
    assert sel.propose(_ctx("10.0.0.9", "recon", ["http"], "linux")) is None


def test_service_match_proposes_apt_chain(monkeypatch):
    """Given a matching http service, When selecting in exploit, Then apt_chain fires."""
    _bind_registry(monkeypatch)
    decision = ChainSelector(allow_lab=False).propose(_ctx("10.0.0.9", "exploit", ["http"], "linux"))
    assert decision is not None
    assert decision.command == "apt_chain apt_web_http 10.0.0.9"
    assert decision.source == "chain"


def test_platform_mismatch_excludes_chain(monkeypatch):
    """Given a linux host, When only a windows chain matches, Then nothing fires."""
    _bind_registry(monkeypatch)
    decision = ChainSelector(allow_lab=False).propose(_ctx("10.0.0.9", "cred", ["ldap"], "linux"))
    assert decision is None


def test_platform_match_for_windows_ad(monkeypatch):
    """Given a windows host, When an AD chain matches, Then it is proposed."""
    _bind_registry(monkeypatch)
    decision = ChainSelector(allow_lab=False).propose(_ctx("10.0.0.9", "cred", ["ldap"], "windows"))
    assert decision is not None
    assert decision.command == "apt_chain apt_ad_coerce 10.0.0.9"


def test_lab_chains_excluded_when_flag_off(monkeypatch):
    """Given allow_lab False, When only a gym chain matches, Then nothing fires."""
    _bind_registry(monkeypatch)
    decision = ChainSelector(allow_lab=False).propose(_ctx("10.0.0.9", "lateral", ["microsoft-ds"], "linux"))
    assert decision is None


def test_lab_chains_allowed_when_flag_set(monkeypatch):
    """Given allow_lab True, When a gym chain matches, Then it is proposed."""
    _bind_registry(monkeypatch)
    decision = ChainSelector(allow_lab=True).propose(_ctx("10.0.0.9", "lateral", ["microsoft-ds"], "linux"))
    assert decision is not None
    assert decision.command == "apt_chain apt_ad_lab 10.0.0.9"


def test_no_match_returns_none(monkeypatch):
    """Given an unknown service, When selecting, Then no chain is proposed."""
    _bind_registry(monkeypatch)
    assert ChainSelector(allow_lab=False).propose(_ctx("10.0.0.9", "exploit", ["gopher"], "linux")) is None


def test_each_pair_proposed_once(monkeypatch):
    """Given a prior proposal in the exclude set, When re-selecting, Then it is not repeated."""
    _bind_registry(monkeypatch)
    sel = ChainSelector(allow_lab=False)
    first = sel.propose(_ctx("10.0.0.9", "exploit", ["http"], "linux"))
    assert first is not None
    again = sel.propose(_ctx("10.0.0.9", "exploit", ["http"], "linux", exclude={first.command}))
    assert again is None


def test_disabled_and_invalid_chains_ignored(monkeypatch):
    """Given only disabled or invalid http chains, When selecting, Then nothing fires."""
    rows = [
        {"name": "apt_disabled", "enabled": False, "valid": True, "tags": ["http"], "platforms": ["linux"]},
        {"name": "apt_invalid", "enabled": True, "valid": False, "tags": ["http"], "platforms": ["linux"]},
    ]
    _bind_registry(monkeypatch, rows=rows)
    assert ChainSelector(allow_lab=False).propose(_ctx("10.0.0.9", "exploit", ["http"], "linux")) is None


def test_master_switch_off_drops_chain_selector(monkeypatch):
    """Given AUTO_CHAIN_SELECTOR off, When the cascade is built, Then no chain selector is present."""
    monkeypatch.setenv("AUTO_CHAIN_SELECTOR", "0")
    assert not any(getattr(sel, "name", "") == "chain" for sel in all_selectors())


def test_master_switch_on_includes_chain_selector(monkeypatch):
    """Given AUTO_CHAIN_SELECTOR on, When the cascade is built, Then the chain selector is present."""
    monkeypatch.setenv("AUTO_CHAIN_SELECTOR", "1")
    assert any(getattr(sel, "name", "") == "chain" for sel in all_selectors())
