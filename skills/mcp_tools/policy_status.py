"""MCP tool ``lazyown_policy_status`` (migrated from the call_tool dispatch chain)."""

from __future__ import annotations

import asyncio
from typing import Any

from mcp import types

from mcp_tools._context import MCPContext

TOOL = types.Tool(
    name="lazyown_policy_status",
    description=(
        "Show the policy engine episode summary and next-action recommendations for a target. "
        "Displays total accumulated reward, number of steps, last observed state, and "
        "ranked recommended categories derived from learned transition frequencies and "
        "hand-coded override rules. Use after bootstrap or after executing commands."
    ),
    inputSchema={
        "type": "object",
        "properties": {
            "target": {
                "type": "string",
                "description": "Target IP or hostname. Defaults to rhost from payload.json.",
            }
        },
        "required": [],
    },
)


async def handle(arguments: dict[str, Any], tool_name: str, ctx: MCPContext) -> list:
    """Handle the lazyown_policy_status MCP tool."""
    _policy = ctx.get_policy()
    if _policy is None:
        return ctx.text(tool_name, "Policy engine unavailable. Run: python3 skills/lazyown_policy.py bootstrap")
    cfg = ctx.load_payload()
    target = arguments.get("target") or cfg.get("rhost", "") or "127.0.0.1"
    summary = await asyncio.get_event_loop().run_in_executor(None, lambda: _policy._advisor.episode_summary(target))
    recs = await asyncio.get_event_loop().run_in_executor(None, lambda: _policy.get_recommendations(target))
    lines: list[str] = []
    if summary:
        lines.append(
            f"Episode  target={summary['target']}  "
            f"steps={summary['steps']}  "
            f"total_reward={summary['total_reward']:+d}  "
            f"last_state={summary['last_state']}"
        )
    else:
        lines.append(f"No episode data for {target}. Run bootstrap or execute commands first.")
    lines.append("\nRecommendations:")
    for i, r in enumerate(recs, 1):
        bar = "█" * int(r["confidence"] * 10)
        lines.append(f"  {i}. [{bar:<10}] {r['confidence']:.0%}  category={r['category']}  [{r['source']}]")
        lines.append(f"       {r['reason']}")
    return ctx.text(tool_name, "\n".join(lines))
