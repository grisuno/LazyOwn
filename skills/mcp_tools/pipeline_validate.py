"""MCP tool ``lazyown_pipeline_validate`` (migrated from the call_tool dispatch chain)."""

from __future__ import annotations

import sys
from typing import Any

from mcp import types
from mcp_tools._context import MCPContext

TOOL = types.Tool(
    name="lazyown_pipeline_validate",
    description=(
        "Parse and validate a pipeline's YAML schema without "
        "executing it. Returns the resolved step list with index, "
        "command/pipeline, condition and on_failure metadata."
    ),
    inputSchema={
        "type": "object",
        "properties": {
            "name": {"type": "string", "description": "Pipeline name."},
        },
        "required": ["name"],
    },
)


def handle(arguments: dict[str, Any], tool_name: str, ctx: MCPContext) -> list:
    """Handle the lazyown_pipeline_validate MCP tool."""
    try:
        sys.path.insert(0, str(ctx.lazyown_dir / "modules"))
        from pipeline_engine import mcp_pipeline_validate as _pl_validate
    except Exception as exc:
        return ctx.text(tool_name, f"[pipeline_validate error] pipeline_engine import failed: {exc}")
    try:
        pipeline_name = str(arguments.get("name", "")).strip()
        if not pipeline_name:
            return ctx.text(tool_name, "[pipeline_validate error] name is required")
        return ctx.text(tool_name, _pl_validate(pipeline_name))
    except Exception as exc:
        return ctx.text(tool_name, f"[pipeline_validate error] {exc}")
