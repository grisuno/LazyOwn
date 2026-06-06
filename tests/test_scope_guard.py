#!/usr/bin/env python3
"""Test suite for cli/scope_guard.py.

Covers the pure scope-authorization logic in isolation: mode coercion, scope
normalisation from every accepted form, CIDR/IP/hostname matching, the
offensive-command classifier, and every branch of the fail-open decision
matrix. A drift test pins the offensive category strings against the canonical
definitions in utils.py.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

_ROOT = Path(__file__).parent.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from cli.scope_guard import (  # noqa: E402
    OFFENSIVE_CATEGORIES,
    ScopeDecision,
    ScopeGuard,
    ScopeMode,
    build_offensive_commands,
    normalize_scope,
    target_in_scope,
)


class TestScopeMode:
    def test_from_value_passthrough(self):
        assert ScopeMode.from_value(ScopeMode.ENFORCE) is ScopeMode.ENFORCE

    @pytest.mark.parametrize("raw,expected", [
        ("off", ScopeMode.OFF),
        ("WARN", ScopeMode.WARN),
        ("  Enforce  ", ScopeMode.ENFORCE),
    ])
    def test_from_value_strings(self, raw, expected):
        assert ScopeMode.from_value(raw) is expected

    @pytest.mark.parametrize("raw", ["", None, "bogus", 123])
    def test_unknown_defaults_to_warn(self, raw):
        assert ScopeMode.from_value(raw) is ScopeMode.WARN


class TestNormalizeScope:
    def test_none(self):
        assert normalize_scope(None) == ()

    def test_list(self):
        assert normalize_scope(["10.0.0.0/24", " host ", ""]) == ("10.0.0.0/24", "host")

    def test_tuple_and_set(self):
        assert normalize_scope(("a",)) == ("a",)
        assert set(normalize_scope({"a", "b"})) == {"a", "b"}

    def test_json_array_string(self):
        assert normalize_scope('["10.0.0.0/24", "10.0.1.5"]') == ("10.0.0.0/24", "10.0.1.5")

    def test_comma_separated_string(self):
        assert normalize_scope("10.0.0.0/24, 10.0.1.5") == ("10.0.0.0/24", "10.0.1.5")

    def test_space_separated_string(self):
        assert normalize_scope("a b   c") == ("a", "b", "c")

    def test_empty_string(self):
        assert normalize_scope("   ") == ()

    def test_unsupported_type(self):
        assert normalize_scope(42) == ()


class TestTargetInScope:
    def test_empty_target(self):
        assert target_in_scope("", ["10.0.0.0/24"]) is False

    def test_ip_in_cidr(self):
        assert target_in_scope("10.0.0.5", ["10.0.0.0/24"]) is True

    def test_ip_outside_cidr(self):
        assert target_in_scope("10.0.1.5", ["10.0.0.0/24"]) is False

    def test_bare_ip_match(self):
        assert target_in_scope("10.10.11.5", ["10.10.11.5"]) is True

    def test_bare_ip_mismatch(self):
        assert target_in_scope("10.10.11.6", ["10.10.11.5"]) is False

    def test_exact_hostname(self):
        assert target_in_scope("dc.corp.local", ["dc.corp.local"]) is True

    def test_subdomain_match(self):
        assert target_in_scope("dc.corp.local", ["corp.local"]) is True

    def test_wildcard_match(self):
        assert target_in_scope("dc.corp.local", ["*.corp.local"]) is True
        assert target_in_scope("corp.local", ["*.corp.local"]) is True

    def test_hostname_not_in_cidr(self):
        assert target_in_scope("dc.corp.local", ["10.0.0.0/24"]) is False

    def test_ip_not_matched_by_hostname_entry(self):
        assert target_in_scope("10.0.0.5", ["corp.local"]) is False

    def test_ipv6_in_cidr(self):
        assert target_in_scope("2001:db8::5", ["2001:db8::/32"]) is True

    def test_blank_entries_ignored(self):
        assert target_in_scope("10.0.0.5", ["", "  ", "10.0.0.0/24"]) is True


class TestBuildOffensiveCommands:
    def test_selects_offensive_only(self):
        cats = {
            "lazynmap": "02. Scanning & Enumeration",
            "do_report": "11. Reporting",
            "assign": "12. Miscellaneous",
            "exploit_x": "03. Exploitation",
            "uncategorised": None,
        }
        result = build_offensive_commands(cats)
        assert result == frozenset({"lazynmap", "exploit_x"})

    def test_empty(self):
        assert build_offensive_commands({}) == frozenset()


def _guard(scope, mode, offensive_names=("nmap_scan",)):
    offensive = set(offensive_names)
    return ScopeGuard(scope, mode, lambda name: name in offensive)


class TestScopeGuardEvaluate:
    def test_mode_off_is_noop(self):
        decision = _guard(["10.0.0.0/24"], "off").evaluate("nmap_scan", "8.8.8.8")
        assert decision.allowed is True
        assert decision.reason == ""

    def test_no_scope_allows(self):
        decision = _guard([], "enforce").evaluate("nmap_scan", "8.8.8.8")
        assert decision.allowed is True
        assert decision.reason == ""

    def test_benign_command_allowed(self):
        decision = _guard(["10.0.0.0/24"], "enforce").evaluate("do_report", "8.8.8.8")
        assert decision.allowed is True
        assert decision.reason == ""

    def test_empty_target_allowed(self):
        decision = _guard(["10.0.0.0/24"], "enforce").evaluate("nmap_scan", "")
        assert decision.allowed is True

    def test_in_scope_allowed(self):
        decision = _guard(["10.0.0.0/24"], "enforce").evaluate("nmap_scan", "10.0.0.5")
        assert decision.allowed is True
        assert decision.reason == ""

    def test_out_of_scope_warn_allows_with_reason(self):
        decision = _guard(["10.0.0.0/24"], "warn").evaluate("nmap_scan", "8.8.8.8")
        assert decision.allowed is True
        assert decision.needs_confirmation is False
        assert "OUTSIDE the authorized scope" in decision.reason
        assert decision.mode is ScopeMode.WARN

    def test_out_of_scope_enforce_blocks(self):
        decision = _guard(["10.0.0.0/24"], "enforce").evaluate("nmap_scan", "8.8.8.8")
        assert decision.allowed is False
        assert decision.needs_confirmation is True
        assert "8.8.8.8" in decision.reason
        assert decision.mode is ScopeMode.ENFORCE

    def test_classifier_exception_fails_open(self):
        def boom(_name):
            raise RuntimeError("classifier failure")

        guard = ScopeGuard(["10.0.0.0/24"], "enforce", boom)
        decision = guard.evaluate("nmap_scan", "8.8.8.8")
        assert decision.allowed is True

    def test_decision_is_value_object(self):
        decision = _guard(["10.0.0.0/24"], "warn").evaluate("nmap_scan", "8.8.8.8")
        assert isinstance(decision, ScopeDecision)
        assert decision.command == "nmap_scan"
        assert decision.target == "8.8.8.8"


class TestOffensiveCategoryDrift:
    """The hardcoded offensive category strings must stay in sync with utils."""

    def test_categories_exist_in_utils(self):
        import utils

        known = {
            value
            for name, value in vars(utils).items()
            if name.endswith("_category") and isinstance(value, str)
        }
        known.add("15. Adversary YAML.")
        missing = OFFENSIVE_CATEGORIES - known
        assert not missing, f"offensive categories not defined in utils: {missing}"
