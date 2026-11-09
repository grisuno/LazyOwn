"""MCP tool ``lazyown_hive_forget`` (migrated from the call_tool dispatch chain)."""

from __future__ import annotations

from typing import Any

from mcp import types

from mcp_tools._context import MCPContext

TOOL = types.Tool(
    name="lazyown_hive_forget",
    description="Prune hive episodic memory. Remove entries older than N hours, optionally filtered by topic.",
    inputSchema={
        "type": "object",
        "properties": {
            "older_than_hours": {"type": "number", "default": 24.0},
            "topic": {"type": "string", "default": ""},
        },
        "required": [],
    },
)


def handle(arguments: dict[str, Any], tool_name: str, ctx: MCPContext) -> list:
    """Handle the lazyown_hive_forget MCP tool."""
    try:
        from hive_mind import mcp_hive_forget as _hive_forget
    except Exception:
        return ctx.text(tool_name, "[hive] hive_mind.py not importable")
    try:
        return ctx.text(
            tool_name,
            _hive_forget(
                older_than_hours=float(arguments.get("older_than_hours", 24.0)),
                topic=arguments.get("topic", ""),
            ),
        )
    except Exception as exc:
        return ctx.text(tool_name, f"[hive_forget error] {exc}")
