"""Autonomous-run mode for the loop engine.

While the loop runs, interactive prompts have no operator in front of
them: ``input()`` calls from automation verbs must never steal the
keyboard from the shell. The context manager flips an environment flag
(so shell commands can detect unattended mode) and replaces
``builtins.input`` with a prompt-skipping stub that announces why the
default was taken.
"""

from __future__ import annotations

import builtins
import contextlib
import os
from collections.abc import Iterator

AUTONOMOUS_ENV = "LAZYOWN_AUTONOMOUS"


def is_autonomous() -> bool:
    """Return True while an autonomous loop run owns the process."""
    return os.environ.get(AUTONOMOUS_ENV) == "1"


@contextlib.contextmanager
def autonomous_mode() -> Iterator[None]:
    """Suppress interactive prompts for the duration of a loop run.

    Yields:
        Control with prompts answered by an empty string and
        ``LAZYOWN_AUTONOMOUS=1`` exported. Everything is restored on
        exit, including when an exception unwinds the block.
    """
    previous_env = os.environ.get(AUTONOMOUS_ENV)
    os.environ[AUTONOMOUS_ENV] = "1"
    original_input = builtins.input

    def _guarded_input(prompt: str = "") -> str:
        print(f"[!] autonomous mode: prompt auto-skipped: {str(prompt).strip()[:100]}")
        return ""

    builtins.input = _guarded_input
    try:
        yield
    finally:
        builtins.input = original_input
        if previous_env is None:
            os.environ.pop(AUTONOMOUS_ENV, None)
        else:
            os.environ[AUTONOMOUS_ENV] = previous_env


__all__ = ["AUTONOMOUS_ENV", "autonomous_mode", "is_autonomous"]
