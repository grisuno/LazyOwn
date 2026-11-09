"""MCP tool ``lazyown_hive_plan`` (migrated from the call_tool dispatch chain)."""

from __future__ import annotations

from typing import Any

from mcp import types

from mcp_tools._context import MCPContext

TOOL = types.Tool(
    name="lazyown_hive_plan",
    description=(
        "Queen generates a task decomposition plan for a goal WITHOUT spawning drones. "
        "Shows the role → sub-goal breakdown that would be dispatched."
    ),
    inputSchema={
        "type": "object",
        "properties": {
            "goal": {"type": "string"},
            "n_drones": {"type": "integer", "default": 0},
        },
        "required": ["goal"],
    },
)


def handle(arguments: dict[str, Any], tool_name: str, ctx: MCPContext) -> list:
    """Handle the lazyown_hive_plan MCP tool."""
    try:
        from hive_mind import mcp_hive_plan as _hive_plan
    except Exception:
        return ctx.text(tool_name, "[hive] hive_mind.py not importable")
    try:
        return ctx.text(
            tool_name,
            _hive_plan(
                goal=arguments.get("goal", ""),
                n_drones=int(arguments.get("n_drones", 0)),
            ),
        )
    except Exception as exc:
        return ctx.text(tool_name, f"[hive_plan error] {exc}")
