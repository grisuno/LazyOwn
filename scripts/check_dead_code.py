#!/usr/bin/env python3
"""AST dead-code detector for the LazyOwn repo.

Reports zero-reference functions and methods. Reachability by
convention is honoured: ``do_*`` (cmd2 commands), ``run_*`` (the
``run <name>`` script dispatch on the shell), ``action_*``/``on_*``
(cmd2), ``complete_*``, dunders and decorated registration surfaces
are never reported. The remaining candidates are checked against
every code surface that can reach them: Python sources, lazyaddon /
plugin / gym / playbook / chain YAML, ``.ls`` scripts, docs and the
payload.

Usage:
    python3 scripts/check_dead_code.py [--json PATH]

Exit codes:
    0 - no dead candidates
    1 - candidates found (CI gate)
"""

from __future__ import annotations

import argparse
import ast
import json
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

EXCLUDED_DIRS = {
    ".git",
    "__pycache__",
    "build",
    "dist",
    "node_modules",
    "readmenator-agent",
    "readmenator-maps",
    "readmenator-wiki",
    "readmenator-diagrams",
    "sessions",
    "venv",
    ".venv",
    "venv_telegram",
    "env",
    "external",
    "contrib",
    "runs",
}

SURFACE_SUFFIXES = {".yaml", ".yml", ".ls", ".json", ".md", ".html"}

DYNAMIC_PREFIXES = ("do_", "run_", "action_", "on_", "complete_", "postcmd", "precmd", "__", "test_")

REGISTRATION_DECORATORS = {
    "route",
    "app_template_filter",
    "app_template_global",
    "app_errorhandler",
    "contextprocessor",
    "with_category",
    "command",
    "cli",
    "tool",
    "mcp_tool",
    "property",
    "setter",
    "pytest",
    "fixture",
    "abstractmethod",
    "overload",
    "dataclass",
    "total_ordering",
    "contextmanager",
    "cached_property",
    "register",
    "receiver",
    "task",
    "shared_task",
    "app_task",
}

_WORD_RE = re.compile(r"\w+")


@dataclass(frozen=True)
class Candidate:
    file: str
    line: int
    name: str
    kind: str


def _excluded(path: Path) -> bool:
    return any(part in EXCLUDED_DIRS for part in path.parts)


def iter_py_files() -> list[Path]:
    return sorted(p for p in ROOT.rglob("*.py") if not _excluded(p))


def iter_surface_files() -> list[Path]:
    out = set()
    for suffix in SURFACE_SUFFIXES:
        out.update(p for p in ROOT.rglob(f"*{suffix}") if not _excluded(p))
    return sorted(out)


def is_registered(node: ast.FunctionDef | ast.AsyncFunctionDef) -> bool:
    for dec in node.decorator_list:
        label = ""
        if isinstance(dec, ast.Name):
            label = dec.id
        elif isinstance(dec, ast.Attribute):
            label = dec.attr
        elif isinstance(dec, ast.Call):
            inner = dec.func
            if isinstance(inner, ast.Name):
                label = inner.id
            elif isinstance(inner, ast.Attribute):
                label = inner.attr
        if label and label in REGISTRATION_DECORATORS:
            return True
    return False


def is_dynamic(name: str) -> bool:
    return any(name.startswith(prefix) for prefix in DYNAMIC_PREFIXES)


def collect_candidates(tree: ast.Module, rel: str) -> list[Candidate]:
    found: list[Candidate] = []

    def visit_body(body: list[ast.stmt], class_name: str) -> None:
        for node in body:
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                name = node.name
                if not is_dynamic(name) and not is_registered(node):
                    kind = f"{class_name}.{name}" if class_name else name
                    found.append(Candidate(rel, node.lineno, name, kind))
                visit_body(node.body, class_name)
            elif isinstance(node, ast.ClassDef):
                visit_body(node.body, node.name)

    visit_body(tree.body, "")
    return found


def collect_identifiers(tree: ast.Module) -> set[str]:
    seen: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Name):
            seen.add(node.id)
        elif isinstance(node, ast.Attribute):
            seen.add(node.attr)
    return seen


def main() -> int:
    parser = argparse.ArgumentParser(description="Dead-code detector")
    parser.add_argument("--json", dest="json_path", default="", help="Write report JSON")
    args = parser.parse_args()

    candidates: list[Candidate] = []
    referenced: set[str] = set()
    for path in iter_py_files():
        try:
            source = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        rel = str(path.relative_to(ROOT))
        try:
            tree = ast.parse(source)
        except SyntaxError:
            continue
        candidates.extend(collect_candidates(tree, rel))
        referenced |= collect_identifiers(tree)

    candidate_names = {c.name for c in candidates}
    for path in iter_surface_files():
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        referenced.update(_WORD_RE.findall(text))

    dead = [c for c in candidates if c.name not in referenced]
    dead.sort(key=lambda c: (c.file, c.line))
    report = [asdict(c) for c in dead]
    if args.json_path:
        Path(args.json_path).write_text(json.dumps(report, indent=2), encoding="utf-8")
    for cand in dead:
        print(f"{cand.file}:{cand.line}: {cand.kind}")
    print(f"\n{len(dead)} dead candidates (dynamic-dispatch aware)")
    return 1 if dead else 0


if __name__ == "__main__":
    sys.exit(main())
