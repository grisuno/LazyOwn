#!/usr/bin/env python3
"""
Tests for lazyown_objective.py — ObjectiveStore and SoulUpdater.

All file I/O is redirected to tmp_path (pytest fixture).
No writes to the real sessions/ directory.
"""

from __future__ import annotations

import datetime
import json
import sys
from pathlib import Path

import pytest

_SKILLS_DIR = Path(__file__).parent.parent
if str(_SKILLS_DIR) not in sys.path:
    sys.path.insert(0, str(_SKILLS_DIR))

from lazyown_objective import (
    DEFAULT_SOUL,
    OBJECTIVE_TTL_HOURS,
    ObjectiveStore,
    SoulUpdater,
)


# ─────────────────────────────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────────────────────────────


def _store(tmp_path: Path) -> ObjectiveStore:
    """Return an ObjectiveStore backed by tmp_path."""
    return ObjectiveStore(path=tmp_path / "objectives.jsonl")


def _soul_updater(tmp_path: Path) -> SoulUpdater:
    """Return a SoulUpdater whose soul file lives in tmp_path."""
    import lazyown_objective as _mod
    soul_file = tmp_path / "soul.md"
    # Write the default soul so it exists before patching
    soul_file.write_text(DEFAULT_SOUL)
    su = SoulUpdater.__new__(SoulUpdater)
    su._path = soul_file
    return su


# ─────────────────────────────────────────────────────────────────────────────
# ObjectiveStore tests
# ─────────────────────────────────────────────────────────────────────────────


class TestObjectiveStore:
    def test_inject_basic(self, tmp_path):
        """inject() → objective appears in list_pending()."""
        store = _store(tmp_path)
        obj = store.inject("Enumerate SMB shares on 10.10.11.78", priority="high")
        pending = store.list_pending()
        ids = [o.id for o in pending]
        assert obj.id in ids
        assert obj.status == "pending"
        assert obj.priority == "high"

    def test_dedup(self, tmp_path):
        """Inject same text twice → only one pending objective."""
        store = _store(tmp_path)
        text = "Run nmap full port scan against 10.10.11.78"
        o1 = store.inject(text, priority="medium")
        o2 = store.inject(text, priority="medium")
        # Both calls should return the same ID
        assert o1.id == o2.id
        pending = store.list_pending()
        matching = [o for o in pending if ObjectiveStore._text_hash(o.text) == ObjectiveStore._text_hash(text)]
        assert len(matching) == 1

    def test_ttl_expiry(self, tmp_path):
        """Low-priority objective with created_at 48h ago → cleanup() marks it skipped."""
        store = _store(tmp_path)
        obj = store.inject("Low priority old task", priority="low")

        # Manually backdate the created_at to 48 hours ago
        objs = store._load_all()
        past = (
            datetime.datetime.now(datetime.timezone.utc)
            - datetime.timedelta(hours=48)
        ).isoformat()
        for o in objs:
            if o.id == obj.id:
                o.created_at = past
                o.updated_at = past
        store._save_all(objs)

        # TTL for "low" is 24h, so 48h should expire it
        assert OBJECTIVE_TTL_HOURS["low"] == 24.0
        expired = store.cleanup()
        assert expired >= 1

        # Verify it's now skipped
        all_objs = store.list_all(status="all", limit=100)
        skipped = [o for o in all_objs if o.id == obj.id]
        assert len(skipped) == 1
        assert skipped[0].status == "skipped"

    def test_next_pending_priority(self, tmp_path):
        """Inject low + critical → next_pending() returns critical."""
        store = _store(tmp_path)
        low_obj = store.inject("Low importance task", priority="low")
        critical_obj = store.inject("CRITICAL: exploit CVE-2021-41773 NOW", priority="critical")
        nxt = store.next_pending()
        assert nxt is not None
        assert nxt.priority == "critical"
        assert nxt.id == critical_obj.id

    def test_next_pending_fifo_same_priority(self, tmp_path):
        """Two medium objectives → next_pending() returns the earlier one (FIFO)."""
        store = _store(tmp_path)
        o1 = store.inject("First medium task", priority="medium")
        o2 = store.inject("Second medium task", priority="medium")
        nxt = store.next_pending()
        assert nxt is not None
        # Should return first injected (FIFO within same priority)
        assert nxt.id == o1.id

    def test_complete(self, tmp_path):
        """complete() marks objective as done."""
        store = _store(tmp_path)
        obj = store.inject("Task to complete", priority="medium")
        ok = store.complete(obj.id, notes="finished successfully")
        assert ok is True
        all_objs = store.list_all(status="all", limit=100)
        done = [o for o in all_objs if o.id == obj.id]
        assert done[0].status == "done"

    def test_block(self, tmp_path):
        """block() marks objective as blocked with reason."""
        store = _store(tmp_path)
        obj = store.inject("Blocked task", priority="high")
        ok = store.block(obj.id, "firewall blocking access")
        assert ok is True
        all_objs = store.list_all(status="all")
        blocked = [o for o in all_objs if o.id == obj.id]
        assert blocked[0].status == "blocked"
        assert "firewall" in blocked[0].notes

    def test_inject_invalid_priority_defaults_medium(self, tmp_path):
        """Invalid priority string → falls back to 'medium'."""
        store = _store(tmp_path)
        obj = store.inject("Task with bad priority", priority="ultra-mega-critical")
        assert obj.priority == "medium"

    def test_list_pending_empty(self, tmp_path):
        """Empty store → list_pending() returns []."""
        store = _store(tmp_path)
        assert store.list_pending() == []

    def test_next_pending_none_when_empty(self, tmp_path):
        """Empty store → next_pending() returns None."""
        store = _store(tmp_path)
        assert store.next_pending() is None

    def test_objectives_persist_on_disk(self, tmp_path):
        """Inject objective, create fresh store from same path → still in pending."""
        path = tmp_path / "objectives.jsonl"
        store1 = ObjectiveStore(path=path)
        obj = store1.inject("Persistent objective", priority="high")

        store2 = ObjectiveStore(path=path)
        pending = store2.list_pending()
        assert any(o.id == obj.id for o in pending)

    def test_cleanup_medium_72h_ttl(self, tmp_path):
        """Medium-priority objective 80h old → expires (TTL=72h)."""
        store = _store(tmp_path)
        obj = store.inject("Medium old task", priority="medium")
        objs = store._load_all()
        past = (
            datetime.datetime.now(datetime.timezone.utc)
            - datetime.timedelta(hours=80)
        ).isoformat()
        for o in objs:
            if o.id == obj.id:
                o.created_at = past
                o.updated_at = past
        store._save_all(objs)

        assert OBJECTIVE_TTL_HOURS["medium"] == 72.0
        expired = store.cleanup()
        assert expired >= 1

    def test_cleanup_critical_never_expires(self, tmp_path):
        """Critical-priority objective 1000h old → does NOT expire (TTL=None)."""
        store = _store(tmp_path)
        obj = store.inject("Ancient critical task", priority="critical")
        objs = store._load_all()
        past = (
            datetime.datetime.now(datetime.timezone.utc)
            - datetime.timedelta(hours=1000)
        ).isoformat()
        for o in objs:
            if o.id == obj.id:
                o.created_at = past
                o.updated_at = past
        store._save_all(objs)

        assert OBJECTIVE_TTL_HOURS["critical"] is None
        expired = store.cleanup()
        assert expired == 0


# ─────────────────────────────────────────────────────────────────────────────
# SoulUpdater tests
# ─────────────────────────────────────────────────────────────────────────────


class TestSoulUpdater:
    def test_soul_updater_patch_line(self, tmp_path):
        """update_phase('exploit') → soul.md contains 'Phase:' followed by 'exploit'."""
        su = _soul_updater(tmp_path)
        su.update_phase("exploit")
        content = su._path.read_text()
        # The regex uses \g<1> which preserves the original spacing (e.g. "Phase:  ")
        # so we check that a Phase: line exists and contains 'exploit'
        phase_lines = [ln for ln in content.splitlines() if ln.startswith("Phase:")]
        assert len(phase_lines) >= 1, "No Phase: line found"
        assert "exploit" in phase_lines[0]

    def test_soul_updater_target_line(self, tmp_path):
        """update_target('10.10.11.78') → soul.md contains 'Target: 10.10.11.78'."""
        su = _soul_updater(tmp_path)
        su.update_target("10.10.11.78")
        content = su._path.read_text()
        assert "Target: 10.10.11.78" in content

    def test_soul_updater_section(self, tmp_path):
        """update_credentials([{username, password}]) → soul.md has Known Credentials section."""
        su = _soul_updater(tmp_path)
        su.update_credentials([{"username": "admin", "password": "pass"}])
        content = su._path.read_text()
        assert "## Known Credentials" in content
        assert "admin:pass" in content

    def test_soul_updater_credentials_hash(self, tmp_path):
        """update_credentials with hash_value → soul.md shows truncated hash with (NTLM) tag."""
        su = _soul_updater(tmp_path)
        su.update_credentials([
            {"username": "jsmith", "password": "", "hash_value": "aabbccdd11223344aabbccdd11223344"}
        ])
        content = su._path.read_text()
        assert "jsmith" in content
        assert "NTLM" in content

    def test_soul_updater_credentials_username_only(self, tmp_path):
        """update_credentials with username only → shows 'username only' notation."""
        su = _soul_updater(tmp_path)
        su.update_credentials([{"username": "bob", "password": "", "hash_value": ""}])
        content = su._path.read_text()
        assert "bob" in content
        assert "username only" in content

    def test_soul_updater_section_os(self, tmp_path):
        """update_os() → soul.md has Detected OS section."""
        su = _soul_updater(tmp_path)
        su.update_os("Windows Server 2019", "10.10.11.78")
        content = su._path.read_text()
        assert "## Detected OS" in content
        assert "Windows Server 2019" in content

    def test_soul_updater_section_access(self, tmp_path):
        """update_access() → soul.md has Achieved Access section."""
        su = _soul_updater(tmp_path)
        su.update_access("admin", "10.10.11.78", method="evil-winrm")
        content = su._path.read_text()
        assert "## Achieved Access" in content
        assert "evil-winrm" in content

    def test_soul_updater_vulnerabilities(self, tmp_path):
        """update_vulnerabilities() → soul.md has Key Vulnerabilities section."""
        su = _soul_updater(tmp_path)
        su.update_vulnerabilities([
            {"vuln_id": "CVE-2021-34527", "severity": "critical", "title": "PrintNightmare"}
        ])
        content = su._path.read_text()
        assert "## Key Vulnerabilities" in content
        assert "CVE-2021-34527" in content
        assert "PrintNightmare" in content

    def test_soul_updater_patch_replaces_existing(self, tmp_path):
        """Calling update_phase twice → second value replaces first (not appended)."""
        su = _soul_updater(tmp_path)
        su.update_phase("recon")
        su.update_phase("exploit")
        content = su._path.read_text()
        # Should not have TWO Phase: lines with different values
        phase_lines = [l for l in content.splitlines() if l.strip().startswith("Phase:")]
        assert len(phase_lines) == 1, f"Expected 1 Phase: line, got {phase_lines}"
        assert "exploit" in phase_lines[0]

    def test_soul_updater_empty_creds_noop(self, tmp_path):
        """update_credentials([]) → soul.md unchanged (no section added)."""
        su = _soul_updater(tmp_path)
        original = su._path.read_text()
        su.update_credentials([])
        after = su._path.read_text()
        assert after == original

    def test_soul_updater_appends_new_section(self, tmp_path):
        """Section that doesn't exist yet → appended at end of file."""
        su = _soul_updater(tmp_path)
        # Remove any existing Known Credentials section from default soul
        content = su._path.read_text()
        if "## Known Credentials" not in content:
            # Confirm it's not there, then add it
            su.update_credentials([{"username": "newuser", "password": "newpass"}])
            after = su._path.read_text()
            assert "## Known Credentials" in after
