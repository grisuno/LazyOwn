"""MCP tool ``lazyown_list_addons`` (migrated from the call_tool dispatch chain)."""

from __future__ import annotations

from typing import Any

from mcp import types
from mcp_tools._context import MCPContext

TOOL = types.Tool(
    name="lazyown_list_addons",
    description=(
        "List all YAML addons in lazyaddons/ with their name, enabled status, "
        "description, repo URL, os platform and trigger services."
    ),
    inputSchema={"type": "object", "properties": {}},
)


def handle(arguments: dict[str, Any], tool_name: str, ctx: MCPContext) -> list:
    """Handle the lazyown_list_addons MCP tool."""
    addons_dir = ctx.lazyown_dir / "lazyaddons"
    try:
        import yaml as _yaml
    except ImportError:
        _yaml = None

    lines = []
    for f in sorted(addons_dir.glob("*.yaml")):
        if f.name == "README.md":
            continue
        try:
            content = f.read_text()
            if _yaml:
                data = _yaml.safe_load(content)
                enabled_flag = "✓" if data.get("enabled", False) else "✗"
                desc = (data.get("description") or "").strip().replace("\n", " ")[:60]
                repo = (data.get("tool") or {}).get("repo_url", "")
                addon_os_value = str(data.get("os", "any")).strip().lower() or "any"
                trigger_raw = data.get("trigger", []) or []
                if isinstance(trigger_raw, str):
                    trigger_list = [trigger_raw.strip()] if trigger_raw.strip() else []
                elif isinstance(trigger_raw, list):
                    trigger_list = [str(item).strip() for item in trigger_raw if isinstance(item, str) and item.strip()]
                else:
                    trigger_list = []
                trigger_label = ", ".join(trigger_list) if trigger_list else "-"
                lines.append(
                    f"[{enabled_flag}] {data.get('name', f.stem):<30} os={addon_os_value:<10} trigger={trigger_label}"
                )
                if desc:
                    lines.append(f"      desc: {desc}")
                if repo:
                    lines.append(f"      repo: {repo}")
            else:
                lines.append(f.name)
        except Exception:
            lines.append(f"{f.name}  (parse error)")

    return ctx.text(tool_name, f"Addons ({len(lines)}):\n" + "\n".join(lines) if lines else "No addons found.")
