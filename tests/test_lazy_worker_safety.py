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
