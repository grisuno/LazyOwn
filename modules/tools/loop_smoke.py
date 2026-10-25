"""End-to-end smoke of the shared loop runner (no LLM, no network).

Fakes the engine and shell, sandboxes the store, then exercises the
real ``modules.lazy_runner.run_loop`` path with the milestone panel:
bootstrap streaming, verb output visibility, result reporting and the
observer/redirect recursion guard. Reusable across dev sessions via
``python -m modules.tools.loop_smoke`` or ``run()`` from tests.
"""

from __future__ import annotations

import contextlib
import io
import tempfile
import time
from pathlib import Path

PROBE_TARGET = "127.0.0.1"
ORCHESTRATE_DELAY_SEC = 0.4


class FakeShell:
    """Shell stand-in whose verb prints like a real tool would."""

    def onecmd_plus_hooks(self, command: str) -> None:
        """Emit recognizable output for every routed verb."""
        print(f"Starting probe for {command.split()[-1]}")
        print("Nmap done: 1 IP address scanned")


class FakeEngine:
    """Minimal engine surface used by the runner and progress poller."""

    ORCHESTRATOR_CHAIN = ("lazy_task", "lazy_worker")

    def __init__(self) -> None:
        """Bind a sandboxed task store and runtime tracker."""
        from modules.lazy_loop import RuntimeTracker, TaskStore

        self.shell = None
        self.store = TaskStore()
        self.runtime = RuntimeTracker(self.store)

    def bind_shell(self, shell) -> None:
        """Record the bound shell (runner contract)."""
        self.shell = shell

    def set_concurrency(self, value) -> None:
        """Accept the concurrency knob without scheduling anything."""
        return None

    def create_task(self, goal: str, description: str = "") -> dict:
        """Create the task record and return its id."""
        return {"task_id": self.store.create(goal).task_id}

    def orchestrate(self, **kwargs) -> dict:
        """Run the injected executor once and report a done summary.

        The delay keeps the runner thread alive across several poll
        ticks, which is exactly where the transcript feedback loop used
        to hang without emitting anything.
        """
        output = kwargs["executor"]("auto_pwn 127.0.0.1")
        from modules.lazy_loop import ActivityLog

        ActivityLog(kwargs.get("task_id", "")).emit("engine", "round", "smoke round line from the activity bus")
        time.sleep(ORCHESTRATE_DELAY_SEC)
        return {
            "task_id": kwargs.get("task_id", ""),
            "status": "done",
            "rounds": 1,
            "overview": {"facts": 0},
            "verb_output": str(output),
        }


def run() -> dict:
    """Run the smoke and return ``{"ok": bool, "checks": {...}, "result": {...}}``."""
    import modules.lazy_engine as engine_module
    import modules.lazy_loop as loop
    import modules.lazy_runner as runner_module
    from modules.lazy_runner import LoopRunConfig, run_loop

    saved = (loop.STORE_DIR, loop._store_path, runner_module.SESSIONS_DIR, engine_module.LazyEngine)
    tmp = Path(tempfile.mkdtemp(prefix="lazy-loop-smoke-"))
    scan_dir = Path(tempfile.mkdtemp(prefix="lazy-loop-smoke-scans-"))
    (scan_dir / f"scan_{PROBE_TARGET}.nmap.xml").write_text("<nmaprun/>")
    loop.STORE_DIR = tmp
    loop._store_path = lambda name: tmp / name
    runner_module.SESSIONS_DIR = str(scan_dir)
    engine_module.LazyEngine = FakeEngine
    buffer = io.StringIO()
    try:
        with contextlib.redirect_stdout(buffer):
            result = run_loop(
                FakeShell(),
                {"proxy_autostart": False},
                LoopRunConfig(goal="probe surface", target=PROBE_TARGET, progress=True, rounds=1, workers=1),
            )
    finally:
        (loop.STORE_DIR, loop._store_path, runner_module.SESSIONS_DIR, engine_module.LazyEngine) = saved
    text = buffer.getvalue()
    checks = {
        "status_line_streamed": "running (rounds<=" in text,
        "activity_streamed": "[round] engine: smoke round line from the activity bus" in text,
        "bootstrap_streamed": ">>> auto_populate" in text,
        "verb_streamed": ">>> auto_pwn 127.0.0.1" in text,
        "verb_output_visible": "Nmap done: 1 IP address scanned" in text,
        "status_done": result.get("status") == "done" and not result.get("cancelled"),
    }
    return {"ok": all(checks.values()), "checks": checks, "result": result}


def main() -> int:
    """CLI entry point: print the checks and exit 0/1."""
    outcome = run()
    for name, passed in outcome["checks"].items():
        print(f"[{'ok' if passed else 'FAIL'}] {name}")
    print(f"status: {outcome['result'].get('status')}")
    return 0 if outcome["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
