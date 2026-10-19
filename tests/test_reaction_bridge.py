"""BDD tests for the reaction bridge (planner injections + cred reuse)."""

from __future__ import annotations

import pytest

from modules.reaction_bridge import ReactionPick, find_credentials, load_reaction_triggers, save_decisions


class TestDecisionBuffer:
    """Reactive decisions park and drain as planner triggers."""

    def test_save_and_drain_roundtrip(self, monkeypatch, tmp_path):
        """Given parked picks, When the planner drains, Then triggers appear once."""
        story = "reactions survive the round boundary"
        monkeypatch.setattr("modules.reaction_bridge._store_path", lambda name: tmp_path / name)
        save_decisions("t1", [ReactionPick(command="crackmapexec 10.0.0.5", reason="lateral", priority=2)])
        triggers = load_reaction_triggers("t1", consumer="planner")
        assert triggers and triggers[0]["kind"] == "reaction", story
        assert "crackmapexec" in triggers[0]["text"], story
        assert load_reaction_triggers("t1", consumer="planner") == [], story

    def test_assign_rhost_becomes_probe(self, monkeypatch, tmp_path):
        """Given an assign rhost pick, Then the trigger text is a probe ip intent."""
        story = "host discovery is planning info, not a command to run"
        monkeypatch.setattr("modules.reaction_bridge._store_path", lambda name: tmp_path / name)
        save_decisions("t1", [ReactionPick(command="assign rhost 10.9.9.8", priority=3)])
        triggers = load_reaction_triggers("t1", consumer="planner")
        assert triggers and triggers[0]["text"].startswith("probe ip 10.9.9.8"), story

    def test_dedupe_and_cap(self, monkeypatch, tmp_path):
        """Given repeated picks and overflow, Then the buffer stays bounded and unique."""
        story = "no planner noise"
        monkeypatch.setattr("modules.reaction_bridge._store_path", lambda name: tmp_path / name)
        for _ in range(3):
            save_decisions("t1", [ReactionPick(command="lynis"), ReactionPick(command="lynis")])
        for idx in range(10):
            save_decisions("t1", [ReactionPick(command=f"cmd{idx}")])
        triggers = load_reaction_triggers("t1", consumer="planner")
        assert len(triggers) <= 6, story
        assert len({t["text"] for t in triggers}) == len(triggers), story


class TestCredentialExtraction:
    """Cred pairs and hashes from raw output, placeholders rejected."""

    def test_pair_lines_extracted(self):
        """Given 'user:pass' lines, Then pairs are returned."""
        story = "plain kv lines are the common case"
        pairs = find_credentials("Login OK\nsvc_admin:S3cr3t!\nx:x\n")
        assert {"username": "svc_admin", "password": "S3cr3t!"} in pairs, story

    def test_placeholders_dropped(self):
        """Given placeholder-looking values, Then they are rejected."""
        story = "guessing creds from template text is noise"
        pairs = find_credentials("CHANGE_ME:CHANGE_ME\nadmin:password\nroot:toor\n")
        assert not any(p.get("username", "").lower() in ("root", "admin") and p.get("password", "").lower() in ("toor", "password") for p in pairs), story

    def test_hash_detected(self):
        """Given an md5-like line, Then a hash entry appears."""
        story = "hashes are creds too"
        pairs = find_credentials("d41d8cd98f00b204e9800998ecf8427e")
        assert any(hash_value := p.get("hash", "") for p in pairs), story
