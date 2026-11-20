"""Tests for the technique-planner to intent-frontier bridge."""

from __future__ import annotations

from types import SimpleNamespace

import modules.loop.planner_bridge as bridge


def test_technique_candidate_summary_with_command():
    candidate = SimpleNamespace(technique_id="T1046", name="Network Scan", command="nmap -sV target")
    assert bridge.technique_candidate_summary(candidate) == "technique step: Network Scan (T1046) -> nmap -sV target"


def test_technique_candidate_summary_without_command():
    candidate = SimpleNamespace(technique_id="", name="Bare", command="")
    assert bridge.technique_candidate_summary(candidate) == "technique step: Bare"


def test_technique_intents_converts_candidates(monkeypatch):
    plan = SimpleNamespace(
        candidates=[
            SimpleNamespace(technique_id="T1046", name="Scan", command="nmap -sV t"),
            SimpleNamespace(technique_id="T1110", name="Brute", command="hydra"),
        ]
    )

    class FakePlanner:
        def plan(self, target, max_candidates=10):
            return plan

    monkeypatch.setattr("modules.planner.get_planner", lambda: FakePlanner())
    summaries = bridge.technique_intents("10.0.0.1")
    assert len(summaries) == 2
    assert all(s.startswith("technique step:") for s in summaries)


def test_technique_intents_never_raises(monkeypatch):
    def boom():
        raise RuntimeError("planner down")

    monkeypatch.setattr("modules.planner.get_planner", boom)
    assert bridge.technique_intents("10.0.0.1") == []


def test_bridge_dedupes_existing(monkeypatch):
    candidate = SimpleNamespace(technique_id="T1046", name="Scan", command="nmap -sV t")
    plan = SimpleNamespace(candidates=[candidate])
    monkeypatch.setattr(
        bridge,
        "technique_intents",
        lambda target, max_candidates=4: [bridge.technique_candidate_summary(candidate)],
    )
    out = bridge.bridge_candidates_for_task("10.0.0.1", existing={bridge.technique_candidate_summary(candidate)})
    assert out == []
    fresh = bridge.bridge_candidates_for_task("10.0.0.1", existing=set())
    assert len(fresh) == 1
    assert fresh[0][2] == bridge.BRIDGE_PRIORITY


def test_bridge_disabled(monkeypatch):
    monkeypatch.setattr(bridge, "planner_bridge_enabled", lambda: False)
    assert bridge.bridge_candidates_for_task("10.0.0.1", existing=set()) == []
