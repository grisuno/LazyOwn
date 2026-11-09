"""MCP tool ``lazyown_generate_report`` (migrated from the call_tool dispatch chain)."""

from __future__ import annotations

import sys
from typing import Any

from mcp import types
from mcp_tools._context import MCPContext

TOOL = types.Tool(
    name="lazyown_generate_report",
    description=(
        "Auto-generate a structured Markdown penetration test report "
        "from session artefacts (facts, events, credentials, objectives, plan). "
        "The report is written to sessions/report_<timestamp>.md and the path is returned."
    ),
    inputSchema={
        "type": "object",
        "properties": {
            "output": {
                "type": "string",
                "description": "Optional output file path. Defaults to sessions/report_<ts>.md.",
                "default": "",
            },
        },
        "required": [],
    },
)


def handle(arguments: dict[str, Any], tool_name: str, ctx: MCPContext) -> list:
    """Handle the lazyown_generate_report MCP tool."""
    output_path = arguments.get("output", "").strip() or None
    try:
        sys.path.insert(0, str(ctx.lazyown_dir / "modules"))
        from report_generator import ReportGenerator

        rg = ReportGenerator(sessions_dir=ctx.lazyown_dir / "sessions")
        path = rg.generate(output_path=output_path)
        return ctx.text(tool_name, f"Report generated: {path}")
    except Exception as exc:
        return ctx.text(tool_name, f"[report error] {exc}")
