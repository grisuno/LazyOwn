"""MCP tool ``lazyown_pivot_status``: view pivot routes and suggestions."""

from __future__ import annotations

import json
from typing import Any

from mcp import types

from mcp_tools._context import MCPContext

TOOL = types.Tool(
    name="lazyown_pivot_status",
    description=(
        "View active pivot routes, generate proxychains config, and "
        "get suggested next pivot targets based on discovered subnets "
        "from compromised hosts."
    ),
    inputSchema={
        "type": "object",
        "properties": {},
        "required": [],
    },
)


async def handle(arguments: dict[str, Any], tool_name: str, ctx: MCPContext) -> list:
    """Return active routes, proxychains config and next-pivot suggestion."""
    try:
        from modules.auto_pivot import AutoPivotEngine

        engine = AutoPivotEngine(ctx.load_payload())
        result = {
            "active_routes": engine.get_active_routes(),
            "proxychains_config": engine.generate_proxychains_config(),
            "suggested_next_pivot": engine.suggest_next_pivot(),
        }
        return ctx.text(tool_name, json.dumps(result, indent=2, ensure_ascii=False))
    except Exception as exc:
        return ctx.text(tool_name, json.dumps({"error": str(exc)}, indent=2))
