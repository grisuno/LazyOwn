"""MCP tool ``lazyown_rag_query`` (migrated from the call_tool dispatch chain)."""

from __future__ import annotations

import asyncio
import sys
from typing import Any

from mcp import types
from mcp_tools._context import MCPContext

TOOL = types.Tool(
    name="lazyown_rag_query",
    description=(
        "Semantic search over indexed sessions/ artefacts. "
        "Returns the top-n most relevant chunks from logs, scan results, "
        "credential files, and other session data. "
        "Falls back to keyword search when ChromaDB is not available. "
        "Install ChromaDB for full semantic search: pip install chromadb"
    ),
    inputSchema={
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "Natural language query.",
            },
            "n": {
                "type": "integer",
                "description": "Number of results to return.",
                "default": 5,
            },
        },
        "required": ["query"],
    },
)


async def handle(arguments: dict[str, Any], tool_name: str, ctx: MCPContext) -> list:
    """Handle the lazyown_rag_query MCP tool."""
    rq_query = arguments.get("query", "").strip()
    rq_n = int(arguments.get("n", 5))
    if not rq_query:
        return ctx.text(tool_name, "[rag_query] 'query' is required.")
    try:
        sys.path.insert(0, str(ctx.modules_dir))
        from session_rag import get_rag as _get_rag

        _rag = _get_rag()
        # Trigger incremental index first so newly created files are visible
        await asyncio.get_event_loop().run_in_executor(None, _rag.index_new)
        hits = await asyncio.get_event_loop().run_in_executor(None, lambda: _rag.query(rq_query, rq_n))
        if not hits:
            return ctx.text(tool_name, "No results found. Run lazyown_rag_index first.")
        lines = [f"RAG query: '{rq_query}'  ({len(hits)} hits)\n"]
        for i, h in enumerate(hits, 1):
            score_str = f"  score={h['score']:.3f}" if h["score"] is not None else ""
            lines.append(f"{i}. [{h['source']}]{score_str}")
            lines.append(h["text"].strip()[:300])
            lines.append("")
        return ctx.text(tool_name, "\n".join(lines))
    except Exception as exc:
        return ctx.text(tool_name, f"[rag_query error] {exc}")
