"""MCP tool ``lazyown_create_addon`` (migrated from the call_tool dispatch chain)."""

from __future__ import annotations

from typing import Any

from mcp import types
from mcp_tools._context import MCPContext

TOOL = types.Tool(
    name="lazyown_create_addon",
    description=(
        "Create a new YAML addon in lazyaddons/ to integrate ANY GitHub tool into LazyOwn. "
        "The addon becomes an immediately available shell command (do_<name>). "
        "LazyOwn auto-clones the repo on first run and substitutes {param} placeholders "
        "in execute_command with values from payload.json. "
        "Example: create an addon for 'ffuf' that runs fuzzing with {rhost} and {wordlist}."
    ),
    inputSchema={
        "type": "object",
        "properties": {
            "name": {
                "type": "string",
                "description": "Command name (no spaces). Becomes do_<name> in the shell.",
            },
            "description": {
                "type": "string",
                "description": "Human-readable description shown in help.",
            },
            "repo_url": {
                "type": "string",
                "description": "GitHub repo URL to clone (e.g. https://github.com/user/tool.git).",
            },
            "install_path": {
                "type": "string",
                "description": "Local path for the clone (e.g. external/.exploit/toolname). Defaults to external/.exploit/<name>.",
            },
            "install_command": {
                "type": "string",
                "description": "Optional setup command run once after clone (e.g. 'pip install -r requirements.txt').",
                "default": "",
            },
            "execute_command": {
                "type": "string",
                "description": "Command to run. Use {param_name} for substitution from payload.json (e.g. '{rhost}', '{lhost}', '{wordlist}').",
            },
            "params": {
                "type": "array",
                "description": "List of parameter definitions. Each item: {name, required, description}.",
                "items": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"},
                        "required": {"type": "boolean"},
                        "description": {"type": "string"},
                    },
                },
                "default": [],
            },
            "author": {
                "type": "string",
                "description": "Author name (default: LazyOwn RedTeam).",
                "default": "LazyOwn RedTeam",
            },
            "enabled": {
                "type": "boolean",
                "description": "Whether the addon is active immediately (default: true).",
                "default": True,
            },
            "os": {
                "type": "string",
                "description": (
                    "Target platform the addon hits, taken from the MITRE ATT&CK "
                    "platform list. Use 'any' (default) when the addon is OS-agnostic "
                    "(web tools, AI agents, scripts running on the operator host)."
                ),
                "enum": [
                    "any",
                    "linux",
                    "windows",
                    "macos",
                    "network",
                    "containers",
                    "saas",
                    "iaas",
                ],
                "default": "any",
            },
            "trigger": {
                "type": "array",
                "description": (
                    "Nmap service names that should auto-suggest this addon "
                    "(e.g. ['microsoft-ds', 'ldap']). Use ['all'] to trigger on any "
                    "discovered service. Leave empty for addons that are not driven "
                    "by service discovery (manual / strategic tools)."
                ),
                "items": {"type": "string"},
                "default": [],
            },
            "category": {
                "type": "string",
                "description": (
                    "cmd2 palette category. Defaults to '14. Yaml Addon.' which puts "
                    "the addon in the catch-all bucket. Match an existing prefix "
                    "(e.g. '03. Exploitation') to group with related commands."
                ),
                "default": "14. Yaml Addon.",
            },
        },
        "required": ["name", "description", "repo_url", "execute_command"],
    },
)


def handle(arguments: dict[str, Any], tool_name: str, ctx: MCPContext) -> list:
    """Handle the lazyown_create_addon MCP tool."""
    addon_name = arguments["name"].strip().replace(" ", "_")
    description = arguments["description"]
    repo_url = arguments["repo_url"]
    install_path = arguments.get("install_path", f"external/.exploit/{addon_name}")
    install_command = arguments.get("install_command", "")
    execute_command = arguments["execute_command"]
    params = arguments.get("params", [])
    author = arguments.get("author", "LazyOwn RedTeam")
    enabled = arguments.get("enabled", True)
    addon_category = arguments.get("category", "14. Yaml Addon.")
    addon_os_raw = arguments.get("os", "any")
    addon_trigger_raw = arguments.get("trigger", [])

    _allowed_os = {
        "any",
        "linux",
        "windows",
        "macos",
        "network",
        "containers",
        "saas",
        "iaas",
    }
    addon_os = str(addon_os_raw).strip().lower() if isinstance(addon_os_raw, str) else "any"
    if addon_os not in _allowed_os:
        addon_os = "any"
    if isinstance(addon_trigger_raw, str):
        addon_trigger = [addon_trigger_raw.strip().lower()] if addon_trigger_raw.strip() else []
    elif isinstance(addon_trigger_raw, list):
        addon_trigger = [
            str(item).strip().lower() for item in addon_trigger_raw if isinstance(item, str) and item.strip()
        ]
    else:
        addon_trigger = []

    # Build YAML content manually to preserve readable formatting
    lines = [
        f"name: {addon_name}",
        "description: >",
        f"  {description}",
        f'author: "{author}"',
        'version: "1.0"',
        f"enabled: {'true' if enabled else 'false'}",
        f"os: {addon_os}",
        f"trigger: [{', '.join(addon_trigger)}]",
    ]

    if params:
        lines.append("params:")
        for p in params:
            lines.append(f"  - name: {p.get('name', '')}")
            lines.append("    type: string")
            lines.append(f"    required: {'true' if p.get('required', False) else 'false'}")
            if p.get("description"):
                lines.append(f"    description: {p['description']}")

    lines.append("tool:")
    lines.append(f"  name: {addon_name}")
    lines.append(f"  repo_url: {repo_url}")
    lines.append(f"  install_path: {install_path}")
    if install_command:
        lines.append(f"  install_command: {install_command}")
    lines.append(f"  execute_command: {execute_command}")
    lines.append(f"category: {addon_category}")

    yaml_content = "\n".join(lines) + "\n"

    addon_file = ctx.lazyown_dir / "lazyaddons" / f"{addon_name}.yaml"
    try:
        addon_file.write_text(yaml_content)
        return ctx.text(
            tool_name,
            f"Addon '{addon_name}' created at lazyaddons/{addon_name}.yaml\n"
            f"Restart LazyOwn shell or run 'reload' to activate it.\n\n"
            f"--- Preview ---\n{yaml_content}",
        )
    except Exception as e:
        return ctx.text(tool_name, f"error writing addon: {e}")
