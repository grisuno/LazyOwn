"""Deterministic initial-access intent: auto_pwn fires without an LLM."""

from __future__ import annotations

import pytest


@pytest.fixture()
def store(tmp_path, monkeypatch):
    import core.config as core_config
    import modules.lazy_loop as loop

    monkeypatch.setattr(loop, "STORE_DIR", tmp_path)
    monkeypatch.setattr(loop, "_store_path", lambda name: tmp_path / name)
    monkeypatch.setattr(core_config, "load_payload", lambda *a, **k: {})
    return tmp_path


def _make_planner(store, goal: str, target: str):
    import modules.lazy_loop as loop
    from modules.lazy_engine import LazyEngine

    engine = LazyEngine()
    task_id = engine.create_task(goal)["task_id"]
    if target:
        engine.ensure_target(task_id, target, "loop target")
    graph = loop.ExplorationGraph(task_id)
    return (
        loop.Planner(task_id, engine.assets, graph, loop.ActivityLog(task_id), engine.store),
        graph,
        task_id,
    )


def test_initial_access_candidate_emitted_for_access_goal(store):
    planner, _graph, _task = _make_planner(store, "gain initial access on 172.17.0.2", "172.17.0.2")
    candidate = planner._initial_access_candidate({n.text for n in planner.graph.list("intent")})
    assert candidate is not None
    summary, anchors, _parents, priority = candidate
    assert summary == "gain initial access on 172.17.0.2"
    assert priority == 10


def test_initial_access_candidate_skips_when_intent_exists(store):
    planner, graph, _task = _make_planner(store, "gain initial access on 172.17.0.2", "172.17.0.2")
    graph.add_node("intent", "gain initial access on 172.17.0.2", state="open")
    candidate = planner._initial_access_candidate({n.text for n in graph.list("intent")})
    assert candidate is None


def test_initial_access_candidate_skips_for_non_access_goal(store):
    planner, _graph, _task = _make_planner(store, "enumerate services on 172.17.0.2", "172.17.0.2")
    candidate = planner._initial_access_candidate({n.text for n in planner.graph.list("intent")})
    assert candidate is None


def test_plan_emits_initial_access_intent_first(store, monkeypatch):

    planner, graph, _task = _make_planner(store, "gain initial access on 172.17.0.2", "172.17.0.2")
    monkeypatch.setattr(planner, "_candidates", lambda: [])
    created = planner.plan([])
    texts = [node.text for node in created]
    assert texts and texts[0] == "gain initial access on 172.17.0.2"
    second = planner.plan([])
    assert all(node.text != "gain initial access on 172.17.0.2" for node in second)


def test_worker_steps_run_auto_pwn_for_access_intent(store):
    import modules.lazy_loop as loop
    from modules.lazy_engine import LazyEngine

    engine = LazyEngine()
    task_id = engine.create_task("gain initial access on 172.17.0.2")["task_id"]
    engine.ensure_target(task_id, "172.17.0.2", "loop target")
    graph = loop.ExplorationGraph(task_id)
    intent = graph.add_node("intent", "gain initial access on 172.17.0.2")
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
    steps = worker._steps_for(intent)
    assert "auto_pwn 172.17.0.2" in steps


def test_executor_bumps_auto_pwn_timeout(monkeypatch):
    import modules.auto_registry as registry

    captured: dict = {}

    def _fake_stream(command, on_output=None, timeout_sec=0):
        captured["timeout"] = timeout_sec
        return "ok"

    monkeypatch.setattr(registry, "execute_streaming", _fake_stream)
    monkeypatch.setattr(registry, "is_routable_command", lambda command: False)

    from modules.lazy_runner import AUTO_PWN_MIN_TIMEOUT_SEC, LoopRunConfig, build_executor

    config = LoopRunConfig(verb_timeout=300.0)
    executor = build_executor(None, config, lambda text: None, {})
    executor("auto_pwn 10.0.0.5")
    assert captured["timeout"] == AUTO_PWN_MIN_TIMEOUT_SEC
    executor("curl -sS http://10.0.0.5")
    assert captured["timeout"] == 300.0
