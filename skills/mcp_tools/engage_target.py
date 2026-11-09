"""MCP tool ``lazyown_engage_target`` (migrated from the call_tool dispatch chain)."""

from __future__ import annotations

from typing import Any

from mcp import types
from mcp_tools._context import MCPContext

TOOL = types.Tool(
    name="lazyown_engage_target",
    description=(
        "Run the single-command kill-chain orchestrator against one target. "
        "Executes ping/OS-detect, nmap, auto_populate, enum, exploit "
        "search, and initial-access in order. Each step consults the "
        "ApprovalGate (gated by payload.auto_approve), retries via the "
        "bridge catalog when a tool fails, and narrates progress to "
        "sessions/engagement.log + collab feed. Returns the engagement "
        "id when detach=true (default) so callers can poll progress. "
        "With auto=true the run is fully unattended: a ScopeBoundAutoGate "
        "replaces the ApprovalGate (approves in-scope steps, denies "
        "out-of-scope targets under scope_enforcement=enforce, never "
        "prompts) and a client-ready report is written to sessions/."
    ),
    inputSchema={
        "type": "object",
        "properties": {
            "target": {
                "type": "string",
                "description": "Target IPv4 address or hostname to engage.",
            },
            "max_switches_per_step": {
                "type": "integer",
                "description": "Maximum fallback tools tried per phase before giving up.",
                "default": 3,
            },
            "detach": {
                "type": "boolean",
                "description": "Run the engagement in a background thread (default true).",
                "default": True,
            },
            "auto": {
                "type": "boolean",
                "description": (
                    "Full auto mode with no human in the loop. Scope acts as "
                    "the fail-closed safety boundary and a report is generated "
                    "on completion. Default false."
                ),
                "default": False,
            },
        },
        "required": ["target"],
    },
)


def handle(arguments: dict[str, Any], tool_name: str, ctx: MCPContext) -> list:
    """Handle the lazyown_engage_target MCP tool."""
    try:
        from autonomous_daemon import mcp_engage_target as _engage_call
    except Exception as exc:
        return ctx.text(tool_name, f"[engage_target error] autonomous_daemon import failed: {exc}")
    try:
        target = str(arguments.get("target", "")).strip()
        if not target:
            return ctx.text(tool_name, "[engage_target error] target is required")
        return ctx.text(
            tool_name,
            _engage_call(
                target=target,
                max_switches_per_step=int(arguments.get("max_switches_per_step", 3)),
                detach=bool(arguments.get("detach", True)),
                auto=bool(arguments.get("auto", False)),
            ),
        )
    except Exception as exc:
        return ctx.text(tool_name, f"[engage_target error] {exc}")
