"""MCP tool ``lazyown_c2_script`` (migrated from the call_tool dispatch chain)."""

from __future__ import annotations

import asyncio
import json
from typing import Any

from mcp import types
from mcp_tools._context import MCPContext

TOOL = types.Tool(
    name="lazyown_c2_script",
    description=(
        "Ask the LazyOwn C2 AI (Groq) to generate an exploit or pentest script. "
        "Requires the C2 server to be running. "
        "Returns generated code ready to use."
    ),
    inputSchema={
        "type": "object",
        "properties": {
            "request": {
                "type": "string",
                "description": "Script request — describe what the script should do.",
            }
        },
        "required": ["request"],
    },
)


async def handle(arguments: dict[str, Any], tool_name: str, ctx: MCPContext) -> list:
    """Handle the lazyown_c2_script MCP tool."""
    request = arguments["request"]
    result = await asyncio.get_event_loop().run_in_executor(
        None, lambda: ctx.c2_request("/script", method="POST", body={"request": request})
    )
    if "_error" in result:
        return ctx.text(tool_name, f"C2 unreachable or error: {result['_error']}")
    return ctx.text(tool_name, result.get("result", result.get("response", json.dumps(result))))
