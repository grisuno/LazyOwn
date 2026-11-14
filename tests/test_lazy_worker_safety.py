"""Worker safety: step sanitizer, task-wide dedupe, sudo skip, worker pool.

These tests pin the behaviors the live engagement surfaced: the planner
LLM proposing target-less or foreign-host network commands, the same
verb replayed under a new intent, interactive sudo inside an unattended
loop, and one-shot workers losing their shells between rounds.
"""

from __future__ import annotations

import pytest


@pytest.fixture()
def payload_store(tmp_path, monkeypatch):
    """Sandbox the lazy store and orchestrator config for a round."""
    import modules.lazy_loop as loop
    from modules import orchestrator_config as config

    monkeypatch.setattr(loop, "STORE_DIR", tmp_path)
    monkeypatch.setattr(loop, "_store_path", lambda name: tmp_path / name)
    monkeypatch.setattr(config, "_PATH", tmp_path / "payload.json", raising=False)
    config._invalidate()
    yield tmp_path
    config._invalidate()


def _engine(tmp_path, monkeypatch):
    import modules.lazy_loop as loop
    from modules.lazy_engine import LazyEngine

    monkeypatch.setattr(loop, "STORE_DIR", tmp_path)
    monkeypatch.setattr(loop, "_store_path", lambda name: tmp_path / name)
    return loop, LazyEngine()


def _worker(loop, engine, task_id, name="worker-1", **kwargs):
    graph = loop.ExplorationGraph(task_id)
    worker = loop.Worker(
        name,
        task_id,
        engine.assets,
        graph,
        loop.ActivityLog(task_id),
        loop.TrafficLog(task_id),
        loop.Guard(task_id),
        engine.store,
        **kwargs,
    )
    return worker, graph


def test_sanitizer_retargets_and_repairs_commands(tmp_path, monkeypatch):
    """Foreign hosts move to the target; target-less scans gain it."""
    loop, engine = _engine(tmp_path, monkeypatch)
    task_id = engine.create_task("gain initial access on 127.0.0.1")["task_id"]
    worker, graph = _worker(loop, engine, task_id)
    intent = graph.add_node("intent", "probe http surface")
    node = graph.get(intent.node_id)

    assert worker._sanitize_step(node, "nmap -p 75") == "nmap -p 75 127.0.0.1"
    assert worker._sanitize_step(node, "nmap config") == "nmap 127.0.0.1"
    assert worker._sanitize_step(node, "nmap -sV nmap.org") == "nmap -sV 127.0.0.1"
    assert worker._sanitize_step(node, "curl http://nmap.org/x") == "curl http://127.0.0.1/x"
    assert worker._sanitize_step(node, "ssh -p 22 127.0.0.1") == "ssh -p 22 127.0.0.1"
    assert worker._sanitize_step(node, "id") == "id"
    worker.close()


def test_worker_dedupes_commands_already_executed_for_task(tmp_path, monkeypatch):
    """A command run under intent #1 is never replayed under intent #2."""
    loop, engine = _engine(tmp_path, monkeypatch)
    monkeypatch.setattr(loop.Worker, "_agentic_try", lambda self, *a, **k: False)
    task_id = engine.create_task("gain initial access on 127.0.0.1")["task_id"]
    worker, graph = _worker(loop, engine, task_id)
    activity = loop.ActivityLog(task_id)
    activity.emit("worker-1", "tool", "[allow] nmap -sV 127.0.0.1")
    first = graph.add_node("intent", "baseline recon: enumerate 127.0.0.1")
    second = graph.add_node("intent", "baseline recon: enumerate 127.0.0.1 again")
    worker.execute(graph.get(first.node_id), executor=lambda command: "22/tcp open ssh")
    outcome = worker.execute(graph.get(second.node_id), executor=lambda command: "22/tcp open ssh")
    kinds = [record.get("kind") for record in activity.read(200)]
    assert "dedupe" in kinds
    assert outcome["state"] in ("exhausted", "done", "blocked")
    worker.close()


def test_worker_skips_sudo_when_unavailable(tmp_path, monkeypatch):
    """A tool failing on non-interactive sudo is skipped, not an error."""
    loop, engine = _engine(tmp_path, monkeypatch)
    task_id = engine.create_task("gain initial access on 127.0.0.1")["task_id"]
    worker, graph = _worker(loop, engine, task_id)
    intent = graph.add_node("intent", "enumerate 127.0.0.1 ports")

    def executor(command):
        return "[x] LazyNmap requires sudo; unattended loop has no terminal for the password. Aborting."

    outcome = worker.execute(graph.get(intent.node_id), executor=executor)
    trail = loop.ActivityLog(task_id).read(200)
    assert any(record.get("kind") == "block" and "sudo" in record.get("text", "") for record in trail)
    assert outcome["state"] in ("exhausted", "blocked")
    worker.close()


def test_run_round_reuses_worker_pool(payload_store, monkeypatch):
    """A supplied pool keeps the same workers and shells across rounds."""
    import modules.lazy_loop as loop
    from modules import orchestrator_config as config
    from modules.lazy_engine import LazyEngine

    monkeypatch.setattr(loop, "STORE_DIR", payload_store)
    monkeypatch.setattr(loop, "_store_path", lambda name: payload_store / name)
    config._invalidate()
    engine = LazyEngine()
    task_id = engine.create_task("gain initial access on 127.0.0.1")["task_id"]
    graph = loop.ExplorationGraph(task_id)
    graph.add_node("intent", "probe 127.0.0.1")
    graph.add_node("intent", "enumerate 127.0.0.1")

    calls: list[str] = []

    def _fake_execute(self, node, executor=None, timeout_sec=0.0):
        calls.append(self.name)
        return {"intent_id": node.node_id, "worker": self.name, "facts": 0, "assets": 0, "findings": 0, "state": "done"}

    monkeypatch.setattr(loop.Worker, "execute", _fake_execute)
    pool: dict[int, loop.Worker] = {}
    engine.run_round(task_id, workers=1, executor=lambda command: "", pool=pool)
    first_names = [worker.name for worker in pool.values()]
    assert first_names == ["worker-1"]
    loop.ExplorationGraph(task_id).add_node("intent", "third probe 127.0.0.1")
    engine.run_round(task_id, workers=1, executor=lambda command: "", pool=pool)
    assert [worker.name for worker in pool.values()] == first_names
    assert all(worker._closed is False for worker in pool.values())
    for worker in pool.values():
        worker.close()
    assert all(worker._closed is True for worker in pool.values())


def test_needs_sudo_detects_wrappers_and_segments(tmp_path, monkeypatch):
    """Alias and wrapper forms hide sudo; the detector sees through them."""
    from utils import needs_sudo

    assert needs_sudo("sudo lsof -i -P -n")
    assert needs_sudo("sh sudo lsof -i -P -n | grep LISTEN")
    assert needs_sudo("A=1; sudo id")
    assert needs_sudo("env FOO=1 sudo id")
    assert not needs_sudo("lsattr -va")
    assert not needs_sudo("echo sudo")
    assert not needs_sudo("ssh user@host 'sudo id'")


def test_worker_skips_sudo_alias_before_execution(tmp_path, monkeypatch):
    """The lsof alias expands to sudo; it is skipped before any execution."""
    from types import SimpleNamespace

    import utils

    loop, engine = _engine(tmp_path, monkeypatch)
    monkeypatch.setattr(loop.Worker, "_agentic_try", lambda self, *a, **k: False)
    monkeypatch.setattr(utils, "sudo_available", lambda: False)
    task_id = engine.create_task("gain initial access on 127.0.0.1")["task_id"]
    fake_shell = SimpleNamespace(aliases={"lsof": "sh sudo lsof -i -P -n | grep LISTEN"})
    worker, graph = _worker(loop, engine, task_id, shell=fake_shell)
    monkeypatch.setattr(loop.Worker, "_steps_for", lambda self, node: ["lsof"])
    intent = graph.add_node("intent", "list listening ports 127.0.0.1")
    calls: list[str] = []
    worker.execute(graph.get(intent.node_id), executor=lambda command: calls.append(command) or "ok")
    assert calls == []
    trail = loop.ActivityLog(task_id).read(200)
    assert any(record.get("kind") == "block" and "sudo" in record.get("text", "") for record in trail)
    worker.close()


def test_worker_runs_sudo_alias_when_passwordless_available(tmp_path, monkeypatch):
    """With working passwordless sudo the command executes normally."""
    from types import SimpleNamespace

    import utils

    loop, engine = _engine(tmp_path, monkeypatch)
    monkeypatch.setattr(loop.Worker, "_agentic_try", lambda self, *a, **k: False)
    monkeypatch.setattr(utils, "sudo_available", lambda: True)
    task_id = engine.create_task("gain initial access on 127.0.0.1")["task_id"]
    fake_shell = SimpleNamespace(aliases={"lsof": "sh sudo lsof -i -P -n | grep LISTEN"})
    worker, graph = _worker(loop, engine, task_id, shell=fake_shell)
    monkeypatch.setattr(loop.Worker, "_steps_for", lambda self, node: ["lsof"])
    intent = graph.add_node("intent", "list listening ports 127.0.0.1")
    calls: list[str] = []
    worker.execute(graph.get(intent.node_id), executor=lambda command: calls.append(command) or "LISTEN")
    assert calls == ["lsof"]
    worker.close()


def test_capable_member_chain_filters_toy_models():
    """Only tool-calling-capable backends may propose loop commands."""
    from modules.loop.worker_agentic import _capable_member_chain

    members = [
        {"name": "ollama-local", "model": "ollama:deepseek-r1:1.5b", "priority": 9},
        {"name": "groq", "model": "groq:llama-3.3-70b-versatile", "priority": 5},
        "not-a-dict",
        {"name": "bad", "model": "groq:"},
    ]
    chain = _capable_member_chain(members)
    assert [m["name"] for m in chain] == ["groq"]
    assert _capable_member_chain([]) == []
    assert _capable_member_chain([{"name": "only-toy", "model": "ollama:qwen:7b"}]) == []


def test_destructive_or_malformed_steps_rejected():
    """Operator-host destructive heads and flag fragments never execute."""
    from modules.loop.worker_agentic import _is_destructive_or_malformed

    for command in (
        "killall openvpn 2>/dev/null",
        "tmux kill-session -t lazyown_sessions 2>/dev/null",
        "systemctl stop docker",
        "dd if=/dev/zero of=/dev/sda",
        "--profile",
        "-c 'echo hi'",
        "shutdown -h now",
    ):
        assert _is_destructive_or_malformed(command), command
    for command in ("nmap -sV 127.0.0.1", "curl -sSI http://127.0.0.1", "auto_pwn 172.17.0.2"):
        assert not _is_destructive_or_malformed(command), command


def test_initial_access_intent_escalates_to_auto_pwn(tmp_path, monkeypatch):
    """Exploitation-class intents escalate deterministically to auto_pwn."""
    loop, engine = _engine(tmp_path, monkeypatch)
    task_id = engine.create_task("gain initial access on 172.17.0.2")["task_id"]
    worker, graph = _worker(loop, engine, task_id)
    intent = graph.add_node("intent", "gain initial access on 172.17.0.2")
    node = graph.get(intent.node_id)

    steps = worker._steps_for(node)
    assert steps[-1] == "auto_pwn 172.17.0.2"
    worker.close()


def test_enumeration_intent_does_not_escalate(tmp_path, monkeypatch):
    """Plain enumeration keeps the recon step list without auto_pwn."""
    loop, engine = _engine(tmp_path, monkeypatch)
    task_id = engine.create_task("gain initial access on 172.17.0.2")["task_id"]
    worker, graph = _worker(loop, engine, task_id)
    intent = graph.add_node("intent", "enumerate services on 172.17.0.2")
    node = graph.get(intent.node_id)

    steps = worker._steps_for(node)
    assert not any(step.startswith("auto_pwn") for step in steps)
    worker.close()


def test_worker_llm_steps_require_capable_member(tmp_path, monkeypatch):
    """Toy-model-only pools never propose worker commands."""
    import modules.lazy_loop as loop

    loop, engine = _engine(tmp_path, monkeypatch)
    task_id = engine.create_task("gain initial access on 172.17.0.2")["task_id"]
    worker, graph = _worker(loop, engine, task_id)

    class _ToyPool:
        def __init__(self, *a, **k):
            pass

        def members(self):
            return [{"name": "ollama-local", "model": "ollama:deepseek-r1:1.5b", "priority": 1}]

        def complete(self, *a, **k):
            raise AssertionError("toy model must not be consulted for worker steps")

    monkeypatch.setattr(loop, "LlmPool", _ToyPool)
    monkeypatch.setattr(loop, "task_llm_chain", lambda store, task_id: [])
    intent = graph.add_node("intent", "probe http surface")
    node = graph.get(intent.node_id)

    assert worker._llm_steps(node, "") == []
    worker.close()


def test_agent_with_zero_tool_calls_falls_back_to_deterministic(tmp_path, monkeypatch):
    """A dead or silent LLM agent must not suppress the deterministic layer.

    The live t0226 failure: Groq timed out mid-turn, the session returned
    zero executed tools, and ``_agentic_try`` still claimed the intent —
    so lazynmap/auto_pwn never ran. Zero tools means the agent did
    nothing: the deterministic step loop must execute instead.
    """
    import modules.lazy_agent as agent
    import modules.lazy_loop as loop

    loop, engine = _engine(tmp_path, monkeypatch)
    monkeypatch.setattr(agent, "tool_calling_enabled", lambda: True)
    monkeypatch.setattr(agent, "resolve_agentic_model", lambda exclude=None: object())
    monkeypatch.setattr(
        agent,
        "run_worker_session",
        lambda *a, **k: {"reply": "", "tool_calls": {}, "messages": 1},
    )
    task_id = engine.create_task("gain initial access on 172.17.0.2")["task_id"]
    worker, graph = _worker(loop, engine, task_id)
    intent = graph.add_node("intent", "enumerate 172.17.0.2 ports")
    executed: list[str] = []

    def executor(command: str) -> str:
        executed.append(command)
        return "22/tcp open ssh"

    outcome = worker.execute(graph.get(intent.node_id), executor=executor, timeout_sec=75.0)
    assert executed, "agent executed zero tools; deterministic steps must run"
    assert outcome["state"] in ("done", "exhausted")
    worker.close()


def test_agent_skipped_when_task_deadline_expired(tmp_path, monkeypatch):
    """An expired wall clock never starts the agent; steps still settle."""
    import modules.lazy_agent as agent
    import modules.lazy_loop as loop

    loop, engine = _engine(tmp_path, monkeypatch)
    monkeypatch.setattr(agent, "tool_calling_enabled", lambda: True)
    monkeypatch.setattr(agent, "resolve_agentic_model", lambda exclude=None: object())

    calls: list[tuple] = []

    def _must_not_run(*a, **k):
        calls.append((a, k))
        return {"reply": "", "tool_calls": {}, "messages": 0}

    monkeypatch.setattr(agent, "run_worker_session", _must_not_run)
    task_id = engine.create_task("gain initial access on 172.17.0.2")["task_id"]
    record = engine.store.get(task_id) or {}
    record["deadline"] = 1.0
    engine.store._persist()
    worker, graph = _worker(loop, engine, task_id)
    intent = graph.add_node("intent", "enumerate 172.17.0.2 ports")
    executed: list[str] = []
    outcome = worker.execute(
        graph.get(intent.node_id),
        executor=lambda command: (executed.append(command), "22/tcp open ssh")[1],
        timeout_sec=0.0,
    )
    assert not executed
    assert not calls, "agent session must never start on an expired task"
    assert outcome["state"] == "stopped"
    worker.close()


def test_goal_named_target_wins_over_payload_scope(tmp_path, monkeypatch):
    """The host named in the goal outranks a stale payload scope entry.

    Live t0225/t0226 regression: the task inherited payload scope
    (127.0.0.1) before the goal-named target (172.17.0.2), and
    resolve_target returns the first item, so every deterministic step
    attacked loopback. The goal's explicit target must be inserted first.
    """
    import modules.lazy_loop as loop

    loop, engine = _engine(tmp_path, monkeypatch)
    monkeypatch.setattr(
        loop,
        "_payload_scope_items",
        lambda: [{"kind": "ip", "value": "127.0.0.1", "reason": "payload scope"}],
    )
    summary = engine.create_task("gain initial access on 172.17.0.2")
    task_id = summary["task_id"]
    assert loop.resolve_target(task_id, engine.store, loop.ExplorationGraph(task_id)) == "172.17.0.2"
