#!/usr/bin/env python3
"""Activate dormant CommandSet migrations.

Usage: python3 scripts/activate_migrations.py [--dry-run] [--phase <name>]

Scans cli/commands/*_migrated.py files that use PendingCommandSet,
finds the corresponding do_* methods in lazyown.py, removes them,
and changes the base class to LazyOwnCommandSet.

When the originals are deleted from lazyown.py, the migrated CommandSets
activate automatically on next shell start via cli.registry.
"""

from __future__ import annotations

import ast
import sys
from pathlib import Path
from typing import Any

BASE_DIR = Path(__file__).resolve().parent.parent
CLI_COMMANDS = BASE_DIR / "cli" / "commands"
LAZYOWN_PY = BASE_DIR / "lazyown.py"

PENDING_IMPORT = "from cli.commands._dormancy import PendingCommandSet"
ACTIVE_IMPORT = "from cli.commands._base import LazyOwnCommandSet"


class MigrationError(Exception):
    pass


def find_migrated_sets() -> list[Path]:
    """Return paths to all *_migrated.py files using PendingCommandSet."""
    migrated: list[Path] = []
    for path in sorted(CLI_COMMANDS.glob("*_migrated.py")):
        content = path.read_text()
        if "PendingCommandSet" in content:
            migrated.append(path)
    return migrated


def extract_command_names(migrated_path: Path) -> set[str]:
    """Extract do_* method names from a migrated CommandSet file."""
    tree = ast.parse(migrated_path.read_text())
    names: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name.startswith("do_"):
            names.add(node.name)
    return names


def find_in_lazyown(command_names: set[str]) -> dict[str, tuple[int, int]]:
    """Return {name: (start_line, end_line)} for commands in lazyown.py."""
    tree = ast.parse(LAZYOWN_PY.read_text())
    locations: dict[str, tuple[int, int]] = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name in command_names:
            locations[node.name] = (node.lineno, node.end_lineno or node.lineno)
    return locations


def remove_from_lazyown(locations: dict[str, tuple[int, int]], dry_run: bool = False) -> int:
    """Remove the specified do_* methods from lazyown.py. Returns count removed."""
    lines = LAZYOWN_PY.read_text().splitlines(keepends=True)
    ranges_to_remove = sorted(locations.values(), reverse=True)
    removed = 0
    for start, end in ranges_to_remove:
        del lines[start - 1 : end]
        removed += 1
    if not dry_run and removed:
        LAZYOWN_PY.write_text("".join(lines))
    return removed


def activate_migrated_file(migrated_path: Path, dry_run: bool = False) -> bool:
    """Change PendingCommandSet to LazyOwnCommandSet in the migrated file."""
    content = migrated_path.read_text()
    new_content = content.replace(PENDING_IMPORT, ACTIVE_IMPORT)
    if "PendingCommandSet" in new_content:
        new_content = new_content.replace("PendingCommandSet", "LazyOwnCommandSet")
    if new_content == content:
        return False
    if not dry_run:
        migrated_path.write_text(new_content)
    return True


def main() -> None:
    dry_run = "--dry-run" in sys.argv
    phase_filter = None
    for i, arg in enumerate(sys.argv):
        if arg == "--phase" and i + 1 < len(sys.argv):
            phase_filter = sys.argv[i + 1]

    migrated_files = find_migrated_sets()
    if not migrated_files:
        print("[*] No dormant migrated CommandSets found.")
        return

    print(f"[*] Found {len(migrated_files)} dormant migrated CommandSet(s):\n")

    for path in migrated_files:
        if phase_filter and phase_filter not in path.stem:
            continue

        commands = extract_command_names(path)
        if not commands:
            print(f"  {path.stem}: no do_* methods found")
            continue

        locations = find_in_lazyown(commands)
        in_lazyown = set(locations.keys())
        not_in_lazyown = commands - in_lazyown

        print(f"  {path.stem}:")
        print(f"      Commands: {len(commands)}")
        print(f"      In lazyown.py: {len(in_lazyown)}")
        if not_in_lazyown:
            print(f"      Already deleted: {len(not_in_lazyown)} ({', '.join(sorted(not_in_lazyown))[:80]})")

        if dry_run:
            print(f"      [DRY RUN] Would remove {len(in_lazyown)} commands from lazyown.py")
            print(f"      [DRY RUN] Would activate {path.stem}")
        else:
            removed = remove_from_lazyown(locations, dry_run=False)
            activated = activate_migrated_file(path, dry_run=False)
            print(f"      Removed from lazyown.py: {removed} commands")
            print(f"      Activated CommandSet: {activated}")

        print()

    if dry_run:
        print("[DRY RUN] No changes were made. Remove --dry-run to apply.")
    else:
        print("[*] Migration activation complete. Restart the shell (./run) to apply.")


if __name__ == "__main__":
    main()
