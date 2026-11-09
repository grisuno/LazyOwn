"""MCP tool ``lazyown_graph_neighbors`` (migrated from the call_tool dispatch chain)."""

from __future__ import annotations

import json
from typing import Any

from mcp import types
from mcp_tools._context import MCPContext

TOOL = types.Tool(
    name="lazyown_graph_neighbors",
    description=(
        "Return graph neighbours of a node or command from the graphify graph. "
        "Resolves the closest matching node by id or label and walks the graph "
        "outward up to the requested depth. Use this to answer 'what does X depend "
        "on / what is X connected to?' before chaining commands. Returns one entry "
        "per neighbour with the connecting edge relation and confidence."
    ),
    inputSchema={
        "type": "object",
        "properties": {
            "node": {"type": "string", "description": "Node id or fuzzy label."},
            "depth": {"type": "integer", "description": "Hop count (default 1).", "default": 1},
            "limit": {"type": "integer", "description": "Max neighbours (default 25).", "default": 25},
            "budget_tokens": {"type": "integer", "default": 1500},
        },
        "required": ["node"],
    },
)


def handle(arguments: dict[str, Any], tool_name: str, ctx: MCPContext) -> list:
    """Handle the lazyown_graph_neighbors MCP tool."""
    from cli.graph_advisor import GraphAdvisor as _GraphAdvisor

    node = str(arguments.get("node") or "").strip()
    if not node:
        return ctx.text(tool_name, json.dumps({"error": "node is required"}, indent=2))
    depth = int(arguments.get("depth") or 1)
    limit = int(arguments.get("limit") or 25)
    budget = int(arguments.get("budget_tokens") or 1500)
    advisor = _GraphAdvisor.from_path()
    if not advisor.is_available():
        return ctx.text(tool_name, json.dumps(advisor.summary(), indent=2))
    result = advisor.neighbors(node, depth=depth, limit=limit)
    result = advisor.truncate_to_budget(result, budget)
    return ctx.text(tool_name, json.dumps(result, indent=2))
