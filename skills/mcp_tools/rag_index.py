"""MCP tool ``lazyown_rag_index`` (migrated from the call_tool dispatch chain)."""

from __future__ import annotations

import asyncio
import sys
from typing import Any

from mcp import types
from mcp_tools._context import MCPContext

TOOL = types.Tool(
    name="lazyown_rag_index",
    description=(
        "Incrementally index all sessions/ artefacts (*.log, *.txt, *.csv, *.xml, "
        "*.json, *.nmap, *.md) into the ChromaDB semantic store. "
        "Only new or changed files are processed — safe to call from cron. "
        "mode='incremental' (default) indexes only new/changed files. "
        "mode='full' rebuilds the entire index from scratch. "
        "Returns: {files: N, chunks: N} counts."
    ),
    inputSchema={
        "type": "object",
        "properties": {
            "mode": {
                "type": "string",
                "enum": ["incremental", "full"],
                "description": "Indexing mode.",
                "default": "incremental",
            },
        },
        "required": [],
    },
)


async def handle(arguments: dict[str, Any], tool_name: str, ctx: MCPContext) -> list:
    """Handle the lazyown_rag_index MCP tool."""
    rag_mode = arguments.get("mode", "incremental")
    try:
        sys.path.insert(0, str(ctx.modules_dir))
        from session_rag import get_rag as _get_rag

        _rag = _get_rag()
        if rag_mode == "full":
            result_counts = await asyncio.get_event_loop().run_in_executor(None, _rag.index_all)
        else:
            result_counts = await asyncio.get_event_loop().run_in_executor(None, _rag.index_new)
        # Also index knowledge-base parquets (techniques, binarios, lolbas)
        pq_counts = await asyncio.get_event_loop().run_in_executor(
            None, lambda: _rag.index_parquet_sources(force=(rag_mode == "full"))
        )
        stats = _rag.stats()
        lines = [
            f"RAG index ({rag_mode}): {result_counts['files']} session files, {result_counts['chunks']} new chunks",
            f"  + parquets:     {pq_counts['files']} KB files, {pq_counts['chunks']} new chunks",
            f"Backend:        {stats['backend']}",
            f"Indexed files:  {stats['indexed_files']}",
            f"Total chunks:   {stats['total_chunks']}",
        ]
        if not stats["chroma_ok"]:
            lines.append(
                "Note: chromadb not installed — using keyword fallback. For semantic search: pip install chromadb"
            )
        return ctx.text(tool_name, "\n".join(lines))
    except Exception as exc:
        return ctx.text(tool_name, f"[rag_index error] {exc}")
