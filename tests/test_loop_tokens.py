"""Tests for modules.loop.tokens and the llm_pool usage sink."""

from __future__ import annotations

import pytest

from modules.loop import tokens as tok
from modules.loop.tokens import TerminationPolicy, TokenLedger, estimate_tokens


@pytest.fixture()
def ledger(tmp_path):
    """Token ledger on a throwaway database."""
    return TokenLedger(db_path=str(tmp_path / "tokens.db"))


def test_estimate_tokens_floor():
    assert estimate_tokens(0) == 1
    assert estimate_tokens(400) == 100


def test_charge_and_usage(ledger):
    ledger.charge("t1", 100, 50)
    ledger.charge("t1", 10, 5, intent_id=7, member="m")
    usage = ledger.usage("t1")
    assert usage["prompt"] == 110
    assert usage["completion"] == 55
    assert usage["total"] == 165
    assert ledger.usage("t1", intent_id=7)["total"] == 15
    assert ledger.usage("unknown")["total"] == 0


def test_charge_chars_capped(ledger):
    ledger.charge_chars("m", 400, 80, task_id="t1")
    assert ledger.usage("t1") == {"prompt": 100, "completion": 20, "total": 120}
    ledger.charge_chars("m", 10 * tok.SINK_LIMIT_CHARS, 0, task_id="t1")
    assert ledger.usage("t1")["prompt"] == 100 + tok.SINK_LIMIT_CHARS // tok.CHARS_PER_TOKEN


def test_reset(ledger):
    ledger.charge("t1", 100, 50)
    assert ledger.reset("t1") == 1
    assert ledger.usage("t1")["total"] == 0


def test_policy_defaults_are_try_hard():
    policy = TerminationPolicy()
    assert policy.mode == "try_hard"
    assert policy.max_tokens_per_task > 0


def test_policy_save_tokens_wraps_up(ledger):
    policy = TerminationPolicy(mode="save_tokens", max_tokens_per_task=1000, wrapup_reserve_tokens=100)
    ledger.charge("t1", 900, 100)
    verdict = policy.guard("t1", ledger)
    assert verdict["ok"] is False
    assert verdict["action"] == "wrapup"


def test_policy_try_hard_degrades_only(ledger):
    policy = TerminationPolicy(mode="try_hard", max_tokens_per_task=1000, wrapup_reserve_tokens=100)
    ledger.charge("t1", 950, 50)
    verdict = policy.guard("t1", ledger)
    assert verdict["ok"] is False
    assert verdict["action"] == "deterministic_only"


def test_policy_under_budget_continues(ledger):
    policy = TerminationPolicy(mode="save_tokens", max_tokens_per_task=10000, wrapup_reserve_tokens=100)
    ledger.charge("t1", 100, 10)
    verdict = policy.guard("t1", ledger)
    assert verdict["ok"] is True
    assert verdict["action"] == "continue"


def test_policy_intent_cap_degrades_to_deterministic(ledger):
    policy = TerminationPolicy(mode="try_hard", max_tokens_per_task=100000, max_tokens_per_intent=100)
    ledger.charge("t1", 90, 20, intent_id=7)
    verdict = policy.guard("t1", ledger, intent_id=7)
    assert verdict["ok"] is False
    assert verdict["action"] == "deterministic_only"
    assert "intent" in verdict["reason"]


def test_wrapup_reserve_bounds():
    policy = TerminationPolicy(wrapup_reserve_pct=5.0, wrapup_reserve_tokens=20000)
    assert policy.wrapup_reserve(400000) == 20000
    assert policy.wrapup_reserve(100000) == 20000
    assert policy.wrapup_reserve(0) == 0


def test_invalid_mode_falls_back():
    policy = TerminationPolicy(mode="bogus")
    assert policy.mode == "try_hard"


def test_usage_sink_publishes(monkeypatch, tmp_path):
    events = []
    import modules.llm_pool as pool_module

    pool_module.register_usage_sink(lambda member, p, c: events.append((member, p, c)))
    class _Member:
        name = "mem"
        def complete(self, prompt, session_key=""):
            return "ok"
    member = _Member()
    pool_module._publish_usage(member.name, "abcd", "ef")
    assert events[-1] == ("mem", 4, 2)
