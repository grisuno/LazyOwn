"""Ghost-text autosuggest engine for the LazyOwn cmd2 shell.

After every command, the engine consults its provider chain to pick the
most likely next command. The selected :class:`Suggestion` is held as
state, surfaced as a dim ANSI fragment inside the cmd2 prompt, and
executed with a single keystroke via the ``do_next`` shell command (or
its ``.`` alias).

The module is pure presentation + state. It does not import cmd2,
Flask, or any LazyOwn module so providers and the engine remain
unit-testable in isolation. Concrete providers receive their backing
data structures via constructor injection (Dependency Inversion).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Protocol, Sequence

GHOST_TEXT_LIMIT: int = 48
HINT_COMMAND_LIMIT: int = 72
HINT_REASON_LIMIT: int = 40
KILLCHAIN_BASE_SCORE: float = 0.5
PHASE_FALLBACK_FACTOR: float = 0.7
GRAPH_BASE_SCORE: float = 0.8
GRAPH_SCORE_WEIGHT: float = 0.2
ANSI_DIM_GREY: str = "\x1b[2;37m"
ANSI_RESET: str = "\x1b[0m"
ACCEPT_KEY_HINT: str = "."

SKIP_TRIGGER_COMMANDS: frozenset[str] = frozenset(
    {
        "help",
        "?",
        "exit",
        "quit",
        "history",
        "next",
        ".",
        ",",
        "shell",
        "set",
        "assign",
    }
)


@dataclass(frozen=True)
class SuggestionContext:
    """Inputs available to every suggestion provider.

    Args:
        last_command: First token of the last command executed.
        phase: Current engagement phase (recon, enum, exploit, ...).
        recent_commands: Last N commands from the session transcript,
            newest entries appearing last.
        target: Active rhost loaded from ``payload.json``.
        os_hint: Detected target OS — ``"linux"``, ``"windows"``, or
            ``"unknown"``.
    """

    last_command: str = ""
    phase: str = ""
    recent_commands: Sequence[str] = ()
    target: str = ""
    os_hint: str = "unknown"


@dataclass(frozen=True)
class Suggestion:
    """One next-command suggestion with its rationale.

    Args:
        command: Shell command executed when the operator accepts the
            suggestion via ``do_next``.
        reason: Human-readable explanation surfaced in the prompt and
            event log.
        score: Provider-specific confidence. Higher is better. The
            :class:`CompositeProvider` uses it to arbitrate across
            providers.
        source: Short label identifying which provider produced the
            suggestion (``graph``, ``killchain``, ``phase``, ...).
    """

    command: str
    reason: str = ""
    score: float = 0.0
    source: str = ""


class SuggestionProvider(Protocol):
    """Provider contract: examine context, return one suggestion or ``None``."""

    def suggest(self, context: SuggestionContext) -> Suggestion | None: ...


class CompositeProvider:
    """Aggregator that returns the highest-scoring suggestion across providers.

    Adding a provider is a constructor argument; the engine itself
    never changes, honouring the Open/Closed principle.
    """

    def __init__(self, providers: Sequence[SuggestionProvider]) -> None:
        """Store the provider chain.

        Args:
            providers: Sequence of objects implementing
                :class:`SuggestionProvider`. Order is irrelevant for
                correctness; the highest score wins.
        """
        self._providers: tuple[SuggestionProvider, ...] = tuple(providers)

    def suggest(self, context: SuggestionContext) -> Suggestion | None:
        """Return the best suggestion across the chain, or ``None``.

        A misbehaving provider that raises is silently skipped so a
        single broken adapter cannot break the prompt.
        """
        best: Suggestion | None = None
        for provider in self._providers:
            try:
                candidate = provider.suggest(context)
            except Exception:
                continue
            if candidate is None:
                continue
            if best is None or candidate.score > best.score:
                best = candidate
        return best


class KillChainProvider:
    """Provider backed by the static kill-chain adjacency map.

    Falls back to the phase-priority table when no adjacency entry
    exists for the last command. Commands already present in
    :attr:`SuggestionContext.recent_commands` are skipped so the
    suggestion is always forward-looking.
    """

    def __init__(
        self,
        chain: dict[str, list[str]],
        phase_priority: dict[str, list[str]],
        *,
        base_score: float = KILLCHAIN_BASE_SCORE,
    ) -> None:
        """Configure the provider.

        Args:
            chain: ``command -> [next_command, ...]`` adjacency map.
            phase_priority: ``phase -> [command, ...]`` fallback map.
            base_score: Score assigned to adjacency matches. Phase
                fallbacks receive ``base_score * PHASE_FALLBACK_FACTOR``.
        """
        self._chain: dict[str, list[str]] = dict(chain)
        self._phase_priority: dict[str, list[str]] = dict(phase_priority)
        self._base_score: float = float(base_score)

    def suggest(self, context: SuggestionContext) -> Suggestion | None:
        """Return the first unseen adjacency, or phase fallback, or ``None``."""
        already = set(context.recent_commands)
        last_tokens = context.last_command.strip().split()
        last_cmd = last_tokens[0] if last_tokens else ""
        if last_cmd:
            already.add(last_cmd)
        for candidate in self._chain.get(last_cmd, []):
            if candidate and candidate not in already:
                return Suggestion(
                    command=candidate,
                    reason=f"adjacency from {last_cmd}",
                    score=self._base_score,
                    source="killchain",
                )
        phase_key = (context.phase or "recon").lower()
        for candidate in self._phase_priority.get(phase_key, []):
            if candidate and candidate not in already:
                return Suggestion(
                    command=candidate,
                    reason=f"phase priority for {phase_key}",
                    score=self._base_score * PHASE_FALLBACK_FACTOR,
                    source="phase",
                )
        return None


class GraphProvider:
    """Provider backed by the graphify knowledge-graph advisor.

    Accepts any object exposing ``suggest_next(recent_commands, limit)``
    returning a list of dicts so this module stays decoupled from the
    concrete :class:`cli.graph_advisor.GraphAdvisor` implementation.
    """

    def __init__(
        self,
        advisor: Any,
        *,
        limit: int = 1,
        base_score: float = GRAPH_BASE_SCORE,
        score_weight: float = GRAPH_SCORE_WEIGHT,
    ) -> None:
        """Configure the provider.

        Args:
            advisor: Object exposing ``suggest_next`` with the contract
                described in the class docstring.
            limit: Number of candidates to request from the advisor.
                The top-ranked entry is returned to the engine.
            base_score: Floor score for any non-empty graph result.
            score_weight: Multiplier applied to the advisor-supplied
                score when blending with ``base_score``.
        """
        self._advisor: Any = advisor
        self._limit: int = max(1, int(limit))
        self._base_score: float = float(base_score)
        self._score_weight: float = float(score_weight)

    def suggest(self, context: SuggestionContext) -> Suggestion | None:
        """Query the advisor and adapt the top result to a :class:`Suggestion`."""
        last_tokens = context.last_command.strip().split()
        if not last_tokens:
            return None
        seeds = list(context.recent_commands) or [last_tokens[0]]
        results = self._advisor.suggest_next(recent_commands=seeds, limit=self._limit)
        if not results:
            return None
        top = results[0]
        label = (top.get("label") or top.get("id") or "").strip()
        if not label:
            return None
        graph_score = float(top.get("score", 0.0))
        bounded_graph_score = min(graph_score, 1.0)
        blended = self._base_score + bounded_graph_score * self._score_weight
        return Suggestion(
            command=label,
            reason="graph proximity from recent commands",
            score=blended,
            source="graph",
        )


class AutoSuggestEngine:
    """Stateful holder for the active ghost-text suggestion.

    The engine is a thin coordinator: it never decides what to suggest
    (delegated to its :class:`SuggestionProvider`) and only owns the
    current-suggestion state machine plus the rendering surface for the
    prompt.
    """

    def __init__(self, provider: SuggestionProvider, *, enabled: bool = True) -> None:
        """Store the provider and enabled flag.

        Args:
            provider: Object implementing :class:`SuggestionProvider`.
                Typically a :class:`CompositeProvider`.
            enabled: Whether the engine refreshes suggestions on each
                postcmd hook. The shell flips this from
                ``payload.json["enable_autosuggest"]`` so the operator
                can toggle without a restart.
        """
        self._provider: SuggestionProvider = provider
        self._current: Suggestion | None = None
        self._enabled: bool = bool(enabled)

    @property
    def enabled(self) -> bool:
        """Whether the engine refreshes suggestions on each command."""
        return self._enabled

    def set_enabled(self, value: bool) -> None:
        """Toggle the engine without losing the provider chain.

        Disabling clears the active suggestion so the prompt returns to
        its plain form on the next render.
        """
        self._enabled = bool(value)
        if not self._enabled:
            self._current = None

    def current(self) -> Suggestion | None:
        """Return the suggestion last computed, or ``None`` when cleared."""
        return self._current

    def clear(self) -> None:
        """Drop the active suggestion (called after accept or abort)."""
        self._current = None

    def refresh(self, context: SuggestionContext) -> Suggestion | None:
        """Recompute the suggestion from the provider chain.

        Commands listed in :data:`SKIP_TRIGGER_COMMANDS` are ignored so
        refreshing after ``help`` or ``next`` is meaningless or
        recursive. When the engine is disabled the current suggestion
        is cleared and ``None`` is returned.
        """
        if not self._enabled:
            self._current = None
            return None
        tokens = context.last_command.strip().split()
        if tokens and tokens[0] in SKIP_TRIGGER_COMMANDS:
            return self._current
        self._current = self._provider.suggest(context)
        return self._current

    def accept(self) -> str | None:
        """Return the active command string and clear the suggestion."""
        if self._current is None:
            return None
        command = self._current.command
        self._current = None
        return command

    def display_text(self) -> str:
        """Return the ANSI-coloured ghost-text fragment for legacy callers.

        The fragment is empty when no suggestion is active or when the
        engine is disabled. The rendered command is truncated to
        :data:`GHOST_TEXT_LIMIT` characters. This API is preserved for
        callers that want to embed the suggestion inline; the cmd2
        shell uses :func:`render_hint_line` instead so the prompt
        itself stays clean.
        """
        if not self._enabled or self._current is None:
            return ""
        command = self._current.command
        if len(command) > GHOST_TEXT_LIMIT:
            command = command[: GHOST_TEXT_LIMIT - 3] + "..."
        return f"{ANSI_DIM_GREY}[next: {command}]{ANSI_RESET}"


def _truncate(value: str, max_len: int) -> str:
    """Return ``value`` shortened to ``max_len`` characters with an ellipsis."""
    if max_len <= 3:
        return value[:max_len]
    if len(value) <= max_len:
        return value
    return value[: max_len - 3] + "..."


def format_hint_line(
    suggestion: Suggestion,
    *,
    accept_key: str = ACCEPT_KEY_HINT,
    command_limit: int = HINT_COMMAND_LIMIT,
    reason_limit: int = HINT_REASON_LIMIT,
) -> str:
    """Build the dim hint string surfaced after each command.

    The format is deliberately compact and unambiguous about the
    accept key: ``  >> press '.' to run: gobuster (reason via graph)``.
    Truncation honours :data:`HINT_COMMAND_LIMIT` and
    :data:`HINT_REASON_LIMIT` so the line never exceeds one terminal
    row at the typical 100-column width.

    Args:
        suggestion: Suggestion to render.
        accept_key: Visible key the operator presses to accept.
        command_limit: Maximum command-fragment length.
        reason_limit: Maximum reason-fragment length.

    Returns:
        Plain string (no ANSI). The shell wraps it in dim style at
        render time so callers can pipe the value into logs without
        carrying escape codes.
    """
    command = _truncate(suggestion.command, command_limit)
    reason = (suggestion.reason or suggestion.source or "").strip()
    if reason:
        return f"press '{accept_key}' to run: {command}  ({_truncate(reason, reason_limit)})"
    return f"press '{accept_key}' to run: {command}"


def render_hint_line(
    engine: AutoSuggestEngine,
    *,
    console: Any = None,
    prefix: str = "  >> ",
    accept_key: str = ACCEPT_KEY_HINT,
) -> bool:
    """Print one dim hint line for the engine's active suggestion.

    Returns ``True`` when something was printed, ``False`` otherwise.
    The function is a no-op when the engine is disabled or has no
    active suggestion so callers can register it unconditionally as a
    cmd2 postcmd hook.

    Args:
        engine: :class:`AutoSuggestEngine` whose current suggestion to
            render.
        console: Optional ``rich.console.Console`` instance. When
            ``None`` a module-private console is used so tests can
            inject a capturing console.
        prefix: Leading marker, default matches ``cli.reactive_hints``.
        accept_key: Visible accept-key hint passed through to
            :func:`format_hint_line`.
    """
    suggestion = engine.current()
    if suggestion is None:
        return False
    text = format_hint_line(suggestion, accept_key=accept_key)
    target = console if console is not None else _hint_console()
    target.print(f"[dim cyan]{prefix}[/dim cyan][dim white italic]{text}[/dim white italic]")
    return True


_HINT_CONSOLE_CACHE: list = []


def _hint_console() -> Any:
    """Return a lazily-initialised :class:`rich.console.Console`.

    Imported lazily so unit tests can run without ``rich`` installed.
    The instance is cached at module scope so subsequent calls reuse
    the same console.
    """
    if _HINT_CONSOLE_CACHE:
        return _HINT_CONSOLE_CACHE[0]
    from rich.console import Console

    console = Console(stderr=False, highlight=False, soft_wrap=True)
    _HINT_CONSOLE_CACHE.append(console)
    return console


def build_default_engine(
    advisor: Any | None,
    chain: dict[str, list[str]],
    phase_priority: dict[str, list[str]],
    *,
    enabled: bool = True,
) -> AutoSuggestEngine:
    """Wire the canonical provider chain used by the cmd2 shell.

    Order is: graph provider (high signal) followed by the kill-chain
    fallback. Each provider is wrapped defensively so a misbehaving
    advisor cannot break the prompt.

    Args:
        advisor: Optional graph advisor. When ``None`` or when
            ``advisor.is_available()`` returns ``False`` the graph
            provider is omitted.
        chain: Static kill-chain adjacency map shared with
            ``cli.reactive_hints``.
        phase_priority: Phase-priority map shared with the same module.
        enabled: Initial enable state for the engine.

    Returns:
        An :class:`AutoSuggestEngine` ready to register with cmd2.
    """
    providers: list[SuggestionProvider] = []
    if advisor is not None:
        try:
            if advisor.is_available():
                providers.append(GraphProvider(advisor))
        except Exception:
            pass
    providers.append(KillChainProvider(chain, phase_priority))
    composite = CompositeProvider(providers)
    return AutoSuggestEngine(composite, enabled=enabled)


__all__ = [
    "ACCEPT_KEY_HINT",
    "ANSI_DIM_GREY",
    "ANSI_RESET",
    "AutoSuggestEngine",
    "CompositeProvider",
    "GHOST_TEXT_LIMIT",
    "GraphProvider",
    "HINT_COMMAND_LIMIT",
    "HINT_REASON_LIMIT",
    "KillChainProvider",
    "SKIP_TRIGGER_COMMANDS",
    "Suggestion",
    "SuggestionContext",
    "SuggestionProvider",
    "build_default_engine",
    "format_hint_line",
    "render_hint_line",
]
