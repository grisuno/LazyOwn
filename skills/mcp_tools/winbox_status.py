"""MCP tool ``lazyown_winbox_status``: report WinBox lab readiness."""

from __future__ import annotations

import json
from typing import Any

from mcp import types

from mcp_tools._context import MCPContext

TOOL = types.Tool(
    name="lazyown_winbox_status",
    description=(
        "Report WinBox lab readiness: winbox binary, QEMU/libvirt prereqs, VM built, "
        "VM state and IP, plus whether the autonomous loop can attack the lab now."
    ),
    inputSchema={"type": "object", "properties": {}, "required": []},
)


def handle(arguments: dict[str, Any], tool_name: str, ctx: MCPContext) -> list:
    """Report WinBox lab readiness, VM state and autonomous-loop attackability."""
    try:
        from modules import winbox_gym
    except Exception as error:
        return ctx.text(tool_name, json.dumps({"ready": False, "reason": str(error)}))
    try:
        status = winbox_gym.check_readiness(ctx.load_payload())
        status["attack"] = winbox_gym.attack_readiness(ctx.load_payload())
        return ctx.text(tool_name, json.dumps(status, indent=2))
    except Exception as error:
        return ctx.text(tool_name, json.dumps({"ready": False, "reason": str(error)}))
