"""Chain v2 BDD contract: safe conditions, retries, capture and error policy.

Every scenario states Given, When, Then. The runner is the only executor
for YAML chains; the registry remains the resolver and validator.
"""

from __future__ import annotations

import threading
import time

from modules.chain_registry import Chain, ChainStep, evaluate_when, validate_chain
from modules.chain_runner import ChainRunner


def _chain(steps: list[ChainStep], **kwargs) -> Chain:
    """Build a chain for a runner scenario."""
    return Chain(name="demo", defaults={"target": "127.0.0.1"}, steps=steps, **kwargs)


def test_when_evaluator_is_safe_and_expressive():
    """Given string variables, When conditions evaluate, Then only safe grammar works."""
    values = {"phase": "recon", "skip": "false", "count": "2"}
    assert evaluate_when('phase == "recon" and skip != "true"', values) is True
    assert evaluate_when('phase == "exploit" or skip == "false"', values) is True
    assert evaluate_when('not phase == "exploit"', values) is True
    assert evaluate_when('phase in "recon exploit"', values) is True
    assert evaluate_when('count == "2" and phase == "recon"', values) is True
    assert evaluate_when("", values) is True
    assert evaluate_when('__import__("os").system("id")', values) is False
    assert evaluate_when("open('/etc/passwd')", values) is False
    assert evaluate_when("phase ==", values) is False


def test_runner_captures_output_for_later_steps():
    """Given a capture step, When the next step renders, Then it sees the captured value."""
    seen: list[str] = []

    def executor(command: str) -> str:
        seen.append(command)
        if command.startswith("echo hello"):
            return "hello"
        return "ok"

    chain = _chain(
        [
            ChainStep(id="probe", run="echo hello", capture="first"),
            ChainStep(id="use", run="echo {first}", when='first == "hello"'),
        ]
    )
    result = ChainRunner(chain, executor=executor, retry_backoff=0).run()
    assert result.ok is True and result.aborted is False
    assert result.steps[0].captured == "hello"
    assert seen == ["echo hello", "echo hello"]
    assert result.variables["first"] == "hello"


def test_runner_retries_then_succeeds():
    """Given a flaky executor, When retries remain, Then the step succeeds on the next attempt."""
    attempts = {"n": 0}

    def executor(command: str) -> str:
        attempts["n"] += 1
        if attempts["n"] < 2:
            raise RuntimeError("transient")
        return "recovered"

    chain = _chain([ChainStep(id="flaky", run="probe", retries=1)])
    result = ChainRunner(chain, executor=executor, retry_backoff=0).run()
    assert result.ok is True
    assert result.steps[0].attempts == 2
    assert result.steps[0].output == "recovered"


def test_runner_aborts_unless_continue_on_error():
    """Given a failing step, When continue_on_error is false, Then later steps never run."""
    calls: list[str] = []

    def executor(command: str) -> str:
        calls.append(command)
        if command == "fail":
            raise RuntimeError("boom")
        return "ok"

    chain = _chain(
        [
            ChainStep(id="bad", run="fail"),
            ChainStep(id="never", run="echo never"),
        ]
    )
    result = ChainRunner(chain, executor=executor, retry_backoff=0).run()
    assert result.ok is False and result.aborted is True
    assert calls == ["fail"]
    assert len(result.steps) == 1


def test_runner_continues_when_policy_allows():
    """Given continue_on_error, When a step fails, Then the next step still runs."""
    calls: list[str] = []

    def executor(command: str) -> str:
        calls.append(command)
        if command == "fail":
            raise RuntimeError("boom")
        return "ok"

    chain = _chain(
        [
            ChainStep(id="bad", run="fail", continue_on_error=True),
            ChainStep(id="next", run="echo next"),
        ]
    )
    result = ChainRunner(chain, executor=executor, retry_backoff=0).run()
    assert result.aborted is False
    assert result.ok is False
    assert calls == ["fail", "echo next"]
    assert result.steps[1].status == "ok"


def test_runner_dry_run_never_executes():
    """Given dry_run, When a chain resolves, Then commands are returned without execution."""
    called: list[str] = []
    chain = _chain([ChainStep(id="one", run="echo {target}")])
    result = ChainRunner(chain, executor=lambda command: called.append(command) or "x", dry_run=True).run()
    assert result.ok is True
    assert result.steps[0].status == "dry-run"
    assert result.steps[0].run == "echo 127.0.0.1"
    assert called == []


def test_runner_skips_when_and_unresolved_and_checks_expect():
    """Given skipped or unresolved steps, When executed, Then they never run; expect enforces text."""
    calls: list[str] = []

    def executor(command: str) -> str:
        calls.append(command)
        return "wrong"

    chain = _chain(
        [
            ChainStep(id="skip", run="echo skip", when='mode == "off"'),
            ChainStep(id="unresolved", run="echo {missing}"),
            ChainStep(id="expect", run="echo expected", expect="right"),
        ]
    )
    result = ChainRunner(chain, tokens={"mode": "on"}, executor=executor, retry_backoff=0).run()
    assert result.steps[0].status == "skipped"
    assert result.steps[1].status == "skipped" and "unresolved" in result.steps[1].reason
    assert result.steps[2].status == "failed" and "expected" in result.steps[2].reason
    assert calls == ["echo expected"]


def test_runner_resolves_newest_and_skip_if_exists(tmp_path, monkeypatch):
    """Given files on disk, When guards evaluate, Then newest globs bind and existing paths skip."""
    monkeypatch.chdir(tmp_path)
    (tmp_path / "sessions").mkdir()
    (tmp_path / "sessions" / "scan.nmap.xml").write_text("<x/>", encoding="utf-8")
    newest = tmp_path / "plan_new.yaml"
    newest.write_text("new", encoding="utf-8")
    oldest = tmp_path / "plan_old.yaml"
    oldest.write_text("old", encoding="utf-8")
    time.sleep(0.01)
    newest.touch()
    chain = _chain(
        [
            ChainStep(id="skip", run="echo skip", skip_if_exists="sessions/scan.nmap.xml"),
            ChainStep(
                id="newest",
                run="echo {plan}",
                resolve_newest_glob="plan_*.yaml",
                resolve_newest_as="plan",
            ),
        ]
    )
    result = ChainRunner(chain, executor=lambda command: command, retry_backoff=0).run()
    assert result.steps[0].status == "skipped"
    assert result.steps[1].run == f"echo {newest.resolve()}"


def test_v2_schema_accepts_policy_and_rejects_bad_values(tmp_path):
    """Given v2 fields, When validated, Then valid files pass and bad policy is named."""
    valid = {
        "name": "demo",
        "version": 2,
        "vars": {"mode": "recon"},
        "tags": ["gym"],
        "platforms": ["linux"],
        "steps": [
            {
                "id": "probe",
                "run": "echo hi",
                "phase": "recon",
                "when": 'mode == "recon"',
                "timeout": 30,
                "retries": 2,
                "continue_on_error": True,
                "capture": "output",
                "expect": "hi",
                "artifacts": ["sessions/x"],
                "sinks": ["intel_graph"],
            }
        ],
    }
    assert validate_chain(valid, filename="demo") == []
    bad = {
        "name": "demo",
        "version": 2,
        "steps": [
            {"id": "Bad Id", "run": "x", "timeout": -1, "retries": 99, "capture": "Bad Name"},
            {"id": "dup", "run": "y"},
            {"id": "dup", "run": "z"},
        ],
    }
    errors = validate_chain(bad, filename="demo")
    assert any("invalid step id" in error for error in errors)
    assert any("timeout" in error for error in errors)
    assert any("retries" in error for error in errors)
    assert any("capture" in error for error in errors)
    assert any("duplicate step id" in error for error in errors)


def test_runner_falls_back_to_os_commands():
    """Given a raw command, When the shell has no matching verb, Then subprocess output is captured."""
    class Shell:
        aliases: dict = {}

        def do_echo(self, line: str) -> None:
            raise AssertionError("raw command must not route through cmd2")

    chain = _chain([ChainStep(id="raw", run="printf fallback")])
    result = ChainRunner(chain, shell=Shell(), retry_backoff=0).run()
    assert result.steps[0].status == "ok"
    assert "fallback" in result.steps[0].output


def test_runner_executes_python_module_commands():
    """Given a python3 module command, When the chain runs, Then subprocess captures its output."""
    class Shell:
        aliases: dict = {}

    chain = _chain([ChainStep(id="py", run='python3 -c "print(123)"')])
    result = ChainRunner(chain, shell=Shell(), retry_backoff=0).run()
    assert result.steps[0].status == "ok"
    assert "123" in result.steps[0].output


def test_runner_keeps_verbs_on_calling_thread():
    """Given a cmd2 verb, When the chain runs, Then it stays on the operator thread."""
    seen: list[threading.Thread] = []

    class Shell:
        aliases: dict = {}

        def do_assign(self, line: str) -> None:
            seen.append(threading.current_thread())

        def onecmd(self, command: str) -> bool:
            _verb, _, args = command.partition(" ")
            getattr(self, f"do_{_verb}")(args)
            return False

    chain = _chain([ChainStep(id="verb", run="assign target 10.0.0.5")])
    result = ChainRunner(chain, shell=Shell(), retry_backoff=0).run()
    assert result.steps[0].status == "ok"
    assert result.steps[0].output == ""
    assert seen == [threading.main_thread()]


def test_runner_fails_on_nonzero_exit():
    """Given a raw command that exits non-zero, When the chain runs, Then the step fails."""
    class Shell:
        aliases: dict = {}

    chain = _chain([ChainStep(id="bad", run="false")])
    result = ChainRunner(chain, shell=Shell(), retry_backoff=0).run()
    assert result.steps[0].status == "failed"
    assert result.aborted is True


def test_runner_routes_known_verb_through_shell():
    """Given a cmd2 verb, When the chain runs, Then the live shell handles it."""
    calls: list[str] = []

    class Shell:
        aliases: dict = {}

        def do_assign(self, line: str) -> None:
            calls.append(line)

        def onecmd(self, command: str) -> None:
            _verb, _, args = command.partition(" ")
            getattr(self, f"do_{_verb}")(args)

    chain = _chain([ChainStep(id="verb", run="assign target 10.0.0.5")])
    result = ChainRunner(chain, shell=Shell(), retry_backoff=0).run()
    assert result.steps[0].status == "ok"
    assert calls == ["target 10.0.0.5"]


def test_runner_timeout_marks_step_timeout():
    """Given a slow executor, When the step timeout elapses, Then the step reports timeout."""
    chain = _chain([ChainStep(id="slow", run="sleep", timeout=1)])
    result = ChainRunner(chain, executor=lambda command: time.sleep(1.2) or "late", retry_backoff=0).run()
    assert result.steps[0].status == "timeout"
    assert result.aborted is True


def test_when_evaluator_accepts_list_literals():
    """Given a list literal, When the condition evaluates, Then membership works."""
    values = {"port": "22"}
    assert evaluate_when('port in ["22", "80"]', values) is True
    assert evaluate_when('port not in ["443"]', values) is True


def test_validate_rejects_malformed_when():
    """Given a broken condition, When validating, Then the chain is rejected."""
    errors = validate_chain(
        {"name": "demo", "steps": [{"id": "one", "run": "echo", "when": "phase =="}]}
    )
    assert any("invalid when" in error for error in errors)


def test_runner_quotes_captured_values_in_raw_shell_steps():
    """Given untrusted captured output, When a raw shell step renders, Then it is quoted."""
    seen: list[str] = []

    def executor(command: str) -> str:
        seen.append(command)
        return "x; touch /tmp/pwned"

    chain = _chain(
        [
            ChainStep(id="cap", run="probe", capture="out"),
            ChainStep(id="use", run="echo {out}"),
        ]
    )
    ChainRunner(chain, executor=executor, retry_backoff=0).run()
    assert seen[1] == "echo 'x; touch /tmp/pwned'"


def test_runner_captures_verb_stdout():
    """Given a cmd2 verb that prints, When it runs, Then capture sees stdout."""
    class FakeShell:
        aliases = {}

        def do_lazy_note(self, line: str) -> None:
            print(f"noted {line}")

        def onecmd(self, command: str):
            return self.do_lazy_note(command.split(maxsplit=1)[1])

    chain = _chain([ChainStep(id="cap", run="lazy_note hello", capture="out")])
    result = ChainRunner(chain, shell=FakeShell(), retry_backoff=0).run()
    assert result.steps[0].status == "ok"
    assert "noted hello" in result.steps[0].captured
