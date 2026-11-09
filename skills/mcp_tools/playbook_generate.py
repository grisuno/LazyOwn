"""MCP tool ``lazyown_playbook_generate`` (migrated from the call_tool dispatch chain)."""

from __future__ import annotations

import asyncio
import sys
from typing import Any

from mcp import types
from mcp_tools._context import MCPContext

TOOL = types.Tool(
    name="lazyown_playbook_generate",
    description=(
        "Generate a MITRE ATT&CK-grounded playbook for a target using STIX2 "
        "technique data and Atomic Red Team tests. The playbook is derived "
        "from the current engagement phase in the WorldModel and saved as YAML. "
        "Returns the saved path and a step summary."
    ),
    inputSchema={
        "type": "object",
        "properties": {
            "target": {
                "type": "string",
                "description": "Target IP or hostname to derive the playbook for.",
            },
            "phase": {
                "type": "string",
                "description": (
                    "Engagement phase override. One of: recon, scanning, "
                    "enumeration, exploitation, post_exploitation. "
                    "If omitted, derived from WorldModel."
                ),
                "default": "",
            },
            "platform": {
                "type": "string",
                "description": "Target platform: linux, windows, macos. Default: linux.",
                "default": "linux",
            },
            "top_n": {
                "type": "string",
                "description": "Maximum number of steps to include (default 5).",
                "default": "5",
            },
        },
        "required": ["target"],
    },
)


async def handle(arguments: dict[str, Any], tool_name: str, ctx: MCPContext) -> list:
    """Handle the lazyown_playbook_generate MCP tool."""
    pb_target = arguments.get("target", "").strip()
    pb_phase = arguments.get("phase", "").strip() or None
    pb_platform = arguments.get("platform", "linux").strip() or "linux"
    pb_top_n = int(arguments.get("top_n", "5") or "5")
    if not pb_target:
        return ctx.text(tool_name, "[playbook_generate] 'target' is required.")
    try:
        sys.path.insert(0, str(ctx.lazyown_dir / "modules"))
        from playbook_engine import PlaybookEngine

        engine = PlaybookEngine(top_n=pb_top_n)
        playbook = await asyncio.get_event_loop().run_in_executor(
            None,
            lambda: engine.derive(pb_target, phase=pb_phase, platform=pb_platform),
        )
        saved_path = await asyncio.get_event_loop().run_in_executor(None, lambda: engine.save(playbook))
        lines = [
            f"Playbook generated: {saved_path}",
            f"Target: {playbook.target}  Phase: {playbook.phase}  "
            f"Platform: {pb_platform}  Steps: {len(playbook.steps)}",
            "",
        ]
        for i, step in enumerate(playbook.steps, 1):
            atomic_id = step.atomic_id or "no atomic"
            lines.append(f"  Step {i}: [{step.technique_id}] {step.name[:60]} ({atomic_id})")
        return ctx.text(tool_name, "\n".join(lines))
    except Exception as exc:
        return ctx.text(tool_name, f"[playbook_generate error] {exc}")
