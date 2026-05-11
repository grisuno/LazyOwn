"""Curses-based fuzzy dropdown picker for the LazyOwn interactive shell.

This module is self-contained: it ships a ``PickerConfig`` with every tunable
constant, a pure scoring primitive, a curses view, an orchestrator that wires
them together, and a thin readline bridge that installs the picker into a
``cmd2`` shell as the Tab-completion display handler.

The module follows SOLID:

- ``PickerConfig`` centralises every magic value (colors, key codes,
  geometry, glyphs) so callers can override without touching the core.
- ``MatchScorer`` is the only place that knows how to rank a candidate
  against a query (Strategy / Single Responsibility).
- ``PickerView`` is an abstract base class; ``CursesPickerView`` is the only
  concrete realisation but tests can substitute a fake without touching
  curses (Dependency Inversion / Liskov).
- ``FuzzyPicker`` orchestrates scorer + view and exposes a small surface.
- ``ReadlineBridge`` is the integration adaptor with the GNU readline
  display hook contract; it never imports cmd2.
- ``install_fuzzy_completion`` is the only public entry point cmd2 callers
  should use.

The picker is invoked on a single Tab press whenever readline reports two or
more candidate completions. With a single candidate, readline's default
behaviour is preserved (auto-insert). The picker honours arrow navigation,
Tab/Enter for selection, Escape/Ctrl-C/Ctrl-G for cancel, and Backspace to
edit the query in-place. Selection is injected back into the readline buffer
through ``readline.insert_text`` so the rest of the framework sees the same
final input string it would have seen with a normal completion.

The picker degrades gracefully when curses cannot initialise (e.g. dumb
terminal, no TTY, no color support) by returning ``None`` and letting
readline's default display take over.
"""

from __future__ import annotations

import curses
import os
import re
import sys
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from difflib import SequenceMatcher
from typing import Callable, Sequence


@dataclass(frozen=True)
class PickerConfig:
    """Centralised constants for the fuzzy picker.

    Every magic number / glyph / key code lives here so that operators or
    tests can override behaviour without editing the picker core. Instances
    are frozen to keep the configuration value-semantics-safe.
    """

    max_visible_rows: int = 12
    min_visible_rows: int = 3
    column_gap: int = 2
    description_max_width: int = 80
    name_max_width: int = 32
    box_padding_x: int = 1
    header_height: int = 1
    footer_height: int = 1

    glyph_top_left: str = "╔"
    glyph_top_right: str = "╗"
    glyph_bottom_left: str = "╚"
    glyph_bottom_right: str = "╝"
    glyph_horizontal: str = "═"
    glyph_vertical: str = "║"
    glyph_pointer: str = "➜"
    glyph_match_marker: str = "▸"
    glyph_arrow_up: str = "▲"
    glyph_arrow_down: str = "▼"

    header_label: str = "LazyOwn fuzzy completion"
    footer_help: str = "[↑/↓] move  [Tab/Enter] select  [Esc] cancel  [Bksp] edit"
    no_matches_label: str = "no matches"

    color_pair_border: int = 1
    color_pair_header: int = 2
    color_pair_footer: int = 3
    color_pair_item: int = 4
    color_pair_selected: int = 5
    color_pair_highlight: int = 6
    color_pair_description: int = 7

    color_border_fg: int = curses.COLOR_CYAN
    color_header_fg: int = curses.COLOR_GREEN
    color_footer_fg: int = curses.COLOR_YELLOW
    color_item_fg: int = curses.COLOR_WHITE
    color_selected_fg: int = curses.COLOR_BLACK
    color_selected_bg: int = curses.COLOR_GREEN
    color_highlight_fg: int = curses.COLOR_MAGENTA
    color_description_fg: int = curses.COLOR_BLUE

    key_tab: int = 9
    key_enter: int = 10
    key_carriage_return: int = 13
    key_escape: int = 27
    key_ctrl_c: int = 3
    key_ctrl_g: int = 7

    score_exact: float = 1.0
    score_prefix: float = 0.9
    score_subsequence: float = 0.7
    score_substring: float = 0.6
    score_similarity_weight: float = 0.55
    score_similarity_floor: float = 0.4
    score_zero: float = 0.0

    activation_threshold: int = 2

    @classmethod
    def from_payload(cls, payload: dict | None) -> "PickerConfig":
        """Build a config from a payload.json view, falling back to defaults.

        Honours an optional ``fuzzy_picker`` mapping inside ``payload.json``
        so operators can pin the picker geometry without code changes. Any
        unknown key is ignored.
        """
        if not payload:
            return cls()
        block = payload.get("fuzzy_picker") or {}
        if not isinstance(block, dict):
            return cls()
        valid_fields = {f.name for f in cls.__dataclass_fields__.values()}
        overrides = {k: v for k, v in block.items() if k in valid_fields}
        if not overrides:
            return cls()
        try:
            return cls(**overrides)
        except TypeError:
            return cls()


@dataclass(frozen=True)
class PickerItem:
    """Single candidate displayed in the picker.

    ``text`` is the value inserted into the readline buffer on selection.
    ``description`` is an optional secondary string rendered to the right of
    the name; it never participates in matching.
    """

    text: str
    description: str = ""


@dataclass(frozen=True)
class ScoredItem:
    """A picker item paired with a relevance score and matched positions."""

    item: PickerItem
    score: float
    positions: tuple[int, ...] = ()


class MatchScorer:
    """Score and rank candidates against a query.

    The scorer prefers exact and prefix matches, then ordered-subsequence
    matches (the classic fuzzy-finder behaviour), then substring matches,
    then ``difflib`` similarity as a graceful floor. Positions of matched
    characters are exposed for in-line highlighting in the view.
    """

    def __init__(self, config: PickerConfig) -> None:
        self._cfg = config

    def rank(self, items: Sequence[PickerItem], query: str) -> list[ScoredItem]:
        """Return ``items`` ranked by descending relevance against ``query``.

        An empty query yields every input ranked by its position in the
        original sequence so the operator sees a stable list.
        """
        q = (query or "").lower()
        if not q:
            return [
                ScoredItem(item=it, score=self._cfg.score_exact, positions=())
                for it in items
            ]
        scored: list[ScoredItem] = []
        for it in items:
            score, positions = self._score(it.text.lower(), q)
            if score > self._cfg.score_zero:
                scored.append(ScoredItem(item=it, score=score, positions=positions))
        scored.sort(key=lambda s: (-s.score, s.item.text))
        return scored

    def _score(self, haystack: str, query: str) -> tuple[float, tuple[int, ...]]:
        if not haystack:
            return self._cfg.score_zero, ()
        if haystack == query:
            return self._cfg.score_exact, tuple(range(len(query)))
        if haystack.startswith(query):
            return self._cfg.score_prefix, tuple(range(len(query)))
        positions = self._subsequence_positions(haystack, query)
        if positions:
            return self._cfg.score_subsequence, positions
        idx = haystack.find(query)
        if idx >= 0:
            return self._cfg.score_substring, tuple(range(idx, idx + len(query)))
        similarity = SequenceMatcher(None, haystack, query).ratio()
        if similarity >= self._cfg.score_similarity_floor:
            return similarity * self._cfg.score_similarity_weight, ()
        return self._cfg.score_zero, ()

    @staticmethod
    def _subsequence_positions(haystack: str, query: str) -> tuple[int, ...]:
        positions: list[int] = []
        cursor = 0
        for char in query:
            found = haystack.find(char, cursor)
            if found < 0:
                return ()
            positions.append(found)
            cursor = found + 1
        return tuple(positions)


class PickerView(ABC):
    """Abstract view contract for a fuzzy picker.

    Returning ``None`` signals the user cancelled the picker. Returning a
    string is the selected ``PickerItem.text`` to be injected into readline.
    Tests can substitute a deterministic fake view to drive integration
    scenarios.
    """

    @abstractmethod
    def run(self, items: Sequence[PickerItem], initial_query: str) -> str | None: ...


class CursesPickerView(PickerView):
    """Curses-driven implementation of :class:`PickerView`.

    The view paints a bordered dropdown anchored to the cursor location and
    consumes keystrokes until the user selects an entry or cancels. All
    layout values come from :class:`PickerConfig` so the geometry can be
    retuned by operators without source edits.
    """

    def __init__(self, config: PickerConfig, scorer: MatchScorer) -> None:
        self._cfg = config
        self._scorer = scorer

    def run(self, items: Sequence[PickerItem], initial_query: str) -> str | None:
        if not items:
            return None
        if not self._tty_available():
            return None
        try:
            return curses.wrapper(self._event_loop, list(items), initial_query)
        except curses.error:
            return None
        except KeyboardInterrupt:
            return None

    @staticmethod
    def _tty_available() -> bool:
        return (
            sys.stdin.isatty()
            and sys.stdout.isatty()
            and os.environ.get("TERM", "") not in {"", "dumb"}
        )

    def _init_colors(self) -> None:
        if not curses.has_colors():
            return
        try:
            curses.start_color()
            curses.use_default_colors()
        except curses.error:
            return
        default_bg = -1
        pairs = (
            (self._cfg.color_pair_border, self._cfg.color_border_fg, default_bg),
            (self._cfg.color_pair_header, self._cfg.color_header_fg, default_bg),
            (self._cfg.color_pair_footer, self._cfg.color_footer_fg, default_bg),
            (self._cfg.color_pair_item, self._cfg.color_item_fg, default_bg),
            (self._cfg.color_pair_selected, self._cfg.color_selected_fg, self._cfg.color_selected_bg),
            (self._cfg.color_pair_highlight, self._cfg.color_highlight_fg, default_bg),
            (self._cfg.color_pair_description, self._cfg.color_description_fg, default_bg),
        )
        for pair_id, fg, bg in pairs:
            try:
                curses.init_pair(pair_id, fg, bg)
            except curses.error:
                continue

    def _event_loop(self, stdscr: "curses._CursesWindow", items: list[PickerItem], initial_query: str) -> str | None:
        curses.curs_set(0)
        stdscr.keypad(True)
        self._init_colors()
        query = initial_query or ""
        cursor_index = 0
        scroll_offset = 0
        while True:
            ranked = self._scorer.rank(items, query)
            if not ranked:
                self._render_empty(stdscr, query)
                key = stdscr.getch()
                action = self._classify_key(key)
                if action == "cancel":
                    return None
                if action == "select":
                    return None
                if action == "backspace" and query:
                    query = query[:-1]
                elif action == "char":
                    query += chr(key)
                continue
            cursor_index = min(cursor_index, len(ranked) - 1)
            scroll_offset = self._clamp_scroll(scroll_offset, cursor_index, len(ranked))
            self._render(stdscr, ranked, query, cursor_index, scroll_offset)
            key = stdscr.getch()
            action = self._classify_key(key)
            if action == "cancel":
                return None
            if action == "select":
                return ranked[cursor_index].item.text
            if action == "up":
                cursor_index = max(0, cursor_index - 1)
            elif action == "down":
                cursor_index = min(len(ranked) - 1, cursor_index + 1)
            elif action == "page_up":
                cursor_index = max(0, cursor_index - self._visible_rows())
            elif action == "page_down":
                cursor_index = min(len(ranked) - 1, cursor_index + self._visible_rows())
            elif action == "home":
                cursor_index = 0
            elif action == "end":
                cursor_index = len(ranked) - 1
            elif action == "backspace" and query:
                query = query[:-1]
                cursor_index = 0
            elif action == "char":
                query += chr(key)
                cursor_index = 0

    def _classify_key(self, key: int) -> str:
        cfg = self._cfg
        if key in (cfg.key_escape, cfg.key_ctrl_c, cfg.key_ctrl_g):
            return "cancel"
        if key in (cfg.key_tab, cfg.key_enter, cfg.key_carriage_return, curses.KEY_ENTER):
            return "select"
        if key == curses.KEY_UP:
            return "up"
        if key == curses.KEY_DOWN:
            return "down"
        if key in (curses.KEY_PPAGE,):
            return "page_up"
        if key in (curses.KEY_NPAGE,):
            return "page_down"
        if key == curses.KEY_HOME:
            return "home"
        if key == curses.KEY_END:
            return "end"
        if key in (curses.KEY_BACKSPACE, 127, 8):
            return "backspace"
        if 32 <= key <= 126:
            return "char"
        return "noop"

    def _visible_rows(self) -> int:
        return max(self._cfg.min_visible_rows, self._cfg.max_visible_rows)

    def _clamp_scroll(self, offset: int, cursor: int, total: int) -> int:
        visible = self._visible_rows()
        if cursor < offset:
            return cursor
        if cursor >= offset + visible:
            return cursor - visible + 1
        if offset + visible > total:
            return max(0, total - visible)
        return offset

    def _layout(self, stdscr: "curses._CursesWindow", row_count: int) -> tuple[int, int, int, int]:
        max_h, max_w = stdscr.getmaxyx()
        visible = min(max(self._cfg.min_visible_rows, row_count), self._cfg.max_visible_rows)
        height = visible + self._cfg.header_height + self._cfg.footer_height + 2
        height = min(height, max_h)
        width = min(max_w, self._cfg.name_max_width + self._cfg.description_max_width + self._cfg.column_gap + 4)
        width = max(width, len(self._cfg.footer_help) + 4, len(self._cfg.header_label) + 4)
        width = min(width, max_w)
        top = max(0, max_h - height)
        left = 0
        return top, left, height, width

    def _render_empty(self, stdscr: "curses._CursesWindow", query: str) -> None:
        top, left, height, width = self._layout(stdscr, 1)
        stdscr.erase()
        self._draw_box(stdscr, top, left, height, width)
        self._draw_header(stdscr, top, left, width, query, 0, 0)
        text = self._cfg.no_matches_label
        try:
            stdscr.addnstr(
                top + self._cfg.header_height + 1,
                left + self._cfg.box_padding_x + 1,
                text,
                width - 2 - self._cfg.box_padding_x,
                self._color(self._cfg.color_pair_item),
            )
        except curses.error:
            pass
        self._draw_footer(stdscr, top + height - self._cfg.footer_height - 1, left, width)
        stdscr.refresh()

    def _render(
        self,
        stdscr: "curses._CursesWindow",
        ranked: list[ScoredItem],
        query: str,
        cursor_index: int,
        scroll_offset: int,
    ) -> None:
        top, left, height, width = self._layout(stdscr, len(ranked))
        stdscr.erase()
        self._draw_box(stdscr, top, left, height, width)
        self._draw_header(stdscr, top, left, width, query, len(ranked), cursor_index + 1)
        visible = min(
            self._cfg.max_visible_rows,
            max(self._cfg.min_visible_rows, height - self._cfg.header_height - self._cfg.footer_height - 2),
        )
        end = min(len(ranked), scroll_offset + visible)
        for row_index, scored_index in enumerate(range(scroll_offset, end)):
            row_y = top + self._cfg.header_height + 1 + row_index
            self._draw_item(
                stdscr,
                row_y,
                left,
                width,
                ranked[scored_index],
                scored_index == cursor_index,
            )
        self._draw_footer(stdscr, top + height - self._cfg.footer_height - 1, left, width)
        stdscr.refresh()

    def _draw_box(self, stdscr: "curses._CursesWindow", top: int, left: int, height: int, width: int) -> None:
        attr = self._color(self._cfg.color_pair_border)
        cfg = self._cfg
        horizontal = cfg.glyph_horizontal * (width - 2)
        try:
            stdscr.addnstr(top, left, cfg.glyph_top_left + horizontal + cfg.glyph_top_right, width, attr)
            for y in range(top + 1, top + height - 1):
                stdscr.addnstr(y, left, cfg.glyph_vertical, 1, attr)
                stdscr.addnstr(y, left + width - 1, cfg.glyph_vertical, 1, attr)
            stdscr.addnstr(top + height - 1, left, cfg.glyph_bottom_left + horizontal + cfg.glyph_bottom_right, width, attr)
        except curses.error:
            pass

    def _draw_header(
        self,
        stdscr: "curses._CursesWindow",
        top: int,
        left: int,
        width: int,
        query: str,
        total: int,
        selected: int,
    ) -> None:
        attr = self._color(self._cfg.color_pair_header) | curses.A_BOLD
        label = f"{self._cfg.header_label}  [{selected}/{total}]  query: {query or ''}"
        try:
            stdscr.addnstr(top + 1, left + self._cfg.box_padding_x + 1, label, width - 2 - self._cfg.box_padding_x, attr)
        except curses.error:
            pass

    def _draw_footer(self, stdscr: "curses._CursesWindow", row_y: int, left: int, width: int) -> None:
        attr = self._color(self._cfg.color_pair_footer)
        try:
            stdscr.addnstr(row_y, left + self._cfg.box_padding_x + 1, self._cfg.footer_help, width - 2 - self._cfg.box_padding_x, attr)
        except curses.error:
            pass

    def _draw_item(
        self,
        stdscr: "curses._CursesWindow",
        row_y: int,
        left: int,
        width: int,
        scored: ScoredItem,
        selected: bool,
    ) -> None:
        cfg = self._cfg
        text = scored.item.text
        description = scored.item.description
        base_attr = self._color(cfg.color_pair_selected) if selected else self._color(cfg.color_pair_item)
        marker = cfg.glyph_match_marker if selected else " "
        prefix = f"{marker} "
        try:
            stdscr.addnstr(row_y, left + cfg.box_padding_x + 1, " " * (width - 2 - cfg.box_padding_x), width - 2 - cfg.box_padding_x, base_attr)
            stdscr.addnstr(row_y, left + cfg.box_padding_x + 1, prefix, width - 2 - cfg.box_padding_x, base_attr)
            self._draw_highlighted(stdscr, row_y, left + cfg.box_padding_x + 1 + len(prefix), text, scored.positions, base_attr, selected)
            if description:
                desc_x = left + cfg.box_padding_x + 1 + len(prefix) + cfg.name_max_width + cfg.column_gap
                desc_attr = base_attr if selected else self._color(cfg.color_pair_description)
                stdscr.addnstr(row_y, desc_x, description, width - desc_x - 2, desc_attr)
        except curses.error:
            pass

    def _draw_highlighted(
        self,
        stdscr: "curses._CursesWindow",
        row_y: int,
        start_x: int,
        text: str,
        positions: tuple[int, ...],
        base_attr: int,
        selected: bool,
    ) -> None:
        cfg = self._cfg
        pos_set = set(positions)
        clipped = text[: cfg.name_max_width]
        x = start_x
        highlight_attr = (
            base_attr
            if selected
            else self._color(cfg.color_pair_highlight) | curses.A_BOLD
        )
        for index, char in enumerate(clipped):
            attr = highlight_attr if index in pos_set else base_attr
            try:
                stdscr.addnstr(row_y, x, char, 1, attr)
            except curses.error:
                return
            x += 1

    def _color(self, pair_id: int) -> int:
        if not curses.has_colors():
            return curses.A_NORMAL
        try:
            return curses.color_pair(pair_id)
        except curses.error:
            return curses.A_NORMAL


class FuzzyPicker:
    """Top-level orchestrator binding a scorer to a view."""

    def __init__(self, config: PickerConfig | None = None, view_factory: Callable[[PickerConfig, MatchScorer], PickerView] | None = None) -> None:
        self._cfg = config or PickerConfig()
        self._scorer = MatchScorer(self._cfg)
        factory = view_factory or (lambda cfg, scorer: CursesPickerView(cfg, scorer))
        self._view = factory(self._cfg, self._scorer)

    @property
    def config(self) -> PickerConfig:
        return self._cfg

    def pick(self, items: Sequence[PickerItem], initial_query: str = "") -> str | None:
        """Return the selected item text or ``None`` on cancel / empty input.

        When there are fewer items than ``activation_threshold`` the picker
        short-circuits to the single value, preserving readline's normal
        single-match auto-insertion semantics for callers that route every
        match through the picker.
        """
        if not items:
            return None
        if len(items) < self._cfg.activation_threshold:
            return items[0].text
        return self._view.run(items, initial_query)


class ReadlineBridge:
    """Bridge a :class:`FuzzyPicker` into GNU readline's display hook.

    The bridge is the single place that touches the ``readline`` module so
    that the rest of the picker code remains testable without a terminal.
    Installation is idempotent: calling :py:meth:`install` twice replaces
    any previously installed hook, which keeps a single live picker per
    shell process.
    """

    _ANSI_RE = re.compile(r"\x1b\[[0-9;?]*[a-zA-Z]")

    def __init__(self, picker: FuzzyPicker) -> None:
        self._picker = picker

    def install(self) -> None:
        """Wire the picker into ``readline.set_completion_display_matches_hook``."""
        try:
            import readline
        except ImportError:
            return
        readline.set_completion_display_matches_hook(self._on_display_matches)

    def uninstall(self) -> None:
        """Remove the readline display hook installed by :py:meth:`install`."""
        try:
            import readline
        except ImportError:
            return
        readline.set_completion_display_matches_hook(None)

    def _on_display_matches(self, substitution: str, matches: Sequence[str], longest_match_length: int) -> None:
        try:
            import readline
        except ImportError:
            return
        normalised = [self._strip_ansi(m) for m in matches if m]
        if not normalised:
            return
        items = [PickerItem(text=text) for text in normalised]
        chosen = self._picker.pick(items, initial_query=substitution or "")
        if not chosen:
            self._redraw_prompt()
            return
        remainder = chosen[len(substitution) :] if chosen.startswith(substitution) else chosen
        try:
            readline.insert_text(remainder)
            readline.redisplay()
        except Exception:
            self._redraw_prompt()

    @classmethod
    def _strip_ansi(cls, value: str) -> str:
        return cls._ANSI_RE.sub("", value)

    @staticmethod
    def _redraw_prompt() -> None:
        try:
            import readline
            readline.redisplay()
        except Exception:
            pass


def install_fuzzy_completion(
    shell: object,
    payload: dict | None = None,
    config: PickerConfig | None = None,
) -> ReadlineBridge | None:
    """Install the fuzzy picker into a cmd2 shell.

    The function is the single public entry point used by ``lazyown.py``.
    Returns the live :class:`ReadlineBridge` so the caller can later
    uninstall the hook (useful in tests). Returns ``None`` when running in
    a non-interactive environment where readline is unavailable.
    """
    try:
        import readline  # noqa: F401
    except ImportError:
        return None
    resolved_config = config or PickerConfig.from_payload(payload)
    picker = FuzzyPicker(config=resolved_config)
    bridge = ReadlineBridge(picker)
    bridge.install()
    setattr(shell, "_fuzzy_bridge", bridge)
    setattr(shell, "_fuzzy_picker", picker)
    return bridge


__all__ = [
    "CursesPickerView",
    "FuzzyPicker",
    "MatchScorer",
    "PickerConfig",
    "PickerItem",
    "PickerView",
    "ReadlineBridge",
    "ScoredItem",
    "install_fuzzy_completion",
]
