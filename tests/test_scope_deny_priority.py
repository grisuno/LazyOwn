"""Tests for scope denylist priority (engine lab scope + CLI guard).

Covers:
    - lazy_scope read_denylist parsing
    - Deny literal / CIDR priority over allowlist
    - Deny does not disturb normal lab allow behavior
    - cli.scope_guard ScopeGuard deny priority in warn/enforce
"""

from __future__ import annotations

from pathlib import Path

import pytest


@pytest.fixture
def scope_module():
    from modules import lazy_scope

    return lazy_scope


@pytest.fixture
def guard_module():
    from cli import scope_guard as sg

    return sg


class TestEngineDeny:
    def test_read_denylist(self, scope_module, tmp_path: Path):
        ls = scope_module
        (tmp_path / ls.DENYLIST_FILENAME).write_text("# comment\n10.0.0.7\nsvc.internal\n", encoding="utf-8")
        deny = ls.read_denylist(tmp_path)
        assert deny == frozenset({"10.0.0.7", "svc.internal"})

    def test_deny_literal_priority(self, scope_module):
        ls = scope_module
        verdict = ls.scope_verdict("192.168.56.10", denylist=frozenset({"192.168.56.10"}))
        assert verdict.allowed is False and verdict.reason == "denylist"

    def test_deny_cidr_priority(self, scope_module):
        ls = scope_module
        verdict = ls.scope_verdict(
            "10.13.37.99",
            allowlist=frozenset({"10.13.37.99"}),
            denylist=frozenset({"10.13.0.0/16"}),
        )
        assert verdict.allowed is False and verdict.reason == "denylist"

    def test_no_deny_keeps_allow(self, scope_module):
        ls = scope_module
        verdict = ls.scope_verdict("10.99.0.4", denylist=frozenset())
        assert verdict.allowed is True


class TestCliGuardDeny:
    def test_deny_blocks_even_warn(self, guard_module):
        sg = guard_module
        guard = sg.ScopeGuard(["10.0.0.0/24"], "warn", lambda cmd: True, deny_entries=["10.0.0.7"])
        decision = guard.evaluate("nmap", "10.0.0.7")
        assert decision.allowed is False
        assert "DENIED" in decision.reason

    def test_deny_outside_allow_equal(self, guard_module):
        sg = guard_module
        guard = sg.ScopeGuard([], "enforce", lambda cmd: True, deny_entries=["8.8.8.8"])
        decision = guard.evaluate("hydra", "8.8.8.8")
        assert decision.allowed is False and decision.needs_confirmation is True

    def test_deny_spares_off_command(self, guard_module):
        sg = guard_module
        guard = sg.ScopeGuard([], "enforce", lambda cmd: False, deny_entries=["8.8.8.8"])
        assert guard.evaluate("docs", "8.8.8.8").allowed is True
