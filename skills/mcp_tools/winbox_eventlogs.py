"""MCP tool ``lazyown_winbox_eventlogs``: query guest Windows event logs."""

from __future__ import annotations

import json
from typing import Any

from mcp import types

from mcp_tools._context import MCPContext

_DEFAULT_MAX_EVENTS = 100

TOOL = types.Tool(
    name="lazyown_winbox_eventlogs",
    description=(
        "Query Windows event logs inside the WinBox guest via Get-WinEvent. Useful to "
        "review what the guest logged about a run (logon events, Sysmon, Defender)."
    ),
    inputSchema={
        "type": "object",
        "properties": {
            "since": {"type": "string", "description": "Window like 5m, 1h, 1d."},
            "max": {"type": "integer", "description": "Maximum events (default 100)."},
            "logs": {
                "type": "array",
                "items": {"type": "string"},
                "description": "Channels, e.g. ['Security', 'Microsoft-Windows-Sysmon/Operational'].",
            },
        },
        "required": [],
    },
)


def handle(arguments: dict[str, Any], tool_name: str, ctx: MCPContext) -> list:
    """Query Windows event logs inside the WinBox guest."""
    try:
        from modules import winbox_gym
    except Exception as error:
        return ctx.text(tool_name, json.dumps({"error": str(error)}))
    try:
        argv = ["eventlogs"]
        since = str(arguments.get("since") or "").strip()
        if since:
            argv += ["--since", since]
        max_events = int(arguments.get("max", _DEFAULT_MAX_EVENTS))
        argv += ["--max", str(max_events)]
        for channel in arguments.get("logs") or []:
            argv += ["--log", str(channel)]
        result = winbox_gym.run_cli(argv, timeout=winbox_gym.CLI_TIMEOUT_SEC)
        return ctx.text(tool_name, json.dumps(result, indent=2))
    except Exception as error:
        return ctx.text(tool_name, json.dumps({"error": str(error)}))
