"""MCP tool ``lazyown_c2_redop`` (migrated from the call_tool dispatch chain)."""

from __future__ import annotations

import asyncio
import json
from typing import Any

from mcp import types
from mcp_tools._context import MCPContext

TOOL = types.Tool(
    name="lazyown_c2_redop",
    description=(
        "Ask the LazyOwn C2 AI (Groq) to plan a red team operation. "
        "Requires the C2 server to be running. "
        "Returns a structured attack plan based on the scenario."
    ),
    inputSchema={
        "type": "object",
        "properties": {
            "scenario": {
                "type": "string",
                "description": "Red team scenario or objective to plan.",
            }
        },
        "required": ["scenario"],
    },
)


async def handle(arguments: dict[str, Any], tool_name: str, ctx: MCPContext) -> list:
    """Handle the lazyown_c2_redop MCP tool."""
    scenario = arguments["scenario"]
    result = await asyncio.get_event_loop().run_in_executor(
        None, lambda: ctx.c2_request("/redop", method="POST", body={"scenario": scenario})
    )
    if "_error" in result:
        return ctx.text(tool_name, f"C2 unreachable or error: {result['_error']}")
    return ctx.text(tool_name, result.get("result", result.get("response", json.dumps(result))))
