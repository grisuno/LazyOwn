"""MCP tool ``lazyown_swan_ensemble`` (migrated from the call_tool dispatch chain)."""

from __future__ import annotations

import sys
from typing import Any

from mcp import types
from mcp_tools._context import MCPContext

TOOL = types.Tool(
    name="lazyown_swan_ensemble",
    description=(
        "Run a task with multiple top experts in parallel and synthesize their outputs. "
        "Spawns N experts simultaneously via ThreadPoolExecutor, then aggregates results "
        "using weighted text synthesis and consensus confidence scoring. "
        "Higher consensus_pct means experts agreed on the approach. "
        "Use this for high-stakes decisions where corroboration improves confidence: "
        "exploit path selection, privilege escalation strategy, lateral movement planning."
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
                "description": "Natural language description of what the experts should accomplish.",
            },
            "n_experts": {
                "type": "integer",
                "description": "Number of experts to consult in parallel (default 3, max 5).",
                "default": 3,
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
    """Handle the lazyown_swan_ensemble MCP tool."""
    task_type = arguments.get("task_type", "analyze")
    goal = arguments.get("goal", "")
    n_experts = int(arguments.get("n_experts", 3))
    phase = arguments.get("phase", "exploitation")
    if not goal.strip():
        return ctx.text(tool_name, "[swan_ensemble] 'goal' parameter is required.")
    try:
        sys.path.insert(0, str(ctx.lazyown_dir / "skills"))
        from swan_agent import mcp_swan_ensemble as _swan_ensemble

        return ctx.text(tool_name, _swan_ensemble(task_type, goal, n_experts, phase))
    except Exception as exc:
        return ctx.text(tool_name, f"[swan_ensemble error] {exc}")
