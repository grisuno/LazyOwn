"""Contract tests for the LLM budget cap.

The tests below pin the contract the spec declares. Every test
verifies a single behaviour the operator can read in plain English.
The tests start red until the implementation in
``core/llm_budget.py`` ships.
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path
from typing import Any

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
SKILLS_ROOT = REPO_ROOT / "skills"
if str(SKILLS_ROOT) not in sys.path:
    sys.path.insert(0, str(SKILLS_ROOT))
sys.path.insert(0, str(REPO_ROOT))
sys.path.insert(0, str(REPO_ROOT / "core"))
sys.path.insert(0, str(REPO_ROOT / "modules"))


@pytest.fixture()
def tmp_sessions(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """Redirect the session directory to a temporary path."""
    sessions = tmp_path / "sessions"
    sessions.mkdir(parents=True, exist_ok=True)
    monkeypatch.setenv("LAZYOWN_SESSIONS_DIR", str(sessions))
    return sessions


def test_budget_module_is_importable() -> None:
    """The budget module lives at core/llm_budget and exports the public surface."""
    from core import llm_budget  # noqa: F401

    assert hasattr(llm_budget, "BudgetConfig")
    assert hasattr(llm_budget, "BudgetLedger")
    assert hasattr(llm_budget, "TokenEstimator")
    assert hasattr(llm_budget, "BudgetGuard")
    assert hasattr(llm_budget, "BudgetExceeded")
    assert hasattr(llm_budget, "load_budget_config")
    assert hasattr(llm_budget, "read_budget_status")
    assert hasattr(llm_budget, "format_budget_status")
    assert hasattr(llm_budget, "wrap_backend_with_budget")
    assert hasattr(llm_budget, "TOKEN_BUDGET_FIELDS")


def test_budget_config_dataclass_carries_expected_fields() -> None:
    """The BudgetConfig dataclass carries every key the spec declares."""
    from core.llm_budget import BudgetConfig

    config = BudgetConfig(
        daily_budget_usd=2.5,
        per_call_token_cap=4096,
        reset_at_utc="00:00",
        model_prices={
            "llama-3.3-70b-versatile": {"input": 0.59, "output": 0.79},
        },
        enabled=True,
        ledger_path=Path("/tmp/test.json"),
    )
    assert config.daily_budget_usd == 2.5
    assert config.per_call_token_cap == 4096
    assert config.enabled is True
    assert "llama-3.3-70b-versatile" in config.model_prices


def test_token_estimator_counts_text_tokens() -> None:
    """The token estimator returns a positive integer for a non empty string."""
    from core.llm_budget import TokenEstimator

    estimator = TokenEstimator()
    count = estimator.count("hello world")
    assert isinstance(count, int)
    assert count > 0


def test_token_estimator_handles_empty_string() -> None:
    """The token estimator returns zero for the empty string."""
    from core.llm_budget import TokenEstimator

    estimator = TokenEstimator()
    assert estimator.count("") == 0


def test_token_estimator_is_deterministic() -> None:
    """The same input yields the same count on every call."""
    from core.llm_budget import TokenEstimator

    estimator = TokenEstimator()
    first = estimator.count("the lazy operator reads the spec before the run")
    second = estimator.count("the lazy operator reads the spec before the run")
    assert first == second


def test_budget_ledger_records_a_charge(tmp_path: Path) -> None:
    """The ledger appends a record and persists the cumulative cost."""
    from core.llm_budget import BudgetLedger, LedgerEntry, ModelPrice

    ledger = BudgetLedger(path=tmp_path / "ledger.json")
    entry = LedgerEntry(
        model="llama-3.3-70b-versatile",
        input_tokens=100,
        output_tokens=50,
        cost_usd=0.0001,
        timestamp="2026-06-29T08:00:00+00:00",
    )
    ledger.record(entry)
    assert ledger.spent_today() > 0
    assert ledger.calls_today() == 1


def test_budget_ledger_persists_to_disk(tmp_sessions: Path) -> None:
    """The ledger survives a process restart by writing to disk."""
    from core.llm_budget import BudgetLedger, LedgerEntry

    path = tmp_sessions / "llm_budget.json"
    ledger = BudgetLedger(path=path)
    ledger.record(
        LedgerEntry(
            model="llama-3.3-70b-versatile",
            input_tokens=10,
            output_tokens=10,
            cost_usd=0.0001,
            timestamp="2026-06-29T08:00:00+00:00",
        )
    )
    reloaded = BudgetLedger(path=path)
    assert reloaded.spent_today() == ledger.spent_today()
    assert reloaded.calls_today() == 1


def test_budget_ledger_rolls_over_at_midnight(tmp_sessions: Path) -> None:
    """The ledger zeroes the spend when the day boundary passes."""
    from core.llm_budget import BudgetLedger, LedgerEntry

    path = tmp_sessions / "llm_budget.json"
    path.write_text(
        json.dumps(
            {
                "day": "2026-06-28",
                "entries": [
                    {
                        "model": "llama-3.3-70b-versatile",
                        "input_tokens": 10,
                        "output_tokens": 10,
                        "cost_usd": 0.5,
                        "timestamp": "2026-06-28T23:59:00+00:00",
                    }
                ],
            }
        ),
        encoding="utf-8",
    )
    ledger = BudgetLedger(path=path, today="2026-06-29")
    assert ledger.spent_today() == 0.0


def test_budget_guard_refuses_call_when_daily_budget_exhausted(tmp_sessions: Path) -> None:
    """The guard raises BudgetExceeded when the daily budget is already spent."""
    from core.llm_budget import (
        BudgetConfig,
        BudgetExceeded,
        BudgetGuard,
        LedgerEntry,
        ModelPrice,
        TokenEstimator,
    )

    config = BudgetConfig(
        daily_budget_usd=0.01,
        per_call_token_cap=100000,
        reset_at_utc="00:00",
        model_prices={"test-model": ModelPrice(input=1.0, output=1.0)},
        enabled=True,
        ledger_path=tmp_sessions / "llm_budget.json",
    )
    guard = BudgetGuard(config=config, estimator=TokenEstimator())
    guard.ledger.record(
        LedgerEntry(
            model="test-model",
            input_tokens=10,
            output_tokens=10,
            cost_usd=0.02,
            timestamp="2026-06-29T08:00:00+00:00",
        )
    )
    with pytest.raises(BudgetExceeded):
        guard.estimate_and_check(prompt="hello", model="test-model")


def test_budget_guard_refuses_call_when_token_cap_exceeded(tmp_sessions: Path) -> None:
    """The guard raises BudgetExceeded when the per call token cap is exceeded."""
    from core.llm_budget import (
        BudgetConfig,
        BudgetExceeded,
        BudgetGuard,
        ModelPrice,
        TokenEstimator,
    )

    config = BudgetConfig(
        daily_budget_usd=10.0,
        per_call_token_cap=5,
        reset_at_utc="00:00",
        model_prices={"test-model": ModelPrice(input=0.0, output=0.0)},
        enabled=True,
        ledger_path=tmp_sessions / "llm_budget.json",
    )
    guard = BudgetGuard(config=config, estimator=TokenEstimator())
    with pytest.raises(BudgetExceeded):
        guard.estimate_and_check(prompt="a longer prompt that exceeds the cap", model="test-model")


def test_budget_guard_charges_a_successful_call(tmp_sessions: Path) -> None:
    """The guard records a charge when the call fits the budget."""
    from core.llm_budget import (
        BudgetConfig,
        BudgetGuard,
        ModelPrice,
        TokenEstimator,
    )

    config = BudgetConfig(
        daily_budget_usd=1.0,
        per_call_token_cap=1000,
        reset_at_utc="00:00",
        model_prices={"test-model": ModelPrice(input=0.59, output=0.79)},
        enabled=True,
        ledger_path=tmp_sessions / "llm_budget.json",
    )
    guard = BudgetGuard(config=config, estimator=TokenEstimator())
    before = guard.ledger.spent_today()
    guard.estimate_and_check(prompt="hello", model="test-model", output_tokens=20)
    after = guard.ledger.spent_today()
    assert after > before


def test_budget_guard_disabled_passes_through(tmp_sessions: Path) -> None:
    """The guard does not record or check when the budget is disabled."""
    from core.llm_budget import (
        BudgetConfig,
        BudgetGuard,
        TokenEstimator,
    )

    config = BudgetConfig(
        daily_budget_usd=0.0,
        per_call_token_cap=0,
        reset_at_utc="00:00",
        model_prices={},
        enabled=False,
        ledger_path=tmp_sessions / "llm_budget.json",
    )
    guard = BudgetGuard(config=config, estimator=TokenEstimator())
    before = guard.ledger.calls_today()
    guard.estimate_and_check(prompt="hello", model="test-model", output_tokens=20)
    after = guard.ledger.calls_today()
    assert after == before


def test_format_budget_status_includes_spent_and_remaining(tmp_sessions: Path) -> None:
    """The formatted status surfaces the spent and remaining amounts."""
    from core.llm_budget import (
        BudgetConfig,
        BudgetLedger,
        format_budget_status,
    )

    config = BudgetConfig(
        daily_budget_usd=1.0,
        per_call_token_cap=1000,
        reset_at_utc="00:00",
        model_prices={},
        enabled=True,
        ledger_path=tmp_sessions / "llm_budget.json",
    )
    ledger = BudgetLedger(path=config.ledger_path)
    status = format_budget_status(config=config, ledger=ledger)
    assert "1.0000" in status or "1.0" in status
    assert "spent" in status.lower()


def test_read_budget_status_returns_dict(tmp_sessions: Path) -> None:
    """The read helper returns a structured status the MCP tool can serve."""
    from core.llm_budget import read_budget_status

    status = read_budget_status(
        payload={
            "llm_daily_budget_usd": 0.5,
            "llm_per_call_token_cap": 100,
            "llm_budget_enabled": True,
        },
        sessions_dir=tmp_sessions,
    )
    assert isinstance(status, dict)
    assert "spent_usd" in status
    assert "remaining_usd" in status
    assert "calls_today" in status
    assert "limit_usd" in status
    assert "per_call_token_cap" in status


def test_wrap_backend_with_budget_returns_same_shape(tmp_sessions: Path) -> None:
    """The wrapper exposes generate, complete, and stream_generate."""
    from core.llm_budget import (
        BudgetConfig,
        ModelPrice,
        TokenEstimator,
        wrap_backend_with_budget,
    )

    class _StubBackend:
        def generate(self, prompt: str) -> str:
            return "ok"

        def stream_generate(self, prompt: str):
            yield "ok"

        def complete(self, system: str, user: str, max_tokens: int, temperature: float) -> str:
            return "ok"

    config = BudgetConfig(
        daily_budget_usd=10.0,
        per_call_token_cap=100000,
        reset_at_utc="00:00",
        model_prices={"stub": ModelPrice(input=0.0, output=0.0)},
        enabled=True,
        ledger_path=tmp_sessions / "llm_budget.json",
    )
    wrapper = wrap_backend_with_budget(
        backend=_StubBackend(),
        config=config,
        estimator=TokenEstimator(),
        model="stub",
    )
    assert callable(wrapper.generate)
    assert callable(wrapper.complete)
    assert callable(wrapper.stream_generate)
    assert wrapper.generate("hello") == "ok"
    assert wrapper.complete("system", "user", 100, 0.2) == "ok"


def test_wrap_backend_with_budget_charges_call(tmp_sessions: Path) -> None:
    """The wrapper records a charge when a call succeeds."""
    from core.llm_budget import (
        BudgetConfig,
        ModelPrice,
        TokenEstimator,
        wrap_backend_with_budget,
    )

    class _StubBackend:
        def generate(self, prompt: str) -> str:
            return "ok"

        def stream_generate(self, prompt: str):
            yield "ok"

        def complete(self, system: str, user: str, max_tokens: int, temperature: float) -> str:
            return "ok"

    config = BudgetConfig(
        daily_budget_usd=1.0,
        per_call_token_cap=100000,
        reset_at_utc="00:00",
        model_prices={"stub": ModelPrice(input=0.59, output=0.79)},
        enabled=True,
        ledger_path=tmp_sessions / "llm_budget.json",
    )
    wrapper = wrap_backend_with_budget(
        backend=_StubBackend(),
        config=config,
        estimator=TokenEstimator(),
        model="stub",
    )
    wrapper.generate("hello world")
    assert wrapper.guard.ledger.calls_today() == 1


def test_payload_schema_recognises_budget_keys() -> None:
    """The schema registry contains every new budget key."""
    from core.llm_budget import TOKEN_BUDGET_FIELDS

    assert "llm_daily_budget_usd" in TOKEN_BUDGET_FIELDS
    assert "llm_per_call_token_cap" in TOKEN_BUDGET_FIELDS
    assert "llm_budget_enabled" in TOKEN_BUDGET_FIELDS
    assert "llm_reset_at_utc" in TOKEN_BUDGET_FIELDS
    assert "llm_model_prices" in TOKEN_BUDGET_FIELDS


def test_load_budget_config_reads_payload(tmp_sessions: Path) -> None:
    """The loader builds a BudgetConfig from a payload mapping."""
    from core.llm_budget import load_budget_config

    config = load_budget_config(
        payload={
            "llm_daily_budget_usd": 3.0,
            "llm_per_call_token_cap": 2000,
            "llm_budget_enabled": True,
            "llm_reset_at_utc": "00:00",
            "llm_model_prices": {
                "test-model": {"input": 0.5, "output": 1.0},
            },
        },
        sessions_dir=tmp_sessions,
    )
    assert config.daily_budget_usd == 3.0
    assert config.per_call_token_cap == 2000
    assert config.enabled is True
    assert config.model_prices["test-model"].input == 0.5
