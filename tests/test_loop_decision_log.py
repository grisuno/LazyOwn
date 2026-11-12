"""Tests for the reproducible loop decision ledger and planner determinism.

Covers the three contracts that make up the determinism increment: the
digest helpers that fingerprint a decision's inputs, the bounded JSONL ledger
that records and replays decisions, the JSON-first planner output parser, and
the greedy default temperature that pins the planner. The ledger is exercised
against a temporary path so no test touches the shared ``sessions/`` file.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from modules.loop import decision_log
from modules.loop.worker_agentic import _extract_llm_commands, _planner_temperature


class _Ctx:
    """Minimal SelectionContext-shaped stand-in for digest tests."""

    def __init__(self, extra=None, services=("http", "smb")):
        self.target = "10.10.10.5"
        self.phase = "recon"
        self.os_hint = "linux"
        self.services = services
        self.has_creds = False
        self.exclude = frozenset()
        self.extra = extra if extra is not None else {"goal": "root", "n": 1}


def test_digest_is_stable_and_bounded():
    first = decision_log.digest("nmap -sV 10.0.0.1")
    assert first == decision_log.digest("nmap -sV 10.0.0.1")
    assert len(first) == 16
    assert decision_log.digest("") == ""


def test_context_digest_ignores_mapping_order():
    left = _Ctx(extra={"goal": "root", "n": 1})
    right = _Ctx(extra={"n": 1, "goal": "root"})
    assert decision_log.context_digest(left) == decision_log.context_digest(right)


def test_context_digest_ignores_service_order():
    assert decision_log.context_digest(_Ctx(services=("http", "smb"))) == decision_log.context_digest(
        _Ctx(services=("smb", "http"))
    )


def test_context_digest_changes_with_state():
    base = decision_log.context_digest(_Ctx())
    moved = _Ctx()
    moved.phase = "exploit"
    assert decision_log.context_digest(moved) != base


def test_config_digest_only_tracks_relevant_keys():
    base = {"loop_planner_temperature": "0.0", "llm_backend": "groq", "rhost": "1.1.1.1"}
    churn = dict(base, rhost="2.2.2.2", unrelated="x")
    assert decision_log.config_digest(base) == decision_log.config_digest(churn)
    changed = dict(base, loop_planner_temperature="0.7")
    assert decision_log.config_digest(changed) != decision_log.config_digest(base)


def test_config_digest_empty_inputs():
    assert decision_log.config_digest(None) == ""
    assert decision_log.config_digest({}) == ""
    assert decision_log.config_digest({"rhost": "1.1.1.1"}) == ""


def test_config_digest_tracks_determinism_flags():
    base = {"loop_deterministic": False, "loop_guard_rules": ""}
    assert decision_log.config_digest(dict(base, loop_deterministic=True)) != decision_log.config_digest(base)
    assert decision_log.config_digest(dict(base, loop_guard_rules="rm")) != decision_log.config_digest(base)
    assert decision_log.config_digest(dict(base, loop_wire_capture=False)) != decision_log.config_digest(base)


def test_record_and_read_round_trip(tmp_path: Path):
    ledger = tmp_path / "decisions.jsonl"
    rec = decision_log.DecisionRecord(
        run_id="run_abc",
        step=3,
        source="chain",
        model_fallback=False,
        chosen="apt_chain ms2_web 10.10.10.5",
        reason="service match",
        ctx_digest="deadbeefdeadbeef",
        config_digest="cafecafecafecafe",
        candidates=("apt_chain ms2_web 10.10.10.5",),
    )
    assert decision_log.record(rec, path=ledger) is True
    rows = decision_log.read_records(path=ledger)
    assert len(rows) == 1
    assert rows[0]["source"] == "chain"
    assert rows[0]["model_fallback"] is False
    assert rows[0]["chosen"].startswith("apt_chain")


def test_read_records_skips_corrupt_lines(tmp_path: Path):
    ledger = tmp_path / "decisions.jsonl"
    ledger.write_text('{"run_id":"r","step":1,"source":"llm"}\nnot-json\n{"step":2}\n', encoding="utf-8")
    rows = decision_log.read_records(path=ledger)
    assert [row.get("step") for row in rows] == [1, 2]


def test_record_marks_model_fallback_for_llm(tmp_path: Path):
    ledger = tmp_path / "decisions.jsonl"
    rec = decision_log.DecisionRecord(
        run_id="run_x",
        step=7,
        source="llm",
        model_fallback=True,
        chosen="id",
        prompt_digest="1111111111111111",
        reply_digest="2222222222222222",
        candidates=("id", "sudo su"),
        filtered=decision_log.filtered_rows([("sudo su", "sudo-no-tty")]),
    )
    decision_log.record(rec, path=ledger)
    row = decision_log.read_records(path=ledger)[0]
    assert row["model_fallback"] is True
    assert row["filtered"] == [{"command": "sudo su", "reason": "sudo-no-tty"}]


def test_record_never_raises_on_bad_path(tmp_path: Path):
    blocker = tmp_path / "blocker"
    blocker.write_text("x", encoding="utf-8")
    rec = decision_log.DecisionRecord(run_id="r", step=0, source="llm")
    assert decision_log.record(rec, path=blocker / "nested" / "decisions.jsonl") is False


def test_filtered_rows_bounds_and_shape():
    rows = decision_log.filtered_rows([("c" * 400, "r" * 400)])
    assert len(rows[0]["command"]) == 300
    assert len(rows[0]["reason"]) == 160


def test_extract_json_contract():
    reply = '[{"command": "nmap -sV 10.0.0.1", "reason": "scan"}, {"command": "id"}]'
    assert _extract_llm_commands(reply) == ["nmap -sV 10.0.0.1", "id"]


def test_extract_json_fenced_block():
    reply = '```json\n[{"command": "whoami"}]\n```'
    assert _extract_llm_commands(reply) == ["whoami"]


def test_extract_json_string_array():
    assert _extract_llm_commands('["ls -la", "pwd"]') == ["ls -la", "pwd"]


def test_extract_line_fallback_on_non_json():
    reply = "nmap -sV x\n2. id\n`ls`\n# comment stays a candidate"
    out = _extract_llm_commands(reply)
    assert "nmap -sV x" in out
    assert "id" in out
    assert "ls" in out


def test_extract_dedupes_preserving_order():
    assert _extract_llm_commands('["id", "id", "whoami"]') == ["id", "whoami"]


def test_extract_empty_reply():
    assert _extract_llm_commands("") == []
    assert _extract_llm_commands("   ") == []


def test_planner_temperature_default_is_greedy(monkeypatch):
    import modules.lazy_loop as loop

    monkeypatch.setattr(loop, "load_payload", lambda: {}, raising=False)
    assert loop.planner_temperature() == 0.0
    assert _planner_temperature() == 0.0


def test_planner_temperature_reads_payload(monkeypatch):
    import core.config as config

    monkeypatch.setattr(config, "load_payload", lambda: {"loop_planner_temperature": "0.4"})
    import modules.lazy_loop as loop

    assert loop.planner_temperature() == pytest.approx(0.4)


def test_planner_temperature_clamps_negative(monkeypatch):
    import core.config as config

    monkeypatch.setattr(config, "load_payload", lambda: {"loop_planner_temperature": "-3"})
    import modules.lazy_loop as loop

    assert loop.planner_temperature() == 0.0


def test_planner_temperature_survives_malformed(monkeypatch):
    import core.config as config

    monkeypatch.setattr(config, "load_payload", lambda: {"loop_planner_temperature": "hot"})
    import modules.lazy_loop as loop

    assert loop.planner_temperature() == 0.0
