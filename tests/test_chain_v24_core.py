"""Chain v2.4 BDD contract: branching, verify, captures, gates, checkpoints.

Every scenario states Given, When, Then. These scenarios cover the
adaptive layer the v2.4 upgrade added on top of the v2 runner: regex and
JSON captures, post-step verification, expect_exit, on_fail/on_success
branching, confirm gates, total timeout, loop guards, checkpoints and
the replanner.
"""

from __future__ import annotations

import os
import time

from modules.chain_registry import Chain, ChainStep, validate_chain
from modules.chain_runner import ChainRunner, ReplanContext
from modules.chain_state import checkpoint_dir, load_checkpoint, new_run_id, write_checkpoint


def _chain(steps: list[ChainStep], **kwargs) -> Chain:
    """Build a chain for a runner scenario."""
    return Chain(name="demo", defaults={"target": "127.0.0.1"}, steps=steps, **kwargs)


def test_runner_captures_regex_named_groups_for_later_steps():
    """Given a regex capture, When the next step renders, Then variables bind."""
    seen: list[str] = []

    def executor(command: str) -> str:
        seen.append(command)
        if command.startswith("probe"):
            return "listening on port 4455"
        return "done 4455"

    chain = _chain(
        [
            ChainStep(id="scan", run="probe", capture_regex=r"port (?P<port>\d+)"),
            ChainStep(id="use", run="echo {port}", expect="4455"),
        ]
    )
    result = ChainRunner(chain, executor=executor, retry_backoff=0).run()
    assert result.ok is True
    assert result.steps[0].captured == "4455"
    assert result.variables["port"] == "4455"
    assert seen[1] == "echo 4455"


def test_runner_captures_json_fields_from_output():
    """Given JSON output, When keys are declared, Then each key becomes a variable."""

    def executor(command: str) -> str:
        if command.startswith("probe"):
            return 'notice {"user": "svc-acc", "path": "/var/www"}'
        return "ok"

    chain = _chain(
        [
            ChainStep(id="probe", run="probe", capture_json="user,path"),
            ChainStep(id="use", run="echo {user}", when='user == "svc-acc"'),
        ]
    )
    result = ChainRunner(chain, executor=executor, retry_backoff=0).run()
    assert result.ok is True
    assert result.variables["user"] == "svc-acc"
    assert result.variables["path"] == "/var/www"


def test_runner_verify_fails_a_step_when_probe_fails():
    """Given verify, When the probe fails, Then the step reports verify failure."""
    calls: list[str] = []

    def executor(command: str) -> str:
        calls.append(command)
        if command == "probe":
            return "done"
        raise RuntimeError("verify boom")

    chain = _chain([ChainStep(id="step", run="probe", verify="echo verified")])
    result = ChainRunner(chain, executor=executor, retry_backoff=0).run()
    assert result.steps[0].status == "failed"
    assert "verify failed" in result.steps[0].reason
    assert result.aborted is True


def test_runner_verify_may_consume_capture():
    """Given capture then verify, When verify renders, Then it sees the capture."""
    call_log: list[str] = []

    def executor(command: str) -> str:
        call_log.append(command)
        if command == "probe":
            return "token 777"
        return "verified"

    chain = _chain(
        [
            ChainStep(id="get", run="probe", capture="token", capture_regex=r"token (\d+)"),
            ChainStep(id="check", run="probe", verify="echo {token}"),
        ]
    )
    result = ChainRunner(chain, executor=executor, retry_backoff=0).run()
    assert result.ok is True
    assert "echo 777" in call_log


def test_runner_expect_exit_accepts_configured_codes_only():
    """Given expect_exit, When the process exits with a listed code, Then ok."""
    chain = _chain([ChainStep(id="exits", run="exit 3", expect_exit=[3, 7])])
    result = ChainRunner(chain, shell=object(), retry_backoff=0).run()
    assert result.steps[0].status == "ok"


def test_runner_on_fail_routes_to_fallback_step():
    """Given a failing step with on_fail, When it fails, Then the fallback runs."""
    calls: list[str] = []

    def executor(command: str) -> str:
        calls.append(command)
        if command == "fail":
            raise RuntimeError("boom")
        return "ok"

    chain = _chain(
        [
            ChainStep(id="primary", run="fail", on_fail="fallback"),
            ChainStep(id="skipped", run="echo skipped"),
            ChainStep(id="fallback", run="echo fallback"),
        ]
    )
    result = ChainRunner(chain, executor=executor, retry_backoff=0).run()
    assert result.branches == ["primary --fail--> fallback"]
    assert result.steps[-1].id == "fallback"
    assert result.steps[-1].status == "ok"
    assert calls == ["fail", "echo fallback"]
    assert result.ok is False


def test_runner_on_success_reorders_execution():
    """Given on_success, When the step succeeds, Then the jump target runs next."""
    calls: list[str] = []

    def executor(command: str) -> str:
        calls.append(command)
        return "ok"

    chain = _chain(
        [
            ChainStep(id="first", run="one", on_success="third"),
            ChainStep(id="second", run="two"),
            ChainStep(id="third", run="three"),
        ]
    )
    result = ChainRunner(chain, executor=executor, retry_backoff=0).run()
    assert calls == ["one", "three"]
    assert [step.id for step in result.steps] == ["first", "third"]
    assert result.branches == ["first --success--> third"]
    assert result.ok is True


def test_runner_loop_guard_blocks_infinite_branching():
    """Given a branch cycle, When steps translate, Then the guard aborts."""
    calls: list[str] = []

    def executor(command: str) -> str:
        calls.append(command)
        return "ok"

    chain = _chain(
        [
            ChainStep(id="a", run="a", on_success="b"),
            ChainStep(id="b", run="b", on_success="a"),
        ]
    )
    result = ChainRunner(chain, executor=executor, retry_backoff=0).run()
    assert result.aborted is True
    assert "loop guard" in result.reason
    assert len(calls) <= 6


def test_runner_total_timeout_stops_pending_steps():
    """Given a chain wall clock, When it elapses, Then remaining steps skip."""
    sleeps = [0.2, 0.2, 0.2, 0.2, 0.2]

    def executor(command: str) -> str:
        time.sleep(sleeps.pop(0) if sleeps else 0.01)
        return "ok"

    chain = _chain([ChainStep(id=f"step{index}", run=f"run{index}") for index in range(5)])
    result = ChainRunner(chain, executor=executor, retry_backoff=0, total_timeout=0.4).run()
    assert result.aborted is True
    assert "total timeout" in result.reason
    assert any(outcome.reason == "total timeout" for outcome in result.steps)


def test_runner_confirm_requires_approver_failure_closed():
    """Given a confirm step without approver, When it resolves, Then it denies."""
    chain = _chain([ChainStep(id="guarded", run="echo guarded", confirm=True)])
    result = ChainRunner(chain, executor=lambda command: "ok", retry_backoff=0).run()
    assert result.steps[0].status == "denied"
    assert result.aborted is True


def test_runner_confirm_approval_grants_or_denies():
    """Given an approver, When it says no, Then the step denies and aborts."""
    chain = _chain(
        [
            ChainStep(id="guarded", run="echo guarded", confirm=True),
            ChainStep(id="after", run="echo after"),
        ]
    )
    denied = ChainRunner(chain, executor=lambda command: "ok", retry_backoff=0, approver=lambda sid, cmd: False).run()
    assert denied.steps[0].status == "denied"
    assert not any(step.id == "after" and step.status == "ok" for step in denied.steps)

    granted_calls: list[str] = []

    def record(command: str) -> str:
        granted_calls.append(command)
        return "ok"

    granted = ChainRunner(chain, executor=record, retry_backoff=0, approver=lambda sid, cmd: True).run()
    assert "echo guarded" in granted_calls
    assert granted.steps[0].status == "ok"


def test_runner_checkpoints_enable_resume(tmp_path, monkeypatch):
    """Given an interrupted run, When resuming, Then done steps skip and state flows."""
    monkeypatch.chdir(tmp_path)
    probes: list[str] = []

    def executor(command: str) -> str:
        probes.append(command)
        if command == "fail":
            raise RuntimeError("interrupted")
        return "ok"

    chain = _chain(
        [
            ChainStep(id="first", run="probe", capture="token"),
            ChainStep(id="second", run="fail"),
            ChainStep(id="third", run="echo {token}"),
        ]
    )
    directory = checkpoint_dir()
    first = ChainRunner(chain, executor=executor, retry_backoff=0, checkpoint_dir=directory, run_id="resume_demo").run()
    assert first.aborted is True
    state = load_checkpoint(directory, "resume_demo")
    assert state is not None and state["steps"][0]["status"] == "ok"

    resumed_probes: list[str] = []

    def resumed_executor(command: str) -> str:
        resumed_probes.append(command)
        return "recovered"

    second = ChainRunner(
        chain,
        executor=resumed_executor,
        retry_backoff=0,
        checkpoint_dir=directory,
        run_id="resume_demo",
        resume_state=state,
    ).run()
    assert second.ok is True
    assert not any(step.id == "first" and step.status == "ok" for step in second.steps)
    assert any(outcome.reason == "resumed (already completed)" for outcome in second.steps)
    assert "probe" not in resumed_probes
    assert "fail" in resumed_probes


def test_runner_replanner_sets_vars_and_inserts_steps():
    """Given a replanner, When step1 succeeds, Then deltas apply with caps."""
    seen: list[str] = []

    def executor(command: str) -> str:
        seen.append(command)
        return "ok"

    def replanner(context: ReplanContext) -> None:
        context.set_var("mode", "deep")
        context.insert_step(ChainStep(id="inserted", run="inserted", continue_on_error=False))
        context.insert_step(ChainStep(id="extra2", run="extra2"))
        context.insert_step(ChainStep(id="extra3", run="extra3"))
        context.insert_step(ChainStep(id="extra4", run="never"))

    chain = _chain(
        [
            ChainStep(id="start", run="start"),
            ChainStep(id="end", run="end {mode}"),
        ]
    )
    result = ChainRunner(chain, executor=executor, retry_backoff=0, replanner=replanner).run()
    runs = [outcome.run for outcome in result.steps]
    assert result.steps[0].status == "ok"
    assert runs[0] == "start"
    assert "inserted" in runs and any("end deep" in item for item in runs)
    assert not any("never" in item for item in runs)
    inserted_count = sum(1 for item in runs if item.startswith(("inserted", "extra")))
    assert inserted_count == 3


def test_runner_replanner_skip_rest_ends_early():
    """Given skip_rest, When invoked, Then remaining steps mark skipped."""

    def executor(command: str) -> str:
        return "ok"

    def replanner(context: ReplanContext) -> None:
        context.skip_rest()

    chain = _chain(
        [
            ChainStep(id="first", run="first"),
            ChainStep(id="second", run="second"),
        ]
    )
    result = ChainRunner(chain, executor=executor, retry_backoff=0, replanner=replanner).run()
    assert result.ok is True
    assert result.steps[-1].reason.startswith("skip_rest")


def test_checkpoint_state_round_trip(tmp_path):
    """Given checkpoints on disk, When writing then loading, Then state survives."""
    run_id = new_run_id("demo")
    assert run_id.endswith(str(os.getpid()))
    path = write_checkpoint(tmp_path, {"run_id": run_id, "chain": "demo", "state": "running", "steps": []})
    assert path.is_file()
    loaded = load_checkpoint(tmp_path, run_id)
    assert loaded and loaded["chain"] == "demo"
    assert load_checkpoint(tmp_path, "missing_run") is None


def test_schema_v24_accepts_and_rejects_new_fields():
    """Given v2.4 fields, When validating, Then valid pass and bad values fail."""
    valid = {
        "name": "demo",
        "version": 2,
        "total_timeout": 900,
        "steps": [
            {
                "id": "probe",
                "run": "probe",
                "capture_regex": r"port (?P<port>\d+)",
                "capture_json": "user,path",
                "verify": "echo {port}",
                "expect_exit": [3, 7],
                "on_fail": "fallback",
                "on_success": "final",
                "confirm": True,
            },
            {"id": "fallback", "run": "echo fallback"},
            {"id": "final", "run": "echo final", "on_fail": "fallback"},
        ],
    }
    assert validate_chain(valid, filename="demo") == []
    bad = {
        "name": "demo",
        "total_timeout": 999999,
        "steps": [
            {
                "id": "probe",
                "run": "probe",
                "capture_regex": "(broken[",
                "capture_json": "a" * 200,
                "verify": "x" * 700,
                "expect_exit": [999],
                "on_fail": "missing_id",
                "confirm": "yes",
            },
        ],
    }
    errors = validate_chain(bad, filename="demo")
    assert any("total_timeout" in error for error in errors)
    assert any("capture_regex" in error for error in errors)
    assert any("capture_json" in error for error in errors)
    assert any("verify" in error for error in errors)
    assert any("expect_exit" in error for error in errors)
    assert any("on_fail" in error for error in errors)
    assert any("confirm" in error for error in errors)


def test_validated_shipped_chains_still_load():
    """Given the shipped registry, When loading, Then every file stays valid."""
    from modules.chain_registry import load_all, scan_all

    rows = scan_all()
    chains = load_all()
    assert len(rows) >= 60
    assert not [row for row in rows if not row["valid"]]
    base = chains.get("apt_chain")
    assert base is not None and len(base.steps) == 12 and base.total_timeout == 0
