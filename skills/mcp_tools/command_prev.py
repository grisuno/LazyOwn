"""MCP tool ``lazyown_command_prev`` (migrated from the call_tool dispatch chain)."""

from __future__ import annotations

import json
from typing import Any

from mcp import types
from mcp_tools._context import MCPContext

TOOL = types.Tool(
    name="lazyown_command_prev",
    description=(
        "Return the declared prerequisite commands for a verb (the chain's 'prev' arrow). "
        "Useful before launching a command to verify the chain is satisfied. "
        "Mirrors the CLI 'prev <command>' shell command."
    ),
    inputSchema={
        "type": "object",
        "properties": {
            "command": {
                "type": "string",
                "description": "Command verb (with or without the 'do_' prefix).",
            }
        },
        "required": ["command"],
    },
)


def handle(arguments: dict[str, Any], tool_name: str, ctx: MCPContext) -> list:
    """Handle the lazyown_command_prev MCP tool."""
    verb = arguments.get("command", "")
    if not verb:
        return ctx.text(tool_name, json.dumps({"error": "command argument is required"}))
    try:
        from cli.command_chain import CommandChain
    except Exception as exc:
        return ctx.text(tool_name, json.dumps({"error": f"command_chain import failed: {exc}"}))
    chain = CommandChain()
    return ctx.text(tool_name, json.dumps({"command": verb, "prev": chain.prev(verb)}))
