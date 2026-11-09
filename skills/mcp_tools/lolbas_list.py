"""MCP tool ``lazyown_lolbas_list``: list LOLBAS techniques from plugins."""

from __future__ import annotations

import json
from typing import Any

from mcp import types

from mcp_tools._context import MCPContext

_CATEGORY_STEMS = ("bypass", "obfuscation", "reflection")

TOOL = types.Tool(
    name="lazyown_lolbas_list",
    description=(
        "List available LOLBAS (Living Off The Land Binaries and Scripts) "
        "techniques from plugins. Categories: amsi bypass, etw bypass, "
        "powershell obfuscation, dotnet reflection loading."
    ),
    inputSchema={
        "type": "object",
        "properties": {
            "category": {
                "type": "string",
                "description": "Filter by category: amsi, etw, powershell, dotnet, all",
            },
        },
        "required": [],
    },
)


async def handle(arguments: dict[str, Any], tool_name: str, ctx: MCPContext) -> list:
    """Return LOLBAS techniques discovered in plugin YAML files as JSON."""
    filter_cat = str(arguments.get("category", "all")).lower()
    plugins_dir = ctx.lazyown_dir / "plugins"
    techniques: list[dict] = []
    try:
        import yaml
    except ImportError:
        return ctx.text(tool_name, json.dumps({"error": "PyYAML not installed"}, indent=2))
    for plugin_file in sorted(plugins_dir.glob("*.yaml")):
        if not any(stem in plugin_file.stem for stem in _CATEGORY_STEMS):
            continue
        try:
            data = yaml.safe_load(plugin_file.read_text())
        except Exception:
            continue
        cat = data.get("category", "")
        if filter_cat != "all" and filter_cat not in cat.lower() and filter_cat not in plugin_file.stem.lower():
            continue
        for tech in data.get("techniques", []):
            techniques.append(
                {
                    "plugin": plugin_file.stem,
                    "name": tech.get("name", ""),
                    "description": tech.get("description", ""),
                    "requires_admin": tech.get("requires_admin", False),
                    "platforms": data.get("platforms", []),
                    "command": tech.get("command", ""),
                }
            )
    return ctx.text(
        tool_name,
        json.dumps({"count": len(techniques), "techniques": techniques}, indent=2, ensure_ascii=False),
    )
