"""MCP tool ``lazyown_fast_run`` (migrated from the call_tool dispatch chain)."""

from __future__ import annotations

import asyncio
import os
import subprocess
import time
from typing import Any

from mcp import types
from mcp_tools._context import MCPContext

TOOL = types.Tool(
    name="lazyown_fast_run",
    description=(
        "Launch the LazyOwn full-stack HackTheBox orchestrator "
        "(fast_run_as_r00t.sh). Opens a tmux session with: nmap recon, "
        "ping sweep, C2 implant, auto-loop, Flask C2 server, HTTP file "
        "server, and VPN pane. Optional panes controlled by payload.json "
        "flags: DeepSeek/Ollama, Discord C2, Telegram C2, Cloudflare "
        "tunnel, NC reverse shell. "
        "IMPORTANT: requires root — will prompt for sudo password via a "
        "GUI dialog (ssh-askpass/zenity/yad). "
        "Call with confirm=false first to see the plan without launching."
    ),
    inputSchema={
        "type": "object",
        "properties": {
            "confirm": {
                "type": "boolean",
                "description": (
                    "Set to true to actually launch the stack. "
                    "Defaults to false (dry-run: shows the plan without executing)."
                ),
                "default": False,
            },
            "vpn": {
                "type": "integer",
                "description": "VPN interface index passed to --vpn (default 1).",
                "default": 1,
            },
        },
        "required": [],
    },
)


async def handle(arguments: dict[str, Any], tool_name: str, ctx: MCPContext) -> list:
    """Handle the lazyown_fast_run MCP tool."""
    confirm = bool(arguments.get("confirm", False))
    vpn = int(arguments.get("vpn", 1))

    cfg = ctx.load_payload()
    rhost = cfg.get("rhost", "<not set>")
    domain = cfg.get("domain", "<not set>")

    plan_lines = [
        "LazyOwn fast_run_as_r00t.sh — launch plan",
        "==========================================",
        f"  Primary target  : rhost={rhost}",
        f"  Domain          : {domain}",
        f"  VPN interface   : {vpn}",
        "",
        "Panes that will open in tmux session 'lazyown_sessions':",
        "  [0] Recon        — lazynmap full scan",
        "  [1] Network      — addhosts + ping sweep",
        "  [2] C2 implant   — createcredentials + c2 launch",
        "  [3] Auto-loop    — autonomous loop",
        "  [4] lazyc2       — Flask C2 server (unprivileged)",
        "  [5] www          — HTTP file server + certs",
        "  [6] VPN          — tun interface",
        "",
        "Optional panes (driven by payload.json flags):",
        "  DeepSeek/Ollama, Discord C2, Telegram C2, Cloudflare tunnel, NC revshell",
        "",
        "sudo password will be requested via GUI dialog (ssh-askpass/zenity/yad).",
        "A display (DISPLAY/WAYLAND_DISPLAY) must be available.",
    ]

    if not confirm:
        plan_lines += [
            "",
            "DRY RUN — nothing launched.",
            "Call with confirm=true to start the stack.",
        ]
        return ctx.text(tool_name, "\n".join(plan_lines))

    def _launch() -> str:

        askpass_script = str(ctx.lazyown_dir / "modules" / "gui_askpass.sh")
        fast_run = str(ctx.lazyown_dir / "fast_run_as_r00t.sh")

        if not os.path.isfile(askpass_script):
            return f"[fast_run] SUDO_ASKPASS helper not found: {askpass_script}"
        if not os.path.isfile(fast_run):
            return f"[fast_run] Script not found: {fast_run}"

        # Ensure gui_askpass.sh is executable
        os.chmod(askpass_script, 0o755)

        env = os.environ.copy()
        env["SUDO_ASKPASS"] = askpass_script

        try:
            proc = subprocess.Popen(
                ["sudo", "-A", "./fast_run_as_r00t.sh", "--no-attach", "--vpn", str(vpn)],
                cwd=str(ctx.lazyown_dir),
                env=env,
                stdin=subprocess.DEVNULL,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                start_new_session=True,
            )
        except Exception as exc:
            return f"[fast_run] Failed to launch: {exc}"

        # Wait for tmux session to initialise (up to 15 s)
        session_up = False
        for _ in range(15):
            time.sleep(1)
            try:
                r = subprocess.run(
                    ["tmux", "has-session", "-t", "lazyown_sessions"],
                    capture_output=True,
                )
                if r.returncode == 0:
                    session_up = True
                    break
            except Exception:
                pass

        # Collect any early output / errors (non-blocking)
        try:
            out, err = proc.communicate(timeout=0.1)
        except subprocess.TimeoutExpired:
            _out, err = b"", b""

        lines = ["\n".join(plan_lines), ""]
        if session_up:
            lines.append("tmux session 'lazyown_sessions' is UP.")
            lines.append("Attach manually:  tmux attach -t lazyown_sessions")
        else:
            lines.append(
                "WARNING: tmux session 'lazyown_sessions' not detected after 15 s. "
                "The script may still be initialising."
            )
            lines.append("Check manually:  tmux ls  |  tmux attach -t lazyown_sessions")
        if err:
            lines.append("")
            lines.append("stderr (first 500 chars):")
            lines.append(err.decode(errors="replace")[:500])
        return "\n".join(lines)

    result = await asyncio.get_event_loop().run_in_executor(None, _launch)
    return ctx.text(tool_name, result)
