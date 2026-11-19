"""Technique intents resolve deterministically, not via the model.

Pins the operator contract: a MITRE-technique objective (``Review T1105:
...``) runs a headless ``atomic_tests`` through the deterministic step
loop and never reaches the tool-calling agent, so the loop stops spending
model turns on technique emulation. Exploitation intents are untouched.
"""

from __future__ import annotations

import pytest


def test_technique_intent_classification():
    """Only technique objectives match; exploitation and recon do not."""
    from modules.lazy_loop import _technique_intent

    assert _technique_intent("Review T1105: Apache WebDAV PUT") is True
    assert _technique_intent("objective: Review T1059.004 command injection") is True
    assert _technique_intent("gain initial access on 172.17.0.2") is False
    assert _technique_intent("baseline recon on 10.0.0.1") is False
    assert _technique_intent("enumerate services") is False


def test_technique_steps_are_headless():
    """The resolved command is a non-interactive atomic_tests line."""
    from modules.lazy_loop import _technique_steps

    assert _technique_steps("Review T1105: Apache WebDAV PUT") == [
        "atomic_tests T1105 --non-interactive"
    ]
    assert _technique_steps("Review T1059.004: cmd injection") == [
        "atomic_tests T1059.004 --non-interactive"
    ]
    assert _technique_steps("no technique here") == []


@pytest.fixture()
def worker_env(tmp_path, monkeypatch):
    """Sandbox the lazy store and build a worker on a lab target."""
    import core.config as core_config
    import modules.lazy_loop as loop
    from modules.lazy_engine import LazyEngine

    monkeypatch.setattr(loop, "STORE_DIR", tmp_path)
    monkeypatch.setattr(loop, "_store_path", lambda name: tmp_path / name)
    monkeypatch.setattr(core_config, "load_payload", lambda *a, **k: {})
    engine = LazyEngine()
    task_id = engine.create_task("killchain all on 172.17.0.2")["task_id"]
    engine.ensure_target(task_id, "172.17.0.2", "loop target")
    graph = loop.ExplorationGraph(task_id)
    worker = loop.Worker(
        "worker-2",
        task_id,
        engine.assets,
        graph,
        loop.ActivityLog(task_id),
        loop.TrafficLog(task_id),
        loop.Guard(task_id),
        engine.store,
    )
    return loop, worker, graph


def test_steps_for_resolves_technique(worker_env):
    """A technique intent's deterministic steps are the atomic_tests line."""
    loop, worker, graph = worker_env
    intent = graph.add_node("intent", "Review T1105: Apache WebDAV PUT", state="open")
    steps = worker._steps_for(graph.get(intent.node_id))
    assert steps == ["atomic_tests T1105 --non-interactive"]


def test_technique_deterministic_step_when_steps_run(worker_env, monkeypatch):
    """When the step loop runs for a technique intent it uses atomic_tests.

    The tier cascade is pure (code mode -> agent -> auto_pwn); the
    deterministic atomic line only replaces the generic probes inside the
    step loop, it never skips the agent.
    """
    loop, worker, graph = worker_env
    intent = graph.add_node("intent", "Review T1105: Apache WebDAV PUT", state="open")
    monkeypatch.setattr(worker, "_lazymode_try", lambda *a, **k: False)
    monkeypatch.setattr(worker, "_agentic_try", lambda *a, **k: False)
    ran: list = []

    def _executor(command):
        ran.append(command)
        return "staged (non-interactive)"

    worker.execute(graph.get(intent.node_id), executor=_executor)

    assert any(cmd.startswith("atomic_tests T1105") for cmd in ran)


def test_execute_uses_model_for_nontechnique(worker_env, monkeypatch):
    """A non-technique objective still reaches the agent (unchanged path)."""
    loop, worker, graph = worker_env
    intent = graph.add_node("intent", "enumerate the web surface", state="open")
    monkeypatch.setattr(worker, "_lazymode_try", lambda *a, **k: False)
    called = {"n": 0}

    def _agentic(*a, **k):
        called["n"] += 1
        return True

    monkeypatch.setattr(worker, "_agentic_try", _agentic)
    monkeypatch.setattr(worker, "_finish", lambda *a, **k: {"state": "done"})

    worker.execute(graph.get(intent.node_id), executor=lambda c: "ok")

    assert called["n"] == 1
