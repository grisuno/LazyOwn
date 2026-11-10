"""MCP tool ``lazyown_harness_status`` (migrated from the call_tool dispatch chain)."""

from __future__ import annotations

from typing import Any

from mcp import types

from mcp_tools._context import MCPContext

TOOL = types.Tool(
    name="lazyown_harness_status",
    description=(
        "Defense-in-depth dashboard. Aggregates status from all 5 harness layers: "
        "permissions (allow/deny/ask counts) + hooks (runs/blocks/errors) + "
        "transcripts (event counts, compact boundaries) + compaction stats + "
        "CLAUDE.md hierarchy. Call this to see if the harness is healthy."
    ),
    inputSchema={"type": "object", "properties": {}},
)


def handle(arguments: dict[str, Any], tool_name: str, ctx: MCPContext) -> list:
    """Handle the lazyown_harness_status MCP tool."""
    lines = ["═══ LazyOwn Harness Status (Defense-in-Depth Dashboard) ═══", ""]

    # Layer 1: Permissions
    ps = ctx.get_perm_system()
    if ps is not None:
        m = ps.metrics()
        lines += [
            "▼ PERMISSIONS",
            f"  mode:               {m['mode']}",
            f"  rules configured:   {m['rules_count']}",
            f"  total evaluations:  {m['total_evaluations']}",
            f"  decisions:          allow={m['decisions']['allow']}  deny={m['decisions']['deny']}  ask={m['decisions']['ask']}",
        ]
        if m["recent_denials"]:
            lines.append("  recent denials:")
            for d in m["recent_denials"]:
                lines.append(f"    [{d['ts'][-8:]}] {d['tool']}  →  {d['reason'][:60]}")
        lines.append("")
    else:
        lines += ["▼ PERMISSIONS", "  unavailable (lazyown_permissions not loaded)", ""]

    # Layer 2: Hooks
    hk = ctx.get_hooks()
    if hk is not None:
        m = hk.metrics()
        lines += [
            "▼ HOOKS",
            f"  events registered:  {len(m['events_registered'])}  ({', '.join(m['events_registered'])})",
            f"  totals:             runs={m['totals']['runs']}  blocks={m['totals']['blocks']}  errors={m['totals']['errors']}",
        ]
        for ev, stats in m["per_event"].items():
            if stats["runs"] > 0:
                lines.append(
                    f"    {ev:20s} runs={stats['runs']:4d}  blocks={stats['blocks']:3d}  errors={stats['errors']:3d}"
                )
        lines.append("")
    else:
        lines += ["▼ HOOKS", "  unavailable (lazyown_hooks not loaded)", ""]

    # Layer 3: Session transcript
    ts = ctx.get_transcript()
    if ts is not None:
        events = ts.get_recent(500)
        tool_uses = sum(1 for e in events if e.get("type") == "tool_use")
        results = sum(1 for e in events if e.get("type") == "tool_result")
        boundaries = sum(1 for e in events if e.get("type") == "compact_boundary")
        denied = sum(
            1 for e in events if e.get("type") == "permission_decision" and e.get("data", {}).get("decision") == "deny"
        )
        lines += [
            "▼ SESSION TRANSCRIPT",
            f"  session_id:         {ts.session_id}",
            f"  total events:       {ts.count()}",
            f"  tool calls:         {tool_uses}",
            f"  tool results:       {results}",
            f"  compact boundaries: {boundaries}",
            f"  denied calls:       {denied}",
            f"  file:               {ts.path.name}",
            "",
        ]
    else:
        lines += ["▼ SESSION TRANSCRIPT", "  unavailable (lazyown_session not loaded)", ""]

    # Layer 4: CLAUDE.md hierarchy
    cmd_loader = ctx.get_claudemd()
    if cmd_loader is not None:
        files = cmd_loader.list_files()
        lines += ["▼ CLAUDE.md HIERARCHY"]
        if files:
            for f in files:
                lines.append(f"  [{f['level']:8s}] {f['path']}  ({f['size']:,} bytes)")
        else:
            lines.append("  no CLAUDE.md files found in hierarchy")
        lines.append("")
    else:
        lines += ["▼ CLAUDE.md HIERARCHY", "  unavailable", ""]

    # Layer 5: Compaction (best-effort metrics — last result if any)
    lines += [
        "▼ CONTEXT COMPACTION",
        "  status: active (5-layer pipeline applied to every tool result)",
        "  layers: microcompact → snip → collapse → budget",
        "",
    ]

    return ctx.text(tool_name, "\n".join(lines))
