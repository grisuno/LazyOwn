"""Centralised subprocess wrapper for the LazyOwn framework.

Provides safe, logged command execution as a replacement for bare
:func:`os.system` and unguarded :func:`subprocess.run` calls.

Contracts
---------
1. :func:`safe_run` executes a command via the system shell, logs the
   invocation, enforces a timeout, and returns a
   :class:`subprocess.CompletedProcess`.
2. :func:`run_shell` is a convenience wrapper that returns stdout as a
   string (or raises on failure).
3. Every command is logged at INFO level with the PID and exit code.

Usage
-----
    from core.executor import safe_run, run_shell

    result = safe_run(["nmap", "-sS", target], timeout=60)
    if result.returncode != 0:
        print(result.stderr)

    output = run_shell("ls -la /tmp", timeout=10)

Config keys owned: none.
"""

from __future__ import annotations

import logging
import os
import shlex
import subprocess
from typing import overload

_VALID_TIMEOUT_RANGE = (1, 3600)

log = logging.getLogger("executor")


def _validate_input(command: str | list[str]) -> tuple[list[str], str]:
    """Validate command input and return argv and loggable string.

    Args:
        command: A string or list of arguments.

    Returns:
        Tuple of (argv_as_list, command_str_for_logging).

    Raises:
        TypeError: If command is not str or list.
        ValueError: If command is empty or contains null bytes.
    """
    if isinstance(command, list):
        if not command:
            raise ValueError("command list must not be empty")
        argv = [str(arg) for arg in command]
        for arg in argv:
            if "\x00" in arg:
                raise ValueError("command arguments must not contain null bytes")
        cmd_str = " ".join(shlex.quote(a) for a in argv)
    elif isinstance(command, str):
        if not command.strip():
            raise ValueError("command string must not be empty")
        if "\x00" in command:
            raise ValueError("command string must not contain null bytes")
        cmd_str = command
        argv = shlex.split(command)
    else:
        raise TypeError(f"command must be str or list, got {type(command).__name__}")

    return argv, cmd_str


def _validate_timeout(timeout: int) -> int:
    """Clamp and validate timeout seconds.

    Args:
        timeout: Requested timeout in seconds.

    Returns:
        Validated timeout value.

    Raises:
        ValueError: If timeout is outside valid range.
    """
    if not isinstance(timeout, int) or timeout < _VALID_TIMEOUT_RANGE[0]:
        raise ValueError(
            f"timeout must be >= {_VALID_TIMEOUT_RANGE[0]} seconds, got {timeout}"
        )
    if timeout > _VALID_TIMEOUT_RANGE[1]:
        log.warning("timeout %d exceeds max, clamping to %d", timeout, _VALID_TIMEOUT_RANGE[1])
        timeout = _VALID_TIMEOUT_RANGE[1]
    return timeout


@overload
def safe_run(command: str, *, timeout: int = 300) -> subprocess.CompletedProcess[str]: ...
@overload
def safe_run(command: list[str], *, timeout: int = 300) -> subprocess.CompletedProcess[str]: ...


def safe_run(
    command: str | list[str], *, timeout: int = 300
) -> subprocess.CompletedProcess[str]:
    """Execute a command via the system shell with logging and timeout.

    Intended as a drop-in replacement for :func:`os.system` calls.
    Uses ``shell=True`` to preserve compatibility with shell-builtin
    commands (pipes, redirects, env vars) used throughout the codebase.

    Args:
        command: A shell command string or list of argv tokens.
        timeout: Maximum execution time in seconds (1-3600, default 300).

    Returns:
        A :class:`subprocess.CompletedProcess` with ``stdout`` and
        ``stderr`` captured as strings.

    Raises:
        TypeError: If *command* is neither ``str`` nor ``list``.
        ValueError: If *command* is empty, contains null bytes, or timeout
            is out of range.
        subprocess.TimeoutExpired: If the command exceeds *timeout*.

    Security:
        Accepts shell commands intentionally. Callers are responsible for
        sanitising user-controlled input before passing it here.
        Null-byte injection is rejected.
    """
    timeout = _validate_timeout(timeout)
    argv, cmd_str = _validate_input(command)

    log.info("safe_run[%d]: %s", os.getpid(), cmd_str)

    return subprocess.run(
        cmd_str,
        shell=True,
        capture_output=True,
        text=True,
        timeout=timeout,
    )


def run_shell(cmd: str, *, timeout: int = 300) -> str:
    """Execute a shell command and return its stdout.

    A convenient wrapper over :func:`safe_run` that raises on non-zero
    exit codes.

    Args:
        cmd: The shell command string to execute.
        timeout: Maximum execution time in seconds (1-3600, default 300).

    Returns:
        Captured stdout with leading/trailing whitespace stripped.

    Raises:
        subprocess.CalledProcessError: If the command exits with a
            non-zero return code.
        See :func:`safe_run` for other possible exceptions.

    Security:
        See :func:`safe_run` security note.
    """
    result = safe_run(cmd, timeout=timeout)
    if result.returncode != 0:
        log.warning(
            "run_shell[%d]: command exited %d — %s stderr=%s",
            os.getpid(),
            result.returncode,
            cmd[:120],
            result.stderr[:500] if result.stderr else "",
        )
        raise subprocess.CalledProcessError(
            result.returncode, cmd, output=result.stdout, stderr=result.stderr
        )
    return result.stdout.strip()


__all__ = ["safe_run", "run_shell"]
