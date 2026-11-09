"""MCP tool ``lazyown_target_context`` (migrated from the call_tool dispatch chain)."""

from __future__ import annotations

import json
from typing import Any

from lazyown_mcp_helpers import build_target_context
from mcp import types
from mcp_tools._context import MCPContext

TOOL = types.Tool(
    name="lazyown_target_context",
    description=(
        "Aggregate everything known about a target (host[, port]) into one structured "
        "JSON response: open ports from nmap, world-model credentials with provenance and "
        "confidence scores, vulnerabilities, pwntomate evidence directories with freshness, "
        "nmap scan freshness. Replaces 4-5 separate lookups when deciding next steps."
    ),
    inputSchema={
        "type": "object",
        "properties": {
            "host": {
                "type": "string",
                "description": "Target IP/hostname. Defaults to payload.json rhost.",
                "default": "",
            },
            "port": {
                "type": "integer",
                "description": "Optional port filter (return only data scoped to this port).",
            },
        },
    },
)


def handle(arguments: dict[str, Any], tool_name: str, ctx: MCPContext) -> list:
    """Handle the lazyown_target_context MCP tool."""
    cfg_tc = ctx.load_payload()
    host_tc = (arguments.get("host") or cfg_tc.get("rhost") or "").strip()
    if not host_tc:
        return ctx.text(tool_name, json.dumps({"error": "host not provided and rhost is empty"}))
    port_tc = arguments.get("port")
    wm_path_tc = ctx.sessions_dir / "world_model.json"
    wm_data: dict = {}
    if wm_path_tc.exists():
        try:
            wm_data = json.loads(wm_path_tc.read_text())
        except (OSError, json.JSONDecodeError):
            wm_data = {}
    ctx = build_target_context(
        host=host_tc,
        port=int(port_tc) if port_tc not in (None, "") else None,
        sessions_dir=ctx.sessions_dir,
        payload=cfg_tc,
        world_model=wm_data,
    )
    return ctx.text(tool_name, json.dumps(ctx, indent=2, default=str))
