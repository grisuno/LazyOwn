"""Campaign import trust boundaries hold against hostile packages.

SDD contract: ``core.safe_import`` owns ZipSlip-safe extraction,
identifier validation and column filtering. ``cli/commands/campaign``
must route its import path through these helpers instead of raw
``extractall`` and interpolated source columns.
"""

from __future__ import annotations

import ast
import sqlite3
import zipfile
from pathlib import Path

from core.safe_import import (
    filter_columns,
    is_safe_identifier,
    safe_copy_tree,
    safe_extract_zip,
)

REPO_ROOT = Path(__file__).resolve().parent.parent
CAMPAIGN_SRC = (REPO_ROOT / "cli" / "commands" / "campaign.py").read_text(encoding="utf-8")


def _make_evil_zip(path: Path) -> None:
    with zipfile.ZipFile(path, "w") as zf:
        zf.writestr("manifest.json", "{}")
        zf.writestr("sessions/ok.txt", "fine")
        zf.writestr("../../evil.txt", "escape")
        zf.writestr("/absolute.txt", "absolute")


class TestZipSlip:
    def test_evil_members_skipped(self, tmp_path: Path) -> None:
        archive = tmp_path / "pkg.zip"
        _make_evil_zip(archive)
        dest = tmp_path / "out"
        extracted = safe_extract_zip(archive, dest)
        assert (dest / "sessions" / "ok.txt").read_text() == "fine"
        assert not (tmp_path / "evil.txt").exists()
        assert not (dest / "absolute.txt").exists()
        assert all(".." not in e and not e.startswith("/") for e in extracted)

    def test_legit_tree_extracted(self, tmp_path: Path) -> None:
        archive = tmp_path / "pkg.zip"
        with zipfile.ZipFile(archive, "w") as zf:
            zf.writestr("a/b.txt", "data")
        dest = tmp_path / "out"
        assert safe_extract_zip(archive, dest) == ["a/b.txt"]
        assert (dest / "a" / "b.txt").read_text() == "data"


class TestColumnFiltering:
    def test_identifier_policy(self) -> None:
        assert is_safe_identifier("workspace_id") is True
        assert is_safe_identifier("_x1") is True
        for evil in ("", "a b", '");DROP TABLE x;--', '"col"', "a-b", "9lives", "a.b"):
            assert is_safe_identifier(evil) is False, evil

    def test_unknown_and_hostile_dropped(self) -> None:
        dest = ["id", "workspace_id", "address"]
        src = ["id", '");DROP TABLE hosts;--', "address", "attacker_col"]
        assert filter_columns(src, dest) == ["id", "address"]

    def test_order_preserved(self) -> None:
        assert filter_columns(["b", "a"], ["a", "b"]) == ["b", "a"]

    def test_filtered_insert_roundtrip(self, tmp_path: Path) -> None:
        db = sqlite3.connect(tmp_path / "d.db")
        db.execute("CREATE TABLE hosts (id INTEGER PRIMARY KEY, address TEXT)")
        columns = filter_columns(["id", "address", 'x");--'], ["id", "address"])
        col_str = ", ".join(columns)
        placeholders = ", ".join("?" for _ in columns)
        db.execute(f"INSERT INTO hosts ({col_str}) VALUES ({placeholders})", (None, "10.0.0.1"))
        assert db.execute("SELECT address FROM hosts").fetchone()[0] == "10.0.0.1"


class TestCopyTree:
    def test_symlinks_not_followed(self, tmp_path: Path) -> None:
        src = tmp_path / "src"
        src.mkdir()
        (src / "real.txt").write_text("data")
        outside = tmp_path / "secret.txt"
        outside.write_text("secret")
        try:
            (src / "link.txt").symlink_to(outside)
        except OSError:
            pass
        dest = tmp_path / "dest"
        assert safe_copy_tree(src, dest) == 1
        assert (dest / "real.txt").read_text() == "data"


class TestCampaignRoutesThroughHelpers:
    def test_no_raw_extractall_on_import(self) -> None:
        tree = ast.parse(CAMPAIGN_SRC)
        calls = [
            n
            for n in ast.walk(tree)
            if isinstance(n, ast.Call)
            and isinstance(n.func, ast.Attribute)
            and n.func.attr == "extractall"
        ]
        assert not calls, "campaign import must use safe_extract_zip"

    def test_uses_safe_helpers(self) -> None:
        assert "safe_extract_zip" in CAMPAIGN_SRC
        assert "filter_columns" in CAMPAIGN_SRC
        assert "safe_copy_tree" in CAMPAIGN_SRC
