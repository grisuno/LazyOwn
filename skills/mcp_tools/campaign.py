"""MCP tool ``lazyown_campaign`` (migrated from the call_tool dispatch chain)."""

from __future__ import annotations

import asyncio
import json
from typing import Any

from mcp import types
from mcp_tools._context import MCPContext

TOOL = types.Tool(
    name="lazyown_campaign",
    description=(
        "Manage a pentest campaign: group multiple targets under a named engagement "
        "with CIDR scope, per-host phase tracking, and milestones. "
        "Actions: new, status, phase, milestone, complete, add_scope."
    ),
    inputSchema={
        "type": "object",
        "properties": {
            "action": {
                "type": "string",
                "enum": ["new", "status", "phase", "milestone", "complete", "add_scope"],
                "description": "Campaign action to perform.",
            },
            "name": {"type": "string", "description": "Campaign name (for 'new')."},
            "scope": {
                "type": "string",
                "description": (
                    "Comma-separated IPs and/or CIDRs in scope (for 'new'). "
                    "Examples: '127.0.0.1', '10.10.11.0/24,10.10.12.0/24', '192.168.1.5,192.168.1.10'."
                ),
            },
            "host": {"type": "string", "description": "Target host IP (for 'phase')."},
            "phase": {"type": "string", "description": "Phase name (for 'phase')."},
            "title": {"type": "string", "description": "Milestone title (for 'milestone')."},
            "notes": {"type": "string", "description": "Notes (for 'milestone'/'complete'/'new')."},
            "ip_or_cidr": {"type": "string", "description": "IP or CIDR to add to scope (for 'add_scope')."},
        },
        "required": ["action"],
    },
)


async def handle(arguments: dict[str, Any], tool_name: str, ctx: MCPContext) -> list:
    """Handle the lazyown_campaign MCP tool."""
    action = arguments.get("action", "status")

    def _run_campaign() -> str:
        try:
            from lazyown_campaign import CampaignStore

            cs = CampaignStore()
        except ImportError:
            return "lazyown_campaign.py not found in ctx.skills_dir."

        if action == "new":
            camp_name = arguments.get("name", "default")
            raw_scope = arguments.get("scope", "")
            # Accept string (comma-sep), JSON array string, or already-a-list
            if isinstance(raw_scope, list):
                scope = [s.strip() for s in raw_scope if s.strip()]
            elif isinstance(raw_scope, str):
                raw_scope = raw_scope.strip()
                if raw_scope.startswith("["):
                    try:
                        scope = json.loads(raw_scope)
                    except Exception:
                        scope = [raw_scope]
                else:
                    scope = [s.strip() for s in raw_scope.split(",") if s.strip()]
            else:
                scope = []
            notes = arguments.get("notes", "")
            camp = cs.create(camp_name, scope, notes=notes)
            scope_str = ", ".join(scope) if scope else "(none)"
            return f"Campaign '{camp.name}' created. ID: {camp.campaign_id}\nScope: {scope_str}"

        elif action == "status":
            return cs.summary()

        elif action == "phase":
            host = arguments.get("host", "")
            phase = arguments.get("phase", "")
            if not host or not phase:
                return "host and phase are required for action='phase'."
            cs.update_phase(host, phase)
            return f"Phase for {host} set to '{phase}'."

        elif action == "milestone":
            title = arguments.get("title", "")
            notes = arguments.get("notes", "")
            if not title:
                return "title is required for action='milestone'."
            cs.add_milestone(title=title, notes=notes)
            return f"Milestone '{title}' added."

        elif action == "complete":
            notes = arguments.get("notes", "")
            cs.complete(notes=notes)
            return "Campaign marked complete."

        elif action == "add_scope":
            ip_or_cidr = arguments.get("ip_or_cidr", "")
            if not ip_or_cidr:
                return "ip_or_cidr is required for action='add_scope'."
            cs.add_to_scope(ip_or_cidr)
            return f"Added '{ip_or_cidr}' to campaign scope."

        return f"Unknown campaign action: {action}"

    result = await asyncio.get_event_loop().run_in_executor(None, _run_campaign)
    return ctx.text(tool_name, result)
