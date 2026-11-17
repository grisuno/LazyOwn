"""Concurrency guard for :func:`core.config.save_payload`.

``payload.json`` is written by several processes (the C2, the shell, the
autonomous daemon). The write is a read-merge-replace, which loses updates
when two writers interleave without serialization. These tests pin the
advisory-lock behaviour that makes concurrent writers safe and confirm the
merge semantics are unchanged.
"""

from __future__ import annotations

import json
import threading
from pathlib import Path

from core.config import _payload_write_lock, save_payload


def test_lock_is_reentrant_across_sequential_acquires(tmp_path: Path) -> None:
    """Acquiring the lock twice in sequence works and creates the sidecar."""
    target = tmp_path / "payload.json"
    with _payload_write_lock(target):
        pass
    with _payload_write_lock(target):
        pass
    assert (tmp_path / "payload.json.lock").exists()


def test_merge_preserves_absent_keys(tmp_path: Path) -> None:
    """A partial write keeps keys it does not mention (merge, not replace)."""
    target = tmp_path / "payload.json"
    save_payload({"a": 1, "b": 2}, target)
    save_payload({"b": 3}, target)
    data = json.loads(target.read_text(encoding="utf-8"))
    assert data == {"a": 1, "b": 3}


def test_concurrent_writers_do_not_lose_updates(tmp_path: Path) -> None:
    """Many threads each writing a distinct key all survive under the lock."""
    target = tmp_path / "payload.json"
    save_payload({"seed": 0}, target)
    writer_count = 24

    def write(index: int) -> None:
        save_payload({f"key_{index}": index}, target)

    threads = [threading.Thread(target=write, args=(i,)) for i in range(writer_count)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

    data = json.loads(target.read_text(encoding="utf-8"))
    for index in range(writer_count):
        assert data[f"key_{index}"] == index, f"lost update for key_{index}"
    assert data["seed"] == 0
