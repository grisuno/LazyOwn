"""MCP tool ``lazyown_list_plugins`` (migrated from the call_tool dispatch chain)."""

from __future__ import annotations

from typing import Any

from mcp import types
from mcp_tools._context import MCPContext

TOOL = types.Tool(
    name="lazyown_list_plugins",
    description="List all Lua plugins in plugins/ with their name, enabled status, and description.",
    inputSchema={"type": "object", "properties": {}},
)


def handle(arguments: dict[str, Any], tool_name: str, ctx: MCPContext) -> list:
    """Handle the lazyown_list_plugins MCP tool."""
    plugins_dir = ctx.lazyown_dir / "plugins"
    try:
        import yaml as _yaml
    except ImportError:
        _yaml = None

    lines = []
    for f in sorted(plugins_dir.glob("*.lua")):
        meta_file = f.with_suffix(".yaml")
        enabled_flag = "?"
        desc = ""
        if meta_file.exists() and _yaml:
            try:
                data = _yaml.safe_load(meta_file.read_text())
                enabled_flag = "✓" if data.get("enabled", False) else "✗"
                desc = (data.get("description") or "").strip().replace("\n", " ")[:60]
            except Exception:
                pass
        lines.append(f"[{enabled_flag}] {f.stem:<35} {desc}")

    return ctx.text(tool_name, f"Lua plugins ({len(lines)}):\n" + "\n".join(lines) if lines else "No plugins found.")
