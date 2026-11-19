"""Deterministic-first, LLM-last for exploitation intents (lever #5).

A run that burns ~500s of LLM codegen only to arrive at auto_pwn, which roots
the box in ~1s, is spending tokens to reach a verb the deterministic layer
already owns. When an intent is exploitation-class the worker now skips the
lazymode and agentic LLM tiers and runs the deterministic playbook directly;
the LLM stays reserved for non-exploit gaps. Gated by
``payload.json:loop_exploit_first`` (default on).
"""

from __future__ import annotations

import pytest


@pytest.fixture()
def worker_env(tmp_path, monkeypatch):
    """Sandbox the lazy store and build a worker on a lab target."""
    import core.config as core_config
    import modules.lazy_loop as loop
    from modules.lazy_engine import LazyEngine

    monkeypatch.setattr(loop, "STORE_DIR", tmp_path)
    monkeypatch.setattr(loop, "_store_path", lambda name: tmp_path / name)
    monkeypatch.setattr(core_config, "load_payload", lambda *a, **k: {})
    monkeypatch.setattr(loop, "task_llm_chain", lambda *a, **k: ["member-a"])
    monkeypatch.setattr(loop.LlmPool, "members", lambda self: ["member-a"])
    engine = LazyEngine()
    task_id = engine.create_task("gain initial access on 172.17.0.2")["task_id"]
    engine.ensure_target(task_id, "172.17.0.2", "loop target")
    graph = loop.ExplorationGraph(task_id)
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
    return loop, worker, graph


def _spy_llm_tiers(worker, monkeypatch, calls):
    """Record whether the LLM tiers fire; both decline so deterministic runs."""
    monkeypatch.setattr(
        worker, "_lazymode_try", lambda *a, **k: calls.__setitem__("lazymode", calls["lazymode"] + 1) or False
    )
    monkeypatch.setattr(
        worker, "_agentic_try", lambda *a, **k: calls.__setitem__("agentic", calls["agentic"] + 1) or False
    )
    monkeypatch.setattr(worker, "_with_llm_steps", lambda intent, steps, prior: steps)


def test_loop_exploit_first_opt_in_default_off():
    """The lever is opt-in so the verified lazymode-first contract is preserved."""
    import modules.lazy_loop as loop

    assert loop._loop_exploit_first() is False


def test_exploit_intent_skips_llm_tiers_when_enabled(worker_env, monkeypatch):
    """With the lever on, an exploitation intent runs auto_pwn directly."""
    loop, worker, graph = worker_env
    monkeypatch.setattr(loop, "_loop_exploit_first", lambda: True)
    intent = graph.add_node("intent", "gain initial access on 172.17.0.2", state="open")
    calls = {"lazymode": 0, "agentic": 0}
    _spy_llm_tiers(worker, monkeypatch, calls)
    executed: list[str] = []
    worker.execute(intent, executor=lambda cmd: executed.append(cmd) or "benign output")
    assert calls["lazymode"] == 0
    assert calls["agentic"] == 0
    assert any("auto_pwn" in command for command in executed)


def test_recon_intent_still_uses_llm_tiers_when_enabled(worker_env, monkeypatch):
    """Even with the lever on, a non-exploit intent keeps the LLM-first path."""
    loop, worker, graph = worker_env
    monkeypatch.setattr(loop, "_loop_exploit_first", lambda: True)
    intent = graph.add_node("intent", "enumerate services on 172.17.0.2", state="open")
    calls = {"lazymode": 0, "agentic": 0}
    _spy_llm_tiers(worker, monkeypatch, calls)
    worker.execute(intent, executor=lambda cmd: "benign output")
    assert calls["lazymode"] == 1


def test_default_off_keeps_llm_first_for_exploit(worker_env, monkeypatch):
    """By default an exploit intent still goes through the LLM tiers first."""
    loop, worker, graph = worker_env
    intent = graph.add_node("intent", "gain initial access on 172.17.0.2", state="open")
    calls = {"lazymode": 0, "agentic": 0}
    _spy_llm_tiers(worker, monkeypatch, calls)
    worker.execute(intent, executor=lambda cmd: "benign output")
    assert calls["lazymode"] == 1
