"""MCP tool ``lazyown_c2_status``: check C2 reachability and dashboard data."""

from __future__ import annotations

import asyncio
import json
from typing import Any

from mcp import types

from mcp_tools._context import MCPContext

TOOL = types.Tool(
    name="lazyown_c2_status",
    description="Check if the LazyOwn C2 server is reachable and return dashboard data.",
    inputSchema={"type": "object", "properties": {}},
)


async def handle(arguments: dict[str, Any], tool_name: str, ctx: MCPContext) -> list:
    """Query the C2 dashboard endpoint and return its JSON."""
    result = await asyncio.get_event_loop().run_in_executor(None, lambda: ctx.c2_request("/api/data"))
    return ctx.text(tool_name, json.dumps(result, indent=2))
