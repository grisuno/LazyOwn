"""Contract conformance checker for single-file LAZY port modules.

Usage:
    python3 /tmp/opencode/contract_check.py modules/intercept.py [files...]

Checks: docstrings on public classes and functions, no absolute
operator paths, presence of a Config class, no emoji bytes.
"""

from __future__ import annotations

import ast
import sys
from pathlib import Path

BANNED_PREFIXES = ("/home/", "/Users/", "/root/", "C:\\", "C:/")


def check_file(path: Path) -> list[str]:
    """Validate one module and return human readable violations."""
    violations: list[str] = []
    text = path.read_text(encoding="utf-8")
    if any(b in text for b in BANNED_PREFIXES):
        violations.append(f"{path}: absolute operator path detected")
    try:
        tree = ast.parse(text)
    except SyntaxError as exc:
        return [f"{path}: syntax error {exc}"]
    has_config = any(isinstance(n, ast.ClassDef) and "Config" in n.name
                     for n in tree.body)
    if not has_config:
        violations.append(f"{path}: missing Config class")
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
            if node.name.startswith("_"):
                continue
            if ast.get_docstring(node) is None:
                violations.append(f"{path}: {node.name} lacks docstring")
    try:
        text.encode("ascii")
    except UnicodeEncodeError:
        violations.append(f"{path}: non-ascii bytes present")
    return violations


def main(argv: list[str]) -> int:
    """Check each file argument and report violations."""
    targets = argv[1:] or []
    if not targets:
        print("usage: contract_check.py FILE [FILE ...]")
        return 2
    failures: list[str] = []
    for raw in targets:
        failures.extend(check_file(Path(raw)))
    if failures:
        for item in failures:
            print(item)
        return 1
    print(f"OK: {len(targets)} file(s) conform")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
