"""MCP tool ``lazyown_atomic_resolve`` (migrated from the call_tool dispatch chain)."""

from __future__ import annotations

import sys
from typing import Any

from mcp import types
from mcp_tools._context import MCPContext

TOOL = types.Tool(
    name="lazyown_atomic_resolve",
    description=(
        "Translate between MITRE ATT&CK IDs and Atomic Red Team tests. "
        "Accepts a technique ID (T1078, T1059.001), a prefix (T1059), "
        "or a test GUID, with optional platform filter. Returns concrete "
        "tests: GUID, name, platforms, MITRE URL, and command preview. "
        "Offline-first: reads the vendored Atomic repo, falling back to "
        "parquets/techniques_enriched.parquet. Never executes anything."
    ),
    inputSchema={
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "MITRE technique ID, prefix, or Atomic GUID (e.g. 'T1059.001', 'T1059', GUID).",
            },
            "platform": {
                "type": "string",
                "description": "Platform filter: linux | windows | macos | containers (default: all).",
                "default": "",
            },
            "limit": {
                "type": "integer",
                "description": "Max tests to return (default 10, max 30).",
                "default": 10,
            },
            "include_command": {
                "type": "boolean",
                "description": "Include command_preview (first 300 chars).",
                "default": False,
            },
        },
        "required": ["query"],
    },
)


def handle(arguments: dict[str, Any], tool_name: str, ctx: MCPContext) -> list:
    """Handle the lazyown_atomic_resolve MCP tool."""
    ar_query = arguments.get("query", "").strip()
    ar_platform = arguments.get("platform", "").strip()
    ar_limit = max(1, min(int(arguments.get("limit", 10)), 30))
    ar_incl_cmd = bool(arguments.get("include_command", False))
    if not ar_query:
        return ctx.text(tool_name, "[atomic_resolve] 'query' is required (TID, prefix, or GUID).")
    try:
        sys.path.insert(0, str(ctx.modules_dir))
        from atomic_resolver import get_resolver

        resolver = get_resolver()
        tests = resolver.resolve(ar_query, platform=ar_platform)[:ar_limit]
        if not tests and resolver.available:
            return ctx.text(
                tool_name,
                f"[atomic_resolve] No tests for '{ar_query}' "
                f"platform='{ar_platform or 'any'}'. Try a prefix (e.g. 'T1059') "
                f"or lazyown_atomic_search for broader filters.",
            )
        if not tests:
            sys.path.insert(0, str(ctx.modules_dir))
            from atomic_enricher import query_atomic as _qa

            rows = _qa(mitre_id=ar_query, platform=ar_platform, limit=ar_limit, include_command=ar_incl_cmd)
            if not rows:
                return ctx.text(
                    tool_name,
                    "[atomic_resolve] Atomic repo unavailable and no parquet "
                    "match. Run atomic_tests once to clone the repo, or "
                    "lazyown_atomic_search for keyword alternativas.",
                )
            lines = [f"Atomic resolve (parquet fallback): {len(rows)} results\n"]
            for r in rows:
                lines.append(f"{r['mitre_id']:12s}  {r['name']}")
                lines.append(f"  id: {r['id']}  platforms: {', '.join(r['platform_list'])}")
                if ar_incl_cmd and r.get("command_preview"):
                    lines.append(f"  command: {r['command_preview'][:150]}")
                lines.append("")
            return ctx.text(tool_name, "\n".join(lines))
        lines = [f"Atomic resolve '{ar_query}' platform='{ar_platform or 'any'}': {len(tests)} test(s)\n"]
        for t in tests:
            lines.append(f"[{t.mitre_id}] {t.name}")
            lines.append(f"  guid: {t.guid}")
            lines.append(f"  platforms: {', '.join(t.platforms)}")
            lines.append(f"  mitre_url: {t.mitre_url}")
            if ar_incl_cmd and t.command:
                lines.append(f"  command: {t.command[:150]}")
            lines.append("")
        lines.append("Stage one with: atomic_gen <guid>  (or atomic_tests <TID> --non-interactive)")
        return ctx.text(tool_name, "\n".join(lines))
    except ValueError as exc:
        return ctx.text(tool_name, f"[atomic_resolve] Invalid input: {exc}")
    except Exception as exc:
        return ctx.text(tool_name, f"[atomic_resolve error] {exc}")
