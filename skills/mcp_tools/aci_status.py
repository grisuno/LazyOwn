"""MCP tool ``lazyown_aci_status`` (migrated from the call_tool dispatch chain)."""

from __future__ import annotations

from typing import Any

from mcp import types

from mcp_tools._context import MCPContext

TOOL = types.Tool(
    name="lazyown_aci_status",
    description=(
        "Return live status of the active ACI plan: phase breakdown, completion percentage, "
        "blocked objective count, replan recommendation, and per-phase technique mapping. "
        "Syncs phase statuses against the ObjectiveStore before reporting. "
        "Returns {available: false} if no plan exists — call lazyown_aci_plan first."
    ),
    inputSchema={
        "type": "object",
        "properties": {},
    },
)


def handle(arguments: dict[str, Any], tool_name: str, ctx: MCPContext) -> list:
    """Handle the lazyown_aci_status MCP tool."""
    try:
        from aci_planner import mcp_aci_status as _aci_status
    except Exception:
        return ctx.text(tool_name, "[aci_status] aci_planner module unavailable.")
    try:
        return ctx.text(tool_name, _aci_status())
    except Exception as exc:
        return ctx.text(tool_name, f"[aci_status error] {exc}")
