"""MCP tool ``lazyown_add_rule`` (migrated from the call_tool dispatch chain)."""

from __future__ import annotations

import asyncio
from typing import Any

from mcp import types

from mcp_tools._context import MCPContext

TOOL = types.Tool(
    name="lazyown_add_rule",
    description=(
        "Add or update an event detection rule. Rules define what LazyOwn command patterns "
        "trigger which events. Use this to teach the event engine to detect new conditions. "
        "Trigger fields: 'command' (exact), 'command_contains', 'args_contains', 'output_contains'."
    ),
    inputSchema={
        "type": "object",
        "properties": {
            "id": {"type": "string", "description": "Unique rule ID (snake_case)."},
            "description": {"type": "string", "description": "What this rule detects."},
            "trigger": {
                "type": "object",
                "description": "Match conditions. Keys: command, command_contains, args_contains, output_contains.",
            },
            "event_type": {"type": "string", "description": "Event type emitted (e.g. CREDS_FOUND)."},
            "severity": {
                "type": "string",
                "enum": ["info", "high", "critical"],
                "default": "info",
            },
            "suggest": {"type": "string", "description": "Action suggestion shown in the event."},
        },
        "required": ["id", "description", "trigger", "event_type"],
    },
)


async def handle(arguments: dict[str, Any], tool_name: str, ctx: MCPContext) -> list:
    """Handle the lazyown_add_rule MCP tool."""
    try:
        from event_engine import add_rule
        from event_engine import load_rules
    except Exception:
        return ctx.text(tool_name, "Event engine not available.")
    rule = {
        "id": arguments["id"],
        "description": arguments["description"],
        "trigger": arguments["trigger"],
        "event_type": arguments["event_type"],
        "severity": arguments.get("severity", "info"),
        "suggest": arguments.get("suggest", ""),
    }
    result = await asyncio.get_event_loop().run_in_executor(None, lambda: add_rule(rule))
    return ctx.text(tool_name, f"Rule '{rule['id']}' {result}. Total rules: {len(load_rules())}")
