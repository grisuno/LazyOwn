"""MCP tool ``lazyown_run_command_async`` (migrated from the call_tool dispatch chain)."""

from __future__ import annotations

from lazyown_mcp_helpers import needs_confirmation
import json
from typing import Any

from mcp import types

from mcp_tools._context import MCPContext

TOOL = types.Tool(
    name="lazyown_run_command_async",
    description=(
        "Submit a long-running LazyOwn command to a background job. Returns a job_id "
        "immediately. Poll with lazyown_job_status. Use this for lazynmap, pwntomate, "
        "auto_loop and anything documented as ≥30min. The synchronous run_command tool "
        "blocks the agent; this one frees it to work on something else."
    ),
    inputSchema={
        "type": "object",
        "properties": {
            "command": {
                "type": "string",
                "description": "LazyOwn shell command(s) to execute, newline-separated.",
            },
            "timeout": {
                "type": "integer",
                "description": "Max seconds before the job is killed (default 1800).",
                "default": 1800,
            },
        },
        "required": ["command"],
    },
)


def handle(arguments: dict[str, Any], tool_name: str, ctx: MCPContext) -> list:
    """Handle the lazyown_run_command_async MCP tool."""
    cmd_async = arguments.get("command", "").strip()
    if not cmd_async:
        return ctx.text(tool_name, json.dumps({"error": "command is required"}))
    timeout_async = int(arguments.get("timeout", 1800))
    if needs_confirmation(tool_name, arguments):
        return ctx.text(
            tool_name,
            json.dumps(
                {
                    "error": "confirmation_required",
                    "message": "Re-call with confirm=true for destructive commands.",
                }
            ),
        )
    job_id = ctx.job_store.submit(
        cmd_async,
        runner=ctx.run_command,
        timeout=timeout_async,
    )
    return ctx.text(
        tool_name,
        json.dumps(
            {
                "job_id": job_id,
                "command": cmd_async,
                "timeout": timeout_async,
                "poll_with": f"lazyown_job_status(job_id='{job_id}')",
            },
            indent=2,
        ),
    )
