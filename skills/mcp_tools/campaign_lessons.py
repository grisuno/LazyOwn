"""MCP tool ``lazyown_campaign_lessons`` (migrated from the call_tool dispatch chain)."""

from __future__ import annotations

import json
from typing import Any

from mcp import types
from mcp_tools._context import MCPContext

TOOL = types.Tool(
    name="lazyown_campaign_lessons",
    description=(
        "Read campaign lessons derived from completed objectives. "
        "Lessons are tactical insights written to sessions/campaign_lessons.jsonl "
        "at each milestone. Each lesson has: campaign_id, topic, lesson text, context, timestamp. "
        "topics: intrusion, privesc, lateral, cred, scope_coverage, campaign_duration, other. "
        "Use these to avoid repeating mistakes and carry forward winning techniques."
    ),
    inputSchema={
        "type": "object",
        "properties": {
            "topic": {
                "type": "string",
                "description": "Filter by topic (optional). Leave empty for all lessons.",
                "default": "",
            },
            "last_n": {
                "type": "integer",
                "description": "Return only the last N lessons (default 20).",
                "default": 20,
            },
        },
        "required": [],
    },
)


def handle(arguments: dict[str, Any], tool_name: str, ctx: MCPContext) -> list:
    """Handle the lazyown_campaign_lessons MCP tool."""
    topic_filter = arguments.get("topic", "").strip()
    last_n = int(arguments.get("last_n", 20))
    lessons_file = ctx.sessions_dir / "campaign_lessons.jsonl"
    if not lessons_file.exists():
        return ctx.text(tool_name, "No campaign lessons found. Run a campaign with milestones to generate lessons.")
    try:
        lessons = [json.loads(line) for line in lessons_file.read_text().splitlines() if line.strip()]
    except Exception as e:
        return ctx.text(tool_name, f"Error reading lessons: {e}")
    if topic_filter:
        lessons = [lesson for lesson in lessons if lesson.get("topic", "") == topic_filter]
    lessons = lessons[-last_n:]
    if not lessons:
        return ctx.text(tool_name, f"No lessons found{' for topic=' + topic_filter if topic_filter else ''}.")
    lines = [f"Campaign lessons ({len(lessons)} entries):", ""]
    for les in lessons:
        lines.append(
            f"[{les.get('campaign_name', '?')}] [{les.get('topic', '?')}] {les.get('derived_at', '')[:10]}\n"
            f"  {les.get('lesson', '')}\n"
            f"  ctx: {les.get('context', '')}\n"
        )
    return ctx.text(tool_name, "\n".join(lines))
