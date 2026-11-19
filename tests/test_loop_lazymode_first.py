"""Code-mode (lazymode) is the worker's first option.

Pins the three-tier contract: the model authors ONE lazymode SDK script
(executed via sdk.lazymode.run) before the tool-calling agent; only when
the script is empty, errors, or does not prove progress does the worker
fall back to the agent (the model as before) and then to the deterministic
auto_pwn engine. The fall-through must be clean so the kill chain never
regresses.
"""

from __future__ import annotations

from types import SimpleNamespace

import pytest


def _result(ok=True, result=None, stdout="", error="", duration=0.1):
    """Return a stand-in for sdk.lazymode.LazymodeResult."""
    return SimpleNamespace(ok=ok, result=result, stdout=stdout, error=error, duration_s=duration)


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
    intent = graph.add_node("intent", "gain initial access on 172.17.0.2", state="open")
    return loop, worker, graph, intent


def _patch_model(monkeypatch, loop, reply, run_result):
    """Make the pool return *reply* and sdk.lazymode.run return *run_result*."""
    import sdk.lazymode as lazymode

    monkeypatch.setattr(loop.LlmPool, "complete", lambda self, *a, **k: reply)
    monkeypatch.setattr(lazymode, "run", lambda script, **k: run_result)


def test_codemode_shell_wins_and_skips_agent(worker_env, monkeypatch):
    """A script that proves a shell owns the intent before the agent runs."""
    loop, worker, _graph, intent = worker_env
    script_reply = "```python\nimport socket\nresult = {'shell': True, 'proof': 'uid=0(root)'}\n```"
    _patch_model(monkeypatch, loop, script_reply, _result(ok=True, result={"shell": True, "proof": "uid=0(root)"}))
    monkeypatch.setattr(worker, "_publish_shell_proof", lambda *a, **k: True)
    agentic = {"n": 0}
    monkeypatch.setattr(worker, "_agentic_try", lambda *a, **k: agentic.__setitem__("n", 1) or True)

    outcome = {"facts": 0, "assets": 0, "findings": 0, "state": "done"}
    transcripts: list = []
    from modules.lazy_loop import Budget

    won = worker._lazymode_try(intent, outcome, transcripts, None, Budget(worker.store))

    assert won is True
    assert outcome["findings"] == 1
    assert agentic["n"] == 0
    assert transcripts and transcripts[0][0] == f"lazymode:script#{intent.node_id}"


def test_codemode_exploit_without_shell_falls_through(worker_env, monkeypatch):
    """An exploitation script with no shell returns False (auto_pwn must run)."""
    loop, worker, _graph, intent = worker_env
    _patch_model(monkeypatch, loop, "```python\nresult = {'note': 'no shell'}\n```", _result(ok=True, result={"note": "x"}))
    monkeypatch.setattr(worker, "_publish_shell_proof", lambda *a, **k: False)

    outcome = {"facts": 0, "assets": 0, "findings": 0, "state": "done"}
    from modules.lazy_loop import Budget

    won = worker._lazymode_try(intent, outcome, [], None, Budget(worker.store))

    assert won is False
    assert outcome["findings"] == 0


def test_codemode_no_script_falls_through(worker_env, monkeypatch):
    """A reply with no code block hands off to the agent."""
    loop, worker, _graph, intent = worker_env
    ran = {"n": 0}
    import sdk.lazymode as lazymode

    monkeypatch.setattr(loop.LlmPool, "complete", lambda self, *a, **k: "I cannot help with that.")
    monkeypatch.setattr(lazymode, "run", lambda script, **k: ran.__setitem__("n", 1))

    from modules.lazy_loop import Budget

    won = worker._lazymode_try(intent, {"facts": 0, "findings": 0, "state": "done"}, [], None, Budget(worker.store))

    assert won is False
    assert ran["n"] == 0


def test_codemode_disabled_is_noop(worker_env, monkeypatch):
    """The payload flag off disables the code-mode first attempt entirely."""
    loop, worker, _graph, intent = worker_env
    monkeypatch.setattr(worker, "_lazymode_enabled", lambda: False)
    called = {"n": 0}
    monkeypatch.setattr(loop.LlmPool, "complete", lambda self, *a, **k: called.__setitem__("n", 1) or "")

    from modules.lazy_loop import Budget

    won = worker._lazymode_try(intent, {"facts": 0, "findings": 0, "state": "done"}, [], None, Budget(worker.store))

    assert won is False
    assert called["n"] == 0


def test_codemode_recon_owns_on_content(worker_env, monkeypatch):
    """A non-exploitation script that returns content resolves the intent."""
    loop, worker, graph, _intent = worker_env
    recon = graph.add_node("intent", "enumerate the web surface on 172.17.0.2", state="open")
    _patch_model(
        monkeypatch,
        loop,
        "```python\nresult = {'ports': [80, 443], 'server': 'Apache'}\n```",
        _result(ok=True, result={"ports": [80, 443], "server": "Apache"}),
    )

    outcome = {"facts": 0, "assets": 0, "findings": 0, "state": "done"}
    from modules.lazy_loop import Budget

    won = worker._lazymode_try(recon, outcome, [], None, Budget(worker.store))

    assert won is True
    assert outcome["facts"] == 1


def test_execute_tries_codemode_before_agentic(worker_env, monkeypatch):
    """execute dispatches the code-mode attempt ahead of the model agent."""
    loop, worker, _graph, intent = worker_env
    order: list[str] = []
    monkeypatch.setattr(worker, "_lazymode_try", lambda *a, **k: order.append("lazymode") or True)
    monkeypatch.setattr(worker, "_agentic_try", lambda *a, **k: order.append("agentic") or True)
    monkeypatch.setattr(worker, "_finish", lambda *a, **k: {"state": "done"})

    worker.execute(intent)

    assert order == ["lazymode"]
