"""Fact-gated todolist contract + planner wiring (lever #6).

The pure contract partitions todolist items by whether their prerequisite facts
exist; the planner uses it to hold back foothold-dependent intents (lateral,
privesc, exfil) until a foothold is proven, so the campaign advances in
evidence order. The dual graph it rides on (global AssetGraph + per-task
exploration graph joined by anchors) already exists; this adds the gate.
"""

from __future__ import annotations

import modules.fact_gated_todolist as todolist
import modules.lazy_loop as loop


def _sandbox(tmp_path, monkeypatch):
    """Redirect loop persistence into a scratch directory."""
    monkeypatch.setattr(loop, "STORE_DIR", tmp_path)
    monkeypatch.setattr(loop, "SESSIONS_DIR", tmp_path, raising=False)
    monkeypatch.setattr(loop, "_store_path", lambda name: tmp_path / name)


def test_unmet_requirements_substring_and_case():
    """A predicate is met by any fact containing it, case-insensitively."""
    facts = ["Foothold shell on 172.17.0.2", "ssh creds for admin"]
    assert todolist.unmet_requirements(["foothold"], facts) == []
    assert todolist.unmet_requirements(["CREDS"], facts) == []
    assert todolist.unmet_requirements(["domain admin"], facts) == ["domain admin"]
    assert todolist.unmet_requirements(["", "  "], facts) == []


def test_gate_partitions_ready_and_blocked():
    """Items with met requirements are ready; others are blocked with reasons."""
    items = [
        {"id": "recon", "requires": []},
        {"id": "lateral", "requires": ["foothold"]},
        {"id": "exfil", "requires": ["foothold", "loot"]},
    ]
    result = todolist.gate(items, ["foothold obtained"])
    ready_ids = [item["id"] for item in result["ready"]]
    assert ready_ids == ["recon", "lateral"]
    assert len(result["blocked"]) == 1
    assert result["blocked"][0]["item"]["id"] == "exfil"
    assert result["blocked"][0]["missing"] == ["loot"]


def _planner(tmp_path, monkeypatch):
    """Build a planner over a sandboxed graph with a scoped goal."""
    _sandbox(tmp_path, monkeypatch)
    graph = loop.ExplorationGraph("tg")
    graph.add_node("goal", "gain initial access on 172.17.0.2", state="pending")
    planner = loop.Planner.__new__(loop.Planner)
    planner.task_id = "tg"
    planner.graph = graph
    planner.activity = loop.ActivityLog("tg")
    planner.store = None
    return planner, graph


def test_planner_defers_lateral_without_foothold(tmp_path, monkeypatch):
    """A lateral candidate is held back while no foothold fact exists."""
    planner, _graph = _planner(tmp_path, monkeypatch)
    candidates = [
        ("enumerate services on 172.17.0.2", [], [], 5),
        ("gain initial access on 172.17.0.2", [], [], 10),
        ("lateral movement to 10.0.0.5", [], [], 3),
    ]
    kept = planner._fact_gate_candidates(candidates)
    summaries = [candidate[0] for candidate in kept]
    assert "lateral movement to 10.0.0.5" not in summaries
    assert "gain initial access on 172.17.0.2" in summaries
    assert "enumerate services on 172.17.0.2" in summaries


def test_planner_releases_lateral_after_foothold(tmp_path, monkeypatch):
    """Once a foothold is confirmed, the lateral candidate is cleared."""
    planner, graph = _planner(tmp_path, monkeypatch)
    graph.add_node(
        "finding",
        "Foothold shell obtained on 172.17.0.2 via auto_pwn",
        state="confirmed",
        meta={"verdict": "reproduced"},
    )
    candidates = [("lateral movement to 10.0.0.5", [], [], 3)]
    kept = planner._fact_gate_candidates(candidates)
    assert [candidate[0] for candidate in kept] == ["lateral movement to 10.0.0.5"]


def test_fact_gate_flag_default_on():
    """The gate ships enabled so the todolist advances in evidence order."""
    assert loop._loop_fact_gate() is True


def test_fact_gate_is_fail_open(tmp_path, monkeypatch):
    """A gate fault returns the candidates untouched, never stalling planning."""
    _sandbox(tmp_path, monkeypatch)
    planner = loop.Planner.__new__(loop.Planner)
    planner.task_id = "tg"
    planner.graph = None
    planner.activity = loop.ActivityLog("tg")
    planner.store = None
    candidates = [("lateral movement to 10.0.0.5", [], [], 3)]
    assert planner._fact_gate_candidates(candidates) == candidates
