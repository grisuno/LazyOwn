"""MCP tool ``lazyown_list_event_rules`` (migrated from the call_tool dispatch chain)."""

from __future__ import annotations

import asyncio
from typing import Any

from mcp import types

from mcp_tools._context import MCPContext

TOOL = types.Tool(
    name="lazyown_list_event_rules",
    description=(
        "List all active event detection rules in the LazyOwn Event Engine. "
        "Returns id, description, trigger conditions, event_type, severity, and suggest action "
        "for every rule currently registered in sessions/event_rules.json. "
        "Use this to audit what patterns are being monitored, identify gaps, "
        "and avoid duplicating existing rules before calling lazyown_add_rule."
    ),
    inputSchema={"type": "object", "properties": {}},
)


async def handle(arguments: dict[str, Any], tool_name: str, ctx: MCPContext) -> list:
    """Handle the lazyown_list_event_rules MCP tool."""
    try:
        from event_engine import load_rules
    except Exception:
        return ctx.text(tool_name, "Event engine not available.")
    rules = await asyncio.get_event_loop().run_in_executor(None, load_rules)
    if not rules:
        return ctx.text(tool_name, "No event detection rules registered.")
    lines = [f"Active event detection rules ({len(rules)} total):\n"]
    for r in rules:
        trigger_parts = [f"{k}={v!r}" for k, v in r.get("trigger", {}).items()]
        lines.append(
            f"[{r['id']}] {r.get('event_type', '?')} ({r.get('severity', 'info')})\n"
            f"  Desc   : {r.get('description', '')}\n"
            f"  Trigger: {', '.join(trigger_parts) or '(none)'}\n"
            f"  Suggest: {r.get('suggest', '')}\n"
        )
    return ctx.text(tool_name, "\n".join(lines))
