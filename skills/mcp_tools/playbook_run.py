"""MCP tool ``lazyown_playbook_run`` (migrated from the call_tool dispatch chain)."""

from __future__ import annotations

from pathlib import Path
import asyncio
import shlex
import sys
from typing import Any

from mcp import types

from mcp_tools._context import MCPContext


def _substitute_playbook_target(command: str, target: str) -> str:
    """Substitute a quoted target into a playbook command template."""
    return command.replace("{target}", shlex.quote(target)) if target else command


TOOL = types.Tool(
    name="lazyown_playbook_run",
    description=(
        "Execute a previously generated playbook YAML against the target. "
        "Each step is dispatched as a LazyOwn MCP command. "
        "Tool output is parsed by ObsParser and ingested into WorldModel. "
        "Returns a result summary with per-step success/failure and findings."
    ),
    inputSchema={
        "type": "object",
        "properties": {
            "path": {
                "type": "string",
                "description": "Path to the playbook YAML file.",
                "default": "",
            },
            "target": {
                "type": "string",
                "description": (
                    "Target IP used for command substitution. If omitted, uses the active target from payload.json."
                ),
                "default": "",
            },
            "dry_run": {
                "type": "boolean",
                "description": "If true, log steps without executing them.",
                "default": False,
            },
        },
        "required": [],
    },
)


async def handle(arguments: dict[str, Any], tool_name: str, ctx: MCPContext) -> list:
    """Handle the lazyown_playbook_run MCP tool."""
    pb_path = arguments.get("path", "").strip()
    pb_target = arguments.get("target", "").strip()
    pb_dry_run = bool(arguments.get("dry_run", False))
    try:
        sys.path.insert(0, str(ctx.lazyown_dir / "modules"))
        from playbook_engine import PlaybookEngine

        engine = PlaybookEngine()

        # Resolve playbook path
        PLAYS_DIRECTORY = ctx.lazyown_dir / "playbooks"
        if pb_path:
            pb_file = Path(pb_path)
            if not pb_file.exists() and PLAYS_DIRECTORY.is_dir():
                alt = PLAYS_DIRECTORY / pb_file.name
                if alt.exists():
                    pb_file = alt
        else:
            sessions_pb = sorted(
                list((ctx.lazyown_dir / "sessions").glob("playbook_*.yaml")) + list(PLAYS_DIRECTORY.glob("apt_*.yaml")),
                key=lambda p: p.stat().st_mtime,
                reverse=True,
            )
            if not sessions_pb:
                return ctx.text(tool_name, "[playbook_run] No playbook found. Run lazyown_playbook_generate first.")
            pb_file = sessions_pb[0]

        playbook = await asyncio.get_event_loop().run_in_executor(None, lambda: engine.load(pb_file))

        # Resolve target
        effective_target = pb_target or playbook.target
        if not effective_target:
            cfg = ctx.load_payload()
            effective_target = cfg.get("rhost", "") or cfg.get("target_ip", "")

        # Executor: runs each step command via subprocess
        # Signature: (command, target) matching PlaybookEngine.execute() contract
        def _mcp_executor(command: str, target: str = "") -> str:
            import subprocess

            cmd = _substitute_playbook_target(command, target)
            result = subprocess.run(
                cmd,
                shell=True,
                capture_output=True,
                text=True,
                timeout=120,
                cwd=str(ctx.lazyown_dir),
            )
            return (result.stdout + result.stderr).strip()

        pb_result = await asyncio.get_event_loop().run_in_executor(
            None,
            lambda: engine.execute(
                playbook,
                executor=_mcp_executor,
                dry_run=pb_dry_run,
            ),
        )
        summary = engine.result_summary(pb_result)
        return ctx.text(tool_name, summary)
    except Exception as exc:
        return ctx.text(tool_name, f"[playbook_run error] {exc}")
