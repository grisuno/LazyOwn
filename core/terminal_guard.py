"""Terminal state guard for interactive automation.

Child processes, curses apps, Rich ``Live`` regions and interrupted
prompts can leave a terminal in raw mode, with echo off, mouse
reporting on or the alternate screen active. This module snapshots the
termios attributes before the loop starts and restores them on exit,
atexit and explicit calls, then emits the standard sequences that undo
the modes a crashed child may have enabled.
"""

from __future__ import annotations

import atexit
import subprocess
import sys
from typing import Any

RESTORE_SEQUENCE = (
    b"\x1b[0m"  # reset attributes
    b"\x1b[?25h"  # show cursor
    b"\x1b[?1000l"  # mouse reporting off
    b"\x1b[?1002l"
    b"\x1b[?1003l"
    b"\x1b[?1006l"
    b"\x1b[?2004l"  # bracketed paste off
    b"\x1b[?1049l"  # leave alternate screen
)


def _tty_fd() -> int | None:
    """Return a writable tty fd for the process, or None when headless."""
    for stream in (sys.stdin, sys.stdout, sys.stderr):
        try:
            if stream is not None and stream.isatty():
                return stream.fileno()
        except Exception:
            continue
    return None


def emit_restore_sequences() -> None:
    """Write the mode-reset sequences to the controlling terminal.

    A crashed child can leave mouse tracking or the alternate screen on;
    those modes are not part of termios, so the bytes go straight to
    ``/dev/tty`` (or stdout when that is the tty).
    """
    try:
        with open("/dev/tty", "wb", buffering=0) as tty:
            tty.write(RESTORE_SEQUENCE)
            return
    except OSError:
        pass
    try:
        if sys.stdout is not None and sys.stdout.isatty():
            sys.stdout.write(RESTORE_SEQUENCE.decode("ascii"))
            sys.stdout.flush()
    except Exception:
        pass


def apply_stty_sane() -> None:
    """Best-effort ``stty sane`` fallback when termios restore fails."""
    try:
        with open("/dev/tty", "rb") as tty_in:
            subprocess.run(
                ["stty", "sane"], stdin=tty_in, check=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
            )
    except Exception:
        pass


class TerminalGuard:
    """Snapshot termios on enter and restore it on every exit path.

    Usage::

        with TerminalGuard():
            run_interactive_thing()

    The guard is reentrant-safe enough for nested use: each instance
    keeps its own snapshot and restores only its own.
    """

    def __init__(self) -> None:
        """Prepare an empty guard; the snapshot happens on ``__enter__``."""
        self._fd: int | None = None
        self._saved: Any = None
        self._restored = False

    def __enter__(self) -> TerminalGuard:
        """Capture current termios attributes when a tty is present."""
        try:
            import termios

            self._fd = _tty_fd()
            if self._fd is not None:
                self._saved = termios.tcgetattr(self._fd)
        except Exception:
            self._saved = None
        atexit.register(self.restore)
        return self

    def __exit__(self, *_exc: object) -> None:
        """Restore the terminal on context exit."""
        self.restore()

    def restore(self) -> None:
        """Restore saved termios, then reset extra terminal modes once."""
        if self._restored:
            return
        self._restored = True
        try:
            atexit.unregister(self.restore)
        except Exception:
            pass
        restored = False
        if self._saved is not None and self._fd is not None:
            try:
                import termios

                termios.tcsetattr(self._fd, termios.TCSADRAIN, self._saved)
                restored = True
            except Exception:
                restored = False
        if not restored:
            apply_stty_sane()
        emit_restore_sequences()


__all__ = ["RESTORE_SEQUENCE", "TerminalGuard", "apply_stty_sane", "emit_restore_sequences"]
