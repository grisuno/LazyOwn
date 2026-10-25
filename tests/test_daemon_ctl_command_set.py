"""Daemon command set extraction tests.

SDD contract for the daemon cluster split out of
``cli/commands/misc_migrated.py`` into ``cli/commands/daemon_ctl.py``.

Stage B (active): the originals are deleted from ``misc_migrated.py``
and ``DaemonControlCommandSet`` subclasses ``LazyOwnCommandSet`` so
``cli.registry`` registers it on the shell. Tests assert active
registration eligibility, command coverage, and absence of the
methods in the source module.
"""

from __future__ import annotations

import ast
import sys
from dataclasses import dataclass
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
SOURCE_PATH = REPO_ROOT / "cli" / "commands" / "misc_migrated.py"
TARGET_PATH = REPO_ROOT / "cli" / "commands" / "daemon_ctl.py"


@pytest.fixture(scope="module", autouse=True)
def _add_repo_root_to_syspath() -> None:
    if str(REPO_ROOT) not in sys.path:
        sys.path.insert(0, str(REPO_ROOT))


@dataclass(frozen=True)
class DaemonSuiteConfig:
    """Centralised constants for the daemon extraction suite."""

    expected_commands: tuple[str, ...] = (
        "do_daemon_mode",
        "do_daemon_pause",
        "do_daemon_resume",
        "do_daemon_veto",
        "do_daemon_focus",
        "do_daemon_approve",
    )
    expected_phase: str = "misc"
    target_class: str = "DaemonControlCommandSet"
    source_class: str = "MiscMigratedCommandSet"


CONFIG = DaemonSuiteConfig()


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
    from cli.commands.daemon_ctl import DaemonControlCommandSet

    assert issubclass(DaemonControlCommandSet, LazyOwnCommandSet)
    assert not is_pending(DaemonControlCommandSet)


def test_target_exposes_full_daemon_cluster() -> None:
    from cli.commands.daemon_ctl import DaemonControlCommandSet

    found = {name for name in dir(DaemonControlCommandSet) if name.startswith("do_")}
    assert set(CONFIG.expected_commands) <= found


def test_target_phase_metadata() -> None:
    from cli.commands.daemon_ctl import DaemonControlCommandSet

    assert DaemonControlCommandSet.phase == CONFIG.expected_phase


def test_source_no_longer_defines_cluster() -> None:
    source = _methods_of(SOURCE_PATH, CONFIG.source_class)
    for name in CONFIG.expected_commands:
        assert name not in source, f"{name} still duplicated in source"


def test_registry_registers_target() -> None:
    from cli.registry import iter_command_sets

    discovered = {cls.__name__ for cls in iter_command_sets(include_pending=False)}
    assert CONFIG.target_class in discovered


def test_no_command_collisions_with_source() -> None:
    from cli.commands.daemon_ctl import DaemonControlCommandSet
    from cli.commands.misc_migrated import MiscMigratedCommandSet

    target_cmds = {n for n in dir(DaemonControlCommandSet) if n.startswith("do_")}
    source_cmds = {n for n in dir(MiscMigratedCommandSet) if n.startswith("do_")}
    assert target_cmds.isdisjoint(source_cmds)
