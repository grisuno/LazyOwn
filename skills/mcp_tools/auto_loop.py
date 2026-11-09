"""MCP tool ``lazyown_auto_loop`` (migrated from the call_tool dispatch chain)."""

from __future__ import annotations

from typing import Any

from mcp import types
from mcp_tools._context import MCPContext

TOOL = types.Tool(
    name="lazyown_auto_loop",
    description=(
        "Autonomous loop over the LazyOrchestrator engine (single orchestrator, "
        "same engine as the auto_loop CLI). Drive rounds, workers and a wall-clock "
        "timeout; the engine covers scope guards, budget, planner, chain steering "
        "and honest failure handling. The retired ad-hoc engine is gone: the "
        '"legacy" flag is accepted for compatibility and only annotates the output.'
    ),
    inputSchema={
        "type": "object",
        "properties": {
            "target": {
                "type": "string",
                "description": "Target IP or hostname. Defaults to rhost from payload.json.",
            },
            "objective": {
                "type": "string",
                "description": "Goal for the orchestrator task. Defaults to gaining initial access on target.",
            },
            "rounds": {
                "type": "integer",
                "description": "Maximum orchestrator rounds (default 5, max 20).",
            },
            "workers": {
                "type": "integer",
                "description": "Concurrent workers per round (default 2, max 5).",
            },
            "timeout": {
                "type": "number",
                "description": "Whole-run wall-clock deadline in seconds (0 = unlimited).",
            },
        },
        "required": [],
    },
)


def handle(arguments: dict[str, Any], tool_name: str, ctx: MCPContext) -> list:
    """Handle the lazyown_auto_loop MCP tool."""
    try:
        from modules.lazy_engine import LazyEngine as _LazyEngine

        _cfg = ctx.load_payload()
        _explicit_target = (arguments.get("target") or "").strip()
        if _explicit_target:
            try:
                from types import SimpleNamespace

                from modules.lazy_runner import bind_target_authority

                bind_target_authority(SimpleNamespace(params=_cfg), [_explicit_target])
                _cfg = ctx.load_payload()
            except Exception:
                pass
        _target = (_explicit_target or _cfg.get("rhost", "") or "127.0.0.1").strip()
        _goal = (arguments.get("objective") or arguments.get("goal") or "").strip()
        if not _goal and _target:
            _goal = f"gain initial access on {_target}"
        _rounds = max(1, min(20, int(arguments.get("max_steps", arguments.get("rounds", 5)))) or 5)
        _workers = max(1, min(5, int(arguments.get("workers", 2))))
        _timeout = max(0.0, float(arguments.get("timeout_s", arguments.get("timeout", 0.0)) or 0.0))
        _eng = _LazyEngine()
        _summary = _eng.create_task(_goal)
        _tid = _summary["task_id"]
        _ensured = _eng.ensure_target(_tid, _target, "mcp auto_loop target") if _target else {}
        _result = _eng.run(_tid, max_rounds=_rounds, workers=_workers, timeout_sec=_timeout)
        _ov = _result.get("overview", {})
        prefix = (
            "[lazy_loop] legacy engine retired; routed to LazyEngine\n"
            if bool(arguments.get("legacy", False))
            else "[lazy_loop] "
        )
        return ctx.text(
            tool_name,
            f"{prefix}task {_tid} [{_result.get('status')}] rounds={_result.get('rounds')} "
            f"intents={len(_ov.get('intents', []))} facts={_ov.get('facts', 0)} "
            f"findings={_ov.get('findings', 0)} target={_target} asset={(_ensured or {}).get('asset_id', 0)}\n"
            f"Inspect: lazy_finding list --task {_tid} / lazy_trace list --task {_tid} / "
            f"lazy_report --task {_tid} / lazy_runtime show --task {_tid}",
        )
    except Exception as _loop_exc:
        return ctx.text(tool_name, f"[lazy_loop] engine failure: {_loop_exc}")
