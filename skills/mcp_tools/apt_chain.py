"""MCP tool ``lazyown_apt_chain`` (migrated from the call_tool dispatch chain)."""

from __future__ import annotations

import asyncio
import shlex
import sys
from typing import Any

from mcp import types
from mcp_tools._context import MCPContext

TOOL = types.Tool(
    name="lazyown_apt_chain",
    description=(
        "Run a fully YAML-administered APT chain with one call "
        "(assign, scan unless cached, exploit sweep, C2 deploy, loot, "
        "playbook validate/run, emulation staging, session shell check). "
        "Chain first arg names a file in chains/ (per-APT files like "
        "apt_rocke inherit the base apt_chain and only pin the playbook); "
        "a bare playbook name falls back to its apt_<name> chain. "
        "Long-running: prefer a generous timeout_s."
    ),
    inputSchema={
        "type": "object",
        "properties": {
            "chain": {
                "type": "string",
                "description": "Chain file name in chains/ (e.g. 'apt_rocke') or playbook shorthand (e.g. 'rocke').",
                "default": "apt_chain",
            },
            "target": {
                "type": "string",
                "description": "Target IP. Defaults to rhost from payload.json.",
                "default": "",
            },
            "timeout_s": {
                "type": "integer",
                "description": "Max seconds for the whole chain (default 900, max 1800).",
                "default": 900,
            },
            "playbook": {
                "type": "string",
                "description": "Override the playbook token for the chain (e.g. 'rocke').",
                "default": "",
            },
            "steps": {
                "type": "string",
                "description": "Comma-separated step ids to run (e.g. 'recon,exploit'); others are skipped.",
                "default": "",
            },
            "vars": {
                "type": "object",
                "description": "Token overrides as key=value pairs injected into chain steps.",
                "default": {},
            },
            "dry_run": {
                "type": "boolean",
                "description": "Resolve every step without executing.",
                "default": False,
            },
            "json": {
                "type": "boolean",
                "description": "Emit machine-readable result with per-step outcomes, variables and run_id.",
                "default": False,
            },
            "replan": {
                "type": "boolean",
                "description": "Let the reactive engine insert extra steps after each executed step (capped at 3 inserts).",
                "default": False,
            },
            "continue_all": {
                "type": "boolean",
                "description": "Do not abort on the first failed step; keep executing as long as possible.",
                "default": False,
            },
            "resume": {
                "type": "string",
                "description": "Run id of an interrupted checkpoint; resumes it (apt_chain checkpoints lists them).",
                "default": "",
            },
            "no_checkpoint": {
                "type": "boolean",
                "description": "Do not persist a resumable checkpoint for this run.",
                "default": False,
            },
        },
        "required": [],
    },
)


async def handle(arguments: dict[str, Any], tool_name: str, ctx: MCPContext) -> list:
    """Handle the lazyown_apt_chain MCP tool."""
    ch_chain = (arguments.get("chain", "") or "").strip().lower() or "apt_chain"
    _cfg = ctx.load_payload()
    ch_target = (arguments.get("target", "") or "").strip() or str(_cfg.get("rhost", "") or "").strip()
    ch_timeout = max(60, min(int(arguments.get("timeout_s", 900)), 1800))
    if not ch_target:
        return ctx.text(tool_name, "[apt_chain] target is required (or set rhost).")
    try:
        sys.path.insert(0, str(ctx.modules_dir))
        from chain_registry import get as _chain_get

        chain = _chain_get(ch_chain)
        if chain is None:
            from chain_registry import load_all as _chain_all

            available = sorted(_chain_all().keys())
            return ctx.text(
                tool_name, f"[apt_chain] unknown/disabled chain '{ch_chain}'. Available: {', '.join(available)}"
            )
    except Exception as exc:
        return ctx.text(tool_name, f"[apt_chain error] chain registry unavailable: {exc}")
    cmd_parts = ["apt_chain", ch_chain, ch_target]
    ch_vars = arguments.get("vars") or {}
    if isinstance(ch_vars, dict) and ch_vars:
        for var_name, var_value in list(ch_vars.items())[:16]:
            if str(var_name).isidentifier():
                cmd_parts.append(f"--var {str(var_name)}={shlex.quote(str(var_value))}")
    if arguments.get("dry_run"):
        cmd_parts.append("--dry-run")
    if arguments.get("json"):
        cmd_parts.append("--json")
    if arguments.get("replan"):
        cmd_parts.append("--replan")
    if arguments.get("continue_all"):
        cmd_parts.append("--continue")
    ch_resume = str(arguments.get("resume", "") or "").strip()
    if ch_resume:
        cmd_parts.append(f"--resume {shlex.quote(ch_resume)}")
    ch_steps = str(arguments.get("steps", "") or "").strip()
    if ch_steps:
        cmd_parts.append(f"--step {shlex.quote(ch_steps)}")
    ch_playbook = str(arguments.get("playbook", "") or "").strip()
    if ch_playbook:
        cmd_parts.append(f"--playbook {shlex.quote(ch_playbook)}")
    if arguments.get("no_checkpoint"):
        cmd_parts.append("--no-checkpoint")
    cmd = " ".join(cmd_parts)
    try:
        output = await asyncio.get_event_loop().run_in_executor(None, lambda: ctx.run_command(cmd, ch_timeout))
    except Exception as exc:
        return ctx.text(tool_name, f"[apt_chain error] {exc}")
    return ctx.text(tool_name, f"[apt_chain {ch_chain} {ch_target}]\n{str(output)[-8000:]}")
