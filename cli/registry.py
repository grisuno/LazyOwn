"""``cmd2.CommandSet`` discovery and registration for ``cli.commands``.

Tier 2 introduces ``cli.commands.*`` modules where each module exposes one
or more ``CommandSet`` subclasses scoped to a kill-chain phase (recon,
enum, exploit, ...). This module discovers those CommandSets and registers
them on a live :class:`cmd2.Cmd` instance.

The point: ``lazyown.py`` does not import every phase module — it calls
:func:`register_command_sets(self)` at startup and the plumbing happens
declaratively. Adding a new phase is a single new file under
``cli/commands/`` plus a ``CommandSet`` subclass.

Migration coexistence
---------------------

During the staged migration the legacy ``LazyOwnShell`` still owns most
``do_*`` methods. The replacement phase modules subclass
:class:`cli.commands._dormancy.PendingCommandSet` so they are discovered
(and therefore testable) without colliding with the originals on the
shell. :func:`register_command_sets` skips them; once a phase is fully
moved out of ``lazyown.py`` its set swaps its base class to
:class:`cli.commands._base.LazyOwnCommandSet` and joins the active
registry on the next shell start.
"""

from __future__ import annotations

import importlib
import inspect
import pkgutil
from typing import Iterable

from cmd2 import CommandSet

from cli.commands._dormancy import is_pending

PACKAGE_NAME = "cli.commands"
UNDERSCORE_MODULE_PREFIX = "_"


def iter_command_sets(include_pending: bool = True) -> Iterable[type[CommandSet]]:
    """Yield every ``CommandSet`` subclass found under ``cli.commands.*``.

    Each module under ``cli.commands`` is imported and scanned for classes
    that subclass ``cmd2.CommandSet``. Modules whose leaf name begins with
    an underscore (``_base``, ``_dormancy``) are skipped because they hold
    shared scaffolding rather than concrete command sets.

    Args:
        include_pending: When ``True`` (default) pending sets are yielded
            so tests can validate their structure. When ``False`` the
            iterator filters them out — used by :func:`register_command_sets`
            to avoid collisions with the legacy shell.

    Yields:
        Each concrete ``CommandSet`` subclass declared in a discovered
        module.
    """
    pkg = importlib.import_module(PACKAGE_NAME)
    for module_info in pkgutil.iter_modules(pkg.__path__, prefix=f"{PACKAGE_NAME}."):
        leaf = module_info.name.rsplit(".", 1)[-1]
        if leaf.startswith(UNDERSCORE_MODULE_PREFIX):
            continue
        module = importlib.import_module(module_info.name)
        for _, obj in inspect.getmembers(module, inspect.isclass):
            if obj is CommandSet:
                continue
            if not issubclass(obj, CommandSet):
                continue
            if obj.__module__ != module.__name__:
                continue
            if not include_pending and is_pending(obj):
                continue
            yield obj


def register_command_sets(shell) -> list[CommandSet]:
    """Instantiate and register every active ``CommandSet`` on ``shell``.

    Pending sets (subclasses of
    :class:`cli.commands._dormancy.PendingCommandSet`) are skipped so they
    can coexist with the legacy ``do_*`` methods on ``LazyOwnShell``
    during the incremental migration.

    Args:
        shell: A live :class:`cmd2.Cmd` instance (typically
            ``LazyOwnShell``).

    Returns:
        The list of ``CommandSet`` instances that were successfully
        registered. Errors during registration of an individual set are
        reported via the shell's ``perror`` (or :func:`print` as a
        fallback) and skipped — one failing set must not prevent the
        shell from booting.
    """
    registered: list[CommandSet] = []
    for cs_class in iter_command_sets():
        if is_pending(cs_class):
            continue
        try:
            instance = cs_class()
            shell.register_command_set(instance)
            registered.append(instance)
        except Exception as exc:
            reporter = getattr(shell, "perror", None) or print
            reporter(f"[cli.registry] failed to register {cs_class.__name__}: {exc}")
    return registered


__all__ = ["PACKAGE_NAME", "iter_command_sets", "register_command_sets"]
