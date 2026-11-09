"""MCP tool ``lazyown_pipeline_run`` (migrated from the call_tool dispatch chain)."""

from __future__ import annotations

import sys
from typing import Any

from mcp import types
from mcp_tools._context import MCPContext

TOOL = types.Tool(
    name="lazyown_pipeline_run",
    description=(
        "Run a declarative YAML pipeline from pipelines/<name>.yaml. "
        "The pipeline engine executes the steps in order, resolves "
        "{{ previous.X }} / {{ steps.<name>.X }} / {{ payload.X }} "
        "templates against the typed step context, skips steps whose "
        "'condition:' renders falsy, and persists every step plus the "
        "final summary under sessions/pipelines/<name>__<run-id>/. "
        "Set background=true to detach and poll progress with "
        "lazyown_pipeline_status."
    ),
    inputSchema={
        "type": "object",
        "properties": {
            "name": {
                "type": "string",
                "description": "Pipeline name (matches pipelines/<name>.yaml).",
            },
            "target": {
                "type": "string",
                "description": "Optional target override. Defaults to payload.rhost.",
                "default": "",
            },
            "background": {
                "type": "boolean",
                "description": "Detach into a background worker (default false).",
                "default": False,
            },
        },
        "required": ["name"],
    },
)


def handle(arguments: dict[str, Any], tool_name: str, ctx: MCPContext) -> list:
    """Handle the lazyown_pipeline_run MCP tool."""
    try:
        sys.path.insert(0, str(ctx.lazyown_dir / "modules"))
        from pipeline_engine import mcp_pipeline_run as _pl_run
    except Exception as exc:
        return ctx.text(tool_name, f"[pipeline_run error] pipeline_engine import failed: {exc}")
    try:
        pipeline_name = str(arguments.get("name", "")).strip()
        if not pipeline_name:
            return ctx.text(tool_name, "[pipeline_run error] name is required")
        return ctx.text(
            tool_name,
            _pl_run(
                name=pipeline_name,
                target=str(arguments.get("target", "")).strip(),
                background=bool(arguments.get("background", False)),
            ),
        )
    except Exception as exc:
        return ctx.text(tool_name, f"[pipeline_run error] {exc}")
