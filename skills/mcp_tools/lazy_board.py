"""MCP tool ``lazyown_lazy_board``: paginated broadcast board view."""

from __future__ import annotations

import asyncio
import json
from typing import Any

from mcp import types

from mcp_tools._context import MCPContext

_DEFAULT_PER_PAGE = 20

TOOL = types.Tool(
    name="lazyown_lazy_board",
    description=(
        "Read the loop exploration timeline for a task: node rows with "
        "upstream/downstream neighbours and anchored assets."
    ),
    inputSchema={
        "type": "object",
        "properties": {
            "task_id": {"type": "string"},
            "kind": {"type": "string", "description": "Node kind filter (intent, fact, finding, goal...)"},
            "query": {"type": "string", "description": "Keyword or #id filter"},
            "page": {"type": "integer", "default": 1},
            "per_page": {"type": "integer", "default": _DEFAULT_PER_PAGE},
            "order": {"type": "string", "enum": ["asc", "desc"], "default": "desc"},
        },
        "required": ["task_id"],
    },
)


async def handle(arguments: dict[str, Any], tool_name: str, ctx: MCPContext) -> list:
    """Return one page of the broadcast board as JSON."""
    try:
        from modules.lazy_engine import LazyEngine

        engine = LazyEngine()
        kind = str(arguments.get("kind", "")).strip()
        page = await asyncio.get_event_loop().run_in_executor(
            None,
            lambda: engine.broadcast(
                str(arguments.get("task_id", "")),
                kinds=[kind] if kind else None,
                query=str(arguments.get("query", "")),
                order=str(arguments.get("order", "desc")),
                page=int(arguments.get("page", 1) or 1),
                per_page=int(arguments.get("per_page", _DEFAULT_PER_PAGE) or _DEFAULT_PER_PAGE),
            ),
        )
        return ctx.text(tool_name, json.dumps(page, indent=2, ensure_ascii=False, default=str))
    except Exception as exc:
        return ctx.text(tool_name, json.dumps({"error": str(exc)}, indent=2))
