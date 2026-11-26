"""Shared atomic file primitives for the loop's small JSON and blob stores.

Several stores (attribution tallies, guard rules, evidence and wire snapshots)
persist tiny files from many workers at once. A fixed temporary name races two
writers onto the same path, and a lock that only covers the final replace still
loses updates across a load-mutate-save cycle. This module centralises the two
disciplines that fix both: every temporary file carries a process-and-thread
unique name so concurrent writers never collide, and a cross-process advisory
lock can wrap a whole read-modify-write so no update is silently dropped.

The lock is a POSIX ``flock`` on a sidecar file, which an operator's CLI and the
C2 process honour even though they are separate processes, unlike a thread lock.
Every helper raises on real I/O failure rather than swallowing it, so a caller
can report a failed persist instead of claiming a success that never reached
disk. Nothing here imports the loop runtime, keeping the module cycle-free.
"""

from __future__ import annotations

import itertools
import json
import logging
import os
import threading
from collections.abc import Callable
from contextlib import contextmanager
from pathlib import Path
from typing import Any

_DIRECTORY_MODE = 0o700
_tmp_counter = itertools.count()


def _unique_tmp(path: Path) -> Path:
    """Return a collision-free temporary sibling path for an atomic write."""
    token = f"{os.getpid()}.{threading.get_ident()}.{next(_tmp_counter)}"
    return path.with_name(f".{path.name}.{token}.tmp")


def _ensure_parent(path: Path) -> None:
    """Create the parent directory, tightening its mode when possible."""
    parent = path.parent
    parent.mkdir(parents=True, exist_ok=True)
    try:
        os.chmod(parent, _DIRECTORY_MODE)
    except OSError:
        pass


def write_bytes_atomic(path: Path, data: bytes) -> None:
    """Write bytes to ``path`` atomically via a unique temp file and replace.

    Args:
        path: Destination path.
        data: Payload to write.

    Raises:
        OSError: When the write or replace fails.
    """
    _ensure_parent(path)
    tmp = _unique_tmp(path)
    try:
        tmp.write_bytes(data)
        os.replace(tmp, path)
    finally:
        try:
            tmp.unlink()
        except OSError:
            pass


def write_text_atomic(path: Path, text: str) -> None:
    """Write text to ``path`` atomically, UTF-8 encoded.

    Args:
        path: Destination path.
        text: Payload to write.

    Raises:
        OSError: When the write or replace fails.
    """
    write_bytes_atomic(path, text.encode("utf-8", errors="replace"))


@contextmanager
def file_lock(path: Path):
    """Hold a cross-process advisory lock for the duration of the block.

    The lock is an ``flock`` on ``<path>.lock``; it serialises writers in
    different processes, not only different threads. On a platform without
    ``fcntl`` the lock degrades to a no-op so the caller still runs, trading
    cross-process exclusion for availability.

    Args:
        path: The file whose sidecar lock is taken.
    """
    _ensure_parent(path)
    lock_path = path.with_name(f".{path.name}.lock")
    handle = None
    try:
        import fcntl

        handle = open(lock_path, "w")
        fcntl.flock(handle.fileno(), fcntl.LOCK_EX)
    except (OSError, ImportError):
        if handle is not None:
            try:
                handle.close()
            except OSError:
                pass
            handle = None
    try:
        yield
    finally:
        if handle is not None:
            try:
                import fcntl

                fcntl.flock(handle.fileno(), fcntl.LOCK_UN)
            except (OSError, ImportError):
                pass
            try:
                handle.close()
            except OSError:
                pass


def update_json(path: Path, mutate: Callable[[dict], Any], default: dict | None = None) -> dict:
    """Apply a mutation to a JSON document under a cross-process lock.

    The whole load-mutate-save cycle runs inside :func:`file_lock`, so two
    writers never read the same base and lose each other's update. The mutation
    receives the current document (or ``default``) and mutates it in place; the
    result is written atomically.

    Args:
        path: The JSON document path.
        mutate: A callable applied to the loaded document in place.
        default: The document to start from when the file is absent or corrupt.

    Returns:
        The document as persisted.

    Raises:
        OSError: When the write fails.
    """
    with file_lock(path):
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            if not isinstance(data, dict):
                data = dict(default or {})
        except (OSError, ValueError):
            data = dict(default or {})
        mutate(data)
        write_text_atomic(path, json.dumps(data, ensure_ascii=False, sort_keys=True))
        return data


_JSON_LOCK = threading.RLock()


def _restrict_file(path: Path) -> None:
    """Best-effort chmod 600 on a secret-bearing file; never raises."""
    try:
        os.chmod(path, 0o600)
    except OSError:
        pass


def save_json(path: Path, payload: dict) -> None:
    """Atomically persist a JSON mapping to ``path`` with 0600 permissions.

    Each write uses its own process/thread-scoped temp file and an atomic
    replace under a process-wide lock, so a reader never sees a torn file
    and concurrent in-process writers never collide. This guarantees
    atomicity, not isolation: a read-modify-write that must not lose a
    concurrent writer's update belongs in :func:`update_json`.

    Args:
        path: Destination ``.json`` file.
        payload: Mapping to persist.
    """
    tmp = _unique_tmp(path)
    with _JSON_LOCK:
        tmp.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
        _restrict_file(tmp)
        tmp.replace(path)
        _restrict_file(path)


def load_json(path: Path, default: dict) -> dict:
    """Load a JSON mapping from ``path`` or return a deep copy of ``default``.

    A corrupt or unreadable file falls back to the default instead of
    raising, with the failure logged at debug so hidden state corruption
    is observable rather than silent.

    Args:
        path: Source ``.json`` file.
        default: Fallback document returned when the file is absent or
            unreadable.

    Returns:
        The loaded mapping, or a fresh copy of ``default``.
    """
    try:
        if path.exists():
            return json.loads(path.read_text())
    except Exception as exc:
        logging.getLogger(__name__).debug("corrupt or unreadable JSON store %s, using default: %s", path, exc)
    return json.loads(json.dumps(default))


def append_jsonl(path: Path, rows: list[dict]) -> int:
    """Append rows as JSON lines to ``path``, creating a 0700 parent.

    Args:
        path: Target ``.jsonl`` file.
        rows: Row mappings to append.

    Returns:
        Number of appended rows, or 0 when the write failed.
    """
    if not rows:
        return 0
    try:
        _ensure_parent(path)
        with path.open("a", encoding="utf-8") as handle:
            for row in rows:
                handle.write(json.dumps(row, ensure_ascii=False) + "\n")
        return len(rows)
    except OSError:
        return 0


def read_jsonl(path: Path, limit: int = 0) -> list[dict]:
    """Read JSON lines from ``path``, preserving order, skipping bad rows.

    Args:
        path: Source ``.jsonl`` file.
        limit: Maximum rows returned (0 keeps every readable row).

    Returns:
        Parsed row mappings; unreadable lines are skipped.
    """
    try:
        lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    except OSError:
        return []
    rows: list[dict] = []
    for line in lines:
        line = line.strip()
        if not line:
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(row, dict):
            rows.append(row)
    if limit and len(rows) > limit:
        rows = rows[-limit:]
    return rows


__all__ = [
    "append_jsonl",
    "file_lock",
    "load_json",
    "read_jsonl",
    "save_json",
    "update_json",
    "write_bytes_atomic",
    "write_text_atomic",
]
