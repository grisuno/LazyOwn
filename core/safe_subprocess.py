"""Safe subprocess runner for the LazyOwn framework.

Contract: this module replaces the legacy ``subprocess.run(..., shell=True, ...)``
call sites that pepper :mod:`utils` and :mod:`lazyc2`. The default
behaviour is to refuse shell execution; callers that genuinely need the
shell must pass ``allow=True`` and a free-text ``reason`` that is
recorded in the audit log together with the returncode.

Invariants:

1. :meth:`SafeRunner.run_shell` raises :class:`ShellNotAllowedError` when
   ``allow`` is missing or ``False``.
2. :meth:`SafeRunner.run_shell` requires a non-empty ``reason``; an
   empty string raises :class:`ValueError`.
3. :meth:`SafeRunner.run` (argv list) is always allowed and never audits.
4. The audit log, when configured, receives a single JSON line per
   ``run_shell`` call (allowed and denied attempts alike).
5. The returned :class:`SafeRunResult` exposes ``returncode``,
   ``stdout``, ``stderr`` and ``duration_seconds``.

Config keys owned: none (the audit log path is supplied at construction).
"""

from __future__ import annotations

import json
import shlex
import subprocess
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Sequence


class ShellNotAllowedError(PermissionError):
    """Raised when a shell invocation is attempted without ``allow=True``."""


@dataclass(frozen=True)
class SafeRunResult:
    """Outcome of a :class:`SafeRunner` invocation.

    Attributes:
        returncode: The exit code of the process.
        stdout: Captured standard output.
        stderr: Captured standard error.
        duration_seconds: Wall-clock execution time.
    """

    returncode: int
    stdout: str
    stderr: str
    duration_seconds: float


class SafeRunner:
    """Default-deny shell runner used by the LazyOwn framework.

    Args:
        audit_log_path: Optional filesystem path. When provided, every
            ``run_shell`` call is appended as a single JSON line.
    """

    __slots__ = ("_audit_log_path",)

    def __init__(self, audit_log_path: str | Path | None = None) -> None:
        self._audit_log_path = Path(audit_log_path) if audit_log_path is not None else None

    def run(self, argv: Sequence[str], *, timeout: float | None = None) -> SafeRunResult:
        """Execute ``argv`` without invoking a shell.

        Args:
            argv: The program and its arguments as a sequence of strings.
            timeout: Optional wall-clock timeout in seconds.

        Returns:
            A :class:`SafeRunResult` describing the outcome.

        Raises:
            FileNotFoundError: if the program does not exist.
            subprocess.TimeoutExpired: if the timeout elapses.
        """
        if not argv:
            raise ValueError("argv must contain at least the program name")
        start = time.monotonic()
        completed = subprocess.run(
            list(argv),
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )
        duration = time.monotonic() - start
        return SafeRunResult(
            returncode=completed.returncode,
            stdout=completed.stdout,
            stderr=completed.stderr,
            duration_seconds=duration,
        )

    def run_shell(
        self,
        command: str,
        *,
        allow: bool = False,
        reason: str = "",
        timeout: float | None = None,
    ) -> SafeRunResult:
        """Execute ``command`` through the system shell, gated by policy.

        Args:
            command: The shell command to run.
            allow: Must be ``True`` to execute; otherwise a
                :class:`ShellNotAllowedError` is raised (and audited).
            reason: Free-text justification, recorded in the audit log.
                Required when ``allow`` is ``True``.
            timeout: Optional wall-clock timeout in seconds.

        Returns:
            A :class:`SafeRunResult` describing the outcome.

        Raises:
            ShellNotAllowedError: when ``allow`` is not ``True``.
            ValueError: when ``allow`` is ``True`` but ``reason`` is empty.
        """
        argv = shlex.split(command) if command else []
        if not allow:
            self._audit({"allowed": False, "command": command, "reason": reason})
            raise ShellNotAllowedError(
                "SafeRunner.run_shell requires allow=True; "
                "pass a free-text reason explaining the call site."
            )
        if not reason or not reason.strip():
            raise ValueError("SafeRunner.run_shell requires a non-empty reason")
        if not argv:
            self._audit(
                {
                    "allowed": True,
                    "command": command,
                    "reason": reason,
                    "returncode": -1,
                    "error": "empty command after shlex split",
                }
            )
            return SafeRunResult(returncode=-1, stdout="", stderr="empty command", duration_seconds=0.0)
        start = time.monotonic()
        completed = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )
        duration = time.monotonic() - start
        self._audit(
            {
                "allowed": True,
                "command": command,
                "reason": reason,
                "returncode": completed.returncode,
                "duration_seconds": duration,
            }
        )
        return SafeRunResult(
            returncode=completed.returncode,
            stdout=completed.stdout,
            stderr=completed.stderr,
            duration_seconds=duration,
        )

    def _audit(self, record: dict[str, object]) -> None:
        if self._audit_log_path is None:
            return
        record = dict(record)
        record["timestamp"] = datetime.now(timezone.utc).isoformat()
        self._audit_log_path.parent.mkdir(parents=True, exist_ok=True)
        with self._audit_log_path.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(record, ensure_ascii=False) + "\n")


__all__ = ["SafeRunner", "SafeRunResult", "ShellNotAllowedError"]
