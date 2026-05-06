"""Lint quality gate.

Runs ``ruff check`` and ``ruff format --check`` against every Python file that
the active tier has touched, and fails the test suite if any violation appears.
This prevents Tier-N regressions from shipping to ``main`` even if a developer
forgets to run pre-commit.

The strict set grows as we refactor:

- Tier 0: ``setup.py``, ``tests/test_tier0_foundation.py``
- Tier 1: ``core/``, ``tests/test_tier1_core.py``, ``utils.py`` (legacy rules
  whitelisted in ``pyproject.toml`` per-file-ignores)
- Tier N: append the files that tier touches when it lands.

Tests are parametrized so a failure points at the exact file.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent

LINT_TARGETS: list[str] = [
    "setup.py",
    "core",
    "utils.py",
    "tests/test_tier0_foundation.py",
    "tests/test_tier1_core.py",
    "tests/test_lint_quality.py",
]

FORMAT_TARGETS: list[str] = [
    "setup.py",
    "core",
    "tests/test_tier0_foundation.py",
    "tests/test_tier1_core.py",
    "tests/test_lint_quality.py",
]


def _run_ruff(args: list[str]) -> subprocess.CompletedProcess[str]:
    """Invoke ``python -m ruff`` so the venv's ruff binary is always used."""
    return subprocess.run(
        [sys.executable, "-m", "ruff", *args],
        capture_output=True,
        text=True,
        cwd=str(REPO_ROOT),
        timeout=120,
    )


@pytest.mark.parametrize("target", LINT_TARGETS, ids=LINT_TARGETS)
def test_ruff_check_clean(target: str) -> None:
    """``ruff check`` must report zero issues on touched paths."""
    result = _run_ruff(["check", target])
    assert result.returncode == 0, (
        f"ruff check failed for {target}\n--- stdout ---\n{result.stdout}\n--- stderr ---\n{result.stderr}"
    )


@pytest.mark.parametrize("target", FORMAT_TARGETS, ids=FORMAT_TARGETS)
def test_ruff_format_clean(target: str) -> None:
    """``ruff format --check`` must report zero formatting drift on touched paths."""
    result = _run_ruff(["format", "--check", target])
    assert result.returncode == 0, (
        f"ruff format check failed for {target} — run 'ruff format {target}' to fix\n"
        f"--- stdout ---\n{result.stdout}\n"
        f"--- stderr ---\n{result.stderr}"
    )


def test_lint_targets_exist() -> None:
    """Every entry in ``LINT_TARGETS`` must exist on disk."""
    missing = [t for t in LINT_TARGETS if not (REPO_ROOT / t).exists()]
    assert missing == [], f"LINT_TARGETS references missing paths: {missing}"


def test_format_targets_exist() -> None:
    """Every entry in ``FORMAT_TARGETS`` must exist on disk."""
    missing = [t for t in FORMAT_TARGETS if not (REPO_ROOT / t).exists()]
    assert missing == [], f"FORMAT_TARGETS references missing paths: {missing}"
