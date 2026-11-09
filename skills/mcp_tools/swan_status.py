"""MCP tool ``lazyown_swan_status`` (migrated from the call_tool dispatch chain)."""

from __future__ import annotations

import sys
from typing import Any

from mcp import types
from mcp_tools._context import MCPContext

TOOL = types.Tool(
    name="lazyown_swan_status",
    description=(
        "Show current SWAN system status: MoE expert weights, RL epsilon (exploration rate), "
        "per-expert performance EMA, total routing calls, and temperature. "
        "Useful for understanding which experts are currently preferred and how "
        "much exploration is still happening."
    ),
    inputSchema={"type": "object", "properties": {}},
)


def handle(arguments: dict[str, Any], tool_name: str, ctx: MCPContext) -> list:
    """Handle the lazyown_swan_status MCP tool."""
    try:
        sys.path.insert(0, str(ctx.lazyown_dir / "skills"))
        from swan_agent import mcp_swan_status as _swan_status

        return ctx.text(tool_name, _swan_status())
    except Exception as exc:
        return ctx.text(tool_name, f"[swan_status error] {exc}")
