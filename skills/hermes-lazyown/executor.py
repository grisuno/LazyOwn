"""
LazyOwn command executor for the Hermes-LazyOwn integration.

Wraps subprocess interaction with the LazyOwn CLI in a robust,
timeout-aware, output-sanitizing layer.

Follows the Command pattern: each execution is encapsulated in an
ExecutionResult with metadata.
"""

import os
import select
import struct
import subprocess
import sys
import termios
from pathlib import Path
from typing import Any

from constants import Defaults, Paths


class ExecutionResult:
    """Immutable result of a LazyOwn command execution."""

    def __init__(
        self,
        stdout: str,
        stderr: str,
        returncode: int | None,
        timed_out: bool = False,
        duration_ms: float = 0.0,
    ) -> None:
        self.stdout = stdout
        self.stderr = stderr
        self.returncode = returncode
        self.timed_out = timed_out
        self.duration_ms = duration_ms

    @property
    def combined(self) -> str:
        """Return stdout and stderr combined."""
        parts = [self.stdout]
        if self.stderr:
            parts.append(f"[stderr]\n{self.stderr}")
        return "\n".join(parts)

    @property
    def success(self) -> bool:
        """Return True if the command exited cleanly and did not time out."""
        return not self.timed_out and (self.returncode == 0 or self.returncode is None)

    def __str__(self) -> str:
        status = "OK" if self.success else f"FAIL({self.returncode})"
        if self.timed_out:
            status = "TIMEOUT"
        return f"[{status} {self.duration_ms:.0f}ms] {self.stdout[:200]}"


class LazyOwnExecutor:
    """
    Executes commands against the LazyOwn CLI via subprocess.

    Uses a pseudo-terminal when available so that cmd2-based prompts
    and ANSI output are handled correctly.
    """

    def __init__(
        self,
        lazyown_dir: Path | None = None,
        timeout: int = Defaults.TIMEOUT_SECONDS,
    ) -> None:
        self._lazyown_dir = lazyown_dir or Paths.lazyown_dir()
        self._lazyown_py = self._lazyown_dir / "lazyown.py"
        self._default_timeout = timeout

    # ── Public API ──────────────────────────────────────────────────────────────

    def execute(self, command: str, timeout: int | None = None) -> ExecutionResult:
        """
        Execute a single LazyOwn command string.

        Args:
            command: The command to run (e.g., "lazynmap" or "set rhost 10.10.11.5").
            timeout: Seconds before killing the process. Defaults to constructor value.

        Returns:
            An ExecutionResult with stdout, stderr, and metadata.
        """
        if not self._lazyown_py.exists():
            return ExecutionResult(
                stdout="",
                stderr=f"lazyown.py not found at {self._lazyown_py}",
                returncode=-1,
            )

        to = timeout or self._default_timeout
        return self._run_via_subprocess(command, to)

    def execute_batch(self, commands: list[str], timeout: int | None = None) -> ExecutionResult:
        """
        Execute multiple commands in a single LazyOwn session.

        Args:
            commands: List of command strings.
            timeout: Total timeout for the entire batch.

        Returns:
            An ExecutionResult with combined output.
        """
        script = "\n".join(commands) + "\n"
        return self.execute(script, timeout)

    # ── Internal helpers ────────────────────────────────────────────────────────

    def _run_via_subprocess(self, command: str, timeout: int) -> ExecutionResult:
        """Execute via subprocess.Popen with PTY when available."""
        import time as time_module

        start = time_module.time()

        argv = [sys.executable, "-W", "ignore", str(self._lazyown_py)]
        env = os.environ.copy()
        env["TERM"] = "dumb"

        use_pty = self._has_pty()

        try:
            if use_pty:
                result = self._run_with_pty(argv, command, timeout, env)
            else:
                result = self._run_without_pty(argv, command, timeout, env)
        except Exception as exc:
            duration = (time_module.time() - start) * 1000
            return ExecutionResult(
                stdout="",
                stderr=f"Execution error: {exc}",
                returncode=-1,
                duration_ms=duration,
            )

        duration = (time_module.time() - start) * 1000
        return ExecutionResult(
            stdout=result.get("stdout", ""),
            stderr=result.get("stderr", ""),
            returncode=result.get("returncode"),
            timed_out=result.get("timed_out", False),
            duration_ms=duration,
        )

    def _run_without_pty(
        self, argv: list[str], command: str, timeout: int, env: dict[str, str]
    ) -> dict[str, Any]:
        """Run without PTY (fallback for constrained environments)."""
        proc = subprocess.Popen(
            argv,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=str(self._lazyown_dir),
            env=env,
        )
        try:
            stdout_b, stderr_b = proc.communicate(command.encode(), timeout=timeout)
            return {
                "stdout": stdout_b.decode(errors="replace").strip(),
                "stderr": stderr_b.decode(errors="replace").strip(),
                "returncode": proc.returncode,
                "timed_out": False,
            }
        except subprocess.TimeoutExpired:
            proc.kill()
            stdout_b, stderr_b = proc.communicate()
            return {
                "stdout": stdout_b.decode(errors="replace").strip(),
                "stderr": stderr_b.decode(errors="replace").strip(),
                "returncode": proc.returncode,
                "timed_out": True,
            }

    def _run_with_pty(
        self, argv: list[str], command: str, timeout: int, env: dict[str, str]
    ) -> dict[str, Any]:
        """Run with PTY for proper cmd2 shell handling."""
        import pty as pty_module

        master_fd, slave_fd = pty_module.openpty()

        proc = subprocess.Popen(
            argv,
            stdin=slave_fd,
            stdout=slave_fd,
            stderr=slave_fd,
            cwd=str(self._lazyown_dir),
            env=env,
        )
        os.close(slave_fd)

        stdout_chunks: list[bytes] = []
        timed_out = False

        try:
            os.write(master_fd, command.encode() + b"\n")
            os.write(master_fd, b"exit\n")

            while True:
                ready, _, _ = select.select([master_fd], [], [], timeout)
                if not ready:
                    timed_out = True
                    break
                try:
                    chunk = os.read(master_fd, 4096)
                except OSError:
                    break
                if not chunk:
                    break
                stdout_chunks.append(chunk)
        finally:
            try:
                os.close(master_fd)
            except OSError:
                pass
            if proc.poll() is None:
                proc.kill()
                proc.wait()

        stdout = b"".join(stdout_chunks).decode(errors="replace").strip()
        return {
            "stdout": stdout,
            "stderr": "",
            "returncode": proc.returncode,
            "timed_out": timed_out,
        }

    def _has_pty(self) -> bool:
        """Return True if the platform supports PTY subprocesses."""
        try:
            import pty as _pty_test
            return True
        except ImportError:
            return False
