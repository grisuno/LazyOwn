"""MCP tool ``lazyown_run_api`` (migrated from the call_tool dispatch chain)."""

from __future__ import annotations

import asyncio
import json
from typing import Any

from mcp import types
from mcp_tools._context import MCPContext

TOOL = types.Tool(
    name="lazyown_run_api",
    description=(
        "Execute a shell command on the C2 server host via the /api/run endpoint. Requires the C2 server to be running."
    ),
    inputSchema={
        "type": "object",
        "properties": {
            "command": {
                "type": "string",
                "description": "Shell command to run on the C2 host.",
            }
        },
        "required": ["command"],
    },
)


async def handle(arguments: dict[str, Any], tool_name: str, ctx: MCPContext) -> list:
    """Handle the lazyown_run_api MCP tool."""
    command = arguments["command"]
    body = {"command": command}
    result = await asyncio.get_event_loop().run_in_executor(
        None, lambda: ctx.c2_request("/api/run", method="POST", body=body)
    )
    return ctx.text(tool_name, json.dumps(result, indent=2))
