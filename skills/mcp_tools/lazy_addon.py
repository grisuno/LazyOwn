"""MCP tool ``lazyown_lazy_addon``: list or match lazyaddon triggers."""

from __future__ import annotations

import asyncio
import json
from typing import Any

from mcp import types

from mcp_tools._context import MCPContext

TOOL = types.Tool(
    name="lazyown_lazy_addon",
    description="List lazyaddons with their service triggers, or rank addons matching one service value.",
    inputSchema={
        "type": "object",
        "properties": {
            "action": {"type": "string", "enum": ["matches", "list"], "default": "matches"},
            "service": {"type": "string"},
        },
        "required": [],
    },
)


async def handle(arguments: dict[str, Any], tool_name: str, ctx: MCPContext) -> list:
    """List addon triggers or return matches for a service as JSON."""
    try:
        from modules.auto_registry import addon_hits_for as _hits
        from modules.auto_registry import iter_addon_triggers as _triggers

        action = str(arguments.get("action", "matches")).lower()
        if action == "list":
            entries = await asyncio.get_event_loop().run_in_executor(None, _triggers)
            return ctx.text(
                tool_name,
                json.dumps(
                    [{"name": name, "triggers": trig} for name, trig in entries],
                    indent=2,
                    ensure_ascii=False,
                    default=str,
                ),
            )
        service = str(arguments.get("service", ""))
        hits = await asyncio.get_event_loop().run_in_executor(None, lambda: _hits(service))
        return ctx.text(
            tool_name,
            json.dumps(
                {"service": service, "hits": [{"name": name, "source": src} for name, src in hits]},
                indent=2,
                ensure_ascii=False,
                default=str,
            ),
        )
    except Exception as exc:
        return ctx.text(tool_name, json.dumps({"error": str(exc)}, indent=2))
