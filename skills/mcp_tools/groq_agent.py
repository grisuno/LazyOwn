"""MCP tool ``lazyown_groq_agent`` (migrated from the call_tool dispatch chain)."""

from __future__ import annotations

import asyncio
import os
import sys
from typing import Any

from mcp import types
from mcp_tools._context import MCPContext

TOOL = types.Tool(
    name="lazyown_groq_agent",
    description=(
        "Spawn an autonomous Groq or Ollama agent pre-loaded with 21 LazyOwn tools: "
        "run_command, bridge_suggest, bridge_catalog, parquet_context, facts_show, "
        "cve_lookup, memory_search, session_status, read_session_file, list_sessions, "
        "c2_status, c2_command, task_list, task_add, inject_objective, "
        "reactive_suggest, searchsploit, command_help, rag_query, threat_model, "
        "atomic_search. "
        "Groq uses native tool calling; Ollama uses ReAct prompt engineering. "
        "async_mode=False (default) blocks and returns the final answer. "
        "async_mode=True fires-and-forgets and returns an agent_id to poll with "
        "lazyown_agent_status / lazyown_agent_result."
    ),
    inputSchema={
        "type": "object",
        "properties": {
            "goal": {
                "type": "string",
                "description": "Autonomous goal for the agent to pursue.",
            },
            "tools_filter": {
                "type": "array",
                "items": {"type": "string"},
                "description": (
                    "Restrict the agent to a subset of the 18 tools. "
                    "Default: all tools. Example: ['run_command','bridge_suggest','facts_show']"
                ),
                "default": [],
            },
            "backend": {
                "type": "string",
                "enum": ["groq", "ollama"],
                "description": "'groq' for native tool calling, 'ollama' for local ReAct.",
                "default": "groq",
            },
            "max_iterations": {
                "type": "integer",
                "description": "Max tool-call iterations before the agent returns a Final Answer.",
                "default": 8,
            },
            "async_mode": {
                "type": "boolean",
                "description": "True = fire-and-forget (returns agent_id); False = block until done.",
                "default": False,
            },
            "system_prompt": {
                "type": "string",
                "description": "Override the default agent system prompt (optional).",
                "default": "",
            },
        },
        "required": ["goal"],
    },
)


async def handle(arguments: dict[str, Any], tool_name: str, ctx: MCPContext) -> list:
    """Handle the lazyown_groq_agent MCP tool."""
    ga_goal = arguments.get("goal", "").strip()
    if not ga_goal:
        return ctx.text(tool_name, "[groq_agent] 'goal' is required.")
    ga_tools = arguments.get("tools_filter") or None
    ga_backend = arguments.get("backend", "groq")
    ga_max_iter = int(arguments.get("max_iterations", 8))
    ga_async = bool(arguments.get("async_mode", False))
    ga_sys_prompt = arguments.get("system_prompt", "")
    try:
        sys.path.insert(0, str(ctx.skills_dir))
        from lazyown_groq_agents import get_pool as _groq_pool

        cfg = ctx.load_payload()
        api_key = cfg.get("api_key", "") or os.environ.get("GROQ_API_KEY", "")
        pool = _groq_pool()

        if ga_async:
            agent_id = pool.spawn(
                goal=ga_goal,
                tools_filter=ga_tools,
                api_key=api_key,
                backend=ga_backend,
                max_iterations=ga_max_iter,
                system_prompt=ga_sys_prompt,
                block=False,
            )
            return ctx.text(
                tool_name,
                f"Agent spawned: {agent_id}\n"
                f"Backend  : {ga_backend}\n"
                f"Tools    : {len(ga_tools) if ga_tools else 18}\n"
                f"Max iter : {ga_max_iter}\n\n"
                f"Poll: lazyown_agent_status(agent_id='{agent_id}')\n"
                f"Read: lazyown_agent_result(agent_id='{agent_id}')",
            )

        # Synchronous mode — run in thread executor so we don't block the
        # MCP async event loop while the agent iterates.
        def _blocking_run() -> str:
            aid = pool.spawn(
                goal=ga_goal,
                tools_filter=ga_tools,
                api_key=api_key,
                backend=ga_backend,
                max_iterations=ga_max_iter,
                system_prompt=ga_sys_prompt,
                block=True,
            )
            return pool.result(aid)

        answer = await asyncio.get_event_loop().run_in_executor(None, _blocking_run)
        return ctx.text(tool_name, answer)

    except Exception as exc:
        return ctx.text(tool_name, f"[groq_agent error] {exc}")
