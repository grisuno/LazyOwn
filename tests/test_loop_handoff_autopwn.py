"""Terminal auto_pwn must fire when the LLM strikes out on the objective.

The engagement decision returns ``handoff`` after the strike cap (the LLM made
no objective progress). Before drafting an operator handoff, the run loop runs
the deterministic ``auto_pwn`` fallback once: the loop's purpose is to win a
foothold, so a strikeout is exactly when the goal-independent exploit engine
should take over. Only when auto_pwn also fails to land a shell does the loop
hand off. ``save_tokens`` mode still skips the heavy fallback.
"""

from __future__ import annotations

import pytest

import modules.lazy_loop as loop


@pytest.fixture()
def engine(tmp_path, monkeypatch):
    """Engine with stores under tmp_path and an isolated token ledger."""
    from modules.lazy_engine import LazyEngine
    from modules.loop import state_db, tokens

    monkeypatch.setattr(loop, "STORE_DIR", tmp_path)
    monkeypatch.setattr(loop, "SESSIONS_DIR", tmp_path)
    monkeypatch.setattr(loop, "_store_path", lambda name: tmp_path / name)
    monkeypatch.setattr(state_db, "default_db_path", lambda: tmp_path / "loop_state.db")
    monkeypatch.setattr(tokens, "shared_ledger", lambda: tokens.TokenLedger(db_path=str(tmp_path / "tokens.db")))
    loop._TOKEN_POLICY = None
    engine = LazyEngine()
    yield engine
    loop._TOKEN_POLICY = None


def _strike_out(engine, monkeypatch):
    """Force every round to return the ``handoff`` engagement decision."""
    monkeypatch.setattr(engine, "_engagement_decision", lambda *a, **k: "handoff")


def test_handoff_runs_autopwn_fallback_and_marks_done(engine, monkeypatch):
    task_id = engine.create_task("gain initial access on 127.0.0.1")["task_id"]
    _strike_out(engine, monkeypatch)
    calls = []

    def _fallback(tid, executor, activity):
        calls.append(tid)
        return True

    monkeypatch.setattr(engine, "_terminal_autopwn_fallback", _fallback)
    result = engine.run(task_id, max_rounds=3, workers=1, executor=lambda command: "")
    record = engine.store.get(task_id)
    assert calls == [task_id]
    assert record["status"] == "done"
    assert result["status"] == "done"
    assert record["runtime"]["abort_cause"] == "autopwn_fallback"


def test_handoff_without_shell_still_hands_off(engine, monkeypatch):
    task_id = engine.create_task("gain initial access on 127.0.0.1")["task_id"]
    _strike_out(engine, monkeypatch)
    monkeypatch.setattr(engine, "_terminal_autopwn_fallback", lambda *a, **k: False)
    engine.run(task_id, max_rounds=3, workers=1, executor=lambda command: "")
    record = engine.store.get(task_id)
    assert record["status"] == "handoff"
    assert record["runtime"]["abort_cause"] == "handoff"


def test_handoff_in_save_tokens_mode_skips_autopwn(engine, monkeypatch):
    task_id = engine.create_task("gain initial access on 127.0.0.1")["task_id"]
    _strike_out(engine, monkeypatch)
    monkeypatch.setattr(engine, "_save_tokens_mode", lambda *a, **k: True)
    called = []
    monkeypatch.setattr(engine, "_terminal_autopwn_fallback", lambda *a, **k: called.append(1) or True)
    engine.run(task_id, max_rounds=3, workers=1, executor=lambda command: "")
    record = engine.store.get(task_id)
    assert called == []
    assert record["status"] == "handoff"
