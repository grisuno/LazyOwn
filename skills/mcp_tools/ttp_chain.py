"""MCP tool ``lazyown_ttp_chain`` (migrated from the call_tool dispatch chain)."""

from __future__ import annotations

import json
import sys
from typing import Any

from mcp import types
from mcp_tools._context import MCPContext

TOOL = types.Tool(
    name="lazyown_ttp_chain",
    description=(
        "Build an ordered APT emulation plan from MITRE technique IDs. "
        "Each technique is resolved to its first platform-compatible "
        "Atomic Red Team test (GUID + command preview) and enriched "
        "with TTPScope/parquet context. The plan is staged to "
        "sessions/ttp_chain_<ts>.json for the autonomous loop. "
        "Read-only: nothing is executed on any target. "
        "Example: techniques=['T1003','T1059.001'] platform='windows'."
    ),
    inputSchema={
        "type": "object",
        "properties": {
            "techniques": {
                "type": "array",
                "items": {"type": "string"},
                "description": "Ordered MITRE technique IDs (max 20).",
            },
            "platform": {
                "type": "string",
                "description": "Target platform for every step.",
                "default": "linux",
            },
            "limit": {
                "type": "integer",
                "description": "Max context hits per technique (default 3, max 10).",
                "default": 3,
            },
        },
        "required": ["techniques"],
    },
)


def handle(arguments: dict[str, Any], tool_name: str, ctx: MCPContext) -> list:
    """Handle the lazyown_ttp_chain MCP tool."""
    tc_techs = arguments.get("techniques", [])
    tc_platform = (arguments.get("platform", "linux") or "linux").strip().lower()
    tc_limit = max(1, min(int(arguments.get("limit", 3)), 10))
    if not isinstance(tc_techs, list) or not tc_techs:
        return ctx.text(tool_name, "[ttp_chain] 'techniques' must be a non-empty array of MITRE IDs.")
    if len(tc_techs) > 20:
        return ctx.text(tool_name, "[ttp_chain] Max 20 techniques per chain.")
    if tc_platform not in ("linux", "windows", "macos"):
        return ctx.text(tool_name, "[ttp_chain] platform must be linux | windows | macos.")
    try:
        sys.path.insert(0, str(ctx.modules_dir))
        from atomic_resolver import get_resolver
        from ttpscope_bridge import do_chain

        resolver = get_resolver()
        plan: list[dict[str, Any]] = []
        for raw in tc_techs:
            tid = str(raw).strip().upper()
            step: dict[str, Any] = {"technique_id": tid, "atomic": None, "context_staged": ""}
            try:
                candidates = resolver.list_for_technique(tid, platform=tc_platform)
            except ValueError:
                candidates = []
            if candidates:
                first = candidates[0]
                step["atomic"] = {
                    "guid": first.guid,
                    "name": first.name,
                    "command_preview": first.command[:300],
                    "cleanup_preview": first.cleanup_command[:200],
                    "mitre_url": first.mitre_url,
                    "stage_cmd": f"atomic_gen {first.guid}",
                }
            try:
                ctx = do_chain(tid, platform=tc_platform, limit=tc_limit)
                step["context_staged"] = ctx.get("staged", "")
            except Exception as exc:
                step["context_error"] = str(exc)[:200]
            plan.append(step)
        import datetime as _dt

        stamp = _dt.datetime.now(_dt.UTC).strftime("%Y%m%d_%H%M%S")
        out_path = ctx.sessions_dir / f"ttp_chain_{tc_platform}_{stamp}.json"
        out_path.write_text(
            json.dumps(
                {"platform": tc_platform, "generated_at": stamp, "steps": plan},
                indent=2,
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )
        covered = sum(1 for s in plan if s["atomic"] is not None)
        lines = [f"TTP chain ({tc_platform}): {covered}/{len(plan)} techniques resolved\n"]
        for i, s in enumerate(plan, 1):
            if s["atomic"]:
                lines.append(f"{i}. [{s['technique_id']}] {s['atomic']['name']}")
                lines.append(f"   guid: {s['atomic']['guid']}")
                lines.append(f"   stage: {s['atomic']['stage_cmd']}")
            else:
                lines.append(f"{i}. [{s['technique_id']}] NO atomic test on {tc_platform} — skipped")
        lines.append("")
        lines.append(f"Plan staged: {out_path}")
        lines.append("Emulate step-by-step with atomic_gen <guid>, or run the plan via attack_plan.")
        return ctx.text(tool_name, "\n".join(lines))
    except Exception as exc:
        return ctx.text(tool_name, f"[ttp_chain error] {exc}")
