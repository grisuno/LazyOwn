"""MCP tool ``lazyown_discover_commands`` (migrated from the call_tool dispatch chain)."""

from __future__ import annotations

import asyncio
import sys
from typing import Any

from mcp import types
from mcp_tools._context import MCPContext

TOOL = types.Tool(
    name="lazyown_discover_commands",
    description=(
        "Discover LazyOwn commands. "
        "With phase parameter: returns bridge catalog entries for that pentest phase "
        "(recon/enum/exploit/postexp/persist/privesc/cred/lateral/exfil/c2/report) "
        "with MITRE tactic, description, and service tags — use this during a pentest "
        "to know which commands are relevant for the current step. "
        "Without phase: discovers ALL commands from the shell (builtins, Lua, YAML, adversaries)."
    ),
    inputSchema={
        "type": "object",
        "properties": {
            "phase": {
                "type": "string",
                "description": (
                    "Pentest phase to list commands for. "
                    "One of: recon, enum, exploit, postexp, persist, privesc, "
                    "cred, lateral, exfil, c2, report. "
                    "If omitted, runs 'help' and returns all shell commands."
                ),
                "enum": [
                    "recon",
                    "enum",
                    "exploit",
                    "postexp",
                    "persist",
                    "privesc",
                    "cred",
                    "lateral",
                    "exfil",
                    "c2",
                    "report",
                ],
            }
        },
    },
)


async def handle(arguments: dict[str, Any], tool_name: str, ctx: MCPContext) -> list:
    """Handle the lazyown_discover_commands MCP tool."""
    phase_filter = arguments.get("phase", "").strip().lower()

    # Phase-specific mode: use bridge catalog (pentest-phase organized)
    if phase_filter:
        try:
            sys.path.insert(0, str(ctx.lazyown_dir / "modules"))
            from lazyown_bridge import get_dispatcher as _bd_dc

            _disp_dc = _bd_dc()
            entries = _disp_dc.list_phase(phase_filter)
            if not entries:
                return ctx.text(
                    tool_name,
                    f"[discover_commands] No commands in bridge catalog for phase '{phase_filter}'.\n"
                    f"Valid phases: recon, enum, exploit, postexp, persist, privesc, cred, lateral, exfil, c2, report",
                )
            out = [
                f"LazyOwn commands for phase: {phase_filter.upper()} ({len(entries)} commands)",
                "",
                f"  {'Command':<22} {'MITRE':<9} {'OS':<8} {'Services':<16} Description",
                f"  {'-' * 22} {'-' * 9} {'-' * 8} {'-' * 16} {'-' * 40}",
            ]
            for e in entries:
                svc = ",".join(e.services[:4]) if hasattr(e, "services") and e.services else "any"
                os_t = getattr(e, "os_target", "any") or "any"
                mit = getattr(e, "mitre_tactic", "") or ""
                desc = getattr(e, "description", "") or ""
                out.append(f"  {e.command:<22} [{mit:<7}] {os_t:<8} {svc:<16} {desc[:50]}")
            out.append("\nUse lazyown_command_help(command='<name>') for full docs.")
            return ctx.text(tool_name, "\n".join(out))
        except Exception as _ex_dc:
            return ctx.text(tool_name, f"[discover_commands] Bridge error: {_ex_dc}\nFalling back to shell help...")

    # No-phase mode: run shell 'help' and parse cmd2 categories
    raw = await asyncio.get_event_loop().run_in_executor(None, lambda: ctx.run_command("help", timeout=30))
    # cmd2 help format: category header line, then === underline, then
    # commands as space-separated tokens across multiple columns.
    import re as _re

    lines = raw.splitlines()
    groups: dict[str, list[str]] = {}
    current_group = "General"
    # Skip banner/startup noise — only parse after "Documented commands" header
    start_idx = next((i for i, line in enumerate(lines) if "Documented commands" in line), 0)
    lines = lines[start_idx:]
    i = 0
    while i < len(lines):
        line = lines[i]
        # Detect category: next line is all '=' and at least 3 chars
        if i + 1 < len(lines) and _re.match(r"^=+$", lines[i + 1].strip()) and len(lines[i + 1].strip()) >= 3:
            current_group = line.strip()
            groups.setdefault(current_group, [])
            i += 2  # skip the === line
            continue
        # Collect command tokens from content lines (non-header, non-empty)
        stripped = line.strip()
        if stripped and not stripped.startswith("Documented") and not _re.match(r"^=+$", stripped):
            tokens = stripped.split()
            for tok in tokens:
                if _re.match(r"^\w[\w_-]+$", tok):
                    groups.setdefault(current_group, []).append(tok)
        i += 1

    if not any(groups.values()):
        return ctx.text(tool_name, raw[:4000])

    total = sum(len(v) for v in groups.values())
    out = [f"LazyOwn shell commands ({total} total):\n"]
    for group, cmds in groups.items():
        if cmds:
            out.append(f"── {group} ({len(cmds)}) ──")
            # 3-column display
            for j in range(0, len(cmds), 3):
                out.append("  " + "  ".join(f"{c:<30}" for c in cmds[j : j + 3]))
            out.append("")
    out.append("Tip: use lazyown_discover_commands(phase='recon') for phase-organized commands.")
    out.append("Tip: use lazyown_command_help(command) for full docs on any command.")
    return ctx.text(tool_name, "\n".join(out))
