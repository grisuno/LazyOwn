"""Tests for the incremental migration of ``LazyOwnShell`` commands.

The migration moves ``do_*`` methods out of ``lazyown.py`` into phase-
scoped :class:`cmd2.CommandSet` subclasses under ``cli/commands/``. While
the originals still live in ``LazyOwnShell`` the new modules inherit from
:class:`cli.commands._dormancy.PendingCommandSet`, so they coexist
without collisions.

These tests pin down three invariants:

1. The dormancy mechanism: pending sets are discovered (so they are
   testable) but excluded from :func:`cli.registry.register_command_sets`.
2. Coverage parity: every legacy ``do_*`` method targeted by a migrated
   set still appears on :class:`LazyOwnShell` (no premature deletion)
   and is mirrored on the migrated set (no missing migrations).
3. Production hygiene: migrated module bodies do not contain emoji or
   ``TODO``/``FIXME`` comment markers, in line with the project coding
   standards.
"""

from __future__ import annotations

import ast
import re
import sys
import unicodedata
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
LAZYOWN_PATH = REPO_ROOT / "lazyown.py"
COMMANDS_PACKAGE = REPO_ROOT / "cli" / "commands"

LEGACY_SHELL_CLASS_NAME = "LazyOwnShell"
MIGRATED_MODULES = {
    "ai": "AiCommandSet",
    "privilege_escalation": "PrivilegeEscalationCommandSet",
    "exfiltration": "ExfiltrationCommandSet",
}
EXPECTED_PHASES = {
    "AiCommandSet": "ai",
    "PrivilegeEscalationCommandSet": "privesc",
    "ExfiltrationCommandSet": "exfil",
}
EXPECTED_CATEGORY_DECORATORS = {
    "AiCommandSet": {"ai_category", "ai"},
    "PrivilegeEscalationCommandSet": {"privilege_escalation_category"},
    "ExfiltrationCommandSet": {"exfiltration_category"},
}
FORBIDDEN_MARKERS = ("TODO", "FIXME", "XXX")


@pytest.fixture(scope="module", autouse=True)
def _ensure_repo_on_path() -> None:
    """Insert the repository root onto :data:`sys.path` for direct imports."""
    if str(REPO_ROOT) not in sys.path:
        sys.path.insert(0, str(REPO_ROOT))


def _parse_class(file_path: Path, class_name: str) -> ast.ClassDef:
    """Return the AST ``ClassDef`` node named ``class_name`` in ``file_path``.

    Args:
        file_path: Path to a Python source file.
        class_name: Identifier of the class to locate.

    Returns:
        The matching :class:`ast.ClassDef` node.

    Raises:
        AssertionError: When the class cannot be found.
    """
    tree = ast.parse(file_path.read_text(encoding="utf-8"))
    for node in tree.body:
        if isinstance(node, ast.ClassDef) and node.name == class_name:
            return node
    raise AssertionError(f"class {class_name!r} not found in {file_path}")


def _category_argument(decorator: ast.AST) -> str | None:
    """Extract the category identifier from a ``with_category`` decorator.

    Args:
        decorator: The decorator AST node.

    Returns:
        The identifier or literal string passed to ``with_category``, or
        ``None`` when the decorator is not a ``with_category`` call.
    """
    if not isinstance(decorator, ast.Call):
        return None
    callee = decorator.func
    is_with_category = (isinstance(callee, ast.Attribute) and callee.attr == "with_category") or (
        isinstance(callee, ast.Name) and callee.id == "with_category"
    )
    if not is_with_category:
        return None
    if not decorator.args:
        return None
    argument = decorator.args[0]
    if isinstance(argument, ast.Name):
        return argument.id
    if isinstance(argument, ast.Constant) and isinstance(argument.value, str):
        return argument.value
    return None


def _legacy_methods_by_category(category_names: set[str]) -> dict[str, set[str]]:
    """Collect ``LazyOwnShell.do_*`` method names grouped by category.

    Args:
        category_names: Identifiers passed to ``@with_category`` that
            mark methods belonging to a single migrated set.

    Returns:
        Mapping from each requested category identifier to the set of
        ``do_*`` method names decorated with it on
        :class:`LazyOwnShell`.
    """
    shell = _parse_class(LAZYOWN_PATH, LEGACY_SHELL_CLASS_NAME)
    buckets: dict[str, set[str]] = {name: set() for name in category_names}
    for item in shell.body:
        if not isinstance(item, ast.FunctionDef):
            continue
        if not item.name.startswith("do_"):
            continue
        for decorator in item.decorator_list:
            category = _category_argument(decorator)
            if category in buckets:
                buckets[category].add(item.name)
                break
    return buckets


def _module_path(module_name: str) -> Path:
    """Return the source path of a ``cli.commands.<module_name>`` module."""
    return COMMANDS_PACKAGE / f"{module_name}.py"


class TestDormancyMechanism:
    def test_pending_marker_attribute(self) -> None:
        from cli.commands._dormancy import PENDING_FLAG_ATTRIBUTE, PendingCommandSet

        assert getattr(PendingCommandSet, PENDING_FLAG_ATTRIBUTE) is True

    def test_is_pending_helper(self) -> None:
        from cli.commands._base import LazyOwnCommandSet
        from cli.commands._dormancy import PendingCommandSet, is_pending

        assert is_pending(PendingCommandSet) is True
        assert is_pending(LazyOwnCommandSet) is False
        assert is_pending(int) is False
        assert is_pending("not-a-class") is False

    def test_subclass_inherits_pending_flag(self) -> None:
        from cli.commands._dormancy import PendingCommandSet, is_pending

        class _Sample(PendingCommandSet):
            phase = "sample"

        assert is_pending(_Sample) is True

    def test_iter_command_sets_includes_pending_by_default(self) -> None:
        from cli.registry import iter_command_sets

        discovered = {c.__name__ for c in iter_command_sets()}
        for class_name in MIGRATED_MODULES.values():
            assert class_name in discovered, f"{class_name} should be discovered"

    def test_iter_command_sets_excludes_pending_when_requested(self) -> None:
        from cli.registry import iter_command_sets

        active = {c.__name__ for c in iter_command_sets(include_pending=False)}
        for class_name in MIGRATED_MODULES.values():
            assert class_name not in active, f"{class_name} should be filtered out when include_pending=False"

    def test_register_skips_pending_sets(self) -> None:
        import cmd2

        from cli.registry import register_command_sets

        class _Bare(cmd2.Cmd):
            pass

        shell = _Bare()
        registered = {c.__class__.__name__ for c in register_command_sets(shell)}
        for class_name in MIGRATED_MODULES.values():
            assert class_name not in registered, f"{class_name} should not register while pending"


class TestMigratedSetsStructure:
    @pytest.mark.parametrize(
        "module_name, class_name",
        sorted(MIGRATED_MODULES.items()),
    )
    def test_class_imports_and_subclasses_pending(self, module_name: str, class_name: str) -> None:
        from cli.commands._dormancy import PendingCommandSet

        module = __import__(f"cli.commands.{module_name}", fromlist=[class_name])
        cls = getattr(module, class_name)
        assert issubclass(cls, PendingCommandSet)
        assert cls.phase == EXPECTED_PHASES[class_name]
        assert cls.category, f"{class_name} must declare a non-empty category"

    @pytest.mark.parametrize(
        "module_name, class_name",
        sorted(MIGRATED_MODULES.items()),
    )
    def test_only_with_category_decorators_match_phase(self, module_name: str, class_name: str) -> None:
        class_node = _parse_class(_module_path(module_name), class_name)
        for item in class_node.body:
            if not isinstance(item, ast.FunctionDef):
                continue
            if not item.name.startswith("do_"):
                continue
            decorators = {_category_argument(decorator) for decorator in item.decorator_list}
            decorators.discard(None)
            assert decorators.issubset(EXPECTED_CATEGORY_DECORATORS[class_name]), (
                f"{class_name}.{item.name} carries unexpected categories: {decorators}"
            )


class TestParityWithLegacyShell:
    @pytest.mark.parametrize(
        "module_name, class_name",
        sorted(MIGRATED_MODULES.items()),
    )
    def test_every_legacy_method_is_mirrored(self, module_name: str, class_name: str) -> None:
        legacy = _legacy_methods_by_category(EXPECTED_CATEGORY_DECORATORS[class_name])
        legacy_names: set[str] = set().union(*legacy.values())
        class_node = _parse_class(_module_path(module_name), class_name)
        migrated_names = {
            item.name for item in class_node.body if isinstance(item, ast.FunctionDef) and item.name.startswith("do_")
        }
        missing = legacy_names - migrated_names
        assert not missing, f"{class_name} is missing migrated copies of: {sorted(missing)}"

    def test_legacy_originals_still_present(self) -> None:
        shell = _parse_class(LAZYOWN_PATH, LEGACY_SHELL_CLASS_NAME)
        legacy_do_methods = {
            item.name for item in shell.body if isinstance(item, ast.FunctionDef) and item.name.startswith("do_")
        }
        for module_name, class_name in MIGRATED_MODULES.items():
            class_node = _parse_class(_module_path(module_name), class_name)
            migrated_names = {
                item.name
                for item in class_node.body
                if isinstance(item, ast.FunctionDef) and item.name.startswith("do_")
            }
            missing_in_shell = migrated_names - legacy_do_methods
            assert not missing_in_shell, (
                f"{class_name} migrated do_* methods absent from "
                f"LazyOwnShell (originals must remain until deletion "
                f"phase): {sorted(missing_in_shell)}"
            )


class TestProductionHygiene:
    @pytest.mark.parametrize(
        "module_name",
        sorted(MIGRATED_MODULES),
    )
    def test_no_forbidden_markers(self, module_name: str) -> None:
        source = _module_path(module_name).read_text(encoding="utf-8")
        for marker in FORBIDDEN_MARKERS:
            pattern = rf"(?:^|\s)({re.escape(marker)})(?:\b|:)"
            offenders = re.findall(pattern, source)
            assert not offenders, f"{module_name}.py contains forbidden marker(s): {offenders}"

    @pytest.mark.parametrize(
        "module_name",
        sorted(MIGRATED_MODULES),
    )
    def test_no_emoji(self, module_name: str) -> None:
        source = _module_path(module_name).read_text(encoding="utf-8")
        offenders = [character for character in source if unicodedata.category(character) == "So"]
        assert not offenders, f"{module_name}.py contains symbol/emoji characters: {sorted(set(offenders))}"

    @pytest.mark.parametrize(
        "module_name",
        sorted(MIGRATED_MODULES),
    )
    def test_module_is_parseable(self, module_name: str) -> None:
        ast.parse(_module_path(module_name).read_text(encoding="utf-8"))
