"""Resumable, hash-identified shell sessions.

A real remote socket dies with the process, so what is persisted is the
session descriptor -- target, the exploit primitive that produced the shell,
port, lhost and provenance -- under a content-hashed id. ``resume`` re-opens
the shell through the recorded primitive, exactly how serious post-exploitation
tooling reconnects over a non-persistent transport.
"""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))
sys.path.insert(0, str(REPO_ROOT / "modules"))

import pytest  # noqa: E402

from modules import shell_session_store as store  # noqa: E402


@pytest.fixture()
def sandbox(tmp_path, monkeypatch):
    monkeypatch.setattr(store, "_SESSIONS_DIR", tmp_path, raising=False)
    return tmp_path


def test_session_id_is_stable_hash(sandbox):
    a = store.session_id("10.0.0.2", "ms2_vsftpd_backdoor", "2026-01-01T00:00:00Z")
    b = store.session_id("10.0.0.2", "ms2_vsftpd_backdoor", "2026-01-01T00:00:00Z")
    c = store.session_id("10.0.0.3", "ms2_vsftpd_backdoor", "2026-01-01T00:00:00Z")
    assert a == b
    assert a != c
    assert len(a) == store.ID_LENGTH
    assert all(ch in "0123456789abcdef" for ch in a)


def test_register_persists_descriptor(sandbox):
    rec = store.register("10.0.0.2", via="ms2_distcc_exec", port=3632, lhost="10.0.0.1")
    assert rec["id"]
    assert rec["target"] == "10.0.0.2"
    assert rec["via"] == "ms2_distcc_exec"
    assert rec["port"] == 3632
    assert rec["status"] == "live"
    path = sandbox / "shell_sessions" / f"{rec['id']}.json"
    assert path.exists()
    assert store.get(rec["id"])["via"] == "ms2_distcc_exec"


def test_register_is_idempotent_per_target_via(sandbox):
    first = store.register("10.0.0.2", via="ms2_distcc_exec", port=3632)
    second = store.register("10.0.0.2", via="ms2_distcc_exec", port=3632)
    assert first["id"] == second["id"]
    assert len(store.list_sessions("10.0.0.2")) == 1


def test_list_and_mark_closed(sandbox):
    store.register("10.0.0.2", via="ms2_distcc_exec", port=3632)
    store.register("10.0.0.2", via="ms2_unrealircd_backdoor", port=6667)
    assert len(store.list_sessions("10.0.0.2")) == 2
    assert store.mark_closed("10.0.0.2", via="ms2_distcc_exec") == 1
    rows = {r["via"]: r for r in store.list_sessions("10.0.0.2")}
    assert rows["ms2_distcc_exec"]["status"] == "closed"
    assert rows["ms2_unrealircd_backdoor"]["status"] == "live"


def test_resume_reopens_through_recorded_primitive(sandbox, monkeypatch):
    rec = store.register("10.0.0.2", via="ms2_distcc_exec", port=3632, lhost="10.0.0.1")
    monkeypatch.setattr(store, "mark_closed", store.mark_closed)
    calls: list[tuple] = []

    def fake_reopen(target, via, lhost):
        calls.append((target, via, lhost))
        return True

    monkeypatch.setattr(store, "_reopen_primitive", fake_reopen)
    out = store.resume(rec["id"])
    assert out["ok"] is True
    assert out["target"] == "10.0.0.2"
    assert out["via"] == "ms2_distcc_exec"
    assert calls == [("10.0.0.2", "ms2_distcc_exec", "10.0.0.1")]
    assert store.get(rec["id"])["resume_count"] == 1


def test_resume_unknown_id_fails_cleanly(sandbox):
    out = store.resume("deadbeefdeadbeef")
    assert out["ok"] is False
    assert "not found" in out["error"].lower()


def test_resume_marks_stale_when_primitive_dead(sandbox, monkeypatch):
    rec = store.register("10.0.0.2", via="ms2_distcc_exec", port=3632)
    monkeypatch.setattr(store, "_reopen_primitive", lambda *a, **k: False)
    out = store.resume(rec["id"])
    assert out["ok"] is False
    assert store.get(rec["id"])["status"] == "stale"


def test_corrupt_descriptor_is_skipped(sandbox):
    d = sandbox / "shell_sessions"
    d.mkdir(parents=True, exist_ok=True)
    (d / "garbage.json").write_text("{not json", encoding="utf-8")
    store.register("10.0.0.2", via="ms2_distcc_exec", port=3632)
    assert len(store.list_sessions()) == 1
