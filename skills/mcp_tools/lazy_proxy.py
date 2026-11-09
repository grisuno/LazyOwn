"""MCP tool ``lazyown_lazy_proxy``: control the lazy-engine proxy."""

from __future__ import annotations

import asyncio
import json
from typing import Any

from mcp import types

from mcp_tools._context import MCPContext

_DEFAULT_PROXY_PORT = 8899

TOOL = types.Tool(
    name="lazyown_lazy_proxy",
    description=(
        "Control the loop recorder proxy: start/stop HTTP(S) capture "
        "with a local CA, report status, read the trust env. Once "
        "started, routed tool exchanges are stored and auto-ingested "
        "into the task traffic log for findings evidence."
    ),
    inputSchema={
        "type": "object",
        "properties": {
            "action": {
                "type": "string",
                "enum": ["start", "stop", "status", "env"],
                "default": "status",
            },
            "port": {"type": "integer", "default": _DEFAULT_PROXY_PORT},
            "task_id": {"type": "string"},
        },
        "required": [],
    },
)


async def handle(arguments: dict[str, Any], tool_name: str, ctx: MCPContext) -> list:
    """Dispatch the proxy action and return its status as JSON."""
    try:
        from modules.lazy_engine import LazyEngine

        engine = LazyEngine()
        action = str(arguments.get("action", "status") or "status").lower()
        if action == "start":
            status = await asyncio.get_event_loop().run_in_executor(
                None,
                lambda: engine.proxy_start(
                    port=int(arguments.get("port", 0) or 0), task_id=str(arguments.get("task_id", ""))
                ),
            )
        elif action == "stop":
            status = await asyncio.get_event_loop().run_in_executor(None, engine.proxy_stop)
        elif action == "env":
            status = {"env": engine.proxy_env()}
        else:
            status = engine.proxy_status()
        return ctx.text(tool_name, json.dumps(status, indent=2, ensure_ascii=False, default=str))
    except Exception as exc:
        return ctx.text(tool_name, json.dumps({"error": str(exc)}, indent=2))
