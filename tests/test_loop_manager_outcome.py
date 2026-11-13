"""Loop manager outcome propagation: workspace result.json drives status."""

from __future__ import annotations

import json
import threading

import pytest


@pytest.fixture()
def manager(tmp_path):
    from modules import loop_manager

    return loop_manager.LoopManager(loops_dir=tmp_path, repo_root=tmp_path)


def _register(manager, loop_id: str, workspace) -> None:
    from modules import loop_manager

    records = manager._load_registry_locked()
    records.append(
        {
            "id": loop_id,
            "kind": "auto_loop",
            "target": "10.0.0.5",
            "goal": "gain initial access",
            "rounds": 2,
            "workers": 1,
            "timeout": 0,
            "command": "auto_loop",
            "argv": [],
            "pid": 0,
            "start_ticks": 0,
            "status": loop_manager.STATUS_RUNNING,
            "exit_code": None,
            "started_at": "2026-01-01T00:00:00+00:00",
            "finished_at": None,
            "started_by": "test",
            "log_path": str(workspace / "output.log"),
            "log_bytes": 0,
            "workspace": str(workspace),
        }
    )
    manager._save_registry_locked(records)


class _FakeProcess:
    def __init__(self, exit_code: int) -> None:
        self._code = exit_code

    def wait(self) -> int:
        return self._code


def test_read_outcome_parses_result_json(manager, tmp_path):
    workspace = tmp_path / "ws1"
    workspace.mkdir()
    (workspace / "result.json").write_text(
        json.dumps({"task_id": "t1", "status": "exhausted", "success": False, "verdict": "partial"})
    )
    outcome = manager._read_outcome(workspace)
    assert outcome["success"] is False
    assert outcome["status"] == "exhausted"
    assert manager._read_outcome(tmp_path / "missing") is None


def test_reap_marks_failed_on_honest_outcome(manager, tmp_path):
    from modules import loop_manager

    loop_id = "a" * 32
    workspace = tmp_path / loop_id
    workspace.mkdir()
    _register(manager, loop_id, workspace)
    (workspace / "result.json").write_text(
        json.dumps({"task_id": "t1", "status": "exhausted", "success": False, "verdict": "partial", "rounds": 6})
    )
    manager._reap(loop_id, _FakeProcess(0))
    record = manager.get_loop(loop_id)
    assert record["status"] == loop_manager.STATUS_FAILED
    assert record["exit_code"] == 0
    assert record["outcome"]["verdict"] == "partial"
    metadata = json.loads((workspace / "metadata.json").read_text())
    assert metadata["status"] == loop_manager.STATUS_FAILED


def test_reap_marks_finished_on_success(manager, tmp_path):
    from modules import loop_manager

    loop_id = "b" * 32
    workspace = tmp_path / loop_id
    workspace.mkdir()
    _register(manager, loop_id, workspace)
    (workspace / "result.json").write_text(
        json.dumps({"task_id": "t2", "status": "done", "success": True, "verdict": "achieved", "rounds": 3})
    )
    manager._reap(loop_id, _FakeProcess(0))
    record = manager.get_loop(loop_id)
    assert record["status"] == loop_manager.STATUS_FINISHED
    assert record["outcome"]["success"] is True


def test_reap_falls_back_to_exit_code_without_outcome(manager, tmp_path):
    from modules import loop_manager

    loop_id = "c" * 32
    workspace = tmp_path / loop_id
    workspace.mkdir()
    _register(manager, loop_id, workspace)
    manager._reap(loop_id, _FakeProcess(0))
    record = manager.get_loop(loop_id)
    assert record["status"] == loop_manager.STATUS_FINISHED
    assert "outcome" not in record


def test_reap_stopped_overrides_outcome(manager, tmp_path):
    from modules import loop_manager

    loop_id = "d" * 32
    workspace = tmp_path / loop_id
    workspace.mkdir()
    _register(manager, loop_id, workspace)
    (workspace / "result.json").write_text(json.dumps({"status": "done", "success": True}))
    manager._stopping[loop_id] = True
    manager._reap(loop_id, _FakeProcess(0))
    record = manager.get_loop(loop_id)
    assert record["status"] == loop_manager.STATUS_STOPPED


def test_reap_cancelled_outcome_maps_stopped(manager, tmp_path):
    from modules import loop_manager

    loop_id = "e" * 32
    workspace = tmp_path / loop_id
    workspace.mkdir()
    _register(manager, loop_id, workspace)
    (workspace / "result.json").write_text(
        json.dumps({"status": "cancelled", "success": False, "cancelled": True})
    )
    manager._reap(loop_id, _FakeProcess(1))
    record = manager.get_loop(loop_id)
    assert record["status"] == loop_manager.STATUS_STOPPED


def test_spawn_binds_workspace_env(manager, tmp_path, monkeypatch):
    from modules import loop_manager

    spawned: dict = {}

    class _FakePopen:
        def __init__(self, argv, **kwargs):
            spawned["argv"] = argv
            spawned["env"] = kwargs.get("env") or {}
            self.pid = 4242

    monkeypatch.setattr(loop_manager.subprocess, "Popen", _FakePopen)
    monkeypatch.setattr(loop_manager, "_process_start_ticks", lambda pid: 7)

    started = threading.Event()

    def _fake_reap(self, loop_id, process):
        started.set()

    monkeypatch.setattr(loop_manager.LoopManager, "_reap", _fake_reap)
    spec = loop_manager.LoopSpec("auto_loop", "10.0.0.5", "gain initial access", 2, 1, 0)
    record = manager._spawn_locked(spec, operator="test")
    assert started.is_set()
    assert spawned["env"].get("LAZYOWN_LOOP_WORKSPACE") == record["workspace"]
    assert spawned["env"].get("LAZYOWN_AUTONOMOUS") == "1"
    assert record["workspace"]
