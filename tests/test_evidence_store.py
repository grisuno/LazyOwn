"""Tests for the durable, content-addressed evidence store and its wiring.

The store must preserve a finding's proof beyond the rotating traffic window,
address snapshots by their content digest (so re-binding is idempotent), reject
unsafe digests before they touch a path, and reap only unreferenced, aged
snapshots. The TrafficLog integration must snapshot on bind and fall back to the
store when the live traffic window no longer holds the exchange.
"""

from __future__ import annotations

import time
import types

from modules.evidence_store import EvidenceStore


def _record(digest="abc123", output="proof body"):
    return {
        "digest": digest,
        "command": "curl http://t/",
        "output": output,
        "preview": output[:50],
        "bytes": len(output),
        "template": "curl",
        "meta": {"worker": "w1"},
    }


def test_preserve_and_fetch_round_trip(tmp_path):
    store = EvidenceStore("t1", base_dir=tmp_path)
    assert store.preserve(_record()) == "abc123"
    snap = store.fetch("abc123")
    assert snap is not None and snap["output"] == "proof body"
    assert store.has("abc123") is True


def test_preserve_is_idempotent(tmp_path):
    store = EvidenceStore("t1", base_dir=tmp_path)
    store.preserve(_record(output="first"))
    first = store.fetch("abc123")
    store.preserve(_record(output="second"))
    assert store.fetch("abc123")["output"] == first["output"]


def test_preserve_rejects_unsafe_digest(tmp_path):
    store = EvidenceStore("t1", base_dir=tmp_path)
    assert store.preserve(_record(digest="../../etc/passwd")) == ""
    assert store.preserve(_record(digest="")) == ""
    assert store.fetch("../../etc/passwd") is None


def test_fetch_missing_returns_none(tmp_path):
    store = EvidenceStore("t1", base_dir=tmp_path)
    assert store.fetch("deadbeef") is None
    assert store.has("deadbeef") is False


def test_full_body_preserved_unlike_truncated_traffic(tmp_path):
    store = EvidenceStore("t1", base_dir=tmp_path)
    big = "A" * 20000
    store.preserve(_record(output=big))
    assert store.fetch("abc123")["output"] == big


def test_gc_keeps_referenced_and_recent(tmp_path):
    store = EvidenceStore("t1", base_dir=tmp_path)
    store.preserve(_record(digest="aaa111", output="kept-ref"))
    store.preserve(_record(digest="bbb222", output="kept-young"))
    store.preserve(_record(digest="ccc333", output="reaped"))
    old = store.directory / "ccc333.json"
    past = time.time() - 100000
    import os

    os.utime(old, (past, past))
    removed = store.gc(referenced={"aaa111"}, grace_seconds=86400)
    assert removed == 1
    assert store.has("aaa111") and store.has("bbb222")
    assert not store.has("ccc333")


def test_gc_empty_store(tmp_path):
    store = EvidenceStore("t1", base_dir=tmp_path)
    assert store.gc(referenced=set()) == 0


def test_task_isolation(tmp_path):
    a = EvidenceStore("task-a", base_dir=tmp_path)
    b = EvidenceStore("task-b", base_dir=tmp_path)
    a.preserve(_record(digest="aaaaaa"))
    assert a.has("aaaaaa") is True
    assert b.has("aaaaaa") is False


def test_trafficlog_preserves_on_bind_and_survives_rotation(tmp_path, monkeypatch):
    import modules.lazy_loop as loop

    monkeypatch.setattr(loop, "STORE_DIR", tmp_path / "lazy", raising=False)
    monkeypatch.setattr("modules.evidence_store._BASE_DIR", tmp_path, raising=False)
    traffic = loop.TrafficLog("task-ev")
    record = traffic.record("bash", "curl http://t/", "the real proof body")
    digest = record["digest"]

    finding = types.SimpleNamespace(kind="finding", meta={}, updated=0.0)
    graph = types.SimpleNamespace(get=lambda _id: finding, _persist=lambda: None)

    assert traffic.bind(1, digest, graph=graph, role="proof") is True

    store = EvidenceStore("task-ev", base_dir=tmp_path / "sessions" / "evidence")
    assert store.has(digest) is True

    traffic._path.write_text("", encoding="utf-8")
    fetched = traffic.get(digest)
    assert fetched is not None and "the real proof body" in fetched["output"]
