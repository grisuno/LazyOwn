"""Interactive kill-chain chaining coordinator.

This module glues the framework's existing "what next" brains
(:class:`cli.command_chain.CommandChain`, which fuses the static
kill-chain tables with nmap-discovered services, addon triggers and the
engagement phase) to an interactive prompt loop so the operator can walk
every kill-chain phase without ever leaving the shell flow.

After a command executes the operator is shown the world-model-driven
next steps and may:

* press **Enter** to run the top suggestion,
* type ``1..N`` to run that ranked alternative,
* type **any command** to override the suggestion ("no, run nmap
  instead") — that command executes and the chain continues from it,
* type ``skip`` to step out of the chain while keeping chain mode on,
* press **ESC**, **Ctrl+C** or type ``exit``/``quit``/``off`` to leave
  chain mode entirely (persisted, so it stays off until the operator
  runs ``chainmode on`` again).

Design (SOLID):

* ``ChainModeConfig`` centralises every magic value.
* ``ChainModeStore`` owns atomic persistence to
  ``sessions/chain_mode.json`` (same pattern as ``daemon_control.json``).
* ``ChainPromptEngine`` is pure coordination: it receives suggestions
  from an injected ``resolver`` callable, renders via an injected
  ``print_fn``, reads operator input (TTY-aware, with ESC/Ctrl+C
  support) and returns a :class:`ChainOutcome` — it never executes
  commands itself and has zero coupling to ``cmd2`` or ``lazyown.py``.
"""

from __future__ import annotations

import json
import os
import sys
import tempfile
from collections.abc import Callable, Sequence
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

STATE_FILE_NAME: str = "chain_mode.json"
MAX_STEPS_DEFAULT: int = 12
MAX_OPTIONS_DEFAULT: int = 5
LOOP_GUARD_MARGIN: int = 4

OUTCOME_RUN: str = "run"
OUTCOME_SKIP: str = "skip"
OUTCOME_OFF: str = "off"
OUTCOME_NONE: str = "none"

EXIT_WORDS: frozenset[str] = frozenset({"off", "stop", "exit", "quit", "end", "disable"})
SKIP_WORDS: frozenset[str] = frozenset({"skip", "none", "later", "s"})


class _ChainEscExit(Exception):
    """Internal signal: the operator pressed ESC at the chain prompt."""


def _read_line_unix(prompt: str) -> str:
    """Read one line in raw TTY mode, honouring ESC, Ctrl+C and backspace.

    Raw mode is required because canonical terminal input does not
    deliver a lone ESC byte until Enter is pressed. The original termios
    settings are restored in ``finally`` so the cmd2 readline prompt is
    unaffected.

    Args:
        prompt: Text printed before reading.

    Returns:
        The typed line without the trailing newline.

    Raises:
        _ChainEscExit: The operator pressed ESC.
        KeyboardInterrupt: The operator pressed Ctrl+C.
        EOFError: End of input with an empty line.
    """
    import termios
    import tty

    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    chars: list[str] = []
    sys.stdout.write(prompt)
    sys.stdout.flush()
    try:
        tty.setraw(fd)
        while True:
            chunk = os.read(fd, 1)
            if not chunk:
                raise EOFError
            code = chunk[0]
            if code == 0x1B:
                raise _ChainEscExit
            if code == 0x03:
                raise KeyboardInterrupt
            if code in (0x0D, 0x0A):
                sys.stdout.write("\r\n")
                sys.stdout.flush()
                break
            if code in (0x7F, 0x08):
                if chars:
                    chars.pop()
                    sys.stdout.write("\b \b")
                    sys.stdout.flush()
                continue
            if code == 0x04 and not chars:
                raise EOFError
            if 0x20 <= code <= 0x7E:
                chars.append(chr(code))
                sys.stdout.write(chr(code))
                sys.stdout.flush()
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return "".join(chars)


def _read_line_windows(prompt: str) -> str:
    """Read one line on Windows, honouring ESC, Ctrl+C and backspace.

    Args:
        prompt: Text printed before reading.

    Returns:
        The typed line without the trailing newline.

    Raises:
        _ChainEscExit: The operator pressed ESC.
        KeyboardInterrupt: The operator pressed Ctrl+C.
        EOFError: End of input with an empty line.
    """
    import msvcrt

    sys.stdout.write(prompt)
    sys.stdout.flush()
    chars: list[str] = []
    while True:
        ch = msvcrt.getwch()
        if ch == "\x1b":
            raise _ChainEscExit
        if ch == "\x03":
            raise KeyboardInterrupt
        if ch in ("\r", "\n"):
            sys.stdout.write("\r\n")
            sys.stdout.flush()
            break
        if ch in ("\x08", "\x7f"):
            if chars:
                chars.pop()
                sys.stdout.write("\b \b")
                sys.stdout.flush()
            continue
        if ch == "\x04" and not chars:
            raise EOFError
        chars.append(ch)
        sys.stdout.write(ch)
        sys.stdout.flush()
    return "".join(chars)

CHAIN_SKIP_VERBS: frozenset[str] = frozenset(
    {
        "help",
        "?",
        "exit",
        "quit",
        "history",
        "shell",
        "dashboard",
        "next",
        ".",
        ",",
        "set",
        "assign",
        "show",
        "palette",
        "palette_k",
        "browse",
        "timeline_browser",
        "form",
        "graph_overlay",
        "toast_clear",
        "edit",
        "run_script",
        "shortcuts",
        "_relative_run",
        "sitrep",
        "ctx",
        "phase",
        "note",
        "l00t",
        "pivot",
        "tasks",
        "scans",
        "wizard",
        "prev",
        "chainmode",
        "recommend_next",
        "suggest_next",
        "explore",
    }
)


@dataclass
class ChainSuggestion:
    """A single next-step proposal, normalised from any resolver output."""

    name: str
    source: str = ""
    reason: str = ""

    @classmethod
    def from_step(cls, step: Any) -> ChainSuggestion:
        """Build a suggestion from a duck-typed resolver step object.

        Args:
            step: Any object exposing ``name``, ``source`` and ``reason``
                attributes (e.g. :class:`cli.command_chain.NextStep`) or a
                plain string.

        Returns:
            A normalised :class:`ChainSuggestion`.
        """
        if isinstance(step, str):
            return cls(name=step)
        return cls(
            name=str(getattr(step, "name", "") or "").strip(),
            source=str(getattr(step, "source", "") or ""),
            reason=str(getattr(step, "reason", "") or ""),
        )


@dataclass(frozen=True)
class ChainOutcome:
    """Result of one chain prompt round.

    Attributes:
        state: One of ``OUTCOME_RUN`` (execute ``command``), ``OUTCOME_SKIP``,
            ``OUTCOME_OFF`` (chain mode disabled) or ``OUTCOME_NONE``
            (no interaction happened).
        command: The command line to execute when state is ``run``. This is
            either the top suggestion, a numbered alternative, or the
            operator's own override.
        reason: Human-readable explanation for the outcome.
    """

    state: str
    command: str = ""
    reason: str = ""


@dataclass
class ChainModeConfig:
    """Centralised configuration for the chain prompt engine."""

    sessions_dir: str = "sessions"
    max_steps: int = MAX_STEPS_DEFAULT
    max_options: int = MAX_OPTIONS_DEFAULT
    enabled_default: bool = False
    skip_verbs: frozenset[str] = field(default_factory=lambda: frozenset(CHAIN_SKIP_VERBS))


class ChainModeStore:
    """Atomic persistence of the chain-mode toggle in the sessions dir."""

    def __init__(self, sessions_dir: str = "sessions") -> None:
        """Store the sessions directory that owns the state file.

        Args:
            sessions_dir: Directory under which ``chain_mode.json`` lives.
        """
        self.path = Path(sessions_dir) / STATE_FILE_NAME

    def load(self) -> bool | None:
        """Return the persisted enabled flag, or ``None`` when unset.

        Returns:
            The stored boolean, or ``None`` when the file is missing or
            malformed.
        """
        try:
            if not self.path.exists():
                return None
            data = json.loads(self.path.read_text(encoding="utf-8"))
            if isinstance(data, dict) and isinstance(data.get("enabled"), bool):
                return bool(data["enabled"])
        except Exception:
            pass
        return None

    def save(self, enabled: bool) -> None:
        """Persist the enabled flag atomically.

        Args:
            enabled: Whether chain mode is currently active.
        """
        try:
            self.path.parent.mkdir(parents=True, exist_ok=True)
            tmp_fd, tmp_name = tempfile.mkstemp(
                dir=str(self.path.parent), prefix=f".{STATE_FILE_NAME}.", suffix=".tmp"
            )
            try:
                with os.fdopen(tmp_fd, "w", encoding="utf-8") as fh:
                    json.dump({"enabled": bool(enabled)}, fh)
                os.replace(tmp_name, str(self.path))
            except Exception:
                try:
                    os.unlink(tmp_name)
                except OSError:
                    pass
                raise
        except Exception:
            pass


class ChainPromptEngine:
    """Coordinate one interactive chain prompt round per executed command."""

    def __init__(
        self,
        config: ChainModeConfig | None = None,
        resolver: Callable[[str, str], Sequence[Any]] | None = None,
        *,
        input_fn: Callable[[str], str] = input,
        print_fn: Callable[[str], None] = print,
        interactive: bool = True,
    ) -> None:
        """Wire the engine with its config, resolver and I/O functions.

        Args:
            config: Centralised configuration. Built from defaults when
                omitted.
            resolver: Callable ``(cmd, phase) -> sequence`` returning
                duck-typed steps with ``name``/``source``/``reason``
                attributes. ``None`` yields no suggestions.
            input_fn: Function used to read one line of operator input.
            print_fn: Function used to render the menu lines.
            interactive: When ``False`` the engine never prompts (used by
                headless/daemon shells so the flow cannot block).
        """
        self.config = config or ChainModeConfig()
        self.resolver = resolver
        self._input_fn = input_fn
        self._print_fn = print_fn
        self._menu_prompt = "  chain> "
        self.interactive = interactive
        self.store = ChainModeStore(self.config.sessions_dir)
        persisted = self.store.load()
        self._enabled = bool(self.config.enabled_default if persisted is None else persisted)
        self._steps_run = 0
        self._paused = False

    @property
    def enabled(self) -> bool:
        """Whether the chain prompt loop is currently active."""
        return self._enabled

    @property
    def steps_run(self) -> int:
        """Number of commands executed through the chain this activation."""
        return self._steps_run

    def set_enabled(self, value: bool, persist: bool = True) -> None:
        """Toggle chain mode and optionally persist the choice.

        Args:
            value: New enabled state.
            persist: When ``True`` write through to the state file.
        """
        self._enabled = bool(value)
        if self._enabled:
            self._steps_run = 0
            self._paused = False
        if persist:
            self.store.save(self._enabled)

    def step(self, last_cmd: str, phase: str = "") -> ChainOutcome:
        """Run one chain prompt round for the command that just executed.

        Args:
            last_cmd: First token (or full line) of the command that just
                ran, used as the resolver seed.
            phase: Current engagement phase (``recon``, ``enum``, ...)
                forwarded to the resolver.

        Returns:
            A :class:`ChainOutcome` describing what the caller should do:
            execute ``command``, skip, or disable chain mode. Returns
            ``OUTCOME_NONE`` without touching stdin when the engine is
            disabled, non-interactive, the verb is in ``skip_verbs`` or
            the auto-pause limit was reached.
        """
        if not self._enabled or not self.interactive:
            return ChainOutcome(OUTCOME_NONE)
        if self._paused:
            self.set_enabled(False, persist=False)
            return ChainOutcome(
                OUTCOME_OFF,
                reason=f"chainmode paused after {self._steps_run} chained steps — "
                "run 'chainmode on' to resume",
            )
        verb = (last_cmd or "").strip().split()[0] if last_cmd else ""
        if verb in self.config.skip_verbs:
            return ChainOutcome(OUTCOME_NONE)
        suggestions = self._suggest(verb, phase)
        self._render_menu(verb, suggestions)
        try:
            raw = self._prompt_line().strip()
        except _ChainEscExit:
            return self._disable("chainmode off — exited with ESC")
        except KeyboardInterrupt:
            return self._disable("chainmode off — interrupted")
        except EOFError:
            return self._disable("chainmode off — end of input")
        return self._interpret(raw, suggestions)

    def _prompt_line(self) -> str:
        """Read one chain-prompt line with ESC/Ctrl+C support on real TTYs.

        Uses the raw terminal readers when stdin is an interactive TTY so
        ESC and Ctrl+C work without pressing Enter. Falls back to the
        injected ``input_fn`` (tests, pipes) or the builtin ``input`` for
        non-TTY interactive streams.

        Returns:
            The operator's line, or raises ``_ChainEscExit`` /
            ``KeyboardInterrupt`` / ``EOFError``.
        """
        if self.interactive:
            try:
                if sys.stdin.isatty():
                    if os.name == "nt":
                        return _read_line_windows(self._menu_prompt)
                    return _read_line_unix(self._menu_prompt)
            except (ImportError, OSError):
                pass
        return self._input_fn(self._menu_prompt)

    def _suggest(self, verb: str, phase: str) -> list[ChainSuggestion]:
        if self.resolver is None:
            return []
        try:
            steps = self.resolver(verb, phase) or []
        except Exception:
            return []
        suggestions: list[ChainSuggestion] = []
        seen: set[str] = set()
        for step in steps:
            suggestion = ChainSuggestion.from_step(step)
            if not suggestion.name or suggestion.name in seen:
                continue
            seen.add(suggestion.name)
            suggestions.append(suggestion)
        return suggestions[: self.config.max_options]

    def _render_menu(self, verb: str, suggestions: list[ChainSuggestion]) -> None:
        label = verb or "the engagement"
        self._print_fn("    " + "\u2500" * 8 + " chain " + "\u2500" * 8)
        if not suggestions:
            self._print_fn(
                f"  chain: no suggestions after '{label}' — type any command to "
                "keep chaining, Enter or 'skip' to continue manually, ESC/exit to leave"
            )
            return
        self._print_fn(f"  chain: {len(suggestions)} next step(s) after '{label}':")
        for index, suggestion in enumerate(suggestions, start=1):
            tail = f"  [{suggestion.source}] {suggestion.reason}" if suggestion.source else ""
            self._print_fn(f"    [{index}] {suggestion.name}{tail}")
        self._print_fn(
            "  chain> [Enter=1] [1-N] [skip] [ESC/Ctrl-C/exit/quit = leave]"
            " — or type any command to override"
        )

    def _interpret(self, raw: str, suggestions: list[ChainSuggestion]) -> ChainOutcome:
        lowered = raw.lower()
        if lowered in EXIT_WORDS:
            return self._disable("chainmode off")
        if lowered in SKIP_WORDS:
            return ChainOutcome(OUTCOME_SKIP)
        if not raw:
            if not suggestions:
                return ChainOutcome(OUTCOME_SKIP)
            return self._run(suggestions[0].name)
        if raw.isdigit():
            index = int(raw) - 1
            if 0 <= index < len(suggestions):
                return self._run(suggestions[index].name)
            self._print_fn(f"    no option {raw} — run 'skip' or pick 1-{len(suggestions)}")
            return ChainOutcome(OUTCOME_SKIP)
        return self._run(raw)

    def _run(self, command: str) -> ChainOutcome:
        self._steps_run += 1
        if self._steps_run >= self.config.max_steps:
            self._paused = True
        return ChainOutcome(OUTCOME_RUN, command=command.strip())

    def _disable(self, reason: str) -> ChainOutcome:
        self.set_enabled(False, persist=True)
        return ChainOutcome(OUTCOME_OFF, reason=reason)


__all__ = [
    "CHAIN_SKIP_VERBS",
    "ChainModeConfig",
    "ChainModeStore",
    "ChainOutcome",
    "ChainPromptEngine",
    "ChainSuggestion",
    "EXIT_WORDS",
    "LOOP_GUARD_MARGIN",
    "MAX_STEPS_DEFAULT",
    "OUTCOME_NONE",
    "OUTCOME_OFF",
    "OUTCOME_RUN",
    "OUTCOME_SKIP",
    "SKIP_WORDS",
]
