"""BDD-style tests for persistent beacon command/result history storage.

Scenario: captured implant results are appended to an ordered JSONL file that
is replayable across restarts, safe against path traversal, and isolated per
beacon id.
"""

from __future__ import annotations

from modules.beacon_history import (
    BeaconHistoryConfig,
    append_record,
    read_records,
    records_path,
    sanitize_client_id,
)


def _config(tmp_path) -> BeaconHistoryConfig:
    return BeaconHistoryConfig(base_dir=tmp_path)


class TestSanitization:
    def test_sanitize_client_id_strips_unsafe_chars(self):
        """Given: a hostile beacon id, Then: only safe chars survive."""
        assert sanitize_client_id("A/B.C| D_e-F-----") == "ABCD_e-F-----"
        assert sanitize_client_id("safe-id_1") == "safe-id_1"

    def test_records_path_is_bounded_inside_sessions(self, tmp_path):
        """Given a hostile id, Then its history path never escapes sessions."""
        cfg = _config(tmp_path)
        # When a path is resolved for a traversal attempt
        resolved = records_path("../../etc/passwd", cfg).resolve()
        # Then the normalised path stays inside the sessions root
        assert cfg.sessions_dir().resolve() in resolved.parents


class TestAppendRead:
    def test_append_then_read_round_trips(self, tmp_path):
        # Given: two records for the same beacon
        cfg = _config(tmp_path)
        assert append_record({"client_id": "lnx", "command": "id", "output": "uid=0"}, cfg)
        assert append_record({"client_id": "lnx", "command": "ip a", "output": "inet 1.2.3.4"}, cfg)
        # When: history is read back
        records = read_records("lnx", cfg)
        # Then: both records come back in order
        assert [r["command"] for r in records] == ["id", "ip a"]
        assert records[1]["output"] == "inet 1.2.3.4"

    def test_multiple_beacons_do_not_interleave(self, tmp_path):
        # Given two distinct beacons wrote one record each
        cfg = _config(tmp_path)
        append_record({"client_id": "alice", "command": "ls", "output": "a"}, cfg)
        append_record({"client_id": "bob", "command": "pwd", "output": "b"}, cfg)
        # Then each beacon only sees its own record
        assert read_records("alice", cfg)[0]["command"] == "ls"
        assert read_records("bob", cfg)[0]["command"] == "pwd"

    def test_skips_malformed_lines(self, tmp_path):
        # Given a history file with one malformed JSON line
        cfg = _config(tmp_path)
        append_record({"client_id": "lnx", "command": "ok"}, cfg)
        path = records_path("lnx", cfg)
        with path.open("a", encoding="utf-8") as fh:
            fh.write("not-json\n")
        # When: read back
        records = read_records("lnx", cfg)
        # Then: the valid record survives and the malformed one is skipped
        assert len(records) == 1
        assert records[0]["command"] == "ok"

    def test_missing_history_reads_empty(self, tmp_path):
        assert read_records("never-existed", _config(tmp_path)) == []

    def test_record_without_client_id_is_rejected(self, tmp_path):
        # Given a record missing its client id
        # When append is attempted
        ok = append_record({"command": "id", "output": "x"}, _config(tmp_path))
        # Then it is rejected as invalid
        assert ok is False
