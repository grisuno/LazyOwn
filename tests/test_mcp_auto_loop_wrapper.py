"""MCP auto_loop wrapper contract: one orchestrator, no dual engines.

Every scenario states Given, When, Then. The MCP tool routes to
LazyEngine for real and legacy-flagged calls; the retired engine
surface stays gone and failures surface honestly instead of falling
back into a second loop.
"""

from __future__ import annotations

from types import SimpleNamespace

import pytest


def _patched(monkeypatch, tmp_path, *, run_result=None, raising=False):
    """Patch the LazyEngine path plus payload loader; return captured calls."""
    import modules.lazy_loop as loop
    import skills.lazyown_mcp as mcp

    store = tmp_path / "lazy"
    store.mkdir(parents=True, exist_ok=True)
    monkeypatch.setattr(loop, "STORE_DIR", store, raising=False)
    monkeypatch.setattr(loop, "_store_path", lambda name: store / name, raising=False)

    calls: dict[str, object] = {}
    engines: list[SimpleNamespace] = []

    if raising:

        class _Boom:
            def __init__(self, *args, **kwargs) -> None:
                """Simulate an engine import or construction failure."""
                raise RuntimeError("engine down")

        monkeypatch.setattr(mcp, "_load_payload", lambda: {"rhost": "10.0.0.9"}, raising=False)
        monkeypatch.setitem(
            __import__("sys").modules,
            "modules.lazy_engine",
            SimpleNamespace(LazyEngine=_Boom),
        )
        return engines, calls

    class _FakeEngine:
        def __init__(self) -> None:
            engines.append(self)
            self.calls: list[tuple] = []
            calls.setdefault("engine", self)

        def create_task(self, goal: str) -> dict:
            self.calls.append(("create_task", goal))
            return {"task_id": "t0007", "goal": goal}

        def ensure_target(self, task_id: str, target: str, reason: str = "") -> dict:
            self.calls.append(("ensure_target", task_id, target))
            return {"asset_id": 3}

        def run(self, task_id: str, max_rounds: int = 5, workers: int = 2, timeout_sec: float = 0.0) -> dict:
            self.calls.append(("run", task_id, max_rounds, workers, timeout_sec))
            return run_result or {
                "task_id": task_id,
                "status": "done",
                "rounds": max_rounds,
                "overview": {"intents": [1, 2], "facts": 4, "findings": 1},
            }

    monkeypatch.setattr(mcp, "_load_payload", lambda: {"rhost": "10.0.0.9"}, raising=False)
    monkeypatch.setitem(
        __import__("sys").modules,
        "modules.lazy_engine",
        SimpleNamespace(LazyEngine=_FakeEngine),
    )
    return engines, calls


def test_fast_path_runs_the_engine(monkeypatch, tmp_path):
    """Given no legacy flag, When the tool runs, Then the engine receives the run."""
    engines, _calls = _patched(monkeypatch, tmp_path)
    from skills.lazyown_mcp import call_tool

    response = loop_join(call_tool("lazyown_auto_loop", {"target": "10.0.0.9", "objective": "probe 10.0.0.9", "rounds": 2}))
    assert engines and len(engines) == 1
    engine_calls = engines[0].calls
    assert engine_calls[0][0] == "create_task"
    assert "probe 10.0.0.9" in engine_calls[0][1]
    assert ("run", "t0007") == engine_calls[2][:2]
    assert "legacy engine retired" not in _text(response)


def test_legacy_flag_annotates_but_routes_fast(monkeypatch, tmp_path):
    """Given legacy=true, When the tool runs, Then the engine still runs and output notes retirement."""
    engines, _calls = _patched(monkeypatch, tmp_path)
    from skills.lazyown_mcp import call_tool

    response = loop_join(call_tool("lazyown_auto_loop", {"target": "10.0.0.9", "legacy": True}))
    assert engines, "engine must be invoked"
    assert "legacy engine retired" in _text(response)


def test_engine_failure_surfaces(monkeypatch, tmp_path):
    """Given an engine outage, When the tool runs, Then the failure message is honest."""
    _patched(monkeypatch, tmp_path, raising=True)
    from skills.lazyown_mcp import call_tool

    response = loop_join(call_tool("lazyown_auto_loop", {"target": "10.0.0.9"}))
    assert "engine failure" in _text(response)
    assert "engine down" in _text(response)


def _text(response) -> str:
    """Flatten one TextContent list into a string."""
    import types as _types

    parts: list[str] = []
    for item in list(response):
        if isinstance(item, _types.SimpleNamespace) and isinstance(getattr(item, "text", ""), str):
            parts.append(item.text)
        elif isinstance(item, str):
            parts.append(item)
        else:
            parts.append(str(item))
    return "\n".join(parts)


def loop_join(coro):
    """Run one coroutine to completion on a fresh event loop."""
    import asyncio

    loop = asyncio.new_event_loop()
    try:
        return loop.run_until_complete(coro)
    finally:
        loop.close()
