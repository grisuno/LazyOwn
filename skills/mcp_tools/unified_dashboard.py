"""MCP tool ``lazyown_unified_dashboard``: combined campaign dashboard."""

from __future__ import annotations

import json
from typing import Any

from mcp import types

from mcp_tools._context import MCPContext

TOOL = types.Tool(
    name="lazyown_unified_dashboard",
    description=(
        "Unified campaign dashboard combining world model, Hive Mind status, "
        "policy engine status, autonomous daemon status, LiveSurface graph, "
        "and GraphAdvisor pivot candidates into a single text or JSON snapshot. "
        "Use format=json for structured data, or omit for a text dashboard."
    ),
    inputSchema={
        "type": "object",
        "properties": {
            "format": {
                "type": "string",
                "description": "Output format: 'text' (default) or 'json'.",
                "enum": ["text", "json"],
                "default": "text",
            }
        },
    },
)


async def handle(arguments: dict[str, Any], tool_name: str, ctx: MCPContext) -> list:
    """Render the unified dashboard as text, or JSON when requested."""
    try:
        from modules.unified_dashboard import UnifiedDashboard

        dashboard = UnifiedDashboard(ctx.sessions_dir)
        if arguments.get("format") == "json":
            return ctx.text(tool_name, dashboard.export_json())
        return ctx.text(tool_name, dashboard.render_unified())
    except Exception as exc:
        return ctx.text(tool_name, json.dumps({"error": str(exc)}, indent=2))
