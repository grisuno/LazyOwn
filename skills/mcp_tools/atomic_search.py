"""MCP tool ``lazyown_atomic_search`` (migrated from the call_tool dispatch chain)."""

from __future__ import annotations

import sys
from typing import Any

from mcp import types
from mcp_tools._context import MCPContext

TOOL = types.Tool(
    name="lazyown_atomic_search",
    description=(
        "Structured search over the 1690 Atomic Red Team technique tests "
        "(parquets/techniques_enriched.parquet). "
        "Supports simultaneous filtering by keyword, MITRE ID/prefix, platform, "
        "scope, prerequisites, and complexity. "
        "Returns id, name, mitre_id, platform_list, scope, complexity, "
        "has_prereqs, keyword_tags, description_preview — and optionally command_preview. "
        "Examples: keyword='bypass amsi' platform='windows'; "
        "mitre_id='T1548' platform='linux' complexity='low'; "
        "keyword='kerberos' no_prereqs=true."
    ),
    inputSchema={
        "type": "object",
        "properties": {
            "keyword": {
                "type": "string",
                "description": "Free-text search over name, description, tags.",
                "default": "",
            },
            "mitre_id": {
                "type": "string",
                "description": "MITRE technique ID or prefix (T1059, T1059.001, T1548.002).",
                "default": "",
            },
            "platform": {
                "type": "string",
                "description": "Target platform: linux | windows | macos | freebsd | cloud.",
                "default": "",
            },
            "scope": {
                "type": "string",
                "enum": ["", "local", "remote", "elevated", "any"],
                "description": "Execution scope.",
                "default": "",
            },
            "complexity": {
                "type": "string",
                "enum": ["", "low", "medium", "high"],
                "description": "Command complexity based on line count.",
                "default": "",
            },
            "has_prereqs": {
                "type": "boolean",
                "description": "true = only tests with prerequisites; false = no prereqs needed.",
            },
            "limit": {
                "type": "integer",
                "description": "Max results to return (default 10).",
                "default": 10,
            },
            "include_command": {
                "type": "boolean",
                "description": "Include command_preview (first 300 chars) in results.",
                "default": False,
            },
        },
        "required": [],
    },
)


def handle(arguments: dict[str, Any], tool_name: str, ctx: MCPContext) -> list:
    """Handle the lazyown_atomic_search MCP tool."""
    as_keyword = arguments.get("keyword", "").strip()
    as_mitre = arguments.get("mitre_id", "").strip()
    as_platform = arguments.get("platform", "").strip()
    as_scope = arguments.get("scope", "").strip()
    as_complexity = arguments.get("complexity", "").strip()
    as_has_prereqs = arguments.get("has_prereqs")  # None | True | False
    as_limit = int(arguments.get("limit", 10))
    as_incl_cmd = bool(arguments.get("include_command", False))
    if as_has_prereqs is not None:
        as_has_prereqs = bool(as_has_prereqs)
    if not any([as_keyword, as_mitre, as_platform, as_scope, as_complexity, as_has_prereqs is not None]):
        return ctx.text(
            tool_name,
            "[atomic_search] Provide at least one filter: keyword, mitre_id, "
            "platform, scope, complexity, or has_prereqs.",
        )
    try:
        sys.path.insert(0, str(ctx.modules_dir))
        from atomic_enricher import enrich as _enrich_atomic
        from atomic_enricher import query_atomic as _qa

        # Build enriched parquet on first use
        _enrich_atomic()
        rows = _qa(
            keyword=as_keyword,
            mitre_id=as_mitre,
            platform=as_platform,
            scope=as_scope,
            has_prereqs=as_has_prereqs,
            complexity=as_complexity,
            limit=as_limit,
            include_command=as_incl_cmd,
        )
        if not rows:
            return ctx.text(
                tool_name,
                f"[atomic_search] No results for: keyword='{as_keyword}' "
                f"mitre='{as_mitre}' platform='{as_platform}' scope='{as_scope}' "
                f"complexity='{as_complexity}'. Try broader filters.",
            )
        lines = [f"Atomic Red Team search: {len(rows)} results\n"]
        for r in rows:
            plat_str = ", ".join(r["platform_list"]) or "any"
            lines.append(f"{r['mitre_id']:12s}  [{r['complexity']:6s}] [{r['scope']:8s}]  {r['name']}")
            lines.append(f"  platforms: {plat_str}   prereqs: {r['has_prereqs']}")
            lines.append(f"  tags: {', '.join(r['keyword_tags'][:6])}")
            if as_incl_cmd and r.get("command_preview"):
                lines.append(f"  command: {r['command_preview'][:120]}")
            lines.append("")
        return ctx.text(tool_name, "\n".join(lines))
    except Exception as exc:
        return ctx.text(tool_name, f"[atomic_search error] {exc}")
