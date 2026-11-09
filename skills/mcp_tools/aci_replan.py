"""MCP tool ``lazyown_aci_replan`` (migrated from the call_tool dispatch chain)."""

from __future__ import annotations

from typing import Any

from mcp import types

from mcp_tools._context import MCPContext

TOOL = types.Tool(
    name="lazyown_aci_replan",
    description=(
        "Force adaptive replanning of the active ACI plan when objectives are blocked or stalled. "
        "Generates new objectives for remaining phases using the LLM (with fallback). "
        "Appends lessons to sessions/campaign_lessons.jsonl for future campaigns. "
        "Use this when: blocked_count >= 3, a key technique failed, or the threat model changed. "
        "Example: reason='Kerberoasting blocked by AV, pivot to AS-REP roasting'"
    ),
    inputSchema={
        "type": "object",
        "properties": {
            "reason": {
                "type": "string",
                "description": "Why replanning is needed (informs the LLM for better alternatives).",
                "default": "",
            },
        },
    },
)


def handle(arguments: dict[str, Any], tool_name: str, ctx: MCPContext) -> list:
    """Handle the lazyown_aci_replan MCP tool."""
    try:
        from aci_planner import mcp_aci_replan as _aci_replan
    except Exception:
        return ctx.text(tool_name, "[aci_replan] aci_planner module unavailable.")
    try:
        return ctx.text(tool_name, _aci_replan(reason=arguments.get("reason", "")))
    except Exception as exc:
        return ctx.text(tool_name, f"[aci_replan error] {exc}")
