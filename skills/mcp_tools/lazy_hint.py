"""MCP tool ``lazyown_lazy_hint``: add a hint node to a task."""

from __future__ import annotations

import json
from typing import Any

from mcp import types

from mcp_tools._context import MCPContext

TOOL = types.Tool(
    name="lazyown_lazy_hint",
    description="Inject a human steering hint that fires the next planner round and forces a probe on it.",
    inputSchema={
        "type": "object",
        "properties": {
            "task_id": {"type": "string"},
            "text": {"type": "string"},
        },
        "required": ["task_id", "text"],
    },
)


async def handle(arguments: dict[str, Any], tool_name: str, ctx: MCPContext) -> list:
    """Create a hint node and return its record as JSON."""
    try:
        from modules.lazy_engine import LazyEngine

        engine = LazyEngine()
        node = engine.add_hint(str(arguments.get("task_id", "")), str(arguments.get("text", "")))
        record = {
            "node_id": node.node_id,
            "kind": node.kind,
            "state": node.state,
            "text": node.text,
            "created": node.created,
        }
        return ctx.text(tool_name, json.dumps(record, indent=2, ensure_ascii=False, default=str))
    except Exception as exc:
        return ctx.text(tool_name, json.dumps({"error": str(exc)}, indent=2))
