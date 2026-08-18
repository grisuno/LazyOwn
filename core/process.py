"""Process and subprocess utilities for the LazyOwn framework.

Extracted from ``utils.py`` — command execution, binary/package detection,
sudo escalation, virtualenv activation.
"""

from __future__ import annotations

import importlib
import os
import shlex
import shutil
import subprocess
import sys
import threading
import time
from collections.abc import Callable
from typing import Any

from core.console import (
    BRIGHT_BLACK,
    RESET,
    YELLOW,
    print_error,
    print_msg,
    print_warn,
)
from core.safe_subprocess import SafeRunner
from core.validators import check_rhost


def check_go_tool_installed(tool_name: str) -> bool:
    """Check if a Go tool binary is installed and runnable.

    Args:
        tool_name: Name of the binary to check.

    Returns:
        True if the tool responds with a zero exit code to ``help``.
    """
    try:
        process = subprocess.run(
            [tool_name, "help"],
            capture_output=True,
            check=False,
        )
        return process.returncode == 0
    except FileNotFoundError:
        return False


def is_binary_present(binary_name: str) -> bool:
    """Check whether binary is on ``PATH``.

    Uses ``shutil.which`` — no shell spawning, no injection surface.

    Args:
        binary_name: Name of the binary.

    Returns:
        True if found on PATH.
    """
    return shutil.which(binary_name) is not None


def handle_multiple_rhosts(func: Callable) -> Callable:
    """Decorator that iterates over a list of remote hosts.

    Wraps a shell method so it runs against each host in
    ``self.params["rhost"]``.  The original host is restored after
    each iteration.

    Args:
        func: The method to wrap.

    Returns:
        The decorated wrapper.
    """

    def wrapper(self, *args: Any, **kwargs: Any) -> None:
        rhosts = self.params["rhost"]
        if isinstance(rhosts, str):
            rhosts = [rhosts]
        for rhost in rhosts:
            if not check_rhost(rhost):
                continue
            original_rhost = self.params["rhost"]
            self.params["rhost"] = rhost
            func(self, *args, **kwargs)
            self.params["rhost"] = original_rhost

    return wrapper


def check_sudo() -> None:
    """Re-launch the script with ``sudo`` if not already root.

    Exits the current process and replaces it with a sudo invocation.
    """
    if os.geteuid() != 0:
        print_warn("This script requires superuser permissions. Relaunching with sudo...")
        args = ["sudo", sys.executable] + sys.argv
        os.execvpe("sudo", args, os.environ)  # noqa: S606


def run(command: str) -> str:
    """Execute a shell command via ``SafeRunner``.

    Args:
        command: Shell command string.

    Returns:
        Stripped stdout on success, error message on failure.
    """
    try:
        print_msg(f"Attempting to execute: {command}")
        result = SafeRunner().run_shell(
            command,
            allow=True,
            reason="legacy utils.run call site; requires opt-in at every invocation",
        )
        if result.returncode != 0:
            print_error(f"Command failed with exit code {result.returncode}: {command}")
            return result.stderr or f"exit={result.returncode}"
        print_msg(result.stdout)
        return result.stdout.strip()
    except FileNotFoundError as fnf_error:
        print_error(f"Command not found: {command}")
        return str(fnf_error)
    except subprocess.CalledProcessError as cpe_error:
        print_error(f"Command failed with exit code {cpe_error.returncode}: {command}")
        return str(cpe_error)
    except subprocess.TimeoutExpired as te_error:
        print_error(f"Command timed out: {command}")
        return str(te_error)
    except Exception as e:
        print_error(f"An unexpected error occurred: {str(e)}")
        return str(e)


def is_package_installed(package_name: str) -> bool:
    """Check whether a Python package is importable.

    Args:
        package_name: Name of the package (e.g. ``requests``).

    Returns:
        True if ``importlib.util.find_spec`` succeeds.
    """
    return importlib.util.find_spec(package_name) is not None


RUN_COMMAND_STATUS_MIN_SECONDS = 1.0
_RUN_COMMAND_MAX_DISPLAY = 80


def _print_run_command_status(command: str, elapsed: float, exit_code: int | None) -> None:
    """Print a dim completion line (elapsed time + exit code) after a run.

    Only shown on interactive terminals and only when the command took long
    enough to matter (``RUN_COMMAND_STATUS_MIN_SECONDS``) or reported a
    non-zero exit, so quick aliases stay silent while long scans and failed
    tools always leave a visible trace. Never touches the returned output.
    """
    try:
        if not sys.stdout.isatty():
            return
        if elapsed < RUN_COMMAND_STATUS_MIN_SECONDS and exit_code in (0, None):
            return
        label = command
        if len(label) > _RUN_COMMAND_MAX_DISPLAY:
            label = label[: _RUN_COMMAND_MAX_DISPLAY - 1] + "…"
        code = "interrupted" if exit_code is None else f"exit={exit_code}"
        color = BRIGHT_BLACK if exit_code in (0, None) else YELLOW
        sys.stdout.write(f"{color}[done] {label}  {code}  {elapsed:.1f}s{RESET}\n")
        sys.stdout.flush()
    except Exception:
        pass


def run_command(command: str, timeout: float | None = None) -> str:
    """Run a command, streaming output in real time.

    Uses ``subprocess.Popen`` to execute ``command``, printing stdout and
    stderr as they arrive and returning the complete output string.

    stderr is drained on a worker thread so a chatty process writing to
    stderr while stdout is quiet can never deadlock the read loop.

    Args:
        command: The command string to execute.
        timeout: Optional per-command timeout in seconds. When exceeded the
            process is killed and the partial output is returned.

    Returns:
        Combined stdout + stderr output.
    """
    output = ""
    command_tokens = shlex.split(command)
    start_time = time.monotonic()
    exit_code: int | None = None
    process = None
    try:
        process = subprocess.Popen(
            command_tokens,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
    except FileNotFoundError:
        print_error(f"Command not found: {command_tokens[0] if command_tokens else command}")
        _print_run_command_status(command, time.monotonic() - start_time, 127)
        return output

    stderr_chunks: list[str] = []

    def _drain_stderr() -> None:
        if process is None or process.stderr is None:
            return
        for line in iter(process.stderr.readline, ""):
            stderr_chunks.append(line)
            sys.stdout.write(line)
        sys.stdout.flush()

    stderr_thread = threading.Thread(target=_drain_stderr, daemon=True)
    stderr_thread.start()
    try:
        if process.stdout is not None:
            for line in iter(process.stdout.readline, ""):
                sys.stdout.write(line)
                output += line
        stderr_thread.join()
        try:
            process.wait(timeout=timeout)
        except subprocess.TimeoutExpired:
            process.kill()
            process.wait()
            print_error(f"Command timed out: {command}")
    except KeyboardInterrupt:
        process.terminate()
        print_warn("\n[Interrupted] Process terminated")
        process.wait()
    finally:
        exit_code = process.returncode
        output += "".join(stderr_chunks)
        _print_run_command_status(command, time.monotonic() - start_time, exit_code)
    return output


def ensure_tmux_session(session_name: str) -> None:
    """Create a tmux session if it does not already exist.

    Args:
        session_name: Name for the tmux session.
    """
    result = subprocess.run(
        ["tmux", "has-session", "-t", session_name],
        capture_output=True,
        stderr=subprocess.PIPE,
    )
    if result.returncode != 0:
        subprocess.run(
            ["tmux", "new-session", "-d", "-s", session_name],
            check=False,
        )


def activate_server(httpd: Any, url: str, lhost: str) -> None:
    """Start an HTTP server and print the serving URL.

    Args:
        httpd: An HTTPServer instance with a ``serve_forever`` method.
        url: URL path for the server.
        lhost: Listening host address.
    """
    print(f"[+] Serving HTTP on {lhost} on {url}")
    print_msg("Server started. Press Ctrl+C to stop.")
    httpd.serve_forever()


__all__ = [
    "check_go_tool_installed",
    "is_binary_present",
    "handle_multiple_rhosts",
    "check_sudo",
    "run",
    "is_package_installed",
    "run_command",
    "ensure_tmux_session",
    "activate_server",
]
