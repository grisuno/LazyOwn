"""Tests for cli/chain_mode.py.

The chain prompt engine is pure coordination: suggestions come from an
injected resolver, input from an injected ``input_fn`` and output from an
injected ``print_fn``, so every branch is exercised with fakes — no
monkeypatching and no cmd2 coupling. Persistence is tested against a
temporary sessions directory.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(_ROOT))

from cli.chain_mode import (  # noqa: E402
    CHAIN_SKIP_VERBS,
    EXIT_WORDS,
    OUTCOME_NONE,
    OUTCOME_OFF,
    OUTCOME_RUN,
    OUTCOME_SKIP,
    ChainModeConfig,
    ChainModeStore,
    ChainOutcome,
    ChainPromptEngine,
    ChainSuggestion,
)


class _Step:
    """Duck-typed resolver step matching cli.command_chain.NextStep."""

    def __init__(self, name: str, source: str = "static", reason: str = "") -> None:
        self.name = name
        self.source = source
        self.reason = reason


def _resolver(*suggestions):
    def resolve(cmd: str, phase: str):
        return list(suggestions)

    return resolve


def _engine(
    resolver=None,
    *,
    answers: list[str],
    enabled: bool = True,
    interactive: bool = True,
    config: ChainModeConfig | None = None,
) -> tuple[ChainPromptEngine, list[str]]:
    printed: list[str] = []
    queue = iter(answers)

    def fake_input(prompt: str) -> str:
        printed.append(prompt)
        try:
            return next(queue)
        except StopIteration:
            return ""

    if config is None:
        import tempfile

        config = ChainModeConfig(sessions_dir=tempfile.mkdtemp(prefix="chain_mode_test_"))
    engine = ChainPromptEngine(
        config=config,
        resolver=resolver,
        input_fn=fake_input,
        print_fn=printed.append,
        interactive=interactive,
    )
    engine.set_enabled(enabled, persist=False)
    return engine, printed


def test_suggestion_from_step_and_string() -> None:
    assert ChainSuggestion.from_step(_Step("gobuster", "service", "open http")).name == "gobuster"
    assert ChainSuggestion.from_step("nmap").name == "nmap"


def test_step_none_when_disabled() -> None:
    engine, _ = _engine(_resolver(_Step("nmap")), answers=[], enabled=False)
    assert engine.step("ping") == ChainOutcome(OUTCOME_NONE)


def test_step_none_when_not_interactive() -> None:
    engine, _ = _engine(_resolver(_Step("nmap")), answers=[], interactive=False)
    assert engine.step("ping") == ChainOutcome(OUTCOME_NONE)


@pytest.mark.parametrize("verb", sorted(CHAIN_SKIP_VERBS))
def test_step_none_for_skip_verbs(verb: str) -> None:
    engine, _ = _engine(_resolver(_Step("nmap")), answers=[])
    assert engine.step(verb) == ChainOutcome(OUTCOME_NONE)


def test_enter_runs_top_suggestion() -> None:
    engine, _ = _engine(
        _resolver(_Step("lazynmap", "static", "after ping"), _Step("arpscan")),
        answers=[""],
    )
    outcome = engine.step("ping")
    assert outcome.state == OUTCOME_RUN
    assert outcome.command == "lazynmap"


def test_number_selects_ranked_alternative() -> None:
    engine, _ = _engine(
        _resolver(_Step("lazynmap"), _Step("arpscan"), _Step("hosts_discovery")),
        answers=["2"],
    )
    outcome = engine.step("ping")
    assert outcome.state == OUTCOME_RUN
    assert outcome.command == "arpscan"


def test_override_runs_operator_command() -> None:
    engine, _ = _engine(
        _resolver(_Step("gobuster")),
        answers=["nmap -sV -p- 10.10.10.5"],
    )
    outcome = engine.step("ping")
    assert outcome.state == OUTCOME_RUN
    assert outcome.command == "nmap -sV -p- 10.10.10.5"


def test_skip_keeps_chain_mode_enabled() -> None:
    engine, _ = _engine(_resolver(_Step("lazynmap")), answers=["skip"])
    outcome = engine.step("ping")
    assert outcome.state == OUTCOME_SKIP
    assert engine.enabled


@pytest.mark.parametrize("word", sorted(EXIT_WORDS))
def test_exit_words_disable_chain_mode(word: str) -> None:
    engine, _ = _engine(_resolver(_Step("lazynmap")), answers=[word])
    outcome = engine.step("ping")
    assert outcome.state == OUTCOME_OFF
    assert not engine.enabled


def test_no_suggestions_enter_skips_custom_command_runs() -> None:
    engine, _ = _engine(None, answers=[""])
    assert engine.step("whoami_priv").state == OUTCOME_SKIP
    engine, _ = _engine(None, answers=["nmap"])
    outcome = engine.step("whoami_priv")
    assert outcome.state == OUTCOME_RUN
    assert outcome.command == "nmap"


def test_invalid_number_skips() -> None:
    engine, _ = _engine(_resolver(_Step("lazynmap")), answers=["9"])
    outcome = engine.step("ping")
    assert outcome.state == OUTCOME_SKIP
    assert engine.enabled


def test_keyboard_interrupt_disables(tmp_path: Path) -> None:
    def raise_ki(prompt: str) -> str:
        raise KeyboardInterrupt

    engine = ChainPromptEngine(
        config=ChainModeConfig(sessions_dir=str(tmp_path)),
        resolver=_resolver(_Step("lazynmap")),
        input_fn=raise_ki,
        print_fn=lambda _s: None,
        interactive=True,
    )
    engine.set_enabled(True, persist=False)
    outcome = engine.step("ping")
    assert outcome.state == OUTCOME_OFF
    assert not engine.enabled


def test_auto_pause_after_max_steps(tmp_path: Path) -> None:
    store_path = tmp_path / "chain_mode.json"
    engine, _ = _engine(
        _resolver(_Step("lazynmap")),
        answers=["", ""],
        config=ChainModeConfig(sessions_dir=str(tmp_path), max_steps=2),
    )
    engine.set_enabled(True, persist=False)
    assert engine.step("ping").state == OUTCOME_RUN
    assert engine.step("ping").state == OUTCOME_RUN
    outcome = engine.step("ping")
    assert outcome.state == OUTCOME_OFF
    assert "paused" in outcome.reason
    assert not store_path.exists()


def test_resolver_failure_degrades_to_no_suggestions() -> None:
    def broken(cmd: str, phase: str):
        raise RuntimeError("boom")

    engine, _ = _engine(broken, answers=["nmap"])
    outcome = engine.step("ping")
    assert outcome.state == OUTCOME_RUN
    assert outcome.command == "nmap"


def test_store_roundtrip_and_missing(tmp_path: Path) -> None:
    store = ChainModeStore(str(tmp_path))
    assert store.load() is None
    store.save(True)
    assert store.load() is True
    store.save(False)
    assert store.load() is False


def test_store_survives_malformed_file(tmp_path: Path) -> None:
    store = ChainModeStore(str(tmp_path))
    store.path.parent.mkdir(parents=True, exist_ok=True)
    store.path.write_text("{not json", encoding="utf-8")
    assert store.load() is None
    store.save(True)
    assert store.load() is True


def test_engine_reads_persisted_state(tmp_path: Path) -> None:
    store = ChainModeStore(str(tmp_path))
    store.save(True)
    engine = ChainPromptEngine(
        config=ChainModeConfig(sessions_dir=str(tmp_path)),
        resolver=_resolver(_Step("lazynmap")),
        input_fn=lambda _p: "off",
        print_fn=lambda _s: None,
        interactive=True,
    )
    assert engine.enabled


def test_persist_toggle_writes_state_file(tmp_path: Path) -> None:
    store_path = tmp_path / "chain_mode.json"
    engine = ChainPromptEngine(
        config=ChainModeConfig(sessions_dir=str(tmp_path)),
        resolver=_resolver(_Step("lazynmap")),
        input_fn=lambda _p: "off",
        print_fn=lambda _s: None,
        interactive=True,
    )
    engine.set_enabled(True, persist=True)
    assert json.loads(store_path.read_text(encoding="utf-8"))["enabled"] is True
    engine.set_enabled(False, persist=True)
    assert json.loads(store_path.read_text(encoding="utf-8"))["enabled"] is False


def test_prompt_exit_words_persist_off(tmp_path: Path) -> None:
    store_path = tmp_path / "chain_mode.json"
    engine, _ = _engine(
        _resolver(_Step("lazynmap")),
        answers=["off"],
        config=ChainModeConfig(sessions_dir=str(tmp_path)),
    )
    assert engine.step("ping").state == OUTCOME_OFF
    assert not engine.enabled
    assert json.loads(store_path.read_text(encoding="utf-8"))["enabled"] is False
