"""MCP tool ``lazyown_loop_smoke``: single-leg autonomous loop smoke test."""

from __future__ import annotations

import json
from typing import Any

from mcp import types

from mcp_tools._context import MCPContext

_DEFAULT_MEMBER = "llamacpp-local"
_DEFAULT_MODEL = "llamacpp:local-model"
_DEFAULT_ROUNDS = 4
_MAX_ROUNDS = 12
_DEFAULT_WORKERS = 2
_MAX_WORKERS = 5
_MEMBER_PRIORITY = 10

TOOL = types.Tool(
    name="lazyown_loop_smoke",
    description=(
        "Run the autonomous loop smoke test against a target with one "
        "LLM leg (default llamacpp-local, the local Qwen server). "
        "Returns the independent goal verdict plus findings. Proves "
        "a model leg end to end before production runs."
    ),
    inputSchema={
        "type": "object",
        "properties": {
            "target": {
                "type": "string",
                "description": "Target IP for the smoke run (lab guest).",
            },
            "member": {
                "type": "string",
                "description": "Pool member name to bind (default llamacpp-local).",
                "default": _DEFAULT_MEMBER,
            },
            "model": {
                "type": "string",
                "description": "Model spec to bind (default llamacpp:local-model).",
                "default": _DEFAULT_MODEL,
            },
            "rounds": {
                "type": "integer",
                "description": "Max orchestrator rounds (default 4, cap 12).",
                "default": _DEFAULT_ROUNDS,
            },
            "workers": {
                "type": "integer",
                "description": "Parallel workers (default 2, cap 5).",
                "default": _DEFAULT_WORKERS,
            },
            "goal": {
                "type": "string",
                "description": "Goal override (default gain initial access on target).",
            },
        },
        "required": ["target"],
    },
)


def handle(arguments: dict[str, Any], tool_name: str, ctx: MCPContext) -> list:
    """Run a one-leg loop smoke test and return the goal verdict."""
    target = str(arguments.get("target", "") or "").strip()
    if not target:
        return ctx.text(tool_name, "target is required (lab IP, e.g. MSF guest)")
    member = str(arguments.get("member", _DEFAULT_MEMBER) or _DEFAULT_MEMBER).strip()
    model = str(arguments.get("model", _DEFAULT_MODEL) or _DEFAULT_MODEL).strip()
    try:
        rounds = max(1, min(_MAX_ROUNDS, int(arguments.get("rounds", _DEFAULT_ROUNDS) or _DEFAULT_ROUNDS)))
    except (TypeError, ValueError):
        rounds = _DEFAULT_ROUNDS
    try:
        workers = max(1, min(_MAX_WORKERS, int(arguments.get("workers", _DEFAULT_WORKERS) or _DEFAULT_WORKERS)))
    except (TypeError, ValueError):
        workers = _DEFAULT_WORKERS
    goal = str(arguments.get("goal", "") or f"gain initial access on {target}").strip()
    try:
        from modules.lazy_engine import LazyEngine
    except Exception as error:
        return ctx.text(tool_name, json.dumps({"error": str(error)}))
    try:
        engine = LazyEngine()
        summary = engine.create_task(goal)
        task_id = summary["task_id"]
        engine.ensure_target(task_id, target, "loop smoke")
        engine.store.set_llm_chain(task_id, [{"name": member, "model": model, "priority": _MEMBER_PRIORITY}])
        result = engine.run(task_id, max_rounds=rounds, workers=workers, executor=None)
        verdict = result.get("verdict") or {}
        return ctx.text(
            tool_name,
            json.dumps(
                {
                    "task": task_id,
                    "status": result.get("status"),
                    "rounds": result.get("rounds"),
                    "verdict": verdict.get("verdict"),
                    "coverage_pct": verdict.get("coverage_pct"),
                    "facts": verdict.get("facts"),
                    "findings": verdict.get("findings"),
                    "confirmed": verdict.get("confirmed"),
                    "report": verdict.get("path"),
                    "member": member,
                },
                indent=2,
            ),
        )
    except Exception as error:
        return ctx.text(tool_name, json.dumps({"error": str(error)}))
