"""MCP tool ``lazyown_swan_route`` (migrated from the call_tool dispatch chain)."""

from __future__ import annotations

import sys
from typing import Any

from mcp import types
from mcp_tools._context import MCPContext

TOOL = types.Tool(
    name="lazyown_swan_route",
    description=(
        "Preview expert routing for a task without executing it. "
        "Returns the top-4 candidates with base_weight, adjusted_weight (after RL performance bonus), "
        "backend, model, and estimated latency. "
        "Use this to understand and explain routing decisions before committing resources."
    ),
    inputSchema={
        "type": "object",
        "properties": {
            "task_type": {
                "type": "string",
                "description": "Category of the task (recon, exploit, privesc, lateral, cred, analyze, report).",
            },
            "goal": {
                "type": "string",
                "description": "Optional goal text for context (first 100 chars used).",
                "default": "",
            },
        },
        "required": ["task_type"],
    },
)


def handle(arguments: dict[str, Any], tool_name: str, ctx: MCPContext) -> list:
    """Handle the lazyown_swan_route MCP tool."""
    task_type = arguments.get("task_type", "analyze")
    goal = arguments.get("goal", "")
    try:
        sys.path.insert(0, str(ctx.lazyown_dir / "skills"))
        from swan_agent import mcp_swan_route as _swan_route

        return ctx.text(tool_name, _swan_route(task_type, goal))
    except Exception as exc:
        return ctx.text(tool_name, f"[swan_route error] {exc}")
