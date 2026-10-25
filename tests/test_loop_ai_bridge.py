"""Loop AI-stack bridge: event bus, oracle, MoE/RL and SWAN wiring.

The bridge is exercised with stubbed dependencies so no expert, trainer
or oracle file is touched; every stage is enabled explicitly per test.
"""

from __future__ import annotations

from types import SimpleNamespace

import pytest


@pytest.fixture()
def store(tmp_path, monkeypatch):
    """Sandbox the lazy store for every test in this module."""
    import modules.lazy_loop as loop

    monkeypatch.setattr(loop, "STORE_DIR", tmp_path)
    monkeypatch.setattr(loop, "_store_path", lambda name: tmp_path / name)
    return tmp_path


@pytest.fixture()
def bridge(monkeypatch):
    """Bridge with every stage enabled and singletons reset."""
    import modules.loop_ai_bridge as module

    monkeypatch.setattr(module, "_stage", lambda name, default=True: True)
    monkeypatch.setattr(module, "_SINGLETONS", {})
    return module


def test_publish_loop_event_skips_stream_kinds(bridge, monkeypatch):
    """Stream noise never reaches the bus; meaningful kinds are categorized."""
    captured: list = []

    class _Bus:
        def publish(self, event) -> None:
            captured.append(event)

    import modules.event_bus as bus_module

    monkeypatch.setattr(bus_module, "get_event_bus", lambda: _Bus())
    bridge.publish_loop_event("t1", "worker-1", "tool", "[allow] nmap")
    bridge.publish_loop_event("t1", "reporter", "finding", "SQLi found")
    assert len(captured) == 1
    assert captured[0].event_type == "loop:finding"
    assert captured[0].payload["task_id"] == "t1"


def test_activity_log_publishes_to_bridge(store, bridge, monkeypatch):
    """Every activity line reaches the bridge (which gates and maps it)."""
    calls: list = []
    monkeypatch.setattr(bridge, "publish_loop_event", lambda task, worker, kind, text: calls.append((kind, worker)))
    from modules.lazy_loop import ActivityLog

    ActivityLog("t1").emit("worker-1", "finish", "intent #1 -> done")
    assert calls == [("finish", "worker-1")]


def test_annotate_detection_uses_oracle(bridge, monkeypatch):
    class _Oracle:
        def assess(self, tool, command, category):
            return SimpleNamespace(probability=0.42, sigma_names=["sigma-a"], recommendation="safe")

    import modules.detection_oracle as oracle_module

    monkeypatch.setattr(oracle_module, "get_oracle", lambda: _Oracle())
    out = bridge.annotate_detection("nmap -sV 127.0.0.1")
    assert out == {"probability": 0.42, "sigma_names": ["sigma-a"], "recommendation": "safe"}


def test_worker_annotates_detection_and_records_outcome(store, bridge, monkeypatch):
    """Guard steps carry oracle risk and feed MoE/RL with the outcome."""
    import modules.lazy_loop as loop
    from modules.lazy_engine import LazyEngine

    monkeypatch.setattr(
        bridge,
        "annotate_detection",
        lambda command, action_category="execution": {"probability": 0.42, "sigma_names": ["s"], "recommendation": ""},
    )
    recorded: list = []
    monkeypatch.setattr(bridge, "record_step", lambda *args, **kwargs: recorded.append(args))
    engine = LazyEngine()
    task_id = engine.create_task("gain initial access on 127.0.0.1")["task_id"]
    graph = loop.ExplorationGraph(task_id)
    intent = graph.add_node("intent", "baseline recon: enumerate 127.0.0.1")
    worker = loop.Worker(
        "worker-1",
        task_id,
        engine.assets,
        graph,
        loop.ActivityLog(task_id),
        loop.TrafficLog(task_id),
        loop.Guard(task_id),
        engine.store,
    )
    worker.execute(intent, executor=lambda command: "22/tcp open ssh")
    kinds = [record.get("kind") for record in loop.ActivityLog(task_id).read(300)]
    assert "detection" in kinds
    records = loop.TrafficLog(task_id).read(50)
    assert records and records[-1]["meta"]["detection_prob"] == 0.42
    assert recorded


def test_llm_pool_prefers_moe_expert_and_records_outcome(store, bridge, monkeypatch):
    """The router's expert runs first and its outcome is fed back."""
    import modules.lazy_loop as loop
    import modules.llm_factory as factory

    monkeypatch.setattr(bridge, "moe_route", lambda task_type, goal="": SimpleNamespace(expert_id="b", model="m-b"))
    monkeypatch.setattr(bridge, "rl_select", lambda *args, **kwargs: "b")
    outcomes: list = []
    monkeypatch.setattr(bridge, "moe_record_outcome", lambda *args, **kwargs: outcomes.append(args))
    monkeypatch.setattr(bridge, "rl_update", lambda *args, **kwargs: None)
    calls: list = []

    def _complete(model, prompt, max_tokens=800):
        calls.append(model)
        return "ok"

    monkeypatch.setattr(factory, "complete", _complete)
    pool = loop.LlmPool()
    pool._health = None
    members = [{"name": "a", "model": "groq:m-a", "priority": 5}, {"name": "b", "model": "groq:m-b", "priority": 5}]
    assert pool.complete("x", members=members) == "ok"
    assert calls and calls[0] == "groq:m-b"
    assert outcomes and outcomes[0][0] == "b"


def test_planner_uses_swan_when_available(store, bridge, monkeypatch):
    """SWAN supplies the planning reply when the stage is on."""
    import modules.lazy_loop as loop
    from modules.lazy_engine import LazyEngine

    monkeypatch.setattr(bridge, "swan_available", lambda: True)

    def _swan(prompt, task_type="recon", phase="enumeration", timeout=90.0):
        return "probe ssh banner\ncheck ollama api"

    monkeypatch.setattr(bridge, "swan_consult", _swan)
    monkeypatch.setattr(loop.LlmPool, "members", lambda self: [{"name": "stub"}])
    engine = LazyEngine()
    task_id = engine.create_task("gain initial access on 127.0.0.1")["task_id"]
    graph = loop.ExplorationGraph(task_id)
    planner = loop.Planner(task_id, engine.assets, graph, loop.ActivityLog(task_id), engine.store)
    proposed = [row[0] for row in planner._llm_candidates(set())]
    assert "probe ssh banner" in proposed
