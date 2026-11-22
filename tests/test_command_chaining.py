"""Tests for the extracted command-chaining mixin."""

from __future__ import annotations

from cli.command_chaining import CommandChainingMixin


class _StubShell(CommandChainingMixin):
    """Minimal host exposing only what the chaining mixin reads."""

    def __init__(self, known=("ping", "sitrep", "lazynmap"), fail_on=()):
        self.aliases: dict[str, str] = {}
        self.shortcuts: dict[str, str] = {}
        self.exit_code = 0
        self.last_result = None
        self._known = set(known)
        self._fail_on = set(fail_on)
        self.ran: list[str] = []

    def perror(self, *args, **kwargs):
        return None

    def get_command_func(self, name):
        return (lambda line: None) if name in self._known else None

    def onecmd_plus_hooks(self, part, add_to_history=True, raise_keyboard_interrupt=True):
        self.ran.append(part)
        first = part.split()[0] if part.split() else part
        if first in self._fail_on:
            self.exit_code = 1
        return False


def test_split_is_quote_aware():
    """Given quoted &&, When split, Then only top-level && splits."""
    assert CommandChainingMixin._split_and_chain("a && b && c") == ["a", "b", "c"]
    assert CommandChainingMixin._split_and_chain('sh echo "a && b"') is None
    assert CommandChainingMixin._split_and_chain("single") is None


def test_chain_runs_all_parts_on_success():
    """Given all-known parts, When chained, Then every part dispatches."""
    shell = _StubShell()
    parts = CommandChainingMixin._split_and_chain("ping && sitrep && lazynmap")
    shell._run_and_chain(parts)
    assert shell.ran == ["ping", "sitrep", "lazynmap"]


def test_chain_short_circuits_on_nonzero_exit():
    """Given a failing part, When chained, Then later parts are skipped."""
    shell = _StubShell(fail_on=("ping",))
    parts = CommandChainingMixin._split_and_chain("ping && sitrep")
    shell._run_and_chain(parts)
    assert shell.ran == ["ping"]


def test_chain_stops_before_unknown_command():
    """Given an unknown first token, When guarded, Then nothing runs."""
    shell = _StubShell()
    parts = CommandChainingMixin._split_and_chain("bogus && sitrep")
    shell._run_and_chain(parts)
    assert shell.ran == []


def test_chain_part_exists_matches_alias_and_shortcut():
    """Given an alias or shortcut, When checked, Then the part is recognized."""
    shell = _StubShell()
    shell.aliases["pp"] = "ping"
    shell.shortcuts["!"] = "shell"
    assert shell._chain_part_exists("pp x") is True
    assert shell._chain_part_exists("! ls") is True
    assert shell._chain_part_exists("nope") is False
