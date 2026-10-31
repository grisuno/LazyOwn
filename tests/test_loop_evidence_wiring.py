"""BDD tests for the loop evidence loop-closure wiring.

Covers the shell-proof publication (the wire that finally lets the loop
advance the kill-chain phase so the strategic selectors — atomic and apt
chain — become reachable), the worker trace ledger consumed by ``traces``,
traffic digest rebinding and the dual evidence hash.
"""

from __future__ import annotations

import json
from pathlib import Path
from types import SimpleNamespace

import pytest

SHELLY_OUTPUT = """whoami: root
Linux target 6.8.0 #1 SMP
@click_here: linux-shell-ok$

---captured---
uid=0(root) gid=0(root) groups=0(root)
"""


@pytest.fixture()
def sink_log():
    """Reset the process-wide bus and capture published events."""
    from modules import outcome_bus

    outcome_bus.reset_bus()
    published: list = []

    def fake_record(**kwargs):
        from modules.outcome_bus import OutcomeEvent

        published.append(OutcomeEvent(**kwargs))
        return {"event_bus": True}

    original = outcome_bus.record_event
    outcome_bus.record_event = fake_record
    try:
        yield published
    finally:
        outcome_bus.record_event = original
        outcome_bus.reset_bus()


def _worker(task_id: str = "t-test2"):
    """Minimal worker with only the fields the helper touches."""
    from modules.lazy_loop import Worker

    return Worker("worker-wire", task_id, None, None, None, None, None, None, shell=None)


def _intent(node_id: int = 3):
    """ExploreLike node stub."""
    return SimpleNamespace(node_id=node_id)


class TestShellProofPublication:
    def test_publishes_exploit_event_with_shell_flag(self, sink_log):
        story = "genuine shell evidence in a step output publishes one exploit outcome"
        worker = _worker("t-wire-shell")
        result = worker._publish_shell_proof(_intent(), "10.66.44.7", "whoami", SHELLY_OUTPUT)
        assert result is True, story
        event = sink_log[-1]
        assert event.kind == "exploit" and event.shell and event.success, story
        assert event.target == "10.66.44.7" and event.task_id == "t-wire-shell", story

    def test_junk_output_never_publishes(self, sink_log):
        story = "prompt-ish noise is never shell proof"
        worker = _worker("t-wire-noise")
        assert worker._publish_shell_proof(_intent(), "10.66.44.7", "curl -I http://x", "# \n$ \n") is False, story
        assert sink_log == [], story

    def test_no_target_no_event(self, sink_log):
        story = "without a target the helper abstains"
        worker = _worker("t-wire-not")
        assert worker._publish_shell_proof(_intent(), "", "whoami", SHELLY_OUTPUT) is False, story


class TestWorkerTraces:
    def test_rows_written_reader_schema(self, tmp_path: Path):
        story = "the trace ledger uses the keys the traces reader surfaces"
        from modules.lazy_loop import record_worker_traces

        path = tmp_path / "worker_traces.jsonl"
        record_worker_traces(
            task_id="t-1",
            worker="worker-a",
            intent_id=9,
            transcripts=[("lazynmap 10.66.44.7", SHELLY_OUTPUT)],
            state="done",
            path=path,
        )
        row = json.loads(path.read_text(encoding="utf-8").splitlines()[-1])
        for key in ("cmd", "via", "evidence", "traffic", "goals", "blocked", "task_id", "intent_id"):
            assert key in row, story
        assert row["cmd"] == "lazynmap 10.66.44.7", story
        assert row["evidence"] and row["traffic"], story

    def test_rotation_keeps_tail(self, tmp_path: Path):
        story = "an oversized ledger keeps its newest lines after rotation"
        import modules.lazy_loop as loop
        from modules.lazy_loop import record_worker_traces

        path = tmp_path / "worker_traces.jsonl"
        path.write_text("\n".join(f'{{"cmd":"old-{i}"}}' for i in range(5)) + "\n", encoding="utf-8")
        original = loop.WORKER_TRACES_MAX_BYTES
        loop.WORKER_TRACES_MAX_BYTES = 10
        try:
            record_worker_traces("t-2", "w", 1, [("cmd2", "output")], path=path)
            assert path.stat().st_size < original + 4096, story
            tail = json.loads(path.read_text(encoding="utf-8").splitlines()[-1])
            assert tail["cmd"] == "cmd2", story
        finally:
            loop.WORKER_TRACES_MAX_BYTES = original

    def test_empty_transcripts_write_nothing(self, tmp_path: Path):
        story = "no output means no trace rows"
        from modules.lazy_loop import record_worker_traces

        path = tmp_path / "worker_traces.jsonl"
        record_worker_traces("t-3", "w", 1, [("", "")], path=path)
        assert not path.exists(), story
        record_worker_traces("t-3", "w", 1, [], path=path)
        assert not path.exists(), story


class TestTrafficDigest:
    def test_same_output_same_digest_other_output_differs(self):
        story = "digest binds command to its output"
        from modules.lazy_loop import TrafficLog

        one = TrafficLog.digest_of("whoami", "root")
        two = TrafficLog.digest_of("whoami", "root")
        three = TrafficLog.digest_of("whoami", "root2")
        assert one == two and one != three, story


class TestEvidenceDualHash:
    def test_full_body_hash_and_stored_hash(self, tmp_path: Path):
        story = "evidence carries the full source digest plus the stored copy digest"
        import modules.lazy_loop as loop

        store = loop.EvidenceStore.__new__(loop.EvidenceStore)
        store.task_id = "t-ev"
        store._path = tmp_path / "evidence.json"
        big = "x" * 8000
        item = store.add(4, "note", big)
        assert len(item["sha256"]) == 64 and len(item["sha256_stored"]) == 64, story
        assert item["sha256"] != item["sha256_stored"], story
        assert store.verify() == [], story

    def test_tamper_detected(self, tmp_path: Path):
        story = "an edited stored copy verifies as bad"
        import modules.lazy_loop as loop

        store = loop.EvidenceStore.__new__(loop.EvidenceStore)
        store.task_id = "t-ev2"
        store._path = tmp_path / "evidence.json"
        store.add(2, "note", "line1")
        data = json.loads(store._path.read_text(encoding="utf-8"))
        data["items"][0]["body"] = "tampered"
        store._path.write_text(json.dumps(data), encoding="utf-8")
        assert store.verify() == [1], story


class TestContracts:
    def test_wiring_sources(self):
        story = "the round loop closes every previously documented gap"
        lazy = (Path(__file__).resolve().parent.parent / "modules" / "lazy_loop.py").read_text(encoding="utf-8")
        daemon = (Path(__file__).resolve().parent.parent / "skills" / "autonomous_daemon.py").read_text(encoding="utf-8")
        assert "_publish_shell_proof" in lazy, story
        assert "record_worker_traces" in lazy, story
        assert "digest_of" in lazy, story
        assert "progress config unavailable" in lazy, story
        assert "save_payload as _save_payload" in daemon, story
        assert "PAYLOAD_FILE.write_text" not in daemon, story
