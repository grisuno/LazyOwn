"""MCP tool ``lazyown_hive_result`` (migrated from the call_tool dispatch chain)."""

from __future__ import annotations

from typing import Any

from mcp import types

from mcp_tools._context import MCPContext

TOOL = types.Tool(
    name="lazyown_hive_result",
    description="Get the result of a specific hive drone by drone_id.",
    inputSchema={
        "type": "object",
        "properties": {"drone_id": {"type": "string"}},
        "required": ["drone_id"],
    },
)


def handle(arguments: dict[str, Any], tool_name: str, ctx: MCPContext) -> list:
    """Handle the lazyown_hive_result MCP tool."""
    try:
        from hive_mind import mcp_hive_result as _hive_result
    except Exception:
        return ctx.text(tool_name, "[hive] hive_mind.py not importable")
    try:
        return ctx.text(tool_name, _hive_result(arguments.get("drone_id", "")))
    except Exception as exc:
        return ctx.text(tool_name, f"[hive_result error] {exc}")
