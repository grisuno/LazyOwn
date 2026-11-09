"""Chain-aware loop execution: stepwise apt_chain decisions inside the
worker, subprocess fallback, telemetry and guard inheritance."""

from __future__ import annotations

from types import SimpleNamespace

import modules.chain_loop as chain_loop
import modules.chain_facts as chain_facts
import modules.chain_registry as chain_registry
import modules.auto_registry as auto_registry
from modules.chain_loop import (
    ChainStepBlocked,
    parse_chain_invocation,
    run_chain_stepwise,
    stepwise_eligible,
)
from modules.chain_registry import Chain, ChainStep


class FakeActivity:
    def __init__(self) -> None:
        self.events: list[tuple[str, str]] = []

    def emit(self, name: str, kind: str, message: str, **kwargs) -> None:
        self.events.append((name, kind))


class FakeWorker:
    name = "worker1"
    task_id = "task1"

    def __init__(self, statuses: dict[str, str] | None = None) -> None:
        self.activity = FakeActivity()
        self.guarded: list[str] = []
        self.statuses = statuses or {}

    def _target_for(self, intent) -> str:
        return "10.0.0.1"

    def _guard_step(self, intent, command, executor, budget, intercept, retry_state):
        self.guarded.append(command)
        status = self.statuses.get(command, "ok")
        if status == "ok":
            return (f"out:{command}", "ok", "")
        return ("", status, status)


def _intent() -> SimpleNamespace:
    return SimpleNamespace(node_id=7)


def _chain() -> Chain:
    return Chain(
        name="demo",
        steps=[
            ChainStep(id="s1", run="lazy_probe one"),
            ChainStep(id="s2", run="lazy_probe two", capture="out"),
            ChainStep(id="s3", run="lazy_probe three", when='out == "out:lazy_probe two"'),
        ],
    )


def _patch_chain(monkeypatch, chain: Chain | None, name: str = "demo") -> None:
    monkeypatch.setattr(chain_registry, "get", lambda chain_name, **kw: chain if chain and chain.name == name else None)


def _routable_true(monkeypatch) -> None:
    monkeypatch.setattr(auto_registry, "is_routable_command", lambda line: True)


def test_parse_chain_invocation_splits_name_target_vars():
    """Given a full invocation, When parsed, Then name, target and vars split."""
    name, target, variables = parse_chain_invocation("apt_chain rocke 10.0.0.5 --var key=value")
    assert (name, target, variables) == ("rocke", "10.0.0.5", {"key": "value"})
    assert parse_chain_invocation("apt_chain --target 10.0.0.9")[1] == "10.0.0.9"
    assert parse_chain_invocation("apt_chain list") == ("", "", {})
    assert parse_chain_invocation("nmap -sS host") == ("", "", {})


def test_stepwise_eligible_reports_unroutable_steps():
    """Given a non-routable step, When probed, Then ineligible with reason."""
    chain = _chain()
    ok, reason = stepwise_eligible(chain, routable=lambda line: True)
    assert ok is True and reason == ""
    ok, reason = stepwise_eligible(chain, routable=lambda line: line.startswith("lazy_probe"))
    assert ok is True
    chain.steps[1].run = "custom_binary --deep"
    ok, reason = stepwise_eligible(chain, routable=lambda line: line.startswith("lazy_probe"))
    assert ok is False and "custom_binary" in reason


def test_run_chain_stepwise_routes_every_step_through_guard(monkeypatch):
    """Given an eligible chain decision, When run, Then every step passes
    the worker guard and telemetry lands in the activity log."""
    _patch_chain(monkeypatch, _chain())
    _routable_true(monkeypatch)
    spooled: list[str] = []
    monkeypatch.setattr(chain_facts, "spool_chain_outputs", lambda result, **kw: spooled.append(result.run_id) or 0)
    worker = FakeWorker()
    result = run_chain_stepwise(worker, _intent(), "apt_chain demo 10.0.0.1", None, None, None, {})
    assert result is not None
    output, status, detail = result
    assert status == "ok" and detail == ""
    assert worker.guarded == ["lazy_probe one", "lazy_probe two", "lazy_probe three"]
    kinds = [kind for _, kind in worker.activity.events]
    assert kinds.count("chain_step") == 3
    assert "chain" in kinds
    assert len(spooled) == 1


def test_run_chain_stepwise_subprocess_mode_falls_through(monkeypatch):
    """Given subprocess mode, When run, Then None keeps the legacy path."""
    _patch_chain(monkeypatch, _chain())
    monkeypatch.setattr(chain_loop, "chain_mode", lambda: "subprocess")
    worker = FakeWorker()
    assert run_chain_stepwise(worker, _intent(), "apt_chain demo", None, None, None, {}) is None
    assert worker.guarded == []


def test_run_chain_stepwise_auto_mode_skips_ineligible(monkeypatch):
    """Given auto mode and an unroutable step, When run, Then fall through."""
    _patch_chain(monkeypatch, _chain())
    monkeypatch.setattr(chain_loop, "chain_mode", lambda: "auto")
    worker = FakeWorker()
    assert run_chain_stepwise(worker, _intent(), "apt_chain demo", None, None, None, {}) is None


def test_run_chain_stepwise_forced_blocks_ineligible(monkeypatch):
    """Given forced stepwise on an ineligible chain, Then blocked loud."""
    chain = Chain(name="demo", steps=[ChainStep(id="s1", run="totally_unknown_binary --deep")])
    _patch_chain(monkeypatch, chain)
    monkeypatch.setattr(chain_loop, "chain_mode", lambda: "stepwise")
    worker = FakeWorker()
    result = run_chain_stepwise(worker, _intent(), "apt_chain demo", None, None, None, {})
    assert result == ("", "blocked", "chain stepwise ineligible")
    assert worker.guarded == []


def test_run_chain_stepwise_guard_block_aborts_chain(monkeypatch):
    """Given a guard-blocked step, When run, Then the chain aborts and the
    summary carries the abort reason with status ok for the planner."""
    chain = _chain()
    _patch_chain(monkeypatch, chain)
    _routable_true(monkeypatch)
    worker = FakeWorker(statuses={"lazy_probe two": "blocked"})
    result = run_chain_stepwise(worker, _intent(), "apt_chain demo", None, None, None, {})
    assert result is not None
    output, status, _ = result
    assert status == "ok"
    assert "aborted" in output and "blocked" in output
    assert worker.guarded == ["lazy_probe one", "lazy_probe two"]


def test_run_chain_stepwise_unknown_chain_falls_through(monkeypatch):
    """Given an unknown chain name, When run, Then None (CLI reports it)."""
    monkeypatch.setattr(chain_registry, "get", lambda chain_name, **kw: None)
    worker = FakeWorker()
    assert run_chain_stepwise(worker, _intent(), "apt_chain ghost", None, None, None, {}) is None


def test_run_chain_stepwise_nesting_limit_blocks(monkeypatch):
    """Given the nesting depth exhausted, When run, Then blocked."""
    chain_loop._DEPTH.count = chain_loop._MAX_CHAIN_NESTING
    try:
        worker = FakeWorker()
        result = run_chain_stepwise(worker, _intent(), "apt_chain demo", None, None, None, {})
        assert result == ("", "blocked", "chain nesting limit")
    finally:
        chain_loop._DEPTH.count = 0


def test_chain_step_blocked_carries_status_and_detail():
    """Given a blocked guard verdict, When raised, Then status survives."""
    error = ChainStepBlocked("skipped", "os-mismatch")
    assert error.status == "skipped" and error.detail == "os-mismatch"
    assert "os-mismatch" in str(error)


def test_run_chain_stepwise_worker_target_used_when_unset(monkeypatch):
    """Given no target on the line, When run, Then the worker target wins."""
    _patch_chain(monkeypatch, _chain())
    _routable_true(monkeypatch)
    seen_tokens: dict[str, str] = {}

    real_runner = chain_loop._build_runner

    def spy_runner(chain, guarded, tokens, total_timeout, run_id, worker, intent):
        seen_tokens.update(tokens)
        return real_runner(chain, guarded, tokens, total_timeout, run_id, worker, intent)

    monkeypatch.setattr(chain_loop, "_build_runner", spy_runner)
    worker = FakeWorker()
    run_chain_stepwise(worker, _intent(), "apt_chain demo", None, None, None, {})
    assert seen_tokens["target"] == "10.0.0.1"
    assert seen_tokens["task_id"] == "task1"
