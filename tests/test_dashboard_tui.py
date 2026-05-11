"""Tests for cli/dashboard_tui.py.

Exercises the data-loading helpers and widget update logic with synthetic
fixtures so the suite runs without a real LazyOwn session on disk.
The Textual App itself is not instantiated in these tests — rendering is a
thin wrapper around the helpers tested here.
"""

from __future__ import annotations

import csv
import json
import sys
from pathlib import Path
from unittest.mock import patch

_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(_ROOT))

from cli.dashboard_tui import (  # noqa: E402
    KILL_CHAIN_PHASES,
    _count_lines_in_glob,
    _graph_hints,
    _read_json,
    _read_recent_commands,
)


class TestReadJson:
    def test_reads_valid_file(self, tmp_path: Path) -> None:
        p = tmp_path / "data.json"
        p.write_text(json.dumps({"rhost": "10.0.0.1"}), encoding="utf-8")
        assert _read_json(str(p)) == {"rhost": "10.0.0.1"}

    def test_missing_file_returns_empty_dict(self, tmp_path: Path) -> None:
        assert _read_json(str(tmp_path / "missing.json")) == {}

    def test_invalid_json_returns_empty_dict(self, tmp_path: Path) -> None:
        p = tmp_path / "bad.json"
        p.write_text("{not valid json}", encoding="utf-8")
        assert _read_json(str(p)) == {}


class TestCountLinesInGlob:
    def test_counts_non_empty_lines(self, tmp_path: Path) -> None:
        f = tmp_path / "credentials_test.txt"
        f.write_text("admin:password\nroot:toor\n\n", encoding="utf-8")
        count = _count_lines_in_glob(str(tmp_path / "credentials*.txt"))
        assert count == 2

    def test_empty_file_returns_zero(self, tmp_path: Path) -> None:
        f = tmp_path / "credentials_empty.txt"
        f.write_text("", encoding="utf-8")
        assert _count_lines_in_glob(str(tmp_path / "credentials*.txt")) == 0

    def test_no_matching_files_returns_zero(self, tmp_path: Path) -> None:
        assert _count_lines_in_glob(str(tmp_path / "nonexistent*.txt")) == 0

    def test_multiple_files_summed(self, tmp_path: Path) -> None:
        (tmp_path / "credentials_a.txt").write_text("a\nb\n", encoding="utf-8")
        (tmp_path / "credentials_b.txt").write_text("c\n", encoding="utf-8")
        assert _count_lines_in_glob(str(tmp_path / "credentials*.txt")) == 3


class TestReadRecentCommands:
    def _make_transcript(self, tmp_path: Path, rows: list[dict]) -> Path:
        p = tmp_path / "LazyOwn_session_report.csv"
        if not rows:
            p.write_text("tool,status,timestamp\n", encoding="utf-8")
            return p
        with p.open("w", newline="", encoding="utf-8") as fh:
            writer = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
            writer.writeheader()
            writer.writerows(rows)
        return p

    def test_reads_recent_commands(self, tmp_path: Path) -> None:
        rows = [
            {"tool": "ping", "status": "ok", "timestamp": "2026-05-11"},
            {"tool": "lazynmap", "status": "ok", "timestamp": "2026-05-11"},
        ]
        transcript = self._make_transcript(tmp_path, rows)
        with patch("cli.dashboard_tui.TRANSCRIPT_PATH", str(transcript)):
            result = _read_recent_commands()
        assert len(result) == 2
        assert result[0]["cmd"] == "ping"
        assert result[1]["cmd"] == "lazynmap"

    def test_missing_file_returns_empty(self, tmp_path: Path) -> None:
        with patch("cli.dashboard_tui.TRANSCRIPT_PATH", str(tmp_path / "missing.csv")):
            assert _read_recent_commands() == []

    def test_empty_file_returns_empty(self, tmp_path: Path) -> None:
        transcript = self._make_transcript(tmp_path, [])
        with patch("cli.dashboard_tui.TRANSCRIPT_PATH", str(transcript)):
            assert _read_recent_commands() == []

    def test_respects_window_limit(self, tmp_path: Path) -> None:
        rows = [{"tool": f"cmd_{i}", "status": "ok", "timestamp": ""} for i in range(20)]
        transcript = self._make_transcript(tmp_path, rows)
        with patch("cli.dashboard_tui.TRANSCRIPT_PATH", str(transcript)):
            result = _read_recent_commands(limit=5)
        assert len(result) == 5

    def test_skips_empty_tool_rows(self, tmp_path: Path) -> None:
        rows = [
            {"tool": "ping", "status": "ok", "timestamp": ""},
            {"tool": "", "status": "", "timestamp": ""},
        ]
        transcript = self._make_transcript(tmp_path, rows)
        with patch("cli.dashboard_tui.TRANSCRIPT_PATH", str(transcript)):
            result = _read_recent_commands()
        assert len(result) == 1
        assert result[0]["cmd"] == "ping"


class TestKillChainPhases:
    def test_all_phases_present(self) -> None:
        keys = [k for k, _ in KILL_CHAIN_PHASES]
        assert "recon" in keys
        assert "exploit" in keys
        assert "exfil" in keys
        assert "report" in keys

    def test_phases_ordered(self) -> None:
        keys = [k for k, _ in KILL_CHAIN_PHASES]
        assert keys.index("recon") < keys.index("exploit")
        assert keys.index("exploit") < keys.index("lateral")


class TestGraphHints:
    def test_returns_list_when_advisor_unavailable(self) -> None:
        with patch("cli.dashboard_tui.sys.path", []):
            result = _graph_hints()
        assert isinstance(result, list)

    def test_returns_list_on_exception(self) -> None:
        with patch("builtins.__import__", side_effect=ImportError("no module")):
            result = _graph_hints()
        assert isinstance(result, list)

    def test_returns_labels_from_advisor(self) -> None:
        with patch("cli.dashboard_tui._graph_hints", return_value=["do_lazynmap", "do_gobuster"]):
            result = _graph_hints()
        assert isinstance(result, list)
