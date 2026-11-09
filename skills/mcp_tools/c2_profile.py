"""MCP tool ``lazyown_c2_profile`` (migrated from the call_tool dispatch chain)."""

from __future__ import annotations

import sys
from typing import Any

from mcp import types
from mcp_tools._context import MCPContext

TOOL = types.Tool(
    name="lazyown_c2_profile",
    description=(
        "Show, set or list malleable C2 profiles. "
        "Profiles control beacon sleep interval, jitter, HTTP headers, "
        "URI paths, and user-agent — affecting how detectable C2 traffic is. "
        "Built-in profiles: default, stealth, aggressive, debug."
    ),
    inputSchema={
        "type": "object",
        "properties": {
            "action": {
                "type": "string",
                "description": "'list' to show available profiles, 'show' to display one, 'set' to activate.",
                "enum": ["list", "show", "set"],
                "default": "list",
            },
            "name": {
                "type": "string",
                "description": "Profile name (required for show/set).",
                "default": "",
            },
        },
        "required": [],
    },
)


def handle(arguments: dict[str, Any], tool_name: str, ctx: MCPContext) -> list:
    """Handle the lazyown_c2_profile MCP tool."""
    cp_action = arguments.get("action", "list").strip()
    cp_name = arguments.get("name", "").strip()
    try:
        sys.path.insert(0, str(ctx.lazyown_dir / "modules"))
        from c2_profile import get_registry

        registry = get_registry()
        if cp_action == "list":
            names = registry.list_names()
            lines = ["Available C2 profiles:", ""]
            for n in names:
                p = registry.get(n)
                lines.append(
                    f"  {n:12s}  sleep={p.sleep.interval_ms}ms  "
                    f"jitter={p.sleep.jitter_pct}%  "
                    f"ua={p.http_get.user_agent[:40]}"
                )
            return ctx.text(tool_name, "\n".join(lines))
        elif cp_action in ("show", "set"):
            if not cp_name:
                return ctx.text(tool_name, f"[c2_profile] 'name' is required for action='{cp_action}'.")
            profile = registry.get(cp_name)
            if profile is None:
                return ctx.text(
                    tool_name, f"[c2_profile] Unknown profile '{cp_name}'. Available: {registry.list_names()}"
                )
            if cp_action == "set":
                cfg = ctx.load_payload()
                cfg["c2_profile"] = cp_name
                try:
                    payload_path = ctx.lazyown_dir / "payload.json"
                    import json as _json

                    payload_path.write_text(_json.dumps(cfg, indent=2))
                except Exception:
                    pass
            lines = [
                f"Profile: {profile.name}",
                f"  {profile.description}",
                f"  Sleep:   {profile.sleep.interval_ms}ms  Jitter: {profile.sleep.jitter_pct}%",
                f"  GET UA:  {profile.http_get.user_agent}",
                f"  GET URI: {profile.http_get.uri_paths}",
                f"  POST URI:{profile.http_post.uri_paths}",
                f"  Headers: {dict(list(profile.http_get.headers.items())[:3])}",
            ]
            if cp_action == "set":
                lines.append(f"  Active profile set to '{cp_name}' in payload.json.")
            return ctx.text(tool_name, "\n".join(lines))
        else:
            return ctx.text(tool_name, f"[c2_profile] Unknown action '{cp_action}'. Use: list, show, set.")
    except Exception as exc:
        return ctx.text(tool_name, f"[c2_profile error] {exc}")
