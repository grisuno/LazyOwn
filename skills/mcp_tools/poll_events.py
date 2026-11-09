"""MCP tool ``lazyown_poll_events`` (migrated from the call_tool dispatch chain)."""

from __future__ import annotations

import asyncio
from typing import Any

from mcp import types

from mcp_tools._context import MCPContext

TOOL = types.Tool(
    name="lazyown_poll_events",
    description=(
        "Read events emitted by the LazyOwn Event Engine. "
        "Events are generated automatically when LazyOwn commands match detection rules "
        "(e.g. new beacon, port found, credentials captured, vuln scan complete). "
        "Poll this regularly to act proactively without waiting for user input."
    ),
    inputSchema={
        "type": "object",
        "properties": {
            "limit": {
                "type": "integer",
                "description": "Max events to return (default 20).",
                "default": 20,
            },
            "status": {
                "type": "string",
                "description": "Filter by status: 'pending' (default), 'processed', or 'all'.",
                "enum": ["pending", "processed", "all"],
                "default": "pending",
            },
        },
    },
)


async def handle(arguments: dict[str, Any], tool_name: str, ctx: MCPContext) -> list:
    """Handle the lazyown_poll_events MCP tool."""
    try:
        from event_engine import read_events
    except Exception:
        return ctx.text(tool_name, "Event engine not available — check modules/event_engine.py")
    limit = int(arguments.get("limit", 20))
    status = arguments.get("status", "pending")
    events = await asyncio.get_event_loop().run_in_executor(None, lambda: read_events(limit=limit, status=status))
    if not events:
        return ctx.text(tool_name, f"No {status} events.")
    lines = [f"{len(events)} {status} event(s):\n"]
    for ev in events:
        lines.append(
            f"[{ev['id']}] {ev['timestamp'][:19]}  "
            f"{'🔴' if ev['severity'] == 'critical' else '🟡' if ev['severity'] == 'high' else '🔵'} "
            f"{ev['type']}  (rule: {ev['rule_id']})\n"
            f"  command: {ev['source']['command']}  target: {ev['source']['target']}\n"
            f"  suggest: {ev['suggest']}\n"
        )
    return ctx.text(tool_name, "\n".join(lines))
