"""Default-credential knowledge base for LazyOwn.

Loads ``modules/data/default_creds.csv`` (vendor, username, password
triples sourced from the open DefaultCreds-Cheat-Sheet, MIT) and exposes
case-insensitive lookups for operators and gym chains. Pure file reads:
no network, no shell.

>>> from modules import lazy_creds
>>> rows = lazy_creds.search("apache")
>>> rows[0]["vendor"]
'Apache'
"""

from __future__ import annotations

import csv
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import Any

BASE_DIR = Path(__file__).resolve().parent.parent
DEFAULT_CREDS_PATH = BASE_DIR / "modules" / "data" / "default_creds.csv"
MAX_OUTPUT_ROWS = 40
MAX_SEED_ROWS = 5000
MAX_FILE_BYTES = 5_000_000


@dataclass(frozen=True)
class CredRow:
    """One default-credential triple from the knowledge base."""

    vendor: str
    username: str
    password: str


@lru_cache(maxsize=1)
def load() -> tuple[CredRow, ...]:
    """Load the CSV knowledge base once per process.

    Returns:
        Immutable tuple of cred rows; empty when the file is missing,
        oversized or malformed (defensive, never raises).
    """
    path = Path(DEFAULT_CREDS_PATH)
    if not path.is_file() or path.stat().st_size > MAX_FILE_BYTES:
        return ()
    rows: list[CredRow] = []
    try:
        with path.open(newline="", encoding="utf-8", errors="replace") as handle:
            for record in csv.DictReader(handle):
                vendor = str(record.get("productvendor") or "").strip()
                username = str(record.get("username") or "").strip()
                password = str(record.get("password") or "").strip()
                if vendor and username:
                    rows.append(CredRow(vendor, username, password))
    except Exception:
        return ()
    return tuple(rows)


def search(query: str) -> list[CredRow]:
    """Return rows whose vendor or username contains the query.

    Args:
        query: Case-insensitive substring (empty returns nothing).

    Returns:
        Matching rows capped at ``MAX_OUTPUT_ROWS``.
    """
    needle = str(query or "").strip().lower()
    if not needle:
        return []
    hits = [row for row in load() if needle in row.vendor.lower() or needle in row.username.lower()]
    return hits[:MAX_OUTPUT_ROWS]


def candidates(limit: int = MAX_OUTPUT_ROWS) -> list[CredRow]:
    """Return the most repeated (username, password) pairs for spraying.

    Args:
        limit: Maximum pairs to return.

    Returns:
        Distinct credential pairs ordered by frequency.
    """
    seen: dict[tuple[str, str], int] = {}
    for row in load():
        key = (row.username, row.password)
        seen[key] = seen.get(key, 0) + 1
    ranked = sorted(seen.items(), key=lambda item: (-item[1], item[0]))
    return [CredRow("", username, password) for (username, password), _ in ranked[: max(1, limit)]]


def count() -> int:
    """Return the total number of knowledge-base rows."""
    return len(load())


def as_lines(rows: list[CredRow]) -> list[str]:
    """Render rows as aligned ``vendor,username,password`` lines."""
    return [f"{row.vendor or '-':<28} {row.username:<24} {row.password}" for row in rows]


def export_pairs(path: Path | str, limit: int = MAX_SEED_ROWS) -> dict[str, Any]:
    """Export ``username:password`` pairs for spray tools.

    Args:
        path: Destination file (created/overwritten).
        limit: Export cap.

    Returns:
        Mapping with ``written`` and ``error``.
    """
    rows = candidates(limit)
    if not rows:
        return {"written": 0, "error": "knowledge base empty"}
    try:
        target = Path(path)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text("\n".join(f"{row.username}:{row.password}" for row in rows) + "\n", encoding="utf-8")
    except Exception as exc:
        return {"written": 0, "error": str(exc)}
    return {"written": len(rows), "error": ""}


if __name__ == "__main__":
    import sys

    query = " ".join(sys.argv[1:]) or "-"
    for line in as_lines(search(query)) or ["no matches"]:
        print(line)
