#!/usr/bin/env python3
"""
Auto-generate MCP tool handlers from cli/command_index.json.

Reads the full command catalog, compares against existing handlers in
lazyown_mcp.py, and writes a new skills/mcp_generated_tools.py that can be
imported by lazyown_mcp.py to close the coverage gap.

Usage:
    python3 skills/mcp_tool_generator.py              # generate + verify
    python3 skills/mcp_tool_generator.py --check       # CI mode: verify only
    python3 skills/mcp_tool_generator.py --limit 50    # generate top N only
"""

import argparse
import json
import re
import sys
import textwrap
from pathlib import Path
from typing import Any

LAZYOWN_ROOT = Path(__file__).parent.parent
COMMAND_INDEX = LAZYOWN_ROOT / "cli" / "command_index.json"
MCP_FILE = LAZYOWN_ROOT / "skills" / "lazyown_mcp.py"
OUTPUT_FILE = LAZYOWN_ROOT / "skills" / "mcp_generated_tools.py"


def load_command_index() -> dict[str, Any]:
    with open(COMMAND_INDEX) as f:
        return json.load(f)


def extract_commands(index: dict[str, Any]) -> dict[str, str]:
    """
    Return {command_name: summary} for all unique non-duplicate commands.

    Strips the 'do_' prefix from method names so 'do_lazynmap' becomes 'lazynmap'.
    """
    commands: dict[str, str] = {}
    for entry in index.get("commands", []):
        if entry.get("duplicate_of"):
            continue
        name = entry["name"]
        if name.startswith("do_"):
            name = name[3:]
        summary = (entry.get("summary") or "").strip()
        if summary:
            commands[name] = summary
        else:
            commands[name] = f"Execute the {name} command."
    return commands


def extract_existing_handlers() -> set[str]:
    """
    Parse lazyown_mcp.py for all defined MCP tool names.

    Looks at both @register_handler decorators and name= strings
    inside the list_tools() function return statement.
    """
    with open(MCP_FILE) as f:
        content = f.read()

    registered = set(re.findall(
        r""+r"@register_handler\(\s*['\"]" + r"(lazyown_\w+)" + r"""['\"]\s*\)""", content
    ))

    tool_defs = set(re.findall(
        r'name\s*=\s*"(lazyown_\w+)"', content
    ))

    return registered | tool_defs


def sanitize_description(summary: str, max_len: int = 200) -> str:
    """Truncate and clean a command summary for use as a tool description."""
    cleaned = summary.strip().rstrip(".")
    cleaned = cleaned.replace("\n", " ")
    cleaned = cleaned.replace("``", "'")
    cleaned = cleaned.replace("\\", " ")
    while "  " in cleaned:
        cleaned = cleaned.replace("  ", " ")
    if len(cleaned) > max_len:
        cleaned = cleaned[:max_len - 3].rsplit(" ", 1)[0] + "..."
    return cleaned


def sanitize_docstring(text: str) -> str:
    """Escape backslashes and quotes for triple-quoted docstrings."""
    escaped = text.replace("\\", "\\\\").replace('"""', '\\"\\"\\"')
    return escaped


def _build_tool_schema(command_param_name: str = "args") -> str:
    """Return the JSON inputSchema for a single-arg command wrapper tool."""
    return textwrap.dedent(f"""\
        inputSchema={{
            "type": "object",
            "properties": {{
                "{command_param_name}": {{
                    "type": "string",
                    "description": "Optional arguments to pass to the command.",
                    "default": "",
                }},
            }},
        }}""")


def generate_module(
    commands: dict[str, str],
    existing_handlers: set[str],
    limit: int | None = None,
) -> str:
    """
    Build the complete Python source for mcp_generated_tools.py.

    The generated file exports:
      - get_generated_tool_definitions() -> list[types.Tool]
      - register_all_generated_handlers(reg_fn, make_fn, run_fn) -> int
    """
    sorted_cmds = sorted(commands.items())

    # Determine which commands need generation
    needs_generation: list[tuple[str, str]] = []  # (tool_name, cmd_name)
    for cmd_name, summary in sorted_cmds:
        tool_name = f"lazyown_{cmd_name}"
        if tool_name in existing_handlers:
            continue
        needs_generation.append((tool_name, cmd_name))
        if limit is not None and len(needs_generation) >= limit:
            break

    lines: list[str] = []
    lines.append("#!/usr/bin/env python3")
    lines.append(
        '"""Auto-generated MCP tool handlers from command_index.json.'
    )
    lines.append("")
    lines.append("DO NOT EDIT BY HAND.  Re-generate with:")
    lines.append("    python3 skills/mcp_tool_generator.py")
    lines.append("")
    lines.append(
        "This file is imported by lazyown_mcp.py to close the coverage gap "
        "between the 148 hand-written handlers and the 670+ CLI commands."
    )
    lines.append('"""')
    lines.append("")
    lines.append("from __future__ import annotations")
    lines.append("")
    lines.append("from typing import Any")
    lines.append("")
    lines.append("")
    lines.append("_COMMAND_MAP: dict[str, str] = {")

    for tool_name, cmd_name in needs_generation:
        summary = sanitize_description(commands[cmd_name])
        lines.append(f'    "{tool_name}": {json.dumps(summary)},')

    lines.append("}")
    lines.append("")
    lines.append("")
    lines.append(
        "def get_generated_tool_definitions() -> list:"
    )
    lines.append(
        '    """Return list[types.Tool] entries for all generated tools."""'
    )
    lines.append("    from mcp import types as _types")
    lines.append("")
    lines.append("    _tools: list = []")
    lines.append("    for _tool, _desc in sorted(_COMMAND_MAP.items()):")
    lines.append("        _tools.append(_types.Tool(")
    lines.append("            name=_tool,")
    lines.append("            description=_desc,")
    schema = _build_tool_schema()
    for schema_line in schema.splitlines():
        lines.append(f"            {schema_line}")
    lines.append("        ))")
    lines.append("    return _tools")
    lines.append("")
    lines.append("")
    lines.append(
        "def register_all_generated_handlers("
    )
    lines.append(
        "    register_handler_fn,"
    )
    lines.append(
        "    make_text_fn,"
    )
    lines.append(
        "    run_lazyown_cmd_fn,"
    )
    lines.append(
        ") -> int:"
    )
    lines.append(
        '    """'
    )
    lines.append(
        "    Register every generated handler via *register_handler_fn*."
    )
    lines.append("")
    lines.append(
        "    Called by lazyown_mcp.py after its infrastructure is ready. "
        "Returns the count registered."
    )
    lines.append(
        '    """'
    )
    lines.append("    _reg = 0")
    lines.append("")

    for tool_name, cmd_name in needs_generation:
        handler_name = tool_name.replace("lazyown_", "_gen_")
        lines.append(
            f"    async def {handler_name}"
            f"(arguments: dict, tool_name: str, "
            f"_cmd={cmd_name!r}) -> list:"
        )
        lines.append(
            '        cmd = arguments.get("args", "")'
        )
        lines.append(
            "        output = run_lazyown_cmd_fn("
            'f"{_cmd} {cmd}".strip())'
        )
        lines.append(
            "        return make_text_fn(tool_name, output)"
        )
        lines.append("")
        lines.append(
            f"    register_handler_fn({tool_name!r})({handler_name})"
        )
        lines.append(
            "    _reg += 1"
        )
        lines.append("")

    lines.append("    return _reg")
    lines.append("")

    return "\n".join(lines)


def verify_coverage(
    commands: dict[str, str],
    existing_handlers: set[str],
) -> tuple[set[str], set[str], set[str]]:
    """
    Compare indexed commands against existing MCP tool coverage.

    Returns (new, existing_match, missing_from_index) sets of tool names.
    """
    indexed_tools: set[str] = {f"lazyown_{c}" for c in commands}

    new = indexed_tools - existing_handlers
    existing_match = indexed_tools & existing_handlers
    missing_from_index = existing_handlers - indexed_tools
    return new, existing_match, missing_from_index


def main():
    parser = argparse.ArgumentParser(
        description="Auto-generate MCP tool handlers from command_index.json"
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Verification-only mode: report coverage gaps, exit 0 if none.",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Cap generated handlers to N (default: all).",
    )
    args = parser.parse_args()

    if not COMMAND_INDEX.is_file():
        print(f"ERROR: command_index.json not found at {COMMAND_INDEX}", file=sys.stderr)
        sys.exit(1)

    index = load_command_index()
    commands = extract_commands(index)
    existing = extract_existing_handlers()

    new, existing_match, missing_from_index = verify_coverage(commands, existing)

    print("=== Verification ===")
    print(f"Commands in index:       {index['totals']['unique_commands']}")
    print(f"Commands extracted:      {len(commands)}")
    print(f"Existing MCP tools:      {len(existing)}")
    print(f"NEW (no MCP coverage):   {len(new)}")
    print(f"Matched (has coverage):  {len(existing_match)}")
    print(f"Tools NOT from command_index (bespoke/compound): {len(missing_from_index)}")
    print()

    if args.check:
        if new:
            print(f"[CHECK] {len(new)} commands lack MCP coverage:")
            for t in sorted(new):
                print(f"  {t}")
            print()
            print(f"[CHECK] Run without --check to generate stubs for {len(new)} tools.")
            sys.exit(1)
        else:
            print("[CHECK] All indexed commands have MCP tool coverage.")
            sys.exit(0)

    if missing_from_index:
        print("Bespoke/compound tools (not in command_index.json):")
        for t in sorted(missing_from_index):
            print(f"  {t}")
        print()

    limit = args.limit
    source = generate_module(commands, existing, limit=limit)

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_FILE, "w") as f:
        f.write(source)

    generated_count = len([1 for t in sorted(commands) if f"lazyown_{t}" not in existing])
    if limit is not None:
        generated_count = min(generated_count, limit)

    print(f"Generated file: {OUTPUT_FILE} ({len(source)} bytes, {generated_count} handlers)")

    if limit is not None:
        print(f"(Limited to first {limit})")
    print()

    print("Import in lazyown_mcp.py with:")
    print("    from skills.mcp_generated_tools import (")
    print("        get_generated_tool_definitions,")
    print("        register_all_generated_handlers,")
    print("    )")
    print("")
    print("Then in list_tools() append:")
    print("    result.extend(get_generated_tool_definitions())")
    print("")
    print("And after module-level setup call:")
    print("    registered = register_all_generated_handlers(")
    print("        register_handler, _make_text, _run_lazyown_command")
    print("    )")


if __name__ == "__main__":
    main()
