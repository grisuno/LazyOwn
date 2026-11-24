"""Tests for the single-writer asynchronous database queue."""

from __future__ import annotations

import threading

from modules.db import LazyOwnDB
from modules.db_writer import DBWriteQueue, get_write_queue, set_write_queue, submit_write


def _make_db(tmp_path) -> LazyOwnDB:
    return LazyOwnDB(str(tmp_path / "writer.db"))


def test_async_submit_persists_via_single_writer(tmp_path):
    """Given an async queue, When ops are submitted, Then all rows persist."""
    database = _make_db(tmp_path)
    q = DBWriteQueue(db_factory=lambda: database)
    try:
        for index in range(25):
            host = f"10.0.0.{index}"

            def _write(db, host=host):
                workspace = db.default_workspace("default")
                host_id = db.host_add(workspace, host, hostname=host)
                db.vuln_add(host_id, "demo", severity="high", description="x")

            assert q.submit(_write) is True
        assert q.flush(timeout=5.0) is True
    finally:
        q.stop()
    hosts = database.host_list(database.default_workspace("default"))
    assert len(hosts) == 25


def test_submit_never_blocks_when_queue_full(tmp_path):
    """Given a full bounded queue, When submitting, Then the op is dropped not blocked."""
    gate = threading.Event()

    def _blocking(_db):
        gate.wait(timeout=5.0)

    q = DBWriteQueue(db_factory=lambda: _make_db(tmp_path), max_queue=1)
    try:
        assert q.submit(_blocking) is True
        accepted = 0
        dropped = 0
        for _ in range(50):
            if q.submit(lambda _db: None):
                accepted += 1
            else:
                dropped += 1
        assert dropped > 0
    finally:
        gate.set()
        q.stop()


def test_failing_op_is_isolated(tmp_path):
    """Given an op that raises, When processed, Then later ops still run."""
    database = _make_db(tmp_path)
    q = DBWriteQueue(db_factory=lambda: database)
    try:

        def _boom(_db):
            raise RuntimeError("boom")

        marker = {"done": False}

        def _ok(db):
            workspace = db.default_workspace("default")
            db.host_add(workspace, "10.9.9.9", hostname="x")
            marker["done"] = True

        q.submit(_boom)
        q.submit(_ok)
        assert q.flush(timeout=5.0) is True
    finally:
        q.stop()
    assert marker["done"] is True
    stats = q.stats()
    assert stats["processed"] == 1


def test_synchronous_mode_applies_inline(tmp_path):
    """Given synchronous mode, When submitting, Then the write happens without a thread."""
    database = _make_db(tmp_path)
    q = DBWriteQueue(db_factory=lambda: database, synchronous=True)
    q.submit(lambda db: db.host_add(db.default_workspace("default"), "10.1.1.1", hostname="a"))
    hosts = database.host_list(database.default_workspace("default"))
    assert len(hosts) == 1
    assert q._thread is None


def test_singleton_submit_roundtrip(tmp_path):
    """Given the module singleton, When replaced, Then submit_write routes through it."""
    database = _make_db(tmp_path)
    q = DBWriteQueue(db_factory=lambda: database, synchronous=True)
    set_write_queue(q)
    try:
        assert get_write_queue() is q
        assert submit_write(lambda db: db.host_add(db.default_workspace("default"), "10.2.2.2", hostname="b"))
        assert len(database.host_list(database.default_workspace("default"))) == 1
    finally:
        set_write_queue(None)
