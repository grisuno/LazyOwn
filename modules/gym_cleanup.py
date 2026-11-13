"""Gym machine cleanup on LazyOwn exit.

Lab scenario containers (``lazyown-lab-*``) and cyber range containers
(``lazyown-range-*``) hold real memory and CPU on the operator host.
When an interactive operator shell closes through any path (quit, EOF,
SIGTERM, SIGHUP, atexit) every running gym machine is stopped so
nothing keeps leasing resources after the session. This is OPT-IN:
``"gym_cleanup_on_exit": true`` in ``payload.json`` enables it.

Autonomous and headless processes (dashboard loop subprocesses,
``-c`` runs, MCP workers) never stop gym machines — a loop subprocess
exiting used to kill the gym out from under the next run, which is why
operators kept finding the lab down after every auto_loop.
"""

from __future__ import annotations

import logging
import os
from typing import Any

log = logging.getLogger("gym_cleanup")

CONFIG_KEY = "gym_cleanup_on_exit"
AUTONOMOUS_ENV = "LAZYOWN_AUTONOMOUS"


def cleanup_enabled() -> bool:
    """Return whether exit cleanup is enabled (default off, opt-in)."""
    if os.environ.get(AUTONOMOUS_ENV, "") == "1":
        return False
    try:
        from core.config import load_payload

        payload = load_payload() or {}
    except Exception:
        return False
    value = payload.get(CONFIG_KEY, False)
    if isinstance(value, str):
        return value.strip().lower() in ("1", "true", "yes", "on")
    return bool(value)


def cleanup_gym_machines(verbose: bool = False) -> dict[str, Any]:
    """Stop every running lab and range machine.

    Args:
        verbose: When True, print one line per stopped machine group.

    Returns:
        Mapping with ``enabled``, ``labs`` and ``ranges`` stop results.
    """
    if not cleanup_enabled():
        if os.environ.get(AUTONOMOUS_ENV, "") == "1":
            print("gym cleanup skipped: autonomous process never stops gym machines", flush=True)
        elif verbose:
            print("gym cleanup disabled (payload.json gym_cleanup_on_exit not enabled)", flush=True)
        return {"enabled": False, "labs": {}, "ranges": {}}
    try:
        from modules import lab_runtime

        labs = lab_runtime.stop_all()
        ranges = lab_runtime.stop_ranges()
    except Exception as exc:
        log.warning("gym machine cleanup failed: %s", exc)
        return {"enabled": True, "labs": {}, "ranges": {}, "error": str(exc)}
    if verbose:
        stopped = list(labs.get("stopped", [])) + list(ranges.get("stopped", []))
        if stopped:
            print(f"gym cleanup: stopped {len(stopped)} machine(s): {', '.join(stopped)}", flush=True)
    return {"enabled": True, "labs": labs, "ranges": ranges}


__all__ = ["CONFIG_KEY", "cleanup_enabled", "cleanup_gym_machines"]
