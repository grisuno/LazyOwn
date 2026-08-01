"""Tests for core.executor — safe_run and run_shell subprocess wrappers."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))


class TestSafeRun:
    """Tests for :func:`core.executor.safe_run`."""

    def test_echo_hello_returns_completed_process_with_stdout(self):
        """safe_run with a list returns a CompletedProcess and captures stdout."""
        from core.executor import safe_run

        result = safe_run(["echo", "hello"])
        assert isinstance(result, subprocess.CompletedProcess)
        assert result.returncode == 0
        assert "hello" in result.stdout

    def test_false_command_returns_nonzero(self):
        """safe_run with the false command returns a non-zero exit code."""
        from core.executor import safe_run

        result = safe_run(["false"])
        assert result.returncode != 0

    def test_empty_list_raises_value_error(self):
        """safe_run raises ValueError when given an empty list."""
        from core.executor import safe_run

        with pytest.raises(ValueError, match="empty"):
            safe_run([])

    def test_empty_string_raises_value_error(self):
        """safe_run raises ValueError when given a whitespace-only string."""
        from core.executor import safe_run

        with pytest.raises(ValueError, match="empty"):
            safe_run("   ")

    def test_timeout_raises_timeout_expired(self):
        """safe_run raises TimeoutExpired when the command exceeds the timeout."""
        from core.executor import safe_run

        with pytest.raises(subprocess.TimeoutExpired):
            safe_run(["sleep", "3"], timeout=1)

    def test_null_bytes_in_list_arg_raises_value_error(self):
        """safe_run rejects null bytes inside list arguments."""
        from core.executor import safe_run

        with pytest.raises(ValueError, match="null"):
            safe_run(["echo", "safe\x00injection"])

    def test_null_bytes_in_string_raises_value_error(self):
        """safe_run rejects null bytes inside a command string."""
        from core.executor import safe_run

        with pytest.raises(ValueError, match="null"):
            safe_run("echo safe\x00injection")

    def test_bad_type_raises_type_error(self):
        """safe_run raises TypeError when command is neither str nor list."""
        from core.executor import safe_run

        with pytest.raises(TypeError, match="command must be str or list"):
            safe_run(42)

    def test_timeout_below_minimum_raises_value_error(self):
        """safe_run raises ValueError when timeout is below the valid range."""
        from core.executor import safe_run

        with pytest.raises(ValueError, match="timeout must be >="):
            safe_run(["echo", "ok"], timeout=0)


class TestRunShell:
    """Tests for :func:`core.executor.run_shell`."""

    def test_echo_hello_returns_stdout_string(self):
        """run_shell returns stripped stdout of a successful command."""
        from core.executor import run_shell

        result = run_shell("echo hello")
        assert isinstance(result, str)
        assert result == "hello"

    def test_nonzero_exit_raises_called_process_error(self):
        """run_shell raises CalledProcessError when the command exits non-zero."""
        from core.executor import run_shell

        with pytest.raises(subprocess.CalledProcessError):
            run_shell("exit 1")

    def test_pipes_and_redirects_work(self):
        """run_shell supports shell-builtins like pipes."""
        from core.executor import run_shell

        result = run_shell("echo one two three | wc -w")
        assert result.strip() == "3"

    def test_stdout_is_stripped_of_whitespace(self):
        """run_shell strips leading and trailing whitespace from stdout."""
        from core.executor import run_shell

        result = run_shell("echo '  padded  '")
        assert result == "padded"
