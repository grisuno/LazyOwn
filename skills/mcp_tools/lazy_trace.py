"""MCP tool ``lazyown_lazy_trace``: search a task activity log."""

from __future__ import annotations

import asyncio
import json
from typing import Any

from mcp import types

from mcp_tools._context import MCPContext

_MAX_HITS = 50

TOOL = types.Tool(
    name="lazyown_lazy_trace",
    description="Search worker traces of a task by keyword and return matching steps with intent attribution.",
    inputSchema={
        "type": "object",
        "properties": {
            "task_id": {"type": "string"},
            "query": {"type": "string"},
        },
        "required": ["task_id", "query"],
    },
)


async def handle(arguments: dict[str, Any], tool_name: str, ctx: MCPContext) -> list:
    """Return up to the hit cap of matching activity-log entries as JSON."""
    try:
        from modules.lazy_engine import ActivityLog

        log = ActivityLog(str(arguments.get("task_id", "")))
        hits = await asyncio.get_event_loop().run_in_executor(
            None,
            lambda: log.search_all(str(arguments.get("query", ""))),
        )
        return ctx.text(
            tool_name,
            json.dumps(
                {"hits": hits[:_MAX_HITS], "total": len(hits)},
                indent=2,
                ensure_ascii=False,
                default=str,
            ),
        )
    except Exception as exc:
        return ctx.text(tool_name, json.dumps({"error": str(exc)}, indent=2))
