"""Failure-memory veto contract: exhausted commands stop burning rounds.

Every scenario states Given, When, Then. The guard consults the durable
failure memory; the second identical failure blocks replay inside the
session and across restarts; resets restore behavior.
"""

from __future__ import annotations

from pathlib import Path

from modules.auto_loop_memory import FailureMemory


def test_block_threshold_and_recovery(tmp_path: Path):
    """Given two failed identical commands, When the guard gates, Then replay is blocked."""
    memory = FailureMemory(tmp_path / "failure_memory.json")
    target = "10.0.0.9"
    command = "probe ssh 10.0.0.9"
    base = FailureMemory.base_of(command)
    assert memory.is_blocked(target, base) is False
    memory.record_failure(target, "bash", command)
    assert memory.is_blocked(target, base) is False
    memory.record_failure(target, "bash", command)
    assert memory.is_blocked(target, base) is True
    assert memory.is_blocked(target, "probe") is True
    assert memory.is_blocked(target, "curl") is False


def test_memory_survives_restart(tmp_path: Path):
    """Given a persisted block, When a new instance loads, Then the block holds."""
    path = tmp_path / "failure_memory.json"
    memory = FailureMemory(path)
    memory.record_failure("10.0.0.9", "bash", "scan 445 now")
    memory.record_failure("10.0.0.9", "bash", "scan 445 twice")

    reloaded = FailureMemory(path)
    assert reloaded.is_blocked("10.0.0.9", "scan") is True


def test_clear_target_releases(tmp_path: Path):
    """Given a blocked target, When cleared, Then the pair runs again."""
    memory = FailureMemory(tmp_path / "failure_memory.json")
    memory.record_failure("10.0.0.9", "bash", "cmd one")
    memory.record_failure("10.0.0.9", "bash", "cmd also")
    base = FailureMemory.base_of("cmd one")
    assert memory.is_blocked("10.0.0.9", base) is True
    memory.clear_target("10.0.0.9")
    assert memory.is_blocked("10.0.0.9", base) is False


def test_worker_helper_redirects_and_degrades(tmp_path, monkeypatch):
    """Given a redirected store, When the worker builds memory, Then the lazy store path is used."""
    import modules.lazy_loop as loop

    original = loop._store_path
    monkeypatch.setattr(loop, "_store_path", lambda name: tmp_path / name, raising=False)
    memory = loop.Worker._failure_memory.__get__("probe", loop.Worker)()
    assert memory is not None
    monkeypatch.setattr(loop, "_store_path", lambda name: (_ for _ in ()).throw(RuntimeError("no store")), raising=False)
    try:
        assert loop.Worker._failure_memory.__get__("probe", loop.Worker)() is None
    finally:
        monkeypatch.setattr(loop, "_store_path", original, raising=False)
