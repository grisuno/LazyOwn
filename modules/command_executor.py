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
import subprocess
import time
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path

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
        """Check if command needs bash -c due to shell operators."""
        return any(op in command for op in ('2>', '>', '<', '|', '&&', '||', '`', '$('))

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
        """Execute a command and tee output to a file."""
        import shlex
        start = time.monotonic()
        try:
            with open(output_path, "w") as log_file:
                if self._needs_shell(command):
                    proc = subprocess.Popen(
                        ["bash", "-c", command],
                        stdout=subprocess.PIPE,
                        stderr=subprocess.STDOUT,
                        text=True,
                    )
                else:
                    proc = subprocess.Popen(
                        shlex.split(command),
                        stdout=subprocess.PIPE,
                        stderr=subprocess.STDOUT,
                        text=True,
                    )
                output_parts = []
                for line in proc.stdout:
                    sys.stdout.write(line)
                    sys.stdout.flush()
                    log_file.write(line)
                    log_file.flush()
                    output_parts.append(line)
                try:
                    proc.wait(timeout=timeout)
                except subprocess.TimeoutExpired:
                    proc.kill()
                    proc.wait()
                    raise
            exit_code = proc.returncode
            output = "".join(output_parts)
            result = ExecutionResult(
                command=command,
                output=output,
                exit_code=exit_code,
                success=exit_code == 0,
                duration_ms=int((time.monotonic() - start) * 1000),
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
            get_event_bus().publish(LazyEvent(
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
            ))
        except Exception:
            pass


def get_executor() -> CommandExecutor:
    return CommandExecutor.instance()
