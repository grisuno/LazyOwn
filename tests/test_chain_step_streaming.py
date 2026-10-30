"""Chain step streaming contract: chain_step events reach the bus per step.

Every scenario states Given, When, Then. Runner scenarios use an injected
executor and monkeypatched store redirections; no network and no shell.
"""

from __future__ import annotations

import json
from pathlib import Path

from modules.chain_registry import Chain, ChainStep
from modules.chain_runner import ChainRunner


def _chain(steps: list[ChainStep], **kwargs) -> Chain:
    """Build a demo chain for a runner scenario."""
    return Chain(name="demo", defaults={"target": "127.0.0.1"}, steps=steps, **kwargs)


def _capture_events(monkeypatch) -> list[dict]:
    """Replace the bus record path with a capture list of event dicts."""
    captured: list[dict] = []

    def fake_record(event, sinks=None):
        captured.append(event.to_dict())
        return {}

    import modules.outcome_bus as outcome_bus_module

    monkeypatch.setattr(outcome_bus_module, "record", fake_record, raising=False)
    return captured


def _chain_steps_for(captured) -> list[dict]:
    """Return the captured chain_step rows from a capture list."""
    return [row for row in captured if row["kind"] == "chain_step"]


def test_dry_run_never_publishes(monkeypatch):
    """Given a dry run, When the chain resolves, Then no chain_step event is published."""
    captured = _capture_events(monkeypatch)
    chain = _chain([ChainStep(id="probe", run="probe {target}")])
    ChainRunner(chain, tokens={"task_id": "t0001"}, dry_run=True).run()
    assert captured == []


def test_every_executed_step_publishes_one_event(monkeypatch):
    """Given a two-step chain, When run, Then every step publishes with run metadata."""

    captured = _capture_events(monkeypatch)

    def executor(command: str) -> str:
        if command.startswith("probe"):
            return "probe fine"
        return "report fine"

    chain = _chain(
        [
            ChainStep(id="probe", run="probe {target}"),
            ChainStep(id="report_step", run="report {target}"),
        ]
    )
    runner = ChainRunner(chain, tokens={"task_id": "t0001", "target": "10.0.0.9"}, executor=executor)
    runner.run()
    run_id = runner.run_id
    steps = _chain_steps_for(captured)
    assert len(steps) == 2
    assert steps[0]["task_id"] == "t0001"
    assert steps[0]["metadata"]["step_id"] == "probe"
    assert steps[0]["metadata"]["status"] == "ok"
    assert steps[0]["metadata"]["steer"] is False
    assert set(steps[0]["sinks"]) == {"chain_feed", "event_bus"}
    assert f"[{run_id}]" in steps[0]["title"]
    assert steps[0]["success"] is True
    assert steps[0]["severity"] == "low"
    assert steps[1]["success"] is True


def _failing_executor(prefixes: set[str]):
    """Return an executor that raises for the given command prefixes."""

    def execute(command: str) -> str:
        name = command.split()[0] if command else ""
        if name in prefixes:
            raise RuntimeError("connection refused")
        return "ok"

    return execute


def test_unhandled_failure_sets_steer_but_handled_failure_does_not(monkeypatch):
    """Given failed steps, When the chain cannot/can resolve them, Then steer flags differ."""
    captured = _capture_events(monkeypatch)
    chain = _chain(
        [
            ChainStep(id="handled", run="handled {target}", continue_on_error=True),
            ChainStep(id="unhandled", run="unhandled {target}"),
        ]
    )
    runner = ChainRunner(chain, tokens={"task_id": "t0001"}, executor=_failing_executor({"handled", "unhandled"}), retry_backoff=0)
    result = runner.run()
    assert result.ok is False
    rows = {row["metadata"]["step_id"]: row for row in _chain_steps_for(captured)}
    assert rows["handled"]["metadata"]["steer"] is False
    assert rows["handled"]["success"] is False
    assert rows["handled"]["severity"] == "medium"
    assert rows["unhandled"]["metadata"]["steer"] is True


def test_alternatives_do_not_resolve_failures(monkeypatch):
    """Given a failing step with benign alternatives, When the chain aborts, Then steer reflects it."""
    captured = _capture_events(monkeypatch)
    chain = _chain(
        [
            ChainStep(id="alt", run="alt {target}", benign_alternatives=["alt_b"]),
            ChainStep(id="routed", run="routed {target}", on_fail="recovery"),
            ChainStep(id="recovery", run="recovery {target}"),
        ]
    )
    ChainRunner(chain, tokens={"task_id": "t0001"}, executor=_failing_executor({"alt", "routed"}), retry_backoff=0).run()
    flags = {row["metadata"]["step_id"]: row["metadata"]["steer"] for row in _chain_steps_for(captured)}
    assert flags["alt"] is True
    assert "routed" not in flags


def test_denied_never_steers(monkeypatch):
    """Given a confirm step the operator denies, When published, Then steer stays false."""
    captured = _capture_events(monkeypatch)
    chain = _chain([ChainStep(id="gate", run="gate {target}", confirm=True)])
    result = ChainRunner(
        chain, tokens={"task_id": "t0001"}, approver=lambda step_id, command: False, retry_backoff=0
    ).run()
    assert result.ok is False
    flags = {row["metadata"]["step_id"]: row["metadata"]["steer"] for row in _chain_steps_for(captured)}
    statuses = {row["metadata"]["step_id"]: row["metadata"]["status"] for row in _chain_steps_for(captured)}
    assert flags["gate"] is False
    assert statuses["gate"] == "denied"


def test_publication_failure_never_blocks_the_chain(monkeypatch):
    """Given a bus outage, When a step fails to publish, Then the chain still runs."""
    import modules.outcome_bus as outcome_bus_module

    def boom(event, sinks=None):
        raise RuntimeError("bus down")

    monkeypatch.setattr(outcome_bus_module, "record", boom, raising=False)
    chain = _chain([ChainStep(id="probe", run="probe {target}")])
    result = ChainRunner(
        chain,
        tokens={"task_id": "t0001"},
        executor=lambda command: "ok",
        retry_backoff=0,
    ).run()
    assert result.ok is True


def _capture_with_sinks(monkeypatch) -> list[tuple[dict, list]]:
    """Capture each published event alongside the explicit sink list."""
    captured: list[tuple[dict, list]] = []

    def fake_record(event, sinks=None):
        captured.append((event.to_dict(), list(sinks or [])))
        return {}

    import modules.outcome_bus as outcome_bus_module

    monkeypatch.setattr(outcome_bus_module, "record", fake_record, raising=False)
    return captured


def test_successful_step_promotes_declared_state_sinks(monkeypatch):
    """Given a step declaring world_model, When it succeeds, Then a proven chain event fans out there."""
    captured = _capture_with_sinks(monkeypatch)
    chain = _chain([ChainStep(id="loot", run="loot {target}", sinks=["world_model", "killchain"])])
    ChainRunner(
        chain,
        tokens={"task_id": "t0001", "target": "10.0.0.9"},
        executor=lambda command: "creds captured",
        retry_backoff=0,
    ).run()
    promoted = [(row, sinks) for row, sinks in captured if row["kind"] == "chain"]
    assert len(promoted) == 1
    row, sinks = promoted[0]
    assert row["success"] is True
    assert row["host"] == "10.0.0.9"
    assert row["metadata"]["step_id"] == "loot"
    assert sinks == ["world_model", "killchain"]
    assert set(sinks).isdisjoint({"chain_feed", "event_bus"})


def test_failed_step_never_promotes_state_sinks(monkeypatch):
    """Given a step declaring state sinks, When it fails, Then only the streaming event fires."""
    captured = _capture_with_sinks(monkeypatch)
    chain = _chain([ChainStep(id="loot", run="loot {target}", sinks=["world_model"])])
    ChainRunner(
        chain,
        tokens={"task_id": "t0001", "target": "10.0.0.9"},
        executor=_failing_executor({"loot"}),
        retry_backoff=0,
    ).run()
    assert [row for row, _ in captured if row["kind"] == "chain"] == []


def test_step_without_declared_sinks_does_not_promote(monkeypatch):
    """Given a step with no sinks, When it succeeds, Then no proven chain event is published."""
    captured = _capture_with_sinks(monkeypatch)
    chain = _chain([ChainStep(id="probe", run="probe {target}")])
    ChainRunner(
        chain,
        tokens={"task_id": "t0001", "target": "10.0.0.9"},
        executor=lambda command: "ok",
        retry_backoff=0,
    ).run()
    assert [row for row, _ in captured if row["kind"] == "chain"] == []


def test_event_bus_receives_chain_step_for_dashboard(tmp_path: Path, monkeypatch):
    """Given a real bus, When a chain step publishes, Then the event lands on the audit ledger."""
    import modules.outcome_bus as outcome_bus_module

    ledger = tmp_path / "outcomes.jsonl"
    bus = outcome_bus_module.OutcomeBus(ledger_path=ledger, sink_map={})
    monkeypatch.setattr(outcome_bus_module, "_BUS", bus, raising=False)

    chain = _chain([ChainStep(id="probe", run="probe {target}")])
    outcome_bus_module.reset_bus()
    try:
        ChainRunner(
            chain,
            tokens={"task_id": "t0001", "target": "10.0.0.9"},
            executor=lambda command: "probe fine",
            retry_backoff=0,
        ).run()
        rows = [json.loads(line) for line in ledger.read_text(encoding="utf-8").splitlines()]
    finally:
        outcome_bus_module.reset_bus()
    chain_steps = [row for row in rows if row["event"]["kind"] == "chain_step"]
    assert len(chain_steps) == 1
    assert chain_steps[0]["event"]["metadata"]["chain"] == "demo"
    assert set(chain_steps[0]["sinks"]) == {"chain_feed", "event_bus"}
