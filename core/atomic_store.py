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


__all__ = ["file_lock", "update_json", "write_bytes_atomic", "write_text_atomic"]
