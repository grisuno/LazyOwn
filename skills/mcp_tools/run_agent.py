"""MCP tool ``lazyown_run_agent`` (migrated from the call_tool dispatch chain)."""

from __future__ import annotations

import asyncio
import os
from typing import Any

from mcp import types

from mcp_tools._context import MCPContext

TOOL = types.Tool(
    name="lazyown_run_agent",
    description=(
        "Delegate a goal to an autonomous AI sub-agent (Groq or Ollama) that runs "
        "LazyOwn commands independently until it completes the goal or hits the iteration limit. "
        "Returns an agent_id immediately — use lazyown_agent_status to poll progress "
        "and lazyown_agent_result to read the final answer.\n\n"
        "Use 'groq' for complex reasoning tasks (requires GROQ_API_KEY in payload.json). "
        "Use 'ollama' for local/offline tasks — currently running: qwen3.5:0.8b.\n\n"
        "Example goals: 'Enumerate SMB shares on rhost', "
        "'Find open ports and identify web services', "
        "'Run LDAP enumeration against the domain'."
    ),
    inputSchema={
        "type": "object",
        "properties": {
            "goal": {
                "type": "string",
                "description": "Natural language task for the agent to complete autonomously.",
            },
            "backend": {
                "type": "string",
                "description": "AI backend: 'groq' (cloud, powerful) or 'ollama' (local, private).",
                "enum": ["groq", "ollama"],
                "default": "ollama",
            },
            "max_iterations": {
                "type": "integer",
                "description": "Max tool-call steps before forcing a summary (default 8).",
                "default": 8,
            },
        },
        "required": ["goal"],
    },
)


async def handle(arguments: dict[str, Any], tool_name: str, ctx: MCPContext) -> list:
    """Handle the lazyown_run_agent MCP tool."""
    try:
        from mcp_agent_bridge import start_agent
    except Exception:
        return ctx.text(tool_name, "Agent bridge not available — check modules/mcp_agent_bridge.py")

    goal = arguments["goal"]
    backend = arguments.get("backend", "ollama")
    max_iterations = int(arguments.get("max_iterations", 8))

    # Inject GROQ_API_KEY from payload.json if not in env
    if backend == "groq" and not os.environ.get("GROQ_API_KEY"):
        cfg = ctx.load_payload()
        key = cfg.get("api_key", "")
        if key:
            os.environ["GROQ_API_KEY"] = key

    def _runner(cmd: str) -> str:
        return ctx.run_command(cmd, timeout=60)

    try:
        agent_id = await asyncio.get_event_loop().run_in_executor(
            None, lambda: start_agent(goal, backend, _runner, max_iterations)
        )
        # Traceability: log spawn to parent transcript (no isolation, just audit)
        try:
            parent = ctx.get_transcript()
            if parent is not None:
                parent.append(
                    "agent_spawned",
                    {
                        "agent_id": agent_id,
                        "goal": goal,
                        "backend": backend,
                        "isolated": False,
                    },
                )
        except Exception:
            pass
        return ctx.text(
            tool_name,
            f"Agent started.\n"
            f"  id:      {agent_id}\n"
            f"  goal:    {goal}\n"
            f"  backend: {backend} (max {max_iterations} steps)\n\n"
            f"Poll with: lazyown_agent_status('{agent_id}')\n"
            f"Results:   lazyown_agent_result('{agent_id}')\n\n"
            f"For ISOLATED execution (sidechain transcript), use:\n"
            f"  lazyown_subagent_run(goal=..., backend=..., max_iterations=...)",
        )
    except Exception as e:
        return ctx.text(tool_name, f"Failed to start agent: {e}")
