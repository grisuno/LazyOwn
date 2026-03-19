#!/usr/bin/env python3
"""
LazyOwn Unified Daemon
======================
Replaces three separate background processes with a single asyncio daemon:

  Role 1 — File Watcher     (was: sessions_watcher.py)
    Watches sessions/ for new/modified files:
    - scan_*.nmap     → generate plan.txt via Ollama, inject PLAN_READY objective
    - scan_*.nmap.xml → ingest into FactStore, update soul.md OS hint
    - sessions/<ip>/<port>/<tool>/*.txt → ingest into FactStore, update soul.md creds
    - sessions/plan.txt → emit PLAN_UPDATED event

  Role 2 — Event Engine Poll (was: heartbeat.py + event_engine CSV tail)
    Every N seconds: tail LazyOwn_session_report.csv for new rows →
    run rule matching → emit matched events to events.jsonl

  Role 3 — Heartbeat        (was: heartbeat.py)
    Every 30 seconds: emit a HEARTBEAT event so the MCP can verify the daemon
    is alive; update sessions/daemon_status.json with uptime and stats.

Communication:
  All roles share a single asyncio.Queue for internal events.
  External consumers (MCP) read sessions/events.jsonl as before — no interface change.

Management:
  python3 skills/lazyown_daemon.py start    # fork and detach
  python3 skills/lazyown_daemon.py stop     # kill via PID file
  python3 skills/lazyown_daemon.py status   # print status from daemon_status.json
  python3 skills/lazyown_daemon.py run      # run in foreground (for debugging)

PID file: sessions/daemon.pid
Status file: sessions/daemon_status.json
"""

from __future__ import annotations

import asyncio
import datetime
import json
import logging
import os
import signal
import sys
import time
from pathlib import Path
from typing import Optional

# ── Paths ─────────────────────────────────────────────────────────────────────

BASE_DIR     = Path(__file__).parent.parent
SESSIONS_DIR = BASE_DIR / "sessions"
SKILLS_DIR   = Path(__file__).parent
MODULES_DIR  = BASE_DIR / "modules"

PID_FILE    = SESSIONS_DIR / "daemon.pid"
STATUS_FILE = SESSIONS_DIR / "daemon_status.json"

# ── sys.path setup ────────────────────────────────────────────────────────────

for _p in (str(SKILLS_DIR), str(MODULES_DIR)):
    if _p not in sys.path:
        sys.path.insert(0, _p)

# ── Logging ───────────────────────────────────────────────────────────────────

logging.basicConfig(
    level=logging.INFO,
    format="[daemon] %(asctime)s %(levelname)s %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger("lazyown_daemon")

# ── Import shared logic from existing modules ─────────────────────────────────

# sessions_watcher dispatch functions (re-used directly)
try:
    import sessions_watcher as _sw
    _dispatch        = _sw._dispatch
    _WATCHER_AVAILABLE = True
    try:
        from watchdog.events import FileSystemEventHandler
        from watchdog.observers import Observer
        _WATCHDOG_AVAILABLE = True
    except ImportError:
        _WATCHDOG_AVAILABLE = False
except ImportError:
    _WATCHER_AVAILABLE = False
    _WATCHDOG_AVAILABLE = False
    log.warning("sessions_watcher not importable — file watcher disabled")

    def _dispatch(path: Path) -> None:  # type: ignore[misc]
        pass

# event_engine process_new_rows
try:
    from event_engine import process_new_rows, _append_event
    _ENGINE_AVAILABLE = True
except ImportError:
    _ENGINE_AVAILABLE = False
    log.warning("event_engine not importable — event engine loop disabled")

    def process_new_rows() -> int:  # type: ignore[misc]
        return 0

    def _append_event(ev: dict) -> None:  # type: ignore[misc]
        pass

# optional: session_state and timeline_narrator (from heartbeat.py)
try:
    from session_state import refresh as _state_refresh
    _STATE_OK = True
except ImportError:
    _STATE_OK = False

try:
    from timeline_narrator import narrate as _narrate
    _NARRATOR_OK = True
except ImportError:
    _NARRATOR_OK = False

# ── Config (env-overridable) ──────────────────────────────────────────────────

ENGINE_INTERVAL_S   = float(os.environ.get("DAEMON_ENGINE_INTERVAL",  "5"))
WATCHER_POLL_S      = float(os.environ.get("DAEMON_WATCHER_POLL",     "3"))
HEARTBEAT_INTERVAL_S = float(os.environ.get("DAEMON_HEARTBEAT_INTERVAL", "30"))
STATE_EVERY_N       = int(os.environ.get("DAEMON_STATE_EVERY",  "3"))   # engine cycles
NARRATE_EVERY_N     = int(os.environ.get("DAEMON_NARRATE_EVERY", "12"))  # engine cycles

# ── Shared stats (mutated by all coroutines) ──────────────────────────────────

_stats = {
    "started_at":      None,
    "files_processed": 0,
    "events_emitted":  0,
}


# ── Role 1 — File Watcher ─────────────────────────────────────────────────────

async def file_watcher_loop(queue: asyncio.Queue) -> None:
    """Watch sessions/ for new/modified files and dispatch handlers."""
    SESSIONS_DIR.mkdir(parents=True, exist_ok=True)

    if _WATCHDOG_AVAILABLE and _WATCHER_AVAILABLE:
        await _watchdog_async(queue)
    else:
        log.info(
            f"poll-based file watcher active (interval={WATCHER_POLL_S}s) — "
            "install watchdog for inotify-based watching"
        )
        await _poll_watcher_loop(queue)


async def _poll_watcher_loop(queue: asyncio.Queue) -> None:
    """Async polling fallback: walk sessions/ every WATCHER_POLL_S seconds."""
    snapshot: dict[str, float] = {}

    def _scan() -> dict[str, float]:
        result: dict[str, float] = {}
        try:
            for root, _dirs, files in os.walk(SESSIONS_DIR):
                for fname in files:
                    fp = Path(root) / fname
                    try:
                        result[str(fp)] = fp.stat().st_mtime
                    except OSError:
                        pass
        except Exception:
            pass
        return result

    loop = asyncio.get_event_loop()
    snapshot = await loop.run_in_executor(None, _scan)

    while True:
        await asyncio.sleep(WATCHER_POLL_S)
        current = await loop.run_in_executor(None, _scan)
        changed = [p for p, mt in current.items()
                   if p not in snapshot or snapshot[p] != mt]
        for path_str in changed:
            await queue.put(("FILE", Path(path_str)))
        snapshot = current


async def _watchdog_async(queue: asyncio.Queue) -> None:
    """Run watchdog Observer in a thread, push events to queue."""
    import threading
    loop = asyncio.get_event_loop()

    class _Handler(FileSystemEventHandler):  # type: ignore[misc]
        def _push(self, src: str):
            asyncio.run_coroutine_threadsafe(
                queue.put(("FILE", Path(src))), loop
            )

        def on_created(self, event):
            if not event.is_directory:
                self._push(event.src_path)

        def on_modified(self, event):
            if not event.is_directory:
                self._push(event.src_path)

    observer = Observer()
    observer.schedule(_Handler(), str(SESSIONS_DIR), recursive=True)
    observer.start()
    log.info(f"watchdog observer active on {SESSIONS_DIR}")

    try:
        while True:
            await asyncio.sleep(1)
    except asyncio.CancelledError:
        observer.stop()
        observer.join()
        raise


async def file_event_consumer(queue: asyncio.Queue) -> None:
    """Consume FILE events from the queue and call _dispatch in executor."""
    loop = asyncio.get_event_loop()
    while True:
        tag, path = await queue.get()
        if tag == "FILE":
            try:
                await loop.run_in_executor(None, _dispatch, path)
                _stats["files_processed"] += 1
            except Exception as exc:
                log.warning(f"dispatch error for {path}: {exc}")
        queue.task_done()


# ── Role 2 — Event Engine Poll ────────────────────────────────────────────────

async def event_engine_loop() -> None:
    """Tail CSV, match rules, emit events — every ENGINE_INTERVAL_S seconds."""
    cycle = 0
    loop  = asyncio.get_event_loop()

    while True:
        await asyncio.sleep(ENGINE_INTERVAL_S)
        cycle += 1

        if _ENGINE_AVAILABLE:
            try:
                n = await loop.run_in_executor(None, process_new_rows)
                if n:
                    _stats["events_emitted"] += n
                    log.info(f"event engine: {n} new event(s) emitted")
            except Exception as exc:
                log.warning(f"event engine error: {exc}")

        if _STATE_OK and cycle % STATE_EVERY_N == 0:
            try:
                state = await loop.run_in_executor(None, _state_refresh)
                log.info(
                    f"session state refreshed — phase={state.get('phase')} "
                    f"hosts={len(state.get('hosts', []))} "
                    f"pending={state.get('open_event_count', 0)}"
                )
            except Exception as exc:
                log.debug(f"state refresh error: {exc}")

        if _NARRATOR_OK and cycle % NARRATE_EVERY_N == 0:
            try:
                await loop.run_in_executor(None, lambda: _narrate(force=False))
                log.info("timeline narrator updated")
            except Exception as exc:
                log.debug(f"narrator error: {exc}")


# ── Role 3 — Heartbeat ────────────────────────────────────────────────────────

async def heartbeat_loop() -> None:
    """Emit HEARTBEAT event and write daemon_status.json every 30 seconds."""
    import uuid as _uuid

    while True:
        await asyncio.sleep(HEARTBEAT_INTERVAL_S)

        started = _stats["started_at"]
        uptime  = (
            (datetime.datetime.now(datetime.timezone.utc) - started).total_seconds()
            if started else 0
        )

        status = {
            "pid":             os.getpid(),
            "uptime_s":        round(uptime, 1),
            "started_at":      started.isoformat() if started else None,
            "files_processed": _stats["files_processed"],
            "events_emitted":  _stats["events_emitted"],
            "updated_at":      datetime.datetime.now(datetime.timezone.utc).isoformat(),
        }

        try:
            STATUS_FILE.write_text(json.dumps(status, indent=2))
        except Exception as exc:
            log.debug(f"status file write error: {exc}")

        hb_event = {
            "id":        _uuid.uuid4().hex[:8],
            "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "type":      "HEARTBEAT",
            "severity":  "info",
            "rule_id":   "daemon_heartbeat",
            "source":    {"pid": os.getpid(), "uptime_s": round(uptime, 1)},
            "suggest":   "Daemon is alive.",
            "status":    "pending",
        }
        try:
            _append_event(hb_event)
            _stats["events_emitted"] += 1
        except Exception as exc:
            log.debug(f"heartbeat event error: {exc}")

        log.info(f"heartbeat — uptime={round(uptime)}s files={_stats['files_processed']} "
                 f"events={_stats['events_emitted']}")


# ── Main asyncio entrypoint ───────────────────────────────────────────────────

async def _main_async() -> None:
    _stats["started_at"] = datetime.datetime.now(datetime.timezone.utc)
    SESSIONS_DIR.mkdir(parents=True, exist_ok=True)

    queue: asyncio.Queue = asyncio.Queue()

    tasks = [
        asyncio.create_task(file_watcher_loop(queue),    name="file_watcher"),
        asyncio.create_task(file_event_consumer(queue),  name="file_consumer"),
        asyncio.create_task(event_engine_loop(),          name="event_engine"),
        asyncio.create_task(heartbeat_loop(),             name="heartbeat"),
    ]

    log.info(f"LazyOwn daemon started (pid={os.getpid()})")

    loop = asyncio.get_event_loop()
    for sig in (signal.SIGTERM, signal.SIGINT):
        loop.add_signal_handler(sig, lambda: [t.cancel() for t in tasks])

    try:
        await asyncio.gather(*tasks)
    except asyncio.CancelledError:
        log.info("daemon shutting down")
    finally:
        STATUS_FILE.write_text(json.dumps({"status": "stopped", "pid": os.getpid()}, indent=2))
        _clear_pid()


# ── PID management ────────────────────────────────────────────────────────────

def _write_pid() -> None:
    SESSIONS_DIR.mkdir(parents=True, exist_ok=True)
    PID_FILE.write_text(str(os.getpid()))


def _clear_pid() -> None:
    if PID_FILE.exists():
        PID_FILE.unlink()


def _read_pid() -> Optional[int]:
    try:
        return int(PID_FILE.read_text().strip())
    except Exception:
        return None


def _is_running() -> tuple[bool, int]:
    pid = _read_pid()
    if pid is None:
        return False, 0
    try:
        os.kill(pid, 0)
        return True, pid
    except (ProcessLookupError, PermissionError):
        return False, 0


# ── CLI commands ──────────────────────────────────────────────────────────────

def cmd_run() -> None:
    """Run in foreground."""
    _write_pid()
    try:
        asyncio.run(_main_async())
    finally:
        _clear_pid()


def cmd_start() -> None:
    """Fork, detach, and run in background."""
    running, pid = _is_running()
    if running:
        print(f"[daemon] already running (pid={pid})")
        sys.exit(1)

    pid = os.fork()
    if pid > 0:
        # parent
        print(f"[daemon] started in background (pid={pid})")
        sys.exit(0)

    # child: detach from terminal
    os.setsid()
    pid2 = os.fork()
    if pid2 > 0:
        sys.exit(0)

    # grandchild: redirect stdio
    sys.stdout.flush()
    sys.stderr.flush()
    with open(os.devnull, "r") as devnull:
        os.dup2(devnull.fileno(), sys.stdin.fileno())
    log_path = SESSIONS_DIR / "daemon.log"
    with open(log_path, "a") as logf:
        os.dup2(logf.fileno(), sys.stdout.fileno())
        os.dup2(logf.fileno(), sys.stderr.fileno())

    _write_pid()
    asyncio.run(_main_async())


def cmd_stop() -> None:
    """Send SIGTERM to the running daemon."""
    running, pid = _is_running()
    if not running:
        print("[daemon] not running")
        sys.exit(1)
    os.kill(pid, signal.SIGTERM)
    print(f"[daemon] sent SIGTERM to pid={pid}")
    # wait up to 5s
    for _ in range(50):
        time.sleep(0.1)
        alive, _ = _is_running()
        if not alive:
            print("[daemon] stopped")
            return
    print("[daemon] still running after 5s — try SIGKILL manually")


def cmd_status() -> None:
    """Print status from daemon_status.json."""
    running, pid = _is_running()
    if not running:
        print("[daemon] not running")
    else:
        print(f"[daemon] running (pid={pid})")

    if STATUS_FILE.exists():
        try:
            data = json.loads(STATUS_FILE.read_text())
            for k, v in data.items():
                print(f"  {k}: {v}")
        except Exception:
            print("  (status file unreadable)")
    else:
        print("  (no status file yet)")


# ── Entry point ───────────────────────────────────────────────────────────────

_COMMANDS = {
    "run":    cmd_run,
    "start":  cmd_start,
    "stop":   cmd_stop,
    "status": cmd_status,
}

if __name__ == "__main__":
    if len(sys.argv) < 2 or sys.argv[1] not in _COMMANDS:
        print(f"Usage: {sys.argv[0]} {{run|start|stop|status}}")
        sys.exit(1)
    _COMMANDS[sys.argv[1]]()
