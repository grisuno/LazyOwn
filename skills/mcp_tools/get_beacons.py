"""MCP tool ``lazyown_get_beacons``: list connected C2 beacons."""

from __future__ import annotations

import asyncio
import json
from typing import Any

from mcp import types

from mcp_tools._context import MCPContext

TOOL = types.Tool(
    name="lazyown_get_beacons",
    description="Query the LazyOwn C2 server for currently connected beacons/implants.",
    inputSchema={"type": "object", "properties": {}},
)


async def handle(arguments: dict[str, Any], tool_name: str, ctx: MCPContext) -> list:
    """Query the C2 for connected clients and return the JSON list."""
    result = await asyncio.get_event_loop().run_in_executor(None, lambda: ctx.c2_request("/get_connected_clients"))
    return ctx.text(tool_name, json.dumps(result, indent=2))
