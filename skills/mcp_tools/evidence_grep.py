"""MCP tool ``lazyown_evidence_grep`` (migrated from the call_tool dispatch chain)."""

from __future__ import annotations

import json
from typing import Any

from lazyown_mcp_helpers import evidence_grep
from mcp import types
from mcp_tools._context import MCPContext

TOOL = types.Tool(
    name="lazyown_evidence_grep",
    description=(
        "Grep across sessions/ artefacts with scope filters (loot|nmap|http|logs|all). "
        "Skips binaries and oversized dumps. Returns file:line matches capped for context."
    ),
    inputSchema={
        "type": "object",
        "properties": {
            "pattern": {
                "type": "string",
                "description": "Regex pattern (Python flavour). Case-insensitive by default.",
            },
            "scope": {
                "type": "string",
                "description": "Filter the search to a class of artefacts.",
                "enum": ["all", "loot", "nmap", "http", "logs"],
                "default": "all",
            },
            "max_matches": {
                "type": "integer",
                "description": "Cap on returned matches (default 200).",
                "default": 200,
            },
            "case_sensitive": {
                "type": "boolean",
                "description": "Match case-sensitively (default false).",
                "default": False,
            },
        },
        "required": ["pattern"],
    },
)


def handle(arguments: dict[str, Any], tool_name: str, ctx: MCPContext) -> list:
    """Handle the lazyown_evidence_grep MCP tool."""
    pat = arguments.get("pattern", "").strip()
    if not pat:
        return ctx.text(tool_name, json.dumps({"error": "pattern is required"}))
    scope_eg = arguments.get("scope", "all")
    max_m = int(arguments.get("max_matches", 200))
    case_sens = bool(arguments.get("case_sensitive", False))
    result = evidence_grep(
        pattern=pat,
        sessions_dir=ctx.sessions_dir,
        scope=scope_eg,
        max_matches=max_m,
        case_insensitive=not case_sens,
    )
    return ctx.text(tool_name, json.dumps(result, indent=2, default=str))
