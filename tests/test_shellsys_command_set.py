"""Shell/sys command set extraction tests.

SDD contract for the shell/sys cluster split out of
``cli/commands/misc_migrated.py`` into ``cli/commands/shellsys.py``.

Stage A (pending): the new ``ShellSysCommandSet`` subclasses
``PendingCommandSet`` so it is discovered but not registered, coexisting
with the originals. Tests assert structure plus AST parity with the
original methods in ``misc_migrated.py``.

Stage B (active): after the originals are deleted and the base class is
flipped to ``LazyOwnCommandSet``, tests assert registry discovery,
active registration eligibility, and absence of the methods in
``misc_migrated.py``.
"""

from __future__ import annotations

import ast
import sys
from dataclasses import dataclass
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
SOURCE_PATH = REPO_ROOT / "cli" / "commands" / "misc_migrated.py"
TARGET_PATH = REPO_ROOT / "cli" / "commands" / "shellsys.py"


@pytest.fixture(scope="module", autouse=True)
def _add_repo_root_to_syspath() -> None:
    if str(REPO_ROOT) not in sys.path:
        sys.path.insert(0, str(REPO_ROOT))


@dataclass(frozen=True)
class ShellsysSuiteConfig:
    """Centralised constants for the shellsys extraction suite."""

    expected_commands: tuple[str, ...] = (
        "do_sh",
        "do_sys",
        "do_pwd",
        "do_nano",
        "do_cron",
        "do_clean",
        "do_fixperm",
        "do_fixel",
        "do_pop",
        "do_tab",
    )
    expected_phase: str = "misc"
    target_class: str = "ShellSysCommandSet"
    source_class: str = "MiscMigratedCommandSet"


CONFIG = ShellsysSuiteConfig()


def _methods_of(path: Path, class_name: str) -> dict[str, ast.FunctionDef]:
    tree = ast.parse(path.read_text(encoding="utf-8"))
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef) and node.name == class_name:
            return {
                item.name: item
                for item in node.body
                if isinstance(item, ast.FunctionDef) and item.name.startswith("do_")
            }
    raise AssertionError(f"{class_name} not found in {path}")


def test_target_is_active_command_set() -> None:
    from cli.commands._base import LazyOwnCommandSet
    from cli.commands._dormancy import is_pending
    from cli.commands.shellsys import ShellSysCommandSet

    assert issubclass(ShellSysCommandSet, LazyOwnCommandSet)
    assert not is_pending(ShellSysCommandSet)


def test_target_exposes_full_shellsys_cluster() -> None:
    from cli.commands.shellsys import ShellSysCommandSet

    found = {name for name in dir(ShellSysCommandSet) if name.startswith("do_")}
    assert set(CONFIG.expected_commands) <= found


def test_target_phase_metadata() -> None:
    from cli.commands.shellsys import ShellSysCommandSet

    assert ShellSysCommandSet.phase == CONFIG.expected_phase


def test_source_no_longer_defines_cluster() -> None:
    source = _methods_of(SOURCE_PATH, CONFIG.source_class)
    for name in CONFIG.expected_commands:
        assert name not in source, f"{name} still duplicated in source"


def test_registry_registers_target() -> None:
    from cli.registry import iter_command_sets

    discovered = {cls.__name__ for cls in iter_command_sets(include_pending=False)}
    assert CONFIG.target_class in discovered


def test_no_command_collisions_with_source() -> None:
    from cli.commands.misc_migrated import MiscMigratedCommandSet
    from cli.commands.shellsys import ShellSysCommandSet

    target_cmds = {n for n in dir(ShellSysCommandSet) if n.startswith("do_")}
    source_cmds = {n for n in dir(MiscMigratedCommandSet) if n.startswith("do_")}
    assert target_cmds.isdisjoint(source_cmds)
