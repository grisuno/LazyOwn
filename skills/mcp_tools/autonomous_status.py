"""MCP tool ``lazyown_autonomous_status`` (migrated from the call_tool dispatch chain)."""

from __future__ import annotations

from typing import Any

from mcp import types

from mcp_tools._context import MCPContext

TOOL = types.Tool(
    name="lazyown_autonomous_status",
    description=(
        "Estado en tiempo real del daemon: fase actual, objetivo activo, "
        "pasos ejecutados, drones spawneados, eventos emitidos."
    ),
    inputSchema={"type": "object", "properties": {}, "required": []},
)


def handle(arguments: dict[str, Any], tool_name: str, ctx: MCPContext) -> list:
    """Handle the lazyown_autonomous_status MCP tool."""
    try:
        from autonomous_daemon import mcp_autonomous_status as _auto_status
    except Exception:
        return ctx.text(tool_name, "[auto] autonomous_daemon.py no importable")
    try:
        return ctx.text(tool_name, _auto_status())
    except Exception as exc:
        return ctx.text(tool_name, f"[autonomous_status error] {exc}")
