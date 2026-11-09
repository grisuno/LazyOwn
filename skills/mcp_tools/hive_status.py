"""MCP tool ``lazyown_hive_status`` (migrated from the call_tool dispatch chain)."""

from __future__ import annotations

from typing import Any

from mcp import types

from mcp_tools._context import MCPContext

TOOL = types.Tool(
    name="lazyown_hive_status",
    description=(
        "Full hive-mind status: all active drones with role/status/duration, "
        "ChromaDB vector count, episodic memory events, queen mailbox depth."
    ),
    inputSchema={"type": "object", "properties": {}, "required": []},
)


def handle(arguments: dict[str, Any], tool_name: str, ctx: MCPContext) -> list:
    """Handle the lazyown_hive_status MCP tool."""
    try:
        from hive_mind import mcp_hive_status as _hive_status
    except Exception:
        return ctx.text(tool_name, "[hive] hive_mind.py not importable")
    try:
        return ctx.text(tool_name, _hive_status())
    except Exception as exc:
        return ctx.text(tool_name, f"[hive_status error] {exc}")
