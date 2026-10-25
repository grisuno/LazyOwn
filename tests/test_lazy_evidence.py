"""Traffic recorder trigram search and frozen evidence package export.

Pins two parity contracts: mid-token body search through the trigram FTS
index (with in-place migration from the legacy tokenizer), and the
hash-manifested evidence zip produced at terminal status.
"""

from __future__ import annotations

import hashlib
import json
import sqlite3
import zipfile


def test_trigram_search_finds_mid_token(tmp_path):
    """A substring inside a token matches through the trigram index."""
    from modules.traffic_recorder import TrafficRecorder

    recorder = TrafficRecorder(tmp_path / "rec")
    recorder.record(
        "GET",
        "http://127.0.0.1/secrets",
        200,
        resp_body=b"aws key AKIAIOSFODNN7EXAMPLE inside body",
    )
    hits = recorder.search_body("IOSFODNN")
    assert hits and hits[0]["exchange_id"]
    assert recorder.search_body("AKIAIOS") and recorder.search_body("n7EXA")
    short = recorder.search_body("IO")
    assert short and short[0]["exchange_id"]


def test_legacy_fts_is_migrated_in_place(tmp_path):
    """A pre-trigram index is rebuilt so substring search keeps working."""
    from modules.traffic_recorder import TrafficRecorder

    base = tmp_path / "rec"
    recorder = TrafficRecorder(base)
    recorder.record("GET", "http://127.0.0.1/a", 200, resp_body=b"secret-midtoken-value")
    with sqlite3.connect(str(base / "index.sqlite")) as conn:
        conn.execute("DROP TABLE bodies_fts")
        conn.execute("CREATE VIRTUAL TABLE bodies_fts USING fts5(exchange_id UNINDEXED, text)")
    reopened = TrafficRecorder(base)
    assert reopened._fts
    with sqlite3.connect(str(base / "index.sqlite")) as conn:
        sql = conn.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name='bodies_fts'").fetchone()[0]
    assert "trigram" in str(sql).lower()
    hits = reopened.search_body("midtoken")
    assert hits and hits[0]["exchange_id"]


def test_export_evidence_freezes_files_with_hashes(tmp_path, monkeypatch):
    """The evidence zip carries a manifest whose hashes verify the files."""
    import modules.lazy_loop as loop
    from modules.lazy_engine import LazyEngine

    monkeypatch.setattr(loop, "STORE_DIR", tmp_path)
    monkeypatch.setattr(loop, "_store_path", lambda name: tmp_path / name)
    engine = LazyEngine()
    task_id = engine.create_task("gain initial access on 127.0.0.1")["task_id"]
    graph = loop.ExplorationGraph(task_id)
    graph.add_node("fact", "127.0.0.1:22 ssh open")
    package = engine.export_evidence(task_id)
    assert package["files"] >= 2
    with zipfile.ZipFile(package["path"]) as archive:
        names = set(archive.namelist())
        assert {"manifest.json", "tasks.json"}.issubset(names)
        manifest = json.loads(archive.read("manifest.json"))
        for entry in manifest["files"]:
            digest = hashlib.sha256(archive.read(entry["name"])).hexdigest()
            assert digest == entry["sha256"]
    assert manifest["task_id"] == task_id
