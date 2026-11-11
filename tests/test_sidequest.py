"""Tests for read-only side questions over immutable decision checkpoints.

The checkpoint ordinal must be content-derived and stable, so the same decision
always resolves to the same id regardless of its position in the ledger. Listing
and retrieval must read the real decision ledger, and asking must be read-only:
it reads a frozen checkpoint, queries the model and records the exchange in its
own isolated ledger without ever touching loop state.
"""

from __future__ import annotations

from modules import sidequest
from modules.loop import decision_log


def _seed_ledger(tmp_path, monkeypatch, rows):
    ledger = tmp_path / "decisions.jsonl"
    for row in rows:
        decision_log.record(decision_log.DecisionRecord(**row), path=ledger)
    monkeypatch.setattr(decision_log, "DECISIONS_FILE", ledger)
    return ledger


def _row(run_id="run_a", step=1, source="chain", chosen="apt_chain ms2 10.0.0.1"):
    return {
        "run_id": run_id,
        "step": step,
        "source": source,
        "model_fallback": source == "llm",
        "chosen": chosen,
        "reason": "service match",
        "ctx_digest": f"ctx{step}",
        "config_digest": "cfg",
    }


def test_checkpoint_id_is_stable_and_position_independent():
    row = _row()
    first = sidequest.checkpoint_id(row)
    assert first == sidequest.checkpoint_id(dict(row))
    assert len(first) == 16
    assert sidequest.checkpoint_id({}) == ""


def test_checkpoint_id_differs_per_decision():
    assert sidequest.checkpoint_id(_row(step=1)) != sidequest.checkpoint_id(_row(step=2))


def test_list_checkpoints(tmp_path, monkeypatch):
    _seed_ledger(tmp_path, monkeypatch, [_row(step=1), _row(step=2, source="llm")])
    rows = sidequest.list_checkpoints()
    assert len(rows) == 2
    assert rows[-1]["model_fallback"] is True
    assert all(r["checkpoint_id"] for r in rows)


def test_list_checkpoints_filters_run(tmp_path, monkeypatch):
    _seed_ledger(tmp_path, monkeypatch, [_row(run_id="run_a"), _row(run_id="run_b", step=9)])
    rows = sidequest.list_checkpoints(run_id="run_b")
    assert len(rows) == 1 and rows[0]["step"] == 9


def test_get_checkpoint_round_trip(tmp_path, monkeypatch):
    _seed_ledger(tmp_path, monkeypatch, [_row(step=1), _row(step=2)])
    listed = sidequest.list_checkpoints()
    ordinal = listed[0]["checkpoint_id"]
    row = sidequest.get_checkpoint(ordinal)
    assert row is not None and row["chosen"] == "apt_chain ms2 10.0.0.1"


def test_get_checkpoint_unknown(tmp_path, monkeypatch):
    _seed_ledger(tmp_path, monkeypatch, [_row()])
    assert sidequest.get_checkpoint("deadbeefdeadbeef") is None
    assert sidequest.get_checkpoint("") is None


def test_ask_empty_question(tmp_path, monkeypatch):
    _seed_ledger(tmp_path, monkeypatch, [_row()])
    assert sidequest.ask("whatever", "")["ok"] is False


def test_ask_unknown_checkpoint(tmp_path, monkeypatch):
    _seed_ledger(tmp_path, monkeypatch, [_row()])
    result = sidequest.ask("notreal", "why this?")
    assert result["ok"] is False and "unknown checkpoint" in result["error"]


def test_ask_is_read_only_and_records(tmp_path, monkeypatch):
    _seed_ledger(tmp_path, monkeypatch, [_row()])
    monkeypatch.setattr(sidequest, "_SIDEQUEST_FILE", tmp_path / "sidequests.jsonl")
    monkeypatch.setattr("modules.llm_factory.complete", lambda *a, **k: "the selector matched the http service")

    ledger_before = (tmp_path / "decisions.jsonl").read_text()
    ordinal = sidequest.list_checkpoints()[0]["checkpoint_id"]
    result = sidequest.ask(ordinal, "why was this chosen?")

    assert result["ok"] is True
    assert "selector" in result["answer"]
    assert (tmp_path / "decisions.jsonl").read_text() == ledger_before
    assert (tmp_path / "sidequests.jsonl").exists()


def test_ask_handles_model_failure(tmp_path, monkeypatch):
    _seed_ledger(tmp_path, monkeypatch, [_row()])

    def _boom(*a, **k):
        raise RuntimeError("no backend")

    monkeypatch.setattr("modules.llm_factory.complete", _boom)
    ordinal = sidequest.list_checkpoints()[0]["checkpoint_id"]
    result = sidequest.ask(ordinal, "why?")
    assert result["ok"] is False and "model unavailable" in result["error"]
