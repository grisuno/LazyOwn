"""MCP tool ``lazyown_lazymode_playbook``: list and run lazymode playbooks.

A lazymode playbook captures a whole exploitation path (recon-informed
trigger, session, proof) as one administrable asset in ``playbooks/``.
This tool lists those playbooks and runs one against a target, returning
the compact structured outcome (never the raw tool output).
"""

from __future__ import annotations

import json
import sys
from typing import Any

from mcp import types

from mcp_tools._context import MCPContext

TOOL = types.Tool(
    name="lazyown_lazymode_playbook",
    description=(
        "List or run lazymode exploit playbooks (per-vector paths such as "
        "vsftpd or samba, managed in playbooks/). action=list returns the "
        "available playbooks; action=run executes one against a target and "
        "returns {ok, steps:[{ok, result, ...}]}. Exploit success is in "
        "each step's result.session_opened, not the step ok flag."
    ),
    inputSchema={
        "type": "object",
        "properties": {
            "action": {
                "type": "string",
                "enum": ["list", "run"],
                "description": "list the playbooks or run one.",
            },
            "name": {
                "type": "string",
                "description": "Playbook file name or declared name (action=run).",
            },
            "target": {
                "type": "string",
                "description": "Host to run the playbook against (action=run).",
            },
            "timeout": {
                "type": "number",
                "description": "Per-step wall-clock override in seconds (action=run).",
            },
        },
    },
)


def handle(arguments: dict[str, Any], tool_name: str, ctx: MCPContext) -> list:
    """List lazymode playbooks or run one, returning JSON text.

    Args:
        arguments: Tool arguments; ``action`` and, for run, ``name``,
            ``target`` and optional ``timeout``.
        tool_name: The dispatched tool name for the text envelope.
        ctx: Injected runtime helpers.

    Returns:
        A one-element ``TextContent`` list with the list or run result.
    """
    if str(ctx.lazyown_dir) not in sys.path:
        sys.path.insert(0, str(ctx.lazyown_dir))
    from modules.lazymode_playbook import list_vector_playbooks, run_playbook

    action = str(arguments.get("action", "list")).strip().lower()
    if action == "run":
        name = str(arguments.get("name", "")).strip()
        if not name:
            return ctx.text(tool_name, "error: name is required for action=run")
        target = str(arguments.get("target", "")).strip() or None
        timeout = arguments.get("timeout")
        outcome = run_playbook(
            name, target=target, timeout=float(timeout) if timeout is not None else None
        )
        return ctx.text(tool_name, json.dumps(outcome, indent=2))
    return ctx.text(tool_name, json.dumps(list_vector_playbooks(), indent=2))
