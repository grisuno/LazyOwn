"""Unit tests for cli.autosuggest.

Coverage:

* Suggestion provider contract: composite arbitration, skip rules,
  defensive error handling.
* Engine state machine: refresh, accept clears state, set_enabled
  toggling.
* Display rendering: empty when no suggestion, ANSI delimiters around
  active suggestion, truncation honours :data:`GHOST_TEXT_LIMIT`.
* Provider adapters: kill-chain adjacency and phase fallback,
  graph-advisor adapter blends scores.
"""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from cli.autosuggest import (  # noqa: E402
    ACCEPT_KEY_HINT,
    ANSI_DIM_GREY,
    ANSI_RESET,
    GHOST_TEXT_LIMIT,
    HINT_COMMAND_LIMIT,
    AutoSuggestEngine,
    CompositeProvider,
    GraphProvider,
    KillChainProvider,
    Suggestion,
    SuggestionContext,
    build_default_engine,
    format_hint_line,
    render_hint_line,
)


class _StaticProvider:
    """Test double that always returns the same suggestion."""

    def __init__(self, suggestion):
        self._suggestion = suggestion

    def suggest(self, context):
        return self._suggestion


class _RaisingProvider:
    """Provider that always raises — composite must skip it."""

    def suggest(self, context):
        raise RuntimeError("boom")


def test_engine_refresh_stores_suggestion():
    suggestion = Suggestion(command="nmap", reason="seed", score=0.5, source="test")
    engine = AutoSuggestEngine(_StaticProvider(suggestion))

    result = engine.refresh(SuggestionContext(last_command="ping 10.0.0.1"))

    assert result == suggestion
    assert engine.current() == suggestion


def test_engine_accept_returns_command_and_clears():
    suggestion = Suggestion(command="gobuster", score=0.5)
    engine = AutoSuggestEngine(_StaticProvider(suggestion))
    engine.refresh(SuggestionContext(last_command="lazynmap"))

    accepted = engine.accept()

    assert accepted == "gobuster"
    assert engine.current() is None
    assert engine.accept() is None


def test_engine_disabled_clears_state_and_returns_none():
    suggestion = Suggestion(command="ffuf", score=0.5)
    engine = AutoSuggestEngine(_StaticProvider(suggestion))
    engine.refresh(SuggestionContext(last_command="lazynmap"))

    engine.set_enabled(False)

    assert engine.enabled is False
    assert engine.current() is None
    assert engine.refresh(SuggestionContext(last_command="lazynmap")) is None


def test_engine_skip_commands_do_not_refresh():
    suggestion = Suggestion(command="nmap", score=0.5)
    engine = AutoSuggestEngine(_StaticProvider(suggestion))

    engine.refresh(SuggestionContext(last_command="help"))

    assert engine.current() is None


def test_engine_display_text_empty_without_suggestion():
    engine = AutoSuggestEngine(_StaticProvider(None))

    assert engine.display_text() == ""


def test_engine_display_text_renders_active_suggestion():
    engine = AutoSuggestEngine(
        _StaticProvider(Suggestion(command="ffuf", score=0.5))
    )
    engine.refresh(SuggestionContext(last_command="lazynmap"))

    rendered = engine.display_text()

    assert rendered.startswith(ANSI_DIM_GREY)
    assert rendered.endswith(ANSI_RESET)
    assert "[next: ffuf]" in rendered


def test_engine_display_text_truncates_long_command():
    long_command = "a" * (GHOST_TEXT_LIMIT + 10)
    engine = AutoSuggestEngine(
        _StaticProvider(Suggestion(command=long_command, score=0.5))
    )
    engine.refresh(SuggestionContext(last_command="lazynmap"))

    rendered = engine.display_text()
    inner_start = rendered.index("[next: ") + len("[next: ")
    inner_end = rendered.index("]", inner_start)
    inner = rendered[inner_start:inner_end]

    assert len(inner) == GHOST_TEXT_LIMIT
    assert inner.endswith("...")


def test_composite_picks_highest_score():
    low = Suggestion(command="low", score=0.2)
    high = Suggestion(command="high", score=0.9)
    composite = CompositeProvider([_StaticProvider(low), _StaticProvider(high)])

    result = composite.suggest(SuggestionContext())

    assert result == high


def test_composite_skips_raising_provider():
    suggestion = Suggestion(command="ok", score=0.5)
    composite = CompositeProvider(
        [_RaisingProvider(), _StaticProvider(suggestion)]
    )

    result = composite.suggest(SuggestionContext())

    assert result == suggestion


def test_composite_returns_none_when_no_provider_responds():
    composite = CompositeProvider([_StaticProvider(None), _StaticProvider(None)])

    assert composite.suggest(SuggestionContext()) is None


def test_killchain_provider_uses_adjacency():
    chain = {"lazynmap": ["gobuster", "ffuf"]}
    provider = KillChainProvider(chain, phase_priority={})

    suggestion = provider.suggest(
        SuggestionContext(last_command="lazynmap", recent_commands=())
    )

    assert suggestion is not None
    assert suggestion.command == "gobuster"
    assert suggestion.source == "killchain"


def test_killchain_provider_skips_already_executed():
    chain = {"lazynmap": ["gobuster", "ffuf"]}
    provider = KillChainProvider(chain, phase_priority={})

    suggestion = provider.suggest(
        SuggestionContext(
            last_command="lazynmap", recent_commands=("gobuster",),
        )
    )

    assert suggestion is not None
    assert suggestion.command == "ffuf"


def test_killchain_provider_falls_back_to_phase_priority():
    provider = KillChainProvider(
        chain={},
        phase_priority={"recon": ["lazynmap"]},
    )

    suggestion = provider.suggest(
        SuggestionContext(last_command="unknown", phase="recon")
    )

    assert suggestion is not None
    assert suggestion.command == "lazynmap"
    assert suggestion.source == "phase"


def test_killchain_provider_returns_none_with_nothing_to_offer():
    provider = KillChainProvider(chain={}, phase_priority={})

    assert provider.suggest(SuggestionContext(last_command="abc")) is None


class _FakeAdvisor:
    def __init__(self, results, available=True):
        self._results = results
        self._available = available

    def is_available(self):
        return self._available

    def suggest_next(self, recent_commands, limit):
        return list(self._results)[:limit]


def test_graph_provider_returns_top_result():
    advisor = _FakeAdvisor([
        {"label": "gobuster", "score": 0.7},
        {"label": "ffuf", "score": 0.3},
    ])
    provider = GraphProvider(advisor)

    suggestion = provider.suggest(
        SuggestionContext(last_command="lazynmap", recent_commands=("lazynmap",))
    )

    assert suggestion is not None
    assert suggestion.command == "gobuster"
    assert suggestion.source == "graph"
    assert suggestion.score > 0.5


def test_graph_provider_returns_none_when_advisor_empty():
    advisor = _FakeAdvisor([])
    provider = GraphProvider(advisor)

    assert provider.suggest(SuggestionContext(last_command="lazynmap")) is None


def test_graph_provider_skips_when_last_command_blank():
    advisor = _FakeAdvisor([{"label": "gobuster", "score": 0.9}])
    provider = GraphProvider(advisor)

    assert provider.suggest(SuggestionContext(last_command="")) is None


def test_build_default_engine_includes_killchain_only_when_no_advisor():
    chain = {"lazynmap": ["gobuster"]}
    phase_priority = {"recon": ["lazynmap"]}

    engine = build_default_engine(
        advisor=None, chain=chain, phase_priority=phase_priority,
    )

    suggestion = engine.refresh(
        SuggestionContext(last_command="lazynmap", recent_commands=())
    )
    assert suggestion is not None
    assert suggestion.command == "gobuster"


def test_format_hint_line_includes_accept_key_and_reason():
    suggestion = Suggestion(
        command="gobuster -u http://target -w list.txt",
        reason="graph proximity from recent commands",
        source="graph",
    )

    text = format_hint_line(suggestion)

    assert ACCEPT_KEY_HINT in text
    assert "gobuster" in text
    assert "graph proximity" in text


def test_format_hint_line_truncates_long_command():
    long_command = "x" * (HINT_COMMAND_LIMIT + 10)
    suggestion = Suggestion(command=long_command, reason="r")

    text = format_hint_line(suggestion)
    fragment_end = text.index("  ")
    rendered_command = text[text.index(": ") + 2 : fragment_end]

    assert len(rendered_command) <= HINT_COMMAND_LIMIT
    assert rendered_command.endswith("...")


def test_format_hint_line_omits_reason_when_blank():
    suggestion = Suggestion(command="ls", reason="", source="")

    text = format_hint_line(suggestion)

    assert "(" not in text


class _CapturingConsole:
    def __init__(self):
        self.lines = []

    def print(self, value):
        self.lines.append(str(value))


def test_render_hint_line_emits_to_console():
    engine = AutoSuggestEngine(
        _StaticProvider(Suggestion(command="gobuster", reason="next", source="graph"))
    )
    engine.refresh(SuggestionContext(last_command="lazynmap"))
    console = _CapturingConsole()

    printed = render_hint_line(engine, console=console)

    assert printed is True
    assert any("gobuster" in line for line in console.lines)
    assert any(ACCEPT_KEY_HINT in line for line in console.lines)


def test_render_hint_line_is_noop_without_suggestion():
    engine = AutoSuggestEngine(_StaticProvider(None))
    console = _CapturingConsole()

    printed = render_hint_line(engine, console=console)

    assert printed is False
    assert console.lines == []


def test_render_hint_line_is_noop_when_disabled():
    engine = AutoSuggestEngine(
        _StaticProvider(Suggestion(command="x", reason="r")),
    )
    engine.refresh(SuggestionContext(last_command="lazynmap"))
    engine.set_enabled(False)
    console = _CapturingConsole()

    printed = render_hint_line(engine, console=console)

    assert printed is False
    assert console.lines == []


class _SequenceProvider:
    """Provider that returns a different suggestion on each call."""

    def __init__(self, suggestions):
        self._suggestions = list(suggestions)
        self._index = 0

    def suggest(self, context):
        if self._index >= len(self._suggestions):
            return None
        value = self._suggestions[self._index]
        self._index += 1
        return value


def test_engine_advances_suggestion_after_accept_refresh():
    first = Suggestion(command="lazynmap", reason="recon", source="killchain")
    second = Suggestion(command="gobuster", reason="enum", source="killchain")
    provider = _SequenceProvider([first, second])
    engine = AutoSuggestEngine(provider)
    engine.refresh(SuggestionContext(last_command="ping"))

    accepted = engine.accept()
    assert accepted == "lazynmap"
    assert engine.current() is None

    engine.refresh(SuggestionContext(last_command=accepted))

    new_suggestion = engine.current()
    assert new_suggestion is not None
    assert new_suggestion.command == "gobuster"


def test_build_default_engine_with_unavailable_advisor():
    chain = {"lazynmap": ["ffuf"]}
    phase_priority = {"recon": ["lazynmap"]}
    advisor = _FakeAdvisor([], available=False)

    engine = build_default_engine(
        advisor=advisor, chain=chain, phase_priority=phase_priority,
    )

    suggestion = engine.refresh(
        SuggestionContext(last_command="lazynmap", recent_commands=())
    )
    assert suggestion is not None
    assert suggestion.command == "ffuf"
