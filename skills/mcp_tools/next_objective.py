"""MCP tool ``lazyown_next_objective`` (migrated from the call_tool dispatch chain)."""

from __future__ import annotations

import asyncio
import json
from typing import Any

from mcp import types

from mcp_tools._context import MCPContext

TOOL = types.Tool(
    name="lazyown_next_objective",
    description=(
        "Return the full frontier-model context needed to reason about the next action: "
        "• soul.md — agent persona, priorities, hard stops\n"
        "• sessions/plan.txt — current VulnBot-generated attack plan\n"
        "• Next pending objective from the queue\n"
        "• Count of remaining pending objectives\n"
        "• Top 5 pending objectives preview\n\n"
        "USE THIS at the start of each reasoning cycle before deciding what to do. "
        "After reading this, inject new objectives or run auto_loop."
    ),
    inputSchema={"type": "object", "properties": {}},
)


async def handle(arguments: dict[str, Any], tool_name: str, ctx: MCPContext) -> list:
    """Handle the lazyown_next_objective MCP tool."""
    try:
        from lazyown_objective import full_context_for_claude as _full_context_for_claude
    except Exception:
        return ctx.text(tool_name, "Objective store unavailable.")
    ctx = await asyncio.get_event_loop().run_in_executor(None, lambda: _full_context_for_claude())
    parts = []
    parts.append("=== SOUL ===")
    parts.append(ctx.get("soul", "(none)"))
    parts.append("\n=== CURRENT ATTACK PLAN ===")
    parts.append(ctx.get("plan", "(none)"))
    parts.append(f"\n=== OBJECTIVES ({ctx.get('pending_count', 0)} pending) ===")
    next_obj = ctx.get("next_objective")
    if next_obj:
        parts.append(f"NEXT [{next_obj['priority']}] [{next_obj['id']}]\n  {next_obj['text']}")
        if next_obj.get("notes"):
            parts.append(f"  Notes: {next_obj['notes']}")
        if next_obj.get("context"):
            parts.append(f"  Context: {json.dumps(next_obj['context'])}")
    else:
        parts.append("No pending objectives. Inject one with lazyown_inject_objective.")
    if ctx.get("pending_preview"):
        parts.append("\nFull queue:")
        for o in ctx["pending_preview"]:
            parts.append(f"  [{o['priority']:8s}] [{o['id']}] {o['text'][:80]}")
    return ctx.text(tool_name, "\n".join(parts))
