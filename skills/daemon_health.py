"""Daemon health monitor — watchdog for the autonomous daemon and C2 listeners.

Writes periodic heartbeat timestamps and provides a simple liveness check
so other components (MCP, C2 API, CLI) can detect a crashed daemon.

Health file: ``sessions/daemon_health.json``

Usage:
    from skills.daemon_health import DaemonHealth, is_daemon_alive

    health = DaemonHealth()
    health.start(interval=5)   # background thread, writes every 5s
    ...
    if is_daemon_alive():
        print("daemon is running")
"""

from __future__ import annotations

import json
import os
import threading
import time
from datetime import UTC, datetime
from pathlib import Path

DEFAULT_HEALTH_FILE = "sessions/daemon_health.json"
DEFAULT_INTERVAL = 5
DEFAULT_TIMEOUT = 30


def _health_path() -> str:
    return os.environ.get("LAZYOWN_HEALTH_FILE", DEFAULT_HEALTH_FILE)


def is_daemon_alive(timeout: int = DEFAULT_TIMEOUT) -> bool:
    """Check whether the autonomous daemon wrote a heartbeat recently.

    Args:
        timeout: Maximum seconds since last heartbeat before considering dead.

    Returns:
        True when a heartbeat exists and was written within ``timeout`` seconds.
    """
    path = _health_path()
    if not os.path.exists(path):
        return False
    try:
        with open(path) as f:
            data = json.load(f)
        last = data.get("last_heartbeat_ts", 0)
        age = time.time() - last
        return age < timeout
    except (json.JSONDecodeError, OSError, ValueError):
        return False


def daemon_status(timeout: int = DEFAULT_TIMEOUT) -> dict:
    """Return the full daemon health snapshot.

    Args:
        timeout: Maximum seconds since last heartbeat.

    Returns:
        Dict with ``alive``, ``last_heartbeat``, ``uptime_seconds``,
        ``pid``, ``phase``, ``error_count`` keys.
    """
    path = _health_path()
    if not os.path.exists(path):
        return {"alive": False, "reason": "no_health_file"}

    try:
        with open(path) as f:
            data = json.load(f)
    except (json.JSONDecodeError, OSError):
        return {"alive": False, "reason": "corrupt_health_file"}

    last = data.get("last_heartbeat_ts", 0)
    age = time.time() - last
    alive = age < timeout

    return {
        "alive": alive,
        "last_heartbeat": datetime.fromtimestamp(last, tz=UTC).isoformat() if last else None,
        "age_seconds": round(age, 1),
        "uptime_seconds": round(data.get("uptime_seconds", 0), 1),
        "pid": data.get("pid"),
        "phase": data.get("phase"),
        "error_count": data.get("error_count", 0),
        "cycles_completed": data.get("cycles_completed", 0),
    }


class DaemonHealth:
    """Background thread that writes a heartbeat timestamp periodically.

    Args:
        interval: Seconds between heartbeats.
        health_file: Path to the health JSON file.
    """

    def __init__(self, interval: int = DEFAULT_INTERVAL, health_file: str | None = None):
        self._interval = interval
        self._health_file = health_file or _health_path()
        self._thread: threading.Thread | None = None
        self._stop_event = threading.Event()
        self._start_time: float | None = None
        self._error_count = 0
        self._cycles = 0
        self._phase = "idle"
        self._lock = threading.Lock()

    @property
    def error_count(self) -> int:
        with self._lock:
            return self._error_count

    @error_count.setter
    def error_count(self, value: int):
        with self._lock:
            self._error_count = value

    @property
    def phase(self) -> str:
        with self._lock:
            return self._phase

    @phase.setter
    def phase(self, value: str):
        with self._lock:
            self._phase = value

    def _write_heartbeat(self):
        uptime = time.time() - self._start_time if self._start_time else 0
        payload = {
            "pid": os.getpid(),
            "last_heartbeat_ts": time.time(),
            "uptime_seconds": round(uptime, 1),
            "cycles_completed": self._cycles,
            "error_count": self.error_count,
            "phase": self.phase,
        }
        Path(self._health_file).parent.mkdir(parents=True, exist_ok=True)
        with open(self._health_file, "w") as f:
            json.dump(payload, f)

    def _loop(self):
        while not self._stop_event.wait(self._interval):
            self._cycles += 1
            try:
                self._write_heartbeat()
            except Exception:
                pass

    def start(self):
        """Launch the heartbeat thread."""
        if self._thread and self._thread.is_alive():
            return
        self._start_time = time.time()
        self._stop_event.clear()
        self._thread = threading.Thread(target=self._loop, daemon=True, name="daemon-health")
        self._thread.start()

    def stop(self):
        """Stop the heartbeat thread."""
        self._stop_event.set()
        if self._thread:
            self._thread.join(timeout=5)
        if os.path.exists(self._health_file):
            try:
                os.remove(self._health_file)
            except OSError:
                pass

    def record_error(self):
        """Increment the error counter."""
        with self._lock:
            self._error_count += 1

    def set_phase(self, phase: str):
        """Update the current daemon phase."""
        with self._lock:
            self._phase = phase

    def increment_cycles(self):
        """Increment the completed cycles counter."""
        self._cycles += 1
