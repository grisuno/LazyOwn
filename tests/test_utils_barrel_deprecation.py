"""Deprecation gate for the ``utils`` stdlib barrel.

``utils`` re-exports standard-library modules (``os``, ``json``, ``re``...)
for historical reasons. New code must import them directly; the committed
baseline shrinks as existing call sites migrate, and the gate fails on any
new barrel import. Target: an empty baseline.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
BASELINE_PATH = REPO_ROOT / "tests" / "utils_barrel_baseline.json"

_STDLIB_BARREL_NAMES = frozenset(
    {
        "os",
        "re",
        "json",
        "csv",
        "subprocess",
        "time",
        "glob",
        "io",
        "shlex",
        "yaml",
        "requests",
        "datetime",
        "curses",
        "bisect",
        "gzip",
        "argparse",
        "base64",
        "threading",
        "socket",
        "struct",
        "sys",
        "random",
        "string",
        "urllib",
        "hashlib",
        "ipaddress",
        "sqlite3",
        "tempfile",
        "shutil",
        "stat",
        "signal",
        "getpass",
        "textwrap",
        "uuid",
        "webbrowser",
        "zlib",
        "binascii",
        "html",
        "difflib",
        "queue",
        "types",
        "inspect",
        "importlib",
        "ctypes",
        "smtplib",
        "imaplib",
        "ftplib",
        "telnetlib",
        "secrets",
        "math",
        "collections",
        "itertools",
        "functools",
        "copy",
        "pprint",
        "platform",
    }
)

_SKIP_ROOTS = (
    "tests",
    "contrib",
    "docs",
    "env",
    "external",
    "generated",
    "build",
    "mutants",
    "graphify-out",
    "modules_ext",
    ".venv",
    "venv_telegram",
    "venv",
    "skills",
    "modules",
    "lazygui",
    "poc_tui",
)

_DATETIME_CLASS_MEMBERS = frozenset(
    {
        "now",
        "today",
        "utcnow",
        "utcfromtimestamp",
        "fromtimestamp",
        "fromisoformat",
        "fromordinal",
        "combine",
        "strptime",
    }
)

_PAREN_RE = re.compile(r"from utils import \(([^)]*)\)", re.S)
_SIMPLE_RE = re.compile(r"^from utils import ([^(\n]+)$", re.M)


def _scan_barrel_imports() -> dict[str, list[str]]:
    """Map each production file to the stdlib names it pulls from ``utils``."""
    hits: dict[str, list[str]] = {}
    for path in REPO_ROOT.rglob("*.py"):
        rel = path.relative_to(REPO_ROOT)
        if not rel.parts or rel.parts[0] in _SKIP_ROOTS:
            continue
        try:
            source = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        found: set[str] = set()
        for match in _PAREN_RE.finditer(source):
            for token in match.group(1).replace("\n", " ").split(","):
                name = token.strip().split(" as ")[0].strip()
                if name in _STDLIB_BARREL_NAMES:
                    found.add(name)
        for match in _SIMPLE_RE.finditer(source):
            for token in match.group(1).split(","):
                name = token.strip().split(" as ")[0].strip()
                if name in _STDLIB_BARREL_NAMES:
                    found.add(name)
        if found:
            hits[str(rel)] = sorted(found)
    return hits


def test_no_new_barrel_imports() -> None:
    """No file may import more stdlib names from ``utils`` than its baseline."""
    baseline: dict[str, list[str]] = json.loads(BASELINE_PATH.read_text(encoding="utf-8"))
    live = _scan_barrel_imports()
    violations: list[str] = []
    for file_name, names in sorted(live.items()):
        allowed = set(baseline.get(file_name, []))
        extra = set(names) - allowed
        if extra:
            violations.append(f"{file_name}: {sorted(extra)} (import them directly)")
    for file_name in set(baseline) - set(live):
        del baseline[file_name]
    assert not violations, "utils barrel imports outside baseline:\n" + "\n".join(violations)


def test_baseline_has_no_stale_entries() -> None:
    """Baseline entries for files with no barrel imports must be removed."""
    baseline: dict[str, list[str]] = json.loads(BASELINE_PATH.read_text(encoding="utf-8"))
    live = _scan_barrel_imports()
    stale = sorted(set(baseline) - set(live))
    assert not stale, f"stale baseline entries (delete them): {stale}"


def test_utils_barrel_baseline_matches_scan() -> None:
    """Every live barrel import must be covered by exactly the baseline."""
    baseline: dict[str, list[str]] = json.loads(BASELINE_PATH.read_text(encoding="utf-8"))
    live = _scan_barrel_imports()
    uncovered = {f: n for f, n in live.items() if not set(n) <= set(baseline.get(f, []))}
    assert not uncovered, "baseline must list every live barrel import"


def test_datetime_binding_matches_usage() -> None:
    """``datetime`` must be bound to the class when class members are used.

    ``utils`` re-exports ``datetime`` as the ``datetime.datetime`` class, so
    migrated call sites that switch to ``import datetime`` (the module) break
    ``datetime.now()`` at runtime with ``AttributeError``. The guard fails
    when a production file calls a class member on a module-bound name, or
    when a class-bound name is used with module-only members.
    """
    import ast

    violations: list[str] = []
    for path in REPO_ROOT.rglob("*.py"):
        rel = path.relative_to(REPO_ROOT)
        if not rel.parts or rel.parts[0] in _SKIP_ROOTS:
            continue
        try:
            source = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        try:
            tree = ast.parse(source)
        except SyntaxError:
            continue
        bound_as_module = False
        bound_as_class = False
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                bound_as_module = bound_as_module or any(
                    alias.name == "datetime" and not alias.asname for alias in node.names
                )
            if isinstance(node, ast.ImportFrom) and node.module == "datetime":
                bound_as_class = bound_as_class or any(
                    alias.name == "datetime" and not alias.asname for alias in node.names
                )
        if bound_as_module and bound_as_class:
            violations.append(f"{rel}: binds datetime both as module and as class")
            continue
        if not (bound_as_module or bound_as_class):
            continue
        for node in ast.walk(tree):
            if not (
                isinstance(node, ast.Attribute) and isinstance(node.value, ast.Name) and node.value.id == "datetime"
            ):
                continue
            if bound_as_module and node.attr in _DATETIME_CLASS_MEMBERS:
                violations.append(f"{rel}:{node.lineno}: datetime.{node.attr}() needs 'from datetime import datetime'")
            if bound_as_class and node.attr in {"timedelta", "date", "timezone"}:
                violations.append(
                    f"{rel}:{node.lineno}: datetime.{node.attr} needs 'import datetime' or a direct from-import"
                )
    assert not violations, "datetime binding mismatches:\n" + "\n".join(violations)
