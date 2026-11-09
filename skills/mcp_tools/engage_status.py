"""MCP tool ``lazyown_engage_status`` (migrated from the call_tool dispatch chain)."""

from __future__ import annotations

from typing import Any

from mcp import types
from mcp_tools._context import MCPContext

TOOL = types.Tool(
    name="lazyown_engage_status",
    description=(
        "Read the tail of sessions/engagement.log and the current list "
        "of approval requests awaiting an operator decision. Use to "
        "monitor a running engagement started with lazyown_engage_target."
    ),
    inputSchema={
        "type": "object",
        "properties": {
            "last_n": {
                "type": "integer",
                "description": "Number of log lines to return.",
                "default": 20,
            },
        },
        "required": [],
    },
)


def handle(arguments: dict[str, Any], tool_name: str, ctx: MCPContext) -> list:
    """Handle the lazyown_engage_status MCP tool."""
    try:
        from autonomous_daemon import mcp_engage_status as _engage_status_call
    except Exception as exc:
        return ctx.text(tool_name, f"[engage_status error] autonomous_daemon import failed: {exc}")
    try:
        return ctx.text(tool_name, _engage_status_call(last_n=int(arguments.get("last_n", 20))))
    except Exception as exc:
        return ctx.text(tool_name, f"[engage_status error] {exc}")
