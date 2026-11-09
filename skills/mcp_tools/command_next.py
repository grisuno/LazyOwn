"""MCP tool ``lazyown_command_next`` (migrated from the call_tool dispatch chain)."""

from __future__ import annotations

import json
from typing import Any

from mcp import types
from mcp_tools._context import MCPContext

TOOL = types.Tool(
    name="lazyown_command_next",
    description=(
        "Return ordered next-step recommendations for a verb. Combines the static "
        "kill-chain map, nmap-discovered services, and exploration engine triggers "
        "(addons + tools) into one deduplicated list with provenance. Mirrors the "
        "CLI 'next <command>' shell command."
    ),
    inputSchema={
        "type": "object",
        "properties": {
            "command": {
                "type": "string",
                "description": "Command verb (with or without the 'do_' prefix).",
            },
            "target": {
                "type": "string",
                "description": "Optional rhost filter for nmap XML lookups.",
            },
            "phase": {
                "type": "string",
                "description": "Optional engagement phase (recon|enum|exploit|...).",
            },
            "limit": {
                "type": "integer",
                "description": "Maximum number of recommendations (default 5).",
                "default": 5,
            },
        },
        "required": ["command"],
    },
)


def handle(arguments: dict[str, Any], tool_name: str, ctx: MCPContext) -> list:
    """Handle the lazyown_command_next MCP tool."""
    verb = arguments.get("command", "")
    if not verb:
        return ctx.text(tool_name, json.dumps({"error": "command argument is required"}))
    try:
        from cli.command_chain import CommandChain
    except Exception as exc:
        return ctx.text(tool_name, json.dumps({"error": f"command_chain import failed: {exc}"}))
    cfg = ctx.load_payload()
    target = arguments.get("target") or cfg.get("rhost") or None
    phase = arguments.get("phase") or cfg.get("phase") or ""
    limit = arguments.get("limit") or 5
    chain = CommandChain()
    steps = chain.next(cmd=verb, params=cfg, target=target, phase=phase, limit=limit)
    return ctx.text(
        tool_name,
        json.dumps(
            {
                "command": verb,
                "target": target,
                "phase": phase,
                "next": [step.to_dict() for step in steps],
            }
        ),
    )
