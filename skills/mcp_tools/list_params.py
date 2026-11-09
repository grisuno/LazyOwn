"""MCP tool ``lazyown_list_params`` (migrated from the call_tool dispatch chain)."""

from __future__ import annotations

from typing import Any

from mcp import types
from mcp_tools._context import MCPContext

TOOL = types.Tool(
    name="lazyown_list_params",
    description=(
        "List the shared parameter catalog: every builtin payload key plus the "
        "operator parameters declared in params/operator.yaml. Parameters are the "
        "tokens every addon, alias and pipeline can substitute, so reuse them "
        "instead of inventing addon-branded keys."
    ),
    inputSchema={
        "type": "object",
        "properties": {
            "keyword": {
                "type": "string",
                "description": "Case-insensitive filter over name and description.",
            },
            "source": {
                "type": "string",
                "description": "Filter by origin: builtin, operator or all (default).",
                "enum": ["all", "builtin", "operator"],
                "default": "all",
            },
        },
    },
)


def handle(arguments: dict[str, Any], tool_name: str, ctx: MCPContext) -> list:
    """Handle the lazyown_list_params MCP tool."""
    try:
        from core.param_registry import list_params

        keyword = str(arguments.get("keyword") or "")
        source = str(arguments.get("source") or "all").strip().lower()
        params = list_params(include_builtin=source in ("all", "builtin"), keyword=keyword)
        if source == "operator":
            params = [p for p in params if p.source == "operator"]
        lines = [
            f"{'*' if p.source == 'operator' else ' '} {p.name:<28} {p.kind:<10} "
            f"{str(p.default)[:30]:<32} {p.description[:70]}"
            for p in params
        ]
    except Exception as e:
        return ctx.text(tool_name, f"error listing parameters: {e}")
    return ctx.text(
        tool_name, f"Parameters ({len(lines)}):\n" + "\n".join(lines) if lines else "No parameters matched."
    )
