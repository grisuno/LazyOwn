"""TDD tests for the safe subprocess runner contract.

Contract: ``core.safe_subprocess.SafeRunner`` replaces the legacy
``subprocess.run(..., shell=True, ...)`` call sites in :mod:`utils` and
:mod:`lazyc2` with a default-deny wrapper that requires an explicit
``allow=True`` and a free-text ``reason`` for every shell invocation.

Invariants:

1. ``run_shell(cmd, allow=False)`` raises ``ShellNotAllowedError``.
2. ``run_shell(cmd, allow=True, reason="...")`` executes the command and
   appends one JSON line to the audit log.
3. ``run(argv_list)`` is always allowed and never touches the audit log.
4. Both APIs return a ``SafeRunResult`` exposing ``returncode``,
   ``stdout``, ``stderr``, and ``duration_seconds``.
5. The audit log records ``argv`` (or the raw string), ``reason``,
   ``returncode``, and the timestamp.
"""

from __future__ import annotations

import json
import shlex
import sys
from pathlib import Path

import pytest

from core.safe_subprocess import (
    SafeRunResult,
    SafeRunner,
    ShellNotAllowedError,
)


class TestRunArgv:
    """``run`` accepts an argv list, never logs, never blocks."""

    def test_run_returns_completed_result(self) -> None:
        runner = SafeRunner()
        result = runner.run([sys.executable, "-c", "print('ok')"])
        assert isinstance(result, SafeRunResult)
        assert result.returncode == 0
        assert "ok" in result.stdout
        assert result.duration_seconds >= 0.0

    def test_run_does_not_audit(self, tmp_path: Path) -> None:
        audit = tmp_path / "audit.jsonl"
        runner = SafeRunner(audit_log_path=audit)
        runner.run([sys.executable, "-c", "print('x')"])
        assert not audit.exists()


class TestRunShellDefaultDeny:
    """``run_shell`` requires explicit opt-in."""

    def test_default_deny_raises(self) -> None:
        runner = SafeRunner()
        with pytest.raises(ShellNotAllowedError):
            runner.run_shell("echo hello")

    def test_deny_audit_logged(self, tmp_path: Path) -> None:
        audit = tmp_path / "audit.jsonl"
        runner = SafeRunner(audit_log_path=audit)
        with pytest.raises(ShellNotAllowedError):
            runner.run_shell("echo hello")
        record = json.loads(audit.read_text(encoding="utf-8").splitlines()[-1])
        assert record["allowed"] is False
        assert record["command"] == "echo hello"


class TestRunShellAllowed:
    """``run_shell(allow=True, reason=...)`` executes and audits."""

    def test_allowed_executes(self) -> None:
        runner = SafeRunner()
        result = runner.run_shell(
            "echo hello",
            allow=True,
            reason="smoke test",
        )
        assert result.returncode == 0
        assert "hello" in result.stdout

    def test_allowed_is_audited(self, tmp_path: Path) -> None:
        audit = tmp_path / "audit.jsonl"
        runner = SafeRunner(audit_log_path=audit)
        runner.run_shell("echo logged", allow=True, reason="behaviour test")
        record = json.loads(audit.read_text(encoding="utf-8").splitlines()[-1])
        assert record["allowed"] is True
        assert record["reason"] == "behaviour test"
        assert record["command"] == "echo logged"
        assert record["returncode"] == 0

    def test_empty_reason_rejected(self) -> None:
        runner = SafeRunner()
        with pytest.raises(ValueError):
            runner.run_shell("echo x", allow=True, reason="")

    def test_failed_command_returns_nonzero(self) -> None:
        runner = SafeRunner()
        result = runner.run_shell(
            "sh -c 'exit 7'",
            allow=True,
            reason="checking nonzero exit",
        )
        assert result.returncode == 7
