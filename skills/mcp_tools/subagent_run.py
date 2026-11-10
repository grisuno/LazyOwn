"""MCP tool ``lazyown_subagent_run`` (migrated from the call_tool dispatch chain)."""

from __future__ import annotations

import asyncio
import os
from typing import Any

from mcp import types

from mcp_tools._context import MCPContext

TOOL = types.Tool(
    name="lazyown_subagent_run",
    description=(
        "Run a goal in an ISOLATED subagent transcript (sidechain). "
        "Forks the parent transcript so the subagent has no permission inheritance, "
        "wraps tool calls to log to the sidechain, and returns ONLY the summary "
        "to the parent context (no inflation). Full subagent transcript "
        "remains on disk for audit."
    ),
    inputSchema={
        "type": "object",
        "properties": {
            "goal": {
                "type": "string",
                "description": "What the subagent should accomplish.",
            },
            "backend": {
                "type": "string",
                "description": "groq | ollama (default groq).",
                "default": "groq",
            },
            "max_iterations": {
                "type": "integer",
                "description": "Max steps (default 5).",
                "default": 5,
            },
        },
        "required": ["goal"],
    },
)


async def handle(arguments: dict[str, Any], tool_name: str, ctx: MCPContext) -> list:
    """Handle the lazyown_subagent_run MCP tool."""
    goal = arguments.get("goal", "").strip()
    backend = arguments.get("backend", "groq")
    max_iter = int(arguments.get("max_iterations", 5))
    if not goal:
        return ctx.text(tool_name, "'goal' parameter is required.")

    try:
        from mcp_agent_bridge import start_agent
    except Exception:
        return ctx.text(tool_name, "Agent bridge not available — check modules/mcp_agent_bridge.py")

    # 1. Fork transcript → sidechain (no permission inheritance)
    parent = ctx.get_transcript()
    try:
        from lazyown_session import SessionTranscript

        sidechain = SessionTranscript(ctx.sessions_dir)  # fresh session_id
        sidechain.append(
            "subagent_init",
            {
                "goal": goal,
                "backend": backend,
                "parent_session": parent.session_id if parent else None,
            },
        )
    except Exception as exc:
        return ctx.text(tool_name, f"Failed to create sidechain transcript: {exc}")

    # 2. Log spawn event in PARENT transcript
    if parent is not None:
        parent.append(
            "subagent_spawned",
            {
                "goal": goal,
                "sidechain_session": sidechain.session_id,
            },
        )

    # 3. Wrap _runner so subagent's tool calls write to SIDECHAIN, not parent
    def _isolated_runner(cmd: str) -> str:
        sidechain.append("tool_use", {"tool_name": "shell", "arguments": {"command": cmd}})
        try:
            output = ctx.run_command(cmd, timeout=60)
        except Exception as exc:
            output = f"[runner error] {exc}"
        sidechain.append("tool_result", {"tool_name": "shell", "content": output[:800]})
        return output

    # 4. Inject Groq API key if needed
    if backend == "groq" and not os.environ.get("GROQ_API_KEY"):
        cfg = ctx.load_payload()
        key = cfg.get("api_key", "")
        if key:
            os.environ["GROQ_API_KEY"] = key

    # 5. Spawn the subagent
    try:
        agent_id = await asyncio.get_event_loop().run_in_executor(
            None, lambda: start_agent(goal, backend, _isolated_runner, max_iter)
        )
    except Exception as exc:
        sidechain.append("subagent_error", {"error": str(exc)})
        return ctx.text(tool_name, f"Subagent failed to start: {exc}")

    # 6. Return ONLY summary to parent context (no full history inflation)
    sidechain.append("subagent_started", {"agent_id": agent_id})
    return ctx.text(
        tool_name,
        f"## Subagent Spawned (Isolated Sidechain)\n"
        f"  agent_id:           {agent_id}\n"
        f"  goal:               {goal}\n"
        f"  backend:            {backend} (max {max_iter} steps)\n"
        f"  sidechain session:  {sidechain.session_id}\n"
        f"  sidechain file:     {sidechain.path}\n"
        f"  parent session:     {parent.session_id if parent else '(none)'}\n\n"
        f"Permissions are NOT inherited from parent (security isolation).\n"
        f"Tool calls log to sidechain only — parent context stays clean.\n\n"
        f"Track progress: lazyown_agent_status('{agent_id}')\n"
        f"Get final result: lazyown_agent_result('{agent_id}')\n"
        f"Resume sidechain: lazyown_session_resume('{sidechain.session_id}')",
    )
