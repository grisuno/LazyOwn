"""MCP tool ``lazyown_eval_quality`` (migrated from the call_tool dispatch chain)."""

from __future__ import annotations

import asyncio
import sys
from typing import Any

from mcp import types
from mcp_tools._context import MCPContext

TOOL = types.Tool(
    name="lazyown_eval_quality",
    description=(
        "Show LLM decision quality report: success rate, top/worst MITRE tactics, "
        "confidence calibration. Helps identify where the auto_loop makes poor choices. "
        "Optionally export a fine-tuning dataset from successful decisions."
    ),
    inputSchema={
        "type": "object",
        "properties": {
            "session_id": {
                "type": "string",
                "description": "Filter to a specific session (default: all sessions).",
                "default": "",
            },
            "export_dataset": {
                "type": "boolean",
                "description": "Export fine-tuning JSONL to sessions/finetuning_dataset.jsonl.",
                "default": False,
            },
        },
        "required": [],
    },
)


async def handle(arguments: dict[str, Any], tool_name: str, ctx: MCPContext) -> list:
    """Handle the lazyown_eval_quality MCP tool."""
    eq_session = arguments.get("session_id", "").strip() or None
    eq_export = bool(arguments.get("export_dataset", False))
    try:
        sys.path.insert(0, str(ctx.lazyown_dir / "modules"))
        from llm_evaluator import get_evaluator

        ev = get_evaluator()
        report = ev.quality_report(session_id=eq_session)
        if eq_export:
            out_path = ctx.lazyown_dir / "sessions" / "finetuning_dataset.jsonl"
            exported = await asyncio.get_event_loop().run_in_executor(
                None, lambda: ev.export_finetuning_dataset(out_path)
            )
            report += f"\n\nFine-tuning dataset exported: {exported}"
        return ctx.text(tool_name, report)
    except Exception as exc:
        return ctx.text(tool_name, f"[eval_quality error] {exc}")
