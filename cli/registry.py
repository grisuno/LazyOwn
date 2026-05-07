"""``cmd2.CommandSet`` discovery and registration.

Tier 2 introduces ``cli.commands.*`` modules where each module exposes one or
more ``CommandSet`` subclasses scoped to a kill-chain phase (recon, enum,
exploit, ...). This module discovers those CommandSets and registers them on
a live :class:`cmd2.Cmd` instance.

The point: ``lazyown.py`` doesn't have to import every phase module — it
calls :func:`register_command_sets(self)` at startup and the plumbing happens
declaratively. Adding a new phase is a single new file under
``cli/commands/`` plus an entry in ``CommandSet`` subclassing.
"""

from __future__ import annotations

import importlib
import inspect
import pkgutil
from typing import Iterable

from cmd2 import CommandSet

PACKAGE_NAME = "cli.commands"


def iter_command_sets() -> Iterable[type[CommandSet]]:
    """Yield every ``CommandSet`` subclass found under ``cli.commands.*``.

    Each module under ``cli.commands`` is imported and scanned for classes
    that subclass ``cmd2.CommandSet``. The ``CommandSet`` base itself is
    excluded.
    """
    pkg = importlib.import_module(PACKAGE_NAME)
    for module_info in pkgutil.iter_modules(pkg.__path__, prefix=f"{PACKAGE_NAME}."):
        leaf = module_info.name.rsplit(".", 1)[-1]
        if leaf.startswith("_"):
            continue
        module = importlib.import_module(module_info.name)
        for _, obj in inspect.getmembers(module, inspect.isclass):
            if obj is CommandSet:
                continue
            if not issubclass(obj, CommandSet):
                continue
            if obj.__module__ != module.__name__:
                continue
            yield obj


def register_command_sets(shell) -> list[CommandSet]:
    """Instantiate and register every discovered CommandSet on ``shell``.

    Args:
        shell: A live :class:`cmd2.Cmd` instance (typically ``LazyOwnShell``).

    Returns:
        The list of CommandSet instances that were successfully registered.
        Errors during registration of an individual set are logged via the
        shell's ``perror`` (or ``print`` fallback) and skipped — one bad
        CommandSet must not prevent the shell from booting.
    """
    registered: list[CommandSet] = []
    for cs_class in iter_command_sets():
        try:
            instance = cs_class()
            shell.register_command_set(instance)
            registered.append(instance)
        except Exception as exc:
            reporter = getattr(shell, "perror", None) or print
            reporter(f"[cli.registry] failed to register {cs_class.__name__}: {exc}")
    return registered


__all__ = ["PACKAGE_NAME", "iter_command_sets", "register_command_sets"]
