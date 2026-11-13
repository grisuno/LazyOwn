"""Honest loop endings: exit-code mapping, autonomous gate and headless runner."""

from __future__ import annotations

import json

import pytest


def test_loop_exit_code_mapping():
    from modules.lazy_runner import loop_exit_code

    assert loop_exit_code({"status": "done", "verdict": {"verdict": "achieved"}}) == 0
    assert loop_exit_code({"status": "pentest_proven", "verdict": {"verdict": "achieved"}}) == 0
    assert loop_exit_code({"status": "done", "verdict": {}}) == 0
    assert loop_exit_code({"status": "done", "verdict": {"verdict": "partial"}}) == 1
    assert loop_exit_code({"status": "done", "verdict": {"verdict": "failed"}}) == 1
    assert loop_exit_code({"status": "exhausted"}) == 1
    assert (
        loop_exit_code(
            {"status": "exhausted", "verdict": {"verdict": "achieved", "evidence_verified": True}}
        )
        == 0
    )
    assert loop_exit_code({"status": "exhausted", "verdict": {"verdict": "achieved"}}) == 1
    assert (
        loop_exit_code({"status": "failed", "verdict": {"verdict": "achieved", "evidence_verified": True}})
        == 1
    )
    assert loop_exit_code({"status": "timeout"}) == 4
    assert (
        loop_exit_code(
            {"status": "timeout", "verdict": {"verdict": "achieved", "evidence_verified": True}}
        )
        == 0
    )
    assert loop_exit_code({"status": "handoff"}) == 1
    assert loop_exit_code({"error": "boom"}) == 1
    assert loop_exit_code({"cancelled": True}) == 1
    assert loop_exit_code({"mode": "multi-target", "failed": 0}) == 0
    assert loop_exit_code({"mode": "multi-target", "failed": 2}) == 1
    assert loop_exit_code(None) == 1


def test_autonomous_gate_raises_only_when_env_set(monkeypatch):
    from modules import lazy_runner

    result = {"status": "exhausted", "task_id": "t1"}
    monkeypatch.delenv(lazy_runner.AUTONOMOUS_ENV, raising=False)
    assert lazy_runner.autonomous_exit_gate(result) is None

    monkeypatch.setenv(lazy_runner.AUTONOMOUS_ENV, "1")
    with pytest.raises(SystemExit) as excinfo:
        lazy_runner.autonomous_exit_gate(result)
    assert excinfo.value.code == 1

    with pytest.raises(SystemExit) as excinfo:
        lazy_runner.autonomous_exit_gate({"status": "timeout"})
    assert excinfo.value.code == 4

    assert lazy_runner.autonomous_exit_gate({"status": "done", "verdict": {"verdict": "achieved"}}) is None


def test_write_loop_result_workspace(tmp_path, monkeypatch):
    from modules import lazy_runner
    from modules.lazy_runner import LoopRunConfig, write_loop_result

    workspace = tmp_path / "ws"
    workspace.mkdir()
    monkeypatch.setenv(lazy_runner.LOOP_WORKSPACE_ENV, str(workspace))
    config = LoopRunConfig(goal="own it", target="10.0.0.5")
    write_loop_result(config, {"task_id": "t5", "status": "exhausted", "rounds": 6, "verdict": {"verdict": "partial"}, "overview": {}})
    payload = json.loads((workspace / lazy_runner.LOOP_RESULT_FILENAME).read_text())
    assert payload["success"] is False
    assert payload["verdict"] == "partial"
    assert payload["task_id"] == "t5"
    assert payload["goal"] == "own it"


def test_write_loop_result_sessions_fallback(tmp_path, monkeypatch):
    from modules import lazy_runner
    from modules.lazy_runner import LoopRunConfig, write_loop_result

    monkeypatch.delenv(lazy_runner.LOOP_WORKSPACE_ENV, raising=False)
    monkeypatch.setattr(lazy_runner, "SESSIONS_DIR", str(tmp_path / "sessions"))
    config = LoopRunConfig(goal="g")
    write_loop_result(config, {"task_id": "t7", "status": "done", "verdict": {"verdict": "achieved"}, "overview": {}})
    payload = json.loads((tmp_path / "sessions" / "loop_result_t7.json").read_text())
    assert payload["success"] is True


class _ExitShell:
    def __init__(self, code) -> None:
        self._code = code

    def onecmd(self, cmd):
        raise SystemExit(self._code)


def test_headless_catches_systemexit():
    from cli.headless import HeadlessRunner

    runner = HeadlessRunner(_ExitShell(3), json_output=False)
    result = runner.run_command("auto_loop --target 10.0.0.5")
    assert result["success"] is False
    assert result["exit_code"] == 3
    assert runner.exit_code == 3


def test_headless_chain_stops_on_failure():
    from cli.headless import EXIT_ERROR, HeadlessRunner

    class _Shell:
        def __init__(self) -> None:
            self.calls = 0

        def onecmd(self, cmd):
            self.calls += 1
            if self.calls == 1:
                raise SystemExit(EXIT_ERROR)
            return False

    shell = _Shell()
    runner = HeadlessRunner(shell, json_output=False)
    results = runner.run_chain(["auto_loop a", "nmap_scan"])
    assert len(results) == 1
    assert shell.calls == 1
    assert runner.exit_code == EXIT_ERROR


def test_report_result_prints_verdict(capsys):
    from modules.lazy_runner import report_result

    report_result(
        {
            "task_id": "t9",
            "status": "done",
            "rounds": 3,
            "verdict": {"verdict": "achieved", "coverage_pct": 75.0, "confirmed": 2, "completion_reason": "shell", "path": "/tmp/r.md"},
            "overview": {"intents": [], "facts": 5, "findings": 4},
        }
    )
    out = capsys.readouterr().out
    assert "[verdict] achieved" in out
    assert "coverage=75.0%" in out
    assert "/tmp/r.md" in out
