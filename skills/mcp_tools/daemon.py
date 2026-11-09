"""MCP tool ``lazyown_daemon`` (migrated from the call_tool dispatch chain)."""

from __future__ import annotations

import asyncio
import subprocess
import sys
from typing import Any

from mcp import types
from mcp_tools._context import MCPContext

TOOL = types.Tool(
    name="lazyown_daemon",
    description=(
        "Manage the LazyOwn unified background daemon that combines the file watcher, "
        "event engine, and heartbeat into a single asyncio process. "
        "Actions: start, stop, status."
    ),
    inputSchema={
        "type": "object",
        "properties": {
            "action": {
                "type": "string",
                "enum": ["start", "stop", "status"],
                "description": "Daemon action.",
            },
        },
        "required": ["action"],
    },
)


async def handle(arguments: dict[str, Any], tool_name: str, ctx: MCPContext) -> list:
    """Handle the lazyown_daemon MCP tool."""
    action = arguments.get("action", "status")

    def _run_daemon() -> str:

        daemon_script = str(ctx.skills_dir / "lazyown_daemon.py")

        if action == "start":
            try:
                proc = subprocess.Popen(
                    [sys.executable, daemon_script, "start"],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                )
                out, err = proc.communicate(timeout=10)
                return (out + err).decode(errors="replace").strip() or "Daemon start requested."
            except Exception as exc:
                return f"Failed to start daemon: {exc}"

        elif action == "stop":
            try:
                proc = subprocess.run(
                    [sys.executable, daemon_script, "stop"],
                    capture_output=True,
                    timeout=10,
                )
                return proc.stdout.decode(errors="replace").strip() or "Daemon stop requested."
            except Exception as exc:
                return f"Failed to stop daemon: {exc}"

        elif action == "status":
            try:
                proc = subprocess.run(
                    [sys.executable, daemon_script, "status"],
                    capture_output=True,
                    timeout=10,
                )
                return proc.stdout.decode(errors="replace").strip() or "No daemon status available."
            except Exception as exc:
                return f"Daemon status error: {exc}"

        return f"Unknown daemon action: {action}"

    result = await asyncio.get_event_loop().run_in_executor(None, _run_daemon)
    return ctx.text(tool_name, result)
