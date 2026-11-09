"""MCP tool ``lazyown_inject_objective``: queue a new attack objective."""

from __future__ import annotations

import asyncio
from typing import Any

from mcp import types

from mcp_tools._context import MCPContext

_DEFAULT_PRIORITY = "high"
_PENDING_LIST_LIMIT = 100

TOOL = types.Tool(
    name="lazyown_inject_objective",
    description=(
        "Inject a new high-level attack objective into the objective queue. "
        "USE THIS as the frontier-model reasoning entry point: after reading "
        "plan.txt, facts, or events, formulate specific next-step objectives "
        "and inject them here so the autonomous loop can execute them. "
        "Example objectives: "
        "'Enumerate SMB shares on 10.10.11.78 port 445 — use crackmapexec', "
        "'Kerberoast service accounts found in LDAP enum', "
        "'Run linPEAS on beacon abc123 — privesc phase'. "
        "Injected objectives are picked up by auto_loop and next_objective."
    ),
    inputSchema={
        "type": "object",
        "properties": {
            "text": {
                "type": "string",
                "description": "Objective text — be specific: include target, tool, port.",
            },
            "priority": {
                "type": "string",
                "description": "Priority: critical / high / medium / low (default: high).",
                "enum": ["critical", "high", "medium", "low"],
                "default": _DEFAULT_PRIORITY,
            },
            "notes": {
                "type": "string",
                "description": "Optional reasoning notes — why this objective, what evidence.",
                "default": "",
            },
        },
        "required": ["text"],
    },
)


async def handle(arguments: dict[str, Any], tool_name: str, ctx: MCPContext) -> list:
    """Inject one objective into the queue and report the new pending count."""
    try:
        from lazyown_objective import ObjectiveStore
    except Exception:
        return ctx.text(tool_name, "Objective store unavailable. Check skills/lazyown_objective.py.")
    objectives = ObjectiveStore()
    obj_text = arguments["text"]
    priority = arguments.get("priority", _DEFAULT_PRIORITY)
    notes = arguments.get("notes", "")
    obj = await asyncio.get_event_loop().run_in_executor(
        None,
        lambda: objectives.inject(obj_text, priority=priority, source="claude", notes=notes),
    )
    pending = len(objectives.list_pending(limit=_PENDING_LIST_LIMIT))
    return ctx.text(
        tool_name,
        f"Objective injected [{obj.id}] priority={obj.priority}\n"
        f"  {obj.text}\n\n"
        f"Queue now has {pending} pending objective(s).\n"
        f"Use lazyown_auto_loop or lazyown_run_command to act on it.",
    )
