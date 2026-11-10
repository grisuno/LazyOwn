"""MCP tool ``lazyown_manage_permissions`` (migrated from the call_tool dispatch chain)."""

from __future__ import annotations

import json
from typing import Any

from mcp import types

from mcp_tools._context import MCPContext

TOOL = types.Tool(
    name="lazyown_manage_permissions",
    description=(
        "View or modify the LazyOwn permission system. "
        "Actions: status | set_mode | add_rule | remove_rule | list_rules. "
        "Modes: default | dont_ask | bypass_permissions | plan. "
        "Rule actions: allow | deny | ask. "
        "Example: add allow rule for 'lazyown_run_command' so it never asks."
    ),
    inputSchema={
        "type": "object",
        "properties": {
            "action": {
                "type": "string",
                "description": "status | set_mode | add_rule | remove_rule | list_rules",
                "enum": ["status", "set_mode", "add_rule", "remove_rule", "list_rules"],
            },
            "mode": {
                "type": "string",
                "description": "Permission mode (for set_mode action).",
            },
            "tool_pattern": {
                "type": "string",
                "description": "Glob pattern for tool name (for add_rule/remove_rule).",
            },
            "rule_action": {
                "type": "string",
                "description": "allow | deny | ask (for add_rule).",
            },
            "condition": {
                "type": "string",
                "description": "Optional condition: 'contains:<text>' or 'target:<glob>'.",
            },
            "description": {
                "type": "string",
                "description": "Human note for the rule.",
                "default": "",
            },
        },
        "required": ["action"],
    },
)


def handle(arguments: dict[str, Any], tool_name: str, ctx: MCPContext) -> list:
    """Handle the lazyown_manage_permissions MCP tool."""
    action = arguments.get("action", "status")
    perm_sys = ctx.get_perm_system()
    if perm_sys is None:
        return ctx.text(tool_name, "Permission system unavailable (lazyown_permissions.py not found).")

    if action == "status":
        return ctx.text(tool_name, perm_sys.status_text())

    if action == "set_mode":
        mode = arguments.get("mode", "")
        if not mode:
            return ctx.text(tool_name, "'mode' parameter required for set_mode action.")
        try:
            return ctx.text(tool_name, perm_sys.set_mode(mode))
        except ValueError as e:
            return ctx.text(
                tool_name,
                f"Invalid mode: {e}\nValid: plan | default | accept_edits | auto | dont_ask | bypass_permissions",
            )

    if action == "add_rule":
        tp = arguments.get("tool_pattern", "")
        ra = arguments.get("rule_action", "")
        if not tp or not ra:
            return ctx.text(tool_name, "'tool_pattern' and 'rule_action' required for add_rule.")
        result = perm_sys.add_rule(
            tool_pattern=tp,
            action=ra,
            condition=arguments.get("condition"),
            description=arguments.get("description", ""),
        )
        return ctx.text(tool_name, result)

    if action == "remove_rule":
        tp = arguments.get("tool_pattern", "")
        ra = arguments.get("rule_action", "")
        if not tp or not ra:
            return ctx.text(tool_name, "'tool_pattern' and 'rule_action' required for remove_rule.")
        return ctx.text(tool_name, perm_sys.remove_rule(tp, ra))

    if action == "list_rules":
        rules = perm_sys.list_rules()
        if not rules:
            return ctx.text(tool_name, "No rules configured.")
        return ctx.text(tool_name, json.dumps(rules, indent=2))

    return ctx.text(tool_name, f"Unknown action: {action}")
