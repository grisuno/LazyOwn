"""MCP tool ``lazyown_lazy_mention``: search mention sources, paginated."""

from __future__ import annotations

import asyncio
import json
from typing import Any

from mcp import types

from mcp_tools._context import MCPContext

TOOL = types.Tool(
    name="lazyown_lazy_mention",
    description="Search @ mention candidates (intents, facts, findings, assets) with cursor pagination.",
    inputSchema={
        "type": "object",
        "properties": {
            "kind": {"type": "string"},
            "query": {"type": "string"},
            "cursor": {"type": "string"},
        },
        "required": [],
    },
)


async def handle(arguments: dict[str, Any], tool_name: str, ctx: MCPContext) -> list:
    """Return one page of mention items plus the next cursor as JSON."""
    try:
        from dataclasses import asdict as _asdict

        from modules.lazy_mentions import search_mentions_page as _mentions

        page = await asyncio.get_event_loop().run_in_executor(
            None,
            lambda: _mentions(
                str(arguments.get("kind", "")),
                str(arguments.get("query", "")),
                str(arguments.get("cursor", "")),
            ),
        )
        return ctx.text(
            tool_name,
            json.dumps(
                {
                    "items": [_asdict(item) for item in page.items],
                    "next_cursor": page.next_cursor,
                },
                indent=2,
                ensure_ascii=False,
                default=str,
            ),
        )
    except Exception as exc:
        return ctx.text(tool_name, json.dumps({"error": str(exc)}, indent=2))
