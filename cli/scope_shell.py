"""Scope-guard shell wiring mixin for ``LazyOwnShell``.

The pure scope policy (classification, normalization, the ``ScopeGuard``
decision engine) lives in :mod:`cli.scope_guard`. This mixin is the thin
shell-bound layer that binds that policy to the live cmd2 shell: building
the offensive-command set from cmd2 categories, authorizing each command
against the live payload scope, rendering decisions, and the ``scope``
verb's completion and persistence helpers.

Keeping this cluster in one single-responsibility class removes the scope
wiring from the ``LazyOwnShell`` god class while preserving every
behaviour. The mixin reads only shell attributes exposed through ``self``
(``params``, ``aliases``, ``console``, ``get_all_commands``,
``_scope_offensive``) and writes config through the same atomic
``save_payload`` path the ``assign`` verb uses.
"""

from __future__ import annotations

import shlex
import sys
from collections.abc import Callable
from typing import Any

import cmd2
from rich.console import Console

from cli.scope_guard import (
    ScopeGuard,
    ScopeMode,
    build_offensive_commands,
    normalize_scope,
)
from core.config import save_payload
from utils import (
    GREEN,
    RESET,
    YELLOW,
    miscellaneous_category,
    print_error,
    print_msg,
    print_warn,
)


class ScopeShellMixin:
    """Bind the scope-guard policy to the live cmd2 shell.

    Mixed into :class:`LazyOwnShell`; every method is an instance method
    that reads shell state through ``self``.
    """

    aliases: dict[str, str]
    console: Console
    params: dict[str, Any]
    get_all_commands: Callable[[], list[str]]
    _scope_offensive: frozenset[str]

    def _build_scope_offensive(self) -> frozenset:
        """Compute the set of offensive command names from cmd2 categories.

        Reads each command's help category via cmd2 introspection and delegates
        the offensive/benign decision to
        :func:`cli.scope_guard.build_offensive_commands`, so the classification
        policy lives in one tested place.

        Returns:
            The frozenset of offensive command names.
        """
        categories: dict = {}
        for name in self.get_all_commands():
            func = getattr(self, f"do_{name}", None)
            categories[name] = getattr(func, cmd2.constants.COMMAND_ATTR_HELP_CATEGORY, None)
        return build_offensive_commands(categories)

    def _resolve_offensive(self, name: str) -> bool:
        """Return whether a command (or custom alias) is offensive.

        Args:
            name: The command name or custom alias typed by the operator.

        Returns:
            ``True`` when the command, or the command a custom alias expands to,
            belongs to an offensive kill-chain category.
        """
        if name in self._scope_offensive:
            return True
        expansion = self.aliases.get(name)
        if expansion:
            tokens = expansion.split()
            if tokens and tokens[0] in self._scope_offensive:
                return True
        return False

    def _scope_check(self, cmd_name: str, target: str = "", force_offensive: bool = False) -> bool:
        """Authorize a command against the configured engagement scope.

        Builds a fresh :class:`cli.scope_guard.ScopeGuard` from the live payload
        values so mid-session changes to ``scope`` / ``scope_enforcement`` take
        effect immediately, then renders the decision. The guard fails open: any
        unexpected error allows the command so a defect here never blocks the
        operator.

        Args:
            cmd_name: The command name about to run.
            target: Explicit target override (defaults to ``rhost``). Commands
                such as ``apt_chain`` take the victim as an argument, so the
                argument — not the ambient ``rhost`` — is what gets vetted.
            force_offensive: Veto the category classification and treat the
                command as offensive, for callers that already know the verb
                acts on the target.

        Returns:
            ``True`` when the command may proceed, ``False`` when it must be
            skipped (enforce mode, out of scope, confirmation declined).
        """
        try:
            guard = ScopeGuard(
                scope_entries=self.params.get("scope"),
                mode=self.params.get("scope_enforcement"),
                is_offensive=(lambda name: True) if force_offensive else self._resolve_offensive,
                deny_entries=self.params.get("scope_deny"),
            )
            resolved = str(target if str(target or "").strip() else self.params.get("rhost") or "").strip()
            decision = guard.evaluate(cmd_name, resolved)
            if not decision.reason:
                return True
            if decision.mode is ScopeMode.WARN:
                print_warn(decision.reason)
                self.console.print(
                    f"  [dim]Tip:[/] Use [bold cyan]scope add {target}[/] to authorize this target, "
                    f"or [bold cyan]scope mode off[/] to disable the scope guard."
                )
                return True
            print_error(decision.reason)
            self.console.print(
                f"  [bold yellow]To fix this:[/]\n"
                f"    1. Add the target to scope:  [bold cyan]scope add {target}[/]\n"
                f"    2. Or switch to warn mode:    [bold cyan]scope mode warn[/]\n"
                f"    3. Or disable scope guard:    [bold cyan]scope mode off[/]"
            )
            if self._scope_confirm(decision):
                return True
            print_warn("Command blocked: target is outside the authorized scope.")
            return False
        except Exception:
            return True

    def _scope_confirm(self, decision) -> bool:
        """Ask the operator to confirm an out-of-scope offensive command.

        Non-interactive sessions (piped input, ``-c`` execution, scripted runs)
        cannot answer a prompt, so they are treated as a refusal: the safer
        default for an enforce-mode block.

        Args:
            decision: The blocking :class:`cli.scope_guard.ScopeDecision`.

        Returns:
            ``True`` only when an interactive operator explicitly confirms.
        """
        if not sys.stdin.isatty():
            return False
        try:
            answer = input("    [?] Run anyway against the out-of-scope target? [y/N]: ")
        except (EOFError, KeyboardInterrupt):
            return False
        return answer.strip().lower() in ("y", "yes")

    @cmd2.with_category(miscellaneous_category)
    def complete_scope(self, text, line, begidx, endidx):
        """Tab-complete the scope subcommands."""
        try:
            tokens = shlex.split(line[:endidx]) if line else []
        except ValueError:
            tokens = line[:endidx].split()
        index = len(tokens) - (0 if line[:endidx].endswith(" ") else 1)
        if index == 1:
            return [a for a in ("add", "rm", "clear", "mode") if a.startswith(text)]
        if index == 2 and tokens[1].lower() == "mode":
            return [m for m in ("off", "warn", "enforce") if m.startswith(text)]
        return []

    def _scope_entries(self) -> list:
        """Return the current scope as a fresh mutable list of entry strings."""
        return list(normalize_scope(self.params.get("scope")))

    def _scope_save(self, entries: list | None = None, mode: str | None = None) -> None:
        """Persist scope and/or mode changes to ``payload.json``.

        Mutates ``self.params`` in place and writes through the same atomic
        ``save_payload`` path used by ``assign``, keeping a single writer for
        the config file.

        Args:
            entries: Replacement scope list, or ``None`` to leave it unchanged.
            mode: Replacement enforcement mode, or ``None`` to leave it
                unchanged.
        """
        if entries is not None:
            self.params["scope"] = entries
        if mode is not None:
            self.params["scope_enforcement"] = mode
        save_payload(self.params)

    def _scope_render(self, entries: list, mode: str) -> None:
        """Print the current scope and enforcement mode."""
        print_msg(f"{YELLOW}Scope enforcement mode:{RESET} {GREEN}{mode}{RESET}")
        if not entries:
            print_msg(
                f"{YELLOW}Authorized scope is empty — the guard is dormant. "
                f"Add entries with {GREEN}scope add <cidr|ip|host>{RESET}"
            )
            return
        print_msg(f"{YELLOW}Authorized scope ({len(entries)}):{RESET}")
        for entry in entries:
            print_msg(f"    {GREEN}{entry}{RESET}")
