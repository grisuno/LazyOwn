"""MCP tool ``lazyown_winbox_gym_list``: list and validate WinBox gym vectors."""

from __future__ import annotations

import json
from typing import Any

from mcp import types

from mcp_tools._context import MCPContext

TOOL = types.Tool(
    name="lazyown_winbox_gym_list",
    description=(
        "List WinBox gym vectors (severity/service breakdown) and validate the index/exploit/chain matrix consistency."
    ),
    inputSchema={"type": "object", "properties": {}, "required": []},
)


def handle(arguments: dict[str, Any], tool_name: str, ctx: MCPContext) -> list:
    """List WinBox gym vectors and validate the index/exploit/chain matrix."""
    try:
        from modules import winbox_gym
    except Exception as error:
        return ctx.text(tool_name, json.dumps({"error": str(error)}))
    try:
        return ctx.text(tool_name, json.dumps(winbox_gym.summary(), indent=2))
    except Exception as error:
        return ctx.text(tool_name, json.dumps({"error": str(error)}))
