"""Tests for cli.reactive_hints — expanded kill-chain tables.

Covers:
    - New commands in _KILL_CHAIN_NEXT (auto_pwn, chain, hunt, nuclei, yara, etc.)
    - New commands in _PHASE_PRIORITY
    - New session tips and protips
    - Protip trigger functions
"""

from __future__ import annotations

import pytest


class TestKillChainNextExpanded:
    def test_auto_pwn_in_lazynmap_followups(self):
        from cli.reactive_hints import _KILL_CHAIN_NEXT
        followups = _KILL_CHAIN_NEXT.get("lazynmap", [])
        assert "auto_pwn" in followups
        assert "chain" in followups or any("auto_populate" in f for f in followups)

    def test_auto_pwn_has_followups(self):
        from cli.reactive_hints import _KILL_CHAIN_NEXT
        followups = _KILL_CHAIN_NEXT.get("auto_pwn", [])
        assert len(followups) > 0
        assert any(c in followups for c in ("hunt", "l00t", "sitrep", "note", "dashboard"))

    def test_chain_has_followups(self):
        from cli.reactive_hints import _KILL_CHAIN_NEXT
        followups = _KILL_CHAIN_NEXT.get("chain", [])
        assert "hunt" in followups

    def test_hunt_has_followups(self):
        from cli.reactive_hints import _KILL_CHAIN_NEXT
        followups = _KILL_CHAIN_NEXT.get("hunt", [])
        assert len(followups) > 0

    def test_nuclei_has_followups(self):
        from cli.reactive_hints import _KILL_CHAIN_NEXT
        followups = _KILL_CHAIN_NEXT.get("nuclei", [])
        assert any(c in followups for c in ("gobuster", "lazynmap", "auto_pwn"))

    def test_yara_scan_has_followups(self):
        from cli.reactive_hints import _KILL_CHAIN_NEXT
        followups = _KILL_CHAIN_NEXT.get("yara_scan", [])
        assert len(followups) > 0

    def test_lazynmap_suggests_nuclei(self):
        from cli.reactive_hints import _KILL_CHAIN_NEXT
        followups = _KILL_CHAIN_NEXT.get("nmap", [])
        assert "nuclei" in followups

    def test_campaign_has_followups(self):
        from cli.reactive_hints import _KILL_CHAIN_NEXT
        followups = _KILL_CHAIN_NEXT.get("campaign", [])
        assert len(followups) > 0

    def test_collab_has_followups(self):
        from cli.reactive_hints import _KILL_CHAIN_NEXT
        followups = _KILL_CHAIN_NEXT.get("collab_join", [])
        assert len(followups) > 0


class TestPhasePriorityExpanded:
    def test_exploit_includes_automation(self):
        from cli.reactive_hints import _PHASE_PRIORITY
        exploit = _PHASE_PRIORITY.get("exploit", [])
        assert "auto_pwn" in exploit
        assert "chain" in exploit
        assert "hunt" in exploit

    def test_enum_includes_nuclei(self):
        from cli.reactive_hints import _PHASE_PRIORITY
        enum = _PHASE_PRIORITY.get("enum", [])
        assert "nuclei" in enum

    def test_postexp_includes_security(self):
        from cli.reactive_hints import _PHASE_PRIORITY
        postexp = _PHASE_PRIORITY.get("postexp", [])
        assert "yara_scan" in postexp
        assert "encrypt" in postexp

    def test_lateral_includes_collab(self):
        from cli.reactive_hints import _PHASE_PRIORITY
        lateral = _PHASE_PRIORITY.get("lateral", [])
        assert "collab_join" in lateral

    def test_persist_phase_exists(self):
        from cli.reactive_hints import _PHASE_PRIORITY
        assert "persist" in _PHASE_PRIORITY
        persist = _PHASE_PRIORITY["persist"]
        assert "encrypt" in persist


class TestProtipsExpanded:
    def test_tips_include_automation(self):
        from cli.protips import TIPS
        automation_tips = [t for t in TIPS if t.category == "automation"]
        assert len(automation_tips) >= 3
        commands = [t.command for t in automation_tips]
        assert "auto_pwn" in commands
        assert any("chain" in c for c in commands)
        assert any("hunt" in c for c in commands)
        assert any("nuclei" in c for c in commands)
        assert any("playbook" in c for c in commands)

    def test_tips_include_security(self):
        from cli.protips import TIPS
        security_tips = [t for t in TIPS if t.category == "security"]
        assert len(security_tips) >= 3
        commands = [t.command for t in security_tips]
        assert "encrypt" in commands
        assert "yara_scan" in commands
        assert "decrypt" in commands

    def test_tips_include_collab(self):
        from cli.protips import TIPS
        collab_tips = [t for t in TIPS if t.category == "collab"]
        assert len(collab_tips) >= 3
        commands = [t.command for t in collab_tips]
        assert any("campaign" in c for c in commands)
        assert any("collab_join" in c for c in commands)
        assert any("dashboard" in c for c in commands)
        assert any("marketplace" in c for c in commands)

    def test_tips_include_discovery(self):
        from cli.protips import TIPS
        discovery_tips = [t for t in TIPS if t.category == "discovery"]
        assert len(discovery_tips) >= 1
        commands = [t.command for t in discovery_tips]
        assert any("nuclei_marketplace" in c for c in commands)

    def test_session_tips_expanded(self):
        from cli.protips import _SESSION_TIPS
        all_text = " ".join(_SESSION_TIPS)
        assert "auto_pwn" in all_text
        assert "encrypt" in all_text
        assert "collab_join" in all_text
        assert "nuclei_marketplace" in all_text
        assert "yara_marketplace" in all_text
        assert "playbook_generate" in all_text


class TestProtipTriggers:
    def test_os_linux_detection(self):
        from cli.protips import _os_linux
        assert _os_linux({"os_id": "1"}) is True
        assert _os_linux({"os_id": "2"}) is False
        assert _os_linux({}) is False

    def test_os_windows_detection(self):
        from cli.protips import _os_windows
        assert _os_windows({"os_id": "2"}) is True
        assert _os_windows({"os_id": "1"}) is False

    def test_after_trigger(self):
        from cli.protips import _after
        assert _after({"last_cmd": "lazynmap -p 80"}, "lazynmap") is True
        assert _after({"last_cmd": "ping 10.0.0.1"}, "lazynmap") is False

    def test_phase_in_trigger(self):
        from cli.protips import _phase_in
        assert _phase_in({"phase": "exploit"}, "exploit") is True
        assert _phase_in({"phase": "recon"}, "exploit") is False
