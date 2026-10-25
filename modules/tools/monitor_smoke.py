"""Headless smoke of the Textual worker monitor (``lazy_view``).

Sandboxes the store, seeds one task with activity and a guard audit
record, then drives the real :class:`cli.lazy_monitor.LazyMonitorApp`
through Textual's ``run_test`` pilot (compose, poll, tab and control
keys). No tty, no network. Reusable via ``python -m
modules.tools.monitor_smoke`` or ``run()`` from tests.
"""

from __future__ import annotations

import asyncio
import tempfile
from pathlib import Path

PAUSE_SEC = 0.8
KEYS = ("g", "t", "p", "r")


def run() -> dict:
    """Run the monitor smoke and return ``{"ok": bool, "checks": {...}}``."""
    import modules.lazy_loop as loop

    saved = (loop.STORE_DIR, loop._store_path)
    tmp = Path(tempfile.mkdtemp(prefix="lazy-monitor-smoke-"))
    loop.STORE_DIR = tmp
    loop._store_path = lambda name: tmp / name
    try:
        from modules.lazy_engine import LazyEngine

        engine = LazyEngine()
        task_id = engine.create_task("gain initial access on 127.0.0.1")["task_id"]
        activity = loop.ActivityLog(task_id)
        activity.emit("worker-1", "tool", "[allow] nmap -sV 127.0.0.1", intent_id=0)
        activity.emit("worker-1", "result", "22/tcp open ssh", intent_id=0)
        loop.Guard(task_id).check("Bash", "rm -rf /", source="worker")

        from cli.lazy_monitor import LazyMonitorApp

        async def _drive() -> LazyMonitorApp:
            app = LazyMonitorApp(task_id=task_id)
            async with app.run_test() as pilot:
                await pilot.pause(PAUSE_SEC)
                await pilot.press(*KEYS)
                await pilot.pause(0.4)
            return app

        app = asyncio.run(_drive())
        checks = {
            "task_bound": app.task_id == task_id,
            "stages_rendered": app._stages is not None,
            "worker_panes": bool(app._panes),
        }
    finally:
        loop.STORE_DIR, loop._store_path = saved
    return {"ok": all(checks.values()), "checks": checks, "task_id": task_id}


def main() -> int:
    """CLI entry point: print the checks and exit 0/1."""
    outcome = run()
    for name, passed in outcome["checks"].items():
        print(f"[{'ok' if passed else 'FAIL'}] {name}")
    print(f"task: {outcome['task_id']}")
    return 0 if outcome["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
