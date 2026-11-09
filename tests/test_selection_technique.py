"""Tests for the TechniqueSelector and its playbook_engine helper.

The selector must turn the canonical loop phase into a routable
``atomic_tests`` staging line via the STIX-first fallback helper.
Unit tests stub the STIX loader (the real MemoryStore load is far too
slow for unit scope); the STIX query itself is covered by the engine.
"""

from __future__ import annotations

import pytest

import modules.playbook_engine as pe
from modules.selection.base import SelectionContext
from modules.selection.technique import TechniqueSelector


class _FakeStore:
    def __init__(self, techniques):
        self._techniques = techniques

    def query(self, filters):
        return self._techniques


class _FakeStix:
    def __init__(self, techniques, available=True):
        self._store = _FakeStore(techniques)
        self._available = available

    def available(self):
        return self._available

    def store(self):
        return self._store

    def techniques_for_tactics(self, tactics, platform=None):
        out = []
        for t in self._store.query([]):
            phases = [p.get("phase_name", "") for p in t.get("kill_chain_phases", [])]
            if not any(phase in tactics for phase in phases):
                continue
            if platform and platform not in [p.lower() for p in t.get("x_mitre_platforms", [])]:
                continue
            tid = t.get("external_id", "")
            out.append({"technique_id": tid, "name": t.get("name", "")})
        return out


_STIX_TECHNIQUES = [
    {
        "external_id": "T1059",
        "name": "Command and Scripting Interpreter",
        "kill_chain_phases": [{"phase_name": "execution"}],
        "x_mitre_platforms": ["linux", "windows"],
    },
    {
        "external_id": "T1003",
        "name": "OS Credential Dumping",
        "kill_chain_phases": [{"phase_name": "credential-access"}],
        "x_mitre_platforms": ["linux", "windows"],
    },
]


@pytest.fixture
def fake_stix(monkeypatch):
    """Install a fast fake STIX loader on the engine singleton."""
    engine = pe.get_engine()
    fake = _FakeStix(_STIX_TECHNIQUES)
    monkeypatch.setattr(engine, "_stix", fake)
    return fake


def _ctx(phase: str = "postexp", os_hint: str = "linux", target: str = "10.66.44.7", exclude=()):
    return SelectionContext(
        target=target, phase=phase, os_hint=os_hint, exclude=frozenset(exclude), extra={}
    )


class TestPhaseTechniques:
    def test_stix_phase_scoped(self, fake_stix):
        story = "a STIX-backed phase returns technique dicts with ids"
        out = pe.phase_techniques("exploit", "linux", top_n=5)
        ids = [t["technique_id"] for t in out]
        assert ids == ["T1059"], story

    def test_unknown_phase_empty(self, fake_stix):
        story = "an unknown phase yields no techniques"
        assert pe.phase_techniques("warp", "linux", top_n=5) == [], story

    def test_top_n_cap(self, fake_stix, monkeypatch, tmp_path):
        story = "top_n bounds the result list"
        monkeypatch.setattr(
            pe, "_ENTERPRISE_ATTACK_JSON", tmp_path / "missing.json", raising=False
        )
        engine = pe.get_engine()
        monkeypatch.setattr(
            engine, "_stix", pe._StixLoader(tmp_path / "missing.json"), raising=False
        )
        out = pe.phase_techniques("postexp", "", top_n=3)
        assert 0 < len(out) <= 3, story

    def test_atomic_fallback_when_stix_missing(self, monkeypatch, tmp_path):
        story = "without the STIX bundle the atomic index still feeds candidates"
        engine = pe.get_engine()
        monkeypatch.setattr(
            engine, "_stix", pe._StixLoader(tmp_path / "missing.json"), raising=False
        )
        out = pe.phase_techniques("exploit", "linux", top_n=4)
        assert out and all(t.get("technique_id", "").startswith("T") for t in out), story


class TestTechniqueSelector:
    def test_postexp_phase_proposes_atomic_tests(self, fake_stix):
        story = "a post-foothold phase proposes a routable atomic_tests line"
        decision = TechniqueSelector().propose(_ctx())
        assert decision is not None and decision.source == "technique", story
        assert decision.command.startswith("atomic_tests T"), story
        assert decision.command.endswith(" --non-interactive"), story

    def test_recon_phase_abstains(self, fake_stix):
        story = "pre-foothold phases never propose technique emulation"
        assert TechniqueSelector().propose(_ctx(phase="recon")) is None, story

    def test_requires_target(self):
        story = "no target means no proposal"
        ctx = SelectionContext(target="", phase="postexp", extra={})
        assert TechniqueSelector().propose(ctx) is None, story

    def test_exclude_skips_to_next_technique(self, fake_stix, monkeypatch):
        story = "an excluded command falls through to the next candidate"
        monkeypatch.setattr(
            pe,
            "phase_techniques",
            lambda *a, **k: [
                {"technique_id": "T1003", "name": "first"},
                {"technique_id": "T1005", "name": "second"},
            ],
        )
        decision = TechniqueSelector().propose(
            _ctx(exclude={"atomic_tests T1003 --non-interactive"})
        )
        assert decision is not None and "T1005" in decision.command, story

    def test_routable_through_loop(self, fake_stix):
        story = "the emitted command survives the real loop routing gate"
        from modules.auto_registry import is_routable_command

        decision = TechniqueSelector().propose(_ctx())
        assert decision is not None, story
        assert is_routable_command(decision.command), story
