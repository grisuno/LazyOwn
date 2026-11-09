"""MCP tool ``lazyown_list_sessions`` (migrated from the call_tool dispatch chain)."""

from __future__ import annotations

from typing import Any

from mcp import types
from mcp_tools._context import MCPContext

TOOL = types.Tool(
    name="lazyown_list_sessions",
    description="List files in the LazyOwn sessions directory (logs, exfil data, etc.).",
    inputSchema={
        "type": "object",
        "properties": {
            "subdir": {
                "type": "string",
                "description": "Optional subdirectory under sessions/ to list.",
                "default": "",
            }
        },
    },
)


def handle(arguments: dict[str, Any], tool_name: str, ctx: MCPContext) -> list:
    """Handle the lazyown_list_sessions MCP tool."""
    subdir = arguments.get("subdir", "").strip("/")
    target = ctx.sessions_dir / subdir if subdir else ctx.sessions_dir
    try:
        lines = []
        for item in sorted(target.rglob("*")):
            rel = item.relative_to(ctx.sessions_dir)
            if item.is_file():
                lines.append(f"{rel}  ({item.stat().st_size:,} bytes)")
            else:
                lines.append(f"{rel}/")
        return ctx.text(tool_name, "\n".join(lines) if lines else "(empty)")
    except Exception as e:
        return ctx.text(tool_name, f"error: {e}")
