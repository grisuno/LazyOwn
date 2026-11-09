"""MCP tool ``lazyown_read_session_file`` (migrated from the call_tool dispatch chain)."""

from __future__ import annotations

from typing import Any

from mcp import types
from mcp_tools._context import MCPContext

TOOL = types.Tool(
    name="lazyown_read_session_file",
    description="Read the contents of a file in the LazyOwn sessions directory.",
    inputSchema={
        "type": "object",
        "properties": {
            "filepath": {
                "type": "string",
                "description": "Relative path inside sessions/ (e.g. 'logs/beacon1.log').",
            }
        },
        "required": ["filepath"],
    },
)


def handle(arguments: dict[str, Any], tool_name: str, ctx: MCPContext) -> list:
    """Handle the lazyown_read_session_file MCP tool."""
    filepath = arguments["filepath"].lstrip("/")
    target = ctx.sessions_dir / filepath
    # Safety: ensure path stays inside sessions/
    try:
        target.resolve().relative_to(ctx.sessions_dir.resolve())
    except ValueError:
        return ctx.text(tool_name, "error: path traversal not allowed")
    try:
        content = target.read_text(errors="replace")
        if len(content) > 8000:
            content = content[:8000] + "\n... [truncated]"
        return ctx.text(tool_name, content)
    except Exception as e:
        return ctx.text(tool_name, f"error: {e}")
