"""MCP tool ``lazyown_lolbas_use``: execute one LOLBAS technique."""

from __future__ import annotations

import json
from typing import Any

from mcp import types

from mcp_tools._context import MCPContext

_EXEC_TIMEOUT_SEC = 30
_RESOLVED_PREVIEW = 300
_OUTPUT_PREVIEW = 3000

TOOL = types.Tool(
    name="lazyown_lolbas_use",
    description=(
        "Execute a specific LOLBAS technique by plugin and technique name. "
        "Resolves variables from payload.json automatically. "
        "Use lazyown_lolbas_list first to discover available techniques."
    ),
    inputSchema={
        "type": "object",
        "properties": {
            "plugin": {
                "type": "string",
                "description": "Plugin name (e.g. amsi_bypass, etw_bypass)",
            },
            "technique": {
                "type": "string",
                "description": "Technique name within the plugin",
            },
            "technique_ref": {
                "type": "string",
                "description": "Shorthand: plugin/technique (e.g. amsi_bypass/amsiInitFailed)",
            },
        },
        "required": [],
    },
)


async def handle(arguments: dict[str, Any], tool_name: str, ctx: MCPContext) -> list:
    """Resolve and run one LOLBAS technique, returning command and output."""
    plugin_name = arguments.get("plugin", "")
    technique_name = arguments.get("technique", "")
    if not plugin_name or not technique_name:
        combined = str(arguments.get("technique_ref", "")).split("/")
        if len(combined) == 2:
            plugin_name, technique_name = combined
    if not plugin_name or not technique_name:
        return ctx.text(tool_name, json.dumps({"error": "plugin and technique are required"}, indent=2))
    plugin_path = ctx.lazyown_dir / "plugins" / f"{plugin_name}.yaml"
    if not plugin_path.exists():
        return ctx.text(tool_name, json.dumps({"error": f"Plugin not found: {plugin_name}"}, indent=2))
    try:
        import yaml

        data = yaml.safe_load(plugin_path.read_text())
    except Exception as exc:
        return ctx.text(tool_name, json.dumps({"error": f"Failed to load plugin: {exc}"}, indent=2))
    technique = next((t for t in data.get("techniques", []) if t.get("name") == technique_name), None)
    if technique is None:
        return ctx.text(tool_name, json.dumps({"error": f"Technique '{technique_name}' not found"}, indent=2))
    cfg = ctx.load_payload()
    command = technique.get("command", "")
    resolved = (
        command.replace("{rhost}", cfg.get("rhost", ""))
        .replace("{lhost}", cfg.get("lhost", ""))
        .replace("{lport}", str(cfg.get("lport", "")))
    )
    output = ctx.run_command(resolved, _EXEC_TIMEOUT_SEC)
    return ctx.text(
        tool_name,
        json.dumps(
            {
                "plugin": plugin_name,
                "technique": technique_name,
                "resolved_command": resolved[:_RESOLVED_PREVIEW],
                "output": output[:_OUTPUT_PREVIEW],
            },
            indent=2,
            ensure_ascii=False,
        ),
    )
