"""MCP tool ``lazyown_session_resume`` (migrated from the call_tool dispatch chain)."""

from __future__ import annotations

from typing import Any

from mcp import types

from mcp_tools._context import MCPContext

TOOL = types.Tool(
    name="lazyown_session_resume",
    description=(
        "Reconstruct context from an append-only session transcript. "
        "Returns: event counts, recent tool calls, key findings, "
        "permission decisions, and compact boundaries. Use to pick up "
        "where a previous session left off."
    ),
    inputSchema={
        "type": "object",
        "properties": {
            "session_id": {
                "type": "string",
                "description": "Transcript session_id (12-char). Empty = current active session.",
                "default": "",
            },
            "limit": {
                "type": "integer",
                "description": "Max recent events to summarize (default 50).",
                "default": 50,
            },
        },
    },
)


def handle(arguments: dict[str, Any], tool_name: str, ctx: MCPContext) -> list:
    """Handle the lazyown_session_resume MCP tool."""
    sid = arguments.get("session_id", "").strip()
    limit = int(arguments.get("limit", 50))

    try:
        from lazyown_session import SessionTranscript
    except ImportError:
        return ctx.text(tool_name, "lazyown_session module not available.")

    if sid:
        ts_obj = SessionTranscript(ctx.sessions_dir, sid)
    else:
        ts_obj = ctx.get_transcript()
        if ts_obj is None:
            return ctx.text(tool_name, "No active transcript and no session_id provided.")

    events = ts_obj.get_recent(limit)
    if not events:
        return ctx.text(tool_name, f"Session {ts_obj.session_id}: no events found.")

    # Aggregate
    tool_calls: list[str] = []
    tool_results: list[str] = []
    denials: list[str] = []
    boundaries: list[str] = []
    for e in events:
        t = e.get("type", "")
        d = e.get("data", {})
        ts_str = e.get("ts", "")[-8:]
        if t == "tool_use":
            tool = d.get("tool_name", "?")
            args_str = str(d.get("arguments", {}))[:60]
            tool_calls.append(f"  [{ts_str}] {tool}  {args_str}")
        elif t == "tool_result":
            tool = d.get("tool_name", "?")
            preview = (d.get("content", "") or "")[:80].replace("\n", " ")
            tool_results.append(f"  [{ts_str}] {tool}  →  {preview}")
        elif t == "compact_boundary":
            summary = d.get("summary", "")[:80]
            boundaries.append(f"  [{ts_str}] {summary}")
        elif t == "permission_decision":
            if d.get("decision") == "deny":
                denials.append(f"  [{ts_str}] {d.get('tool_name', '?')} → {d.get('reason', '')[:60]}")

    lines = [
        f"═══ Session Resume: {ts_obj.session_id} ═══",
        f"  total events: {ts_obj.count()}  (showing last {len(events)})",
        f"  transcript:   {ts_obj.path}",
        "",
        f"▼ Tool calls ({len(tool_calls)}):",
        *tool_calls[-10:],
        "",
        f"▼ Tool results ({len(tool_results)}):",
        *tool_results[-10:],
    ]
    if boundaries:
        lines += ["", f"▼ Compact boundaries ({len(boundaries)}):", *boundaries[-3:]]
    if denials:
        lines += ["", f"▼ Permission denials ({len(denials)}):", *denials[-5:]]
    lines += ["", "Use lazyown_run_command or lazyown_subagent_run to continue from this state."]
    return ctx.text(tool_name, "\n".join(lines))
