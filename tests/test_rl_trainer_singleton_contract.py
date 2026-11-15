"""Watchdog: the RL trainer and MoE router are single shared singletons.

Both ``modules.rl_trainer`` and ``modules.moe_router`` expose a module-level
singleton that persists a learned table to a single file under ``sessions/``
(``expert_qvalues.json`` / ``expert_performance.json``). When a module reaches
that singleton through the bare top-level name (``import rl_trainer``) instead
of the package-qualified name (``import modules.rl_trainer``), Python registers
two distinct module objects — because entry points place ``modules/`` on
``sys.path`` — each holding its own singleton. Two in-memory tables then race to
overwrite the same on-disk file, silently discarding one autonomous loop's
learning.

This test fails if any core module reaches those singleton-backed modules by
their bare names, which would reintroduce the dual-singleton reward-clobbering
bug.
"""

from __future__ import annotations

import ast
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

CORE_DIRS = ("modules", "cli", "core", "skills")
CORE_FILES = ("lazyown.py", "lazyc2.py", "utils.py")

SINGLETON_MODULES = {"rl_trainer", "moe_router"}

EXCLUDED_SUBDIRS = {"__pycache__", ".git", "tests", "test", "legacy", "mutants"}

SELF_FILES = {"rl_trainer.py", "moe_router.py"}


def _core_source_files() -> list[Path]:
    files = [ROOT / name for name in CORE_FILES if (ROOT / name).exists()]
    for directory in CORE_DIRS:
        base = ROOT / directory
        if not base.is_dir():
            continue
        for dirpath, dirnames, filenames in os.walk(base):
            dirnames[:] = [d for d in dirnames if d not in EXCLUDED_SUBDIRS]
            for filename in filenames:
                if filename.endswith(".py") and filename not in SELF_FILES:
                    files.append(Path(dirpath) / filename)
    return files


def _bare_singleton_imports(path: Path) -> list[str]:
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"))
    except (SyntaxError, UnicodeDecodeError):
        return []
    offenders: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom):
            root = (node.module or "").split(".")[0]
            if root in SINGLETON_MODULES:
                offenders.append(f"from {node.module} import ...")
        elif isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name.split(".")[0] in SINGLETON_MODULES:
                    offenders.append(f"import {alias.name}")
    return offenders


def test_no_core_module_imports_singleton_modules_by_bare_name() -> None:
    violations: dict[str, list[str]] = {}
    for path in _core_source_files():
        bad = _bare_singleton_imports(path)
        if bad:
            violations[str(path.relative_to(ROOT))] = bad
    assert not violations, (
        "Core modules must reach the RL trainer / MoE router singletons through "
        "the package-qualified name 'modules.<name>' so there is exactly one "
        f"singleton and one persisted table. Bare imports found: {violations}"
    )
