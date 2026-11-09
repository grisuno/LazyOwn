"""MCP tool ``lazyown_lazy_delete``: soft/hard delete a task intent."""

from __future__ import annotations

import asyncio
import json
from typing import Any

from mcp import types

from mcp_tools._context import MCPContext

TOOL = types.Tool(
    name="lazyown_lazy_delete",
    description=(
        "Delete a loop intent: soft keeps lineage and outputs, hard cascades "
        "exclusive descendants. Hard requires confirm."
    ),
    inputSchema={
        "type": "object",
        "properties": {
            "task_id": {"type": "string"},
            "intent_id": {"type": "integer"},
            "reason": {"type": "string"},
            "mode": {"type": "string", "enum": ["soft", "hard"], "default": "soft"},
            "confirm": {"type": "string", "description": "Echo the intent id to confirm a hard delete"},
        },
        "required": ["task_id", "intent_id", "reason"],
    },
)


async def handle(arguments: dict[str, Any], tool_name: str, ctx: MCPContext) -> list:
    """Delete or preview-delete an intent and return the result as JSON."""
    try:
        from modules.lazy_loop import LazyLoopEngine as _Engine

        engine = _Engine()
        task_id = str(arguments.get("task_id", ""))
        intent_id = int(arguments.get("intent_id", 0) or 0)
        reason = str(arguments.get("reason", ""))
        mode = str(arguments.get("mode", "soft")).lower()
        if mode not in ("soft", "hard"):
            mode = "soft"
        if mode == "hard" and not str(arguments.get("confirm", "")):
            preview = await asyncio.get_event_loop().run_in_executor(
                None, lambda: engine.preview_delete_intent(task_id, intent_id)
            )
            return ctx.text(tool_name, json.dumps({"preview": preview}, indent=2, ensure_ascii=False, default=str))
        result = await asyncio.get_event_loop().run_in_executor(
            None, lambda: engine.delete_intent(task_id, intent_id, mode=mode, reason=reason)
        )
        return ctx.text(tool_name, json.dumps(result, indent=2, ensure_ascii=False, default=str))
    except Exception as exc:
        return ctx.text(tool_name, json.dumps({"error": str(exc)}, indent=2))
