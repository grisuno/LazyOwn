"""MCP tool ``lazyown_c2_search_agent`` (migrated from the call_tool dispatch chain)."""

from __future__ import annotations

import asyncio
import json
from typing import Any

from mcp import types
from mcp_tools._context import MCPContext

TOOL = types.Tool(
    name="lazyown_c2_search_agent",
    description=(
        "Delegate a research query to the LazyOwn C2 AI search agent (Groq). "
        "Requires the C2 server to be running. "
        "Use for OSINT queries, technique lookups, or tooling research."
    ),
    inputSchema={
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "Research query or OSINT question.",
            }
        },
        "required": ["query"],
    },
)


async def handle(arguments: dict[str, Any], tool_name: str, ctx: MCPContext) -> list:
    """Handle the lazyown_c2_search_agent MCP tool."""
    query = arguments["query"]
    result = await asyncio.get_event_loop().run_in_executor(
        None, lambda: ctx.c2_request("/search", method="POST", body={"query": query})
    )
    if "_error" in result:
        return ctx.text(tool_name, f"C2 unreachable or error: {result['_error']}")
    return ctx.text(tool_name, result.get("result", result.get("response", json.dumps(result))))
