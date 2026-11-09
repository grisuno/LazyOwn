"""MCP tool ``lazyown_swan_run`` (migrated from the call_tool dispatch chain)."""

from __future__ import annotations

import sys
from typing import Any

from mcp import types
from mcp_tools._context import MCPContext

TOOL = types.Tool(
    name="lazyown_swan_run",
    description=(
        "Route a task to the best expert using the MoE+RL (SWAN) system and execute it. "
        "The Mixture-of-Experts router selects the optimal LLM expert (groq_fast, "
        "groq_powerful, groq_deepseek_r1, ollama_reason, groq_gemma) based on learned "
        "Q-values for the (task_type, engagement_phase) state. "
        "Returns the expert's output along with routing metadata: expert chosen, "
        "detection probability, and RL reward signal. "
        "task_type examples: recon, exploit, privesc, lateral, cred, analyze, report. "
        "phase examples: reconnaissance, exploitation, post_exploitation, lateral_movement."
    ),
    inputSchema={
        "type": "object",
        "properties": {
            "task_type": {
                "type": "string",
                "description": "Category of the task (recon, exploit, privesc, lateral, cred, analyze, report).",
            },
            "goal": {
                "type": "string",
                "description": "Natural language description of what the expert should accomplish.",
            },
            "phase": {
                "type": "string",
                "description": "Current engagement phase (default: exploitation).",
                "default": "exploitation",
            },
        },
        "required": ["task_type", "goal"],
    },
)


def handle(arguments: dict[str, Any], tool_name: str, ctx: MCPContext) -> list:
    """Handle the lazyown_swan_run MCP tool."""
    task_type = arguments.get("task_type", "analyze")
    goal = arguments.get("goal", "")
    phase = arguments.get("phase", "exploitation")
    if not goal.strip():
        return ctx.text(tool_name, "[swan_run] 'goal' parameter is required.")
    try:
        sys.path.insert(0, str(ctx.lazyown_dir / "skills"))
        from swan_agent import mcp_swan_run as _swan_run

        return ctx.text(tool_name, _swan_run(task_type, goal, phase))
    except Exception as exc:
        return ctx.text(tool_name, f"[swan_run error] {exc}")
