"""MCP tool ``lazyown_engage_list_pending`` (migrated from the call_tool dispatch chain)."""

from __future__ import annotations

from typing import Any

from mcp import types
from mcp_tools._context import MCPContext

TOOL = types.Tool(
    name="lazyown_engage_list_pending",
    description=(
        "List every approval request currently awaiting an operator "
        "decision. Useful when running with auto_approve=false to find "
        "the approval ids that need lazyown_engage_approve."
    ),
    inputSchema={"type": "object", "properties": {}, "required": []},
)


def handle(arguments: dict[str, Any], tool_name: str, ctx: MCPContext) -> list:
    """Handle the lazyown_engage_list_pending MCP tool."""
    try:
        from autonomous_daemon import mcp_engage_list_pending as _engage_pending_call
    except Exception as exc:
        return ctx.text(tool_name, f"[engage_list_pending error] autonomous_daemon import failed: {exc}")
    try:
        return ctx.text(tool_name, _engage_pending_call())
    except Exception as exc:
        return ctx.text(tool_name, f"[engage_list_pending error] {exc}")
