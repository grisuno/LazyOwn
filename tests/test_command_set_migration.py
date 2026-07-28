"""Tests for the incremental migration of ``LazyOwnShell`` commands.

The migration moves ``do_*`` methods out of ``lazyown.py`` into phase-scoped
:class:`cmd2.CommandSet` subclasses under ``cli/commands/``. It runs in two
tiers that coexist:

* **Promoted** sets subclass :class:`cli.commands._base.LazyOwnCommandSet`.
  Their originals have been deleted from ``lazyown.py`` and the set is
  registered live on the shell (``ai``, ``recon``, ``scan``, ``cred`` ...).
* **Pending** sets subclass :class:`cli.commands._dormancy.PendingCommandSet`.
  They are auto-generated copies (``*_migrated.py``) whose originals still
  live in ``LazyOwnShell``; the registry discovers them (so they are
  testable) but skips registration so they never collide with the originals.

These tests pin the invariants that keep both tiers healthy:

1. Import integrity: every module under ``cli/commands`` imports without
   raising. A single import-time error (for example a module-level
   ``NameError``) aborts :func:`cli.registry.iter_command_sets` and silently
   drops every set discovered after it, so the whole regression is guarded
   here.
2. Registration integrity: every active set registers on a bare shell with
   none dropped.
3. The dormancy mechanism: pending sets are discovered but excluded from
   registration.
4. Parity: every pending ``do_*`` copy still has its original on
   ``LazyOwnShell`` (no premature deletion).
"""

from __future__ import annotations

import ast
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
LAZYOWN_PATH = REPO_ROOT / "lazyown.py"
COMMANDS_PACKAGE = REPO_ROOT / "cli" / "commands"

LEGACY_SHELL_CLASS_NAME = "LazyOwnShell"


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


def _first_command_set_class(file_path: Path) -> str | None:
    """Return the name of the first ``*CommandSet`` class in ``file_path``."""
    tree = ast.parse(file_path.read_text(encoding="utf-8"))
    for node in tree.body:
        if isinstance(node, ast.ClassDef) and node.name.endswith("CommandSet"):
            return node.name
    return None


def _do_methods(class_node: ast.ClassDef) -> set[str]:
    """Return the ``do_*`` method names declared directly on ``class_node``."""
    return {
        item.name
        for item in class_node.body
        if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)) and item.name.startswith("do_")
    }


def _pending_migrated_modules() -> dict[str, str]:
    """Map every ``*_migrated`` module stem to its ``CommandSet`` class name."""
    modules: dict[str, str] = {}
    for path in sorted(COMMANDS_PACKAGE.glob("*_migrated.py")):
        class_name = _first_command_set_class(path)
        if class_name is not None:
            modules[path.stem] = class_name
    return modules


def _command_modules() -> list[str]:
    """Return the importable module names under ``cli.commands`` (no dunder)."""
    return [
        f"cli.commands.{path.stem}"
        for path in sorted(COMMANDS_PACKAGE.glob("*.py"))
        if not path.stem.startswith("__")
    ]


PENDING_MODULES = _pending_migrated_modules()


class TestImportIntegrity:
    """Every command module must import cleanly.

    ``iter_command_sets`` imports each module in turn; one import-time error
    aborts discovery and silently drops every later set. This regression is
    what a module-level ``__all__ = [f"{phase.title()}CommandSet"]`` (with
    ``phase`` undefined at module scope) once caused across all ten
    ``*_migrated`` files.
    """

    @pytest.mark.parametrize("module_name", _command_modules())
    def test_module_imports_without_error(self, module_name: str) -> None:
        __import__(module_name)

    def test_iter_command_sets_does_not_raise(self) -> None:
        from cli.registry import iter_command_sets

        discovered = list(iter_command_sets())
        assert discovered, "discovery yielded no command sets"


class TestRegistrationIntegrity:
    """Active sets register on a bare shell with none silently dropped."""

    def test_all_active_sets_register(self) -> None:
        import cmd2

        from cli.registry import iter_command_sets, register_command_sets

        class _Bare(cmd2.Cmd):
            def __init__(self) -> None:
                super().__init__(auto_load_commands=False)
                self.params: dict = {}

        expected = {c.__name__ for c in iter_command_sets(include_pending=False)}
        shell = _Bare()
        registered = {c.__class__.__name__ for c in register_command_sets(shell)}
        assert registered == expected, f"dropped sets: {sorted(expected - registered)}"

    def test_pending_sets_not_registered(self) -> None:
        import cmd2

        from cli.registry import register_command_sets

        class _Bare(cmd2.Cmd):
            def __init__(self) -> None:
                super().__init__(auto_load_commands=False)
                self.params: dict = {}

        shell = _Bare()
        registered = {c.__class__.__name__ for c in register_command_sets(shell)}
        for class_name in PENDING_MODULES.values():
            assert class_name not in registered, f"{class_name} must stay dormant"


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
        for class_name in PENDING_MODULES.values():
            assert class_name in discovered, f"{class_name} should be discovered"

    def test_iter_command_sets_excludes_pending_when_requested(self) -> None:
        from cli.registry import iter_command_sets

        active = {c.__name__ for c in iter_command_sets(include_pending=False)}
        for class_name in PENDING_MODULES.values():
            assert class_name not in active, f"{class_name} should be filtered out when include_pending=False"


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
            probe.cmd

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


class TestPendingSetsStructure:
    @pytest.mark.parametrize("module_name, class_name", sorted(PENDING_MODULES.items()))
    def test_class_subclasses_pending(self, module_name: str, class_name: str) -> None:
        from cli.commands._dormancy import PendingCommandSet

        module = __import__(f"cli.commands.{module_name}", fromlist=[class_name])
        cls = getattr(module, class_name)
        assert issubclass(cls, PendingCommandSet)
        assert cls.phase, f"{class_name} must declare a non-empty phase"
        assert cls.category, f"{class_name} must declare a non-empty category"

    @pytest.mark.parametrize("module_name, class_name", sorted(PENDING_MODULES.items()))
    def test_all_public_matches_class(self, module_name: str, class_name: str) -> None:
        module = __import__(f"cli.commands.{module_name}", fromlist=[class_name])
        assert getattr(module, "__all__", None) == [class_name]


class TestParityWithLegacyShell:
    @pytest.mark.parametrize("module_name, class_name", sorted(PENDING_MODULES.items()))
    def test_pending_originals_still_present(self, module_name: str, class_name: str) -> None:
        shell = _parse_class(LAZYOWN_PATH, LEGACY_SHELL_CLASS_NAME)
        legacy_do_methods = _do_methods(shell)
        migrated = _do_methods(_parse_class(COMMANDS_PACKAGE / f"{module_name}.py", class_name))
        missing_in_shell = migrated - legacy_do_methods
        assert not missing_in_shell, (
            f"{class_name} copies do_* absent from LazyOwnShell "
            f"(originals must remain until the deletion phase): {sorted(missing_in_shell)}"
        )


class TestPromotedSetsAreActive:
    def test_active_sets_are_not_pending(self) -> None:
        from cli.commands._dormancy import is_pending
        from cli.registry import iter_command_sets

        for cls in iter_command_sets(include_pending=False):
            assert not is_pending(cls), f"{cls.__name__} is active yet flagged pending"
