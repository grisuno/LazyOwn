"""Chain-feed sink contract: live step visibility and unhandled-failure steering.

Every scenario states Given, When, Then. The sink only reacts to
``chain_step`` events bound to a valid task id; anything else is out of
scope and leaves loop state untouched.
"""

from __future__ import annotations

import json
from pathlib import Path

from modules.outcome_bus import OutcomeEvent


def _store_dir(monkeypatch, tmp_path: Path) -> Path:
    """Point the loop store at a temporary directory."""
    import modules.lazy_loop as core

    store = tmp_path / "lazy"
    store.mkdir(parents=True, exist_ok=True)
    monkeypatch.setattr(core, "STORE_DIR", store, raising=False)
    monkeypatch.setattr(core, "_store_path", lambda name: store / name, raising=False)
    return store


def _step_event(steer: bool = False) -> OutcomeEvent:
    """Build one representative chain_step event."""
    return OutcomeEvent(
        kind="chain_step",
        task_id="t0042",
        target="10.0.0.9",
        title=f"chain demo step probe [run1]{' steer' if steer else ''}",
        description="connection refused",
        severity="medium",
        success=False,
        source="demo",
        command="apt_probe 10.0.0.9",
        sinks=["chain_feed", "event_bus"],
        metadata={"run_id": "run1", "chain": "demo", "step_id": "probe", "status": "failed", "steer": steer},
    )


def test_ignores_out_of_scope_events(tmp_path: Path):
    """Given a finding event or a chain_step without task, When applied, Then nothing is fed."""
    from modules.sinks.chain_feed import apply

    no_task = _step_event()
    no_task.task_id = ""
    assert apply(OutcomeEvent(kind="finding", target="10.0.0.9", task_id="t0042")) is False
    assert apply(no_task) is False


def test_rejects_unsafe_task_ids(tmp_path: Path):
    """Given a path-traversal task id, When applied, Then the event is dropped."""
    from modules.sinks.chain_feed import apply

    event = _step_event()
    event.task_id = "../../evil"
    assert apply(event) is False


def test_trace_record_wakes_and_appends(monkeypatch, tmp_path: Path):
    """Given a handled chain step, When applied, Then exactly one activity record lands."""
    from modules.sinks.chain_feed import apply

    store = _store_dir(monkeypatch, tmp_path)
    assert apply(_step_event(steer=False)) is True
    rows = [json.loads(line) for line in (store / "activity_t0042.jsonl").read_text(encoding="utf-8").splitlines()]
    assert len(rows) == 1
    record = rows[0]
    assert record["kind"] == "chain-step" and record["worker"] == "chain-demo"
    assert record["task"] == "t0042" and "probe" in record["text"]
    assert not (store / "exp_t0042.json").exists()


def test_unhandled_failure_plants_one_pending_hint(monkeypatch, tmp_path: Path):
    """Given a steer event, When applied, Then a pending hint lands and re-application dedupes."""
    from modules.sinks.chain_feed import apply

    store = _store_dir(monkeypatch, tmp_path)
    assert apply(_step_event(steer=True)) is True
    assert apply(_step_event(steer=True)) is True
    graph_store = store / "exp_t0042.json"
    assert graph_store.exists()
    rows = [json.loads(line) for line in (store / "activity_t0042.jsonl").read_text(encoding="utf-8").splitlines()]
    assert len(rows) == 2
    data = json.loads(graph_store.read_text(encoding="utf-8"))
    hints = [node for node in data.get("nodes", []) if node.get("kind") == "hint"]
    assert len(hints) == 1
    assert hints[0]["state"] == "pending"
    assert hints[0]["meta"]["steer_chain"] == "run1:probe"


def test_steer_hint_dedupe_is_per_run(monkeypatch, tmp_path: Path):
    """Given the same failing step across two runs, When applied, Then each run steers once."""
    from modules.sinks.chain_feed import apply

    store = _store_dir(monkeypatch, tmp_path)
    assert apply(_step_event(steer=True)) is True

    replay = _step_event(steer=True)
    replay.metadata = {"run_id": "run2", "chain": "demo", "step_id": "probe", "status": "failed", "steer": True}
    assert apply(replay) is True

    data = json.loads((store / "exp_t0042.json").read_text(encoding="utf-8"))
    hints = [node for node in data.get("nodes", []) if node.get("kind") == "hint"]
    assert len(hints) == 2


def test_chain_step_activity_maps_to_planner_trigger(monkeypatch, tmp_path: Path):
    """Given a fed chain_step, When the loop drains, Then the planner receives a chain_step trigger."""
    from modules.sinks.chain_feed import apply

    _store_dir(monkeypatch, tmp_path)
    import modules.lazy_loop as loop
    from modules.lazy_engine import LazyEngine

    engine = LazyEngine()
    task_id = engine.create_task("gain initial access on 127.0.0.1")["task_id"]
    event = _step_event(steer=True)
    event.task_id = task_id
    assert apply(event) is True
    triggers = engine._drain_triggers(task_id, loop.ExplorationGraph(task_id))
    matched = [t for t in triggers if t.get("kind") == "chain_step"]
    assert matched and "probe" in matched[0]["text"]
