#!/usr/bin/env python3
"""Sync documentation numbers with the live codebase — single source of truth.

Counts are measured from the code itself and rewritten into the docs so the
README, guides and agent context never contradict each other again:

- ``cli_commands``   — ``do_`` methods in lazyown.py + cli/commands/*.py (AST)
- ``bridge_catalog`` — ``CatalogEntry(`` rows in modules/lazyown_bridge.py
- ``mcp_tools``      — ``name="lazyown_`` registrations in skills/lazyown_mcp.py
- ``aliases``        — keys in cli/aliases.yaml
- ``addons``         — lazyaddons/*.yaml
- ``plugins``        — plugins/*.lua
- ``playbooks``      — playbooks/*.yaml

Usage:
    python3 scripts/sync_doc_stats.py           apply the replacements in place
    python3 scripts/sync_doc_stats.py --check   exit 1 when any doc is stale (CI)
    python3 scripts/sync_doc_stats.py --print   show the measured numbers only
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent

REPLACEMENTS: tuple[tuple[str, str, str], ...] = (
    ("ESSENTIALS.md", r"\(\d+\+? commands\)", "({cli_commands} commands)"),
    ("ESSENTIALS.md", r"All \d+\+? commands with descriptions", "All {cli_commands} commands with descriptions"),
    ("ESSENTIALS.md", r"All \d+\+? aliases", "All {aliases} aliases"),
    ("ESSENTIALS.md", r"\(\d+ tools\)", "({mcp_tools} tools)"),
    ("CHEATSHEET.md", r"full \d+\+?[- ]?command catalog", "full {cli_commands}-command catalog"),
    ("CHEATSHEET.md", r"complete \d+\+?[- ]?command reference", "complete {cli_commands}-command reference"),
    ("CHEATSHEET.md", r"`COMMANDS\.md` \| ~\d+", "`COMMANDS.md` | ~1600"),
    ("QUICKSTART.md", r"full \d+\+?[- ]?command reference", "full {cli_commands}-command reference"),
    ("QUICKSTART.md", r"~\d+ MCP tools", "{mcp_tools} MCP tools"),
    ("QUICKSTART.md", r"exposes \d+ MCP tools", "exposes {mcp_tools} MCP tools"),
    ("COMPARISON.md", r"yes \(\d+\+? tools\)", "yes ({mcp_tools} tools)"),
    ("COMPARISON.md", r"exposes \d+\+? tools", "exposes {mcp_tools} tools"),
    ("AGENTS.md", r"\d+\+? commands and \d+\+? aliases", "{cli_commands} commands and {aliases} aliases"),
    ("AGENTS.md", r"~\d+ tools exposing", "{mcp_tools} tools exposing"),
    ("AGENTS.md", r"\d+ tools exposing the framework", "{mcp_tools} tools exposing the framework"),
    ("AGENTS.md", r"full \d+-tool reference", "full {mcp_tools}-tool reference"),
    ("AGENTS.md", r"Complete \d+-tool MCP playbook", "Complete {mcp_tools}-tool MCP playbook"),
    ("AGENTS.md", r"Full \d+\+?[- ]?command reference", "Full {cli_commands}-command reference"),
    ("AGENTS.md", r"`COMMANDS\.md` \| ~\d+", "`COMMANDS.md` | ~1600"),
    ("CLAUDE.md", r"\d+\+? commands \+ \d+\+? aliases", "{cli_commands} commands + {aliases} aliases"),
    ("CLAUDE.md", r"MCP server \(\d+ tools\)", "MCP server ({mcp_tools} tools)"),
    ("CLAUDE.md", r"~\d+ tools\)", "{mcp_tools} tools)"),
    ("CLAUDE.md", r"never all \d+ commands", "never all {bridge_catalog} commands"),
    ("CLAUDE.md", r"\d+ MCP tools\.", "{mcp_tools} MCP tools."),
    ("skills/lazyown.md", r"\*\*\d+\+ aliases\*\*", "**{aliases} aliases**"),
    ("skills/lazyown.md", r"\d+ commands, 11 phases", "{bridge_catalog} commands, 11 phases"),
    ("skills/lazyown.md", r"Core MCP Tools \(\d+\)", "Core MCP Tools ({mcp_tools})"),
    ("skills/lazyown.md", r"\d+-command catalog", "{bridge_catalog}-command catalog"),
    ("README.md", r"over \d+ attack techniques", "over {cli_hundreds} attack techniques"),
    ("README.md", r"exposes \d+ tools", "exposes {mcp_tools} tools"),
    ("README.md", r"exposes \d+ LazyOwn tools", "exposes {mcp_tools} LazyOwn tools"),
    ("README.md", r"MCP Tool Groups \(\d+ tools\)", "MCP Tool Groups ({mcp_tools} tools)"),
)


def canonical_command_count(root: Path = REPO_ROOT) -> int:
    """Read the canonical command count from the committed command index.

    The command index (``cli/command_index.json``) is the single source of
    truth produced by ``scripts/build_command_index.py``. Re-counting the
    AST here would reintroduce a second counting method and cause the same
    drift this module exists to eliminate.
    """
    index_path = root / "cli" / "command_index.json"
    document = json.loads(index_path.read_text(encoding="utf-8"))
    return int(document["totals"]["unique_commands"])


def measure_stats(root: Path = REPO_ROOT) -> dict[str, int]:
    """Measure every published count from the live tree.

    Args:
        root: Repository root. Injectable so tests can point at a fixture.
    """
    mcp_source = (root / "skills" / "lazyown_mcp.py").read_text(encoding="utf-8")
    bridge_source = (root / "modules" / "lazyown_bridge.py").read_text(encoding="utf-8")
    aliases = yaml.safe_load((root / "cli" / "aliases.yaml").read_text(encoding="utf-8"))
    cli_commands = canonical_command_count(root)
    return {
        "cli_commands": cli_commands,
        "cli_hundreds": (cli_commands // 100) * 100,
        "bridge_catalog": bridge_source.count("CatalogEntry("),
        "mcp_tools": len(re.findall(r'name="lazyown_', mcp_source)),
        "aliases": len(aliases or {}),
        "addons": len(list((root / "lazyaddons").glob("*.yaml"))),
        "plugins": len(list((root / "plugins").glob("*.lua"))),
        "playbooks": len(list((root / "playbooks").glob("*.yaml"))),
    }


def render(template: str, stats: dict[str, int]) -> str:
    """Format one replacement template with the measured stats."""
    return template.format(**stats)


def sync(check: bool, stats: dict[str, int], root: Path = REPO_ROOT) -> list[str]:
    """Apply or verify every replacement; return the list of stale spots.

    Args:
        check: When ``True`` verify without writing, returning stale spots.
        stats: Measured counts produced by :func:`measure_stats`.
        root: Repository root. Injectable so tests can point at a fixture.
    """
    stale: list[str] = []
    for doc, pattern, template in REPLACEMENTS:
        path = root / doc
        if not path.is_file():
            stale.append(f"{doc}: missing file for pattern {pattern!r}")
            continue
        text = path.read_text(encoding="utf-8")
        replacement = render(template, stats)
        updated = re.sub(pattern, replacement, text)
        if updated != text:
            stale.append(f"{doc}: /{pattern}/ -> {replacement!r}")
            if not check:
                path.write_text(updated, encoding="utf-8")
    return stale


def main() -> int:
    """CLI entry point."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="verify docs are in sync, exit 1 when stale")
    parser.add_argument("--print", dest="print_only", action="store_true", help="print measured stats only")
    args = parser.parse_args()

    stats = measure_stats()
    if args.print_only:
        for key, value in stats.items():
            print(f"{key}={value}")
        return 0

    stale = sync(check=args.check, stats=stats)
    if args.check and stale:
        print("Doc stats out of sync — run scripts/sync_doc_stats.py:")
        for spot in stale:
            print(f"  {spot}")
        return 1
    if not args.check:
        print(f"Synced {len(stale)} spot(s) across docs.")
        for spot in stale:
            print(f"  {spot}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
