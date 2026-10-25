"""Ephemeral infrastructure cleanup on shell exit.

Stops disposable assets (cyber range stacks, redirector tunnels, stray
``cloudflared`` processes) when the operator leaves the shell via Ctrl-D,
``quit``, ``qa`` or ``exit``. Everything here is best-effort and bounded:
cleanup must never block or crash the exit path.
"""

from __future__ import annotations

import os
import re
import shutil
import signal
import subprocess
import time
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DEPLOY_DIR = BASE_DIR / "deploy"
RANGE_DIR = DEPLOY_DIR / "range"
REDIRECTOR_COMPOSE = DEPLOY_DIR / "redirector" / "docker-compose.yml"
CLOUDFLARED_PATTERN = re.compile(r"cloudflared\s+tunnel")
PS_PID_PATTERN = re.compile(r"^\s*(\d+)\s+.*cloudflared\s+tunnel")
CLEANUP_TIMEOUT = 30


def find_cloudflared_pids(ps_output: str) -> list[int]:
    """Extract PIDs of ``cloudflared tunnel`` processes from ps output.

    Args:
        ps_output: Raw stdout of ``ps -eo pid,args``.

    Returns:
        Matching PIDs excluding the current process.
    """
    pids: list[int] = []
    own_pid = os.getpid()
    for line in (ps_output or "").splitlines():
        match = PS_PID_PATTERN.match(line)
        if not match:
            continue
        pid = int(match.group(1))
        if pid != own_pid:
            pids.append(pid)
    return pids


def _run_quiet(argv: list[str], timeout: int = CLEANUP_TIMEOUT) -> bool:
    """Run a teardown command, swallowing all failures.

    Args:
        argv: Argument vector, never a shell string.
        timeout: Seconds before aborting.

    Returns:
        True when the command exits zero.
    """
    try:
        result = subprocess.run(argv, capture_output=True, text=True, timeout=timeout, check=False)
    except (OSError, subprocess.TimeoutExpired):
        return False
    return result.returncode == 0


def _compose_down(compose_file: Path, label: str) -> bool:
    """Stop one compose stack when its containers exist.

    Args:
        compose_file: Compose file governing the stack.
        label: Human label for status output.

    Returns:
        True when the stack was stopped or nothing was running.
    """
    if not compose_file.exists() or shutil.which("docker") is None:
        return True
    try:
        running = subprocess.run(
            ["docker", "compose", "-f", str(compose_file), "ps", "-q"],
            capture_output=True,
            text=True,
            timeout=15,
            check=False,
        )
    except (OSError, subprocess.TimeoutExpired):
        return False
    if running.returncode != 0 or not (running.stdout or "").strip():
        return True
    print(f"[*] Stopping {label} ...")
    return _run_quiet(["docker", "compose", "-f", str(compose_file), "down"])


def stop_cloudflared_processes() -> int:
    """Terminate stray ``cloudflared tunnel`` host processes.

    Returns:
        Number of processes signalled.
    """
    if shutil.which("ps") is None:
        return 0
    try:
        listing = subprocess.run(["ps", "-eo", "pid,args"], capture_output=True, text=True, timeout=10, check=False)
    except (OSError, subprocess.TimeoutExpired):
        return 0
    if listing.returncode != 0:
        return 0
    signalled = 0
    for pid in find_cloudflared_pids(listing.stdout):
        try:
            os.kill(pid, signal.SIGTERM)
            signalled += 1
        except (OSError, ProcessLookupError):
            continue
    if signalled:
        time.sleep(1)
    return signalled


def cleanup_ephemeral_infra() -> dict[str, bool]:
    """Stop all disposable infrastructure owned by this checkout.

    Shuts down every range profile stack, the redirector stack, and stray
    ``cloudflared`` host processes. Safe to call when Docker is absent.

    Returns:
        Dict of teardown step name to success flag.
    """
    results: dict[str, bool] = {}
    if RANGE_DIR.exists():
        for compose_file in sorted(RANGE_DIR.glob("*/docker-compose.yml")):
            results[f"range:{compose_file.parent.name}"] = _compose_down(
                compose_file, f"range {compose_file.parent.name}"
            )
    results["redirector"] = _compose_down(REDIRECTOR_COMPOSE, "redirectors")
    try:
        stopped = stop_cloudflared_processes()
        results["cloudflared"] = True
        if stopped:
            print(f"[*] Stopped {stopped} stray cloudflared tunnel(s).")
    except Exception:
        results["cloudflared"] = False
    return results


__all__ = ["cleanup_ephemeral_infra", "find_cloudflared_pids", "stop_cloudflared_processes"]
