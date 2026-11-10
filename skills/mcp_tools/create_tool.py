"""MCP tool ``lazyown_create_tool`` (migrated from the call_tool dispatch chain)."""

from __future__ import annotations

import asyncio
from typing import Any

from mcp import types

from mcp_tools._context import MCPContext

TOOL = types.Tool(
    name="lazyown_create_tool",
    description=(
        "Create a new pwntomate .tool file so that future runs of pwntomate "
        "automatically apply it to matching services discovered by nmap. "
        "Each .tool file defines a command template with placeholders "
        "{ip} {port} {domain} {username} {password} {outputdir} {s} (ssl). "
        "The file is written to tools/ and takes effect on the next pwntomate run. "
        "Use this when you discover a service that has no existing tool coverage."
    ),
    inputSchema={
        "type": "object",
        "properties": {
            "toolname": {
                "type": "string",
                "description": "Unique name for the tool (e.g. 'redis_enum').",
            },
            "command": {
                "type": "string",
                "description": (
                    "Shell command template. Use {ip}, {port}, {domain}, "
                    "{username}, {password}, {outputdir}, {s} as placeholders."
                ),
            },
            "trigger": {
                "type": "array",
                "items": {"type": "string"},
                "description": (
                    "List of nmap service names that activate this tool "
                    "(e.g. ['http', 'https']). Use ['all'] to run on every port."
                ),
            },
            "active": {
                "type": "boolean",
                "description": "Whether the tool is active (default true).",
                "default": True,
            },
        },
        "required": ["toolname", "command", "trigger"],
    },
)


async def handle(arguments: dict[str, Any], tool_name: str, ctx: MCPContext) -> list:
    """Handle the lazyown_create_tool MCP tool."""
    toolname = arguments["toolname"]
    command = arguments["command"]
    trigger = arguments["trigger"]
    active = bool(arguments.get("active", True))
    try:
        from lazyown_facts import create_tool_file as _create_tool_file

        tools_dir = ctx.lazyown_dir / "tools"
        written = await asyncio.get_event_loop().run_in_executor(
            None,
            lambda: _create_tool_file(toolname, command, trigger, active, tools_dir),
        )
        return ctx.text(
            tool_name,
            f"Tool file created: {written}\n"
            f"  toolname: {toolname}\n"
            f"  trigger:  {trigger}\n"
            f"  active:   {active}\n"
            f"  command:  {command}\n\n"
            "Run 'pwntomate <nmap.xml> -x' or the pwntomate LazyOwn command "
            "to apply it to the current scan.",
        )
    except Exception as exc:
        return ctx.text(tool_name, f"Failed to create tool file: {exc}")
