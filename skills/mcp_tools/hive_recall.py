"""MCP tool ``lazyown_hive_recall`` (migrated from the call_tool dispatch chain)."""

from __future__ import annotations

from typing import Any

from mcp import types

from mcp_tools._context import MCPContext

TOOL = types.Tool(
    name="lazyown_hive_recall",
    description=(
        "Semantic + episodic + long-term memory recall from the unified hive ChromaDB. "
        "Searches across ALL drone results, LazyOwn session history, and Parquet knowledge. "
        "Use this instead of lazyown_rag_query for cross-agent queries."
    ),
    inputSchema={
        "type": "object",
        "properties": {
            "query": {"type": "string", "description": "Natural language search"},
            "top_k": {"type": "integer", "default": 10},
        },
        "required": ["query"],
    },
)


def handle(arguments: dict[str, Any], tool_name: str, ctx: MCPContext) -> list:
    """Handle the lazyown_hive_recall MCP tool."""
    try:
        from hive_mind import mcp_hive_recall as _hive_recall
    except Exception:
        return ctx.text(tool_name, "[hive] hive_mind.py not importable")
    try:
        return ctx.text(
            tool_name,
            _hive_recall(
                query=arguments.get("query", ""),
                top_k=int(arguments.get("top_k", 10)),
            ),
        )
    except Exception as exc:
        return ctx.text(tool_name, f"[hive_recall error] {exc}")
