"""Deviation ledger contract tests: record, dedupe, cap, render."""

from __future__ import annotations

import json

import pytest

from modules.lazy_deviations import (
    DEFAULT_LEDGER_PATH,
    DEVIATIONS_MAX_RECORDS,
    DeviationLedger,
)


@pytest.fixture()
def ledger(tmp_path) -> DeviationLedger:
    return DeviationLedger(tmp_path / "deviations.jsonl")


def test_default_path_points_into_sessions_lazy() -> None:
    assert DEFAULT_LEDGER_PATH.name == "deviations.jsonl"
    assert "sessions" in str(DEFAULT_LEDGER_PATH)


def test_record_requires_reason_and_change(ledger) -> None:
    assert ledger.record("loop:t0001", "lazynmap 1.2.3.4", "lazynmap 1.2.3.4", "") is None
    assert ledger.record("loop:t0001", "same", "same", "no change") is None
    row = ledger.record("loop:t0001", "nmap -p bad 1.2.3.4", "nmap 1.2.3.4", "dropped invalid port spec", "loop:sanitize")
    assert row is not None
    assert row.scope == "loop:t0001"
    assert row.source == "loop:sanitize"


def test_record_collapses_repeats(ledger) -> None:
    for _ in range(3):
        ledger.record("loop:t0001", "a", "b", "reason")
    rows = ledger.list()
    assert len(rows) == 1


def test_list_scopes_and_order(ledger) -> None:
    ledger.record("loop:t0001", "p1", "a1", "r1")
    ledger.record("loop:t0002", "p2", "a2", "r2")
    ledger.record("loop:t0001", "p3", "a3", "r3")
    only_first = ledger.list("loop:t0001")
    assert [row.planned for row in only_first] == ["p3", "p1"]
    everything = ledger.list()
    assert len(everything) == 3


def test_texts_cleaned_and_bounded(ledger) -> None:
    row = ledger.record("s", "x\n\ny\t z", "a", "  why   now  ")
    assert row.planned == "x y z"
    assert row.reason == "why now"
    long = ledger.record("s", "p" * 1000, "a", "r" * 1000)
    assert len(long.planned) == 400
    assert len(long.reason) == 400


def test_survives_broken_lines(ledger, tmp_path) -> None:
    path = tmp_path / "deviations.jsonl"
    path.write_text(
        json.dumps({"ts": 1.0, "scope": "s", "planned": "p", "actual": "a", "reason": "r", "source": "x"})
        + "\nnot json\n[[["
    )
    rows = DeviationLedger(path).list()
    assert len(rows) == 1
    assert rows[0].planned == "p"


def test_trim_caps_file(tmp_path) -> None:
    path = tmp_path / "deviations.jsonl"
    ledger = DeviationLedger(path)
    for index in range(DEVIATIONS_MAX_RECORDS + 30):
        ledger.record(f"s{index}", f"p{index}", f"a{index}", f"r{index}")
    rows = ledger.list(limit=DEVIATIONS_MAX_RECORDS + 5)
    assert len(rows) == DEVIATIONS_MAX_RECORDS
    assert rows[0].planned == f"p{DEVIATIONS_MAX_RECORDS + 29}"
    with open(path) as handle:
        assert len(handle.read().strip().splitlines()) == DEVIATIONS_MAX_RECORDS


def test_render_markdown_block(ledger) -> None:
    ledger.record("s", "nmap -p bad t", "nmap t", "dropped invalid port spec", "loop:sanitize")
    block = ledger.render_markdown(ledger.list())
    assert block.startswith("## Deviations")
    assert "- **Planned:** nmap -p bad t -> **Actual:** nmap t" in block
    assert "*Reason:* dropped invalid port spec" in block


def test_render_markdown_empty(ledger) -> None:
    assert ledger.render_markdown([]) == ""


def test_read_missing_file_is_empty(tmp_path) -> None:
    assert DeviationLedger(tmp_path / "absent.jsonl").list() == []


def test_worker_sanitize_records_deviation(tmp_path, monkeypatch) -> None:
    """The loop sanitizer must land repaired commands into the ledger."""
    ledger_path = tmp_path / "deviations.jsonl"
    monkeypatch.setattr("modules.lazy_loop.DeviationLedger", lambda: DeviationLedger(ledger_path))

    class FakeActivity:
        def __init__(self) -> None:
            self.rows = []

        def emit(self, *args, **kwargs) -> None:
            self.rows.append((args, kwargs))

    class FakeIntent:
        node_id = 7

    class FakeWorker:
        activity = FakeActivity()
        name = "worker-1"
        task_id = "t0001"

        @staticmethod
        def _target_for(intent: FakeIntent) -> str:
            return "1.2.3.4"

    from modules.lazy_loop import Worker

    worker = FakeWorker()
    result = Worker._sanitize_step(worker, FakeIntent(), "nmap -sV -p 172.17.0.2 1.2.3.4")
    assert result
    rows = DeviationLedger(ledger_path).list("loop:t0001")
    assert rows and rows[0].source == "loop:sanitize"
    assert "port spec" in rows[0].reason


def test_chain_replanner_deviations_recorded(tmp_path, monkeypatch) -> None:
    """Chain replanner effects land into the shared ledger."""
    from modules.chain_registry import Chain, ChainStep
    from modules.chain_runner import ChainRunner, ReplanContext

    ledger_path = tmp_path / "deviations.jsonl"
    monkeypatch.setattr("modules.chain_runner.DeviationLedger", lambda: DeviationLedger(ledger_path))

    class FakeReplanner:
        def __call__(self, context: ReplanContext) -> None:
            context.set_var("payload_path", "/tmp/p.sh")

    runner = object.__new__(ChainRunner)
    runner.replanner = FakeReplanner()
    runner.chain = Chain(name="probe", steps=[ChainStep(id="s1", run="echo hi")])
    runner.run_id = "run123"
    context = ReplanContext(chain_name="probe")
    FakeReplanner()(context)
    runner._record_replan_deviations(context)
    rows = DeviationLedger(ledger_path).list("chain:probe:run123")
    assert rows and rows[0].reason == "replanner rebound a variable"


def test_handover_brief_includes_deviations(tmp_path, monkeypatch) -> None:
    """The successor playbook carries the recorded deviations."""
    from modules import lazy_continuation

    monkeypatch.setattr(lazy_continuation, "DEFAULT_DIR", tmp_path)
    lazy_continuation.save(
        "1.2.3.4",
        task_id="t0001",
        goal="get flag",
        status="done",
        deviations=["nmap -p bad t -> nmap t (dropped invalid port spec)"],
    )
    brief = lazy_continuation.handover_brief("1.2.3.4")
    assert "deviations the plan took" in brief
    assert "dropped invalid port spec" in brief
