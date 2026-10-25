"""Contract tests for UnifiedBridge.delegate agent polling.

SDD contract: ``delegate`` drives the public agent-bridge API
(``start_agent`` + ``get_agent_status``/``get_agent_result``); the
constructor/thread internals of ``AgentBridgeWorker`` are never touched.
"""

from __future__ import annotations

from itertools import repeat

import pytest


@pytest.fixture
def unified_bridge(monkeypatch):
    from modules import unified_bridge

    monkeypatch.setattr(unified_bridge, "_AGENT_POLL_SECONDS", 0.0)
    instance = unified_bridge.UnifiedBridge()
    monkeypatch.setattr(instance, "_publish", lambda *args, **kwargs: None)
    return instance


def _patch_bridge_api(monkeypatch, statuses, result):
    from modules import mcp_agent_bridge

    started: dict = {}

    def fake_start(goal, backend, runner, max_iterations=8):
        started.update(goal=goal, backend=backend, runner=runner, max_iterations=max_iterations)
        return "agent-42"

    monkeypatch.setattr(mcp_agent_bridge, "start_agent", fake_start)
    monkeypatch.setattr(mcp_agent_bridge, "get_agent_status", lambda agent_id: next(statuses))
    monkeypatch.setattr(mcp_agent_bridge, "get_agent_result", lambda agent_id: result)
    return started


def test_delegate_polls_until_completion(monkeypatch, unified_bridge):
    statuses = iter([{"status": "running"}, {"status": "completed"}])
    started = _patch_bridge_api(monkeypatch, statuses, {"status": "completed", "answer": "found CVE"})

    result = unified_bridge.delegate("Analyze CVE-2023-1234", backend="groq", timeout=10)

    assert result.agent_id == "agent-42"
    assert result.status == "completed"
    assert result.result == "found CVE"
    assert result.error == ""
    assert started["goal"] == "Analyze CVE-2023-1234"
    assert started["backend"] == "groq"
    assert started["runner"] == unified_bridge._run_agent_command


def test_delegate_times_out_when_agent_never_finishes(monkeypatch, unified_bridge):
    statuses = iter(repeat({"status": "running"}, 5))
    _patch_bridge_api(monkeypatch, statuses, {"status": "running"})

    result = unified_bridge.delegate("Analyze CVE", timeout=0)

    assert result.status == "timeout"
    assert result.result == ""
    assert result.error == ""


def test_delegate_reports_agent_failure(monkeypatch, unified_bridge):
    statuses = iter([{"status": "failed"}])
    _patch_bridge_api(monkeypatch, statuses, {"status": "failed", "answer": "partial"})

    result = unified_bridge.delegate("Analyze CVE", timeout=10)

    assert result.status == "failed"
    assert result.result == "partial"
    assert result.error == "agent reported failure"


def test_delegate_surfaces_missing_agent(monkeypatch, unified_bridge):
    statuses = iter([{"error": "Agent nope not found."}])
    _patch_bridge_api(monkeypatch, statuses, {})

    result = unified_bridge.delegate("Analyze CVE", timeout=10)

    assert result.status == "failed"
    assert "not found" in result.error


def test_delegate_wraps_start_errors(monkeypatch, unified_bridge):
    from modules import mcp_agent_bridge

    def boom(*args, **kwargs):
        raise RuntimeError("backend exploded")

    monkeypatch.setattr(mcp_agent_bridge, "start_agent", boom)

    result = unified_bridge.delegate("Analyze CVE", timeout=10)

    assert result.agent_id == ""
    assert result.error == "backend exploded"
