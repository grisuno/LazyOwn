"""Lazy engine (LAZY-faithful) regression tests with stub executor."""

from __future__ import annotations

import pytest

from modules.lazy_engine import LazyEngine
from modules.lazy_loop import ExplorationGraph


def _stub_executor(command: str) -> str:
    if command.startswith("nmap"):
        return ("Nmap scan report for localhost (127.0.0.1)\n"
                "PORT   STATE  SERVICE\n22/tcp closed ssh\n80/tcp closed http\n")
    if command.startswith("curl"):
        return "curl: (7) Failed to connect to 127.0.0.1:80"
    if command.startswith("dig"):
        return "127.0.0.1"
    return "ok"


@pytest.fixture()
def engine(tmp_path, monkeypatch):
    import modules.lazy_loop as loop
    import modules.lazy_loop as shim

    monkeypatch.setattr(loop, "STORE_DIR", tmp_path)
    monkeypatch.setattr(loop, "_store_path",
                        lambda name: (tmp_path.mkdir(exist_ok=True) if False else tmp_path) / name)
    monkeypatch.setattr(shim, "STORE_DIR", tmp_path, raising=False)
    eng = LazyEngine()
    return eng


def test_create_auto_scope_and_asset(engine):
    summary = engine.create_task("gain initial access on 127.0.0.1")
    record = engine.store.get(summary["task_id"])
    assert any(s["value"] == "127.0.0.1" for s in record["scope"])
    assert any(a.value == "127.0.0.1" for a in engine.assets.list("ip"))


def test_scope_strict_no_external_intents(engine):
    summary = engine.create_task("gain initial access on 127.0.0.1")
    task_id = summary["task_id"]
    engine.assets.insert("subdomain", "external.example.com")
    out = engine.run(task_id, max_rounds=2, workers=1, executor=_stub_executor)
    intents = out["overview"].get("intents", [])
    assert intents, "stall-guard must emit at least one intent"
    assert all("external.example.com" not in i["text"] for i in intents)


def test_no_premature_done_goals_pending(engine):
    summary = engine.create_task("gain initial access on 127.0.0.1")
    out = engine.run(summary["task_id"], max_rounds=2, workers=1, executor=_stub_executor)
    assert out["status"] in ("running", "exhausted", "paused", "timeout")
    if out["overview"].get("facts", 0) > 0:
        assert out["status"] != "done" or all(
            g["state"] == "done" for g in out["overview"].get("goals", []))


def test_worker_aggregates_single_fact(engine):
    summary = engine.create_task("gain initial access on 127.0.0.1")
    out = engine.run(summary["task_id"], max_rounds=1, workers=1, executor=_stub_executor)
    assert out["overview"].get("facts", 0) >= 1


def test_pause_resume(engine):
    summary = engine.create_task("gain initial access on 127.0.0.1")
    task_id = summary["task_id"]
    assert engine.store.pause(task_id)
    out = engine.run_round(task_id, workers=1, executor=_stub_executor)
    assert out.get("paused") or out["executed"] == 0
    assert engine.store.resume(task_id)
    assert engine.store.get(task_id)["status"] == "running"


def test_prove_goal_needs_reason_and_evidence(engine):
    summary = engine.create_task("gain initial access on 127.0.0.1")
    task_id = summary["task_id"]
    graph = ExplorationGraph(task_id)
    goal = graph.list("goal")[0]
    fact = graph.add_node("fact", "observed open ssh", state="done")
    assert engine.prove_goal(task_id, goal.node_id, fact.node_id, "") is False
    assert engine.prove_goal(task_id, goal.node_id, fact.node_id, "ssh observed open") is True


def test_lazy_alias_surface():
    import cli.commands.lazyops as lazyops

    assert hasattr(lazyops, "LazyCommandSet")
    commands = [n for n in dir(lazyops.LazyCommandSet) if n.startswith("do_lazy_")]
    for expected in ("do_lazy_task", "do_lazy_scope", "do_lazy_asset", "do_lazy_loop",
                     "do_lazy_planner", "do_lazy_worker", "do_lazy_goal", "do_lazy_report"):
        assert expected in commands


def test_delete_task_sweeps_only_its_store_files(engine, tmp_path):
    """BDD: deleting a task removes its files and leaves siblings intact."""
    first = engine.create_task("gain initial access on 127.0.0.1")["task_id"]
    second = engine.create_task("gain initial access on 127.0.0.2")["task_id"]
    result = engine.delete_task(first)
    assert result["deleted"] is True
    assert result["removed"]
    assert engine.store.get(first) is None
    assert engine.store.get(second) is not None
    names = {p.name for p in tmp_path.iterdir() if p.is_file()}
    assert not any(name.startswith(f"exp_{first}.") or f"_{first}." in name for name in names)
    assert any(second in name for name in names)


def test_delete_task_unknown_returns_empty(engine):
    """BDD: deleting an unknown task is a no-op, not an error."""
    assert engine.delete_task("t9999") == {"deleted": False, "removed": []}
