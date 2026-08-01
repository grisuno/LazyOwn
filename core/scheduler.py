"""
Centralized task scheduler for the LazyOwn framework.

Uses ``apscheduler`` when available, falling back to a stdlib implementation
built on ``sched.scheduler`` and ``threading.Timer`` for environments where
the library is not installed. Thread-safe for concurrent task registration
and cancellation from any thread.

Usage::

    from core.scheduler import get_scheduler

    sched = get_scheduler()
    sched.start()
    sched.schedule_task("heartbeat", 30, send_heartbeat)
    sched.schedule_once("cleanup", 60, remove_temp_files)
    sched.stop()
"""

from __future__ import annotations

import logging
import sched
import threading
import time
from dataclasses import dataclass, field
from typing import Any, Callable, Optional

log = logging.getLogger("core.scheduler")

try:
    import apscheduler.schedulers.background as _apbg
    _HAS_APSCHEDULER = True
except ImportError:
    _HAS_APSCHEDULER = False


@dataclass
class _TaskInfo:
    name: str
    interval_seconds: int
    func: Callable[[], None]
    next_run: float
    recurring: bool
    active: bool = True


class TaskScheduler:
    """Thread-safe scheduler for recurring and one-shot tasks.

    Automatically selects ``apscheduler`` (BackgroundScheduler) when
    available, falling back to a stdlib implementation using
    ``sched.scheduler`` and ``threading.Timer`` otherwise.
    """

    _instance: Optional["TaskScheduler"] = None
    _instance_lock = threading.Lock()

    def __init__(self) -> None:
        self._lock = threading.RLock()
        self._tasks: dict[str, _TaskInfo] = {}
        self._running = False
        self._std_event: Optional[threading.Event] = None
        self._std_thread: Optional[threading.Thread] = None
        if _HAS_APSCHEDULER:
            self._backend: Any = _apbg.BackgroundScheduler(daemon=True)
        else:
            self._backend = sched.scheduler(time.time, time.sleep)

    @classmethod
    def instance(cls) -> "TaskScheduler":
        """Return the singleton ``TaskScheduler`` instance."""
        if cls._instance is None:
            with cls._instance_lock:
                if cls._instance is None:
                    cls._instance = cls()
        return cls._instance

    def start(self) -> None:
        """Start the scheduler background thread.

        Idempotent: calling ``start()`` on an already-running scheduler is a
        no-op.
        """
        with self._lock:
            if self._running:
                return
            self._running = True
            if _HAS_APSCHEDULER:
                self._backend.start()
                log.info("Scheduler started (apscheduler)")
            else:
                self._std_event = threading.Event()
                self._std_thread = threading.Thread(
                    target=self._run_stdlib_loop, daemon=True, name="lazyown-scheduler"
                )
                self._std_thread.start()
                log.info("Scheduler started (stdlib fallback)")

    def stop(self) -> None:
        """Stop the scheduler and cancel all pending tasks.

        Idempotent: calling ``stop()`` on an already-stopped scheduler is a
        no-op.
        """
        with self._lock:
            if not self._running:
                return
            self._running = False
            if _HAS_APSCHEDULER:
                self._backend.shutdown(wait=False)
            else:
                if self._std_event:
                    self._std_event.set()
                for _ in range(len(self._backend.queue)):
                    try:
                        self._backend.cancel(self._backend.queue[0])
                    except (ValueError, IndexError):
                        break
            self._tasks.clear()
            log.info("Scheduler stopped")

    def schedule_task(
        self, name: str, interval_seconds: int, func: Callable[[], None]
    ) -> None:
        """Register a recurring task to run every ``interval_seconds``.

        If a task with the same ``name`` already exists it is cancelled and
        replaced.

        Args:
            name: Unique identifier for the task.
            interval_seconds: Seconds between invocations.
            func: Zero-argument callable to invoke each cycle.
        """
        with self._lock:
            if name in self._tasks:
                self._cancel_internal(name)
            info = _TaskInfo(
                name=name,
                interval_seconds=interval_seconds,
                func=func,
                next_run=time.time() + interval_seconds,
                recurring=True,
            )
            self._tasks[name] = info
            if _HAS_APSCHEDULER:
                self._backend.add_job(
                    func,
                    "interval",
                    seconds=interval_seconds,
                    id=name,
                    replace_existing=True,
                )
            else:
                self._schedule_recurring_stdlib(info)
            log.debug("Scheduled recurring task %s (interval=%ds)", name, interval_seconds)

    def schedule_once(
        self, name: str, delay_seconds: int, func: Callable[[], None]
    ) -> None:
        """Register a one-shot task to run after ``delay_seconds``.

        If a task with the same ``name`` already exists it is cancelled and
        replaced.

        Args:
            name: Unique identifier for the task.
            delay_seconds: Seconds to delay before invocation.
            func: Zero-argument callable to invoke.
        """
        with self._lock:
            if name in self._tasks:
                self._cancel_internal(name)
            info = _TaskInfo(
                name=name,
                interval_seconds=delay_seconds,
                func=func,
                next_run=time.time() + delay_seconds,
                recurring=False,
            )
            self._tasks[name] = info
            if _HAS_APSCHEDULER:
                self._backend.add_job(
                    func,
                    "date",
                    run_date=time.time() + delay_seconds,
                    id=name,
                )
            else:
                timer = threading.Timer(
                    delay_seconds, self._run_once_wrapper(name, func)
                )
                timer.daemon = True
                timer.start()
            log.debug("Scheduled one-shot task %s (delay=%ds)", name, delay_seconds)

    def cancel_task(self, name: str) -> None:
        """Cancel a scheduled task by name.

        No error is raised if the task does not exist.

        Args:
            name: Identifier of the task to cancel.
        """
        with self._lock:
            self._cancel_internal(name)
            self._tasks.pop(name, None)
            log.debug("Cancelled task %s", name)

    def list_tasks(self) -> list[dict]:
        """Return metadata for all registered tasks.

        Returns:
            A list of dictionaries with keys ``name``, ``interval_seconds``,
            ``recurring``, ``active``, and ``next_run_iso``.
        """
        with self._lock:
            return [
                {
                    "name": t.name,
                    "interval_seconds": t.interval_seconds,
                    "recurring": t.recurring,
                    "active": t.active,
                    "next_run_iso": time.strftime(
                        "%Y-%m-%dT%H:%M:%S", time.localtime(t.next_run)
                    ),
                }
                for t in self._tasks.values()
            ]

    def _cancel_internal(self, name: str) -> None:
        """Cancel a task without holding ``_lock``.

        Called from within locked sections only.
        """
        if _HAS_APSCHEDULER:
            job = self._backend.get_job(name)
            if job:
                job.remove()
        else:
            info = self._tasks.get(name)
            if info:
                info.active = False

    def _schedule_recurring_stdlib(self, info: _TaskInfo) -> None:
        """Schedule a recurring task using ``sched.scheduler``."""
        def _wrapper() -> None:
            if not info.active or not self._running:
                return
            try:
                info.func()
            except Exception:
                log.exception("Recurring task %s failed", info.name)
            if info.active and self._running:
                info.next_run = time.time() + info.interval_seconds
                self._backend.enter(info.interval_seconds, 0, _wrapper)

        self._backend.enter(info.interval_seconds, 0, _wrapper)

    def _run_once_wrapper(
        self, name: str, func: Callable[[], None]
    ) -> Callable[[], None]:
        """Return a callable that invokes ``func`` once and removes the task."""

        def _wrapper() -> None:
            try:
                func()
            except Exception:
                log.exception("One-shot task %s failed", name)
            finally:
                with self._lock:
                    self._tasks.pop(name, None)

        return _wrapper

    def _run_stdlib_loop(self) -> None:
        """Main loop for the stdlib scheduler backend.

        Runs sched actions in a tight loop with a periodic check on the stop
        event, so ``stop()`` is responsive even when no events are pending.
        """
        delay = 0.5
        while self._running and not (self._std_event and self._std_event.is_set()):
            self._backend.run(blocking=False)
            time.sleep(delay)
        try:
            while not self._backend.empty():
                self._backend.run(blocking=False)
        except Exception:
            pass


def get_scheduler() -> TaskScheduler:
    """Return the singleton ``TaskScheduler`` instance."""
    return TaskScheduler.instance()
