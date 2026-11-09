"""MCP tool ``lazyown_rich_tui_snapshot``: non-blocking Rich TUI snapshot."""

from __future__ import annotations

import json
from typing import Any

from mcp import types

from mcp_tools._context import MCPContext

_MAX_RECOMMENDATIONS = 10

TOOL = types.Tool(
    name="lazyown_rich_tui_snapshot",
    description=(
        "Generate a Rich TUI dashboard snapshot with network topology, "
        "host phases, exploit recommendations, active pivots, and beacons. "
        "Returns CLI status string, stats, text map, and ASCII topology. "
        "Non-blocking — does not launch the interactive TUI."
    ),
    inputSchema={
        "type": "object",
        "properties": {},
        "required": [],
    },
)


async def handle(arguments: dict[str, Any], tool_name: str, ctx: MCPContext) -> list:
    """Return a non-interactive snapshot of the Rich TUI dashboard as JSON."""
    try:
        from modules.dashboard_engine import DashboardEngine
        from modules.exploit_recommender import ExploitRecommender
        from modules.world_model import WorldModel

        wm = WorldModel(ctx.sessions_dir / "world_model.json")
        de = DashboardEngine(wm)
        de.set_exploit_recommender(ExploitRecommender(wm))
        snapshot = de.build_snapshot()
        return ctx.text(
            tool_name,
            json.dumps(
                {
                    "cli_status": de.format_for_cli(snapshot),
                    "stats": snapshot.get("stats", {}),
                    "text_map": de.render_text_map(snapshot),
                    "topology": de.render_ascii_topology(snapshot),
                    "recommendations": snapshot.get("recommendations", [])[:_MAX_RECOMMENDATIONS],
                },
                indent=2,
                ensure_ascii=False,
                default=str,
            ),
        )
    except Exception as exc:
        return ctx.text(tool_name, json.dumps({"error": str(exc)}, indent=2))
