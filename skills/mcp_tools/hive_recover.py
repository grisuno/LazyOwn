"""MCP tool ``lazyown_hive_recover`` (migrated from the call_tool dispatch chain)."""

from __future__ import annotations

from typing import Any

from mcp import types

from mcp_tools._context import MCPContext

TOOL = types.Tool(
    name="lazyown_hive_recover",
    description=(
        "Re-queue all hive drones that were interrupted by a previous process crash or "
        "restart. On startup the hive marks any in-flight (queued/running) drones as "
        "'interrupted'. Call this tool to re-spawn them so no work is lost after a "
        "daemon restart or context loss."
    ),
    inputSchema={
        "type": "object",
        "properties": {
            "backend": {"type": "string", "default": "groq"},
            "api_key": {"type": "string", "default": ""},
            "max_iterations": {"type": "integer", "default": 10},
        },
        "required": [],
    },
)


def handle(arguments: dict[str, Any], tool_name: str, ctx: MCPContext) -> list:
    """Handle the lazyown_hive_recover MCP tool."""
    try:
        from hive_mind import mcp_hive_recover as _hive_recover
    except Exception:
        return ctx.text(tool_name, "[hive] hive_mind.py not importable")
    try:
        return ctx.text(
            tool_name,
            _hive_recover(
                backend=arguments.get("backend", "groq"),
                api_key=arguments.get("api_key", ""),
                max_iterations=int(arguments.get("max_iterations", 10)),
            ),
        )
    except Exception as exc:
        return ctx.text(tool_name, f"[hive_recover error] {exc}")
