"""Behaviour tests for the lazymode runners and surface index."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from sdk.lazymode import build_index, run, run_python, search
from sdk.lazymode.runner import build_scope_check


def _payload(tmp_path: Path, data: dict) -> Path:
    path = tmp_path / "payload.json"
    path.write_text(json.dumps(data), encoding="utf-8")
    return path


def test_run_python_returns_result(tmp_path):
    payload = _payload(tmp_path, {"rhost": "10.0.0.1"})
    sessions = tmp_path / "sessions"
    sessions.mkdir()
    script = "result = lazy.config.get('rhost')"
    outcome = run_python(script, payload_path=payload, sessions_dir=sessions)
    assert outcome.ok is True
    assert outcome.result == "10.0.0.1"
    assert outcome.backend == "python"


def test_run_python_captures_stdout(tmp_path):
    payload = _payload(tmp_path, {})
    sessions = tmp_path / "sessions"
    sessions.mkdir()
    outcome = run_python("print('hello')\nresult = 1", payload_path=payload, sessions_dir=sessions)
    assert outcome.ok is True
    assert "hello" in outcome.stdout


def test_run_python_reports_error(tmp_path):
    payload = _payload(tmp_path, {})
    sessions = tmp_path / "sessions"
    sessions.mkdir()
    outcome = run_python("raise RuntimeError('boom')", payload_path=payload, sessions_dir=sessions)
    assert outcome.ok is False
    assert "boom" in outcome.error


def test_run_python_config_set_persists(tmp_path):
    payload = _payload(tmp_path, {"rhost": "10.0.0.1"})
    sessions = tmp_path / "sessions"
    sessions.mkdir()
    outcome = run_python(
        "lazy.config.set('rhost', '10.10.11.5')\nresult = lazy.config.get('rhost')",
        payload_path=payload,
        sessions_dir=sessions,
    )
    assert outcome.result == "10.10.11.5"
    assert json.loads(payload.read_text())["rhost"] == "10.10.11.5"


def test_run_python_timeout(tmp_path):
    payload = _payload(tmp_path, {})
    sessions = tmp_path / "sessions"
    sessions.mkdir()
    outcome = run_python(
        "while True:\n    pass", payload_path=payload, sessions_dir=sessions, timeout=1.0
    )
    assert outcome.ok is False
    assert "timeout" in outcome.error


def test_run_python_bounds_flooding_stdout(tmp_path):
    payload = _payload(tmp_path, {})
    sessions = tmp_path / "sessions"
    sessions.mkdir()
    script = "print('x' * 100000)\nresult = 'ok'"
    outcome = run_python(script, payload_path=payload, sessions_dir=sessions)
    assert outcome.ok is True
    assert outcome.result == "ok"
    assert len(outcome.stdout) < 10000
    assert "truncated" in outcome.stdout


def test_run_dispatch_unknown_backend_raises():
    with pytest.raises(ValueError):
        run("result = 1", lang="ruby")


def test_scope_check_enforce_blocks(tmp_path):
    from sdk.errors import ScopeBlocked

    check = build_scope_check({"scope": ["10.0.0.0/24"], "scope_enforcement": "enforce"})
    with pytest.raises(ScopeBlocked):
        check("nmap", "8.8.8.8")


def test_scope_check_warn_allows():
    check = build_scope_check({"scope": ["10.0.0.0/24"], "scope_enforcement": "warn"})
    assert check("nmap", "8.8.8.8") is None


def test_index_contains_core_methods():
    paths = {entry["path"] for entry in build_index()}
    assert "lazy.config.set" in paths
    assert "lazy.recon.nmap" in paths
    assert "lazy.sh" in paths


def test_search_ranks_relevant():
    hits = search("scan ports nmap")
    assert hits
    assert any("recon" in hit["path"] for hit in hits)
