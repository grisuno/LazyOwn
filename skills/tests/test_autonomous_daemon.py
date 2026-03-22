#!/usr/bin/env python3
"""
skills/tests/test_autonomous_daemon.py — Tests for autonomous_daemon.py (SOLID refactoring)

All tests use tmp_path or tempfile.TemporaryDirectory for isolation.
No real subprocess calls (mock _run_lazyown). No external API calls.
"""

from __future__ import annotations

import asyncio
import json
import sys
import tempfile
import threading
import time
import uuid
from pathlib import Path
from typing import Any, Dict, List, Optional
from unittest.mock import AsyncMock, MagicMock, patch, call

import pytest

# Make skills/ importable
_SKILLS_DIR = Path(__file__).parent.parent
if str(_SKILLS_DIR) not in sys.path:
    sys.path.insert(0, str(_SKILLS_DIR))


# ─────────────────────────────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────────────────────────────

def _patch_paths(tmp_path: Path):
    """Context manager that redirects all file paths to tmp_path."""
    import autonomous_daemon as _ad
    patchers = [
        patch.object(_ad, "SESSIONS_DIR", tmp_path / "sessions"),
        patch.object(_ad, "TASKS_FILE",   tmp_path / "sessions" / "tasks.json"),
        patch.object(_ad, "EVENTS_FILE",  tmp_path / "sessions" / "autonomous_events.jsonl"),
        patch.object(_ad, "STATUS_FILE",  tmp_path / "sessions" / "autonomous_status.json"),
        patch.object(_ad, "PID_FILE",     tmp_path / "sessions" / "autonomous_daemon.pid"),
    ]
    for p in patchers:
        p.start()
    (tmp_path / "sessions").mkdir(parents=True, exist_ok=True)
    return patchers


def _stop_patchers(patchers):
    for p in patchers:
        p.stop()


# ─────────────────────────────────────────────────────────────────────────────
# 1. TestPTYCommandRunner
# ─────────────────────────────────────────────────────────────────────────────

class TestPTYCommandRunner:
    """Tests for PTYCommandRunner."""

    def test_instantiation(self):
        """PTYCommandRunner can be instantiated."""
        from autonomous_daemon import PTYCommandRunner
        runner = PTYCommandRunner()
        assert runner is not None

    def test_name_property(self):
        """name property returns 'pty'."""
        from autonomous_daemon import PTYCommandRunner
        runner = PTYCommandRunner()
        assert runner.name == "pty"

    def test_implements_icommand_runner(self):
        """PTYCommandRunner is a subclass of ICommandRunner."""
        from autonomous_daemon import PTYCommandRunner, ICommandRunner
        assert issubclass(PTYCommandRunner, ICommandRunner)


# ─────────────────────────────────────────────────────────────────────────────
# 2. TestMCPCommandRunner
# ─────────────────────────────────────────────────────────────────────────────

class TestMCPCommandRunner:
    """Tests for MCPCommandRunner."""

    def test_instantiation(self):
        """MCPCommandRunner can be instantiated."""
        from autonomous_daemon import MCPCommandRunner
        runner = MCPCommandRunner()
        assert runner is not None

    def test_name_property(self):
        """name property returns 'mcp'."""
        from autonomous_daemon import MCPCommandRunner
        runner = MCPCommandRunner()
        assert runner.name == "mcp"

    def test_raises_when_import_fails(self):
        """run() raises ImportError when lazyown_mcp is not importable."""
        from autonomous_daemon import MCPCommandRunner
        runner = MCPCommandRunner()
        with patch.dict("sys.modules", {"lazyown_mcp": None}):
            with pytest.raises((ImportError, ModuleNotFoundError)):
                runner.run("test_command", timeout=5)

    def test_delegates_to_mcp_when_available(self):
        """run() delegates to _run_lazyown_command when import succeeds."""
        from autonomous_daemon import MCPCommandRunner

        mock_mcp = MagicMock()
        mock_mcp._run_lazyown_command = MagicMock(return_value="mcp output")

        with patch.dict("sys.modules", {"lazyown_mcp": mock_mcp}):
            runner = MCPCommandRunner()
            result = runner.run("ls", timeout=10)

        assert result == "mcp output"
        mock_mcp._run_lazyown_command.assert_called_once_with("ls", 10)


# ─────────────────────────────────────────────────────────────────────────────
# 3. TestCommandRunnerChain
# ─────────────────────────────────────────────────────────────────────────────

class TestCommandRunnerChain:
    """Tests for CommandRunnerChain (Chain of Responsibility)."""

    def _make_runner(self, name: str, result: str = "ok", raises: bool = False):
        from autonomous_daemon import ICommandRunner
        class _R(ICommandRunner):
            @property
            def name(self) -> str:
                return name
            def run(self, command: str, timeout: int) -> str:
                if raises:
                    raise RuntimeError(f"{name} failed")
                return result
        return _R()

    def test_uses_first_runner_when_successful(self):
        """Chain returns result from first runner when it succeeds."""
        from autonomous_daemon import CommandRunnerChain
        r1 = self._make_runner("first", result="first-result")
        r2 = self._make_runner("second", result="second-result")
        chain  = CommandRunnerChain([r1, r2])
        result = chain.run("cmd", timeout=5)
        assert result == "first-result"

    def test_falls_back_to_second_on_exception(self):
        """Chain uses second runner when first raises."""
        from autonomous_daemon import CommandRunnerChain
        r1 = self._make_runner("first", raises=True)
        r2 = self._make_runner("second", result="fallback-result")
        chain  = CommandRunnerChain([r1, r2])
        result = chain.run("cmd", timeout=5)
        assert result == "fallback-result"

    def test_raises_when_all_fail(self):
        """Chain raises RuntimeError when all runners fail."""
        from autonomous_daemon import CommandRunnerChain
        r1 = self._make_runner("first",  raises=True)
        r2 = self._make_runner("second", raises=True)
        chain = CommandRunnerChain([r1, r2])
        with pytest.raises(RuntimeError):
            chain.run("cmd", timeout=5)

    def test_name_reflects_all_runners(self):
        """name property lists all runner names."""
        from autonomous_daemon import CommandRunnerChain
        r1 = self._make_runner("alpha")
        r2 = self._make_runner("beta")
        chain = CommandRunnerChain([r1, r2])
        assert "alpha" in chain.name
        assert "beta" in chain.name

    def test_requires_at_least_one_runner(self):
        """Instantiation with empty list raises ValueError."""
        from autonomous_daemon import CommandRunnerChain
        with pytest.raises(ValueError):
            CommandRunnerChain([])


# ─────────────────────────────────────────────────────────────────────────────
# 4. TestFallbackSelector
# ─────────────────────────────────────────────────────────────────────────────

class TestFallbackSelector:
    """Tests for FallbackSelector — always returns a CommandDecision."""

    def test_always_returns_decision(self):
        """select() never returns None."""
        from autonomous_daemon import FallbackSelector
        sel    = FallbackSelector()
        result = sel.select(target="10.0.0.1", phase="recon", context={})
        assert result is not None

    def test_returns_command_decision_type(self):
        """select() returns a CommandDecision instance."""
        from autonomous_daemon import FallbackSelector, CommandDecision
        sel    = FallbackSelector()
        result = sel.select(target="10.0.0.1", phase="exploit", context={})
        assert isinstance(result, CommandDecision)
        assert result.command

    def test_source_is_fallback(self):
        """source field is 'fallback'."""
        from autonomous_daemon import FallbackSelector
        sel    = FallbackSelector()
        result = sel.select(target="x", phase="lateral", context={})
        assert result.source == "fallback"

    def test_unknown_phase_returns_decision(self):
        """Even an unknown phase returns a CommandDecision."""
        from autonomous_daemon import FallbackSelector
        sel    = FallbackSelector()
        result = sel.select(target="x", phase="unknown_phase_xyz", context={})
        assert result is not None
        assert result.command


# ─────────────────────────────────────────────────────────────────────────────
# 5. TestParquetSelector
# ─────────────────────────────────────────────────────────────────────────────

class TestParquetSelector:
    """Tests for ParquetSelector."""

    def test_returns_none_when_pdb_unavailable(self):
        """When pdb is None, select() returns None."""
        from autonomous_daemon import ParquetSelector
        sel    = ParquetSelector(pdb=None, fail_counts={})
        result = sel.select(target="10.0.0.1", phase="recon", context={})
        assert result is None

    def test_returns_candidate_when_pdb_has_history(self):
        """When pdb returns session rows, select() returns a CommandDecision."""
        from autonomous_daemon import ParquetSelector, CommandDecision

        mock_pdb = MagicMock()
        mock_pdb.query_session.return_value = [
            {"command": "nmap -sV 10.0.0.1", "phase": "recon", "success": True},
            {"command": "nmap -sV 10.0.0.1", "phase": "recon", "success": True},
        ]

        sel    = ParquetSelector(pdb=mock_pdb, fail_counts={})
        result = sel.select(target="10.0.0.1", phase="recon", context={})
        assert result is not None
        assert isinstance(result, CommandDecision)
        assert result.source == "parquet"

    def test_respects_fail_counts(self):
        """Commands that have hit the fail threshold are skipped."""
        from autonomous_daemon import ParquetSelector, MAX_FAILS_PER_CMD

        mock_pdb = MagicMock()
        mock_pdb.query_session.return_value = [
            {"command": "badcmd --flag", "phase": "recon", "success": True},
        ]

        fail_counts = {"badcmd": MAX_FAILS_PER_CMD}
        sel         = ParquetSelector(pdb=mock_pdb, fail_counts=fail_counts)
        result      = sel.select(target="10.0.0.1", phase="recon", context={})
        # badcmd should be skipped, leaving nothing from parquet
        assert result is None


# ─────────────────────────────────────────────────────────────────────────────
# 6. TestCascadeStrategy
# ─────────────────────────────────────────────────────────────────────────────

class TestCascadeStrategy:
    """Tests for CascadeStrategy."""

    def _make_selector(self, returns):
        """Build a mock ICommandSelector that returns `returns` from select()."""
        from autonomous_daemon import ICommandSelector
        class _S(ICommandSelector):
            def select(self, target, phase, context):
                return returns
        return _S()

    def test_returns_first_non_none_result(self):
        """CascadeStrategy returns the first selector that gives a result."""
        from autonomous_daemon import CascadeStrategy, CommandDecision

        dec1 = CommandDecision(command="nmap", source="reactive")
        dec2 = CommandDecision(command="enum_smb", source="parquet")

        sel_none  = self._make_selector(None)
        sel_first = self._make_selector(dec1)
        sel_never = self._make_selector(dec2)

        cascade = CascadeStrategy([sel_none, sel_first, sel_never])
        result  = cascade.next_command("10.0.0.1", "recon")
        assert result.command == "nmap"
        assert result.source  == "reactive"

    def test_uses_fallback_when_all_none(self):
        """CascadeStrategy uses FallbackSelector when all others return None."""
        from autonomous_daemon import CascadeStrategy, FallbackSelector

        sel_none = self._make_selector(None)
        fallback = FallbackSelector()

        cascade = CascadeStrategy([sel_none, fallback])
        result  = cascade.next_command("10.0.0.1", "recon")
        assert result is not None
        assert result.source == "fallback"

    def test_passes_context_to_selectors(self):
        """CascadeStrategy passes the context dict to selectors."""
        from autonomous_daemon import ICommandSelector, CascadeStrategy

        captured: Dict = {}

        class CapturingSelector(ICommandSelector):
            def select(self, target, phase, context):
                captured.update(context)
                return None

        fallback = self._make_selector(MagicMock(command="x", source="f"))
        cascade  = CascadeStrategy([CapturingSelector(), fallback])
        cascade.next_command("t", "recon", context={"services": ["http"]})

        assert "services" in captured


# ─────────────────────────────────────────────────────────────────────────────
# 7. TestInjectToTasksJson
# ─────────────────────────────────────────────────────────────────────────────

class TestInjectToTasksJson:
    """Tests for _inject_to_tasks_json."""

    def setup_method(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.tmp  = Path(self._tmp.name)
        (self.tmp / "sessions").mkdir()
        self._patchers = _patch_paths(self.tmp)

    def teardown_method(self):
        _stop_patchers(self._patchers)
        self._tmp.cleanup()

    def test_creates_file_if_missing(self):
        """Creates tasks.json when it does not exist."""
        import autonomous_daemon as _ad
        tasks_file = _ad.TASKS_FILE
        assert not tasks_file.exists()
        _ad._inject_to_tasks_json("Test objective")
        assert tasks_file.exists()

    def test_appends_new_task(self):
        """Each call appends a new task to tasks.json."""
        import autonomous_daemon as _ad
        _ad._inject_to_tasks_json("Task One")
        _ad._inject_to_tasks_json("Task Two")
        tasks = json.loads(_ad.TASKS_FILE.read_text())
        assert len(tasks) == 2
        titles = [t["title"] for t in tasks]
        assert "Task One" in titles
        assert "Task Two" in titles

    def test_correct_schema(self):
        """Injected task has all required keys: id, title, description, operator, status."""
        import autonomous_daemon as _ad
        _ad._inject_to_tasks_json(
            title="Schema test",
            description="desc",
            operator="testop",
            status="New",
        )
        tasks = json.loads(_ad.TASKS_FILE.read_text())
        task  = tasks[0]
        assert "id" in task
        assert "title" in task
        assert "description" in task
        assert "operator" in task
        assert "status" in task

    def test_returns_assigned_id(self):
        """Return value is the integer id assigned to the new task."""
        import autonomous_daemon as _ad
        id0 = _ad._inject_to_tasks_json("First")
        id1 = _ad._inject_to_tasks_json("Second")
        assert id0 == 0
        assert id1 == 1

    def test_handles_existing_invalid_json(self):
        """Recovers gracefully when tasks.json contains invalid JSON."""
        import autonomous_daemon as _ad
        _ad.TASKS_FILE.write_text("NOT JSON", encoding="utf-8")
        new_id = _ad._inject_to_tasks_json("Recovery task")
        assert new_id >= 0
        tasks = json.loads(_ad.TASKS_FILE.read_text())
        assert len(tasks) == 1


# ─────────────────────────────────────────────────────────────────────────────
# 8. TestUpdateTaskStatus
# ─────────────────────────────────────────────────────────────────────────────

class TestUpdateTaskStatus:
    """Tests for _update_task_status."""

    def setup_method(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.tmp  = Path(self._tmp.name)
        (self.tmp / "sessions").mkdir()
        self._patchers = _patch_paths(self.tmp)

    def teardown_method(self):
        _stop_patchers(self._patchers)
        self._tmp.cleanup()

    def _write_tasks(self, tasks):
        import autonomous_daemon as _ad
        _ad.TASKS_FILE.write_text(json.dumps(tasks, indent=4), encoding="utf-8")

    def test_updates_existing_task(self):
        """_update_task_status changes the status of a matching task."""
        import autonomous_daemon as _ad
        self._write_tasks([{"id": 0, "title": "Enumerate SMB", "status": "New",
                            "description": "", "operator": "test"}])
        changed = _ad._update_task_status("Enumerate SMB", "Done")
        assert changed is True
        tasks = json.loads(_ad.TASKS_FILE.read_text())
        assert tasks[0]["status"] == "Done"

    def test_ignores_missing_title(self):
        """_update_task_status returns False when title not found."""
        import autonomous_daemon as _ad
        self._write_tasks([{"id": 0, "title": "Existing task", "status": "New",
                            "description": "", "operator": "test"}])
        changed = _ad._update_task_status("Nonexistent title", "Done")
        assert changed is False

    def test_returns_false_when_file_missing(self):
        """_update_task_status returns False when tasks.json does not exist."""
        import autonomous_daemon as _ad
        changed = _ad._update_task_status("Anything", "Done")
        assert changed is False


# ─────────────────────────────────────────────────────────────────────────────
# 9. TestEmitEvent
# ─────────────────────────────────────────────────────────────────────────────

class TestEmitEvent:
    """Tests for _emit."""

    def setup_method(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.tmp  = Path(self._tmp.name)
        (self.tmp / "sessions").mkdir()
        self._patchers = _patch_paths(self.tmp)

    def teardown_method(self):
        _stop_patchers(self._patchers)
        self._tmp.cleanup()

    def test_writes_valid_json_line(self):
        """_emit writes a valid JSON object to EVENTS_FILE."""
        import autonomous_daemon as _ad
        _ad._emit("TEST_EVENT", {"key": "value"})
        assert _ad.EVENTS_FILE.exists()
        lines = _ad.EVENTS_FILE.read_text().splitlines()
        assert len(lines) >= 1
        event = json.loads(lines[-1])
        assert event["type"] == "TEST_EVENT"
        assert event["payload"]["key"] == "value"

    def test_event_has_required_fields(self):
        """Each emitted event has id, ts, type, severity, payload."""
        import autonomous_daemon as _ad
        _ad._emit("HEARTBEAT", {"pid": 1234}, severity="info")
        lines = _ad.EVENTS_FILE.read_text().splitlines()
        event = json.loads(lines[-1])
        for field in ("id", "ts", "type", "severity", "payload"):
            assert field in event, f"Missing field: {field}"

    def test_multiple_emits_append_lines(self):
        """Multiple _emit calls each produce a separate JSON line."""
        import autonomous_daemon as _ad
        _ad._emit("EV1", {"n": 1})
        _ad._emit("EV2", {"n": 2})
        _ad._emit("EV3", {"n": 3})
        lines = _ad.EVENTS_FILE.read_text().splitlines()
        assert len(lines) == 3


# ─────────────────────────────────────────────────────────────────────────────
# 10. TestMCPAutonomousInject
# ─────────────────────────────────────────────────────────────────────────────

class TestMCPAutonomousInject:
    """Tests for mcp_autonomous_inject."""

    def setup_method(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.tmp  = Path(self._tmp.name)
        (self.tmp / "sessions").mkdir()
        self._patchers = _patch_paths(self.tmp)

    def teardown_method(self):
        _stop_patchers(self._patchers)
        self._tmp.cleanup()

    def _make_mock_store(self):
        """Build a mock ObjectiveStore that returns a mock objective."""
        mock_obj          = MagicMock()
        mock_obj.id       = uuid.uuid4().hex
        mock_obj.text     = "Test objective"
        mock_obj.priority = "high"
        mock_obj.status   = "pending"

        mock_store        = MagicMock()
        mock_store.inject = MagicMock(return_value=mock_obj)
        return mock_store, mock_obj

    def test_injects_to_objective_store_and_tasks_json(self):
        """mcp_autonomous_inject writes to both ObjectiveStore and tasks.json."""
        import autonomous_daemon as _ad
        mock_store, mock_obj = self._make_mock_store()

        with patch.object(_ad, "_ObjectiveStore", return_value=mock_store):
            result = _ad.mcp_autonomous_inject("Enumerate AD domain", priority="high")

        data = json.loads(result)
        assert "id" in data
        assert "task_id" in data
        mock_store.inject.assert_called_once()

        # tasks.json must have been created
        assert _ad.TASKS_FILE.exists()
        tasks = json.loads(_ad.TASKS_FILE.read_text())
        assert len(tasks) == 1

    def test_returns_json_with_both_ids(self):
        """Return value contains both objective id and task_id."""
        import autonomous_daemon as _ad
        mock_store, mock_obj = self._make_mock_store()

        with patch.object(_ad, "_ObjectiveStore", return_value=mock_store):
            raw = _ad.mcp_autonomous_inject("Test", priority="medium")

        data = json.loads(raw)
        assert "id" in data
        assert "task_id" in data
        assert data["id"] == mock_obj.id
        assert isinstance(data["task_id"], int)

    def test_returns_error_string_when_store_unavailable(self):
        """mcp_autonomous_inject returns error message when ObjectiveStore is None."""
        import autonomous_daemon as _ad
        with patch.object(_ad, "_ObjectiveStore", None):
            result = _ad.mcp_autonomous_inject("Test")
        assert "ObjectiveStore" in result


# ─────────────────────────────────────────────────────────────────────────────
# 11. TestMCPAutonomousStatus
# ─────────────────────────────────────────────────────────────────────────────

class TestMCPAutonomousStatus:
    """Tests for mcp_autonomous_status."""

    def setup_method(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.tmp  = Path(self._tmp.name)
        (self.tmp / "sessions").mkdir()
        self._patchers = _patch_paths(self.tmp)

    def teardown_method(self):
        _stop_patchers(self._patchers)
        self._tmp.cleanup()

    def test_returns_valid_json(self):
        """mcp_autonomous_status() returns parseable JSON."""
        import autonomous_daemon as _ad
        raw = _ad.mcp_autonomous_status()
        data = json.loads(raw)
        assert isinstance(data, dict)

    def test_contains_expected_fields(self):
        """Status JSON contains 'running', 'objectives_done', 'steps_run'."""
        import autonomous_daemon as _ad
        raw  = _ad.mcp_autonomous_status()
        data = json.loads(raw)
        assert "running" in data
        assert "objectives_done" in data
        assert "steps_run" in data

    def test_running_is_false_when_no_daemon(self):
        """'running' is False when no daemon thread is active."""
        import autonomous_daemon as _ad
        with patch.object(_ad, "_daemon_thread", None):
            raw  = _ad.mcp_autonomous_status()
            data = json.loads(raw)
        assert data["running"] is False

    def test_merges_status_file_when_present(self):
        """Status is enriched from STATUS_FILE when it exists."""
        import autonomous_daemon as _ad
        _ad.STATUS_FILE.write_text(
            json.dumps({"extra_key": "extra_value"}), encoding="utf-8"
        )
        raw  = _ad.mcp_autonomous_status()
        data = json.loads(raw)
        assert "extra_key" in data
        assert data["extra_key"] == "extra_value"


# ─────────────────────────────────────────────────────────────────────────────
# 12. TestObjectiveLoopUnit
# ─────────────────────────────────────────────────────────────────────────────

class TestObjectiveLoopUnit:
    """
    Unit tests for objective_loop logic with ObjectiveStore fully mocked.
    Verifies that _run_objective is called, complete() is called,
    and task status is updated to Done.
    """

    def setup_method(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.tmp  = Path(self._tmp.name)
        (self.tmp / "sessions").mkdir()
        self._patchers = _patch_paths(self.tmp)

    def teardown_method(self):
        _stop_patchers(self._patchers)
        self._tmp.cleanup()

    def _make_mock_objective(self):
        obj          = MagicMock()
        obj.id       = uuid.uuid4().hex
        obj.text     = "Enumerate SMB on 10.10.11.78"
        obj.context  = {"target": "10.10.11.78"}
        obj.priority = "high"
        obj.status   = "pending"
        return obj

    def test_complete_called_after_successful_execution(self):
        """
        When next_pending() returns one objective and _run_objective succeeds,
        store.complete() is called and task status is updated to Done.
        """
        import autonomous_daemon as _ad
        from autonomous_daemon import StepResult

        obj       = self._make_mock_objective()
        mock_store = MagicMock()

        # Return objective first call, then None to stop the loop
        call_count = {"n": 0}
        def _next_pending():
            call_count["n"] += 1
            if call_count["n"] == 1:
                return obj
            # Set should_stop to break the loop after first iteration
            _ad._should_stop.set()
            return None

        mock_store.next_pending = _next_pending
        mock_store.start        = MagicMock()
        mock_store.complete     = MagicMock()
        mock_store.block        = MagicMock()

        fake_results = [StepResult(
            step=1, command="nmap", output="open 445", success=True, source="fallback"
        )]

        async def _fake_run_async(objective_id, objective_text, target):
            return fake_results

        mock_engine = MagicMock()
        mock_engine.run_async = _fake_run_async

        # Inject tasks file (pre-created) for _update_task_status to find
        _ad.TASKS_FILE.write_text(
            json.dumps([{
                "id": 0, "title": obj.text, "status": "New",
                "description": "", "operator": "test",
            }]),
            encoding="utf-8",
        )

        _ad._should_stop.clear()

        async def _run_loop():
            with patch.object(_ad, "_ObjectiveStore", return_value=mock_store), \
                 patch("autonomous_daemon.ExecutionEngine", return_value=mock_engine), \
                 patch("autonomous_daemon.OBJ_POLL_S", 0.01):
                await _ad.objective_loop(max_steps=1, loop=asyncio.get_event_loop())

        asyncio.run(_run_loop())

        mock_store.complete.assert_called_once_with(obj.id)

        tasks = json.loads(_ad.TASKS_FILE.read_text())
        assert tasks[0]["status"] == "Done"

    def test_block_called_on_execution_failure(self):
        """
        When run_async raises an exception, store.block() is called and
        task status is updated to Blocked.
        """
        import autonomous_daemon as _ad

        obj        = self._make_mock_objective()
        mock_store = MagicMock()

        call_count = {"n": 0}
        def _next_pending():
            call_count["n"] += 1
            if call_count["n"] == 1:
                return obj
            _ad._should_stop.set()
            return None

        mock_store.next_pending = _next_pending
        mock_store.start        = MagicMock()
        mock_store.complete     = MagicMock()
        mock_store.block        = MagicMock()

        async def _failing_run_async(objective_id, objective_text, target):
            raise RuntimeError("simulated failure")

        mock_engine       = MagicMock()
        mock_engine.run_async = _failing_run_async

        _ad.TASKS_FILE.write_text(
            json.dumps([{
                "id": 0, "title": obj.text, "status": "New",
                "description": "", "operator": "test",
            }]),
            encoding="utf-8",
        )

        _ad._should_stop.clear()

        async def _run_loop():
            with patch.object(_ad, "_ObjectiveStore", return_value=mock_store), \
                 patch("autonomous_daemon.ExecutionEngine", return_value=mock_engine), \
                 patch("autonomous_daemon.OBJ_POLL_S", 0.01):
                await _ad.objective_loop(max_steps=1, loop=asyncio.get_event_loop())

        asyncio.run(_run_loop())

        mock_store.block.assert_called_once()
        tasks = json.loads(_ad.TASKS_FILE.read_text())
        assert tasks[0]["status"] == "Blocked"

    def test_loop_disabled_when_objective_store_missing(self):
        """
        objective_loop exits immediately when _ObjectiveStore is None.
        """
        import autonomous_daemon as _ad
        _ad._should_stop.clear()

        ran = {"v": False}

        async def _run_loop():
            with patch.object(_ad, "_ObjectiveStore", None):
                await _ad.objective_loop(max_steps=5, loop=asyncio.get_event_loop())
            ran["v"] = True

        asyncio.run(_run_loop())
        assert ran["v"] is True  # Should have returned cleanly


if __name__ == "__main__":
    import pytest
    pytest.main([__file__, "-v"])
