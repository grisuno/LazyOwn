"""MCP tool ``lazyown_ack_event``: mark an event as processed."""

from __future__ import annotations

import asyncio
from typing import Any

from mcp import types

from mcp_tools._context import MCPContext

TOOL = types.Tool(
    name="lazyown_ack_event",
    description="Mark a specific event as processed so it won't appear in future pending polls.",
    inputSchema={
        "type": "object",
        "properties": {
            "event_id": {
                "type": "string",
                "description": "The 8-char event ID returned by lazyown_poll_events.",
            }
        },
        "required": ["event_id"],
    },
)


async def handle(arguments: dict[str, Any], tool_name: str, ctx: MCPContext) -> list:
    """Acknowledge one event by id, reporting whether it was found."""
    try:
        from event_engine import ack_event
    except Exception:
        return ctx.text(tool_name, "Event engine not available.")
    event_id = arguments["event_id"]
    found = await asyncio.get_event_loop().run_in_executor(None, lambda: ack_event(event_id))
    return ctx.text(
        tool_name,
        f"Event {event_id} marked as processed." if found else f"Event {event_id} not found.",
    )
