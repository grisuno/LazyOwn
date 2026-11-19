"""Declarative verb capability registry for the unattended loop.

Some LazyOwn verbs need root or a controlling terminal to run their privileged
primitive: ``lazynmap`` launches a SYN scan under ``sudo``. In an unattended
loop with no tty and no passwordless sudo those verbs degrade or hang, and the
planner keeps re-proposing them, so the loop spins on a verb it can never run.

This registry declares a verb's requirements and the unprivileged fallback to
substitute, so one execution chokepoint can downgrade a privilege-needing verb
instead of looping. It is a pure data module with no framework imports.
"""

from __future__ import annotations

import os
import shlex

_CAPABILITIES: dict[str, dict[str, object]] = {
    "lazynmap": {
        "requires_root": True,
        "requires_tty": True,
        "fallback": "nmap -sT -sV --top-ports 100",
    },
}


def _verb_of(command: str) -> str:
    """Return the lowercased basename of a command's leading token."""
    try:
        head = shlex.split(command or "")[0]
    except (ValueError, IndexError):
        return ""
    return os.path.basename(head).lower()


def capability_of(command: str) -> dict[str, object]:
    """Return the capability record for a command's leading verb, or ``{}``."""
    return dict(_CAPABILITIES.get(_verb_of(command), {}))


def requires_privilege(command: str) -> bool:
    """Return True when the command's verb needs root or a tty to run honestly."""
    cap = _CAPABILITIES.get(_verb_of(command), {})
    return bool(cap.get("requires_root") or cap.get("requires_tty"))


def downgrade_for_unattended(command: str, target: str = "") -> tuple[str, str]:
    """Rewrite a privilege-needing verb to its unprivileged fallback.

    Args:
        command: Proposed command line.
        target: Resolved intent target; used to aim the fallback when the
            original command carried a positional host.

    Returns:
        ``(command, note)``: the original command and an empty note when no
        downgrade applies, else the fallback command and a reason string.
    """
    verb = _verb_of(command)
    cap = _CAPABILITIES.get(verb, {})
    fallback = str(cap.get("fallback", "") or "")
    if not fallback:
        return command, ""
    try:
        args = shlex.split(command)[1:]
    except (ValueError, IndexError):
        args = []
    host = target or next((arg for arg in args if not arg.startswith("-")), "")
    rewritten = f"{fallback} {host}".strip()
    return rewritten, f"{verb} needs root/tty; unattended downgrade to {fallback}"
