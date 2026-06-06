"""Tests for cli/timeline_browser.py.

Verifies CSV ingestion, filtering and column resolution. Textual is not
exercised here.
"""

from __future__ import annotations

import csv
import sys
from pathlib import Path

_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(_ROOT))

from cli.timeline_browser import (  # noqa: E402
    TimelineColumn,
    TimelineConfig,
    TimelineReader,
    build_state,
)


def _write_report(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = sorted({key for row in rows for key in row.keys()})
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def test_reader_returns_empty_when_csv_missing(tmp_path: Path) -> None:
    """Missing report yields an empty list, never raises."""
    reader = TimelineReader(TimelineConfig(sessions_dir=str(tmp_path)), root=tmp_path)
    assert reader.read() == []


def test_reader_parses_rows(tmp_path: Path) -> None:
    """CSV rows become :class:`TimelineEntry` objects with stripped values."""
    report = tmp_path / "LazyOwn_session_report.csv"
    _write_report(
        report,
        [
            {"timestamp": "2026-05-24T10:00:00", "tool": "ping", "status": "ok", "target": "10.0.0.1", "phase": "recon"},
            {"timestamp": "2026-05-24T10:05:00", "tool": "lazynmap", "status": "ok", "target": "10.0.0.1", "phase": "recon"},
        ],
    )
    reader = TimelineReader(TimelineConfig(sessions_dir=str(tmp_path)), root=tmp_path)
    entries = reader.read()
    assert [entry.fields["tool"] for entry in entries] == ["ping", "lazynmap"]


def test_state_filters_across_columns(tmp_path: Path) -> None:
    """Filter substring matches every column value of an entry."""
    report = tmp_path / "LazyOwn_session_report.csv"
    _write_report(
        report,
        [
            {"timestamp": "t1", "tool": "ping", "target": "10.0.0.1", "phase": "recon"},
            {"timestamp": "t2", "tool": "gobuster", "target": "10.0.0.2", "phase": "enum"},
        ],
    )
    state = build_state(sessions_dir=str(tmp_path))
    state.filter_query = "gobuster"
    entries = state.entries()
    assert len(entries) == 1
    assert entries[0].fields["tool"] == "gobuster"


def test_state_filter_empty_returns_all(tmp_path: Path) -> None:
    """An empty filter returns every entry."""
    report = tmp_path / "LazyOwn_session_report.csv"
    _write_report(report, [{"tool": "a"}, {"tool": "b"}])
    state = build_state(sessions_dir=str(tmp_path))
    assert len(state.entries()) == 2


def test_column_value_falls_back_through_source_keys(tmp_path: Path) -> None:
    """The first non-empty source key wins."""
    report = tmp_path / "LazyOwn_session_report.csv"
    _write_report(report, [{"command": "old-form", "tool": ""}])
    state = build_state(sessions_dir=str(tmp_path))
    entries = state.entries()
    column = TimelineColumn("c", "Command", ("tool", "command"), 20)
    assert state.column_value(entries[0], column) == "old-form"


def test_state_reload_drops_cache(tmp_path: Path) -> None:
    """Reload forces the next ``entries`` call to re-read disk."""
    report = tmp_path / "LazyOwn_session_report.csv"
    _write_report(report, [{"tool": "a"}])
    state = build_state(sessions_dir=str(tmp_path))
    assert len(state.entries()) == 1
    _write_report(report, [{"tool": "a"}, {"tool": "b"}])
    state.reload()
    assert len(state.entries()) == 2


def test_reader_truncates_long_field_values(tmp_path: Path) -> None:
    """Field values longer than ``max_field_chars`` are truncated."""
    report = tmp_path / "LazyOwn_session_report.csv"
    long_value = "x" * 500
    _write_report(report, [{"tool": long_value}])
    state = build_state(sessions_dir=str(tmp_path))
    entries = state.entries()
    assert entries[0].fields["tool"].endswith("...")
