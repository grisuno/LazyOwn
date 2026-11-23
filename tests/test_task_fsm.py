"""FSM contract for loop task statuses.

SDD/BDD: ``TaskStore.set_status`` must reject every transition outside
the observed engine table (active->anything, terminal->revive/idempotent)
while keeping the convenience verbs (pause/resume/enqueue) graceful and
``dequeue_next`` FIFO-faithful.
"""

from __future__ import annotations

import pytest


@pytest.fixture()
def store(tmp_path, monkeypatch):
    import modules.lazy_loop as loop

    monkeypatch.setattr(loop, "STORE_DIR", tmp_path)
    monkeypatch.setattr(loop, "SESSIONS_DIR", tmp_path)
    monkeypatch.setattr(loop, "_store_path", lambda name: tmp_path / name)
    return loop.TaskStore()


class TestVocabulary:
    def test_vocab_split_is_exhaustive(self) -> None:
        from modules.loop import task_fsm

        assert set(task_fsm.ACTIVE_STATUSES) | set(task_fsm.TERMINAL_STATUSES) == {
            "queued", "running", "paused", "done", "failed", "timeout", "exhausted", "handoff",
        }
        assert not set(task_fsm.ACTIVE_STATUSES) & set(task_fsm.TERMINAL_STATUSES)

    def test_valid_membership(self) -> None:
        from modules.loop import task_fsm

        assert task_fsm.is_valid_status("running")
        assert task_fsm.is_valid_status("handoff")
        assert not task_fsm.is_valid_status("zombie")

    def test_unknown_current_raises(self) -> None:
        from modules.loop import task_fsm

        with pytest.raises(ValueError):
            task_fsm.allowed_transitions("zombie")

    def test_allowed_transitions_shapes(self) -> None:
        from modules.loop import task_fsm

        assert task_fsm.allowed_transitions("running") >= {"queued", "paused", "done", "exhausted"}
        assert task_fsm.allowed_transitions("done") == {"running", "queued", "done"}
        assert task_fsm.allowed_transitions("exhausted") == {"running", "queued", "exhausted"}


class TestActiveTransitions:
    def test_create_defaults_running(self, store) -> None:
        task = store.create("demo")
        assert task.status == "running"
        assert store.get(task.task_id)["status"] == "running"

    def test_pause_resume_roundtrip(self, store) -> None:
        tid = store.create("demo").task_id
        assert store.pause(tid) is True
        assert store.get(tid)["status"] == "paused"
        assert store.resume(tid) is True
        assert store.get(tid)["status"] == "running"

    def test_enqueue_then_dequeue_fifo(self, store) -> None:
        for goal in ("first", "second"):
            store.enqueue(store.create(goal).task_id)
        assert store.dequeue_next()["goal"] == "first"
        assert store.dequeue_next()["goal"] == "second"
        assert store.dequeue_next() is None

    def test_running_to_queued_allowed_active_mesh(self, store) -> None:
        tid = store.create("demo").task_id
        assert store.set_status(tid, "queued") is True
        assert store.get(tid)["status"] == "queued"

    def test_enqueue_from_running_ok(self, store) -> None:
        tid = store.create("demo").task_id
        assert store.enqueue(tid) is True
        assert store.get(tid)["status"] == "queued"
        assert store.get(tid).get("queued_at")


class TestTerminalTransitions:
    def test_active_to_terminal_allowed(self, store) -> None:
        for terminal in ("done", "failed", "timeout", "exhausted", "handoff"):
            tid = store.create(f"t-{terminal}").task_id
            assert store.set_status(tid, terminal) is True

    def test_terminal_to_terminal_blocked(self, store) -> None:
        from modules.loop.task_fsm import InvalidTaskTransition

        tid = store.create("demo").task_id
        store.set_status(tid, "exhausted")
        with pytest.raises(InvalidTaskTransition):
            store.set_status(tid, "done")
        assert store.get(tid)["status"] == "exhausted"

    def test_terminal_revive_to_running(self, store) -> None:
        for terminal in ("done", "failed", "timeout", "exhausted", "handoff"):
            tid = store.create(f"r-{terminal}").task_id
            store.set_status(tid, terminal)
            assert store.set_status(tid, "running") is True
            assert store.get(tid)["status"] == "running"

    def test_resume_idempotent_on_done(self, store) -> None:
        tid = store.create("demo").task_id
        store.set_status(tid, "done")
        assert store.resume(tid) is True
        assert store.get(tid)["status"] == "done"

    def test_terminal_revive_to_queued(self, store) -> None:
        tid = store.create("demo").task_id
        store.set_status(tid, "done")
        assert store.enqueue(tid) is True
        assert store.get(tid)["status"] == "queued"

    def test_pause_on_terminal_is_graceful_false(self, store) -> None:
        tid = store.create("demo").task_id
        store.set_status(tid, "done")
        assert store.pause(tid) is False
        assert store.get(tid)["status"] == "done"

    def test_same_state_terminal_write_idempotent(self, store) -> None:
        tid = store.create("demo").task_id
        store.set_status(tid, "done")
        assert store.set_status(tid, "done") is True
        assert store.get(tid)["status"] == "done"

    def test_unknown_status_still_valueerror(self, store) -> None:
        tid = store.create("demo").task_id
        with pytest.raises(ValueError):
            store.set_status(tid, "zombie")

    def test_unknown_task_returns_false(self, store) -> None:
        assert store.set_status("t9999", "done") is False
