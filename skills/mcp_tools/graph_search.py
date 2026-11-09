"""MCP tool ``lazyown_graph_search`` (migrated from the call_tool dispatch chain)."""

from __future__ import annotations

import json
from typing import Any

from mcp import types
from mcp_tools._context import MCPContext

TOOL = types.Tool(
    name="lazyown_graph_search",
    description=(
        "Fuzzy-search the graphify knowledge graph for nodes matching a query. "
        "Returns ranked nodes (label, id, degree, community, source file) so agents can "
        "locate a command, class or concept without scanning the full palette. "
        "Use this before lazyown_run_command when you only have a vague description "
        "('AD enumeration', 'kerberoast', 'shellcode loader')."
    ),
    inputSchema={
        "type": "object",
        "properties": {
            "query": {"type": "string", "description": "Free-text query."},
            "limit": {"type": "integer", "description": "Max results (default 10).", "default": 10},
            "budget_tokens": {
                "type": "integer",
                "description": "Soft cap on response size in tokens (default 1500).",
                "default": 1500,
            },
        },
        "required": ["query"],
    },
)


def handle(arguments: dict[str, Any], tool_name: str, ctx: MCPContext) -> list:
    """Handle the lazyown_graph_search MCP tool."""
    from cli.graph_advisor import GraphAdvisor as _GraphAdvisor

    query = str(arguments.get("query") or "").strip()
    if not query:
        return ctx.text(tool_name, json.dumps({"error": "query is required"}, indent=2))
    limit = int(arguments.get("limit") or 10)
    budget = int(arguments.get("budget_tokens") or 1500)
    advisor = _GraphAdvisor.from_path()
    if not advisor.is_available():
        return ctx.text(tool_name, json.dumps(advisor.summary(), indent=2))
    payload = {"query": query, "results": advisor.search(query, limit=limit)}
    payload = advisor.truncate_to_budget(payload, budget)
    return ctx.text(tool_name, json.dumps(payload, indent=2))
