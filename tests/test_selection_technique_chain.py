"""Tests for TechniqueChainSelector and the focused technique-chain synth.

The selector compiles two or more MITRE/Atomic techniques (goal-named or
phase-ranked) into one ordered apt_chain so the ChainRunner's EdrPacer
can pace the configured jitter and sleeper windows between techniques.
"""

from __future__ import annotations

import pytest

from modules import chain_registry, chain_synth
from modules.chain_synth import synth_technique_chain_data
from modules.selection.base import SelectionContext
from modules.selection.technique_chain import TechniqueChainSelector


def _ctx(phase="exploit", os_hint="linux", target="10.66.44.7", exclude=(), extra=None):
    return SelectionContext(
        target=target,
        phase=phase,
        os_hint=os_hint,
        exclude=frozenset(exclude),
        extra=extra or {},
    )


@pytest.fixture()
def synth_sandbox(monkeypatch):
    """Capture chain writes instead of touching the real chains dir."""
    writes: list[dict] = []

    def _fake_write(data, chains_dir=None):
        writes.append(data)
        return ("chains/%s.yaml" % data.get("name", "x"), [])

    monkeypatch.setattr(chain_synth, "write_generated_chain", _fake_write)
    monkeypatch.setattr(chain_registry, "get", lambda name: None)
    return writes


class TestSynthTechniqueChain:
    def test_builds_ordered_atomic_tests_steps(self):
        data, used = synth_technique_chain_data("10.0.0.5", ["T1059.001", "t1003", "T1082"])
        assert used == ["T1059.001", "T1003", "T1082"]
        runs = [step["run"] for step in data["steps"]]
        assert runs[0] == "assign target 10.0.0.5"
        assert runs[1:] == [
            "atomic_tests T1059.001 --non-interactive",
            "atomic_tests T1003 --non-interactive",
            "atomic_tests T1082 --non-interactive",
        ]

    def test_drops_malformed_ids_and_dedupes(self):
        data, used = synth_technique_chain_data("10.0.0.5", ["T1059", "bad", "T1059", "T1003"])
        assert used == ["T1059", "T1003"]
        assert len(data["steps"]) == 3

    def test_under_two_techniques_is_empty(self):
        data, used = synth_technique_chain_data("10.0.0.5", ["T1059"])
        assert data == {}

    def test_validates_against_registry(self):
        data, _used = synth_technique_chain_data("10.0.0.5", ["T1059", "T1003"])
        assert chain_registry.validate_chain(data, filename=data["name"]) == []


class TestTechniqueChainSelector:
    def test_phase_techniques_compile_into_one_chain(self, synth_sandbox, monkeypatch):
        monkeypatch.setattr(
            "modules.playbook_engine.phase_techniques",
            lambda *a, **k: [
                {"technique_id": "T1046", "name": "network scan"},
                {"technique_id": "T1210", "name": "remote services"},
                {"technique_id": "T1021", "name": "remote services"},
            ],
        )
        decision = TechniqueChainSelector().propose(_ctx())
        assert decision is not None
        assert decision.source == "technique_chain"
        assert decision.command.startswith("apt_chain techchain_")
        assert decision.command.endswith(" 10.66.44.7")
        assert decision.mitre == "T1046"
        assert synth_sandbox and len(synth_sandbox[0]["steps"]) == 4

    def test_goal_named_ids_win_verbatim(self, synth_sandbox, monkeypatch):
        monkeypatch.setattr("modules.playbook_engine.phase_techniques", lambda *a, **k: [])
        decision = TechniqueChainSelector().propose(
            _ctx(extra={"goal": "emulate T1059.003 then T1486 ransomware"})
        )
        assert decision is not None
        used = synth_sandbox[0]
        runs = [s["run"] for s in used["steps"]]
        assert "atomic_tests T1059.003 --non-interactive" in runs
        assert "atomic_tests T1486 --non-interactive" in runs

    def test_recon_phase_abstains(self, synth_sandbox):
        assert TechniqueChainSelector().propose(_ctx(phase="recon")) is None

    def test_single_technique_abstains(self, synth_sandbox, monkeypatch):
        monkeypatch.setattr(
            "modules.playbook_engine.phase_techniques",
            lambda *a, **k: [{"technique_id": "T1046", "name": "only one"}],
        )
        assert TechniqueChainSelector().propose(_ctx()) is None

    def test_requires_target(self, synth_sandbox):
        ctx = SelectionContext(target="", phase="exploit", extra={})
        assert TechniqueChainSelector().propose(ctx) is None

    def test_excluded_command_is_not_reproposed(self, synth_sandbox, monkeypatch):
        monkeypatch.setattr(
            "modules.playbook_engine.phase_techniques",
            lambda *a, **k: [
                {"technique_id": "T1046", "name": "a"},
                {"technique_id": "T1210", "name": "b"},
            ],
        )
        first = TechniqueChainSelector().propose(_ctx())
        assert first is not None
        again = TechniqueChainSelector().propose(_ctx(exclude={first.command}))
        assert again is None

    def test_already_registered_chain_is_not_rewritten(self, monkeypatch):
        monkeypatch.setattr(
            "modules.playbook_engine.phase_techniques",
            lambda *a, **k: [
                {"technique_id": "T1046", "name": "a"},
                {"technique_id": "T1210", "name": "b"},
            ],
        )
        monkeypatch.setattr(chain_registry, "get", lambda name: object())
        writes: list = []
        monkeypatch.setattr(
            chain_synth, "write_generated_chain", lambda d, c=None: writes.append(d) or (None, [])
        )
        decision = TechniqueChainSelector().propose(_ctx())
        assert decision is not None
        assert writes == []
