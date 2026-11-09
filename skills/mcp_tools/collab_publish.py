"""MCP tool ``lazyown_collab_publish`` (migrated from the call_tool dispatch chain)."""

from __future__ import annotations

import json
import sys
from typing import Any

from mcp import types
from mcp_tools._context import MCPContext

TOOL = types.Tool(
    name="lazyown_collab_publish",
    description=(
        "Broadcast a structured event to all connected operators via SSE. "
        "Use this to share findings, alerts, or status updates in real time. "
        "Operators connected to /collab/stream will receive the event immediately."
    ),
    inputSchema={
        "type": "object",
        "properties": {
            "type": {
                "type": "string",
                "description": "Event type: 'finding', 'command', 'phase_change', 'alert', 'chat'.",
            },
            "payload": {
                "type": "string",
                "description": "JSON string with event payload data.",
            },
            "operator": {
                "type": "string",
                "description": "Operator name (default: 'agent').",
                "default": "agent",
            },
        },
        "required": ["type", "payload"],
    },
)


def handle(arguments: dict[str, Any], tool_name: str, ctx: MCPContext) -> list:
    """Handle the lazyown_collab_publish MCP tool."""
    cp_type = arguments.get("type", "generic").strip()
    cp_payload = arguments.get("payload", "{}").strip()
    cp_operator = arguments.get("operator", "agent").strip()
    try:
        payload_dict = json.loads(cp_payload) if cp_payload else {}
    except Exception:
        payload_dict = {"raw": cp_payload}
    try:
        sys.path.insert(0, str(ctx.lazyown_dir / "modules"))
        from collab_bp import publish_event

        publish_event(type=cp_type, payload=payload_dict, operator=cp_operator)
        return ctx.text(tool_name, f"Event '{cp_type}' published to {cp_operator} channel.")
    except Exception as exc:
        return ctx.text(tool_name, f"[collab_publish error] {exc}")
