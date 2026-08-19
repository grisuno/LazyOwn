#!/usr/bin/env python3
"""
LazyOwn MCP OpenCode bridge.

Curated, short-named MCP server for autonomous OpenCode agents running on local
models (e.g. ollama/qwen3.8:27b). Local models mis-handle large tool catalogs and
re-namespace long names like ``lazyown_lazyown_campaign_sitrep``. This bridge
exposes only the essential LazyOwn tools under short, memorable names and proxies
every call back to the full ``lazyown_mcp`` server, which keeps the single source
of truth for logic, permissions and hooks.

Usage:
    python3 skills/lazyown_mcp_opencode.py

The stdio transport is used (default), matching OpenCode local MCP config.
"""

import asyncio
import sys
from pathlib import Path
from typing import Any

from mcp import types
from mcp.server import Server
from mcp.server.stdio import stdio_server

_mcp_root = Path(__file__).parent
for _p in [str(_mcp_root), str(_mcp_root.parent / "modules")]:
    if _p not in sys.path:
        sys.path.insert(0, _p)

from lazyown_mcp import call_tool as _call_tool  # noqa: E402
from lazyown_mcp import list_tools as _list_tools  # noqa: E402

server = Server("lazyown")

CURATED_TOOLS: dict[str, str] = {
    "sitrep": "lazyown_campaign_sitrep",
    "session_init": "lazyown_session_init",
    "set_config": "lazyown_set_config",
    "run": "lazyown_run_command",
    "auto_populate": "lazyown_auto_populate",
    "facts": "lazyown_facts_show",
    "recommend_next": "lazyown_recommend_next",
    "soul": "lazyown_soul",
    "get_config": "lazyown_get_config",
    "list_sessions": "lazyown_list_sessions",
    "read_session_file": "lazyown_read_session_file",
    "get_beacons": "lazyown_get_beacons",
    "next_objective": "lazyown_next_objective",
    "phase_guide": "lazyown_phase_guide",
    "command_next": "lazyown_command_next",
}


@server.list_tools()
async def list_tools() -> list[types.Tool]:
    """Expose the curated subset under short names, keeping original schemas."""
    all_tools = await _list_tools()
    by_name = {tool.name: tool for tool in all_tools}
    curated: list[types.Tool] = []
    for short_name, full_name in CURATED_TOOLS.items():
        original = by_name.get(full_name)
        if original is not None:
            curated.append(
                types.Tool(
                    name=short_name,
                    description=original.description,
                    inputSchema=original.inputSchema,
                )
            )
    return curated


@server.call_tool()
async def call_tool(name: str, arguments: dict[str, Any]) -> list[types.TextContent]:
    """Proxy the short name to the full LazyOwn MCP handler."""
    full_name = CURATED_TOOLS.get(name)
    if full_name is None:
        raise ValueError(f"Unknown curated tool '{name}'")
    return await _call_tool(full_name, arguments)


async def main() -> None:
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())


if __name__ == "__main__":
    asyncio.run(main())
