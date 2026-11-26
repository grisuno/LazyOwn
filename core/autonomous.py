"""Autonomous-run mode for the loop engine.

While the loop runs, interactive prompts have no operator in front of
them: ``input()`` calls from automation verbs must never steal the
keyboard from the shell. The context manager flips an environment flag
(so shell commands can detect unattended mode) and replaces
``builtins.input`` with a prompt-skipping stub that announces why the
default was taken.

The stub is thread-scoped, not process-wide: only the thread that entered
:func:`autonomous_mode` and threads spawned after it (loop workers) get
their prompts answered automatically. Threads that already existed when
the mode started — the operator's cmdloop thread in the C2 process, for
example — keep real interactive input, so an autonomous loop can no
longer auto-skip the operator's own prompts in another thread.
"""

from __future__ import annotations

import builtins
import contextlib
import os
import threading
from collections.abc import Iterator

AUTONOMOUS_ENV = "LAZYOWN_AUTONOMOUS"

_state_lock = threading.Lock()
_depth = 0
_owner_ident: int | None = None
_original_input = None
_pre_existing_idents: frozenset[int | None] = frozenset()


def is_autonomous() -> bool:
    """Return True while an autonomous loop run owns the process."""
    return os.environ.get(AUTONOMOUS_ENV) == "1"


def _guarded_input(prompt: object = "") -> str:
    """Answer prompts for loop-owned threads; delegate the rest.

    Args:
        prompt: Text handed to :func:`builtins.input`.

    Returns:
        The operator's typed answer on non-loop threads, or an empty
        string with an explanatory line for loop-owned threads.
    """
    if _original_input is None:
        raise RuntimeError("autonomous stub installed without an original input handler")
    ident = threading.get_ident()
    if ident != _owner_ident and ident in _pre_existing_idents:
        return _original_input(prompt)
    print(f"[!] autonomous mode: prompt auto-skipped: {str(prompt).strip()[:100]}")
    return ""


@contextlib.contextmanager
def autonomous_mode() -> Iterator[None]:
    """Suppress interactive prompts for the duration of a loop run.

    Yields:
        Control with prompts answered by an empty string on the entering
        thread and its descendants, ``LAZYOWN_AUTONOMOUS=1`` exported,
        and pre-existing threads untouched. Everything is restored on
        exit, including when an exception unwinds the block.
    """
    global _depth, _owner_ident, _original_input, _pre_existing_idents

    previous_env = os.environ.get(AUTONOMOUS_ENV)
    os.environ[AUTONOMOUS_ENV] = "1"
    with _state_lock:
        if _depth == 0:
            _original_input = builtins.input
            _owner_ident = threading.get_ident()
            _pre_existing_idents = frozenset(t.ident for t in threading.enumerate())
        _depth += 1
        builtins.input = _guarded_input
    try:
        yield
    finally:
        with _state_lock:
            _depth -= 1
            if _depth <= 0:
                _depth = 0
                if _original_input is not None:
                    builtins.input = _original_input
                _owner_ident = None
                _original_input = None
                _pre_existing_idents = frozenset()
        if previous_env is None:
            os.environ.pop(AUTONOMOUS_ENV, None)
        else:
            os.environ[AUTONOMOUS_ENV] = previous_env


__all__ = ["AUTONOMOUS_ENV", "autonomous_mode", "is_autonomous"]
