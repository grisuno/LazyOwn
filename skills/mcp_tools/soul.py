"""MCP tool ``lazyown_soul`` (migrated from the call_tool dispatch chain)."""

from __future__ import annotations

import asyncio
from typing import Any

from mcp import types

from mcp_tools._context import MCPContext

TOOL = types.Tool(
    name="lazyown_soul",
    description=(
        "Read or update the agent soul (sessions/soul.md). "
        "The soul defines: campaign objective, priority order, hard stops, "
        "guardrails, and current focus. "
        "Reading the soul before reasoning gives the frontier model its "
        "operating mandate. Writing it lets the operator change the campaign "
        "objective or add constraints mid-operation."
    ),
    inputSchema={
        "type": "object",
        "properties": {
            "action": {
                "type": "string",
                "description": "'read' to get current soul, 'write' to replace it.",
                "enum": ["read", "write"],
                "default": "read",
            },
            "content": {
                "type": "string",
                "description": "New soul content (only required when action='write').",
                "default": "",
            },
        },
        "required": [],
    },
)


async def handle(arguments: dict[str, Any], tool_name: str, ctx: MCPContext) -> list:
    """Handle the lazyown_soul MCP tool."""
    try:
        from lazyown_objective import read_soul as _read_soul
        from lazyown_objective import write_soul as _write_soul
    except Exception:
        return ctx.text(tool_name, "Objective store unavailable.")
    action = arguments.get("action", "read")
    if action == "write":
        content = arguments.get("content", "")
        if not content.strip():
            return ctx.text(tool_name, "content must not be empty when action='write'.")
        await asyncio.get_event_loop().run_in_executor(None, lambda: _write_soul(content))
        return ctx.text(tool_name, "soul.md updated.")
    else:
        soul = await asyncio.get_event_loop().run_in_executor(None, _read_soul)
        return ctx.text(tool_name, soul)
