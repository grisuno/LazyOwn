"""MCP tool ``lazyown_claudemd`` (migrated from the call_tool dispatch chain)."""

from __future__ import annotations

from typing import Any

from mcp import types

from mcp_tools._context import MCPContext

TOOL = types.Tool(
    name="lazyown_claudemd",
    description=(
        "Manage LazyOwn's CLAUDE.md instruction hierarchy (4 levels: "
        "managed → user → project → local). "
        "Actions: status | load | create_user | create_project | create_local | add_rule. "
        "Files are merged in priority order on each session start."
    ),
    inputSchema={
        "type": "object",
        "properties": {
            "action": {
                "type": "string",
                "description": "status | load | create_user | create_project | create_local | add_rule",
                "enum": ["status", "load", "create_user", "create_project", "create_local", "add_rule"],
            },
            "content": {
                "type": "string",
                "description": "File content (for create_* / add_rule actions).",
                "default": "",
            },
            "rule_name": {
                "type": "string",
                "description": "Rule file name without extension (for add_rule).",
                "default": "",
            },
        },
        "required": ["action"],
    },
)


def handle(arguments: dict[str, Any], tool_name: str, ctx: MCPContext) -> list:
    """Handle the lazyown_claudemd MCP tool."""
    action = arguments.get("action", "status")
    loader = ctx.get_claudemd()
    if loader is None:
        return ctx.text(tool_name, "ClaudeMdLoader unavailable (lazyown_claudemd.py not found).")

    if action == "status":
        return ctx.text(tool_name, loader.status_text())

    if action == "load":
        merged = loader.load()
        if not merged:
            return ctx.text(tool_name, "No CLAUDE.md files found in hierarchy.")
        return ctx.text(tool_name, merged)

    if action == "create_user":
        content = arguments.get("content", "")
        if not content:
            return ctx.text(tool_name, "'content' parameter required.")
        return ctx.text(tool_name, loader.create_user_file(content))

    if action == "create_project":
        content = arguments.get("content", "")
        if not content:
            return ctx.text(tool_name, "'content' parameter required.")
        return ctx.text(tool_name, loader.create_project_file(content, local=False))

    if action == "create_local":
        content = arguments.get("content", "")
        if not content:
            return ctx.text(tool_name, "'content' parameter required.")
        return ctx.text(tool_name, loader.create_project_file(content, local=True))

    if action == "add_rule":
        rule_name = arguments.get("rule_name", "").strip()
        content = arguments.get("content", "")
        if not rule_name or not content:
            return ctx.text(tool_name, "'rule_name' and 'content' required for add_rule.")
        return ctx.text(tool_name, loader.add_rule(rule_name, content))

    return ctx.text(tool_name, f"Unknown action: {action}")
