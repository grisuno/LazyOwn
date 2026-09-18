"""Session ops command set extraction tests.

SDD contract for the session/state cluster split out of
``cli/commands/misc_migrated.py`` into ``cli/commands/session_ops.py``.

Stage A (pending): the new ``SessionOpsCommandSet`` subclasses
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
TARGET_PATH = REPO_ROOT / "cli" / "commands" / "session_ops.py"


@pytest.fixture(scope="module", autouse=True)
def _add_repo_root_to_syspath() -> None:
    if str(REPO_ROOT) not in sys.path:
        sys.path.insert(0, str(REPO_ROOT))


@dataclass(frozen=True)
class SessionOpsSuiteConfig:
    """Centralised constants for the session ops extraction suite."""

    expected_commands: tuple[str, ...] = (
        "do_note",
        "do_l00t",
        "do_loot",
        "do_pivot",
        "do_tasks",
        "do_scans",
        "do_sitrep",
        "do_assign",
        "do_tenant",
        "do_scope",
        "do_show",
        "do_list",
        "do_run",
        "do_payload",
        "do_next",
        "do_chainmode",
        "do_engage",
        "do_pipeline",
        "do_lazyscript",
        "do_hunt",
        "do_resume",
        "do_getseclist",
        "do_download_resources",
        "do_collab_join",
        "do_kick",
        "do_qa",
        "do_clock",
        "do_gencert",
        "do_load_session",
        "do_clone_site",
        "do_msfshellcoder",
    )
    expected_phase: str = "misc"
    target_class: str = "SessionOpsCommandSet"
    source_class: str = "MiscMigratedCommandSet"


CONFIG = SessionOpsSuiteConfig()


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
    from cli.commands.session_ops import SessionOpsCommandSet

    assert issubclass(SessionOpsCommandSet, LazyOwnCommandSet)
    assert not is_pending(SessionOpsCommandSet)


def test_target_exposes_full_session_cluster() -> None:
    from cli.commands.session_ops import SessionOpsCommandSet

    found = {name for name in dir(SessionOpsCommandSet) if name.startswith("do_")}
    assert set(CONFIG.expected_commands) <= found


def test_target_phase_metadata() -> None:
    from cli.commands.session_ops import SessionOpsCommandSet

    assert SessionOpsCommandSet.phase == CONFIG.expected_phase


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
    from cli.commands.session_ops import SessionOpsCommandSet

    target_cmds = {n for n in dir(SessionOpsCommandSet) if n.startswith("do_")}
    source_cmds = {n for n in dir(MiscMigratedCommandSet) if n.startswith("do_")}
    assert target_cmds.isdisjoint(source_cmds)
