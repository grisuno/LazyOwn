"""Tests for the completed migration of ``LazyOwnShell`` commands.

The migration moved ``do_*`` methods out of ``lazyown.py`` into phase-
scoped :class:`cmd2.CommandSet` subclasses under ``cli/commands/``. The
monolith split is complete: all migrated modules inherit from the active
:class:`cli.commands._base.LazyOwnCommandSet`, originals were removed
from ``LazyOwnShell``, and no set remains dormant.

These tests pin down three invariants:

1. Activation: every discovered ``CommandSet`` subclasses the active
   base (not the dormant :class:`cli.commands._dormancy.PendingCommandSet`),
   survives ``include_pending=False`` discovery, and registers on the shell.
2. Deduplication: every migrated ``do_*`` method is gone from
   :class:`LazyOwnShell` (no lingering duplicate) while the migrated set
   still exposes its ``do_*`` commands.
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
FORBIDDEN_MARKERS = ("TODO", "FIXME", "XXX")


def _discover_migrated_class_names() -> dict[str, str]:
    """Return ``{module_name: class_name}`` for every active ``CommandSet``.

    Uses the same discovery path as the production registry so the
    mapping stays in sync without manual updates.
    """
    mapping: dict[str, str] = {}
    for module_name in sorted(_collect_migrated_modules()):
        source = (COMMANDS_PACKAGE / f"{module_name}.py").read_text(encoding="utf-8")
        tree = ast.parse(source)
        for node in tree.body:
            if isinstance(node, ast.ClassDef) and any(
                base.id == "LazyOwnCommandSet" if isinstance(base, ast.Name) else False
                for base in node.bases
            ):
                mapping[module_name] = node.name
                break
    return mapping


def _collect_migrated_modules() -> set[str]:
    """Return the set of ``cli/commands/*.py`` module names (no private files)."""
    return {
        p.stem
        for p in COMMANDS_PACKAGE.glob("*.py")
        if not p.stem.startswith("_") and p.stem != "__init__"
    }


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


def _collect_legacy_do_methods() -> dict[str, str]:
    """Collect every ``do_*`` method on ``LazyOwnShell`` keyed by name.

    Returns:
        Mapping from method name to its ``@with_category`` category
        identifier, or an empty string when un-categorised.
    """
    shell = _parse_class(LAZYOWN_PATH, LEGACY_SHELL_CLASS_NAME)
    result: dict[str, str] = {}
    for item in shell.body:
        if not isinstance(item, ast.FunctionDef):
            continue
        if not item.name.startswith("do_"):
            continue
        category = ""
        for decorator in item.decorator_list:
            cat = _category_argument(decorator)
            if cat:
                category = cat
                break
        result[item.name] = category
    return result


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

    def test_all_discovered_sets_are_active(self) -> None:
        from cli.commands._dormancy import is_pending
        from cli.registry import iter_command_sets

        dormant = sorted(
            c.__name__
            for c in iter_command_sets(include_pending=True)
            if is_pending(c)
        )
        assert dormant == [], (
            f"Migration is complete; no CommandSet should remain dormant. Found: {dormant}"
        )

    def test_active_sets_excluded_when_pending_skipped(self) -> None:
        from cli.commands._dormancy import is_pending
        from cli.registry import iter_command_sets

        active = {c.__name__ for c in iter_command_sets(include_pending=False)}
        assert len(active) >= 10, (
            f"At least 10 active CommandSets expected, found {len(active)}"
        )

    def test_register_includes_migrated_sets(self) -> None:
        import cmd2

        from cli.registry import register_command_sets

        class _Bare(cmd2.Cmd):
            def __init__(self) -> None:
                super().__init__(auto_load_commands=False)

        shell = _Bare()
        registered = {c.__class__.__name__ for c in register_command_sets(shell)}
        assert len(registered) >= 10, (
            f"At least 10 CommandSets expected, found {len(registered)}"
        )


class TestShellForwarding:
    """Pin the ``_base`` forwarding contract used by every migrated ``do_*``.

    cmd2 keeps the parent shell in a name-mangled private attribute and exposes
    it through the :attr:`cmd2.CommandSet._cmd` property. A regression that
    reads ``self.__dict__`` instead of that property silently turns
    ``self.params`` into an empty dict and every forwarded call (such as
    ``self.cmd(...)``) into ``AttributeError``.
    """

    def _make_set(self):
        from cli.commands._base import LazyOwnCommandSet

        class _Probe(LazyOwnCommandSet):
            phase = "probe"

        return _Probe

    def test_unregistered_params_default_empty(self) -> None:
        probe = self._make_set()()
        assert probe.params == {}

    def test_unregistered_forwarding_raises_attribute_error(self) -> None:
        probe = self._make_set()()
        with pytest.raises(AttributeError):
            _ = probe.cmd

    def test_registered_params_reflect_shell(self) -> None:
        import cmd2

        class _Shell(cmd2.Cmd):
            def __init__(self) -> None:
                super().__init__(auto_load_commands=False)
                self.params = {"rhost": "10.10.11.5"}

        shell = _Shell()
        probe = self._make_set()()
        shell.register_command_set(probe)
        assert probe.params == {"rhost": "10.10.11.5"}

    def test_registered_forwards_shell_methods(self) -> None:
        import cmd2

        captured: list[str] = []

        class _Shell(cmd2.Cmd):
            def __init__(self) -> None:
                super().__init__(auto_load_commands=False)
                self.params = {}

            def cmd(self, line: str) -> None:
                captured.append(line)

        shell = _Shell()
        probe = self._make_set()()
        shell.register_command_set(probe)
        probe.cmd("searchsploit openssh")
        assert captured == ["searchsploit openssh"]


class TestMigratedSetsStructure:
    @pytest.fixture(scope="class")
    def migrated_modules(self) -> dict[str, str]:
        return _discover_migrated_class_names()

    @pytest.fixture(scope="class")
    def module_names(self, migrated_modules: dict[str, str]) -> list[str]:
        return sorted(migrated_modules)

    def test_all_modules_discoverable(self, migrated_modules: dict[str, str]) -> None:
        assert len(migrated_modules) >= 10, (
            f"Expected at least 10 migrated modules, found {len(migrated_modules)}"
        )

    def test_all_active_and_have_phase(self, migrated_modules: dict[str, str]) -> None:
        from cli.commands._base import LazyOwnCommandSet
        from cli.commands._dormancy import is_pending

        for module_name, class_name in migrated_modules.items():
            module = __import__(f"cli.commands.{module_name}", fromlist=[class_name])
            cls = getattr(module, class_name)
            assert issubclass(cls, LazyOwnCommandSet), (
                f"{class_name} in {module_name} must subclass LazyOwnCommandSet"
            )
            assert not is_pending(cls), (
                f"{class_name} in {module_name} must not be dormant"
            )
            assert cls.phase, (
                f"{class_name} in {module_name} must declare a non-empty phase"
            )
            assert cls.category, (
                f"{class_name} in {module_name} must declare a non-empty category"
            )

    def test_each_module_has_do_methods(self, migrated_modules: dict[str, str]) -> None:
        for module_name, class_name in migrated_modules.items():
            class_node = _parse_class(_module_path(module_name), class_name)
            migrated_names = {
                item.name
                for item in class_node.body
                if isinstance(item, ast.FunctionDef) and item.name.startswith("do_")
            }
            assert migrated_names, (
                f"{class_name} in {module_name} must define at least one do_* command"
            )


class TestParityWithLegacyShell:
    def test_no_do_methods_remain_on_shell(self) -> None:
        """Only infrastructure methods remain on LazyOwnShell."""
        shell = _parse_class(LAZYOWN_PATH, LEGACY_SHELL_CLASS_NAME)
        legacy_do_methods = {
            item.name
            for item in shell.body
            if isinstance(item, ast.FunctionDef) and item.name.startswith("do_")
        }
        infrastructure_keepers = {"do_event_log", "do_route", "do_set", "do_state_snapshot"}
        unexpected = legacy_do_methods - infrastructure_keepers
        assert not unexpected, (
            f"Unexpected do_* methods still on LazyOwnShell: {sorted(unexpected)}"
        )

    def test_migrated_methods_not_duplicated_on_shell(self) -> None:
        """Every migrated ``do_*`` method is absent from LazyOwnShell."""
        shell = _parse_class(LAZYOWN_PATH, LEGACY_SHELL_CLASS_NAME)
        shell_do_names = {
            item.name
            for item in shell.body
            if isinstance(item, ast.FunctionDef) and item.name.startswith("do_")
        }
        migrated = _discover_migrated_class_names()
        duplicated: dict[str, list[str]] = {}
        for module_name, class_name in migrated.items():
            class_node = _parse_class(_module_path(module_name), class_name)
            for item in class_node.body:
                if isinstance(item, ast.FunctionDef) and item.name.startswith("do_"):
                    if item.name in shell_do_names:
                        duplicated.setdefault(item.name, []).append(module_name)
        assert not duplicated, (
            f"Migrated do_* methods still duplicated on LazyOwnShell: {duplicated}"
        )


class TestProductionHygiene:
    @pytest.fixture(scope="class")
    def module_names(self) -> list[str]:
        return sorted(_discover_migrated_class_names())

    def test_no_forbidden_markers(self, module_names: list[str]) -> None:
        for module_name in module_names:
            source = _module_path(module_name).read_text(encoding="utf-8")
            for marker in FORBIDDEN_MARKERS:
                pattern = rf"(?:^|\s)({re.escape(marker)})(?:\b|:)"
                offenders = re.findall(pattern, source)
                assert not offenders, (
                    f"{module_name}.py contains forbidden marker(s): {offenders}"
                )

    def test_no_emoji(self, module_names: list[str]) -> None:
        EMOJI_PATTERN = re.compile(
            "[\U0001F600-\U0001F64F"
            "\U0001F300-\U0001F5FF"
            "\U0001F680-\U0001F6FF"
            "\U0001F1E0-\U0001F1FF"
            "\U0001F900-\U0001F9FF"
            "\U0001FA00-\U0001FA6F"
            "\U0001FA70-\U0001FAFF"
            "\U00002600-\U000027BF"
            "\U0001F250-\U0001F251"
            "\U0000FE00-\U0000FE0F"
            "\U0000200D\U0000FE0F"
            "]"
        )
        for module_name in module_names:
            source = _module_path(module_name).read_text(encoding="utf-8")
            offenders = EMOJI_PATTERN.findall(source)
            assert not offenders, (
                f"{module_name}.py contains emoji characters: {offenders!r}"
            )

    def test_every_module_is_parseable(self, module_names: list[str]) -> None:
        for module_name in module_names:
            ast.parse(_module_path(module_name).read_text(encoding="utf-8"))
