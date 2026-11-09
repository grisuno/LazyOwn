"""MCP tool ``lazyown_c2_command`` (migrated from the call_tool dispatch chain)."""

from __future__ import annotations

import asyncio
import json
from typing import Any

from mcp import types
from mcp_tools._context import MCPContext

TOOL = types.Tool(
    name="lazyown_c2_command",
    description=(
        "Issue a tasking command to a specific beacon connected to the LazyOwn C2 server. "
        "Available beacon commands include: whoami, download:<file>, upload:<file>, "
        "rev, exfil, stealth_on, stealth_off, discover, portscan, softenum, "
        "persist, cleanlogs, amsi, escalatelin, terminate, and more."
    ),
    inputSchema={
        "type": "object",
        "properties": {
            "client_id": {
                "type": "string",
                "description": "The beacon/client ID to task.",
            },
            "command": {
                "type": "string",
                "description": "Command to send to the beacon.",
            },
        },
        "required": ["client_id", "command"],
    },
)


async def handle(arguments: dict[str, Any], tool_name: str, ctx: MCPContext) -> list:
    """Handle the lazyown_c2_command MCP tool."""
    client_id = arguments["client_id"]
    command = arguments["command"]
    body = {"client_id": client_id, "command": command}
    result = await asyncio.get_event_loop().run_in_executor(
        None, lambda: ctx.c2_request("/issue_command", method="POST", body=body)
    )
    return ctx.text(tool_name, json.dumps(result, indent=2))
