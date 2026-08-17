"""Shared interactive confirmation helpers with safe non-TTY behaviour.

Every interactive prompt in the CLI should go through :func:`confirm` so
agent-driven sessions (stdin closed or non-interactive) degrade gracefully
instead of crashing with ``EOFError`` or hanging on a prompt that can never
be answered.

Behaviour matrix:

    - TTY stdin: prompt and wait for y/n.
    - Non-TTY stdin (pipe/EOF): return ``default`` immediately.
    - Empty answer: return ``default``.
"""

from __future__ import annotations

import sys


def _read_line(prompt: str) -> str:
    try:
        return input(prompt).strip()
    except EOFError:
        return ""


def confirm(
    question: str,
    default: bool = False,
    yes_values: frozenset[str] = frozenset({"y", "yes", "s", "si"}),
) -> bool:
    """Ask a yes/no question, never raising on non-interactive stdin.

    Args:
        question: The question to show (a trailing `` [y/N] `` is appended).
        default: Answer returned when stdin is not a TTY or input is empty.
        yes_values: Case-insensitive answers treated as yes.

    Returns:
        True when the operator answered yes, False otherwise.
    """
    suffix = " [Y/n] " if default else " [y/N] "
    if not sys.stdin.isatty():
        return default
    answer = _read_line(question + suffix)
    if not answer:
        return default
    return answer.lower() in yes_values


__all__ = ["confirm"]
