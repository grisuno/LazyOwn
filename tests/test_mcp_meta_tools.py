"""MCP progressive disclosure meta-tools tests."""

from __future__ import annotations

import asyncio
import importlib.util
import sys
from pathlib import Path

import pytest

SKILLS_DIR = Path(__file__).resolve().parent.parent / "skills"
META_NAMES = {"lazyown_discover", "lazyown_inspect_tool_schema", "lazyown_execute_verb"}


def _load_runtime():
    spec = importlib.util.spec_from_file_location("lazyown_mcp", SKILLS_DIR / "lazyown_mcp.py")
    module = importlib.util.module_from_spec(spec)
    sys.argv = ["lazyown_mcp"]
    spec.loader.exec_module(module)
    return module


@pytest.fixture(scope="module")
def runtime():
    return _load_runtime()


class TestListFilter:
    def test_meta_tools_registered(self, runtime):
        names = asyncio.run(
            runtime._all_tools.__wrapped__() if hasattr(runtime._all_tools, "__wrapped__") else runtime._all_tools()
        )
        names = {t.name for t in names}
        assert META_NAMES <= names

    def test_meta_only_listing_keeps_three(self, runtime, monkeypatch):
        monkeypatch.setenv("LAZYOWN_MCP_META", "1")
        tools = asyncio.run(runtime._all_tools())
        filtered = [t for t in tools if getattr(t, "name", "") in runtime._META_TOOL_NAMES]
        assert {t.name for t in filtered} == META_NAMES


class TestDiscover:
    def test_keyword_search(self, runtime):
        out = asyncio.run(runtime.call_tool("lazyown_discover", {"query": "beacon", "limit": 5}))
        assert "matching" in out[0].text
        assert "beacon" in out[0].text.lower()

    def test_limit_respected(self, runtime):
        out = asyncio.run(runtime.call_tool("lazyown_discover", {"limit": 3}))
        lines = [line for line in out[0].text.splitlines() if line.startswith("  lazyown_")]
        assert len(lines) <= 3


class TestInspect:
    def test_known_tool_schema(self, runtime):
        out = asyncio.run(runtime.call_tool("lazyown_inspect_tool_schema", {"tool_name": "lazyown_auto_populate"}))
        assert "inputSchema" in out[0].text

    def test_unknown_tool_errors(self, runtime):
        out = asyncio.run(runtime.call_tool("lazyown_inspect_tool_schema", {"tool_name": "lazyown_nope"}))
        assert "Unknown tool" in out[0].text


class TestExecute:
    def test_refuses_self_execution(self, runtime):
        out = asyncio.run(runtime.call_tool("lazyown_execute_verb", {"tool_name": "lazyown_execute_verb"}))
        assert "Refusing" in out[0].text

    def test_requires_tool_name(self, runtime):
        out = asyncio.run(runtime.call_tool("lazyown_execute_verb", {}))
        assert "Pass a tool_name" in out[0].text

    def test_dispatches_real_tool(self, runtime):
        out = asyncio.run(runtime.call_tool("lazyown_execute_verb", {"tool_name": "lazyown_campaign_sitrep"}))
        assert out and out[0].text
