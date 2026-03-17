#!/usr/bin/env python3
"""
LazyOwn Heartbeat
=================
Lightweight background process that drives the event engine.
Runs the CSV-tail → rule-match → event-emit loop every N seconds.

Usage:
    python3 skills/heartbeat.py [--interval 5] [--once]

Options:
    --interval N   Poll interval in seconds (default: 5)
    --once         Run one pass and exit (useful for cron/testing)
    --daemon       Daemonize (write PID to sessions/heartbeat.pid)
"""

import argparse
import os
import sys
import time
from pathlib import Path

# Resolve project root
SKILLS_DIR  = Path(__file__).parent
LAZYOWN_DIR = SKILLS_DIR.parent
sys.path.insert(0, str(LAZYOWN_DIR / "modules"))

from event_engine import process_new_rows, read_events

PID_FILE = LAZYOWN_DIR / "sessions" / "heartbeat.pid"


def write_pid():
    PID_FILE.write_text(str(os.getpid()))


def clear_pid():
    if PID_FILE.exists():
        PID_FILE.unlink()


def is_running() -> tuple[bool, int]:
    """Return (is_running, pid). Checks if stored PID is still alive."""
    if not PID_FILE.exists():
        return False, 0
    try:
        pid = int(PID_FILE.read_text().strip())
        os.kill(pid, 0)   # signal 0 = existence check
        return True, pid
    except (ProcessLookupError, ValueError):
        return False, 0


def run_loop(interval: int, once: bool = False):
    write_pid()
    print(f"[heartbeat] started (pid={os.getpid()}, interval={interval}s)", flush=True)

    try:
        while True:
            try:
                n = process_new_rows()
                if n:
                    print(f"[heartbeat] {n} new event(s) emitted", flush=True)
                    # Print a brief digest of what fired
                    for ev in read_events(limit=n):
                        print(
                            f"  [{ev['severity'].upper()}] {ev['type']}"
                            f" ← {ev['source']['command']} @ {ev['source']['target']}",
                            flush=True
                        )
            except Exception as e:
                print(f"[heartbeat] error in engine: {e}", flush=True)

            if once:
                break
            time.sleep(interval)

    except KeyboardInterrupt:
        print("\n[heartbeat] stopped by user", flush=True)
    finally:
        clear_pid()


def main():
    parser = argparse.ArgumentParser(description="LazyOwn Heartbeat")
    parser.add_argument("--interval", type=int, default=5,
                        help="Poll interval in seconds (default: 5)")
    parser.add_argument("--once", action="store_true",
                        help="Run one pass and exit")
    parser.add_argument("--status", action="store_true",
                        help="Check if heartbeat is running and exit")
    args = parser.parse_args()

    if args.status:
        running, pid = is_running()
        if running:
            print(f"[heartbeat] running (pid={pid})")
        else:
            print("[heartbeat] not running")
        sys.exit(0)

    running, pid = is_running()
    if running and not args.once:
        print(f"[heartbeat] already running (pid={pid}). Use --once to force a single pass.")
        sys.exit(1)

    run_loop(args.interval, once=args.once)


if __name__ == "__main__":
    main()
