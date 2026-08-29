"""Tests for extended HookEngine trigger matching.

Covers:
    - _contains suffix matching (substring, case-insensitive)
    - Case-insensitive exact matching
    - Case-insensitive list matching
    - Host-owned default rule
"""

from __future__ import annotations

import tempfile
from pathlib import Path

import pytest

from modules.conditional_hooks import HookEngine, HookRule


@pytest.fixture
def engine():
    with tempfile.TemporaryDirectory() as d:
        sessions = Path(d)
        rules_file = sessions / "conditional_hooks.json"
        engine = HookEngine()
        engine._rules = []
        yield engine


class TestTriggerMatchContainsSuffix:

    def test_command_contains_substring_match(self):
        rule = HookRule(
            name="test",
            trigger={"event": "command_executed", "command_contains": "linpeas"},
            actions=[],
        )
        assert _match_rule(rule, "command_executed", {"command": "curl linpeas.sh | sh"})

    def test_command_contains_case_insensitive(self):
        rule = HookRule(
            name="test",
            trigger={"event": "command_executed", "command_contains": "LINPEAS"},
            actions=[],
        )
        assert _match_rule(rule, "command_executed", {"command": "run Linpeas.sh"})

    def test_command_contains_no_match(self):
        rule = HookRule(
            name="test",
            trigger={"event": "command_executed", "command_contains": "linpeas"},
            actions=[],
        )
        assert not _match_rule(rule, "command_executed", {"command": "whoami"})

    def test_command_contains_missing_key(self):
        rule = HookRule(
            name="test",
            trigger={"event": "command_executed", "command_contains": "linpeas"},
            actions=[],
        )
        assert not _match_rule(rule, "command_executed", {"ip": "10.0.0.1"})


class TestTriggerMatchCaseInsensitive:

    def test_exact_match_case_insensitive(self):
        rule = HookRule(
            name="test",
            trigger={"event": "beacon_connected", "platform": "Linux"},
            actions=[],
        )
        assert _match_rule(rule, "beacon_connected", {"platform": "linux"})

    def test_list_match_case_insensitive(self):
        rule = HookRule(
            name="test",
            trigger={"event": "beacon_connected", "platform": ["Linux", "Windows"]},
            actions=[],
        )
        assert _match_rule(rule, "beacon_connected", {"platform": "WINDOWS"})

    def test_exact_match_different_event(self):
        rule = HookRule(
            name="test",
            trigger={"event": "beacon_connected", "platform": "linux"},
            actions=[],
        )
        assert not _match_rule(rule, "command_executed", {"platform": "linux"})


def _match_rule(rule: HookRule, event: str, context: dict) -> bool:
    from modules.conditional_hooks import HookEngine as HE

    return HE._match_trigger(HE, rule.trigger, event, context)


class TestDefaultRuleAutoPrivesc:

    def test_auto_privesc_linux_rule_exists(self):
        rules = _load_default_rules()
        names = [r["name"] for r in rules]
        assert "auto-privesc-on-beacon-linux" in names

    def test_auto_privesc_windows_rule_exists(self):
        rules = _load_default_rules()
        names = [r["name"] for r in rules]
        assert "auto-privesc-on-beacon-windows" in names

    def test_auto_crystal_ball_rule_exists(self):
        rules = _load_default_rules()
        names = [r["name"] for r in rules]
        assert "auto-crystal-ball-on-peas-output" in names

    def test_auto_loot_on_owned_rule_exists(self):
        rules = _load_default_rules()
        names = [r["name"] for r in rules]
        assert "auto-loot-on-owned" in names


def _load_default_rules():
    from modules.conditional_hooks import DEFAULT_RULES
    return list(DEFAULT_RULES)
