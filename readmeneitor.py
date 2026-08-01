#!/usr/bin/env python3
"""
readmeneitor.py — Automated documentation generator for LazyOwn RedTeam Framework.

Author: Gris Iscomeback
Email: grisiscomeback[at]gmail[dot]com
Creation date: 09/06/2024
License: GPL v3

Description: Scans all do_* methods across cli/commands/ and lazyown.py via AST,
augments metadata from cli/command_index.json, and generates a categorized
COMMANDS.md reference organized by kill-chain phase.

█████╗      █████╗ ███████╗██╗   ██╗ ██████╗ ██╗    ██╗███╗   ██╗
██╔══██╗   ██╔══██╗╚══███╔╝╚██╗ ██╔╝██╔═══██╗██║    ██║████╗  ██║
███████║   ███████║  ███╔╝  ╚████╔╝ ██║   ██║██║ █╗ ██║██╔██╗ ██║
██╔══██║   ██╔══██║ ███╔╝    ╚██╔╝  ██║   ██║██║███╗██║██║╚██╗██║
██║  ██║   ██║  ██║███████╗   ██║   ╚██████╔╝╚███╔███╔╝██║ ╚████║
╚═╝  ╚═╝   ╚═╝  ╚═╝╚══════╝   ╚═╝    ╚═════╝  ╚══╝╚══╝ ╚═╝  ╚═══╝
"""

from __future__ import annotations

import ast
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parent
COMMANDS_DIR = PROJECT_ROOT / "cli" / "commands"
COMMAND_INDEX_PATH = PROJECT_ROOT / "cli" / "command_index.json"
DOCS_DIR = PROJECT_ROOT / "docs"
DEFAULT_OUTPUT = PROJECT_ROOT / "COMMANDS.md"

PHASE_ORDER: dict[str, str] = {
    "recon": "01",
    "enum": "02",
    "exploit": "03",
    "postexp": "04",
    "persist": "05",
    "privesc": "06",
    "cred": "07",
    "lateral": "08",
    "exfil": "09",
    "c2": "10",
    "report": "11",
    "misc": "12",
    "diagnostics": "13",
    "uncategorized": "zz",
}

PHASE_TITLES: dict[str, str] = {
    "recon": "01. Reconnaissance",
    "enum": "02. Scanning & Enumeration",
    "exploit": "03. Exploitation",
    "postexp": "04. Post-Exploitation",
    "persist": "05. Persistence",
    "privesc": "06. Privilege Escalation",
    "cred": "07. Credential Access",
    "lateral": "08. Lateral Movement",
    "exfil": "09. Data Exfiltration",
    "c2": "10. Command & Control",
    "report": "11. Reporting",
    "misc": "12. Miscellaneous",
    "diagnostics": "13. Diagnostics",
    "uncategorized": "Uncategorized",
}


def load_command_index(index_path: Path) -> dict[str, Any]:
    """Load and parse the command index JSON file.

    Args:
        index_path: Path to cli/command_index.json.

    Returns:
        Parsed JSON dictionary. Returns an empty dict if the file is missing
        or contains invalid JSON.
    """
    try:
        with open(index_path, "r", encoding="utf-8") as fh:
            return json.load(fh)
    except FileNotFoundError:
        print(f"[!] Command index not found at {index_path}, continuing without metadata.")
        return {}
    except json.JSONDecodeError as exc:
        print(f"[!] Invalid JSON in command index: {exc}")
        return {}


def build_command_map(index_data: dict[str, Any]) -> dict[str, dict[str, Any]]:
    """Build a lookup dict from command name to its metadata.

    Combines the ``commands`` list with ``phase_to_commands`` to assign
    every command a phase, category, and summary.

    Args:
        index_data: The parsed command_index.json content.

    Returns:
        Dict mapping ``do_<name>`` to a metadata dict with keys:
        ``phase``, ``summary``, ``source_file``.
    """
    cmd_map: dict[str, dict[str, Any]] = {}

    for entry in index_data.get("commands", []):
        name = entry.get("name", "")
        if not name:
            continue
        cmd_map[name] = {
            "phase": entry.get("phase", "uncategorized"),
            "summary": entry.get("summary", ""),
            "source_file": entry.get("source_file", ""),
        }

    return cmd_map


def extract_docstrings_from_file(filepath: Path) -> dict[str, str]:
    """Parse a single Python file with AST and extract docstrings of ``do_*`` methods.

    Args:
        filepath: Path to a ``.py`` source file.

    Returns:
        Dict mapping function name (e.g. ``do_ask``) to its docstring.
        Returns an empty dict if the file cannot be parsed.
    """
    try:
        with open(filepath, "r", encoding="utf-8") as fh:
            tree = ast.parse(fh.read(), filename=str(filepath))
    except SyntaxError:
        print(f"[!] Syntax error in {filepath}, skipping.")
        return {}
    except (UnicodeDecodeError, OSError) as exc:
        print(f"[!] Cannot read {filepath}: {exc}")
        return {}

    results: dict[str, str] = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name.startswith("do_"):
            docstring = ast.get_docstring(node)
            if docstring:
                results[node.name] = docstring
    return results


def extract_docstrings_from_dir(dirpath: Path) -> dict[str, str]:
    """Recursively scan a directory for Python files and extract all ``do_*`` docstrings.

    Skips files whose name begins with an underscore and
    ``__pycache__`` directories.

    Args:
        dirpath: Root directory to scan.

    Returns:
        Dict mapping function name to its full docstring.
    """
    all_docstrings: dict[str, str] = {}
    if not dirpath.is_dir():
        print(f"[!] Commands directory not found: {dirpath}")
        return all_docstrings

    for pyfile in sorted(dirpath.rglob("*.py")):
        if pyfile.name.startswith("_") or "__pycache__" in pyfile.parts:
            continue
        docstrings = extract_docstrings_from_file(pyfile)
        all_docstrings.update(docstrings)

    return all_docstrings


def group_commands_by_phase(
    cmd_map: dict[str, dict[str, Any]],
) -> dict[str, list[str]]:
    """Group command names by their kill-chain phase.

    Args:
        cmd_map: Command metadata dict from :func:`build_command_map`.

    Returns:
        Dict mapping phase key to a sorted list of command names (``do_*``).
    """
    groups: dict[str, list[str]] = {}
    for name, meta in cmd_map.items():
        phase = meta.get("phase", "uncategorized")
        groups.setdefault(phase, []).append(name)

    for names in groups.values():
        names.sort()

    return groups


def write_commands_md(
    cmd_map: dict[str, dict[str, Any]],
    docstrings: dict[str, str],
    groups: dict[str, list[str]],
    output_path: Path,
) -> int:
    """Generate COMMANDS.md with a table of contents and per-phase command reference.

    Args:
        cmd_map: Command metadata from command_index.json.
        docstrings: Full docstrings extracted via AST.
        groups: Commands grouped by phase key.
        output_path: Destination file path for COMMANDS.md.

    Returns:
        Total number of unique commands written to the file.
    """
    sorted_phases = sorted(
        groups.keys(),
        key=lambda p: PHASE_ORDER.get(p, f"zz_{p}"),
    )

    total_commands = 0
    with open(output_path, "w", encoding="utf-8") as fh:
        fh.write("# LazyOwn Command Reference\n\n")
        fh.write("Auto-generated by readmeneitor.py from source docstrings ")
        fh.write("and cli/command_index.json.\n\n")

        fh.write("## Table of Contents\n\n")
        for phase in sorted_phases:
            title = PHASE_TITLES.get(phase, phase.capitalize())
            anchor = title.lower().replace(" ", "-").replace(".", "")
            count = len(groups[phase])
            fh.write(f"- [{title}](#{anchor}) ({count} commands)\n")
        fh.write("\n---\n\n")

        for phase in sorted_phases:
            title = PHASE_TITLES.get(phase, phase.capitalize())
            fh.write(f"## {title}\n\n")
            commands = groups[phase]
            total_commands += len(commands)
            for name in commands:
                meta = cmd_map.get(name, {})
                summary = meta.get("summary", "")
                source_file = meta.get("source_file", "")
                docstring = docstrings.get(name, summary)
                display_name = name[3:]

                fh.write(f"### `{display_name}`\n\n")
                fh.write(f"**Phase:** {phase}")

                if source_file:
                    fh.write(f" | **Source:** `{source_file}`")
                fh.write("\n\n")

                if docstring:
                    first_line, _, _ = docstring.partition("\n")
                    fh.write(f"{first_line.strip()}\n\n")
                else:
                    fh.write("No description available.\n\n")
            fh.write("\n")

    print(f"[+] Wrote {total_commands} commands to {output_path}")
    return total_commands


def convert_to_html(md_path: Path, html_path: Path) -> None:
    """Convert the generated Markdown file to HTML using pandoc.

    Args:
        md_path: Path to the source Markdown file.
        html_path: Destination path for the HTML output.
    """
    try:
        result = subprocess.run(
            [
                "pandoc",
                str(md_path),
                "-f", "markdown",
                "-t", "html",
                "-s",
                "-o", str(html_path),
                "--metadata", f"title=LazyOwn Framework Doc: {md_path.name}",
            ],
            capture_output=True,
            text=True,
            timeout=60,
        )
        if result.returncode != 0:
            print(f"[!] pandoc error: {result.stderr.strip()}")
        else:
            print(f"[+] HTML generated at {html_path}")
    except FileNotFoundError:
        print("[!] pandoc not found, skipping HTML generation.")
    except (subprocess.TimeoutExpired, OSError) as exc:
        print(f"[!] pandoc failed: {exc}")


def main() -> None:
    """Entry point: scan sources, load metadata, and generate COMMANDS.md."""
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} lazyown.py")
        print("  Generates COMMANDS.md by scanning lazyown.py and cli/commands/")
        print("  Requires cli/command_index.json for metadata.")
        sys.exit(1)

    target_arg = sys.argv[1]
    if target_arg != "lazyown.py":
        output_path = Path(target_arg.upper().replace(".PY", "") + ".md")
    else:
        output_path = DEFAULT_OUTPUT

    index_data = load_command_index(COMMAND_INDEX_PATH)
    cmd_map = build_command_map(index_data)

    docstrings = extract_docstrings_from_dir(COMMANDS_DIR)

    lazyown_py = PROJECT_ROOT / "lazyown.py"
    if lazyown_py.is_file():
        lazy_docs = extract_docstrings_from_file(lazyown_py)
        docstrings.update(lazy_docs)
        for name in lazy_docs:
            if name not in cmd_map:
                cmd_map[name] = {
                    "phase": "uncategorized",
                    "summary": "",
                    "source_file": "lazyown.py",
                }

    if not cmd_map:
        print("[!] No commands found. Aborting.")
        sys.exit(1)

    groups = group_commands_by_phase(cmd_map)
    total = write_commands_md(cmd_map, docstrings, groups, output_path)

    if total > 0 and output_path.suffix == ".md":
        html_output = output_path.with_suffix(".html")
        try:
            DOCS_DIR.mkdir(parents=True, exist_ok=True)
        except OSError as exc:
            print(f"[!] Cannot create docs/ directory: {exc}")
            return
        convert_to_markdown_html = DOCS_DIR / html_output.name
        convert_to_html(output_path, convert_to_markdown_html)

    print(f"[+] Done. {total} commands documented in {output_path}")


if __name__ == "__main__":
    main()
