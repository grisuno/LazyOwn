"""MCP tool ``lazyown_heartbeat_status`` (migrated from the call_tool dispatch chain)."""

from __future__ import annotations

import asyncio
import json
from typing import Any

from mcp import types

from mcp_tools._context import MCPContext

TOOL = types.Tool(
    name="lazyown_heartbeat_status",
    description="Check whether the LazyOwn Heartbeat process is running. Returns PID and event counts.",
    inputSchema={"type": "object", "properties": {}},
)


async def handle(arguments: dict[str, Any], tool_name: str, ctx: MCPContext) -> list:
    """Handle the lazyown_heartbeat_status MCP tool."""
    try:
        from event_engine import is_running as _hb_is_running
        from event_engine import load_rules
    except Exception:
        return ctx.text(tool_name, "Event engine not available.")
    running, pid = await asyncio.get_event_loop().run_in_executor(None, _hb_is_running)
    pid_file = ctx.sessions_dir / "heartbeat.pid"
    events_file = ctx.sessions_dir / "events.jsonl"

    pending_count = 0
    total_count = 0
    if events_file.exists():
        for line in events_file.read_text().splitlines():
            if line.strip():
                try:
                    ev = json.loads(line)
                    total_count += 1
                    if ev.get("status") == "pending":
                        pending_count += 1
                except Exception:
                    pass

    status_lines = [
        f"Heartbeat: {'RUNNING (pid=' + str(pid) + ')' if running else 'STOPPED'}",
        f"Events total: {total_count}  |  pending: {pending_count}",
        f"Rules loaded: {len(load_rules())}",
        "To start: python3 skills/heartbeat.py --interval 5 &",
    ]
    return ctx.text(tool_name, "\n".join(status_lines))
