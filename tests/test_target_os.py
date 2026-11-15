"""Contract tests for modules/loop/target_os.py.

Pins the single-responsibility OS ground-truth contract extracted from the
daemon ``_run_objective`` coroutine: TTL-based OS inference, the canonical
``os_id`` mapping, and the independently-guarded persistence side effects.
"""

import asyncio
import json
import subprocess

import pytest

from modules.loop import target_os


class _FakeCompleted:
    """Minimal stand-in for subprocess.CompletedProcess."""

    def __init__(self, stdout: str, stderr: str = "") -> None:
        self.stdout = stdout
        self.stderr = stderr


class _FakeWorldModel:
    """Captures update_host calls over a seeded snapshot."""

    def __init__(self, snapshot: dict) -> None:
        self._snapshot = snapshot
        self.updates: list[tuple[str, dict]] = []

    def snapshot(self) -> dict:
        return self._snapshot

    def update_host(self, target: str, **kwargs) -> None:
        self.updates.append((target, kwargs))


def _run_detect(monkeypatch, ping_output: str) -> str:
    """Drive detect_target_os with a stubbed ping, no real subprocess."""

    def _fake_run(*_args, **_kwargs):
        return _FakeCompleted(ping_output)

    monkeypatch.setattr(subprocess, "run", _fake_run)
    loop = asyncio.new_event_loop()
    try:
        return loop.run_until_complete(target_os.detect_target_os("10.0.0.1", loop))
    finally:
        loop.close()


def test_detect_linux_ttl(monkeypatch):
    assert _run_detect(monkeypatch, "64 bytes ttl=64 time=0.1 ms") == "linux"


def test_detect_windows_ttl(monkeypatch):
    assert _run_detect(monkeypatch, "Reply ttl=128") == "windows"


def test_detect_unknown_high_ttl(monkeypatch):
    assert _run_detect(monkeypatch, "ttl=250") == "unknown"


def test_detect_unknown_without_ttl(monkeypatch):
    assert _run_detect(monkeypatch, "no reply") == "unknown"


def test_detect_unknown_on_exception(monkeypatch):
    def _boom(*_args, **_kwargs):
        raise OSError("ping missing")

    monkeypatch.setattr(subprocess, "run", _boom)
    loop = asyncio.new_event_loop()
    try:
        assert loop.run_until_complete(target_os.detect_target_os("10.0.0.1", loop)) == "unknown"
    finally:
        loop.close()


@pytest.mark.parametrize(
    "label,expected",
    [("linux", "1"), ("windows", "2"), ("unknown", "4"), ("martian", "4")],
)
def test_os_id_for(label, expected):
    assert target_os.os_id_for(label) == expected


def _collect_emit() -> tuple[list[tuple[str, dict]], object]:
    events: list[tuple[str, dict]] = []

    def _emit(name, payload):
        events.append((name, payload))

    return events, _emit


def test_persist_unknown_only_emits(tmp_path):
    events, emit = _collect_emit()
    wm = _FakeWorldModel({"hosts": {}})
    payload_file = tmp_path / "payload.json"

    target_os.persist_detected_os(
        "obj1",
        "10.0.0.1",
        "unknown",
        world_model=wm,
        emit=emit,
        load_payload=lambda: {},
        sessions_dir=tmp_path,
        payload_file=payload_file,
    )

    assert [e[0] for e in events] == ["OS_DETECTED"]
    assert wm.updates == []
    assert not (tmp_path / "os.json").exists()
    assert not payload_file.exists()


def test_persist_known_writes_all(tmp_path):
    events, emit = _collect_emit()
    wm = _FakeWorldModel({"hosts": {}})
    payload_file = tmp_path / "payload.json"
    saved: dict = {}

    import core.config as core_config

    def _fake_save(payload, path):
        saved["payload"] = payload
        saved["path"] = path

    original_save = core_config.save_payload
    core_config.save_payload = _fake_save
    try:
        target_os.persist_detected_os(
            "obj1",
            "10.0.0.1",
            "linux",
            world_model=wm,
            emit=emit,
            load_payload=lambda: {"os_id": "4"},
            sessions_dir=tmp_path,
            payload_file=payload_file,
        )
    finally:
        core_config.save_payload = original_save

    assert ("OS_DETECTED", {"objective_id": "obj1", "target": "10.0.0.1", "os": "linux"}) in events
    assert wm.updates == [("10.0.0.1", {"os_hint": "linux"})]
    assert saved["payload"]["os_id"] == "1"
    os_entry = json.loads((tmp_path / "os.json").read_text())
    assert os_entry[0]["id"] == "1"
    assert os_entry[0]["os"] == "Linux"
    assert os_entry[0]["ttl"] == 64
    assert os_entry[0]["state"] == "active"


def test_persist_known_skips_payload_when_unchanged(tmp_path):
    events, emit = _collect_emit()
    wm = _FakeWorldModel({"hosts": {}})
    calls: list = []

    import core.config as core_config

    original_save = core_config.save_payload
    core_config.save_payload = lambda payload, path: calls.append(payload)
    try:
        target_os.persist_detected_os(
            "obj1",
            "10.0.0.1",
            "linux",
            world_model=wm,
            emit=emit,
            load_payload=lambda: {"os_id": "1"},
            sessions_dir=tmp_path,
            payload_file=tmp_path / "payload.json",
        )
    finally:
        core_config.save_payload = original_save

    assert calls == []
    assert (tmp_path / "os.json").exists()


def test_persist_known_respects_existing_os_hint(tmp_path):
    events, emit = _collect_emit()
    wm = _FakeWorldModel({"hosts": {"10.0.0.1": {"os_hint": "windows"}}})

    target_os.persist_detected_os(
        "obj1",
        "10.0.0.1",
        "linux",
        world_model=wm,
        emit=emit,
        load_payload=lambda: {"os_id": "1"},
        sessions_dir=tmp_path,
        payload_file=tmp_path / "payload.json",
    )

    assert wm.updates == []
