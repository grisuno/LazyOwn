"""Worker cross-work trace tools (lazy 0.3.10 parity)."""

from __future__ import annotations


def _patched_engine(tmp_path, monkeypatch):
    import modules.lazy_loop as loop
    from modules.lazy_engine import LazyEngine

    monkeypatch.setattr(loop, "STORE_DIR", tmp_path)
    monkeypatch.setattr(loop, "_store_path", lambda name: tmp_path / name)
    return LazyEngine()


def _seed_two_works(engine, task_id):
    import modules.lazy_loop as loop

    first = engine.add_intent(task_id, "probe ssh")
    second = engine.add_intent(task_id, "probe http")
    activity = loop.ActivityLog(task_id)
    activity.emit("worker-1", "tool", "nmap port 22 open banner OpenSSH", intent_id=first.node_id)
    activity.emit("worker-1", "result", "ssh reachable with password auth", intent_id=first.node_id)
    activity.emit("worker-2", "tool", "curl login page title Dashboard", intent_id=second.node_id)
    return first, second


def test_search_all_spans_works_without_intent(tmp_path, monkeypatch):
    """BDD: keyword search hits every work without knowing intent ids."""
    import modules.lazy_loop as loop

    engine = _patched_engine(tmp_path, monkeypatch)
    task_id = engine.create_task("gain initial access on 127.0.0.1")["task_id"]
    first, _second = _seed_two_works(engine, task_id)
    hits = loop.ActivityLog(task_id).search_all("ssh")
    assert hits
    assert all("ssh" in h["text"].lower() for h in hits)
    assert any(h["intent_id"] == first.node_id and h["step"] == 1 for h in hits)


def test_trace_steps_and_single_step(tmp_path, monkeypatch):
    """BDD: lock onto a work, list the step flow, fetch one step in full."""
    import modules.lazy_loop as loop

    engine = _patched_engine(tmp_path, monkeypatch)
    task_id = engine.create_task("gain initial access on 127.0.0.1")["task_id"]
    first, _second = _seed_two_works(engine, task_id)
    view = loop.ActivityLog(task_id).trace(first.node_id)
    assert view["total"] == 3
    assert [s["step"] for s in view["steps"]] == [1, 2, 3]
    filtered = loop.ActivityLog(task_id).trace(first.node_id, query="password")
    assert len(filtered["steps"]) == 1
    single = loop.ActivityLog(task_id).trace(first.node_id, step_id=3)
    assert single["step"]["kind"] == "result"
    assert "password auth" in single["step"]["text"]


def test_worker_lane_binds_node_detail(tmp_path, monkeypatch):
    """BDD: worker keeps node_detail for cross-work lookups."""
    import modules.lazy_loop as loop

    _patched_engine(tmp_path, monkeypatch)
    assert "node" in loop.ToolCatalog().bindings("worker")["worker"]


def test_add_hint_emits_explicit_planner_trigger(tmp_path, monkeypatch):
    """BDD: a new hint fires an explicit planner trigger round."""
    import modules.lazy_loop as loop

    engine = _patched_engine(tmp_path, monkeypatch)
    task_id = engine.create_task("gain initial access on 127.0.0.1")["task_id"]
    node = engine.add_hint(task_id, "focus on login forms")
    trail = loop.ActivityLog(task_id).read(20)
    fired = [r for r in trail if r.get("kind") == "hint-trigger"]
    assert len(fired) == 1
    assert f"#{node.node_id}" in fired[0]["text"]
    assert "login forms" in fired[0]["text"]
    triggers = engine._drain_triggers(task_id, loop.ExplorationGraph(task_id))
    assert any(t["kind"] == "hint" and "login forms" in t.get("text", "") for t in triggers)


def test_worker_bash_unbound_blocks_without_execution(tmp_path, monkeypatch):
    """BDD: unbinding bash from the worker lane stops probes cold."""
    import modules.lazy_loop as loop

    engine = _patched_engine(tmp_path, monkeypatch)
    task_id = engine.create_task("gain initial access on 127.0.0.1")["task_id"]
    loop.ToolCatalog().unbind("worker", "bash")
    graph = loop.ExplorationGraph(task_id)
    intent = graph.add_node("intent", "baseline recon: enumerate 127.0.0.1")
    calls: list[str] = []
    worker = loop.Worker("worker-1", task_id, engine.assets, graph,
                         loop.ActivityLog(task_id), loop.TrafficLog(task_id),
                         loop.Guard(task_id), engine.store)
    outcome = worker.execute(intent, executor=lambda cmd: calls.append(cmd) or "out")
    assert outcome["state"] == "blocked"
    assert calls == []
    assert graph.get(intent.node_id).state == "blocked"


def test_planner_intent_unbound_emits_nothing(tmp_path, monkeypatch):
    """BDD: unbinding intent from the planner lane silences planning."""
    import modules.lazy_loop as loop

    engine = _patched_engine(tmp_path, monkeypatch)
    task_id = engine.create_task("gain initial access on 127.0.0.1")["task_id"]
    loop.ToolCatalog().unbind("planner", "intent")
    planner = loop.Planner(task_id, engine.assets, loop.ExplorationGraph(task_id),
                           loop.ActivityLog(task_id), engine.store)
    assert planner.plan() == []
