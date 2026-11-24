"""Command-chaining mixin for ``LazyOwnShell``.

Implements the ``cmd1 && cmd2 && cmd3`` short-circuit chain operator as a
single-responsibility mixin. It owns three concerns:

- quote-aware splitting of a raw line on top-level ``&&``
  (:meth:`_split_and_chain`);
- sequential dispatch with short-circuit on the first failing part
  (:meth:`_run_and_chain`);
- a pre-dispatch existence guard so an unknown command stops the chain
  before anything runs (:meth:`_chain_part_exists`).

Each part is re-dispatched through the shell's ``onecmd_plus_hooks`` so
aliases, the scope guard and placeholder expansion apply per command. The
mixin reads only shell state exposed through ``self`` (``onecmd_plus_hooks``,
``perror``, ``exit_code``, ``last_result``, ``aliases``,
``get_command_func``, ``shortcuts``).
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

from utils import print_warn


class CommandChainingMixin:
    """Run ``&&``-chained commands with short-circuit on failure.

    Mixed into :class:`LazyOwnShell`; invoked from ``onecmd_plus_hooks``.
    """

    aliases: dict[str, str]
    perror: Callable[..., None]
    onecmd_plus_hooks: Callable[..., Any]
    get_command_func: Callable[..., Any]

    @staticmethod
    def _split_and_chain(raw_input: str) -> list | None:
        """Split a ``cmd1 && cmd2 && cmd3`` chain into parts.

        Quote-aware: ``&&`` inside single/double quotes does not split,
        so ``sh echo "a && b"`` keeps working. Returns ``None`` when
        there is no top-level ``&&`` (normal single-command path).

        Args:
            raw_input: Raw command line as typed by the operator.

        Returns:
            List of stripped command parts, or ``None`` for a single command.
        """
        if "&&" not in raw_input:
            return None
        parts: list = []
        current: list = []
        quote: str | None = None
        i = 0
        while i < len(raw_input):
            char = raw_input[i]
            if quote is not None:
                current.append(char)
                if char == quote:
                    quote = None
                i += 1
                continue
            if char in ("'", '"'):
                quote = char
                current.append(char)
                i += 1
                continue
            if raw_input.startswith("&&", i):
                parts.append("".join(current).strip())
                current = []
                i += 2
                continue
            current.append(char)
            i += 1
        parts.append("".join(current).strip())
        parts = [part for part in parts if part]
        if len(parts) < 2:
            return None
        return parts

    def _run_and_chain(self, parts: list, add_to_history=True, raise_keyboard_interrupt=True):
        """Run ``&&``-chained commands with short-circuit on failure.

        Generic: works with ANY command (``ping && lazynmap && auto``,
        ``sh ... && ...``, aliases, ``;``-free mixes). Each part flows
        through :meth:`onecmd_plus_hooks` again so aliases, scope guard
        and placeholder expansion apply per command. The chain stops at
        the first part that fails, where failure is ANY of:

        - an exception raised by the command,
        - a ``perror`` call (unknown command, cmd2 errors, alias errors),
        - a non-zero ``exit_code`` (e.g. ``ping`` against a dead host),
        - an integer non-zero ``last_result`` (e.g. ``sh false``).

        A ``True`` stop flag (quit/exit) propagates immediately.

        Args:
            parts: Command strings from :meth:`_split_and_chain`.
            add_to_history: Forwarded to each sub-command dispatch.
            raise_keyboard_interrupt: Forwarded to each sub-command dispatch.

        Returns:
            The ``stop`` flag from cmd2 (``True`` ends the loop).
        """
        stop = False
        for index, part in enumerate(parts):
            if not self._chain_part_exists(part):
                first = part.split()[0] if part.split() else part
                print_warn(
                    f"chain stopped at [{index + 1}/{len(parts)}] '{part}': "
                    f"unknown command '{first}' — remaining {len(parts) - index - 1} skipped"
                )
                return False
            self.exit_code = 0
            failed = False
            original_perror = self.perror

            def _chain_perror(*args, _perror=original_perror, **kwargs):
                nonlocal failed
                failed = True
                return _perror(*args, **kwargs)

            self.perror = _chain_perror
            try:
                stop = self.onecmd_plus_hooks(
                    part,
                    add_to_history=add_to_history,
                    raise_keyboard_interrupt=raise_keyboard_interrupt,
                )
            except KeyboardInterrupt:
                print_warn("chain interrupted by user — chain off")
                return False
            except Exception as exc:
                print_warn(f"chain stopped at [{index + 1}/{len(parts)}] '{part}': {exc}")
                return False
            finally:
                self.perror = original_perror
            if stop:
                return stop
            if failed:
                print_warn(
                    f"chain stopped at [{index + 1}/{len(parts)}] '{part}' — remaining {len(parts) - index - 1} skipped"
                )
                return False
            exit_code = getattr(self, "exit_code", 0) or 0
            if exit_code != 0:
                print_warn(
                    f"chain stopped at [{index + 1}/{len(parts)}] '{part}' "
                    f"(exit_code={exit_code}) — remaining {len(parts) - index - 1} skipped"
                )
                return False
            last_result = getattr(self, "last_result", None)
            if isinstance(last_result, bool):
                pass
            elif isinstance(last_result, int) and last_result != 0:
                print_warn(
                    f"chain stopped at [{index + 1}/{len(parts)}] '{part}' "
                    f"(exit={last_result}) — remaining {len(parts) - index - 1} skipped"
                )
                return False
        return stop

    def _chain_part_exists(self, part: str) -> bool:
        """Check whether a chain part starts with a known command or alias.

        Generic guard so ``badcmd && sitrep`` stops before running anything:
        the shell's ``default()`` handler reports unknown commands via
        toastr instead of ``perror``, so the failure would otherwise be
        invisible to the chain runner.

        Args:
            part: Single command string (already split on ``&&``).

        Returns:
            ``True`` when the first token is a real command, a cmd2
            shortcut, or a known alias.
        """
        tokens = part.split()
        if not tokens:
            return False
        first = tokens[0]
        if first in self.aliases:
            return True
        if self.get_command_func(first) is not None:
            return True
        shortcuts = getattr(self, "shortcuts", {}) or {}
        if first in shortcuts:
            return True
        return False
