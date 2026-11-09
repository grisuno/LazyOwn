"""MCP tool ``lazyown_pipeline_status`` (migrated from the call_tool dispatch chain)."""

from __future__ import annotations

import sys
from typing import Any

from mcp import types
from mcp_tools._context import MCPContext

TOOL = types.Tool(
    name="lazyown_pipeline_status",
    description=("Return the N most recent pipeline runs and their summary.json contents from sessions/pipelines/."),
    inputSchema={
        "type": "object",
        "properties": {
            "last_n": {
                "type": "integer",
                "description": "Maximum number of runs to return.",
                "default": 5,
            },
        },
        "required": [],
    },
)


def handle(arguments: dict[str, Any], tool_name: str, ctx: MCPContext) -> list:
    """Handle the lazyown_pipeline_status MCP tool."""
    try:
        sys.path.insert(0, str(ctx.lazyown_dir / "modules"))
        from pipeline_engine import mcp_pipeline_status as _pl_status
    except Exception as exc:
        return ctx.text(tool_name, f"[pipeline_status error] pipeline_engine import failed: {exc}")
    try:
        return ctx.text(tool_name, _pl_status(last_n=int(arguments.get("last_n", 5))))
    except Exception as exc:
        return ctx.text(tool_name, f"[pipeline_status error] {exc}")
