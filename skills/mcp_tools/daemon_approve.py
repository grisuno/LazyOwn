"""MCP tool ``lazyown_daemon_approve`` (migrated from the call_tool dispatch chain)."""

from __future__ import annotations

import json
from typing import Any

from mcp import types
from mcp_tools._context import MCPContext

TOOL = types.Tool(
    name="lazyown_daemon_approve",
    description=(
        "Approve or veto the daemon's currently-pending command. "
        "Returns the resolved PendingAction or an error string when no "
        "action is awaiting a decision."
    ),
    inputSchema={
        "type": "object",
        "properties": {
            "decision": {
                "type": "string",
                "enum": ["approved", "vetoed"],
                "default": "approved",
            },
            "operator": {
                "type": "string",
                "description": "Identifier of the deciding operator.",
                "default": "mcp",
            },
        },
        "required": ["decision"],
    },
)


def handle(arguments: dict[str, Any], tool_name: str, ctx: MCPContext) -> list:
    """Handle the lazyown_daemon_approve MCP tool."""
    try:
        from daemon_control import DaemonControl as _DC

        decision = str(arguments.get("decision", "approved")).strip().lower()
        operator = str(arguments.get("operator", "mcp")).strip()
        control = _DC(ctx.sessions_dir)
        pending = control.load().pending
        if pending is None:
            return ctx.text(
                tool_name,
                json.dumps(
                    {"ok": False, "error": "no pending action"},
                    ensure_ascii=False,
                ),
            )
        final = control.decide(
            pending.action_id,
            decision,
            operator=operator,
        )
        if final is None:
            return ctx.text(
                tool_name,
                json.dumps(
                    {"ok": False, "error": "pending action lost during decide"},
                    ensure_ascii=False,
                ),
            )
        return ctx.text(
            tool_name,
            json.dumps(
                {
                    "ok": True,
                    "action_id": final.action_id,
                    "decision": final.decision,
                    "command": final.command,
                    "operator": final.operator,
                    "decided_at": final.decided_at,
                },
                ensure_ascii=False,
            ),
        )
    except ValueError as exc:
        return ctx.text(tool_name, f"[daemon_approve error] {exc}")
    except Exception as exc:
        return ctx.text(tool_name, f"[daemon_approve error] {exc}")
