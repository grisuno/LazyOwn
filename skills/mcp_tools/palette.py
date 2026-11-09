"""MCP tool ``lazyown_palette`` (migrated from the call_tool dispatch chain)."""

from __future__ import annotations

import json
from typing import Any

from mcp import types
from mcp_tools._context import MCPContext

TOOL = types.Tool(
    name="lazyown_palette",
    description=(
        "Browse the operator command catalogue grouped by kill-chain phase. "
        "Returns structured JSON so agents can route across the 422+ do_* commands "
        "without invoking lazyown_run_command blindly. "
        "Modes: empty input -> overview with command counts per phase; "
        "single phase token (e.g. 'recon') -> commands in that phase; "
        "phase plus query (e.g. 'enum nmap') -> filtered phase listing; "
        "'--search <query>' -> fuzzy search across every phase; "
        "'--info <name>' -> full detail with graph-derived 'calls' and 'related' lists; "
        "'--next <phase>' -> commands in the phase that follows in the kill-chain order."
    ),
    inputSchema={
        "type": "object",
        "properties": {
            "line": {
                "type": "string",
                "description": (
                    "Free-form palette query. Empty string yields the overview. "
                    "Examples: '', 'recon', 'enum nmap', '--search ldap', "
                    "'--info do_assign', '--next recon'."
                ),
                "default": "",
            }
        },
    },
)


def handle(arguments: dict[str, Any], tool_name: str, ctx: MCPContext) -> list:
    """Handle the lazyown_palette MCP tool."""
    from cli.palette import CommandIndexError as _PaletteIndexError
    from cli.palette import load_index as _palette_load_index
    from cli.palette_command import render_json as _palette_render_json

    line = str(arguments.get("line", "") or "")
    try:
        palette_index = _palette_load_index()
    except _PaletteIndexError as exc:
        return ctx.text(tool_name, json.dumps({"error": str(exc)}, indent=2))
    result = _palette_render_json(palette_index, line)
    return ctx.text(tool_name, json.dumps(result, indent=2))
