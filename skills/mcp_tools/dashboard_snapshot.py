"""MCP tool ``lazyown_dashboard_snapshot``: render the live network map."""

from __future__ import annotations

import json
from typing import Any

from mcp import types

from mcp_tools._context import MCPContext


TOOL = types.Tool(
    name="lazyown_dashboard_snapshot",
    description=(
        "Generate a live network map dashboard showing all discovered "
        "hosts with phase status, exploit recommendations, active pivots, "
        "and beacon health. Returns both text map and ASCII topology."
    ),
    inputSchema={
        "type": "object",
        "properties": {},
        "required": [],
    },
)


async def handle(arguments: dict[str, Any], tool_name: str, ctx: MCPContext) -> list:
    """Build and persist a dashboard snapshot, returning map and topology."""
    try:
        from modules.dashboard_engine import DashboardEngine
        from modules.exploit_recommender import ExploitRecommender
        from modules.world_model import WorldModel

        wm = WorldModel(ctx.sessions_dir / "world_model.json")
        de = DashboardEngine(wm)
        de.set_exploit_recommender(ExploitRecommender(wm))
        snapshot = de.build_snapshot()
        text_map = de.render_text_map(snapshot)
        topology = de.render_ascii_topology(snapshot)
        de.persist_snapshot(snapshot)
        return ctx.text(tool_name, text_map + "\n\n" + topology)
    except Exception as exc:
        return ctx.text(tool_name, json.dumps({"error": str(exc)}, indent=2))
