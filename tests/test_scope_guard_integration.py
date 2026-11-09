#!/usr/bin/env python3
"""Integration tests for the scope guard wired into LazyOwnShell.

These exercise the thin shell glue (``_scope_check``, ``_resolve_offensive``,
``_scope_confirm``, ``_scope_entries``) by invoking the real, unbound methods
against a lightweight stub, so the full (heavy) shell constructor is never run.
The pure decision logic lives in :mod:`cli.scope_guard` and is covered by
``tests/test_scope_guard.py``.
"""

from __future__ import annotations

import sys
import types
from pathlib import Path

import pytest

_ROOT = Path(__file__).parent.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

import lazyown  # noqa: E402

Shell = lazyown.LazyOwnShell


def _make_stub(params, offensive=frozenset(), aliases=None, confirm=False):
    stub = types.SimpleNamespace()
    stub.params = params
    stub._scope_offensive = frozenset(offensive)
    stub.aliases = aliases or {}
    stub._resolve_offensive = lambda name: Shell._resolve_offensive(stub, name)
    stub._scope_confirm = lambda decision: confirm
    from rich.console import Console

    stub.console = Console(file=open("/dev/null", "w"))
    return stub


class TestResolveOffensive:
    def test_direct_offensive(self):
        stub = _make_stub({}, offensive={"lazynmap"})
        assert Shell._resolve_offensive(stub, "lazynmap") is True

    def test_benign(self):
        stub = _make_stub({}, offensive={"lazynmap"})
        assert Shell._resolve_offensive(stub, "do_report") is False

    def test_alias_to_offensive(self):
        stub = _make_stub({}, offensive={"lazynmap"}, aliases={"scanit": "lazynmap --fast"})
        assert Shell._resolve_offensive(stub, "scanit") is True

    def test_alias_to_benign(self):
        stub = _make_stub({}, offensive={"lazynmap"}, aliases={"r": "report"})
        assert Shell._resolve_offensive(stub, "r") is False


class TestScopeCheck:
    def test_no_scope_allows(self):
        stub = _make_stub(
            {"scope": [], "scope_enforcement": "enforce", "rhost": "8.8.8.8"},
            offensive={"lazynmap"},
        )
        assert Shell._scope_check(stub, "lazynmap") is True

    def test_in_scope_allows(self):
        stub = _make_stub(
            {"scope": ["8.8.8.0/24"], "scope_enforcement": "enforce", "rhost": "8.8.8.8"},
            offensive={"lazynmap"},
        )
        assert Shell._scope_check(stub, "lazynmap") is True

    def test_benign_command_allows(self):
        stub = _make_stub(
            {"scope": ["10.0.0.0/24"], "scope_enforcement": "enforce", "rhost": "8.8.8.8"},
            offensive={"lazynmap"},
        )
        assert Shell._scope_check(stub, "do_report") is True

    def test_warn_mode_allows_out_of_scope(self, capsys):
        stub = _make_stub(
            {"scope": ["10.0.0.0/24"], "scope_enforcement": "warn", "rhost": "8.8.8.8"},
            offensive={"lazynmap"},
        )
        assert Shell._scope_check(stub, "lazynmap") is True

    def test_enforce_mode_blocks_out_of_scope(self):
        stub = _make_stub(
            {"scope": ["10.0.0.0/24"], "scope_enforcement": "enforce", "rhost": "8.8.8.8"},
            offensive={"lazynmap"},
            confirm=False,
        )
        assert Shell._scope_check(stub, "lazynmap") is False

    def test_enforce_mode_confirmation_allows(self):
        stub = _make_stub(
            {"scope": ["10.0.0.0/24"], "scope_enforcement": "enforce", "rhost": "8.8.8.8"},
            offensive={"lazynmap"},
            confirm=True,
        )
        assert Shell._scope_check(stub, "lazynmap") is True

    def test_off_mode_allows(self):
        stub = _make_stub(
            {"scope": ["10.0.0.0/24"], "scope_enforcement": "off", "rhost": "8.8.8.8"},
            offensive={"lazynmap"},
        )
        assert Shell._scope_check(stub, "lazynmap") is True

    def test_malformed_params_fail_open(self):
        stub = _make_stub(
            {"scope": ["10.0.0.0/24"], "scope_enforcement": "enforce", "rhost": "8.8.8.8"},
            offensive={"lazynmap"},
        )
        stub._resolve_offensive = None  # force an internal failure
        assert Shell._scope_check(stub, "lazynmap") is True


class TestScopeConfirmNonInteractive:
    def test_non_tty_refuses(self, monkeypatch):
        stub = _make_stub({})
        monkeypatch.setattr(lazyown.sys.stdin, "isatty", lambda: False)
        decision = types.SimpleNamespace(reason="x")
        assert Shell._scope_confirm(stub, decision) is False


class TestScopeEntries:
    def test_normalizes_list(self):
        stub = _make_stub({"scope": ["10.0.0.0/24", " host ", ""]})
        assert Shell._scope_entries(stub) == ["10.0.0.0/24", "host"]

    def test_normalizes_string(self):
        stub = _make_stub({"scope": "10.0.0.0/24, 10.0.1.5"})
        assert Shell._scope_entries(stub) == ["10.0.0.0/24", "10.0.1.5"]


class TestOffensiveClassificationIsBuilt:
    def test_build_offensive_from_categories(self):
        stub = types.SimpleNamespace()
        stub.get_all_commands = lambda: ["lazynmap", "report"]
        import cmd2

        def _do_offensive():
            pass

        def _do_benign():
            pass

        setattr(_do_offensive, cmd2.constants.COMMAND_ATTR_HELP_CATEGORY, "02. Scanning & Enumeration")
        setattr(_do_benign, cmd2.constants.COMMAND_ATTR_HELP_CATEGORY, "11. Reporting")
        stub.do_lazynmap = _do_offensive
        stub.do_report = _do_benign
        result = Shell._build_scope_offensive(stub)
        assert "lazynmap" in result
        assert "report" not in result


if __name__ == "__main__":
    sys.exit(pytest.main([__file__, "-v"]))


def test_alias_parameter_is_preserved_after_dynamic_expansion():
    """One-command aliases keep the operator-supplied IP or flag arguments."""
    import cmd2

    shell = object.__new__(Shell)
    cmd2.Cmd.__init__(shell)
    shell.aliases.update({"rm_wm_host": "sh python3 -m modules.world_model remove-host"})
    shell.params = {"scope": [], "scope_enforcement": "off", "rhost": ""}
    shell.version = "test"
    shell.c2_url = ""
    shell.sessions_dir = ""
    shell.captured_images_dir = ""
    shell.path = ""
    shell.url_download = ""
    shell._scope_check = lambda name: True
    captured: dict[str, str] = {}
    shell.do_sh = lambda line: captured.setdefault("line", str(line))

    shell.onecmd_plus_hooks("rm_wm_host 127.0.0.1")
    assert captured["line"] == "python3 -m modules.world_model remove-host 127.0.0.1"


class TestExplicitTargetCheck:
    """Commands taking the victim as an argument are vetted on that argument."""

    def test_enforce_blocks_explicit_out_of_scope_target(self):
        story = "apt_chain with an explicit out-of-scope target is blocked even when rhost is in scope"
        stub = _make_stub(
            {"scope": ["10.10.10.0/24"], "scope_enforcement": "enforce", "rhost": "127.0.0.1"},
            offensive=set(),
            confirm=False,
        )
        assert Shell._scope_check(stub, "apt_chain", target="127.0.0.1", force_offensive=True) is False, story

    def test_enforce_allows_explicit_in_scope_target(self):
        story = "the explicit target inside the scope runs through"
        stub = _make_stub(
            {"scope": ["10.10.10.0/24"], "scope_enforcement": "enforce", "rhost": "127.0.0.1"},
            offensive=set(),
            confirm=False,
        )
        assert Shell._scope_check(stub, "apt_chain", target="10.10.10.5", force_offensive=True) is True, story

    def test_warn_annotates_explicit_out_of_scope_target(self, capsys):
        story = "warn mode keeps annotating but never blocks"
        stub = _make_stub(
            {"scope": ["10.10.10.0/24"], "scope_enforcement": "warn", "rhost": "127.0.0.1"},
            offensive=set(),
        )
        assert Shell._scope_check(stub, "apt_chain", target="127.0.0.1", force_offensive=True) is True, story
        assert "OUTSIDE the authorized scope" in capsys.readouterr().out, story

    def test_default_classification_kept_without_force(self):
        story = "without force_offensive the benign classification allows the broad verb"
        stub = _make_stub(
            {"scope": ["10.10.10.0/24"], "scope_enforcement": "enforce", "rhost": "127.0.0.1"},
            offensive=set(),
        )
        assert Shell._scope_check(stub, "apt_chain", target="127.0.0.1") is True, story
