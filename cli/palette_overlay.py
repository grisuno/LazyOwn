"""Textual Cmd-K palette overlay for the LazyOwn shell.

The overlay is a modal command launcher: the operator presses a single
hotkey, types a fuzzy query against every ``do_*`` command, picks one
with the arrow keys and gets the verb echoed back to the shell. It shares
the index, filtering and ranking logic with the existing
``cli.palette_command`` and ``cli.palette_telemetry`` modules so the C2
``/palette`` view, the MCP ``lazyown_palette`` tool and the CLI overlay
always agree on what is searchable.

Design (SOLID):

- Single Responsibility: :class:`PaletteOverlayConfig` owns constants,
  :class:`PaletteOverlayState` performs filtering and ranking,
  :class:`PaletteOverlayApp` (Textual) renders. The launcher
  :func:`launch_overlay` wires them together and returns the selected
  command name.
- Dependency Inversion: the state takes an already-loaded index and the
  recents list so tests never have to touch the filesystem.
- Open/Closed: ranking strategies live behind a method that subclasses
  can override; the default ranks by recency boost + substring match.
- No magic numbers/paths: every limit and label lives in the config.
- Textual is imported lazily so importing this module on a host without
  Textual does not error — the launcher returns ``None`` instead.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable, Mapping, Sequence

from cli.palette_command import PaletteIndexQuery
from cli.themes import Theme, theme_from_payload


@dataclass(frozen=True)
class PaletteOverlayConfig:
    """Centralised constants for the overlay."""

    title: str = "Command palette"
    subtitle: str = "Type to filter, Enter to select, Esc to cancel"
    input_placeholder: str = "Search commands and summaries"
    recents_section_label: str = "Recent"
    results_section_label: str = "Results"
    empty_message: str = "No commands match the current filter."
    max_rows: int = 30
    summary_max_chars: int = 80
    name_min_width: int = 12
    truncation_suffix: str = "..."
    recents_boost: float = 0.5
    exact_match_boost: float = 1.0
    prefix_match_boost: float = 0.75
    substring_match_boost: float = 0.25
    payload_theme_key: str = "tui_theme"


@dataclass(frozen=True)
class PaletteRow:
    """Immutable row produced by :class:`PaletteOverlayState`."""

    name: str
    phase: str
    summary: str
    score: float
    is_recent: bool


@dataclass
class PaletteOverlayState:
    """Pure data layer for the overlay.

    The state owns the loaded command index, the recents list and the
    current query string. It exposes :meth:`rows` which returns the
    deterministic, ranked list of :class:`PaletteRow` for rendering.
    """

    config: PaletteOverlayConfig
    index: Mapping[str, Any]
    recents: Sequence[str] = field(default_factory=tuple)
    query: str = ""

    def set_query(self, value: str) -> None:
        """Replace the active query with ``value`` (trimmed)."""
        self.query = (value or "").strip()

    def rows(self) -> list[PaletteRow]:
        """Return the ranked, truncated rows for the current query."""
        cfg = self.config
        commands = PaletteIndexQuery(self.index).commands
        recents_set = {name for name in self.recents if isinstance(name, str)}
        scored: list[PaletteRow] = []
        needle = self.query.lower()
        for entry in commands:
            name = str(entry.get("name", ""))
            summary = self._truncate(str(entry.get("summary", "")), cfg.summary_max_chars)
            phase = str(entry.get("phase", ""))
            score = self._score(name, summary, needle, name in recents_set)
            if needle and score <= 0:
                continue
            scored.append(
                PaletteRow(
                    name=name,
                    phase=phase,
                    summary=summary,
                    score=score,
                    is_recent=name in recents_set,
                )
            )
        scored.sort(key=lambda row: (-row.score, row.name))
        return scored[: cfg.max_rows]

    def _score(self, name: str, summary: str, needle: str, is_recent: bool) -> float:
        cfg = self.config
        bonus = cfg.recents_boost if is_recent else 0.0
        if not needle:
            return bonus + 1.0
        haystack_name = name.lower()
        haystack_summary = summary.lower()
        if haystack_name == needle:
            return cfg.exact_match_boost + bonus + 1.0
        if haystack_name.startswith(needle):
            return cfg.prefix_match_boost + bonus + 1.0
        if needle in haystack_name:
            return cfg.substring_match_boost + bonus + 1.0
        if needle in haystack_summary:
            return cfg.substring_match_boost / 2.0 + bonus
        return 0.0

    def _truncate(self, value: str, max_chars: int) -> str:
        if len(value) <= max_chars:
            return value
        keep = max(1, max_chars - len(self.config.truncation_suffix))
        return value[:keep] + self.config.truncation_suffix


def _load_recents() -> tuple[str, ...]:
    """Return the operator's most-recent command names or an empty tuple."""
    try:
        from cli.palette_telemetry import recents, safe_load_telemetry
    except Exception:
        return tuple()
    telemetry = safe_load_telemetry()
    if telemetry is None:
        return tuple()
    try:
        return tuple(recents(telemetry))
    except Exception:
        return tuple()


def _load_index() -> Mapping[str, Any] | None:
    try:
        from cli.palette import load_index
    except Exception:
        return None
    try:
        return load_index()
    except Exception:
        return None


def build_state(
    payload: Mapping[str, Any] | None = None,
    index: Mapping[str, Any] | None = None,
    recents: Sequence[str] | None = None,
    config: PaletteOverlayConfig | None = None,
) -> PaletteOverlayState | None:
    """Wire the canonical state used by :func:`launch_overlay`.

    Args:
        payload: Loaded ``payload.json`` (only used to pick the theme).
        index: Optional pre-loaded command index (tests inject one).
        recents: Optional pre-loaded recents list.
        config: Optional override for the overlay configuration.

    Returns:
        A ready-to-use :class:`PaletteOverlayState`, or ``None`` when the
        command index is unavailable.
    """
    cfg = config or PaletteOverlayConfig()
    idx = index if index is not None else _load_index()
    if idx is None:
        return None
    rec = tuple(recents) if recents is not None else _load_recents()
    return PaletteOverlayState(config=cfg, index=idx, recents=rec)


def launch_overlay(
    payload: Mapping[str, Any] | None = None,
    state: PaletteOverlayState | None = None,
    runner: Callable[[Any], str | None] | None = None,
) -> str | None:
    """Open the Textual overlay and return the selected command verb.

    Args:
        payload: Loaded ``payload.json``; used to pick the theme.
        state: Optional pre-built state (tests inject one).
        runner: Optional callable that takes the Textual app and returns
            the selected command name. Tests substitute a no-Textual
            runner; production passes ``None`` and the function falls
            back to ``app.run()``.

    Returns:
        The chosen command name (``do_<verb>`` form preserved) or
        ``None`` when the overlay was cancelled or could not be opened.
    """
    chosen_state = state if state is not None else build_state(payload)
    if chosen_state is None:
        return None
    theme = theme_from_payload(payload)
    if runner is not None:
        return runner({"state": chosen_state, "theme": theme})
    try:
        app = _build_app(chosen_state, theme)
    except RuntimeError:
        return None
    if app is None:
        return None
    try:
        result = app.run()
    except Exception:
        return None
    if isinstance(result, str) and result:
        return result
    return None


def _build_app(state: PaletteOverlayState, theme: Theme) -> Any | None:
    """Construct the Textual app lazily; return ``None`` when unavailable."""
    try:
        from textual.app import App, ComposeResult
        from textual.binding import Binding
        from textual.containers import Vertical
        from textual.widgets import Footer, Header, Input, ListItem, ListView, Static
    except Exception:
        return None

    cfg = state.config

    class _PaletteOverlayApp(App):
        TITLE = cfg.title
        SUB_TITLE = cfg.subtitle
        BINDINGS = [
            Binding("escape", "cancel", "Cancel"),
            Binding("enter", "select_current", "Select", show=False),
        ]
        CSS = (
            "Screen { align: center middle; }\n"
            "#palette-root { width: 80%; height: 80%; border: round $primary; padding: 1 2; }\n"
            "#palette-input { dock: top; }\n"
            "#palette-status { dock: bottom; color: $text-muted; }\n"
            "#palette-list { height: 1fr; }\n"
        )

        def __init__(self) -> None:
            super().__init__()
            self._state = state
            self._theme = theme
            self._selected: str | None = None

        def compose(self) -> ComposeResult:
            yield Header()
            with Vertical(id="palette-root"):
                yield Input(placeholder=cfg.input_placeholder, id="palette-input")
                yield ListView(id="palette-list")
                yield Static("", id="palette-status")
            yield Footer()

        def on_mount(self) -> None:
            self._refresh_rows()

        def on_input_changed(self, event: Input.Changed) -> None:
            self._state.set_query(event.value)
            self._refresh_rows()

        def on_input_submitted(self, event: Input.Submitted) -> None:
            self.action_select_current()

        def on_list_view_selected(self, event: ListView.Selected) -> None:
            self._commit_from_item(event.item)

        def action_cancel(self) -> None:
            self.exit()

        def action_select_current(self) -> None:
            list_view = self.query_one("#palette-list", ListView)
            if not list_view.children:
                return
            item = list_view.highlighted_child
            self._commit_from_item(item)

        def _commit_from_item(self, item: Any | None) -> None:
            if item is None:
                return
            name = getattr(item, "command_name", None)
            if isinstance(name, str) and name:
                self._selected = name
                self.exit(result=name)

        def _refresh_rows(self) -> None:
            list_view = self.query_one("#palette-list", ListView)
            list_view.clear()
            rows = self._state.rows()
            status = self.query_one("#palette-status", Static)
            if not rows:
                status.update(cfg.empty_message)
                return
            status.update(f"{len(rows)} command(s)")
            for row in rows:
                item = ListItem(Static(self._format_row(row)))
                item.command_name = row.name
                list_view.append(item)

        def _format_row(self, row: PaletteRow) -> str:
            marker = "*" if row.is_recent else " "
            phase = row.phase or "-"
            name = row.name.ljust(cfg.name_min_width)
            return f"{marker} {phase:<10} {name}  {row.summary}"

    return _PaletteOverlayApp()


__all__ = [
    "PaletteOverlayConfig",
    "PaletteOverlayState",
    "PaletteRow",
    "build_state",
    "launch_overlay",
]
