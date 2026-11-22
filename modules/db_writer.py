"""Single-writer asynchronous queue for campaign database writes.

Routine autonomous-loop traffic must never open SQLite on the hot path.
This module owns one background writer thread bound to a single
:class:`modules.db.LazyOwnDB` connection. Because there is exactly one
writer and the database runs in WAL journal mode, concurrent readers are
never blocked and writes never contend for the database lock.

Callers enqueue a write operation and return immediately. Writes are
best-effort: a full queue drops the operation with a debug log and the
caller is never blocked, and an operation that raises is logged and
discarded without affecting the queue or the caller.

The public entry points are :func:`submit_write` (fire-and-forget) and
:func:`get_write_queue` (the process-wide singleton). :meth:`DBWriteQueue.flush`
drains the queue deterministically for tests and graceful shutdown.
"""

from __future__ import annotations

import logging
import queue
import threading
import time
from collections.abc import Callable

from modules.db import LazyOwnDB, get_db

logger = logging.getLogger(__name__)

WriteOp = Callable[[LazyOwnDB], None]

DEFAULT_MAX_QUEUE = 2048
DEFAULT_FLUSH_TIMEOUT = 5.0
FLUSH_POLL_SECONDS = 0.01
WRITER_THREAD_NAME = "lazyown-db-writer"


class DBWriteQueue:
    """Serialize campaign database writes onto one background writer thread.

    The queue starts its writer thread lazily on the first submitted
    operation. Operations are plain callables that receive the shared
    :class:`LazyOwnDB` instance and perform their writes through it.

    Args:
        db_factory: Zero-argument callable returning the database the
            writer binds to. Defaults to :func:`modules.db.get_db`.
        max_queue: Bounded queue capacity. A full queue drops new
            operations so the caller never blocks.
        synchronous: When ``True`` operations run inline on
            :meth:`submit` instead of on the writer thread. Used by tests
            to make writes deterministic without a thread.
    """

    def __init__(
        self,
        db_factory: Callable[[], LazyOwnDB] = get_db,
        max_queue: int = DEFAULT_MAX_QUEUE,
        synchronous: bool = False,
    ) -> None:
        self._db_factory = db_factory
        self._queue: queue.Queue[WriteOp | None] = queue.Queue(maxsize=max_queue)
        self._synchronous = synchronous
        self._thread: threading.Thread | None = None
        self._lock = threading.Lock()
        self._db: LazyOwnDB | None = None
        self._dropped = 0
        self._processed = 0
        self._started = False
        self._stopping = False

    def _db_instance(self) -> LazyOwnDB:
        """Return the writer-owned database, creating it on first use."""
        if self._db is None:
            self._db = self._db_factory()
        return self._db

    def _ensure_thread(self) -> None:
        """Start the writer thread once, on first asynchronous submit."""
        if self._started:
            return
        with self._lock:
            if self._started:
                return
            self._stopping = False
            self._thread = threading.Thread(
                target=self._run,
                name=WRITER_THREAD_NAME,
                daemon=True,
            )
            self._started = True
            self._thread.start()

    def submit(self, op: WriteOp) -> bool:
        """Enqueue one write operation without blocking the caller.

        Args:
            op: Callable applied to the shared database by the writer.

        Returns:
            True when the operation was accepted (enqueued or, in
            synchronous mode, applied), False when the queue was full or
            the queue is stopping.
        """
        if self._stopping:
            return False
        if self._synchronous:
            self._apply(op)
            return True
        self._ensure_thread()
        try:
            self._queue.put_nowait(op)
            return True
        except queue.Full:
            with self._lock:
                self._dropped += 1
            logger.debug("db write queue full; dropping op (dropped=%d)", self._dropped)
            return False

    def _apply(self, op: WriteOp) -> None:
        """Run one operation against the database, never raising."""
        try:
            op(self._db_instance())
            with self._lock:
                self._processed += 1
        except Exception as exc:
            logger.debug("db write op failed: %s", exc)

    def _run(self) -> None:
        """Drain operations until a stop sentinel is received."""
        while True:
            op = self._queue.get()
            try:
                if op is None:
                    return
                self._apply(op)
            finally:
                self._queue.task_done()

    def flush(self, timeout: float = DEFAULT_FLUSH_TIMEOUT) -> bool:
        """Block until every queued operation has been processed.

        Args:
            timeout: Maximum seconds to wait for the queue to drain.

        Returns:
            True when the queue drained within the timeout, else False.
        """
        if self._synchronous or not self._started:
            return True
        deadline = time.monotonic() + timeout
        while time.monotonic() < deadline:
            if self._queue.unfinished_tasks == 0:
                return True
            time.sleep(FLUSH_POLL_SECONDS)
        return self._queue.unfinished_tasks == 0

    def stop(self, timeout: float = DEFAULT_FLUSH_TIMEOUT) -> None:
        """Signal the writer to exit and wait for it to finish.

        Args:
            timeout: Maximum seconds to wait for the writer thread.
        """
        self._stopping = True
        if not self._started:
            return
        try:
            self._queue.put_nowait(None)
        except queue.Full:
            self._queue.put(None)
        thread = self._thread
        if thread is not None:
            thread.join(timeout=timeout)
        with self._lock:
            self._started = False
            self._thread = None

    def stats(self) -> dict[str, int]:
        """Return queue counters for health and diagnostics surfaces.

        Returns:
            Mapping with ``processed``, ``dropped`` and ``pending`` counts.
        """
        with self._lock:
            return {
                "processed": self._processed,
                "dropped": self._dropped,
                "pending": self._queue.unfinished_tasks,
            }


_QUEUE: DBWriteQueue | None = None
_QUEUE_LOCK = threading.Lock()


def get_write_queue() -> DBWriteQueue:
    """Return the process-wide database write queue, creating it once."""
    global _QUEUE
    with _QUEUE_LOCK:
        if _QUEUE is None:
            _QUEUE = DBWriteQueue()
        return _QUEUE


def set_write_queue(write_queue: DBWriteQueue | None) -> None:
    """Replace the process-wide write queue (tests and shutdown)."""
    global _QUEUE
    with _QUEUE_LOCK:
        _QUEUE = write_queue


def submit_write(op: WriteOp) -> bool:
    """Enqueue one write on the process-wide queue without blocking."""
    return get_write_queue().submit(op)


__all__ = [
    "DBWriteQueue",
    "WriteOp",
    "get_write_queue",
    "set_write_queue",
    "submit_write",
]
