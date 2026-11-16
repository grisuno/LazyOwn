"""Behaviour tests for the LazyOwn programmatic SDK facade."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from sdk import ConfigValidationError, Lazy, ScopeBlocked, SessionPathError


def _write_payload(tmp_path: Path, data: dict) -> Path:
    path = tmp_path / "payload.json"
    path.write_text(json.dumps(data), encoding="utf-8")
    return path


def test_config_all_reads_fresh(tmp_path):
    payload = _write_payload(tmp_path, {"rhost": "10.0.0.1"})
    lazy = Lazy(payload_path=payload, sessions_dir=tmp_path / "sessions")
    assert lazy.config.all()["rhost"] == "10.0.0.1"


def test_config_get_default(tmp_path):
    payload = _write_payload(tmp_path, {})
    lazy = Lazy(payload_path=payload, sessions_dir=tmp_path / "sessions")
    assert lazy.config.get("missing", "fallback") == "fallback"


def test_config_set_persists(tmp_path):
    payload = _write_payload(tmp_path, {"rhost": "10.0.0.1"})
    lazy = Lazy(payload_path=payload, sessions_dir=tmp_path / "sessions")
    lazy.config.set("rhost", "10.10.11.5")
    assert json.loads(payload.read_text())["rhost"] == "10.10.11.5"


def test_config_set_rejects_invalid(tmp_path):
    payload = _write_payload(tmp_path, {"rport": "80"})
    lazy = Lazy(payload_path=payload, sessions_dir=tmp_path / "sessions")
    with pytest.raises(ConfigValidationError):
        lazy.config.set("rport", "not-a-port")


def test_sessions_list_and_read(tmp_path):
    sessions = tmp_path / "sessions"
    sessions.mkdir()
    (sessions / "note.txt").write_text("hello", encoding="utf-8")
    lazy = Lazy(payload_path=_write_payload(tmp_path, {}), sessions_dir=sessions)
    assert "note.txt" in lazy.sessions.list()
    assert lazy.sessions.read("note.txt") == "hello"


def test_sessions_read_nested(tmp_path):
    sessions = tmp_path / "sessions"
    (sessions / "logs").mkdir(parents=True)
    (sessions / "logs" / "beacon.log").write_text("ping", encoding="utf-8")
    lazy = Lazy(payload_path=_write_payload(tmp_path, {}), sessions_dir=sessions)
    assert lazy.sessions.read("logs/beacon.log") == "ping"


def test_sessions_read_missing_is_empty(tmp_path):
    sessions = tmp_path / "sessions"
    sessions.mkdir()
    lazy = Lazy(payload_path=_write_payload(tmp_path, {}), sessions_dir=sessions)
    assert lazy.sessions.read("ghost.txt") == ""


def test_sessions_path_traversal_blocked(tmp_path):
    sessions = tmp_path / "sessions"
    sessions.mkdir()
    lazy = Lazy(payload_path=_write_payload(tmp_path, {}), sessions_dir=sessions)
    with pytest.raises(SessionPathError):
        lazy.sessions.read("../payload.json")


def test_sh_runs_through_injected_runner(tmp_path):
    calls = []

    def fake_runner(command, timeout):
        calls.append((command, timeout))
        return "output"

    lazy = Lazy(
        payload_path=_write_payload(tmp_path, {}),
        sessions_dir=tmp_path / "sessions",
        command_runner=fake_runner,
    )
    assert lazy.sh("id") == "output"
    assert calls[0][0] == "id"


def test_scope_check_blocks_offensive_target(tmp_path):
    def enforcing(command, target):
        if target == "1.2.3.4":
            raise ScopeBlocked(target)

    lazy = Lazy(
        payload_path=_write_payload(tmp_path, {}),
        sessions_dir=tmp_path / "sessions",
        scope_check=enforcing,
        command_runner=lambda command, timeout: "",
    )
    with pytest.raises(ScopeBlocked):
        lazy.recon.nmap("1.2.3.4")


def test_scope_dormant_without_check(tmp_path):
    captured = {}

    def fake_runner(command, timeout):
        captured["command"] = command
        return ""

    lazy = Lazy(
        payload_path=_write_payload(tmp_path, {}),
        sessions_dir=tmp_path / "sessions",
        command_runner=fake_runner,
    )
    lazy.recon.ports("10.0.0.1")
    assert "command" not in captured
