"""MCP tool ``lazyown_agent_result`` (migrated from the call_tool dispatch chain)."""

from __future__ import annotations

import asyncio
from typing import Any

from mcp import types

from mcp_tools._context import MCPContext

TOOL = types.Tool(
    name="lazyown_agent_result",
    description=(
        "Read the full result of a completed sub-agent: final answer plus "
        "the complete action log (every tool call and its output)."
    ),
    inputSchema={
        "type": "object",
        "properties": {
            "agent_id": {
                "type": "string",
                "description": "The 8-char agent ID returned by lazyown_run_agent.",
            }
        },
        "required": ["agent_id"],
    },
)


async def handle(arguments: dict[str, Any], tool_name: str, ctx: MCPContext) -> list:
    """Handle the lazyown_agent_result MCP tool."""
    try:
        from mcp_agent_bridge import get_agent_result
    except Exception:
        return ctx.text(tool_name, "Agent bridge not available.")
    agent_id = arguments["agent_id"]
    result = await asyncio.get_event_loop().run_in_executor(None, lambda: get_agent_result(agent_id))
    if "error" in result:
        return ctx.text(tool_name, result["error"])

    lines = [
        f"Agent {agent_id} — {result['status']}",
        f"Goal: {result['goal']}",
        f"Backend: {result['backend']} / {result['model']}",
        f"Steps: {result['iterations']}",
        "",
        "── Action Log ──",
    ]
    for action in result.get("action_log", []):
        lines.append(f"\n[step {action['step']}] {action['tool']}({action['args']})")
        if action.get("output"):
            out = action["output"][:400]
            lines.append(f"  → {out}")
    if result.get("answer"):
        lines.append(f"\n── Final Answer ──\n{result['answer']}")
    return ctx.text(tool_name, "\n".join(lines))
