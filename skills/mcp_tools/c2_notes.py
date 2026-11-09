"""MCP tool ``lazyown_c2_notes`` (migrated from the call_tool dispatch chain)."""

from __future__ import annotations

import json
import os
from typing import Any

from mcp import types
from mcp_tools._context import MCPContext

TOOL = types.Tool(
    name="lazyown_c2_notes",
    description=(
        "Read, append, or clear the operational notes stored in sessions/sessionLazyOwn.json. "
        "Notes are the operator's running commentary — tactical observations, context, "
        "pivot ideas, and handoff messages for the next shift. "
        "actions: 'read' (default) | 'append' (adds a timestamped note) | 'clear'"
    ),
    inputSchema={
        "type": "object",
        "properties": {
            "action": {
                "type": "string",
                "enum": ["read", "append", "clear"],
                "default": "read",
            },
            "note": {
                "type": "string",
                "description": "Note text to append (required for action=append).",
            },
        },
        "required": [],
    },
)


def handle(arguments: dict[str, Any], tool_name: str, ctx: MCPContext) -> list:
    """Handle the lazyown_c2_notes MCP tool."""
    action = arguments.get("action", "read")
    sj_file = ctx.sessions_dir / "sessionLazyOwn.json"
    try:
        sj = json.loads(sj_file.read_text()) if sj_file.exists() else {}
    except Exception:
        sj = {}
    if action == "read":
        notes = sj.get("notes") or "(no notes)"
        return ctx.text(tool_name, f"Operational notes:\n{notes}")
    elif action == "append":
        note_text = arguments.get("note", "").strip()
        if not note_text:
            return ctx.text(tool_name, "note parameter required for action=append")
        ts = __import__("datetime").datetime.now().isoformat(timespec="seconds")
        existing = sj.get("notes") or ""
        sj["notes"] = (existing + f"\n[{ts}] {note_text}").strip()
        ctx.sessions_dir.mkdir(parents=True, exist_ok=True)
        try:
            os.chmod(ctx.sessions_dir, 0o700)
        except OSError:
            pass
        sj_file.write_text(json.dumps(sj, indent=4, ensure_ascii=False))
        try:
            os.chmod(sj_file, 0o600)
        except OSError:
            pass
        return ctx.text(tool_name, f"Note appended at {ts}.")
    elif action == "clear":
        sj["notes"] = ""
        sj_file.write_text(json.dumps(sj, indent=4, ensure_ascii=False))
        try:
            os.chmod(sj_file, 0o600)
        except OSError:
            pass
        return ctx.text(tool_name, "Notes cleared.")
    return ctx.text(tool_name, f"Unknown action: {action}")
