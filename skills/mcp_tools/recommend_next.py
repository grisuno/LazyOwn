"""MCP tool ``lazyown_recommend_next`` (migrated from the call_tool dispatch chain)."""

from __future__ import annotations

import asyncio
import os
from typing import Any

from mcp import types

from mcp_tools._context import MCPContext

TOOL = types.Tool(
    name="lazyown_recommend_next",
    description=(
        "Ask the AI (Groq) to recommend the best 3-5 LazyOwn commands to run next, "
        "ranked by confidence, based on the current session state (phase, findings, creds). "
        "Returns command names, optional args, confidence score, and one-line reasoning. "
        "Requires api_key set in payload.json."
    ),
    inputSchema={"type": "object", "properties": {}},
)


async def handle(arguments: dict[str, Any], tool_name: str, ctx: MCPContext) -> list:
    """Handle the lazyown_recommend_next MCP tool."""
    cfg = ctx.load_payload()
    target = cfg.get("rhost", "") or cfg.get("lhost", "127.0.0.1")
    lines: list[str] = []

    # Layer 1 — unified engine: fused policy + recon + graph + kill-chain
    def _fused_recommendations() -> list:
        from cli.recommendation import KIND_CATEGORY
        from cli.recommendation_signals import build_context, build_default_engine

        engine = build_default_engine(payload=cfg)
        rec_ctx = build_context(cfg, target=target, limit=8)
        out: list[str] = []
        recs = engine.recommend(rec_ctx)
        if recs:
            out.append(f"[Engine] Fused next-best actions for {target}:")
            for i, rec in enumerate(recs, 1):
                bar = "█" * int(min(rec.score, 1.0) * 10)
                tag = "category" if rec.kind == KIND_CATEGORY else rec.kind
                out.append(f"  {i}. [{bar:<10}] {rec.action}  [{tag} · {', '.join(rec.sources)}]")
                for reason in rec.reasons:
                    out.append(f"       {reason}")
                if rec.command_preview:
                    out.append(f"       $ {rec.command_preview}")
            out.append("")
        return out

    lines.extend(await asyncio.get_event_loop().run_in_executor(None, _fused_recommendations))

    # Layer 2 — LLM recommender: specific commands with arguments
    try:
        from recommender import recommend_and_save as _recommend
    except Exception:
        _recommend = None
    if _recommend is not None:
        api_key = cfg.get("api_key", "") or os.environ.get("GROQ_API_KEY", "")
        llm_recs = await asyncio.get_event_loop().run_in_executor(None, lambda: _recommend(api_key))
        if llm_recs and not (len(llm_recs) == 1 and llm_recs[0].get("command") in ("_error", "_unavailable")):
            via = llm_recs[0].get("_via", "")
            header = "[LLM] Specific commands"
            if via:
                header += f" (via {via})"
            lines.append(header + ":")
            for i, r in enumerate(llm_recs, 1):
                bar = "█" * int(r["confidence"] * 10)
                cmd = r["command"]
                args = f" {r['args']}" if r.get("args") else ""
                lines.append(f"  {i}. [{bar:<10}] {r['confidence']:.0%}  {cmd}{args}")
                lines.append(f"       {r['reason']}")
            lines.append("\nSaved to: sessions/recommendations/next_actions.json")

    if not lines:
        return ctx.text(tool_name, "No recommendations available — run bootstrap first or install recommender module.")
    return ctx.text(tool_name, "\n".join(lines))
