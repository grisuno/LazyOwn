"""Generate ``cli/command_index.json`` from a static AST scan.

This script is the single source of truth for the operator-facing command
catalogue. It walks ``lazyown.py`` and every ``cli/commands/*.py`` module,
extracts every direct ``do_<name>`` method on a class body, and emits a
deterministic JSON document that the CLI palette, the C2 ``/palette``
endpoint and the MCP ``lazyown_palette`` tool all consume.

The output is committed to the repository so:

- ``run/test`` cycles do not need to re-parse 27k LOC of ``lazyown.py``;
- the file diff itself is the contract that protects against accidental
  command loss during the Tier 3 migration.

Usage:
    python3 scripts/build_command_index.py            # write cli/command_index.json
    python3 scripts/build_command_index.py --check    # exit 1 if regen needed
    python3 scripts/build_command_index.py --stdout   # print, do not write
"""

from __future__ import annotations

import argparse
import ast
import hashlib
import json
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterable

REPO_ROOT = Path(__file__).resolve().parent.parent
LAZYOWN_PATH = REPO_ROOT / "lazyown.py"
CLI_COMMANDS_DIR = REPO_ROOT / "cli" / "commands"
GRAPH_JSON_PATH = REPO_ROOT / "graphify-out" / "graph_lazyown.json"
OUTPUT_PATH = REPO_ROOT / "cli" / "command_index.json"
SCHEMA_VERSION = 1

CONSTANT_TO_CATEGORY: dict[str, str] = {
    "recon_category": "01. Reconnaissance",
    "scanning_category": "02. Scanning & Enumeration",
    "exploitation_category": "03. Exploitation",
    "post_exploitation_category": "04. Post-Exploitation",
    "persistence_category": "05. Persistence",
    "privilege_escalation_category": "06. Privilege Escalation",
    "credential_access_category": "07. Credential Access",
    "lateral_movement_category": "08. Lateral Movement",
    "exfiltration_category": "09. Data Exfiltration",
    "command_and_control_category": "10. Command & Control",
    "reporting_category": "11. Reporting",
    "miscellaneous_category": "12. Miscellaneous",
    "ai": "16. Artificial Intelligence",
}

CATEGORY_TO_PHASE: dict[str, str] = {
    "01. Reconnaissance": "recon",
    "02. Scanning & Enumeration": "enum",
    "03. Exploitation": "exploit",
    "04. Post-Exploitation": "postexp",
    "05. Persistence": "persist",
    "06. Privilege Escalation": "privesc",
    "07. Credential Access": "cred",
    "08. Lateral Movement": "lateral",
    "09. Data Exfiltration": "exfil",
    "10. Command & Control": "c2",
    "11. Reporting": "report",
    "12. Miscellaneous": "misc",
    "13. Lua Plugin": "plugin",
    "14. Yaml Addon.": "addon",
    "15. Adversary YAML.": "adversary",
    "16. Artificial Intelligence": "ai",
    "Diagnostics": "diagnostics",
}

UNCATEGORIZED_PHASE = "uncategorized"
SUMMARY_MAX_CHARS = 160


@dataclass
class Command:
    """A single operator-visible command entry."""

    name: str
    line: int
    summary: str
    category: str | None
    phase: str
    source_file: str
    class_name: str
    community: int | None = None
    duplicate_of: str | None = None


@dataclass
class IndexBuildResult:
    """Aggregate output of :func:`build_index`."""

    commands: list[Command]
    duplicates: list[dict[str, Any]] = field(default_factory=list)
    sources: list[str] = field(default_factory=list)
    source_sha256: dict[str, str] = field(default_factory=dict)


def _iter_class_defs(tree: ast.Module) -> Iterable[ast.ClassDef]:
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            yield node


def _resolve_category(decorators: list[ast.expr]) -> str | None:
    """Return the cmd2 category string for a method, if any.

    Recognised forms:

    - ``@cmd2.with_category(recon_category)`` → resolved via
      :data:`CONSTANT_TO_CATEGORY`.
    - ``@cmd2.with_category("13. Lua Plugin")`` → returned literally.
    - ``@with_category(...)`` → same shapes.
    """
    for dec in decorators:
        if not isinstance(dec, ast.Call):
            continue
        target = dec.func
        if isinstance(target, ast.Attribute) and target.attr == "with_category":
            pass
        elif isinstance(target, ast.Name) and target.id == "with_category":
            pass
        else:
            continue
        if not dec.args:
            continue
        arg = dec.args[0]
        if isinstance(arg, ast.Constant) and isinstance(arg.value, str):
            return arg.value
        if isinstance(arg, ast.Name):
            return CONSTANT_TO_CATEGORY.get(arg.id)
    return None


def _summary_from_docstring(node: ast.FunctionDef | ast.AsyncFunctionDef) -> str:
    doc = ast.get_docstring(node) or ""
    first_line = next((line.strip() for line in doc.splitlines() if line.strip()), "")
    if len(first_line) > SUMMARY_MAX_CHARS:
        first_line = first_line[: SUMMARY_MAX_CHARS - 1] + "…"
    return first_line


def _collect_commands_from_file(path: Path) -> list[Command]:
    src = path.read_text(encoding="utf-8")
    tree = ast.parse(src, filename=str(path))
    relpath = str(path.relative_to(REPO_ROOT))
    out: list[Command] = []
    for cls in _iter_class_defs(tree):
        for child in cls.body:
            if not isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef)):
                continue
            if not child.name.startswith("do_"):
                continue
            category = _resolve_category(list(child.decorator_list))
            phase = CATEGORY_TO_PHASE.get(category or "", UNCATEGORIZED_PHASE)
            out.append(
                Command(
                    name=child.name,
                    line=child.lineno,
                    summary=_summary_from_docstring(child),
                    category=category,
                    phase=phase,
                    source_file=relpath,
                    class_name=cls.name,
                )
            )
    return out


def _annotate_communities(commands: list[Command], graph_path: Path) -> None:
    """Fill ``Command.community`` from ``graphify-out/graph_lazyown.json``.

    Graphify identifies methods by node id ``lazyown_do_<name>``. When the
    graph file is absent or a name has no node, the community stays ``None``.
    """
    if not graph_path.exists():
        return
    try:
        graph = json.loads(graph_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return
    by_label: dict[str, int] = {}
    for node in graph.get("nodes", []):
        label = node.get("label", "")
        if isinstance(label, str) and label.startswith("do_") and label.endswith("()"):
            name = label[:-2]
            community = node.get("community")
            if isinstance(community, int):
                by_label[name] = community
    for cmd in commands:
        if cmd.name in by_label:
            cmd.community = by_label[cmd.name]


def _detect_duplicates(commands: list[Command]) -> list[dict[str, Any]]:
    """Group commands sharing a name and return the duplicate report.

    Mutates each duplicate ``Command`` so its ``duplicate_of`` points at the
    canonical name (the command itself); the first occurrence is left
    untouched so consumers can pick a deterministic winner.
    """
    seen: dict[str, list[Command]] = {}
    for cmd in commands:
        seen.setdefault(cmd.name, []).append(cmd)
    duplicates: list[dict[str, Any]] = []
    for name, group in seen.items():
        if len(group) <= 1:
            continue
        for cmd in group[1:]:
            cmd.duplicate_of = name
        duplicates.append(
            {
                "name": name,
                "occurrences": [
                    {"line": c.line, "source_file": c.source_file, "class_name": c.class_name} for c in group
                ],
            }
        )
    duplicates.sort(key=lambda d: d["name"])
    return duplicates


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    digest.update(path.read_bytes())
    return digest.hexdigest()


def build_index() -> IndexBuildResult:
    """Build the in-memory index from ``lazyown.py`` + ``cli/commands/``."""
    sources: list[Path] = [LAZYOWN_PATH]
    if CLI_COMMANDS_DIR.is_dir():
        for child in sorted(CLI_COMMANDS_DIR.iterdir()):
            if child.suffix != ".py":
                continue
            if child.name.startswith("_"):
                continue
            sources.append(child)
    commands: list[Command] = []
    sha_map: dict[str, str] = {}
    for path in sources:
        commands.extend(_collect_commands_from_file(path))
        sha_map[str(path.relative_to(REPO_ROOT))] = _sha256(path)
    commands.sort(key=lambda c: (c.source_file, c.line))
    duplicates = _detect_duplicates(commands)
    _annotate_communities(commands, GRAPH_JSON_PATH)
    return IndexBuildResult(
        commands=commands,
        duplicates=duplicates,
        sources=[str(p.relative_to(REPO_ROOT)) for p in sources],
        source_sha256=sha_map,
    )


def render_document(result: IndexBuildResult) -> dict[str, Any]:
    """Serialise the build result into the on-disk JSON shape."""
    by_phase: dict[str, list[str]] = {}
    by_category: dict[str, list[str]] = {}
    unique_names: set[str] = set()
    for cmd in result.commands:
        unique_names.add(cmd.name)
        by_phase.setdefault(cmd.phase, []).append(cmd.name)
        if cmd.category:
            by_category.setdefault(cmd.category, []).append(cmd.name)
    for bucket in (by_phase, by_category):
        for key in bucket:
            bucket[key] = sorted(set(bucket[key]))
    return {
        "schema_version": SCHEMA_VERSION,
        "sources": result.sources,
        "source_sha256": result.source_sha256,
        "totals": {
            "method_definitions": len(result.commands),
            "unique_commands": len(unique_names),
            "duplicates": len(result.duplicates),
            "phases": len(by_phase),
            "categories": len(by_category),
        },
        "phase_to_commands": by_phase,
        "category_to_commands": by_category,
        "duplicates": result.duplicates,
        "commands": [
            {
                "name": c.name,
                "line": c.line,
                "summary": c.summary,
                "category": c.category,
                "phase": c.phase,
                "source_file": c.source_file,
                "class_name": c.class_name,
                "community": c.community,
                "duplicate_of": c.duplicate_of,
            }
            for c in result.commands
        ],
    }


def write_document(document: dict[str, Any], output_path: Path = OUTPUT_PATH) -> None:
    """Atomically write the JSON document with a trailing newline."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(document, indent=2, sort_keys=False, ensure_ascii=False) + "\n"
    tmp = output_path.with_suffix(output_path.suffix + ".tmp")
    tmp.write_text(payload, encoding="utf-8")
    tmp.replace(output_path)


def _parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--check",
        action="store_true",
        help="Exit 1 if the on-disk index does not match a fresh build.",
    )
    parser.add_argument(
        "--stdout",
        action="store_true",
        help="Print the JSON document to stdout instead of writing it.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = _parse_args(argv)
    document = render_document(build_index())
    if args.stdout:
        sys.stdout.write(json.dumps(document, indent=2, ensure_ascii=False) + "\n")
        return 0
    if args.check:
        if not OUTPUT_PATH.exists():
            sys.stderr.write(f"ERROR: {OUTPUT_PATH.relative_to(REPO_ROOT)} missing\n")
            return 1
        on_disk = json.loads(OUTPUT_PATH.read_text(encoding="utf-8"))
        if on_disk != document:
            sys.stderr.write("ERROR: command index out of date — run 'python3 scripts/build_command_index.py'\n")
            return 1
        return 0
    write_document(document)
    sys.stdout.write(
        f"wrote {OUTPUT_PATH.relative_to(REPO_ROOT)}: "
        f"{document['totals']['unique_commands']} unique commands, "
        f"{document['totals']['duplicates']} duplicates, "
        f"{document['totals']['phases']} phases\n"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
