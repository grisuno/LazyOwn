"""MCP tool ``lazyown_set_active_target`` (migrated from the call_tool dispatch chain)."""

from __future__ import annotations

from typing import Any

from mcp import types
from mcp_tools._context import MCPContext

TOOL = types.Tool(
    name="lazyown_set_active_target",
    description=(
        "Set a target from the targets list as the active one — updates rhost, domain, "
        "and related fields in payload.json so all subsequent LazyOwn commands use it. "
        "Optionally updates the target's status."
    ),
    inputSchema={
        "type": "object",
        "properties": {
            "ip": {
                "type": "string",
                "description": "IP of the target to activate (must exist in targets list).",
            },
            "status": {
                "type": "string",
                "description": "Optionally update target status when activating.",
                "enum": ["pending", "in_progress", "owned", "blocked", "done"],
            },
        },
        "required": ["ip"],
    },
)


def handle(arguments: dict[str, Any], tool_name: str, ctx: MCPContext) -> list:
    """Handle the lazyown_set_active_target MCP tool."""
    from datetime import datetime as _dt

    cfg = ctx.load_payload()
    ip = arguments["ip"].strip()
    targets = cfg.get("targets", [])
    target = next((t for t in targets if t.get("ip") == ip), None)

    if not target:
        return ctx.text(tool_name, f"Target {ip} not found in targets list. Add it first with lazyown_add_target.")

    # Update active params
    cfg["rhost"] = ip
    if target.get("domain"):
        cfg["domain"] = target["domain"]

    # Optionally update status
    if "status" in arguments:
        target["status"] = arguments["status"]
        target["updated_at"] = _dt.now().isoformat()
        cfg["targets"] = targets

    ctx.save_payload(cfg)

    summary = (
        f"Active target set to {ip}"
        + (f" ({target['domain']})" if target.get("domain") else "")
        + "\nrhost and domain updated in payload.json."
        + (f"\nStatus → {arguments['status']}" if "status" in arguments else "")
        + f"\nKnown ports: {target.get('ports', [])}"
        + (f"\nNotes: {target['notes']}" if target.get("notes") else "")
    )
    return ctx.text(tool_name, summary)
