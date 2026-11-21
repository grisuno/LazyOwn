"""MCP tool ``lazyown_crack_facts``: crack FactStore crypt hashes for a host."""

from __future__ import annotations

import asyncio
import shlex
from typing import Any

from mcp import types

from mcp_tools._context import MCPContext

TOOL = types.Tool(
    name="lazyown_crack_facts",
    description=(
        "Export the crypt-family password hashes the FactStore spool ingested "
        "for a host (shadow dumps from /etc/shadow reads or container-host-mount "
        "escapes), run john/hashcat against them with the configured wordlist "
        "and return every cracked password to the LazyOwnDB credentials table "
        "and to the loop world model as unbound lateral spray candidates. "
        "Fail-open: an empty FactStore answers without executing anything."
    ),
    inputSchema={
        "type": "object",
        "properties": {
            "host": {
                "type": "string",
                "description": "Host IP whose hashes to consume. Defaults to rhost from payload.json.",
                "default": "",
            },
            "wordlist": {
                "type": "string",
                "description": "Optional wordlist path override (default: the common wordlist list).",
                "default": "",
            },
        },
        "required": [],
    },
)


async def handle(arguments: dict[str, Any], tool_name: str, ctx: MCPContext) -> list:
    """Handle the lazyown_crack_facts MCP tool."""
    host = (arguments.get("host", "") or "").strip()
    wordlist = (arguments.get("wordlist", "") or "").strip()
    if not host:
        host = str(ctx.load_payload().get("rhost", "") or "").strip()
    if not host:
        return ctx.text(tool_name, "[crack_facts] host is required (or set rhost).")

    command = f"crack_facts {shlex.quote(host)}"
    if wordlist:
        command += f" --wordlist {shlex.quote(wordlist)}"

    def _do_crack() -> str:
        return ctx.run_command(command)

    output = await asyncio.get_event_loop().run_in_executor(None, _do_crack)
    return ctx.text(tool_name, output or "[crack_facts] no output captured.")
