"""Contract tests for the beacon storage package.

Covers path confinement, FIFO command queue behaviour, recon-state markers
and result-history delegation for :class:`lazyc2.beacons.BeaconStore`.
"""

from __future__ import annotations

import json

import pytest

from lazyc2.beacons import BeaconPathError, BeaconStore
from modules.beacon_history import BeaconHistoryConfig


def _store(base_dir) -> BeaconStore:
    return BeaconStore(base_dir=base_dir, history_config=BeaconHistoryConfig(base_dir=base_dir))


class TestQueuePath:
    def test_queue_path_stays_inside_base(self, tmp_path):
        store = _store(tmp_path)
        path = store.queue_path("beacon-1")
        assert path.name == "cmd_beacon-1.json"
        assert path.parent == tmp_path.resolve()

    def test_queue_path_sanitizes_traversal(self, tmp_path):
        store = _store(tmp_path)
        path = store.queue_path("../../etc/passwd")
        assert path.name == "cmd_etcpasswd.json"
        assert path.parent == tmp_path.resolve()

    def test_queue_path_rejects_empty_id(self, tmp_path):
        store = _store(tmp_path)
        with pytest.raises(BeaconPathError):
            store.queue_path("")

    def test_queue_path_rejects_symlink_escape(self, tmp_path):
        outside = tmp_path.parent / "outside-queue.json"
        outside.write_text("[]", encoding="utf-8")
        (tmp_path / "cmd_b1.json").symlink_to(outside)
        store = _store(tmp_path)
        with pytest.raises(BeaconPathError):
            store.queue_path("b1")


class TestCommandQueue:
    def test_enqueue_pop_is_fifo(self, tmp_path):
        store = _store(tmp_path)
        assert store.enqueue("b1", "whoami") is True
        assert store.enqueue("b1", "id") is True
        assert store.pop_next("b1") == "whoami"
        assert store.pop_next("b1") == "id"
        assert store.pop_next("b1") is None

    def test_enqueue_creates_sanitized_file(self, tmp_path):
        store = _store(tmp_path)
        assert store.enqueue("../b1", "id") is True
        assert (tmp_path / "cmd_b1.json").is_file()

    def test_save_queue_leaves_no_temp_file(self, tmp_path):
        store = _store(tmp_path)
        assert store.save_queue("b1", ["one", "two"]) is True
        assert list(tmp_path.glob("*.tmp")) == []
        assert json.loads((tmp_path / "cmd_b1.json").read_text(encoding="utf-8")) == ["one", "two"]

    def test_load_queue_corrupt_file_returns_empty(self, tmp_path):
        (tmp_path / "cmd_b1.json").write_text("{not-json", encoding="utf-8")
        assert _store(tmp_path).load_queue("b1") == []

    def test_load_queue_non_array_returns_empty(self, tmp_path):
        (tmp_path / "cmd_b1.json").write_text('{"command": "id"}', encoding="utf-8")
        assert _store(tmp_path).load_queue("b1") == []

    def test_save_queue_invalid_id_returns_false(self, tmp_path):
        assert _store(tmp_path).save_queue("", ["id"]) is False


class TestReconState:
    def test_roundtrip(self, tmp_path):
        store = _store(tmp_path)
        assert store.save_recon_state("b1", {"discover_queued": True}) is True
        assert store.load_recon_state("b1") == {"discover_queued": True}

    def test_missing_state_returns_empty(self, tmp_path):
        assert _store(tmp_path).load_recon_state("ghost") == {}

    def test_corrupt_state_returns_empty(self, tmp_path):
        store = _store(tmp_path)
        path = store.recon_state_path("b1")
        path.parent.mkdir(parents=True)
        path.write_text("[1, 2]", encoding="utf-8")
        assert store.load_recon_state("b1") == {}

    def test_state_path_confined(self, tmp_path):
        store = _store(tmp_path)
        path = store.recon_state_path("b1")
        assert path == (tmp_path / "sessions" / "b1" / "c2" / "recon_state.json").resolve()

    def test_state_path_rejects_empty_id(self, tmp_path):
        with pytest.raises(BeaconPathError):
            _store(tmp_path).recon_state_path("")


class TestHistory:
    def test_append_and_read(self, tmp_path):
        store = _store(tmp_path)
        record = {"client_id": "b1", "command": "id", "output": "uid=0"}
        assert store.append_record(record) is True
        assert store.read_records("b1") == [record]

    def test_read_missing_history_returns_empty(self, tmp_path):
        assert _store(tmp_path).read_records("ghost") == []

    def test_read_empty_id_returns_empty(self, tmp_path):
        assert _store(tmp_path).read_records("") == []

    def test_history_path_uses_sessions_layout(self, tmp_path):
        store = _store(tmp_path)
        assert store.history_path("b1") == (tmp_path / "sessions" / "b1.records.jsonl").resolve()
