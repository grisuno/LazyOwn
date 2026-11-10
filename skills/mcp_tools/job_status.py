"""MCP tool ``lazyown_job_status`` (migrated from the call_tool dispatch chain)."""

from __future__ import annotations

import json
from typing import Any

from mcp import types

from mcp_tools._context import MCPContext

TOOL = types.Tool(
    name="lazyown_job_status",
    description=(
        "Inspect background jobs created by lazyown_run_command_async. "
        "Without job_id returns a list of recent jobs; with job_id returns full record "
        "including stdout once the job finishes."
    ),
    inputSchema={
        "type": "object",
        "properties": {
            "job_id": {
                "type": "string",
                "description": "Job identifier from lazyown_run_command_async.",
                "default": "",
            },
            "limit": {
                "type": "integer",
                "description": "List size when job_id is omitted (default 20).",
                "default": 20,
            },
        },
    },
)


def handle(arguments: dict[str, Any], tool_name: str, ctx: MCPContext) -> list:
    """Handle the lazyown_job_status MCP tool."""
    jid = (arguments.get("job_id") or "").strip()
    if jid:
        status_rec = ctx.job_store.status(jid)
        if status_rec is None:
            return ctx.text(tool_name, json.dumps({"error": f"unknown job_id: {jid}"}))
        return ctx.text(tool_name, json.dumps(status_rec, indent=2, default=str))
    limit_js = int(arguments.get("limit", 20))
    return ctx.text(
        tool_name,
        json.dumps(
            {
                "jobs": ctx.job_store.list(limit=limit_js),
            },
            indent=2,
            default=str,
        ),
    )
