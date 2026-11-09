"""MCP tool ``lazyown_lazy_workspace``: list/read/write workspace files."""

from __future__ import annotations

import asyncio
import json
from typing import Any

from mcp import types

from mcp_tools._context import MCPContext

TOOL = types.Tool(
    name="lazyown_lazy_workspace",
    description=(
        "Confined workspace file browser: list/read/write files under sessions/workspace. Paths cannot escape the root."
    ),
    inputSchema={
        "type": "object",
        "properties": {
            "action": {"type": "string", "enum": ["list", "read", "write"], "default": "list"},
            "path": {"type": "string"},
            "content": {"type": "string"},
        },
        "required": [],
    },
)


async def handle(arguments: dict[str, Any], tool_name: str, ctx: MCPContext) -> list:
    """Dispatch the workspace action and return its result as JSON."""
    try:
        from modules import workspace as _ws

        action = str(arguments.get("action", "list") or "list").lower()
        path = str(arguments.get("path", "") or "")
        if action == "read":
            content = await asyncio.get_event_loop().run_in_executor(None, lambda: _ws.read_text(path))
            return ctx.text(tool_name, json.dumps({"path": path, "content": content}, indent=2, ensure_ascii=False))
        if action == "write":
            written = await asyncio.get_event_loop().run_in_executor(
                None, lambda: _ws.write_text(path, str(arguments.get("content", "")))
            )
            return ctx.text(tool_name, json.dumps({"path": path, "written": written}, indent=2))
        entries = await asyncio.get_event_loop().run_in_executor(None, lambda: _ws.list_entries(path))
        return ctx.text(tool_name, json.dumps({"path": path, "entries": entries}, indent=2, ensure_ascii=False))
    except Exception as exc:
        return ctx.text(tool_name, json.dumps({"error": str(exc)}, indent=2))
