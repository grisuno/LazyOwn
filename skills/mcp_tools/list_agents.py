"""MCP tool ``lazyown_list_agents`` (migrated from the call_tool dispatch chain)."""

from __future__ import annotations

import asyncio
from typing import Any

from mcp import types

from mcp_tools._context import MCPContext

TOOL = types.Tool(
    name="lazyown_list_agents",
    description="List recent sub-agents with their status, goal, backend, and iteration count.",
    inputSchema={
        "type": "object",
        "properties": {
            "limit": {
                "type": "integer",
                "description": "Max agents to return (default 10).",
                "default": 10,
            }
        },
    },
)


async def handle(arguments: dict[str, Any], tool_name: str, ctx: MCPContext) -> list:
    """Handle the lazyown_list_agents MCP tool."""
    try:
        from mcp_agent_bridge import list_agents
    except Exception:
        return ctx.text(tool_name, "Agent bridge not available.")
    limit = int(arguments.get("limit", 10))
    agents = await asyncio.get_event_loop().run_in_executor(None, lambda: list_agents(limit=limit))
    if not agents:
        return ctx.text(tool_name, "No agents found.")
    icon = {"completed": "✅", "running": "🔄", "failed": "❌"}
    lines = [f"Recent agents ({len(agents)}):\n"]
    for a in agents:
        lines.append(
            f"{icon.get(a['status'], '❓')} {a['agent_id']}  "
            f"[{a['backend']}]  {a['status']:<12}  steps={a['iterations']}"
        )
        lines.append(f"   goal: {a['goal'][:70]}")
    return ctx.text(tool_name, "\n".join(lines))
