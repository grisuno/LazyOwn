"""MCP tool ``lazyown_winbox_gym_run``: run the WinBox gym matrix on the lab."""

from __future__ import annotations

import json
from typing import Any

from mcp import types

from mcp_tools._context import MCPContext

_ALL_VECTORS = 0

TOOL = types.Tool(
    name="lazyown_winbox_gym_run",
    description=(
        "Run the WinBox gym matrix against the lab VM: one chain per vector in severity "
        "order, CTF captures verified into sessions/ctf. Ensures the VM is up first."
    ),
    inputSchema={
        "type": "object",
        "properties": {
            "target": {"type": "string", "description": "Lab VM IP (defaults to rhost)."},
            "only": {"type": "array", "items": {"type": "string"}, "description": "Restrict to these vector ids."},
            "dry_run": {"type": "boolean", "description": "Resolve without executing.", "default": False},
            "top_k": {"type": "integer", "description": "Cap the plan (0 keeps all)."},
        },
        "required": [],
    },
)


def handle(arguments: dict[str, Any], tool_name: str, ctx: MCPContext) -> list:
    """Run the WinBox gym matrix against the lab VM and verify captures."""
    try:
        from modules import gym_winbox_runner
    except Exception as error:
        return ctx.text(tool_name, json.dumps({"error": str(error)}))
    payload = ctx.load_payload() or {}
    target = str(arguments.get("target") or payload.get("rhost") or "").strip()
    if not target:
        return ctx.text(tool_name, "target is required (or set rhost)")
    only = arguments.get("only") or []
    try:
        result = gym_winbox_runner.run_matrix(
            target,
            dry_run=bool(arguments.get("dry_run", False)),
            only=[str(i) for i in only],
            top_k=int(arguments.get("top_k", _ALL_VECTORS)),
            lhost=str(payload.get("lhost") or ""),
            lport=str(payload.get("lport") or ""),
        )
        return ctx.text(tool_name, json.dumps(result, indent=2))
    except Exception as error:
        return ctx.text(tool_name, json.dumps({"error": str(error)}))
