"""MCP tool ``lazyown_pipeline_list`` (migrated from the call_tool dispatch chain)."""

from __future__ import annotations

import sys
from typing import Any

from mcp import types
from mcp_tools._context import MCPContext

TOOL = types.Tool(
    name="lazyown_pipeline_list",
    description="List every available pipeline name under pipelines/.",
    inputSchema={"type": "object", "properties": {}, "required": []},
)


def handle(arguments: dict[str, Any], tool_name: str, ctx: MCPContext) -> list:
    """Handle the lazyown_pipeline_list MCP tool."""
    try:
        sys.path.insert(0, str(ctx.lazyown_dir / "modules"))
        from pipeline_engine import mcp_pipeline_list as _pl_list
    except Exception as exc:
        return ctx.text(tool_name, f"[pipeline_list error] pipeline_engine import failed: {exc}")
    try:
        return ctx.text(tool_name, _pl_list())
    except Exception as exc:
        return ctx.text(tool_name, f"[pipeline_list error] {exc}")
