"""BDD behavior scenarios for the safe subprocess contract."""

from __future__ import annotations

import json
import sys
from pathlib import Path

from core.safe_subprocess import SafeRunner, ShellNotAllowedError


def test_given_argv_when_run_then_executes_without_audit(tmp_path: Path) -> None:
    """Given an argv list, ``run`` executes it and writes no audit row."""
    audit = tmp_path / "audit.jsonl"
    runner = SafeRunner(audit_log_path=audit)
    result = runner.run([sys.executable, "-c", "print('argv')"])
    assert result.returncode == 0
    assert "argv" in result.stdout
    assert not audit.exists()


def test_given_shell_without_allow_when_called_then_denied(tmp_path: Path) -> None:
    """Given a shell call without opt-in, the runner denies and audits."""
    audit = tmp_path / "audit.jsonl"
    runner = SafeRunner(audit_log_path=audit)
    try:
        runner.run_shell("echo hidden")
    except ShellNotAllowedError:
        pass
    else:
        raise AssertionError("expected ShellNotAllowedError")
    record = json.loads(audit.read_text(encoding="utf-8").splitlines()[-1])
    assert record["allowed"] is False


def test_given_shell_with_allow_and_reason_when_called_then_executes(tmp_path: Path) -> None:
    """Given a shell call with opt-in and reason, the runner executes and audits."""
    audit = tmp_path / "audit.jsonl"
    runner = SafeRunner(audit_log_path=audit)
    result = runner.run_shell("echo ok", allow=True, reason="smoke")
    assert result.returncode == 0
    assert "ok" in result.stdout
    record = json.loads(audit.read_text(encoding="utf-8").splitlines()[-1])
    assert record["allowed"] is True
    assert record["reason"] == "smoke"
