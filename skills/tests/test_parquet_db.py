#!/usr/bin/env python3
"""
Tests for lazyown_parquet_db.py — ParquetDB.

Uses tmp_path fixture exclusively; never touches real parquets/ or sessions/.
pandas and pyarrow are required (verified at import time).
"""

from __future__ import annotations

import csv
import sys
from pathlib import Path
from typing import Any, Dict, List

import pytest

_SKILLS_DIR = Path(__file__).parent.parent
if str(_SKILLS_DIR) not in sys.path:
    sys.path.insert(0, str(_SKILLS_DIR))

try:
    import pandas as pd
    import pyarrow as pa
    _PANDAS_OK = True
except ImportError:
    _PANDAS_OK = False

pytestmark = pytest.mark.skipif(
    not _PANDAS_OK, reason="pandas and pyarrow not installed"
)

from lazyown_parquet_db import ParquetDB, _stable_id

SCHEMA_COLS = ParquetDB.SCHEMA_COLS


# ─────────────────────────────────────────────────────────────────────────────
# CSV helpers
# ─────────────────────────────────────────────────────────────────────────────

_CSV_FIELDNAMES = [
    "start", "end", "source_ip", "source_port",
    "destination_ip", "destination_port",
    "domain", "subdomain", "url", "pivot_port",
    "command", "args",
]


def _write_csv(path: Path, rows: List[Dict[str, str]]) -> None:
    """Write a minimal session CSV file compatible with ParquetDB.sync()."""
    with path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=_CSV_FIELDNAMES, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            full = {k: "" for k in _CSV_FIELDNAMES}
            full.update(row)
            writer.writerow(full)


def _make_db(tmp_path: Path) -> ParquetDB:
    """
    Create a ParquetDB pointed entirely at tmp_path.

    We patch _root / _parquets / _session_pkt and also pass a non-existent
    lazyown.py so _build_cmd2_category_map returns {} gracefully.
    """
    fake_lazyown = tmp_path / "lazyown.py"
    fake_lazyown.write_text("# empty\n")

    db = ParquetDB.__new__(ParquetDB)
    db._root = tmp_path
    db._parquets = tmp_path / "parquets"
    db._parquets.mkdir(parents=True, exist_ok=True)
    db._session_pkt = db._parquets / "session_knowledge.parquet"
    db._cmd2_map = {}  # skip parsing real lazyown.py
    return db


# ─────────────────────────────────────────────────────────────────────────────
# Tests
# ─────────────────────────────────────────────────────────────────────────────


class TestParquetDBSync:
    def test_sync_from_csv(self, tmp_path):
        """Create a minimal CSV, sync() → parquet has correct rows."""
        db = _make_db(tmp_path)
        csv_path = tmp_path / "LazyOwn_session_report.csv"
        _write_csv(csv_path, [
            {
                "start": "2024-01-01T00:00:00",
                "command": "nmap",
                "args": "-sV 10.10.11.78",
                "destination_ip": "10.10.11.78",
                "destination_port": "0",
            },
            {
                "start": "2024-01-01T00:01:00",
                "command": "gobuster",
                "args": "dir -u http://10.10.11.78",
                "destination_ip": "10.10.11.78",
                "destination_port": "80",
            },
        ])
        n = db.sync(csv_path)
        assert n == 2, f"Expected 2 new rows, got {n}"
        df = pd.read_parquet(db._session_pkt)
        assert len(df) == 2
        assert set(df["command"].tolist()) == {"nmap", "gobuster"}

    def test_sync_skips_empty_command(self, tmp_path):
        """Rows with empty command → skipped by sync()."""
        db = _make_db(tmp_path)
        csv_path = tmp_path / "LazyOwn_session_report.csv"
        _write_csv(csv_path, [
            {"start": "2024-01-01T00:00:00", "command": "", "args": "", "destination_ip": ""},
            {"start": "2024-01-01T00:01:00", "command": "nmap", "args": "-sV 10.0.0.1", "destination_ip": "10.0.0.1"},
        ])
        n = db.sync(csv_path)
        assert n == 1

    def test_sync_idempotent(self, tmp_path):
        """Syncing the same CSV twice → second sync adds 0 rows."""
        db = _make_db(tmp_path)
        csv_path = tmp_path / "LazyOwn_session_report.csv"
        _write_csv(csv_path, [
            {"start": "2024-01-01T00:00:00", "command": "nmap", "args": "-p 445", "destination_ip": "10.0.0.1"},
        ])
        n1 = db.sync(csv_path)
        n2 = db.sync(csv_path)
        assert n1 == 1
        assert n2 == 0  # idempotent

    def test_schema_cols(self, tmp_path):
        """Synced parquet has all SCHEMA_COLS columns."""
        db = _make_db(tmp_path)
        csv_path = tmp_path / "LazyOwn_session_report.csv"
        _write_csv(csv_path, [
            {"start": "2024-01-01T00:00:00", "command": "nmap", "args": "-sV", "destination_ip": "10.0.0.1"},
        ])
        db.sync(csv_path)
        df = pd.read_parquet(db._session_pkt)
        for col in SCHEMA_COLS:
            assert col in df.columns, f"Missing column: {col}"

    def test_sync_missing_csv(self, tmp_path):
        """sync() with non-existent CSV → returns 0, no crash."""
        db = _make_db(tmp_path)
        n = db.sync(tmp_path / "nonexistent.csv")
        assert n == 0


class TestParquetDBAnnotate:
    def _setup_with_one_row(self, tmp_path) -> tuple:
        db = _make_db(tmp_path)
        csv_path = tmp_path / "LazyOwn_session_report.csv"
        _write_csv(csv_path, [
            {
                "start": "2024-02-01T12:00:00",
                "command": "enum4linux",
                "args": "-a 10.10.11.78",
                "destination_ip": "10.10.11.78",
                "destination_port": "445",
            }
        ])
        db.sync(csv_path)
        df = pd.read_parquet(db._session_pkt)
        row_id = df.iloc[0]["id"]
        return db, row_id

    def test_annotate(self, tmp_path):
        """sync then annotate a row with success=False → success column updated."""
        db, row_id = self._setup_with_one_row(tmp_path)
        ok = db.annotate(row_id, success=False)
        assert ok is True
        df = pd.read_parquet(db._session_pkt)
        row = df[df["id"] == row_id].iloc[0]
        assert bool(row["success"]) is False
        assert row["outcome"] == "failure"

    def test_annotate_category(self, tmp_path):
        """annotate() can update category field."""
        db, row_id = self._setup_with_one_row(tmp_path)
        ok = db.annotate(row_id, category="scanning")
        assert ok is True
        df = pd.read_parquet(db._session_pkt)
        row = df[df["id"] == row_id].iloc[0]
        assert row["category"] == "scanning"

    def test_annotate_missing_id(self, tmp_path):
        """annotate() with a non-existent row_id → returns False."""
        db, _ = self._setup_with_one_row(tmp_path)
        ok = db.annotate("ffffffffffffffff", success=True)
        assert ok is False

    def test_annotate_rich_finding_type_credential(self, tmp_path):
        """annotate_rich with output containing 'password:' → finding_type='credential'."""
        db, row_id = self._setup_with_one_row(tmp_path)
        output = "Found credential: password: S3cr3t!\nadmin:password:hunter2"
        ok = db.annotate_rich(row_id, output=output)
        assert ok is True
        df = pd.read_parquet(db._session_pkt)
        row = df[df["id"] == row_id].iloc[0]
        assert row["finding_type"] == "credential"

    def test_annotate_rich_finding_type_vulnerability(self, tmp_path):
        """annotate_rich with 'CVE-' in output → finding_type='vulnerability'."""
        db, row_id = self._setup_with_one_row(tmp_path)
        output = "Found CVE-2021-41773 on Apache httpd"
        ok = db.annotate_rich(row_id, output=output)
        assert ok is True
        df = pd.read_parquet(db._session_pkt)
        row = df[df["id"] == row_id].iloc[0]
        assert row["finding_type"] == "vulnerability"

    def test_annotate_rich_finding_type_hash(self, tmp_path):
        """annotate_rich with NTLM hash pattern → finding_type='hash'."""
        db, row_id = self._setup_with_one_row(tmp_path)
        # The annotate_rich regex requires exactly 32 lowercase hex chars on each side of ':'
        lm  = "aad3b435b51404eeaad3b435b51404ee"  # 32 chars
        nt  = "31d6cfe0d16ae931b73c59d7e0c089c0"  # 32 chars
        output = f"Administrator:500:{lm}:{nt}:::"
        ok = db.annotate_rich(row_id, output=output)
        assert ok is True
        df = pd.read_parquet(db._session_pkt)
        row = df[df["id"] == row_id].iloc[0]
        assert row["finding_type"] == "hash"

    def test_annotate_rich_output_snippet_truncated(self, tmp_path):
        """annotate_rich stores at most 300 chars of output."""
        db, row_id = self._setup_with_one_row(tmp_path)
        long_output = "A" * 500
        db.annotate_rich(row_id, output=long_output)
        df = pd.read_parquet(db._session_pkt)
        row = df[df["id"] == row_id].iloc[0]
        assert len(str(row["output_snippet"])) <= 300

    def test_annotate_rich_explicit_finding_type(self, tmp_path):
        """annotate_rich with explicit finding_type overrides auto-detect."""
        db, row_id = self._setup_with_one_row(tmp_path)
        # output has 'password' but we explicitly say 'path'
        ok = db.annotate_rich(row_id, output="password found", finding_type="path")
        assert ok is True
        df = pd.read_parquet(db._session_pkt)
        row = df[df["id"] == row_id].iloc[0]
        assert row["finding_type"] == "path"


class TestParquetDBQuerySession:
    def _setup_two_phases(self, tmp_path) -> "ParquetDB":
        db = _make_db(tmp_path)
        csv_path = tmp_path / "LazyOwn_session_report.csv"
        _write_csv(csv_path, [
            {
                "start": "2024-03-01T10:00:00",
                "command": "nmap",
                "args": "-sV 10.10.11.78",
                "destination_ip": "10.10.11.78",
            },
            {
                "start": "2024-03-01T10:05:00",
                "command": "gobuster",
                "args": "dir -u http://10.10.11.78",
                "destination_ip": "10.10.11.78",
            },
        ])
        db.sync(csv_path)
        # Manually set categories so the filter is deterministic
        df = pd.read_parquet(db._session_pkt)
        nmap_id = df[df["command"] == "nmap"].iloc[0]["id"]
        gobuster_id = df[df["command"] == "gobuster"].iloc[0]["id"]
        db.annotate(nmap_id, category="recon")
        db.annotate(gobuster_id, category="scanning")
        return db

    def test_query_session_filter(self, tmp_path):
        """query_session(phase='recon') returns only recon rows."""
        db = self._setup_two_phases(tmp_path)
        rows = db.query_session(phase="recon")
        assert len(rows) >= 1
        for row in rows:
            assert row["category"] == "recon", f"Unexpected category: {row['category']}"

    def test_query_session_scanning_filter(self, tmp_path):
        """query_session(phase='scanning') returns only scanning rows."""
        db = self._setup_two_phases(tmp_path)
        rows = db.query_session(phase="scanning")
        assert len(rows) >= 1
        for row in rows:
            assert row["category"] == "scanning"

    def test_query_session_no_filter(self, tmp_path):
        """query_session() with no filter returns all rows."""
        db = self._setup_two_phases(tmp_path)
        rows = db.query_session()
        assert len(rows) == 2

    def test_query_session_empty(self, tmp_path):
        """query_session() on empty parquet → returns []."""
        db = _make_db(tmp_path)
        rows = db.query_session(phase="recon")
        assert rows == []

    def test_query_session_target_filter(self, tmp_path):
        """query_session(target='1.2.3.4') filters by destination_ip."""
        db = _make_db(tmp_path)
        csv_path = tmp_path / "LazyOwn_session_report.csv"
        _write_csv(csv_path, [
            {"start": "2024-01-01", "command": "nmap", "args": "-sV", "destination_ip": "10.10.11.78"},
            {"start": "2024-01-01", "command": "nmap", "args": "-sV", "destination_ip": "192.168.1.1"},
        ])
        db.sync(csv_path)
        rows = db.query_session(target="10.10.11.78")
        assert all(r["destination_ip"] == "10.10.11.78" for r in rows)
        assert len(rows) == 1


class TestParquetDBQueryKnowledge:
    def test_query_knowledge_session_parquet(self, tmp_path):
        """query_knowledge searches session_knowledge.parquet for a command keyword."""
        db = _make_db(tmp_path)
        csv_path = tmp_path / "LazyOwn_session_report.csv"
        _write_csv(csv_path, [
            {"start": "2024-01-01", "command": "curl", "args": "-s http://10.0.0.1", "destination_ip": "10.0.0.1"},
            {"start": "2024-01-01", "command": "nmap", "args": "-sV 10.0.0.1", "destination_ip": "10.0.0.1"},
        ])
        db.sync(csv_path)
        results = db.query_knowledge("curl")
        assert "session_knowledge" in results
        rows = results["session_knowledge"]
        assert len(rows) >= 1
        assert any("curl" in str(r.get("command", "")) for r in rows)

    def test_query_knowledge_no_match(self, tmp_path):
        """query_knowledge for keyword that doesn't exist → empty or missing key."""
        db = _make_db(tmp_path)
        csv_path = tmp_path / "LazyOwn_session_report.csv"
        _write_csv(csv_path, [
            {"start": "2024-01-01", "command": "nmap", "args": "-sV", "destination_ip": "10.0.0.1"},
        ])
        db.sync(csv_path)
        results = db.query_knowledge("xyzzy_nonexistent_keyword_12345")
        # Either empty dict or session_knowledge key with empty list
        total = sum(len(v) for v in results.values())
        assert total == 0

    @pytest.mark.skipif(
        not (Path(__file__).parent.parent.parent / "parquets" / "binarios.parquet").exists(),
        reason="parquets/binarios.parquet not present in this environment",
    )
    def test_query_knowledge_keyword_binarios(self, tmp_path):
        """query_knowledge('curl') against real binarios.parquet → returns results."""
        real_parquets = Path(__file__).parent.parent.parent / "parquets"
        db = _make_db(tmp_path)
        # Point db at the real parquets dir for this test only
        db._parquets = real_parquets
        results = db.query_knowledge("curl", parquet_name="binarios")
        if "binarios" in results:
            assert len(results["binarios"]) >= 1


class TestStableId:
    def test_stable_id_deterministic(self):
        """Same inputs → same ID."""
        id1 = _stable_id("2024-01-01", "nmap", "-sV 10.0.0.1", "10.0.0.1")
        id2 = _stable_id("2024-01-01", "nmap", "-sV 10.0.0.1", "10.0.0.1")
        assert id1 == id2

    def test_stable_id_different_inputs(self):
        """Different inputs → different IDs."""
        id1 = _stable_id("2024-01-01", "nmap", "-sV 10.0.0.1", "10.0.0.1")
        id2 = _stable_id("2024-01-01", "nmap", "-sV 10.0.0.2", "10.0.0.2")
        assert id1 != id2

    def test_stable_id_length(self):
        """Stable ID is 16 hex chars."""
        row_id = _stable_id("2024-01-01", "nmap", "-sV", "10.0.0.1")
        assert len(row_id) == 16
        assert all(c in "0123456789abcdef" for c in row_id)
