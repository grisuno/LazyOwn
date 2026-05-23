"""Guard against drift between CLAUDE.md numeric claims and reality.

CLAUDE.md publishes a handful of small facts about the repository (test
count, presence of optional artefacts) that historically went stale
silently. These assertions keep them honest. Each fact is a single
assertion so a future drift only breaks the one line that needs editing.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).parent.parent
CLAUDE_MD = REPO_ROOT / "CLAUDE.md"
TESTS_DIR = REPO_ROOT / "tests"


@pytest.fixture(scope="module")
def claude_md_text() -> str:
    if not CLAUDE_MD.is_file():
        pytest.skip("CLAUDE.md missing — repository is in an unexpected state")
    return CLAUDE_MD.read_text(encoding="utf-8")


def test_claude_md_reports_actual_test_file_count(claude_md_text: str) -> None:
    """The ``tests/`` row in §2 must match the real ``test_*.py`` file count."""

    real_count = len(list(TESTS_DIR.glob("test_*.py")))
    match = re.search(r"`tests/`\s*\|\s*(\d+)\s*files", claude_md_text)
    assert match is not None, "CLAUDE.md §2 must declare the tests/ file count"
    declared = int(match.group(1))
    assert declared == real_count, (
        f"CLAUDE.md claims {declared} test files but there are {real_count}. "
        "Update the §2 tests/ row when adding or removing test_*.py files."
    )


def test_claude_md_does_not_reference_deduplicated_config(claude_md_text: str) -> None:
    """The obsolete ``two class Config defs`` note must not return."""

    assert "two `class Config` defs" not in claude_md_text, (
        "CLAUDE.md §7 still mentions the deduplicated Config classes. "
        "The single canonical Config now lives in utils.py — remove the note."
    )
