"""MCP tool ``lazyown_graph_summary`` (migrated from the call_tool dispatch chain)."""

from __future__ import annotations

import json
from typing import Any

from mcp import types
from mcp_tools._context import MCPContext

TOOL = types.Tool(
    name="lazyown_graph_summary",
    description=(
        "Summarise the graphify knowledge graph over the LazyOwn codebase. "
        "Returns node / edge / community counts and the resolved graph file path. "
        "Use this once at the start of a session to know whether richer graph "
        "tools (lazyown_graph_search, lazyown_graph_neighbors, lazyown_graph_suggest_next) "
        "have data to work with. If 'available' is false, the operator must run "
        "'/graphify .' in the project root first to build the graph."
    ),
    inputSchema={"type": "object", "properties": {}},
)


def handle(arguments: dict[str, Any], tool_name: str, ctx: MCPContext) -> list:
    """Handle the lazyown_graph_summary MCP tool."""
    from cli.graph_advisor import GraphAdvisor as _GraphAdvisor

    advisor = _GraphAdvisor.from_path()
    payload = advisor.summary()
    return ctx.text(tool_name, json.dumps(payload, indent=2))
