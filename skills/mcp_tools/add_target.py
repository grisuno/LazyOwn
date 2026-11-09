"""MCP tool ``lazyown_add_target`` (migrated from the call_tool dispatch chain)."""

from __future__ import annotations

from typing import Any

from mcp import types
from mcp_tools._context import MCPContext

TOOL = types.Tool(
    name="lazyown_add_target",
    description=(
        "Add or update a target in payload.json's 'targets' list. "
        "Use this to track multiple hosts, their discovered ports, status, and notes. "
        "The active target (rhost/domain) is set separately via lazyown_set_config. "
        "Targets persist across sessions and can be iterated autonomously."
    ),
    inputSchema={
        "type": "object",
        "properties": {
            "ip": {"type": "string", "description": "Target IP address."},
            "domain": {"type": "string", "description": "Target hostname or domain (optional)."},
            "ports": {
                "type": "array",
                "items": {"type": "integer"},
                "description": "Open ports discovered (optional).",
                "default": [],
            },
            "status": {
                "type": "string",
                "description": "Current status of this target.",
                "enum": ["pending", "in_progress", "owned", "blocked", "done"],
                "default": "pending",
            },
            "notes": {"type": "string", "description": "Free-text notes about this target.", "default": ""},
            "tags": {
                "type": "array",
                "items": {"type": "string"},
                "description": "Labels like ['AD', 'web', 'linux'] for filtering.",
                "default": [],
            },
        },
        "required": ["ip"],
    },
)


def handle(arguments: dict[str, Any], tool_name: str, ctx: MCPContext) -> list:
    """Handle the lazyown_add_target MCP tool."""
    from datetime import datetime as _dt

    cfg = ctx.load_payload()
    if "_error" in cfg:
        return ctx.text(tool_name, f"Cannot load payload.json: {cfg['_error']}")

    targets = cfg.get("targets", [])
    ip = arguments["ip"].strip()

    # Find existing or create new
    existing = next((t for t in targets if t.get("ip") == ip), None)
    if existing:
        if "domain" in arguments:
            existing["domain"] = arguments["domain"]
        if "ports" in arguments:
            existing["ports"] = arguments["ports"]
        if "status" in arguments:
            existing["status"] = arguments["status"]
        if "notes" in arguments:
            existing["notes"] = arguments["notes"]
        if "tags" in arguments:
            existing["tags"] = arguments["tags"]
        existing["updated_at"] = _dt.now().isoformat()
        action = "updated"
    else:
        new_target = {
            "ip": ip,
            "domain": arguments.get("domain", ""),
            "ports": arguments.get("ports", []),
            "status": arguments.get("status", "pending"),
            "notes": arguments.get("notes", ""),
            "tags": arguments.get("tags", []),
            "added_at": _dt.now().isoformat(),
            "updated_at": _dt.now().isoformat(),
        }
        targets.append(new_target)
        action = "added"

    cfg["targets"] = targets
    ctx.save_payload(cfg)
    return ctx.text(tool_name, f"Target {ip} {action}. Total targets: {len(targets)}")
