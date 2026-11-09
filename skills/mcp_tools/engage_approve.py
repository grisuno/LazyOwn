"""MCP tool ``lazyown_engage_approve`` (migrated from the call_tool dispatch chain)."""

from __future__ import annotations

from typing import Any

from mcp import types
from mcp_tools._context import MCPContext

TOOL = types.Tool(
    name="lazyown_engage_approve",
    description=(
        "Resolve a pending approval issued by the ApprovalGate. The "
        "decision must be either 'approved' or 'denied'. Approval ids "
        "come from lazyown_engage_status or lazyown_engage_list_pending."
    ),
    inputSchema={
        "type": "object",
        "properties": {
            "approval_id": {
                "type": "string",
                "description": "Approval identifier returned when the gate was triggered.",
            },
            "decision": {
                "type": "string",
                "enum": ["approved", "denied"],
                "description": "Operator decision.",
            },
            "operator": {
                "type": "string",
                "description": "Optional operator handle for audit.",
                "default": "",
            },
        },
        "required": ["approval_id", "decision"],
    },
)


def handle(arguments: dict[str, Any], tool_name: str, ctx: MCPContext) -> list:
    """Handle the lazyown_engage_approve MCP tool."""
    try:
        from autonomous_daemon import mcp_engage_approve as _engage_approve_call
    except Exception as exc:
        return ctx.text(tool_name, f"[engage_approve error] autonomous_daemon import failed: {exc}")
    try:
        approval_id = str(arguments.get("approval_id", "")).strip()
        decision = str(arguments.get("decision", "")).strip().lower()
        operator = str(arguments.get("operator", "")).strip()
        if not approval_id or decision not in ("approved", "denied"):
            return ctx.text(tool_name, "[engage_approve error] approval_id and decision='approved|denied' are required")
        return ctx.text(tool_name, _engage_approve_call(approval_id, decision, operator))
    except Exception as exc:
        return ctx.text(tool_name, f"[engage_approve error] {exc}")
