"""Textual scrubber over ``sessions/LazyOwn_session_report.csv``.

The session report is a CSV that every command appends to. The scrubber
turns it into a paginated, searchable, key-driven view so the operator
can replay decisions, jump to artefacts and answer questions like "what
was the gobuster command we ran last week?" without leaving the shell.

Design (SOLID):

- Single Responsibility: :class:`TimelineConfig` owns constants,
  :class:`TimelineEntry` is the immutable row, :class:`TimelineReader`
  loads CSV rows lazily, :class:`TimelineState` slices and filters,
  :class:`TimelineBrowserApp` renders.
- Open/Closed: a new column is one tuple entry in
  :attr:`TimelineConfig.columns`.
- Dependency Inversion: the app is always built from a
  :class:`TimelineState` so tests bypass Textual entirely.
- No magic numbers / hardcoded paths: every value lives in the config.
"""

from __future__ import annotations

import csv
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Mapping

from cli.themes import Theme, theme_from_payload


@dataclass(frozen=True)
class TimelineColumn:
    """Descriptor for a single column rendered by the scrubber."""

    identifier: str
    label: str
    source_keys: tuple[str, ...]
    width: int


@dataclass(frozen=True)
class TimelineConfig:
    """Centralised constants for the scrubber."""

    title: str = "Timeline scrubber"
    subtitle: str = "Up/Down to navigate, / to filter, Esc to close"
    sessions_dir: str = "sessions"
    report_filename: str = "LazyOwn_session_report.csv"
    max_rows: int = 5000
    max_field_chars: int = 96
    truncation_suffix: str = "..."
    empty_message: str = "(no commands recorded yet)"
    columns: tuple[TimelineColumn, ...] = (
        TimelineColumn("timestamp", "Time", ("timestamp", "date", "ts"), 19),
        TimelineColumn("command", "Command", ("tool", "command", "name"), 28),
        TimelineColumn("status", "Status", ("status", "result", "exit_code"), 10),
        TimelineColumn("target", "Target", ("target", "rhost", "host"), 18),
        TimelineColumn("phase", "Phase", ("phase",), 8),
    )
    detail_keys_skip: tuple[str, ...] = ()


@dataclass(frozen=True)
class TimelineEntry:
    """Immutable row exposed to consumers of :class:`TimelineState`."""

    row_index: int
    fields: Mapping[str, str]


class TimelineReader:
    """Read the CSV report into a list of :class:`TimelineEntry` records."""

    def __init__(self, config: TimelineConfig, root: Path | None = None) -> None:
        """Bind to config and resolve the sessions root."""
        self._config = config
        self._root = Path(root) if root is not None else Path(config.sessions_dir)

    @property
    def root(self) -> Path:
        """Return the resolved sessions root."""
        return self._root

    def read(self) -> list[TimelineEntry]:
        """Return the parsed entries, newest last."""
        path = self._root / self._config.report_filename
        if not path.is_file():
            return []
        try:
            with path.open("r", encoding="utf-8", errors="ignore", newline="") as handle:
                reader = csv.DictReader(handle)
                rows = list(reader)
        except (OSError, csv.Error):
            return []
        bounded = rows[-self._config.max_rows :]
        entries: list[TimelineEntry] = []
        for index, row in enumerate(bounded):
            fields = self._coerce_row(row)
            entries.append(TimelineEntry(row_index=index, fields=fields))
        return entries

    def _coerce_row(self, row: Mapping[str, Any]) -> dict[str, str]:
        out: dict[str, str] = {}
        for key, value in row.items():
            if not isinstance(key, str):
                continue
            if isinstance(value, str):
                cleaned = value.strip()
            elif value is None:
                cleaned = ""
            else:
                cleaned = str(value).strip()
            if len(cleaned) > self._config.max_field_chars:
                keep = max(1, self._config.max_field_chars - len(self._config.truncation_suffix))
                cleaned = cleaned[:keep] + self._config.truncation_suffix
            out[key] = cleaned
        return out


@dataclass
class TimelineState:
    """Filtering + selection state shared with the Textual app."""

    config: TimelineConfig
    reader: TimelineReader
    filter_query: str = ""
    _cached: list[TimelineEntry] | None = field(default=None, init=False, repr=False)

    def reload(self) -> None:
        """Drop the cache so the next :meth:`entries` call re-reads disk."""
        self._cached = None

    def entries(self) -> list[TimelineEntry]:
        """Return filtered entries; reads disk on the first call."""
        if self._cached is None:
            self._cached = self.reader.read()
        if not self.filter_query:
            return list(self._cached)
        needle = self.filter_query.lower()
        out: list[TimelineEntry] = []
        for entry in self._cached:
            haystack = " ".join(entry.fields.values()).lower()
            if needle in haystack:
                out.append(entry)
        return out

    def column_value(self, entry: TimelineEntry, column: TimelineColumn) -> str:
        """Return the first non-empty value among ``column.source_keys``."""
        for key in column.source_keys:
            value = entry.fields.get(key)
            if isinstance(value, str) and value:
                return value
        return ""


def build_state(
    payload: Mapping[str, Any] | None = None,
    sessions_dir: str | None = None,
    config: TimelineConfig | None = None,
) -> TimelineState:
    """Wire the canonical state used by :func:`launch_scrubber`."""
    cfg = config or TimelineConfig()
    root = Path(sessions_dir) if sessions_dir and sessions_dir.strip() else Path(cfg.sessions_dir)
    reader = TimelineReader(cfg, root=root)
    return TimelineState(config=cfg, reader=reader)


def launch_scrubber(
    payload: Mapping[str, Any] | None = None,
    state: TimelineState | None = None,
    runner: Any | None = None,
) -> int | None:
    """Open the scrubber and return the highlighted row index on exit.

    Args:
        payload: Loaded ``payload.json``.
        state: Optional pre-built state (tests inject one).
        runner: Optional callable replacing the real Textual app.

    Returns:
        The 0-based row index the operator last highlighted, or ``None``
        when the scrubber was closed without selection / Textual is
        unavailable.
    """
    chosen = state if state is not None else build_state(payload)
    theme = theme_from_payload(payload)
    if runner is not None:
        return runner({"state": chosen, "theme": theme})
    app = _build_app(chosen, theme)
    if app is None:
        return None
    try:
        result = app.run()
    except Exception:
        return None
    if isinstance(result, int):
        return result
    return None


def _build_app(state: TimelineState, theme: Theme) -> Any | None:
    try:
        from textual.app import App, ComposeResult
        from textual.binding import Binding
        from textual.containers import Vertical
        from textual.widgets import DataTable, Footer, Header, Input, Static
    except Exception:
        return None

    cfg = state.config

    class _TimelineBrowserApp(App):
        TITLE = cfg.title
        SUB_TITLE = cfg.subtitle
        BINDINGS = [
            Binding("escape", "close", "Close"),
            Binding("ctrl+r", "refresh", "Refresh"),
        ]
        CSS = (
            "Screen { layout: vertical; }\n"
            "#filter-input { dock: top; height: 3; }\n"
            "#timeline-body { layout: vertical; height: 1fr; }\n"
            "#timeline-table { height: 1fr; }\n"
            "#timeline-detail { height: 8; border-top: solid $primary; padding: 0 1; }\n"
        )

        def __init__(self) -> None:
            super().__init__()
            self._state = state
            self._theme = theme
            self._row_index: int | None = None

        def compose(self) -> ComposeResult:
            yield Header()
            yield Input(placeholder="Filter (substring across columns)", id="filter-input")
            with Vertical(id="timeline-body"):
                yield DataTable(id="timeline-table")
                yield Static(cfg.empty_message, id="timeline-detail")
            yield Footer()

        def on_mount(self) -> None:
            table = self.query_one("#timeline-table", DataTable)
            for column in cfg.columns:
                table.add_column(column.label, width=column.width, key=column.identifier)
            table.cursor_type = "row"
            self._rebuild_rows()

        def on_input_changed(self, event: Input.Changed) -> None:
            self._state.filter_query = (event.value or "").strip()
            self._rebuild_rows()

        def on_data_table_row_highlighted(self, event: DataTable.RowHighlighted) -> None:
            row_key = event.row_key.value if event.row_key is not None else None
            if isinstance(row_key, int):
                self._row_index = row_key
                self._refresh_detail(row_key)

        def action_refresh(self) -> None:
            self._state.reload()
            self._rebuild_rows()

        def action_close(self) -> None:
            self.exit(result=self._row_index)

        def _rebuild_rows(self) -> None:
            table = self.query_one("#timeline-table", DataTable)
            table.clear()
            entries = self._state.entries()
            if not entries:
                self.query_one("#timeline-detail", Static).update(cfg.empty_message)
                return
            for entry in entries:
                values = [self._state.column_value(entry, column) for column in cfg.columns]
                table.add_row(*values, key=entry.row_index)
            self._refresh_detail(entries[-1].row_index)

        def _refresh_detail(self, row_index: int) -> None:
            entries = self._state.entries()
            target = next((entry for entry in entries if entry.row_index == row_index), None)
            detail = self.query_one("#timeline-detail", Static)
            if target is None:
                detail.update(cfg.empty_message)
                return
            lines = [f"{key}: {value}" for key, value in target.fields.items() if value]
            detail.update("\n".join(lines) if lines else cfg.empty_message)

    return _TimelineBrowserApp()


__all__ = [
    "TimelineColumn",
    "TimelineConfig",
    "TimelineEntry",
    "TimelineReader",
    "TimelineState",
    "build_state",
    "launch_scrubber",
]
