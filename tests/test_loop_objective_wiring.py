"""Loop wiring fidelity: objective queue and Hermes draft consumption.

These close the two orphaned read-sides: ``modules.lazy_objective_queue``
(injected objectives become planner candidates and are settled on wrap-up)
and ``modules.lazy_drafts`` (Hermes/MCP drafts become queued tasks).
"""

from __future__ import annotations

import datetime
import json


def _patched_engine(tmp_path, monkeypatch):
    """Return an engine whose stores live entirely under tmp_path."""
    import modules.lazy_loop as loop
    from modules.lazy_engine import LazyEngine

    monkeypatch.setattr(loop, "STORE_DIR", tmp_path)
    monkeypatch.setattr(loop, "SESSIONS_DIR", tmp_path)
    monkeypatch.setattr(loop, "_store_path", lambda name: tmp_path / name)
    return LazyEngine()


def _point_objectives(tmp_path, monkeypatch):
    """Redirect the objective store to a temp JSONL and return its path.

    ``lazy_objective_queue._objectives_path`` resolves the loop's live
    ``SESSIONS_DIR`` at call time, so redirecting it isolates the store.
    """
    import modules.lazy_loop as loop

    monkeypatch.setattr(loop, "SESSIONS_DIR", tmp_path)
    return tmp_path / "objectives.jsonl"


def _write_objective(path, objective_id, text, status="pending", priority="high", target=""):
    """Append one objective record to the JSONL store."""
    record = {
        "id": objective_id,
        "text": text,
        "status": status,
        "priority": priority,
        "created_at": datetime.datetime.now(datetime.UTC).isoformat(),
        "context": {"target": target} if target else {},
    }
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(record) + "\n")


def _statuses(path):
    """Return the id->status map of the objective store."""
    out = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            record = json.loads(line)
            out[record["id"]] = record["status"]
    return out


def test_pending_objectives_filters_by_target_and_priority(tmp_path, monkeypatch):
    """A target-bound objective for another host is skipped; priority orders."""
    from modules import lazy_objective_queue as objq

    path = _point_objectives(tmp_path, monkeypatch)
    _write_objective(path, "aaaa1111", "low global", priority="low")
    _write_objective(path, "bbbb2222", "high for host", priority="high", target="10.0.0.5")
    _write_objective(path, "cccc3333", "other host", priority="critical", target="10.0.0.9")

    out = objq.pending_objectives(limit=5, target="10.0.0.5")
    ids = [candidate.objective_id for candidate in out]
    assert "cccc3333" not in ids
    assert ids[0] == "bbbb2222"
    assert "aaaa1111" in ids


def test_planner_emits_and_claims_injected_objective(tmp_path, monkeypatch):
    """BDD: a pending objective becomes an intent and is marked in_progress."""
    import modules.lazy_loop as loop

    engine = _patched_engine(tmp_path, monkeypatch)
    path = _point_objectives(tmp_path, monkeypatch)
    task_id = engine.create_task("exploit 10.0.0.5")["task_id"]
    engine.ensure_target(task_id, "10.0.0.5", "test")
    _write_objective(path, "dddd4444", "enumerate shares", target="10.0.0.5")

    graph = loop.ExplorationGraph(task_id)
    planner = loop.Planner(task_id, engine.assets, graph, loop.ActivityLog(task_id), engine.store)
    summaries = [row[0] for row in planner._objective_candidates()]

    assert any(summary.startswith("objective dddd4444: enumerate shares") for summary in summaries)
    assert _statuses(path)["dddd4444"] == "in_progress"


def test_settle_marks_done_when_intent_done(tmp_path, monkeypatch):
    """A claimed objective whose intent reached done settles to done."""
    import modules.lazy_loop as loop

    engine = _patched_engine(tmp_path, monkeypatch)
    path = _point_objectives(tmp_path, monkeypatch)
    task_id = engine.create_task("exploit 10.0.0.5")["task_id"]
    _write_objective(path, "eeee5555", "pop a shell", status="in_progress", target="10.0.0.5")

    graph = loop.ExplorationGraph(task_id)
    node = graph.add_node("intent", "objective eeee5555: pop a shell", state="done")
    assert node is not None

    engine._settle_objectives(task_id)
    assert _statuses(path)["eeee5555"] == "done"


def test_settle_requeues_when_intent_unfinished(tmp_path, monkeypatch):
    """A claimed objective whose intent is not done returns to pending."""
    import modules.lazy_loop as loop

    engine = _patched_engine(tmp_path, monkeypatch)
    path = _point_objectives(tmp_path, monkeypatch)
    task_id = engine.create_task("exploit 10.0.0.5")["task_id"]
    _write_objective(path, "ffff6666", "pivot", status="in_progress", target="10.0.0.5")

    graph = loop.ExplorationGraph(task_id)
    graph.add_node("intent", "objective ffff6666: pivot", state="pending")

    engine._settle_objectives(task_id)
    assert _statuses(path)["ffff6666"] == "pending"


def test_drain_drafts_imports_pending_draft_as_task(tmp_path, monkeypatch):
    """A pending lazy_draft becomes a queued task and is marked imported."""
    import modules.lazy_drafts as drafts

    engine = _patched_engine(tmp_path, monkeypatch)
    monkeypatch.setattr(drafts, "BASE_DIR", str(tmp_path))
    drafts_dir = tmp_path / "sessions" / "lazy_drafts"
    drafts_dir.mkdir(parents=True, exist_ok=True)
    draft_path = drafts_dir / "task_0001.json"
    draft_path.write_text(
        json.dumps({
            "status": "pending",
            "goal": "recon 10.0.0.42",
            "scope": [{"value": "10.0.0.42"}],
        }),
        encoding="utf-8",
    )

    imported = engine._drain_drafts()
    assert len(imported) == 1
    record = json.loads(draft_path.read_text(encoding="utf-8"))
    assert record["status"] == "imported"
    assert record["imported_task_id"] == imported[0]


def test_drain_drafts_is_idempotent(tmp_path, monkeypatch):
    """Draining twice never spawns a second task for the same draft."""
    import modules.lazy_drafts as drafts

    engine = _patched_engine(tmp_path, monkeypatch)
    monkeypatch.setattr(drafts, "BASE_DIR", str(tmp_path))
    drafts_dir = tmp_path / "sessions" / "lazy_drafts"
    drafts_dir.mkdir(parents=True, exist_ok=True)
    (drafts_dir / "task_0001.json").write_text(
        json.dumps({"status": "pending", "goal": "recon 10.0.0.42", "scope": []}),
        encoding="utf-8",
    )

    first = engine._drain_drafts()
    second = engine._drain_drafts()
    assert len(first) == 1
    assert second == []


def test_daemon_drain_drafts_helper_is_safe_without_engine():
    """The daemon helper is a no-op when the loop engine is unavailable."""
    import skills.autonomous_daemon as daemon

    daemon._drain_drafts(None)


def test_daemon_drain_drafts_imports_pending_draft(tmp_path, monkeypatch):
    """The daemon hook imports a pending draft through a LazyEngine."""
    import modules.lazy_drafts as drafts
    import skills.autonomous_daemon as daemon

    engine = _patched_engine(tmp_path, monkeypatch)
    monkeypatch.setattr(drafts, "BASE_DIR", str(tmp_path))
    drafts_dir = tmp_path / "sessions" / "lazy_drafts"
    drafts_dir.mkdir(parents=True, exist_ok=True)
    (drafts_dir / "task_0001.json").write_text(
        json.dumps({"status": "pending", "goal": "recon 10.0.0.7", "scope": []}),
        encoding="utf-8",
    )

    daemon._drain_drafts(engine)
    record = json.loads((drafts_dir / "task_0001.json").read_text(encoding="utf-8"))
    assert record["status"] == "imported"
