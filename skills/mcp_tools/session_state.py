"""MCP tool ``lazyown_session_state`` (migrated from the call_tool dispatch chain)."""

from __future__ import annotations

import asyncio
from typing import Any

from mcp import types

from mcp_tools._context import MCPContext

TOOL = types.Tool(
    name="lazyown_session_state",
    description=(
        "Return the current aggregated session state: active phase, "
        "discovered hosts, open ports, captured credentials, last commands run, "
        "and pending unactioned events. "
        "Use this to understand the full picture before deciding what to do next."
    ),
    inputSchema={
        "type": "object",
        "properties": {
            "refresh": {
                "type": "boolean",
                "description": "Force rebuild from raw data even if cached state is fresh (default false).",
                "default": False,
            }
        },
    },
)


async def handle(arguments: dict[str, Any], tool_name: str, ctx: MCPContext) -> list:
    """Handle the lazyown_session_state MCP tool."""
    try:
        from session_state import load as _state_load
        from session_state import refresh as _state_refresh
    except Exception:
        return ctx.text(tool_name, "session_state module not available — check modules/session_state.py")
    force = arguments.get("refresh", False)
    state = await asyncio.get_event_loop().run_in_executor(None, lambda: _state_refresh() if force else _state_load())
    # Pretty-print key sections
    hosts_lines = []
    for ip, info in state.get("hosts", {}).items():
        ports = info.get("ports", [])
        domain = info.get("domain", "")
        active = " ◄ active" if info.get("is_active") else ""
        hosts_lines.append(
            f"  {ip}" + (f" ({domain})" if domain else "") + (f"  ports:{ports}" if ports else "") + active
        )
    pending = state.get("pending_events", [])
    ev_lines = [f"  [{e['severity'].upper()}] {e['type']}  — {e['suggest'][:70]}" for e in pending]
    output = "\n".join(
        [
            f"Phase:          {state['phase']}",
            f"Active target:  {state['active_target']}  (os: {state['os_target']})",
            f"Domain:         {state['domain'] or 'unknown'}",
            f"Lhost:          {state['lhost']}",
            "",
            f"Hosts ({len(state['hosts'])}):",
        ]
        + (hosts_lines or ["  (none)"])
        + [
            "",
            f"Credentials:    {state['credentials'] or ['none']}",
            f"Last commands:  {', '.join(state['last_commands'][-6:]) or 'none'}",
            "",
            f"Pending events ({state['open_event_count']}):",
        ]
        + (ev_lines or ["  (none)"])
        + [
            "",
            f"Generated: {state['generated_at'][:19]}",
        ]
    )
    return ctx.text(tool_name, output)
