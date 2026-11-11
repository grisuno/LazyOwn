"""Blindspot review contract tests: parse, fence, apply and loop gating."""

from __future__ import annotations

import json

from modules.lazy_blindspot import (
    BLINDSPOT_MAX_FINDINGS,
    BlindspotFinding,
    BlindspotReview,
    build_blindspot_prompt,
    parse_blindspots,
)


def _payload(spots: list[dict]) -> str:
    return json.dumps({"accepted": True, "data": {"blindspots": spots}})


def test_parse_fenced_json() -> None:
    raw = "here you go:\n```json\n" + _payload([{"area": "smb", "risk": "high", "question": "can we relay?", "suggestion": "coerce"}]) + "\n```"
    findings = parse_blindspots(raw)
    assert len(findings) == 1
    assert findings[0].area == "smb"
    assert findings[0].risk == "high"


def test_parse_bare_json_and_defaults() -> None:
    raw = _payload([{"question": "is anonftp writable?"}])
    findings = parse_blindspots(raw)
    assert findings[0].area == "unknown"
    assert findings[0].risk == "medium"
    assert findings[0].suggestion == ""


def test_parse_drops_invalid_entries() -> None:
    raw = _payload([{"area": "a"}, {"question": "q1"}, "junk", {"risk": "high", "question": "  "}])
    findings = parse_blindspots(raw)
    assert [f.question for f in findings] == ["q1"]


def test_parse_accepted_false_yields_none() -> None:
    assert parse_blindspots(json.dumps({"accepted": False, "reason": "no"})) == []


def test_parse_garbage_yields_empty() -> None:
    assert parse_blindspots("not json at all") == []
    assert parse_blindspots("") == []


def test_parse_risk_normalized_and_capped() -> None:
    spots = [{"area": f"a{i}", "risk": "extreme", "question": f"q{i}"} for i in range(BLINDSPOT_MAX_FINDINGS + 3)]
    findings = parse_blindspots(_payload(spots))
    assert len(findings) == BLINDSPOT_MAX_FINDINGS
    assert all(f.risk == "medium" for f in findings)


def test_hint_rendering_with_and_without_suggestion() -> None:
    finding = BlindspotFinding(area="creds", risk="high", question="sprayed yet?", suggestion="try lazycreds")
    assert finding.as_hint() == "[blindspot/high] creds: sprayed yet? - suggestion: try lazycreds"
    plain = BlindspotFinding(area="creds", risk="low", question="sprayed yet?")
    assert plain.as_hint() == "[blindspot/low] creds: sprayed yet?"


def test_prompt_fences_untrusted_blocks() -> None:
    prompt = build_blindspot_prompt("goal ``` evil", "context\n```json\n{}")
    assert "UNTRUSTED DATA" in prompt
    assert prompt.count("```") == 4
    assert "```json" not in prompt
    assert "```\\ " not in prompt


def test_review_applies_findings_as_hints() -> None:
    reply = _payload([{"area": "smb", "risk": "high", "question": "relay?"}])
    hints: list[str] = []
    review = BlindspotReview(lambda prompt, max_tokens: reply, hints.append)
    applied = review.run("get flag", "graph context")
    assert len(applied) == 1
    assert hints == ["[blindspot/high] smb: relay?"]


def test_review_unavailable_or_garbage_is_silent() -> None:
    hints: list[str] = []
    review = BlindspotReview(lambda prompt, max_tokens: "no json", hints.append)
    assert review.run("g", "c") == []
    assert hints == []
    silent = BlindspotReview(None, hints.append)
    assert silent.run("g", "c") == []


def test_review_pool_exception_is_silent() -> None:
    def boom(prompt: str, max_tokens: int) -> str:
        raise RuntimeError("down")

    review = BlindspotReview(boom, lambda text: None)
    assert review.run("g", "c") == []


def test_apply_raising_sink_keeps_finding_out() -> None:
    findings = [BlindspotFinding(area="a", risk="high", question="q")]

    def raising_sink(text: str) -> None:
        raise RuntimeError("storage down")

    review = BlindspotReview(None, raising_sink)
    assert review.apply(findings) == []


def test_apply_none_sink_stops_cleanly() -> None:
    findings = [BlindspotFinding(area="a", risk="high", question="q")]
    review = BlindspotReview(None, None)
    assert review.apply(findings) == []


def test_engine_blindspot_review_disabled_by_default(tmp_path, monkeypatch) -> None:
    """Loop engine must not carry the review unless the payload flag is on."""
    monkeypatch.setattr("core.config.load_payload", lambda: {"loop_blindspot_enabled": False}, raising=False)
    from modules.lazy_loop import LazyLoopEngine

    engine = LazyLoopEngine()
    assert engine.blindspot_enabled is False
    assert engine._blindspot_last_round == {}


def test_engine_blindspot_enabled_reads_payload(tmp_path, monkeypatch) -> None:
    monkeypatch.setattr("core.config.load_payload", lambda: {"loop_blindspot_enabled": True}, raising=False)
    from modules.lazy_loop import LazyLoopEngine

    engine = LazyLoopEngine()
    assert engine.blindspot_enabled is True


def test_maybe_blindspot_requires_flag_and_quiet_planner() -> None:
    from modules.lazy_loop import BLINDSPOT_ROUND_INTERVAL, LazyLoopEngine

    engine = LazyLoopEngine()
    engine.blindspot_enabled = False
    calls: list[str] = []

    def fake_review(task_id: str) -> dict:
        calls.append(task_id)
        return {"findings": [], "summary": ""}

    engine.blindspot_review = fake_review
    engine._maybe_blindspot("t0001", None, lambda name: True, new_intents=3)
    engine._maybe_blindspot("t0001", None, lambda name: True, new_intents=0)
    assert calls == []

    engine.blindspot_enabled = True
    engine.budget = type("B", (), {"usage": staticmethod(lambda task_id: {"rounds": 5})})()
    engine._maybe_blindspot("t0001", None, lambda name: True, new_intents=0)
    assert calls == ["t0001"]
    engine._maybe_blindspot("t0001", None, lambda name: True, new_intents=0)
    assert calls == ["t0001"]
    engine._blindspot_last_round["t0001"] = 5 - BLINDSPOT_ROUND_INTERVAL
    engine._maybe_blindspot("t0001", None, lambda name: True, new_intents=0)
    assert calls == ["t0001", "t0001"]


def test_maybe_blindspot_respects_stage_toggle() -> None:
    from modules.lazy_loop import LazyLoopEngine

    engine = LazyLoopEngine()
    engine.blindspot_enabled = True
    calls: list[str] = []
    engine.blindspot_review = lambda task_id: calls.append(task_id) or {"findings": []}
    engine.budget = type("B", (), {"usage": staticmethod(lambda task_id: {"rounds": 99})})()
    engine._maybe_blindspot("t0001", None, lambda name: False, new_intents=0)
    assert calls == []
