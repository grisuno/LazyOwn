"""Termination mode tests: save_tokens wraps up cleanly, try_hard degrades only."""

from __future__ import annotations

import pytest

import modules.lazy_loop as loop


@pytest.fixture()
def engine(tmp_path, monkeypatch):
    """Engine with stores under tmp_path and isolated token ledger."""
    from modules.lazy_engine import LazyEngine
    from modules.loop import state_db, tokens

    monkeypatch.setattr(loop, "STORE_DIR", tmp_path)
    monkeypatch.setattr(loop, "SESSIONS_DIR", tmp_path)
    monkeypatch.setattr(loop, "_store_path", lambda name: tmp_path / name)
    monkeypatch.setattr(state_db, "default_db_path", lambda: tmp_path / "loop_state.db")
    monkeypatch.setattr(tokens, "shared_ledger", lambda: tokens.TokenLedger(db_path=str(tmp_path / "tokens.db")))
    loop._TOKEN_POLICY = None
    token_ledger = tokens.TokenLedger(db_path=str(tmp_path / "tokens.db"))

    def _guard(task_id, intent_id=0):
        return loop.TerminationPolicy(mode="save_tokens", max_tokens_per_task=1000, wrapup_reserve_tokens=100).guard(
            task_id, token_ledger, intent_id=intent_id
        )

    monkeypatch.setattr(loop, "token_guard", _guard)
    engine = LazyEngine()
    yield engine, token_ledger
    loop._TOKEN_POLICY = None


def test_save_tokens_skips_terminal_autopwn(engine):
    engine, ledger = engine
    task_id = engine.create_task("gain initial access on 127.0.0.1")["task_id"]
    ledger.charge(task_id, 1000, 0)
    assert engine._save_tokens_mode(task_id) is True


def test_save_tokens_run_wraps_up_without_autopwn(engine, monkeypatch):
    engine, ledger = engine
    task_id = engine.create_task("gain initial access on 127.0.0.1")["task_id"]
    ledger.charge(task_id, 1000, 0)
    monkeypatch.setattr(engine, "_terminal_autopwn_fallback", lambda *a, **k: True)
    result = engine.run(task_id, max_rounds=2, workers=1, executor=lambda command: "")
    record = engine.store.get(task_id)
    assert result["status"] in ("exhausted", "timeout", "done")
    assert record["runtime"]["abort_cause"] == "token_budget"
    assert record["status"] != "done"


def test_try_hard_continues_running(engine, monkeypatch):
    engine, ledger = engine
    task_id = engine.create_task("gain initial access on 127.0.0.1")["task_id"]

    def _guard(task_id, intent_id=0):
        return {
            "ok": False,
            "reason": "token budget 500/500",
            "action": "deterministic_only",
            "used": {},
            "limits": {},
        }

    monkeypatch.setattr(loop, "token_guard", _guard)
    monkeypatch.setattr(engine, "_terminal_autopwn_fallback", lambda *a, **k: True)
    result = engine.run(task_id, max_rounds=1, workers=1, executor=lambda command: "")
    record = engine.store.get(task_id)
    assert record["runtime"]["abort_cause"] != "token_budget"
    assert result["status"] in ("exhausted", "done", "timeout")
