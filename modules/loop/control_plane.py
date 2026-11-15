"""Operator control-plane precheck for the autonomous loop.

Single-responsibility contract extracted from the daemon ``_run_objective``
coroutine: the per-step operator control gate that runs before command
selection. It ends the objective when the target leaves the operator focus
list, and it blocks while the daemon is paused, resuming when unpaused or
ending the objective once the pause exceeds its ceiling.

Never raises: any control-plane error is logged and treated as "continue", so a
malfunctioning control file never stalls or aborts the loop.
"""

from __future__ import annotations

import asyncio
import logging
from collections.abc import Callable
from typing import Any

log = logging.getLogger("lazyown.daemon")


async def precheck_control(
    control: Any,
    target: str,
    objective_id: str,
    step_n: int,
    emit: Callable[[str, dict[str, Any]], None],
    loop: asyncio.AbstractEventLoop,
    wait_until_unpaused: Callable[..., bool] | None,
    poll_interval: float,
    max_wait: float,
) -> bool:
    """Run the per-step operator control gate.

    Args:
        control: Daemon control handle (focus/pause state); None disables the
            gate entirely.
        target: Host the current objective targets.
        objective_id: Owning objective identifier (for event correlation).
        step_n: Current step number (for event correlation).
        emit: Event emitter ``(name, payload) -> None``.
        loop: Event loop used to await the blocking pause wait off the hot path.
        wait_until_unpaused: Blocking pause-wait callable, or None when the
            pause helper is unavailable (pause handling is then skipped).
        poll_interval: Seconds between pause-state polls.
        max_wait: Pause ceiling in seconds; a longer pause ends the objective.

    Returns:
        True when the objective should stop (focus lost or pause ceiling
        exceeded); False to continue to command selection.
    """
    if control is None:
        return False
    try:
        if not control.target_in_focus(target):
            emit(
                "TARGET_OUT_OF_FOCUS",
                {
                    "objective_id": objective_id,
                    "target": target,
                    "focus": control.load().focus_targets,
                },
            )
            log.info(
                "  [control] target %s not in focus list — ending objective",
                target,
            )
            return True
        if control.is_paused() and wait_until_unpaused is not None:
            emit("DAEMON_PAUSED", {"objective_id": objective_id, "step": step_n})
            resumed = await loop.run_in_executor(
                None,
                lambda: wait_until_unpaused(
                    control,
                    poll_interval=poll_interval,
                    max_wait_seconds=max_wait,
                ),
            )
            if not resumed:
                emit(
                    "DAEMON_PAUSE_TIMEOUT",
                    {
                        "objective_id": objective_id,
                        "step": step_n,
                        "max_wait_s": max_wait,
                    },
                )
                log.info(
                    "  [control] paused beyond AUTO_PAUSE_MAX (%.0fs) — ending objective",
                    max_wait,
                )
                return True
            emit("DAEMON_RESUMED", {"objective_id": objective_id, "step": step_n})
    except Exception as ctl_exc:
        log.debug("control pre-step error: %s", ctl_exc)
    return False
