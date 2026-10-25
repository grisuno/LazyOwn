"""
UnifiedCommandExecutor — shared shell command execution service.

Replaces scattered subprocess calls across CLI, C2, and MCP with a single
executor that:
- Runs commands via subprocess (real-time streaming or capture)
- Publishes events via UnifiedEventBus
- Logs to CSV via session report
- Records metrics (duration, exit code, success)
- Stores output in StateManager when relevant

Design (SOLID)
--------------
- Single Responsibility : only command execution and its observability.
- Open/Closed           : new output handlers via Callable hooks.
- Liskov                : all execution modes return typed ExecutionResult.
- Interface Segregation : just ``run()`` and ``run_capture()``.
- Dependency Inversion  : consumers depend on the executor, not on subprocess.
"""

from __future__ import annotations

import logging
import os
import select
import shlex
import signal
import subprocess
import sys
import threading
import time
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path

from core.safe_exec import needs_shell as _shared_needs_shell

_THREAD_LIMITS = threading.local()


def set_thread_timeout(seconds: float) -> None:
    """Bound the next ``run_tee`` call on this thread by wall-clock seconds."""
    _THREAD_LIMITS.timeout = max(0.0, float(seconds or 0.0))


def clear_thread_timeout() -> None:
    """Remove this thread's ``run_tee`` deadline, if any."""
    try:
        del _THREAD_LIMITS.timeout
    except AttributeError:
        return


def thread_timeout() -> float | None:
    """Return this thread's pending ``run_tee`` deadline, or None."""
    return getattr(_THREAD_LIMITS, "timeout", None)


def set_thread_stdin_devnull(enabled: bool = True) -> None:
    """Detach the next ``run_tee`` child from the operator terminal."""
    _THREAD_LIMITS.stdin_devnull = bool(enabled)


def clear_thread_stdin_devnull() -> None:
    """Restore inherited stdin for this thread's ``run_tee`` calls."""
    try:
        del _THREAD_LIMITS.stdin_devnull
    except AttributeError:
        return


def thread_stdin_devnull() -> bool:
    """Return True when this thread's ``run_tee`` children drop stdin."""
    return bool(getattr(_THREAD_LIMITS, "stdin_devnull", False))


def _kill_process_group(proc: subprocess.Popen) -> None:
    """Kill a tee'd child and every descendant in its session/process group."""
    try:
        os.killpg(os.getpgid(proc.pid), signal.SIGKILL)
        return
    except Exception:
        pass
    try:
        proc.kill()
    except Exception:
        pass


log = logging.getLogger("command_executor")

_LAZYOWN_DIR = Path(__file__).resolve().parent.parent
_SESSIONS_DIR = _LAZYOWN_DIR / "sessions"


@dataclass
class ExecutionResult:
    command: str
    output: str = ""
    exit_code: int = -1
    duration_ms: int = 0
    success: bool = False
    error: str = ""


class CommandExecutor:
    """Shared shell command execution service.

    Usage::

        executor = CommandExecutor()
        result = executor.run("nmap -sC 10.0.0.1")
        print(result.output[:200])
    """

    _instance: CommandExecutor | None = None

    def __init__(self) -> None:
        self._hooks: list[Callable[[ExecutionResult], None]] = []

    @classmethod
    def instance(cls) -> CommandExecutor:
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def add_hook(self, hook: Callable[[ExecutionResult], None]) -> None:
        """Register a post-execution hook (e.g., for StateManager or metrics)."""
        self._hooks.append(hook)

    def run(self, command: str, timeout: int = 120, stream: bool = False) -> ExecutionResult:
        """Execute a shell command and return the result.

        Args:
            command: The shell command string to execute.
            timeout: Maximum execution time in seconds.
            stream: If True, print output in real-time. If False, capture silently.

        Returns:
            ExecutionResult with output, exit_code, duration_ms, and success.
        """
        start = time.monotonic()
        result = ExecutionResult(command=command)

        try:
            if stream:
                result = self._run_stream(command, timeout)
            else:
                result = self._run_capture(command, timeout)
        except subprocess.TimeoutExpired:
            result.success = False
            result.error = f"Command timed out after {timeout}s"
        except Exception as exc:
            result.success = False
            result.error = str(exc)

        result.duration_ms = int((time.monotonic() - start) * 1000)
        result.success = result.success or (result.exit_code == 0)

        self._fire_hooks(result)
        self._publish_event(result)

        return result

    def _needs_shell(self, command: str) -> bool:
        """Check if command needs bash -c due to shell operators.

        Shared policy from :func:`core.safe_exec.needs_shell` so every
        runner splits argv versus shell identically.
        """
        return _shared_needs_shell(command)

    def _argv(self, command: str) -> list[str] | str:
        """Return the spawn target honoring the shared shell policy."""
        if self._needs_shell(command):
            return ["bash", "-c", command]
        return shlex.split(command)

    def run_passthrough(self, command: str, env: dict | None = None) -> int:
        """Run a command with stdio inherited, returning its exit code.

        Used for the NOLOGS path: output goes straight to the
        operator terminal (colors intact), nothing is captured.

        Args:
            command: Shell command string to execute.
            env: Child environment mapping, or None to inherit.

        Returns:
            The child exit code.
        """
        return subprocess.call(self._argv(command), env=env)

    def run_tee(
        self,
        command: str,
        *,
        env: dict | None = None,
        writer: Callable[[str], object] | None = None,
        log_file: str | Path | None = None,
        timeout: float | None = None,
    ) -> ExecutionResult:
        """Run a command teeing raw output bytes to a writer and a log file.

        Bytes are forwarded untouched (ANSI colors preserved); stderr is
        merged into stdout exactly like an interactive terminal row.

        Args:
            command: Shell command string to execute.
            env: Child environment mapping, or None to inherit. Pass
                :func:`core.hardening.terminal_env` to keep child colors.
            writer: Called with every stdout chunk. Defaults to writing
                and flushing ``sys.stdout``.
            log_file: Optional path appended with the same chunks.
            timeout: Wall-clock seconds for ``wait``; None waits forever.
                On expiry the child is killed and
                :class:`subprocess.TimeoutExpired` propagates.

        Returns:
            ExecutionResult with the full output and exit code.
        """
        start = time.monotonic()
        emit = writer if writer is not None else self._default_writer
        handle = open(log_file, "w") if log_file is not None else None
        effective_timeout = timeout if timeout is not None else thread_timeout()
        detached = thread_stdin_devnull()
        proc = None
        try:
            proc = subprocess.Popen(
                self._argv(command),
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                stdin=subprocess.DEVNULL if detached else None,
                text=True,
                env=env,
                start_new_session=detached,
            )
            try:
                from modules.auto_registry import track_process

                track_process(proc)
            except Exception:
                pass
            output_parts: list[str] = []
            deadline = None if effective_timeout is None else start + effective_timeout
            while True:
                remaining = None if deadline is None else deadline - time.monotonic()
                if remaining is not None and remaining <= 0:
                    raise subprocess.TimeoutExpired(command, effective_timeout)
                ready, _, _ = select.select([proc.stdout], [], [], remaining)
                if not ready:
                    raise subprocess.TimeoutExpired(command, effective_timeout)
                line = proc.stdout.readline()
                if not line:
                    break
                emit(line)
                if handle is not None:
                    handle.write(line)
                    handle.flush()
                output_parts.append(line)
            proc.wait()
        except BaseException:
            if proc is not None:
                if detached:
                    _kill_process_group(proc)
                else:
                    try:
                        proc.kill()
                    except Exception:
                        pass
            raise
        finally:
            if proc is not None:
                try:
                    from modules.auto_registry import untrack_process

                    untrack_process(proc)
                except Exception:
                    pass
            if handle is not None:
                handle.close()
        return ExecutionResult(
            command=command,
            output="".join(output_parts),
            exit_code=proc.returncode,
            success=proc.returncode == 0,
            duration_ms=int((time.monotonic() - start) * 1000),
        )

    @staticmethod
    def _default_writer(line: str) -> None:
        """Write a chunk to stdout, flushing immediately."""
        sys.stdout.write(line)
        sys.stdout.flush()

    def _run_capture(self, command: str, timeout: int) -> ExecutionResult:
        import shlex

        if self._needs_shell(command):
            proc = subprocess.run(
                ["bash", "-c", command],
                capture_output=True,
                text=True,
                timeout=timeout,
            )
        else:
            proc = subprocess.run(
                shlex.split(command),
                capture_output=True,
                text=True,
                timeout=timeout,
            )
        output = (proc.stdout or "") + (proc.stderr or "")
        return ExecutionResult(
            command=command,
            output=output,
            exit_code=proc.returncode,
            success=proc.returncode == 0,
        )

    def _run_stream(self, command: str, timeout: int) -> ExecutionResult:
        import shlex

        if self._needs_shell(command):
            proc = subprocess.Popen(
                ["bash", "-c", command],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )
        else:
            proc = subprocess.Popen(
                shlex.split(command),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )
        output_parts: list[str] = []
        try:
            for line in iter(proc.stdout.readline, ""):
                print(line, end="")
                output_parts.append(line)
            for line in iter(proc.stderr.readline, ""):
                print(line, end="")
                output_parts.append(line)
            proc.wait(timeout=timeout)
        except subprocess.TimeoutExpired:
            proc.kill()
            proc.wait()
            raise
        return ExecutionResult(
            command=command,
            output="".join(output_parts),
            exit_code=proc.returncode,
            success=proc.returncode == 0,
        )

    def run_with_tee(self, command: str, output_path: str, timeout: int = 120) -> ExecutionResult:
        """Execute a command and tee output to a file.

        Args:
            command: Shell command string to execute.
            output_path: Log file receiving the same raw bytes shown.
            timeout: Wall-clock seconds; expiry yields an error result.

        Returns:
            ExecutionResult with the full output and exit code.
        """
        start = time.monotonic()
        try:
            result = self.run_tee(
                command,
                writer=self._default_writer,
                log_file=output_path,
                timeout=timeout,
            )
        except subprocess.TimeoutExpired:
            result = ExecutionResult(
                command=command,
                error=f"Command timed out after {timeout}s",
                duration_ms=int((time.monotonic() - start) * 1000),
            )
        except Exception as exc:
            result = ExecutionResult(
                command=command,
                error=str(exc),
                duration_ms=int((time.monotonic() - start) * 1000),
            )

        self._fire_hooks(result)
        self._publish_event(result)
        return result

    def _fire_hooks(self, result: ExecutionResult) -> None:
        for hook in self._hooks:
            try:
                hook(result)
            except Exception:
                log.debug("Executor hook failed", exc_info=True)

    def _publish_event(self, result: ExecutionResult) -> None:
        try:
            from modules.event_bus import EventCategory, EventSeverity, LazyEvent, get_event_bus

            parts = result.command.strip().split(None, 1)
            cmd_name = parts[0] if parts else result.command
            get_event_bus().publish(
                LazyEvent(
                    category=EventCategory.COMMAND,
                    event_type=cmd_name,
                    source="executor",
                    payload={
                        "command": result.command,
                        "duration_ms": result.duration_ms,
                        "exit_code": result.exit_code,
                        "output_snippet": result.output[:500] if result.output else "",
                        "error": result.error,
                    },
                    severity=EventSeverity.INFO if result.success else EventSeverity.WARNING,
                )
            )
        except Exception:
            pass


def get_executor() -> CommandExecutor:
    return CommandExecutor.instance()
