"""MCP tool ``lazyown_get_llm_budget``: read the LLM cost budget status."""

from __future__ import annotations

import json
from typing import Any

from mcp import types

from mcp_tools._context import MCPContext

TOOL = types.Tool(
    name="lazyown_get_llm_budget",
    description=(
        "Read the LLM daily cost budget, per call token cap, and "
        "current spend the proxy recorded. Returns a structured "
        "JSON object with limit_usd, spent_usd, remaining_usd, "
        "calls_today, per_call_token_cap, model_prices, and "
        "ledger_path. Use this to surface a daily cap to the "
        "operator before scheduling an LLM heavy autonomous loop."
    ),
    inputSchema={"type": "object", "properties": {}},
)


def handle(arguments: dict[str, Any], tool_name: str, ctx: MCPContext) -> list:
    """Return the LLM budget status, or an unavailable marker on failure."""
    try:
        from core.llm_budget import read_budget_status
    except Exception as error:
        return ctx.text(
            tool_name,
            json.dumps({"available": False, "reason": f"llm_budget module not importable: {error}"}),
        )
    try:
        budget = read_budget_status(ctx.lazyown_dir)
        return ctx.text(
            tool_name,
            json.dumps(
                {
                    "available": True,
                    "budget": budget.to_dict() if hasattr(budget, "to_dict") else budget,
                }
            ),
        )
    except Exception as error:
        return ctx.text(tool_name, json.dumps({"available": False, "reason": f"Budget read failed: {error}"}))
