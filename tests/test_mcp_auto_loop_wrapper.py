"""MCP auto_loop wrapper contract: one runner, no dual engines.

Every scenario states Given, When, Then. The MCP tool routes through
``modules.lazy_runner.run_loop_command`` — the same runner behind the
``auto_loop``/``lazy_loop`` CLI verbs — so MCP runs get the full gate set
(budget confirmation, preflight, bootstrap, loop audit). Failures surface
honestly instead of falling back into a second loop.
"""

from __future__ import annotations

import pytest


def _patched(monkeypatch, tmp_path, *, run_result=None, raising=False, refused=False):
    """Patch the shared runner path plus payload loader; return captured calls."""
    import modules.lazy_loop as loop
    import modules.lazy_runner as runner
    import skills.lazyown_mcp as mcp

    store = tmp_path / "lazy"
    store.mkdir(parents=True, exist_ok=True)
    monkeypatch.setattr(loop, "STORE_DIR", store, raising=False)
    monkeypatch.setattr(loop, "_store_path", lambda name: store / name, raising=False)
    import json as _json

    payload_file = tmp_path / "payload.json"
    payload_file.write_text(_json.dumps({"rhost": "10.0.0.9"}))
    monkeypatch.setattr(mcp, "PAYLOAD_FILE", payload_file, raising=False)

    runs: list[tuple] = []
    if raising:

        def _boom(shell, params, line, verb):
            raise RuntimeError("runner down")

        monkeypatch.setattr(runner, "run_loop_command", _boom)
        return runs
    if refused:

        def _refuse(shell, params, line, verb):
            return {"error": "no goal, task or target"}

        monkeypatch.setattr(runner, "run_loop_command", _refuse)
        return runs

    def _fake_run(shell, params, line, verb):
        runs.append((params, line, verb))
        return run_result or {
            "task_id": "t0007",
            "status": "done",
            "rounds": 2,
            "overview": {"intents": [1, 2], "facts": 4, "findings": 1},
        }

    monkeypatch.setattr(runner, "run_loop_command", _fake_run)
    return runs


def test_fast_path_routes_through_the_shared_runner(monkeypatch, tmp_path):
    """Given no legacy flag, When the tool runs, Then the shared runner receives the run."""
    runs = _patched(monkeypatch, tmp_path)
    from skills.lazyown_mcp import call_tool

    response = loop_join(call_tool("lazyown_auto_loop", {"target": "10.0.0.9", "objective": "probe 10.0.0.9", "rounds": 2}))
    assert runs, "runner must be invoked"
    (params, line, verb) = runs[0]
    assert verb == "auto_loop"
    assert params == {"rhost": "10.0.0.9"}
    assert "--target 10.0.0.9" in line and "--rounds 2" in line
    text = _text(response)
    assert "t0007" in text and "legacy engine retired" not in text


def test_legacy_flag_annotates_but_routes_shared(monkeypatch, tmp_path):
    """Given legacy=true, When the tool runs, Then the runner still runs and output notes retirement."""
    runs = _patched(monkeypatch, tmp_path)
    from skills.lazyown_mcp import call_tool

    response = loop_join(call_tool("lazyown_auto_loop", {"target": "10.0.0.9", "legacy": True}))
    assert runs, "runner must be invoked"
    assert "legacy engine retired" in _text(response)


def test_runner_failure_surfaces(monkeypatch, tmp_path):
    """Given a runner outage, When the tool runs, Then the failure message is honest."""
    _patched(monkeypatch, tmp_path, raising=True)
    from skills.lazyown_mcp import call_tool

    response = loop_join(call_tool("lazyown_auto_loop", {"target": "10.0.0.9"}))
    assert "runner failure" in _text(response)
    assert "runner down" in _text(response)


def test_refused_run_reports_the_reason(monkeypatch, tmp_path):
    """Given a run refused by the runner (no goal/target), When the tool runs, Then the reason surfaces."""
    _patched(monkeypatch, tmp_path, refused=True)
    from skills.lazyown_mcp import call_tool

    response = loop_join(call_tool("lazyown_auto_loop", {}))
    text = _text(response)
    assert "run refused" in text
    assert "no goal, task or target" in text


def test_preflight_failed_summary_still_renders_the_task(monkeypatch, tmp_path):
    """Given a preflight failure summary, When the tool runs, Then the task id and error render."""
    runs = _patched(
        monkeypatch,
        tmp_path,
        run_result={"task_id": "t0009", "status": "preflight_failed", "rounds": 0, "overview": {}, "error": "target unreachable"},
    )
    from skills.lazyown_mcp import call_tool

    response = loop_join(call_tool("lazyown_auto_loop", {"target": "10.0.0.9"}))
    assert runs, "runner must be invoked"
    text = _text(response)
    assert "t0009" in text and "preflight_failed" in text and "target unreachable" in text


def test_schema_matches_the_shared_flags():
    """Given the tool schema, When inspected, Then it documents the shared runner limits."""
    from skills.mcp_tools.auto_loop import TOOL

    props = TOOL.inputSchema["properties"]
    assert "target" in props and "objective" in props and "legacy" in props
    assert "clamp 50" in props["rounds"]["description"]
    assert "max 5" in props["workers"]["description"]


def test_loop_line_translation():
    """Given tool arguments, When translated, Then only meaningful flags are emitted."""
    from skills.mcp_tools.auto_loop import _loop_line

    assert _loop_line({}) == []
    assert _loop_line({"max_steps": 3, "workers": 2, "timeout": 90, "objective": "poke"}) == [
        "poke",
        "--rounds",
        "3",
        "--workers",
        "2",
        "--timeout",
        "90.0",
    ]
    assert _loop_line({"rounds": "bogus"}) == []


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
