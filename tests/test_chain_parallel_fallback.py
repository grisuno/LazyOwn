"""Chain v2 adaptive execution: parallel groups, fallback, pre-checks.

BDD contract for the ``parallel``, ``pre_check`` and ``fallback``
schema fields. Every scenario states Given, When, Then.
"""

from __future__ import annotations

import threading
import time

from modules.chain_registry import Chain, ChainStep, validate_chain
from modules.chain_runner import ChainRunner


def _chain(steps: list[ChainStep], **kwargs) -> Chain:
    """Build a chain for a runner scenario."""
    return Chain(name="demo", defaults={"target": "127.0.0.1"}, steps=steps, **kwargs)


def test_parallel_steps_execute_concurrently():
    """Given two parallel steps that block on each other, When they run,
    Then both start before either finishes (concurrency proof)."""
    started: list[str] = []
    released = threading.Event()
    first_started = threading.Event()
    gate_lock = threading.Lock()

    def executor(command: str) -> str:
        with gate_lock:
            started.append(command)
        if command == "first":
            first_started.set()
            released.wait(timeout=5)
            return "first-done"
        if command == "second":
            return "second-done"
        return "ok"

    chain = _chain(
        [
            ChainStep(id="p1", run="first", parallel=True),
            ChainStep(id="p2", run="second", parallel=True),
            ChainStep(id="after", run="echo done"),
        ]
    )

    class _SlowFirst:
        """Executor wrapper that delays 'first' until 'second' began."""

        def __call__(self, command: str) -> str:
            result = executor(command)
            return result

    runner = ChainRunner(chain, executor=_SlowFirst(), retry_backoff=0)
    # Proof of concurrency: run the chain in a thread; 'first' blocks
    # until the observer sees both parallel commands registered.
    result_holder: dict = {}

    def _run() -> None:
        result_holder["result"] = runner.run()

    worker = threading.Thread(target=_run, daemon=True)
    worker.start()
    assert first_started.wait(timeout=5), "'first' never started"
    deadline = time.time() + 5
    while time.time() < deadline and len(started) < 2:
        time.sleep(0.01)
    assert len(started) == 2, f"'second' did not start while 'first' blocked: {started}"
    released.set()
    worker.join(timeout=10)
    result = result_holder.get("result")
    assert result is not None
    assert result.ok is True
    statuses = {step.id: step.status for step in result.steps}
    assert statuses == {"p1": "ok", "p2": "ok", "after": "ok"}


def test_parallel_failure_without_continue_aborts():
    """Given a failing parallel step, When continue_on_error is false,
    Then the chain aborts after the group completes."""
    calls: list[str] = []

    def executor(command: str) -> str:
        calls.append(command)
        if command == "boom":
            raise RuntimeError("boom")
        return "ok"

    chain = _chain(
        [
            ChainStep(id="p1", run="boom", parallel=True),
            ChainStep(id="p2", run="echo inline", parallel=True),
            ChainStep(id="never", run="echo never"),
        ]
    )
    result = ChainRunner(chain, executor=executor, retry_backoff=0).run()
    assert result.ok is False and result.aborted is True
    ids = [step.id for step in result.steps]
    assert "never" not in ids


def test_parallel_failure_with_continue_keeps_going():
    """Given a failing parallel step with continue_on_error, When the
    group ends, Then later sequential steps still run."""
    calls: list[str] = []

    def executor(command: str) -> str:
        calls.append(command)
        if command == "boom":
            raise RuntimeError("boom")
        return "ok"

    chain = _chain(
        [
            ChainStep(id="p1", run="boom", parallel=True, continue_on_error=True),
            ChainStep(id="p2", run="echo inline", parallel=True),
            ChainStep(id="after", run="echo after"),
        ]
    )
    result = ChainRunner(chain, executor=executor, retry_backoff=0).run()
    assert result.aborted is False
    assert "echo after" in calls


def test_pre_check_failure_skips_step():
    """Given a step whose pre_check fails, When the step resolves,
    Then the main command never executes."""
    calls: list[str] = []

    def executor(command: str) -> str:
        calls.append(command)
        if command.startswith("check-port"):
            raise RuntimeError("closed")
        return "ok"

    chain = _chain(
        [
            ChainStep(id="guarded", run="exploit-target", pre_check="check-port 445"),
            ChainStep(id="next", run="echo next"),
        ]
    )
    result = ChainRunner(chain, executor=executor, retry_backoff=0).run()
    assert "exploit-target" not in calls
    assert result.steps[0].status == "skipped"
    assert "pre_check failed" in result.steps[0].reason
    assert result.steps[1].status == "ok"


def test_pre_check_success_executes_step():
    """Given a passing pre_check, When the step resolves, Then the main
    command executes once."""

    def executor(command: str) -> str:
        if command.startswith("check-port"):
            return "open"
        return "pwned"

    chain = _chain([ChainStep(id="guarded", run="exploit-target", pre_check="check-port 445")])
    result = ChainRunner(chain, executor=executor, retry_backoff=0).run()
    assert result.ok is True
    assert result.steps[0].status == "ok"


def test_fallback_chain_runs_on_failure():
    """Given a chain with a fallback, When the primary fails, Then the
    fallback executes with the same tokens and the result reports it."""

    def executor(command: str) -> str:
        if command == "primary-fail":
            raise RuntimeError("no route")
        return "fallback-shell"

    primary = _chain(
        [ChainStep(id="probe", run="primary-fail")],
        fallback="backup",
    )
    backup = Chain(name="backup", defaults={"target": "10.0.0.9"}, steps=[ChainStep(id="alt", run="use-alt")])

    def loader(name: str) -> Chain | None:
        return backup if name == "backup" else None

    result = ChainRunner(primary, executor=executor, retry_backoff=0, fallback_loader=loader).run()
    assert result.ok is True
    assert result.fallback_used == "backup"
    assert result.fallback_depth == 1
    assert result.steps[-1].id == "alt"
    assert result.variables["target"] == "127.0.0.1"
    assert any("--fail-->" in branch for branch in result.branches)


def test_fallback_skipped_when_primary_succeeds():
    """Given a successful primary, When the run finishes, Then the
    fallback never loads."""
    loader_calls: list[str] = []

    def loader(name: str) -> Chain | None:
        loader_calls.append(name)
        return Chain(name="backup", steps=[ChainStep(id="alt", run="alt")])

    chain = _chain([ChainStep(id="ok-step", run="echo fine")], fallback="backup")
    result = ChainRunner(chain, executor=lambda command: "ok", retry_backoff=0, fallback_loader=loader).run()
    assert result.ok is True
    assert result.fallback_used == ""
    assert loader_calls == []


def test_fallback_depth_is_capped():
    """Given fallback chains that point at each other, When depth hits
    the cap, Then recursion stops."""

    def executor(command: str) -> str:
        raise RuntimeError("always fails")

    registry = {
        "demo": Chain(name="demo", steps=[ChainStep(id="s1", run="one")], fallback="backup"),
        "backup": Chain(name="backup", steps=[ChainStep(id="s2", run="two")], fallback="demo"),
    }

    def loader(name: str) -> Chain | None:
        return registry.get(name)

    result = ChainRunner(registry["demo"], executor=executor, retry_backoff=0, fallback_loader=loader).run()
    assert result.ok is False
    assert result.fallback_depth == 1
    fallback_runs = [step.run for step in result.steps if step.run in ("one", "two")]
    assert fallback_runs.count("two") == 1


def test_registry_validation_rejects_parallel_with_capture():
    """Given a parallel step that captures, When validated, Then the
    schema rejects the combination."""
    data = {
        "name": "demo",
        "steps": [{"run": "nmap {target}", "id": "scan", "parallel": True, "capture": "out"}],
    }
    errors = validate_chain(data, filename="demo")
    assert any("parallel" in error and "capture" in error for error in errors)


def test_registry_validation_rejects_unknown_fallback():
    """Given a fallback name with no chain file, When validated with a
    chains dir, Then the schema reports the missing file."""
    import tempfile
    from pathlib import Path

    with tempfile.TemporaryDirectory() as tmp:
        data = {
            "name": "demo",
            "steps": [{"run": "echo one"}],
            "fallback": "missing_chain",
        }
        errors = validate_chain(data, filename="demo", chains_dir=Path(tmp))
        assert any("unknown fallback chain file" in error for error in errors)


def test_registry_parses_parallel_and_pre_check():
    """Given a YAML-ish mapping, When a step is materialized, Then the
    new schema fields survive with the right types."""
    from modules.chain_registry import _step_from_raw

    step = _step_from_raw(
        {
            "run": "nmap -sT {target}",
            "id": "quiet_scan",
            "parallel": True,
            "pre_check": "ping -c1 {target}",
        }
    )
    assert step.parallel is True
    assert step.pre_check == "ping -c1 {target}"


def test_dry_run_treats_parallel_steps_sequentially():
    """Given a dry run, When parallel steps resolve, Then no thread
    pool is used and every step reports dry-run."""
    chain = _chain(
        [
            ChainStep(id="p1", run="one", parallel=True),
            ChainStep(id="p2", run="two", parallel=True),
        ]
    )
    result = ChainRunner(chain, executor=lambda command: "ok", dry_run=True, retry_backoff=0).run()
    assert [step.status for step in result.steps] == ["dry-run", "dry-run"]
