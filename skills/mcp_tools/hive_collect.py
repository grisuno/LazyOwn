"""MCP tool ``lazyown_hive_collect`` (migrated from the call_tool dispatch chain)."""

from __future__ import annotations

from typing import Any

from mcp import types

from mcp_tools._context import MCPContext

TOOL = types.Tool(
    name="lazyown_hive_collect",
    description=(
        "Wait for a set of drones to finish and return the Queen's synthesized summary. "
        "drone_ids_csv: comma-separated drone IDs returned by lazyown_hive_spawn."
    ),
    inputSchema={
        "type": "object",
        "properties": {
            "drone_ids_csv": {"type": "string", "description": "Comma-separated drone IDs"},
            "goal": {"type": "string", "description": "Original goal (for synthesis context)", "default": ""},
        },
        "required": ["drone_ids_csv"],
    },
)


def handle(arguments: dict[str, Any], tool_name: str, ctx: MCPContext) -> list:
    """Handle the lazyown_hive_collect MCP tool."""
    try:
        from hive_mind import mcp_hive_collect as _hive_collect
    except Exception:
        return ctx.text(tool_name, "[hive] hive_mind.py not importable")
    try:
        return ctx.text(
            tool_name,
            _hive_collect(
                drone_ids_csv=arguments.get("drone_ids_csv", ""),
                goal=arguments.get("goal", ""),
            ),
        )
    except Exception as exc:
        return ctx.text(tool_name, f"[hive_collect error] {exc}")
