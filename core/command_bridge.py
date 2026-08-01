"""Lightweight command execution bridge between C2 bots and the LazyOwn CLI shell.

Lazy-loads the heavy shell infrastructure only when a command is actually
executed, reducing import-time overhead for C2 workers.
"""

from __future__ import annotations

import threading
from typing import Any


class CommandBridge:
    """Facade that lazy-loads LazyOwnShell for C2 bot command execution."""

    def __init__(self) -> None:
        self._shell: Any = None
        self._lock = threading.Lock()
        self._ready = False
        self._error: str | None = None

    @property
    def ready(self) -> bool:
        """Whether the bridge has been successfully initialized."""
        return self._ready

    @property
    def error(self) -> str | None:
        """Error message if initialization failed, or None."""
        return self._error

    def _ensure_shell(self) -> Any:
        """Lazy-load and initialize the LazyOwnShell singleton.

        Uses double-checked locking so the import and bootstrap happen at most
        once across all threads.

        Returns:
            The initialized LazyOwnShell instance.

        Raises:
            RuntimeError: If the shell could not be imported or initialized.
        """
        if self._shell is not None:
            return self._shell
        with self._lock:
            if self._shell is not None:
                return self._shell
            try:
                from lazyown import LazyOwnShell

                shell = LazyOwnShell()
                shell.onecmd("p")
                shell.onecmd("create_session_json")
                self._shell = shell
                self._ready = True
            except Exception as exc:
                self._error = str(exc)
                self._ready = False
                raise RuntimeError(
                    f"Failed to initialize LazyOwn shell: {exc}"
                ) from exc
        return self._shell

    def onecmd(self, command: str) -> str:
        """Execute a LazyOwn internal command via the shell.

        Captures all stdout output during execution and returns it as a string.
        All output (banners, status, errors) is included.

        Args:
            command: The LazyOwn command string to execute.

        Returns:
            The captured stdout output, or an error message on failure.
        """
        if not command or not command.strip():
            return ""
        try:
            shell = self._ensure_shell()
            with self._lock:
                import io
                import sys

                original_stdout = sys.stdout
                sys.stdout = io.StringIO()
                try:
                    shell.onecmd(command)
                    return sys.stdout.getvalue()
                finally:
                    sys.stdout = original_stdout
        except Exception as exc:
            return f"CommandBridge error: {exc}"

    def one_cmd(self, command: str) -> str:
        """Execute a command using the shell's one_cmd method.

        Uses the shell's built-in output capture (which may include AI
        enhancement depending on shell configuration).

        Args:
            command: The LazyOwn command string to execute.

        Returns:
            The command output as a string, or an error message on failure.
        """
        if not command or not command.strip():
            return ""
        try:
            shell = self._ensure_shell()
            with self._lock:
                return shell.one_cmd(command)
        except Exception as exc:
            return f"CommandBridge error: {exc}"

    def execute(self, command: str) -> str:
        """Alias for one_cmd. Execute any LazyOwn command.

        Args:
            command: The LazyOwn command string to execute.

        Returns:
            The command output as a string.
        """
        return self.one_cmd(command)


_bridge: CommandBridge | None = None
_bridge_lock = threading.Lock()


def get_bridge() -> CommandBridge:
    """Get or create the singleton CommandBridge instance.

    Returns:
        The shared CommandBridge, created on first call.
    """
    global _bridge
    if _bridge is not None:
        return _bridge
    with _bridge_lock:
        if _bridge is not None:
            return _bridge
        _bridge = CommandBridge()
    return _bridge
