"""MCP tool ``lazyown_lazy_sync``: sync all lazy-bridge sources."""

from __future__ import annotations

import json
from typing import Any

from mcp import types

from mcp_tools._context import MCPContext

TOOL = types.Tool(
    name="lazyown_lazy_sync",
    description="Run bidirectional lazy sync into the world model and objectives queue.",
    inputSchema={"type": "object", "properties": {}, "required": []},
)


async def handle(arguments: dict[str, Any], tool_name: str, ctx: MCPContext) -> list:
    """Run a full lazy-bridge sync and return its result as JSON."""
    try:
        from modules.lazy_bridge import sync_all as _sync

        return ctx.text(tool_name, json.dumps(_sync(), indent=2, ensure_ascii=False, default=str))
    except Exception as exc:
        return ctx.text(tool_name, json.dumps({"error": str(exc)}, indent=2))
