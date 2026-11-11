"""Tests for durable raw wire capture and its TrafficLog wiring.

Capture must content-address by digest, be idempotent, reject unsafe digests
before any path join, and bound its writes. The TrafficLog integration must
snapshot only truncated exchanges and reconstruct the full output from the wire
store once the inline record no longer holds it.
"""

from __future__ import annotations

from modules.wire_capture import WireStore


def test_capture_and_fetch_round_trip(tmp_path):
    store = WireStore("t1", base_dir=tmp_path)
    assert store.capture("abc123", "the full raw body") == "abc123"
    assert store.fetch("abc123") == "the full raw body"
    assert store.has("abc123") is True


def test_capture_is_idempotent(tmp_path):
    store = WireStore("t1", base_dir=tmp_path)
    store.capture("abc123", "first")
    store.capture("abc123", "second")
    assert store.fetch("abc123") == "first"


def test_capture_rejects_unsafe_digest(tmp_path):
    store = WireStore("t1", base_dir=tmp_path)
    assert store.capture("../../etc/passwd", "x") == ""
    assert store.capture("", "x") == ""
    assert store.fetch("../../etc/passwd") is None


def test_capture_bounds_write(tmp_path):
    store = WireStore("t1", base_dir=tmp_path)
    store.capture("abc123", "A" * 100, max_bytes=10)
    assert store.fetch("abc123") == "A" * 10


def test_fetch_missing_returns_none(tmp_path):
    store = WireStore("t1", base_dir=tmp_path)
    assert store.fetch("deadbeef") is None
    assert store.has("deadbeef") is False


def test_task_isolation(tmp_path):
    a = WireStore("task-a", base_dir=tmp_path)
    b = WireStore("task-b", base_dir=tmp_path)
    a.capture("aaaaaa", "body")
    assert a.has("aaaaaa") and not b.has("aaaaaa")


def test_trafficlog_captures_truncated_and_reconstructs(tmp_path, monkeypatch):
    import modules.lazy_loop as loop

    monkeypatch.setattr(loop, "STORE_DIR", tmp_path / "lazy", raising=False)
    monkeypatch.setattr("modules.wire_capture._BASE_DIR", tmp_path, raising=False)
    monkeypatch.setattr(loop, "TRAFFIC_INLINE_CUTOFF", 16, raising=False)
    monkeypatch.setattr(loop, "wire_capture_enabled", lambda: True)

    traffic = loop.TrafficLog("task-wire")
    big = "RAWLINE-" + "Z" * 200
    record = traffic.record("bash", "curl http://t/", big)
    assert record["truncated"] is True

    store = WireStore("task-wire", base_dir=tmp_path / "sessions" / "wire")
    assert store.has(record["digest"]) is True

    traffic._path.write_text("", encoding="utf-8")
    assert traffic.wire(record["digest"]) == big


def test_trafficlog_small_output_not_captured(tmp_path, monkeypatch):
    import modules.lazy_loop as loop

    monkeypatch.setattr(loop, "STORE_DIR", tmp_path / "lazy", raising=False)
    monkeypatch.setattr("modules.wire_capture._BASE_DIR", tmp_path, raising=False)
    monkeypatch.setattr(loop, "wire_capture_enabled", lambda: True)

    traffic = loop.TrafficLog("task-small")
    record = traffic.record("bash", "id", "uid=0(root)")
    assert record["truncated"] is False
    store = WireStore("task-small", base_dir=tmp_path / "sessions" / "wire")
    assert store.has(record["digest"]) is False
    assert traffic.wire(record["digest"]) == "uid=0(root)"


def test_trafficlog_capture_disabled(tmp_path, monkeypatch):
    import modules.lazy_loop as loop

    monkeypatch.setattr(loop, "STORE_DIR", tmp_path / "lazy", raising=False)
    monkeypatch.setattr("modules.wire_capture._BASE_DIR", tmp_path, raising=False)
    monkeypatch.setattr(loop, "TRAFFIC_INLINE_CUTOFF", 16, raising=False)
    monkeypatch.setattr(loop, "wire_capture_enabled", lambda: False)

    traffic = loop.TrafficLog("task-off")
    record = traffic.record("bash", "curl http://t/", "Z" * 200)
    store = WireStore("task-off", base_dir=tmp_path / "sessions" / "wire")
    assert store.has(record["digest"]) is False
