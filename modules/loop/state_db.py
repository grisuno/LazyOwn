"""Shared SQLite state substrate for loop modules.

One WAL database (``sessions/db/loop_state.db``) backs the loop
primitives that need transactional cross-process semantics: claim
leases and token usage. The file lives under ``sessions/`` so it is
gitignored like every other campaign artefact.
"""

from __future__ import annotations

import sqlite3
import threading
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]
DB_DIRNAME = "sessions/db"
DB_FILENAME = "loop_state.db"
_BUSY_TIMEOUT_SEC = 10.0
_local = threading.local()


def default_db_path() -> Path:
    """Return the default loop state database path under sessions."""
    return BASE_DIR / DB_DIRNAME / DB_FILENAME


def connect(db_path: str | Path | None = None) -> sqlite3.Connection:
    """Open a new WAL SQLite connection with a bounded lock wait.

    Args:
        db_path: Database file; defaults to ``sessions/db/loop_state.db``.

    Returns:
        Configured connection (row factory, WAL, busy timeout).
    """
    target = Path(db_path) if db_path else default_db_path()
    target.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(target), timeout=_BUSY_TIMEOUT_SEC)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA busy_timeout=10000")
    return conn


def thread_connection(db_path: str | Path | None = None) -> sqlite3.Connection:
    """Return the per-thread connection for a database path."""
    target = str(Path(db_path) if db_path else default_db_path())
    cache = getattr(_local, "conns", None)
    if cache is None:
        cache = {}
        _local.conns = cache
    conn = cache.get(target)
    if conn is None:
        conn = connect(target)
        cache[target] = conn
    return conn
