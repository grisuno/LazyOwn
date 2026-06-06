"""Tests for cli/sessions_browser.py.

Exercises the data layer (index + preview + filter) using a temporary
``sessions/`` directory fixture. The Textual app is never instantiated.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(_ROOT))

from cli.sessions_browser import (  # noqa: E402
    SessionPreview,
    SessionsBrowserConfig,
    SessionsIndex,
    build_state,
)


def _populate(tmp_path: Path) -> None:
    (tmp_path / "credentials.txt").write_text("alice:hunter2\n", encoding="utf-8")
    (tmp_path / "hash.txt").write_text("0123abcd\n", encoding="utf-8")
    (tmp_path / "vulns_10.0.0.1.json").write_text(
        json.dumps({"cves": ["CVE-2024-0001"]}), encoding="utf-8"
    )
    (tmp_path / "scan_10.0.0.1.nmap").write_text("nmap output\n", encoding="utf-8")
    (tmp_path / "notes.jsonl").write_text("{\"text\": \"x\"}\n", encoding="utf-8")
    (tmp_path / "world_model.json").write_text("{}\n", encoding="utf-8")
    (tmp_path / "unrelated.bin").write_bytes(b"\x00" * 128)


def test_index_groups_known_files(tmp_path: Path) -> None:
    """Known filenames land in the matching categories."""
    _populate(tmp_path)
    index = SessionsIndex(SessionsBrowserConfig(sessions_dir=str(tmp_path)), root=tmp_path)
    grouped = index.categories()
    assert any(e.relative_path == "credentials.txt" for e in grouped.get("creds", []))
    assert any(e.relative_path == "hash.txt" for e in grouped.get("hashes", []))
    assert any(e.relative_path == "vulns_10.0.0.1.json" for e in grouped.get("vulns", []))
    assert any(e.relative_path == "scan_10.0.0.1.nmap" for e in grouped.get("scan", []))
    assert any(e.relative_path == "notes.jsonl" for e in grouped.get("notes", []))
    assert any(e.relative_path == "world_model.json" for e in grouped.get("world", []))


def test_index_other_bucket_contains_unmatched_files(tmp_path: Path) -> None:
    """Files not matched by any category fall into ``other``."""
    _populate(tmp_path)
    index = SessionsIndex(SessionsBrowserConfig(sessions_dir=str(tmp_path)), root=tmp_path)
    grouped = index.categories()
    other = grouped.get("other", [])
    assert any(e.relative_path == "unrelated.bin" for e in other)


def test_preview_returns_text_for_text_files(tmp_path: Path) -> None:
    """Text files are returned verbatim, truncated to the byte cap."""
    _populate(tmp_path)
    preview = SessionPreview(SessionsBrowserConfig(sessions_dir=str(tmp_path)), root=tmp_path)
    text = preview.read("credentials.txt")
    assert "alice:hunter2" in text


def test_preview_flags_binary_files(tmp_path: Path) -> None:
    """Binary files return the configured indicator instead of garbled bytes."""
    _populate(tmp_path)
    preview = SessionPreview(SessionsBrowserConfig(sessions_dir=str(tmp_path)), root=tmp_path)
    assert preview.read("unrelated.bin") == "(binary)"


def test_preview_rejects_path_traversal(tmp_path: Path) -> None:
    """Paths that escape the root return an empty string."""
    _populate(tmp_path)
    preview = SessionPreview(SessionsBrowserConfig(sessions_dir=str(tmp_path)), root=tmp_path)
    assert preview.read("../etc/passwd") == ""
    assert preview.read("/etc/passwd") == ""


def test_state_filter_keeps_matching_entries(tmp_path: Path) -> None:
    """The filter query narrows every category by substring."""
    _populate(tmp_path)
    state = build_state(sessions_dir=str(tmp_path))
    state.filter_query = "hash"
    grouped = state.grouped_entries()
    assert "hashes" in grouped
    assert all("hash" in entry.relative_path.lower() for entries in grouped.values() for entry in entries)


def test_category_label_for_known_identifier(tmp_path: Path) -> None:
    """The label resolver returns the configured human name."""
    state = build_state(sessions_dir=str(tmp_path))
    assert state.category_label("creds") == "Credentials"
    assert state.category_label("other") == "Other"
    assert state.category_label("unknown-id") == "unknown-id"
