"""MCP tool ``lazyown_command_help`` (migrated from the call_tool dispatch chain)."""

from __future__ import annotations

import asyncio
from typing import Any

from mcp import types
from mcp_tools._context import MCPContext

TOOL = types.Tool(
    name="lazyown_command_help",
    description=(
        "Get the full documentation for any LazyOwn command by running 'help <command>'. "
        "Returns parameters, description, and usage examples. "
        "Use this to understand a command before running it."
    ),
    inputSchema={
        "type": "object",
        "properties": {
            "command": {
                "type": "string",
                "description": "The LazyOwn command name to get help for (e.g. 'lazynmap', 'venom', 'c2').",
            }
        },
        "required": ["command"],
    },
)


async def handle(arguments: dict[str, Any], tool_name: str, ctx: MCPContext) -> list:
    """Handle the lazyown_command_help MCP tool."""
    import ast as _ast_help
    import textwrap as _tw
    import warnings as _warn

    _warn.filterwarnings("ignore")
    cmd = arguments["command"].strip()
    if cmd.startswith("do_"):
        cmd = cmd[3:]

    def _read_docstring(cmd_name: str) -> str:
        """Extract do_<cmd> docstring from lazyown.py via AST — no shell spawn, no noise."""
        lo_path = ctx.lazyown_dir / "lazyown.py"
        try:
            src = lo_path.read_text(errors="replace")
            tree = _ast_help.parse(src)
        except Exception as _e:
            return f"Could not parse lazyown.py: {_e}"

        # ── Step 1: resolve aliases ──────────────────────────────────
        # The aliases dict is assigned at module level inside main() as:
        #   aliases = { "ww": "whatweb", "bh": "bloodhound", ... }
        # We extract it by scanning all Dict literals assigned to 'aliases'.
        alias_map: dict[str, str] = {}
        for node in _ast_help.walk(tree):
            if isinstance(node, _ast_help.Assign):
                for t in node.targets:
                    if isinstance(t, _ast_help.Name) and t.id == "aliases":
                        if isinstance(node.value, _ast_help.Dict):
                            for k, v in zip(node.value.keys, node.value.values, strict=False):
                                if isinstance(k, _ast_help.Constant) and isinstance(v, _ast_help.Constant):
                                    alias_map[str(k.value)] = str(v.value)

        resolved = cmd_name
        alias_target = ""
        if cmd_name in alias_map:
            alias_target = alias_map[cmd_name]
            # alias value may be "whatweb" or "sh sudo ..." — extract first word
            resolved = alias_target.split()[0]
            if resolved in ("sh", "run", "run_script"):
                # shell alias — no do_ function, return the alias value directly
                return (
                    f"Alias: {cmd_name}\n"
                    f"Expands to: {alias_target}\n\n"
                    f"This is a shell shortcut — it runs the above command directly.\n"
                    f"No separate do_{cmd_name} function exists."
                )

        # ── Step 2: find do_<resolved> docstring ─────────────────────
        target = f"do_{resolved}"
        for node in _ast_help.walk(tree):
            if isinstance(node, (_ast_help.FunctionDef, _ast_help.AsyncFunctionDef)):
                if node.name == target:
                    doc = _ast_help.get_docstring(node)
                    prefix = ""
                    if alias_target:
                        prefix = f"Alias '{cmd_name}' → '{resolved}'\n\n"
                    if doc:
                        return prefix + _tw.dedent(doc).strip()
                    return f"{prefix}'{target}' exists but has no docstring."

        # ── Step 3: YAML addons ───────────────────────────────────────
        addon_dir = ctx.lazyown_dir / "lazyaddons"
        if addon_dir.exists():
            for f in sorted(addon_dir.glob("*.yaml")):
                try:
                    import yaml as _yaml

                    data = _yaml.safe_load(f.read_text())
                    if isinstance(data, dict):
                        nm = data.get("name", "") or (data.get("tool") or {}).get("name", "")
                        if nm.lower() == cmd_name.lower():
                            desc = data.get("description", "")
                            repo = (data.get("tool") or {}).get("repo_url", "")
                            install = (data.get("tool") or {}).get("install_command", "")
                            execute = (data.get("tool") or {}).get("execute_command", "")
                            return (
                                f"YAML Addon: {nm}\n"
                                f"Description: {desc}\n"
                                f"Repo: {repo}\n"
                                f"Install: {install}\n"
                                f"Execute: {execute}"
                            )
                except Exception:
                    pass

        extra = f" (alias target: '{resolved}')" if alias_target else ""
        return (
            f"Command '{cmd_name}'{extra} not found as do_{resolved}.\n"
            f"Use lazyown_discover_commands() to list all available commands."
        )

    result = await asyncio.get_event_loop().run_in_executor(None, _read_docstring, cmd)
    return ctx.text(tool_name, result[:6000])
