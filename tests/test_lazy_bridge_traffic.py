"""Incremental LAZY traffic mirroring (stall regression).

The loop used to replay every traffic row on each intel sync, blocking the
worker thread long enough to trigger the stall watchdog. These tests pin
the byte-offset cursor and the partial-line safety.
"""

from __future__ import annotations

import json

from modules import lazy_bridge
from modules.traffic_recorder import TrafficRecorder


def _sandbox(tmp_path, monkeypatch):
    lazy_dir = tmp_path / "lazy"
    sessions_dir = tmp_path / "sessions"
    lazy_dir.mkdir()
    sessions_dir.mkdir()
    monkeypatch.setattr(lazy_bridge, "LAZY_DIR", lazy_dir)
    monkeypatch.setattr(lazy_bridge, "SESSIONS_DIR", sessions_dir)
    (lazy_dir / "tasks.json").write_text(
        json.dumps({"tasks": {"t1": {"goal": "probe", "status": "running"}}}), encoding="utf-8"
    )
    return lazy_dir, sessions_dir


def _append(path, rows):
    with path.open("a", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row) + "\n")


def _exchanges(sessions_dir):
    return TrafficRecorder(sessions_dir / "traffic").since(0, 100)


def test_traffic_mirror_is_incremental(tmp_path, monkeypatch):
    """Only new rows are mirrored and the byte cursor is persisted."""
    lazy_dir, sessions_dir = _sandbox(tmp_path, monkeypatch)
    path = lazy_dir / "traffic_t1.jsonl"
    _append(path, [{"command": "id", "output": "uid=0"}, {"command": "ls", "output": "a"}])

    assert lazy_bridge.pull_traffic_to_recorder()["mirrored"] == 2
    assert len(_exchanges(sessions_dir)) == 2

    assert lazy_bridge.pull_traffic_to_recorder()["mirrored"] == 0
    assert len(_exchanges(sessions_dir)) == 2

    _append(path, [{"command": "uname", "output": "Linux"}])
    progress: list[str] = []
    assert lazy_bridge.pull_traffic_to_recorder(progress=progress.append)["mirrored"] == 1
    assert len(_exchanges(sessions_dir)) == 3
    assert any("1 new row" in line for line in progress)

    state = json.loads((sessions_dir / "lazy_bridge_sync.json").read_text(encoding="utf-8"))
    assert state["pull_traffic_offsets"]["summary"]["t1"] == path.stat().st_size


def test_partial_line_is_retried(tmp_path, monkeypatch):
    """A trailing partial write is not consumed until it is complete."""
    lazy_dir, sessions_dir = _sandbox(tmp_path, monkeypatch)
    path = lazy_dir / "traffic_t1.jsonl"
    _append(path, [{"command": "id", "output": "uid=0"}])
    with path.open("ab") as handle:
        handle.write(b'{"command": "half"')

    assert lazy_bridge.pull_traffic_to_recorder()["mirrored"] == 1
    assert len(_exchanges(sessions_dir)) == 1

    with path.open("ab") as handle:
        handle.write(b', "output": "ok"}\n')
    assert lazy_bridge.pull_traffic_to_recorder()["mirrored"] == 1
    assert len(_exchanges(sessions_dir)) == 2


def test_progress_callback_survives_failures(tmp_path, monkeypatch):
    """A raising progress callback never aborts the mirror."""
    lazy_dir, sessions_dir = _sandbox(tmp_path, monkeypatch)
    _append(lazy_dir / "traffic_t1.jsonl", [{"command": "id", "output": "uid=0"}])

    def _boom(_text):
        raise RuntimeError("operator callback")

    assert lazy_bridge.pull_traffic_to_recorder(progress=_boom)["mirrored"] == 1
    assert len(_exchanges(sessions_dir)) == 1
