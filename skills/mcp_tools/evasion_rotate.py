"""MCP tool ``lazyown_evasion_rotate``: rotate to a fresh evasion profile."""

from __future__ import annotations

import json
from typing import Any

from mcp import types

from mcp_tools._context import MCPContext

TOOL = types.Tool(
    name="lazyown_evasion_rotate",
    description=(
        "Rotate to a new evasion profile — generates a fresh random "
        "profile and makes it active. Useful for long-running beacons "
        "to avoid pattern detection."
    ),
    inputSchema={
        "type": "object",
        "properties": {},
        "required": [],
    },
)


async def handle(arguments: dict[str, Any], tool_name: str, ctx: MCPContext) -> list:
    """Rotate the active evasion profile and return it as JSON."""
    try:
        from modules.evasion_engine import EvasionEngine

        engine = EvasionEngine(ctx.load_payload())
        profile = engine.rotate_profile()
        return ctx.text(tool_name, engine.profile_to_json(profile))
    except Exception as exc:
        return ctx.text(tool_name, json.dumps({"error": str(exc)}, indent=2))
