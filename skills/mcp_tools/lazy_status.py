"""MCP tool ``lazyown_lazy_status``: report lazy-bridge status."""

from __future__ import annotations

import json
from typing import Any

from mcp import types

from mcp_tools._context import MCPContext

TOOL = types.Tool(
    name="lazyown_lazy_status",
    description="Loop storage status: task count, assets, per-task graph/activity/traffic sizes and last sync.",
    inputSchema={"type": "object", "properties": {}, "required": []},
)


async def handle(arguments: dict[str, Any], tool_name: str, ctx: MCPContext) -> list:
    """Return the lazy-bridge status snapshot as JSON."""
    try:
        from modules.lazy_bridge import bridge_status as _status

        return ctx.text(tool_name, json.dumps(_status(), indent=2, ensure_ascii=False, default=str))
    except Exception as exc:
        return ctx.text(tool_name, json.dumps({"error": str(exc)}, indent=2))
