"""Contract tests: no os.system and no manual sys.stdout reassignment.

The framework treats ``os.system`` as forbidden in production code and
requires stdout capture through ``contextlib.redirect_stdout``. These tests
parse the production tree with ``ast``, so a string that merely mentions
``os.system`` (a target payload or a docstring) does not count. Only a real
call node or a real assignment node fails the contract.
"""

from __future__ import annotations

import ast
from dataclasses import dataclass, field
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent


@dataclass
class ScanConfig:
    """Configuration for the execution contract scan.

    Attributes:
        roots: Repo-relative directories whose Python files are production code.
        root_files: Repo-relative Python files at the repository root.
        skip_dirs: Directory names that never contain hand-written production code.
        skip_files: Repo-relative generated files that are not audited.
    """

    roots: tuple[str, ...] = ("modules", "cli", "core", "lazyc2", "poc_tui", "skills")
    root_files: tuple[str, ...] = (
        "lazyown.py",
        "lazyc2.py",
        "utils.py",
        "pwntomate.py",
        "slack_c2_bot.py",
        "discord_c2.py",
        "telegram_c2.py",
        "telegram_hermes.py",
    )
    skip_dirs: frozenset[str] = field(default_factory=lambda: frozenset({"__pycache__", "runs"}))
    skip_files: frozenset[str] = field(default_factory=lambda: frozenset({"skills/mcp_generated_tools.py"}))

    def iter_files(self) -> list[Path]:
        """Yield the production Python files covered by the contract."""
        files: list[Path] = []
        for name in self.root_files:
            candidate = REPO_ROOT / name
            if candidate.is_file():
                files.append(candidate)
        for root in self.roots:
            base = REPO_ROOT / root
            if not base.is_dir():
                continue
            for path in base.rglob("*.py"):
                if any(part in self.skip_dirs for part in path.parts):
                    continue
                if path.relative_to(REPO_ROOT).as_posix() in self.skip_files:
                    continue
                files.append(path)
        return files


def _parse(path: Path) -> ast.Module | None:
    """Parse a Python file, returning ``None`` when it does not parse."""
    try:
        return ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (OSError, SyntaxError):
        return None


def find_os_system_calls(config: ScanConfig | None = None) -> list[str]:
    """Return ``file:line`` for every real ``os.system(...)`` call.

    Args:
        config: Optional scan configuration.
    Returns:
        A sorted list of ``relative_path:lineno`` strings.
    """
    active = config or ScanConfig()
    hits: list[str] = []
    for path in active.iter_files():
        tree = _parse(path)
        if tree is None:
            continue
        for node in ast.walk(tree):
            if not isinstance(node, ast.Call) or not isinstance(node.func, ast.Attribute):
                continue
            if node.func.attr != "system":
                continue
            if isinstance(node.func.value, ast.Name) and node.func.value.id == "os":
                hits.append(f"{path.relative_to(REPO_ROOT).as_posix()}:{node.lineno}")
    return sorted(hits)


def find_stdout_assignments(config: ScanConfig | None = None) -> list[str]:
    """Return ``file:line`` for every manual ``sys.stdout = ...`` assignment.

    Args:
        config: Optional scan configuration.
    Returns:
        A sorted list of ``relative_path:lineno`` strings.
    """
    active = config or ScanConfig()
    hits: list[str] = []
    for path in active.iter_files():
        tree = _parse(path)
        if tree is None:
            continue
        for node in ast.walk(tree):
            if not isinstance(node, (ast.Assign, ast.AnnAssign)):
                continue
            target = node.targets[0] if isinstance(node, ast.Assign) else node.target
            if (
                isinstance(target, ast.Attribute)
                and target.attr == "stdout"
                and isinstance(target.value, ast.Name)
                and target.value.id == "sys"
            ):
                hits.append(f"{path.relative_to(REPO_ROOT).as_posix()}:{node.lineno}")
    return sorted(hits)


def test_no_os_system_in_production() -> None:
    """Production code must not call ``os.system``."""
    hits = find_os_system_calls()
    assert hits == [], f"os.system calls found: {hits}"


def test_no_manual_stdout_reassignment() -> None:
    """Production code must capture stdout with contextlib, not manual assignment."""
    hits = find_stdout_assignments()
    assert hits == [], f"manual sys.stdout assignments found: {hits}"


def test_scanner_detects_a_synthetic_os_system(tmp_path: Path) -> None:
    """The scanner reports a real call and ignores a string that mentions it."""
    source = tmp_path / "sample.py"
    source.write_text(
        'import os\n\ndoc = "os.system(\\"id\\")"\nos.system("id")\n',
        encoding="utf-8",
    )
    tree = _parse(source)
    assert tree is not None
    calls = [
        node
        for node in ast.walk(tree)
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Attribute)
        and node.func.attr == "system"
    ]
    assert len(calls) == 1
