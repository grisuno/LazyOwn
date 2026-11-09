"""MCP tool ``lazyown_run_command``: execute LazyOwn shell commands.

The central execution tool. It pre-flights on request, gates destructive
commands behind confirmation, runs via the C2 ``/api/run`` endpoint with a
subprocess fallback, publishes a command event, and reports the outcome to
the policy layer. All runtime dependencies arrive through the injected
:class:`mcp_tools._context.MCPContext`, so this file never imports the MCP
runtime module.
"""

from __future__ import annotations

import asyncio
import json
from typing import Any

from mcp import types

from mcp_tools._context import MCPContext

_DEFAULT_TIMEOUT_SEC = 30
_EVENT_SNIPPET_CHARS = 500

TOOL = types.Tool(
    name="lazyown_run_command",
    description=(
        "Execute one or more commands in the LazyOwn interactive shell. "
        "Separate multiple commands with newlines. "
        "Examples: 'list', 'set rhost 10.10.11.78', 'lazynmap'. "
        "Pass dry_run=true to get a pre-flight report (binary present, OS match, "
        "would-duplicate, missing payload keys) without executing."
    ),
    inputSchema={
        "type": "object",
        "properties": {
            "command": {
                "type": "string",
                "description": "LazyOwn shell command(s) to execute (newline-separated).",
            },
            "timeout": {
                "type": "integer",
                "description": "Max seconds to wait for output (default 30).",
                "default": _DEFAULT_TIMEOUT_SEC,
            },
            "dry_run": {
                "type": "boolean",
                "description": "Pre-flight only: validate without executing.",
                "default": False,
            },
            "confirm": {
                "type": "boolean",
                "description": "Required for destructive commands (rm -rf, exfil, wipe).",
                "default": False,
            },
        },
        "required": ["command"],
    },
)


def _publish_command_event(command: str, output: str, operator: str, target: str) -> None:
    """Publish a COMMAND event for the executed command, best-effort."""
    try:
        from event_bus import EventCategory, LazyEvent, get_event_bus

        parts = command.strip().split(None, 1)
        cmd_name = parts[0] if parts else command
        get_event_bus().publish(
            LazyEvent(
                category=EventCategory.COMMAND,
                event_type=cmd_name,
                source="mcp",
                payload={"command": command, "output_snippet": output[:_EVENT_SNIPPET_CHARS]},
                target=target,
                operator=operator,
            )
        )
    except Exception:
        pass


async def handle(arguments: dict[str, Any], tool_name: str, ctx: MCPContext) -> list:
    """Pre-flight, confirm, execute and record one or more shell commands."""
    from lazyown_mcp_helpers import needs_confirmation, preflight_command

    command = arguments["command"]
    timeout = int(arguments.get("timeout", _DEFAULT_TIMEOUT_SEC))
    dry_run = bool(arguments.get("dry_run", False))

    if dry_run:
        preflight = preflight_command(command, ctx.load_payload(), ctx.sessions_dir)
        return ctx.text(tool_name, json.dumps(preflight, indent=2))

    if needs_confirmation(tool_name, arguments):
        return ctx.text(
            tool_name,
            f"CONFIRMATION REQUIRED for command: {command}\n"
            f"Re-call with confirm=true to execute. "
            f"This command appears destructive (rm -rf, exfil, wipe, encrypt-file).",
        )

    def _run_with_fallback(cmd: str, to: int) -> str:
        c2_result = ctx.c2_request("/api/run", method="POST", body={"command": cmd})
        if "_error" in c2_result or "error" in c2_result:
            return f"[via subprocess]\n{ctx.run_command(cmd, to)}"
        output = c2_result.get("output", c2_result.get("result", ""))
        if not output:
            return f"[via subprocess]\n{ctx.run_command(cmd, to)}"
        return f"[via C2 /api/run]\n{output}"

    output = await asyncio.get_event_loop().run_in_executor(None, lambda: _run_with_fallback(command, timeout))

    cfg = ctx.load_payload()
    _publish_command_event(command, output, arguments.get("operator", "mcp"), cfg.get("rhost", ""))

    policy = ctx.get_policy()
    if policy is not None:
        target = cfg.get("rhost", "") or cfg.get("lhost", "127.0.0.1")
        parts = command.strip().split(None, 1)
        cmd_name = parts[0] if parts else command
        cmd_args = parts[1] if len(parts) > 1 else ""
        try:
            await asyncio.get_event_loop().run_in_executor(
                None,
                lambda: policy.on_command_complete(target, cmd_name, cmd_args, output, None),
            )
        except Exception:
            pass

    return ctx.text(tool_name, output)
