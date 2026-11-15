"""Target operating-system ground truth for the autonomous loop.

Single-responsibility contract extracted from the daemon ``_run_objective``
coroutine: infer the target operating system from an ICMP TTL probe and record
that inference as ground truth across every consumer that needs it — the world
model host entry, ``payload.json`` (so each fresh LazyOwn shell inherits the
correct ``os_id``) and ``sessions/os.json`` (so the ``run_lazynmap`` OS gate
skips a redundant probe).

Both functions never raise: an unreachable or ambiguous target yields
``"unknown"`` and the persistence step degrades each side effect independently
so a single failure never aborts the objective.
"""

from __future__ import annotations

import asyncio
import json
import logging
import re
import subprocess
from collections.abc import Callable
from pathlib import Path
from typing import Any

log = logging.getLogger("lazyown.daemon")

PING_TIMEOUT_S: float = 6.0
PING_WAIT_S: str = "2"
TTL_LINUX_MAX: int = 64
TTL_WINDOWS_MAX: int = 128

OS_LINUX: str = "linux"
OS_WINDOWS: str = "windows"
OS_UNKNOWN: str = "unknown"

_OS_ID_MAP: dict[str, str] = {OS_LINUX: "1", OS_WINDOWS: "2", OS_UNKNOWN: "4"}
_TTL_LINUX_VALUE: int = 64
_TTL_WINDOWS_VALUE: int = 128


async def detect_target_os(
    target: str,
    loop: asyncio.AbstractEventLoop,
) -> str:
    """Infer the target OS from ICMP TTL via a single ping probe.

    TTL heuristics (accounting for up to ~20 router hops consumed):
      TTL <= 64   -> Linux / Unix / macOS (default initial TTL = 64)
      TTL <= 128  -> Windows             (default initial TTL = 128)
      TTL > 128   -> Unknown / network device

    Args:
        target: Host to probe.
        loop: Event loop used to run the blocking ping off the hot path.

    Returns:
        One of ``'linux'``, ``'windows'`` or ``'unknown'``. An unreachable host
        returns ``'unknown'`` — callers must treat unknown as a signal to skip
        OS-specific tooling rather than defaulting to any platform.
    """
    try:
        proc = await asyncio.wait_for(
            loop.run_in_executor(
                None,
                lambda: subprocess.run(
                    ["ping", "-c", "1", "-W", PING_WAIT_S, target],
                    capture_output=True,
                    text=True,
                ),
            ),
            timeout=PING_TIMEOUT_S,
        )
        output = proc.stdout + proc.stderr
        match = re.search(r"ttl=(\d+)", output, re.IGNORECASE)
        if not match:
            log.debug("OS detection: no TTL in ping output for %s", target)
            return OS_UNKNOWN
        ttl = int(match.group(1))
        if ttl <= TTL_LINUX_MAX:
            return OS_LINUX
        if ttl <= TTL_WINDOWS_MAX:
            return OS_WINDOWS
        return OS_UNKNOWN
    except TimeoutError:
        log.debug("OS detection: ping timed out for %s", target)
        return OS_UNKNOWN
    except Exception as exc:
        log.debug("OS detection error for %s: %s", target, exc)
        return OS_UNKNOWN


def os_id_for(detected_os: str) -> str:
    """Map an OS label to the LazyOwn canonical ``os_id`` string.

    Args:
        detected_os: One of ``'linux'``, ``'windows'`` or ``'unknown'``.

    Returns:
        ``'1'`` (Linux), ``'2'`` (Windows) or ``'4'`` (Unknown).
    """
    return _OS_ID_MAP.get(detected_os, "4")


def persist_detected_os(
    objective_id: str,
    target: str,
    detected_os: str,
    world_model: Any,
    emit: Callable[[str, dict[str, Any]], None],
    load_payload: Callable[[], dict],
    sessions_dir: Path,
    payload_file: Path,
) -> None:
    """Record the detected OS as ground truth across every consumer.

    Emits ``OS_DETECTED`` then, when the OS is known, propagates it to the world
    model host hint, ``payload.json`` (``os_id``) and ``sessions/os.json``. Each
    side effect is guarded independently; a failure in one never blocks the
    others and never raises.

    Args:
        objective_id: Owning objective identifier (for event correlation).
        target: Host the OS was detected for.
        detected_os: One of ``'linux'``, ``'windows'`` or ``'unknown'``.
        world_model: World model with ``snapshot``/``update_host``; may be None.
        emit: Event emitter ``(name, payload) -> None``.
        load_payload: Callable returning the current ``payload.json`` as a dict.
        sessions_dir: Sessions directory that holds ``os.json``.
        payload_file: Path of ``payload.json`` to rewrite with ``os_id``.
    """
    emit(
        "OS_DETECTED",
        {"objective_id": objective_id, "target": target, "os": detected_os},
    )

    if detected_os == OS_UNKNOWN:
        return

    if world_model is not None:
        try:
            snapshot = world_model.snapshot()
            host_entry = snapshot.get("hosts", {}).get(target, {})
            if not host_entry.get("os_hint"):
                world_model.update_host(target, os_hint=detected_os)
        except Exception as wm_exc:
            log.debug("world_model OS update error: %s", wm_exc)

    detected_os_id = os_id_for(detected_os)
    try:
        payload = load_payload()
        if payload.get("os_id") != detected_os_id:
            payload["os_id"] = detected_os_id
            from core.config import save_payload

            save_payload(payload, payload_file)
            log.info(
                "[%s] payload.json os_id updated: %s (%s)",
                objective_id,
                detected_os_id,
                detected_os,
            )
    except Exception as pe:
        log.debug("payload.json os_id update error: %s", pe)

    try:
        os_entry = [
            {
                "id": detected_os_id,
                "os": detected_os.capitalize(),
                "ttl": _TTL_LINUX_VALUE
                if detected_os == OS_LINUX
                else (_TTL_WINDOWS_VALUE if detected_os == OS_WINDOWS else "NULL"),
                "state": "active" if detected_os != OS_UNKNOWN else "unknown",
            }
        ]
        os_json_path = sessions_dir / "os.json"
        os_json_path.write_text(
            json.dumps(os_entry, indent=4, ensure_ascii=False), encoding="utf-8"
        )
    except Exception as oe:
        log.debug("sessions/os.json write error: %s", oe)
