"""Subprocess ratchet: raw process-execution sites may only go down.

Counts every operator-side ``subprocess.run/call/check_output/check_call/
Popen``, ``os.system`` and ``os.popen`` call site across the first-party
packages and asserts the count never regrows. The ceiling is the count at
ratchet adoption; a refactor that removes sites must LOWER the ceiling in
the same change.

Excluded by design:
- ``core/safe_exec.py`` / ``core/safe_subprocess.py`` / ``core/process.py``
  (the canonical execution helpers themselves),
- ``modules/cgi-bin/`` (intentional pentest artefacts),
- payload STRING literals are not call sites (AST-based scan).
"""

from __future__ import annotations

import ast
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

SCAN_DIRS = ("cli", "modules", "lazyc2", "core")
SCAN_FILES = ("utils.py", "lazyown.py")

EXCLUDED_PATH_PARTS = (
    "core/safe_exec.py",
    "core/safe_subprocess.py",
    "core/process.py",
    "modules/cgi-bin/",
)

CALL_NAMES = {"run", "call", "check_output", "check_call", "Popen"}


def _raw_subprocess_sites(tree: ast.AST) -> int:
    count = 0
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        func = node.func
        if isinstance(func, ast.Attribute) and func.attr == "system" and isinstance(func.value, ast.Name):
            if func.value.id == "os":
                count += 1
                continue
        if isinstance(func, ast.Attribute) and func.attr == "popen" and isinstance(func.value, ast.Name):
            if func.value.id == "os":
                count += 1
                continue
        if isinstance(func, ast.Attribute) and func.attr in CALL_NAMES:
            owner = func.value
            if isinstance(owner, ast.Name) and owner.id == "subprocess":
                count += 1
    return count


def _iter_sources():
    for name in SCAN_FILES:
        yield ROOT / name
    for directory in SCAN_DIRS:
        base = ROOT / directory
        if not base.is_dir():
            continue
        yield from base.rglob("*.py")


def test_raw_subprocess_sites_never_regrow():
    total = 0
    per_file: dict[str, int] = {}
    for path in _iter_sources():
        rel = str(path.relative_to(ROOT)).replace("\\", "/")
        if any(part in rel for part in EXCLUDED_PATH_PARTS):
            continue
        try:
            tree = ast.parse(path.read_text(encoding="utf-8", errors="replace"))
        except SyntaxError:
            continue
        sites = _raw_subprocess_sites(tree)
        if sites:
            per_file[rel] = sites
            total += sites

    assert 0 < total, "ratchet lost its signal: no subprocess sites counted"
    assert total <= 360, (
        f"raw subprocess sites regrew: {total} > 360 ceiling. "
        "Route new execution through core.safe_exec.safe_run_argv / safe_run_shell "
        "or lower the ceiling when you remove sites. Top offenders: "
        + ", ".join(f"{k}={v}" for k, v in sorted(per_file.items(), key=lambda kv: -kv[1])[:5])
    )
