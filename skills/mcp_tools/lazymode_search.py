"""MCP tool ``lazyown_lazymode_search``: discover the lazymode SDK surface.

The companion of ``lazyown_lazymode_exec``. Instead of loading every tool
schema into the model context, the model queries this tool for the SDK
methods relevant to its goal, then writes one script against them. The
index is introspected live from the SDK facade, so it never drifts from
the code.
"""

from __future__ import annotations

import json
import sys
from typing import Any

from mcp import types

from mcp_tools._context import MCPContext

TOOL = types.Tool(
    name="lazyown_lazymode_search",
    description=(
        "Search the lazymode SDK surface (the programmatic API usable from "
        "lazyown_lazymode_exec). Returns matching call paths, signatures and "
        "summaries so one script can replace many tool calls."
    ),
    inputSchema={
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "Keywords describing the wanted capability.",
            },
            "limit": {
                "type": "integer",
                "description": "Maximum number of entries to return.",
            },
        },
    },
)


def handle(arguments: dict[str, Any], tool_name: str, ctx: MCPContext) -> list:
    """Return SDK surface entries matching the query as JSON text.

    Args:
        arguments: Tool arguments; ``query`` and optional ``limit``.
        tool_name: The dispatched tool name for the text envelope.
        ctx: Injected runtime helpers.

    Returns:
        A one-element ``TextContent`` list with the matching entries.
    """
    if str(ctx.lazyown_dir) not in sys.path:
        sys.path.insert(0, str(ctx.lazyown_dir))
    from sdk.lazymode import search

    query = str(arguments.get("query", ""))
    limit = int(arguments.get("limit", 10))
    entries = search(query, limit)
    return ctx.text(tool_name, json.dumps(entries, indent=2))
