"""MCP tool ``lazyown_agent_status`` (migrated from the call_tool dispatch chain)."""

from __future__ import annotations

import asyncio
from typing import Any

from mcp import types

from mcp_tools._context import MCPContext

TOOL = types.Tool(
    name="lazyown_agent_status",
    description=(
        "Check the current status of a running or completed sub-agent. "
        "Returns: status (running/completed/failed), iterations completed, "
        "last tool called, and the final answer if done."
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
    """Handle the lazyown_agent_status MCP tool."""
    try:
        from mcp_agent_bridge import get_agent_status
    except Exception:
        return ctx.text(tool_name, "Agent bridge not available.")
    agent_id = arguments["agent_id"]
    status = await asyncio.get_event_loop().run_in_executor(None, lambda: get_agent_status(agent_id))
    if "error" in status:
        return ctx.text(tool_name, status["error"])

    icon = {"completed": "✅", "running": "🔄", "failed": "❌"}.get(status["status"], "❓")
    lines = [
        f"{icon} Agent {agent_id}  [{status['status']}]",
        f"  goal:     {status['goal']}",
        f"  backend:  {status['backend']} / {status['model']}",
        f"  steps:    {status['iterations']}",
        f"  started:  {status.get('started_at', '')[:19]}",
    ]
    if status.get("last_action"):
        lines.append(f"  last:     {status['last_action']}")
    if status.get("finished_at"):
        lines.append(f"  finished: {status['finished_at'][:19]}")
    if status.get("answer"):
        lines.append(f"\nAnswer:\n{status['answer'][:800]}")
    return ctx.text(tool_name, "\n".join(lines))
