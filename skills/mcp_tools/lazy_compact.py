"""MCP tool ``lazyown_lazy_compact``: manage cold-compaction digests."""

from __future__ import annotations

import asyncio
import json
from typing import Any

from mcp import types

from mcp_tools._context import MCPContext

_DEFAULT_UNFOLDED_LIMIT = 60

TOOL = types.Tool(
    name="lazyown_lazy_compact",
    description="Cold-graph compaction control: overview, planner-round maintain, unfolded cold nodes, expand a digest.",
    inputSchema={
        "type": "object",
        "properties": {
            "task_id": {"type": "string"},
            "action": {
                "type": "string",
                "enum": ["overview", "maintain", "unfolded", "expand"],
                "default": "overview",
            },
            "limit": {"type": "integer", "default": _DEFAULT_UNFOLDED_LIMIT},
            "digest_id": {"type": "integer"},
        },
        "required": ["task_id"],
    },
)


async def handle(arguments: dict[str, Any], tool_name: str, ctx: MCPContext) -> list:
    """Dispatch the compaction action and return its result as JSON."""
    try:
        from modules.lazy_loop import ActivityLog as _Activity
        from modules.lazy_loop import ColdCompactor as _Compactor
        from modules.lazy_loop import ExplorationGraph as _Graph

        task_id = str(arguments.get("task_id", ""))
        action = str(arguments.get("action", "overview")).lower()
        graph = _Graph(task_id)
        compactor = _Compactor(graph, _Activity(task_id))
        if action == "maintain":
            out = await asyncio.get_event_loop().run_in_executor(None, compactor.on_planner_round)
        elif action == "unfolded":
            out = compactor.unfolded(int(arguments.get("limit", _DEFAULT_UNFOLDED_LIMIT) or _DEFAULT_UNFOLDED_LIMIT))
        elif action == "expand":
            out = {"revived": compactor.expand(int(arguments.get("digest_id", 0) or 0))}
        else:
            out = compactor.digest_overview()
        return ctx.text(tool_name, json.dumps(out, indent=2, ensure_ascii=False, default=str))
    except Exception as exc:
        return ctx.text(tool_name, json.dumps({"error": str(exc)}, indent=2))
