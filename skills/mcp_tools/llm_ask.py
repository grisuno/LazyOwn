"""MCP tool ``lazyown_llm_ask`` (migrated from the call_tool dispatch chain)."""

from __future__ import annotations

import asyncio
import os
from typing import Any

from mcp import types

from mcp_tools._context import MCPContext

TOOL = types.Tool(
    name="lazyown_llm_ask",
    description=(
        "Ask a satellite language model (Groq or local deepseek-r1:1.5b) "
        "to reason about a goal using LazyOwn tools.\n\n"
        "Groq backend — llama-3.3-70b with native tool calling: "
        "run_command, read_nmap, read_plan, read_facts, read_objectives.\n"
        "Ollama backend — deepseek-r1:1.5b via ReAct loop (Thought/Action/Observation). "
        "No API key needed; runs fully offline.\n\n"
        "Use this when you need a satellite model to:\n"
        "  • Analyse an nmap scan and suggest next steps\n"
        "  • Interpret tool output and extract credentials/findings\n"
        "  • Generate a specific exploit or command sequence\n"
        "  • Reason about facts/objectives before injecting a new goal"
    ),
    inputSchema={
        "type": "object",
        "properties": {
            "goal": {
                "type": "string",
                "description": "Goal or question for the satellite model.",
            },
            "context": {
                "type": "string",
                "description": "Optional extra context (paste tool output, facts, etc.).",
                "default": "",
            },
            "backend": {
                "type": "string",
                "description": "'groq' (cloud, tool calling) or 'ollama' (local deepseek-r1, ReAct).",
                "enum": ["groq", "ollama"],
                "default": "groq",
            },
            "model": {
                "type": "string",
                "description": "Override model name (e.g. 'llama-3.1-8b-instant' for groq, 'deepseek-r1:1.5b' for ollama).",
                "default": "",
            },
            "max_iterations": {
                "type": "integer",
                "description": "Max tool-call cycles (default 6).",
                "default": 6,
            },
            "system_prompt": {
                "type": "string",
                "description": "Optional system prompt override.",
                "default": "",
            },
        },
        "required": ["goal"],
    },
)


async def handle(arguments: dict[str, Any], tool_name: str, ctx: MCPContext) -> list:
    """Handle the lazyown_llm_ask MCP tool."""
    try:
        from lazyown_llm import llm_ask as _llm_ask
    except Exception:
        return ctx.text(tool_name, "LLM bridge unavailable. Check skills/lazyown_llm.py.")
    goal = arguments["goal"]
    context = arguments.get("context", "")
    backend = arguments.get("backend", "groq")
    model_override = arguments.get("model", "") or None
    max_iter = int(arguments.get("max_iterations", 6))
    sys_prompt = arguments.get("system_prompt", "")

    cfg = ctx.load_payload()
    api_key = cfg.get("api_key", "") or os.environ.get("GROQ_API_KEY", "")

    if backend == "groq" and not api_key:
        return ctx.text(
            tool_name,
            "Groq backend requires api_key in payload.json or GROQ_API_KEY env var. "
            "Use backend='ollama' for local deepseek-r1:1.5b (no key needed).",
        )

    result = await asyncio.get_event_loop().run_in_executor(
        None,
        lambda: _llm_ask(
            goal=goal,
            context=context,
            backend=backend,
            model=model_override,
            api_key=api_key if backend == "groq" else None,
            max_iterations=max_iter,
            system_prompt=sys_prompt,
        ),
    )
    return ctx.text(tool_name, result)
