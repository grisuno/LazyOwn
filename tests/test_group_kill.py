"""Process-group containment contract: timeouts must not leave orphans.

Every scenario states Given, When, Then. Scenarios spawn distinctive
``sleep 97`` grandchildren so a leaked process is observable with
pgrep; the group kill removes the whole tree either way.
"""

from __future__ import annotations

import subprocess

import pytest

from core.safe_exec import safe_run_argv, safe_run_shell

_SLEEP_MARK = "sleep 97"


def _orphan_count() -> int:
    """Count leftover sleep 97 processes."""
    result = subprocess.run(
        ["pgrep", "-f", _SLEEP_MARK],
        capture_output=True,
        text=True,
        check=False,
    )
    return len(result.stdout.split())


def test_safe_run_shell_timeout_kills_group():
    """Given a shell child with grandkids, When timeout fires, Then no orphan remains."""
    try:
        safe_run_shell(
            f"bash -c '{_SLEEP_MARK} & wait'",
            allow=True,
            reason="orphan probe",
            timeout=1.0,
        )
    except subprocess.TimeoutExpired:
        pass
    assert _orphan_count() == 0


def test_safe_run_argv_timeout_kills_group():
    """Given an argv child with grandkids, When timeout fires, Then no orphan remains."""
    try:
        safe_run_argv(["bash", "-c", f"{_SLEEP_MARK} & wait"], timeout=1.0)
    except subprocess.TimeoutExpired:
        pass
    assert _orphan_count() == 0


def test_safe_run_shell_normal_completion_unchanged():
    """Given a fast command, When executed, Then output and return code stay intact."""
    result = safe_run_shell("printf ok", allow=True, reason="normal probe")
    assert result.returncode == 0 and result.stdout == "ok"


def test_safe_run_argv_normal_completion_unchanged():
    """Given a fast argv command, When executed, Then output and return code stay intact."""
    result = safe_run_argv(["printf", "ok"])
    assert result.returncode == 0 and result.stdout == "ok"


def test_safe_run_argv_check_contract():
    """Given check mode, When a child fails, Then CalledProcessError carries output."""
    with pytest.raises(subprocess.CalledProcessError):
        safe_run_argv(["false"], check=True)


def test_safe_run_argv_stdout_disabled():
    """Given capture disabled, When executed, Then streams land on the inherited terminal."""
    result = safe_run_argv(["true"], capture_output=False)
    assert result.returncode == 0
