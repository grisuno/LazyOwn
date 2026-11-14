"""MCP tool ``lazyown_auto_loop`` (single runner, one path with the CLI).

Routes through :func:`modules.lazy_runner.run_loop_command` — the same
runner behind the ``auto_loop`` and ``lazy_loop`` CLI verbs — so MCP runs
receive the full gate set: budget confirmation, preflight, bootstrap,
terminal safety, loop audit and the proxy/browser-sync autostart.
"""

from __future__ import annotations

from typing import Any

from mcp import types
from mcp_tools._context import MCPContext

TOOL = types.Tool(
    name="lazyown_auto_loop",
    description=(
        "Autonomous loop over the single LazyOrchestrator engine (same runner "
        "as the auto_loop CLI). Accepts target, objective, rounds, workers and "
        "a wall-clock timeout; the runner covers budget confirmation, "
        "preflight, bootstrap, scope guards, chain steering, loop audit and "
        "honest failure handling. The legacy flag is accepted for "
        "compatibility and only annotates the output."
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
                "description": "Maximum orchestrator rounds (default 6, clamp 50).",
            },
            "workers": {
                "type": "integer",
                "description": "Concurrent workers per round (default 2, max 5).",
            },
            "timeout": {
                "type": "number",
                "description": "Whole-run wall-clock deadline in seconds (0 = unlimited).",
            },
            "legacy": {
                "type": "boolean",
                "description": "Compatibility flag; only annotates the output.",
            },
        },
        "required": [],
    },
)


def _loop_line(arguments: dict[str, Any]) -> list[str]:
    """Translate tool arguments into a shared-runner command line.

    Args:
        arguments: Tool arguments (target, objective, rounds, workers,
            timeout, legacy).

    Returns:
        Argument list for :func:`modules.lazy_runner.run_loop_command`.
    """
    parts: list[str] = []
    target = str(arguments.get("target") or "").strip()
    if target:
        parts += ["--target", target]
    goal = str(arguments.get("objective") or arguments.get("goal") or "").strip()
    if goal:
        parts.append(goal)
    try:
        rounds = int(arguments.get("max_steps", arguments.get("rounds", 0)) or 0)
    except (TypeError, ValueError):
        rounds = 0
    if rounds:
        parts += ["--rounds", str(rounds)]
    try:
        workers = int(arguments.get("workers", 0) or 0)
    except (TypeError, ValueError):
        workers = 0
    if workers:
        parts += ["--workers", str(workers)]
    try:
        timeout = float(arguments.get("timeout_s", arguments.get("timeout", 0.0)) or 0.0)
    except (TypeError, ValueError):
        timeout = 0.0
    if timeout:
        parts += ["--timeout", str(timeout)]
    return parts


def _render(summary: dict[str, Any], target: str, prefix: str) -> str:
    """Render one runner summary as the MCP text response.

    Args:
        summary: Runner output (task_id, status, rounds, overview, error).
        target: Explicit target from the arguments, for reporting.
        prefix: Line prefix (legacy annotation included).

    Returns:
        Human-readable multi-line response text.
    """
    overview = summary.get("overview") or {}
    task_id = str(summary.get("task_id", "") or "")
    header = (
        f"{prefix}task {task_id} [{summary.get('status', '')}] rounds={summary.get('rounds', 0)} "
        f"intents={len(overview.get('intents', []) or [])} facts={overview.get('facts', 0)} "
        f"findings={overview.get('findings', 0)} target={target or summary.get('target', '')}"
    )
    lines = [header]
    if summary.get("cancelled"):
        lines.append("run cancelled")
    if summary.get("error"):
        lines.append(f"error: {summary['error']}")
    if task_id:
        lines.append(
            f"Inspect: lazy_finding list --task {task_id} / lazy_trace list --task {task_id} / "
            f"lazy_report --task {task_id} / lazy_runtime show --task {task_id}"
        )
    return "\n".join(lines)


def handle(arguments: dict[str, Any], tool_name: str, ctx: MCPContext) -> list:
    """Handle the lazyown_auto_loop MCP tool through the shared runner.

    Args:
        arguments: Tool arguments (target, objective, rounds, workers,
            timeout, legacy).
        tool_name: Tool name used by the context envelope.
        ctx: Injected runtime context (payload loader, text renderer).

    Returns:
        The MCP text response for the run.
    """
    try:
        from modules.lazy_runner import run_loop_command

        summary = run_loop_command(None, ctx.load_payload(), " ".join(_loop_line(arguments)), "auto_loop")
        if (summary.get("error") and not summary.get("task_id")) and summary.get("status") != "preflight_failed":
            return ctx.text(tool_name, f"[lazy_loop] run refused: {summary.get('error')}")
        prefix = (
            "[lazy_loop] legacy engine retired; routed to the shared runner\n"
            if bool(arguments.get("legacy", False))
            else "[lazy_loop] "
        )
        return ctx.text(tool_name, _render(summary, str(arguments.get("target") or "").strip(), prefix))
    except Exception as _loop_exc:
        return ctx.text(tool_name, f"[lazy_loop] runner failure: {_loop_exc}")
