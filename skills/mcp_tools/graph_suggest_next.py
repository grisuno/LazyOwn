"""MCP tool ``lazyown_graph_suggest_next`` (migrated from the call_tool dispatch chain)."""

from __future__ import annotations

import json
from typing import Any

from mcp import types
from mcp_tools._context import MCPContext

TOOL = types.Tool(
    name="lazyown_graph_suggest_next",
    description=(
        "Suggest the next commands to run by walking the graphify graph outward from "
        "recent activity. If 'recent' is omitted, reads sessions/LazyOwn_session_report.csv. "
        "Suggestions are scored by inverse graph distance from the recent seeds with "
        "exponential decay, so closely connected commands rank higher. Useful as the "
        "agent equivalent of 'what should I try next?' during an autonomous loop."
    ),
    inputSchema={
        "type": "object",
        "properties": {
            "recent": {
                "type": "array",
                "items": {"type": "string"},
                "description": "Optional list of recent command names (overrides the CSV).",
            },
            "limit": {"type": "integer", "description": "Max suggestions (default 5).", "default": 5},
            "budget_tokens": {"type": "integer", "default": 1500},
        },
    },
)


def handle(arguments: dict[str, Any], tool_name: str, ctx: MCPContext) -> list:
    """Handle the lazyown_graph_suggest_next MCP tool."""
    from cli.graph_advisor import GraphAdvisor as _GraphAdvisor

    recent = arguments.get("recent") or []
    if not isinstance(recent, list):
        recent = []
    limit = int(arguments.get("limit") or 5)
    budget = int(arguments.get("budget_tokens") or 1500)
    advisor = _GraphAdvisor.from_path()
    if not advisor.is_available():
        return ctx.text(tool_name, json.dumps(advisor.summary(), indent=2))
    suggestions = advisor.suggest_next(
        [str(item) for item in recent] if recent else None,
        limit=limit,
    )
    payload = {
        "recent": [str(item) for item in recent] or advisor.read_recent_commands(),
        "suggestions": suggestions,
    }
    payload = advisor.truncate_to_budget(payload, budget)
    return ctx.text(tool_name, json.dumps(payload, indent=2))
