"""World-diff retest loop contract: detected changes steer the planner.

The sink records per-host snapshot diffs, the planner mines recent
changes into ``re-test`` candidate intents, and the world-diff sink only
fires for outcome kinds that can move the world.
"""

from __future__ import annotations

import json
from pathlib import Path

from modules.lazy_world_diff import SurfaceChange, record_changes, recent_changes
from modules.outcome_bus import OutcomeEvent
from modules.sinks.world_diff import _DIFF_KINDS


def test_world_diff_sink_gates_non_moving_kinds():
    """Given a report-only event, When the sink gates, Then only moving kinds apply."""
    assert "chain" in _DIFF_KINDS
    assert "finding" in _DIFF_KINDS
    assert "shell" in _DIFF_KINDS
    assert "emulation" in _DIFF_KINDS


def test_record_and_recent_roundtrip(tmp_path: Path):
    """Given a recorded change, When reading recent, Then the row is newest-first."""
    now = 1_900_000_000.0
    written = record_changes(
        [SurfaceChange(kind="port_opened", ip="10.0.0.9", port=443, before=None, after={"service": "https"})],
        tmp_path,
        now=now,
    )
    assert written == 1
    rows = recent_changes(tmp_path, days=7)
    assert rows and rows[0]["ip"] == "10.0.0.9" and rows[0]["kind"] == "port_opened"

    json_path = tmp_path / "lazy_changes.jsonl"
    assert json_path.is_file()
    assert json.loads(json_path.read_text(encoding="utf-8").splitlines()[0])["ip"] == "10.0.0.9"


def test_planner_mines_changes_into_retest_intents(tmp_path, monkeypatch):
    """Given a recent change, When the planner plans, Then a re-test candidate exists."""
    record_changes(
        [SurfaceChange(kind="port_opened", ip="10.0.0.9", port=3389, before=None, after={"service": "ms-wbt-server"})],
        tmp_path,
        now=None,
    )
    import modules.lazy_loop as loop

    store = tmp_path / "lazy"
    store.mkdir(parents=True, exist_ok=True)
    monkeypatch.setattr(loop, "STORE_DIR", store, raising=False)
    monkeypatch.setattr(loop, "_store_path", lambda name: store / name, raising=False)
    monkeypatch.setattr(loop, "SESSIONS_DIR", tmp_path, raising=False)
    from modules.lazy_engine import LazyEngine

    engine = LazyEngine()
    task_id = engine.create_task("gain initial access on 10.0.0.9")["task_id"]
    graph = loop.ExplorationGraph(task_id)
    graph.add_node("goal", "recon 10.0.0.9 fully", state="pending")
    planner = loop.Planner(task_id, engine.assets, graph, loop.ActivityLog(task_id), engine.store)
    summaries = [row[0] for row in planner._candidates()]
    assert any(s.startswith("re-test 10.0.0.9 after ") for s in summaries)


def test_outcome_event_shape_typed(tmp_path: Path):
    """Given a plain world event, When constructing, Then the sink contract stays typed."""
    event = OutcomeEvent(kind="discovery", target="10.0.0.9", host="10.0.0.9")
    assert event.host_value == "10.0.0.9"
    assert _DIFF_KINDS is not None
