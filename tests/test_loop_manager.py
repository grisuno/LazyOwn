"""Tests for modules.loop_manager — safe autonomous loop orchestration.

Covers:
    - Target, goal and numeric-knob validation
    - Argv construction without shell metacharacters
    - Loop spawn, registry persistence and status transitions
    - Log chunk reads with path confinement
    - Stop semantics on a running subprocess
    - Concurrency cap enforcement
"""

from __future__ import annotations

import json
import tempfile
import time
from pathlib import Path

import pytest

from modules.loop_manager import (
    DEFAULT_GOAL,
    KIND_AUTO_LOOP,
    KIND_LAZY_NMAP,
    LoopManager,
    LoopNotFoundError,
    LoopSpec,
    LoopValidationError,
    clamp_int,
    sanitize_goal,
    validate_loop_id,
    validate_target,
)


@pytest.fixture
def loops_dir():
    with tempfile.TemporaryDirectory() as d:
        yield Path(d) / "loops"


@pytest.fixture
def stub_script(tmp_path):
    script = tmp_path / "stub_loop_target.py"
    script.write_text(
        "import signal, sys, time\n"
        "sys.stdout.write('stub loop ready\\n')\n"
        "sys.stdout.flush()\n"
        "signal.signal(signal.SIGTERM, lambda s, f: sys.exit(0))\n"
        "time.sleep(600)\n"
    )
    return script


@pytest.fixture
def manager(loops_dir, stub_script):
    return LoopManager(
        loops_dir=loops_dir,
        lazyown_script=stub_script,
        max_concurrent=2,
    )


class TestValidateTarget:
    def test_accepts_ipv4(self):
        assert validate_target("192.168.1.10") == "192.168.1.10"

    def test_accepts_ipv6(self):
        assert validate_target("::1") == "::1"

    def test_strips_whitespace(self):
        assert validate_target(" 10.0.0.1 ") == "10.0.0.1"

    def test_rejects_hostname(self):
        with pytest.raises(LoopValidationError):
            validate_target("evil.example.com")

    def test_rejects_command_injection(self):
        with pytest.raises(LoopValidationError):
            validate_target("127.0.0.1; rm -rf /")

    def test_rejects_metacharacters(self):
        with pytest.raises(LoopValidationError):
            validate_target("10.0.0.1 && cat /etc/passwd")

    def test_rejects_non_string(self):
        with pytest.raises(LoopValidationError):
            validate_target(1234)

    def test_rejects_empty(self):
        with pytest.raises(LoopValidationError):
            validate_target("   ")


class TestSanitizeGoal:
    def test_defaults_on_empty(self):
        assert sanitize_goal(None) == DEFAULT_GOAL
        assert sanitize_goal("") == DEFAULT_GOAL

    def test_collapses_whitespace(self):
        assert sanitize_goal("  gain   access  ") == "gain access"

    def test_rejects_newlines(self):
        with pytest.raises(LoopValidationError):
            sanitize_goal("goal\nrm -rf /")

    def test_rejects_quotes(self):
        with pytest.raises(LoopValidationError):
            sanitize_goal("goal ' && whoami")

    def test_rejects_semicolons(self):
        with pytest.raises(LoopValidationError):
            sanitize_goal("a; b")

    def test_rejects_too_long(self):
        with pytest.raises(LoopValidationError):
            sanitize_goal("a" * 300)

    def test_accepts_plain_words(self):
        assert sanitize_goal("gain initial access (phase 1)") == "gain initial access (phase 1)"


class TestClampInt:
    def test_default_on_none(self):
        assert clamp_int(None, "rounds", 6, 1, 50) == 6

    def test_clamps_low(self):
        assert clamp_int("0", "rounds", 6, 1, 50) == 1

    def test_clamps_high(self):
        assert clamp_int("999", "rounds", 6, 1, 50) == 50

    def test_rejects_non_numeric(self):
        with pytest.raises(LoopValidationError):
            clamp_int("abc", "rounds", 6, 1, 50)


class TestValidateLoopId:
    def test_accepts_hex32(self):
        assert validate_loop_id("a" * 32) == "a" * 32

    def test_rejects_traversal(self):
        with pytest.raises(LoopNotFoundError):
            validate_loop_id("../../etc/passwd")

    def test_rejects_non_hex(self):
        with pytest.raises(LoopNotFoundError):
            validate_loop_id("xyz")


class TestSpawnAndRegistry:
    def test_start_spawns_and_records(self, manager, loops_dir):
        record = manager.start(LoopSpec(kind=KIND_LAZY_NMAP, target="127.0.0.1"), operator="tester")
        assert record["kind"] == KIND_LAZY_NMAP
        assert record["target"] == "127.0.0.1"
        assert record["status"] == "running"
        assert record["pid"] > 0
        assert (loops_dir / record["id"] / "profile.yaml").exists()
        assert (loops_dir / record["id"] / "output.log").exists()
        profile = (loops_dir / record["id"] / "profile.yaml").read_text()
        assert "rhost: 127.0.0.1" in profile
        manager.stop(record["id"])

    def test_argv_has_no_shell(self, manager):
        record = manager.start(
            LoopSpec(kind=KIND_AUTO_LOOP, target="127.0.0.1", goal="gain access"),
            operator="tester",
        )
        argv = record["argv"]
        assert "auto_loop" in record["command"]
        assert "--no-progress" in record["command"]
        assert "--target 127.0.0.1" in record["command"]
        assert "gain access" in record["command"]
        assert argv[-1] == record["command"]
        assert record["target"] == "127.0.0.1"
        assert record["command"].startswith("auto_loop --no-progress")
        manager.stop(record["id"])

    def test_invalid_kind_rejected(self, manager):
        with pytest.raises(LoopValidationError):
            manager.start(LoopSpec(kind="rm -rf", target="127.0.0.1"))

    def test_invalid_target_rejected(self, manager):
        with pytest.raises(LoopValidationError):
            manager.start(LoopSpec(kind=KIND_LAZY_NMAP, target="not-an-ip"))

    def test_concurrency_cap(self, manager):
        first = manager.start(LoopSpec(kind=KIND_LAZY_NMAP, target="127.0.0.1"))
        second = manager.start(LoopSpec(kind=KIND_LAZY_NMAP, target="127.0.0.2"))
        with pytest.raises(LoopValidationError):
            manager.start(LoopSpec(kind=KIND_LAZY_NMAP, target="127.0.0.3"))
        manager.stop(first["id"])
        manager.stop(second["id"])

    def test_list_loops_sorted_newest_first(self, manager):
        first = manager.start(LoopSpec(kind=KIND_LAZY_NMAP, target="127.0.0.1"))
        time.sleep(0.02)
        second = manager.start(LoopSpec(kind=KIND_LAZY_NMAP, target="127.0.0.2"))
        loops = manager.list_loops()
        assert loops[0]["id"] == second["id"]
        assert loops[1]["id"] == first["id"]
        manager.stop(first["id"])
        manager.stop(second["id"])

    def test_registry_survives_restart(self, manager, loops_dir):
        record = manager.start(LoopSpec(kind=KIND_LAZY_NMAP, target="127.0.0.1"))
        fresh = LoopManager(loops_dir=loops_dir)
        loops = fresh.list_loops()
        assert any(loop["id"] == record["id"] for loop in loops)
        manager.stop(record["id"])

    def test_metadata_written(self, manager, loops_dir):
        record = manager.start(
            LoopSpec(kind=KIND_LAZY_NMAP, target="127.0.0.1"), operator="tester"
        )
        meta = json.loads((loops_dir / record["id"] / "metadata.json").read_text())
        assert meta["id"] == record["id"]
        assert meta["started_by"] == "tester"
        manager.stop(record["id"])


class TestLogReading:
    def test_read_log_chunk(self, manager, loops_dir):
        record = manager.start(LoopSpec(kind=KIND_LAZY_NMAP, target="127.0.0.1"))
        time.sleep(0.4)
        data = manager.read_log(record["id"], 0)
        assert data["loop_id"] == record["id"]
        assert data["offset"] >= 0
        manager.stop(record["id"])

    def test_read_log_unknown_loop(self, manager):
        with pytest.raises(LoopNotFoundError):
            manager.read_log("f" * 32, 0)

    def test_read_log_confinement(self, manager, loops_dir):
        record = manager.start(LoopSpec(kind=KIND_LAZY_NMAP, target="127.0.0.1"))
        with pytest.raises(LoopNotFoundError):
            evil = dict(manager.get_loop(record["id"]))
            evil["log_path"] = str(loops_dir.parent / "evil.txt")
            manager._resolve_log_path(evil)
        manager.stop(record["id"])

    def test_read_log_offset_beyond_size(self, manager):
        record = manager.start(LoopSpec(kind=KIND_LAZY_NMAP, target="127.0.0.1"))
        time.sleep(0.4)
        data = manager.read_log(record["id"], 10**12)
        assert data["chunk"] == ""
        manager.stop(record["id"])


class TestStop:
    def test_stop_terminates_process(self, manager):
        record = manager.start(LoopSpec(kind=KIND_LAZY_NMAP, target="127.0.0.1"))
        time.sleep(0.4)
        updated = manager.stop(record["id"])
        assert updated["status"] in ("stopped", "stopping")
        for _ in range(50):
            current = manager.get_loop(record["id"])
            if current["status"] in ("stopped", "lost"):
                break
            time.sleep(0.1)
        assert manager.get_loop(record["id"])["status"] in ("stopped", "lost")

    def test_stop_unknown_loop(self, manager):
        with pytest.raises(LoopNotFoundError):
            manager.stop("e" * 32)

    def test_stop_finished_loop_rejected(self, manager):
        record = manager.start(
            LoopSpec(kind=KIND_LAZY_NMAP, target="127.0.0.1"),
        )
        manager.stop(record["id"])
        for _ in range(60):
            if manager.get_loop(record["id"])["status"] != "stopping":
                break
            time.sleep(0.1)
        if manager.get_loop(record["id"])["status"] in ("stopped", "lost"):
            with pytest.raises(LoopValidationError):
                manager.stop(record["id"])

class TestLifecycle:
    def test_quick_exit_marks_finished(self, loops_dir, tmp_path):
        script = tmp_path / "quick.py"
        script.write_text("import sys\nsys.stdout.write('done\\n')\n")
        manager = LoopManager(loops_dir=loops_dir, lazyown_script=script)
        record = manager.start(LoopSpec(kind=KIND_LAZY_NMAP, target="127.0.0.1"))
        for _ in range(50):
            if manager.get_loop(record["id"])["status"] != "running":
                break
            time.sleep(0.1)
        finished = manager.get_loop(record["id"])
        assert finished["status"] == "finished"
        assert finished["exit_code"] == 0
        data = manager.read_log(record["id"], 0)
        assert "done" in data["chunk"]

    def test_sigterm_resistant_process_is_killed(self, loops_dir, tmp_path):
        script = tmp_path / "stubborn.py"
        script.write_text(
            "import signal, time\n"
            "signal.signal(signal.SIGTERM, signal.SIG_IGN)\n"
            "signal.signal(signal.SIGINT, signal.SIG_IGN)\n"
            "time.sleep(600)\n"
        )
        manager = LoopManager(loops_dir=loops_dir, lazyown_script=script)
        record = manager.start(LoopSpec(kind=KIND_LAZY_NMAP, target="127.0.0.1"))
        manager.stop(record["id"])
        for _ in range(100):
            if manager.get_loop(record["id"])["status"] != "stopping":
                break
            time.sleep(0.1)
        assert manager.get_loop(record["id"])["status"] in ("stopped", "lost")

    def test_summary_shape(self, manager):
        record = manager.start(LoopSpec(kind=KIND_LAZY_NMAP, target="127.0.0.1"))
        summary = manager.summary()
        assert summary["total"] >= 1
        assert "by_status" in summary
        assert "127.0.0.1" in summary["by_target"]
        manager.stop(record["id"])
