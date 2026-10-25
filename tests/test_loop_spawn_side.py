"""Multi-session chat, persistent side questions, spawn inheritance (lazy 0.3.9)."""

from __future__ import annotations


def _patched_engine(tmp_path, monkeypatch):
    import modules.lazy_loop as loop
    from modules.lazy_engine import LazyEngine

    monkeypatch.setattr(loop, "STORE_DIR", tmp_path)
    monkeypatch.setattr(loop, "_store_path", lambda name: tmp_path / name)
    return LazyEngine()


def test_chat_sessions_stay_independent(tmp_path, monkeypatch):
    """BDD: one task holds many dialogue sessions that never interleave."""
    import modules.lazy_loop as loop

    _patched_engine(tmp_path, monkeypatch)
    engine_task = _patched_engine(tmp_path, monkeypatch)
    task_id = engine_task.create_task("gain initial access on 127.0.0.1")["task_id"]
    chat = loop.TaskChat()
    chat.say(task_id, "mainline status?", session="main")
    chat.say(task_id, "btw what port was that?", session="btw")
    main = chat.log(task_id, session="main")
    btw = chat.log(task_id, session="btw")
    assert len(main) == 2
    assert len(btw) == 2
    assert all(t.get("session") == "main" for t in main)
    assert set(chat.sessions(task_id)) == {"main", "btw"}
    assert chat.clear(task_id, session="btw") is True
    assert chat.log(task_id, session="btw") == []
    assert len(chat.log(task_id, session="main")) == 2


def test_side_questions_persist_and_recall(tmp_path, monkeypatch):
    """BDD: side threads survive restarts and list per session."""
    import modules.lazy_loop as loop

    engine = _patched_engine(tmp_path, monkeypatch)
    task_id = engine.create_task("gain initial access on 127.0.0.1")["task_id"]
    table = loop.SideQuestions()
    first = table.ask(task_id, "which service answered?", session="btw")
    second = table.ask(task_id, "second thread?", session="deep-dive")
    assert first["session"] == "btw"
    assert first["id"] == 1
    assert second["id"] == 2
    assert len(table.history(task_id)) == 2
    assert [i["id"] for i in table.history(task_id, session="btw")] == [1]
    assert table.sessions(task_id) == ["btw", "deep-dive"]


def test_spawn_inherits_scope_and_findings_read_only(tmp_path, monkeypatch):
    """BDD: child task reads parent scope/findings, parents stay intact."""
    import modules.lazy_loop as loop

    engine = _patched_engine(tmp_path, monkeypatch)
    parent = engine.create_task("gain initial access on 127.0.0.1")["task_id"]
    graph = loop.ExplorationGraph(parent)
    service = loop.FindingService(parent, graph, loop.ActivityLog(parent), engine.store)
    service.report("sqli in login", summary="error-based", severity="high")
    parent_scope = (engine.store.get(parent) or {}).get("scope", [])
    assert parent_scope
    child = engine.spawn_task("escalate on 127.0.0.1", source_task_ids=[parent])
    assert child["inherited"]["sources"] == [parent]
    assert child["inherited"]["scope"] == len(parent_scope)
    assert child["inherited"]["facts"] == 1
    child_graph = loop.ExplorationGraph(child["task_id"])
    inherited = [n for n in child_graph.list("fact") if n.meta.get("inherited_from") == parent]
    assert len(inherited) == 1
    assert inherited[0].meta["severity"] == "high"
    assert len(loop.ExplorationGraph(parent).list("finding")) == 1
    assert (engine.store.get(child["task_id"]) or {}).get("scope") != []
