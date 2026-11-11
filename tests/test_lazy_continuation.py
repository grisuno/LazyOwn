"""Continuation record contract tests.

The campaign blackboard port: a finished task writes its settlement to
``sessions/continuations/<target>.json`` and the next task on the same
target recalls the open work as planner wake candidates.
"""

from __future__ import annotations

from modules import lazy_continuation


def _install_sessions_dir(monkeypatch, tmp_path):
    monkeypatch.setattr(lazy_continuation, "DEFAULT_DIR", tmp_path / "continuations")


class TestSaveLoad:
    """Save and load round-trip one target's record."""

    def test_save_then_load_round_trip(self, monkeypatch, tmp_path):
        _install_sessions_dir(monkeypatch, tmp_path)
        saved = lazy_continuation.save(
            "10.10.11.5",
            task_id="t1",
            goal="pwn minio",
            status="exhausted",
            settlement="found minio creds",
            findings=["minio root creds dumped"],
            next_steps=["spray creds against ssh"],
        )
        assert saved is True
        record = lazy_continuation.load("10.10.11.5")
        assert record is not None
        assert record.task_id == "t1"
        assert record.status == "exhausted"
        assert record.next_steps == ["spray creds against ssh"]

    def test_credentials_round_trip_for_successor(self, monkeypatch, tmp_path):
        _install_sessions_dir(monkeypatch, tmp_path)
        lazy_continuation.save(
            "10.10.11.5",
            task_id="t1",
            status="exhausted",
            credentials=["admin:hunter2", "root:toor"],
        )
        record = lazy_continuation.load("10.10.11.5")
        assert record is not None
        assert record.credentials == ["admin:hunter2", "root:toor"]

    def test_handover_brief_renders_playbook(self, monkeypatch, tmp_path):
        _install_sessions_dir(monkeypatch, tmp_path)
        lazy_continuation.save(
            "10.10.11.5",
            task_id="t1",
            goal="pwn minio",
            status="exhausted",
            settlement="found minio creds",
            findings=["minio root creds dumped"],
            next_steps=["spray creds against ssh"],
            credentials=["admin:hunter2"],
        )
        brief = lazy_continuation.handover_brief("10.10.11.5")
        assert "# Handover for 10.10.11.5" in brief
        assert "pwn minio" in brief
        assert "spray creds against ssh" in brief
        assert "admin:hunter2" in brief

    def test_handover_brief_missing_target_is_empty(self, monkeypatch, tmp_path):
        _install_sessions_dir(monkeypatch, tmp_path)
        assert lazy_continuation.handover_brief("10.10.11.99") == ""

    def test_load_missing_target_is_none(self, monkeypatch, tmp_path):
        _install_sessions_dir(monkeypatch, tmp_path)
        assert lazy_continuation.load("10.10.11.10") is None

    def test_save_without_target_is_false(self, monkeypatch, tmp_path):
        _install_sessions_dir(monkeypatch, tmp_path)
        assert lazy_continuation.save("") is False

    def test_target_is_slug_sanitised(self, monkeypatch, tmp_path):
        _install_sessions_dir(monkeypatch, tmp_path)
        lazy_continuation.save("10.10.11.5/../../etc")
        record_file = tmp_path / "continuations" / "10.10.11.5_.._.._etc.json"
        assert record_file.is_file()


class TestRecall:
    """Recall turns open next steps into wake candidates."""

    def test_recall_returns_intent_with_reason(self, monkeypatch, tmp_path):
        _install_sessions_dir(monkeypatch, tmp_path)
        lazy_continuation.save(
            "10.10.11.5", task_id="t1", status="timeout", next_steps=["verify ssh spray"]
        )
        candidates = lazy_continuation.recall_candidates("10.10.11.5")
        assert candidates == [
            ("continuation: verify ssh spray", "prior task t1 (timeout) left this open")
        ]

    def test_recall_without_record_is_empty(self, monkeypatch, tmp_path):
        _install_sessions_dir(monkeypatch, tmp_path)
        assert lazy_continuation.recall_candidates("10.10.11.5") == []

    def test_recall_respects_limit(self, monkeypatch, tmp_path):
        _install_sessions_dir(monkeypatch, tmp_path)
        lazy_continuation.save(
            "10.10.11.5", task_id="t1", next_steps=["one", "two", "three", "four"]
        )
        assert len(lazy_continuation.recall_candidates("10.10.11.5", limit=2)) == 2


class TestPlannerWiring:
    """The planner consults the continuation record for the task target."""

    def test_continuation_marker_constant_exists(self):
        import modules.lazy_loop as lazy_loop

        assert lazy_loop.Planner._CONTINUATION_MARKER == "continuation: "

    def test_lazy_loop_writes_continuation_on_terminal_status(self):
        import inspect

        import modules.lazy_loop as lazy_loop

        source = inspect.getsource(lazy_loop.LazyLoopEngine._run_and_settle) if hasattr(
            lazy_loop.LazyLoopEngine, "_run_and_settle"
        ) else inspect.getsource(lazy_loop)
        assert "_write_continuation" in source
