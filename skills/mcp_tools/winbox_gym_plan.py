"""MCP tool ``lazyown_winbox_gym_plan``: build the WinBox gym attack plan."""

from __future__ import annotations

import json
from typing import Any

from mcp import types

from mcp_tools._context import MCPContext

_ALL_VECTORS = 0

TOOL = types.Tool(
    name="lazyown_winbox_gym_plan",
    description=(
        "Build the ordered WinBox gym attack plan (severity order) for the lab VM IP. "
        "Defaults to rhost when target is omitted."
    ),
    inputSchema={
        "type": "object",
        "properties": {
            "target": {"type": "string", "description": "Lab VM IP (defaults to rhost)."},
            "only": {"type": "array", "items": {"type": "string"}, "description": "Restrict to these vector ids."},
            "top_k": {"type": "integer", "description": "Cap the plan (0 keeps all)."},
        },
        "required": [],
    },
)


def handle(arguments: dict[str, Any], tool_name: str, ctx: MCPContext) -> list:
    """Build the ordered WinBox gym attack plan for a target."""
    try:
        from modules import gym_winbox_runner
    except Exception as error:
        return ctx.text(tool_name, json.dumps({"error": str(error)}))
    target = str(arguments.get("target") or (ctx.load_payload() or {}).get("rhost") or "").strip()
    if not target:
        return ctx.text(tool_name, "target is required (or set rhost)")
    only = arguments.get("only") or []
    try:
        plan = gym_winbox_runner.plan_matrix(
            target,
            only=[str(i) for i in only],
            top_k=int(arguments.get("top_k", _ALL_VECTORS)),
        )
        return ctx.text(tool_name, json.dumps(plan, indent=2))
    except Exception as error:
        return ctx.text(tool_name, json.dumps({"error": str(error)}))
