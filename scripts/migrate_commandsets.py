"""Merge _migrated.py CommandSet methods into clean phase modules.

Reads each ``*_migrated.py`` file under ``cli/commands/``, identifies
``do_*`` methods not yet present in the corresponding clean ``.py`` file,
and appends them. The clean file keeps its existing base class
(LazyOwnCommandSet or PendingCommandSet) unchanged; only new methods
are added.

Usage:
    python3 scripts/migrate_commandsets.py [--dry-run] [--phase scan]

Without ``--phase``, processes every pending phase.
"""

from __future__ import annotations

import argparse
import ast
import os
import sys

CLI_COMMANDS_DIR = os.path.join(os.path.dirname(__file__), "..", "cli", "commands")

_PHASE_MIGRATED = {
    "scan": "scan_migrated.py",
    "recon": "recon_migrated.py",
    "exploit": "exploit_migrated.py",
    "lateral": "lateral_migrated.py",
    "persist": "persist_migrated.py",
    "postexp": "postexp_migrated.py",
    "cred": "cred_migrated.py",
    "command_and_control": "command_and_control_migrated.py",
    "report": "report_migrated.py",
    "misc": "misc_migrated.py",
}


def _extract_method_source(source: str, method_name: str) -> str | None:
    """Extract the source block for *method_name* from Python source string."""
    try:
        tree = ast.parse(source)
    except SyntaxError:
        return None
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name == method_name:
            lines = source.splitlines()
            block = "\n".join(lines[node.lineno - 1 : node.end_lineno])
            return block
    return None


def _method_names_from_file(filepath: str) -> set[str]:
    """Return the set of ``do_*`` method names defined in *filepath*."""
    if not os.path.isfile(filepath):
        return set()
    with open(filepath, encoding="utf-8") as fh:
        source = fh.read()
    names: set[str] = set()
    try:
        tree = ast.parse(source)
    except SyntaxError:
        return names
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name.startswith("do_"):
            names.add(node.name)
    return names


def _find_class_end(source_lines: list[str]) -> int:
    """Return the zero-based line index of the last line inside the module-level class."""
    for i, line in enumerate(source_lines):
        if line.startswith("class "):
            indent = len(line) - len(line.lstrip())
            for j in range(i + 1, len(source_lines)):
                stripped = source_lines[j].strip()
                current_indent = len(source_lines[j]) - len(source_lines[j].lstrip())
                if stripped and current_indent <= indent:
                    return j
            return len(source_lines) - 1
    return len(source_lines)


def _append_methods(clean_path: str, methods: dict[str, str]) -> tuple[bool, int]:
    """Append *methods* to the clean file. Returns (changed, count_added)."""
    if not os.path.isfile(clean_path):
        print(f"  [SKIP] {os.path.basename(clean_path)} does not exist")
        return False, 0

    existing = _method_names_from_file(clean_path)
    new_names = {n for n in methods if n not in existing}
    if not new_names:
        return False, 0

    with open(clean_path, encoding="utf-8") as fh:
        source_lines = fh.readlines()

    class_end = _find_class_end(source_lines)
    insert_pos = min(class_end, len(source_lines))

    print(f"  Adding {len(new_names)} methods to {os.path.basename(clean_path)}...")
    for name in sorted(new_names):
        block = methods[name]
        chunk_lines = ["    # --- migrated\n"]
        for line in block.splitlines(True):
            chunk_lines.append(line if line.startswith(" ") else f"    {line}")
        chunk_lines.append("\n")
        for line in reversed(chunk_lines):
            source_lines.insert(insert_pos, line)
        insert_pos += len(chunk_lines)
        print(f"    + {name}")

    with open(clean_path, "w", encoding="utf-8") as fh:
        fh.writelines(source_lines)
    return True, len(new_names)


def merge_phase(phase: str, dry_run: bool = False) -> bool:
    """Merge one phase's migrated methods into its clean file. Returns True if changed."""
    migrated_filename = _PHASE_MIGRATED.get(phase)
    if not migrated_filename:
        print(f"[SKIP] unknown phase: {phase}")
        return False
    migrated_path = os.path.join(CLI_COMMANDS_DIR, migrated_filename)
    clean_path = os.path.join(CLI_COMMANDS_DIR, f"{phase}.py")
    if not os.path.isfile(migrated_path):
        print(f"[SKIP] {migrated_filename} not found")
        return False
    if not os.path.isfile(clean_path):
        print(f"[SKIP] {phase}.py not found")
        return False

    existing = _method_names_from_file(clean_path)
    with open(migrated_path, encoding="utf-8") as fh:
        source = fh.read()

    migrated = {n for n in _method_names_from_file(migrated_path) if n.startswith("do_")}
    missing = migrated - existing
    if not missing:
        print(f"[OK] {phase}: all {len(migrated)} methods already in {phase}.py")
        return False

    print(f"[MERGE] {phase}: {len(existing)} in clean, {len(migrated)} in migrated, {len(missing)} missing")

    methods: dict[str, str] = {}
    for name in sorted(missing):
        block = _extract_method_source(source, name)
        if block:
            methods[name] = block

    if dry_run:
        print(f"  Would add: {', '.join(sorted(methods.keys()))}")
        return bool(methods)

    changed, count = _append_methods(clean_path, methods)
    return changed


def main() -> None:
    parser = argparse.ArgumentParser(description="Merge _migrated.py methods into clean CommandSet files")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be done without writing")
    parser.add_argument("--phase", help="Process a single phase (e.g., scan, exploit)")
    args = parser.parse_args()

    os.chdir(os.path.join(os.path.dirname(__file__), ".."))
    sys.path.insert(0, os.getcwd())

    phases = [args.phase] if args.phase else list(_PHASE_MIGRATED)
    total_changed = 0
    for phase in phases:
        if merge_phase(phase, dry_run=args.dry_run):
            total_changed += 1
    print(f"\nDone. {total_changed} phase(s) updated.")


if __name__ == "__main__":
    main()
