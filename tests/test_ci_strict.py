"""Contract tests for the strict CI workflow.

The repository must keep the CI workflow honest. The tests below
verify that the strict workflow exists, that it does not swallow
failures through ``|| true`` or ``continue-on-error: true``, and that
it executes the lint, type, security, and test analyzers the contract
defines. The tests were written by the tdd agent and pass through the
bdd agent that ships the strict workflow file.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
STRICT_WORKFLOW = REPO_ROOT / ".github" / "workflows" / "test_strict.yml"


def test_strict_workflow_exists() -> None:
    """The strict workflow file is present in the repository."""
    assert STRICT_WORKFLOW.exists(), f"missing {STRICT_WORKFLOW}"


def test_strict_workflow_contains_no_swallow_flags() -> None:
    """The strict workflow does not contain the failure swallow flags."""
    text = STRICT_WORKFLOW.read_text(encoding="utf-8")
    forbidden_patterns = (
        r"\|\|\s*true",
        r"continue-on-error\s*:\s*true",
    )
    for pattern in forbidden_patterns:
        match = re.search(pattern, text)
        assert match is None, f"forbidden pattern {pattern!r} found in strict workflow"


def test_strict_workflow_runs_lint() -> None:
    """The strict workflow runs ruff on the project."""
    text = STRICT_WORKFLOW.read_text(encoding="utf-8")
    assert re.search(r"run:\s*ruff\s+check", text), "ruff check step is missing"


def test_strict_workflow_runs_type_check() -> None:
    """The strict workflow runs mypy on the project."""
    text = STRICT_WORKFLOW.read_text(encoding="utf-8")
    assert re.search(r"run:\s*mypy", text), "mypy step is missing"


def test_strict_workflow_runs_security_scan() -> None:
    """The strict workflow runs bandit on the project."""
    text = STRICT_WORKFLOW.read_text(encoding="utf-8")
    assert re.search(r"run:\s*bandit", text), "bandit step is missing"


def test_strict_workflow_runs_pytest() -> None:
    """The strict workflow runs the test suite with pytest."""
    text = STRICT_WORKFLOW.read_text(encoding="utf-8")
    assert re.search(r"run:\s*pytest", text), "pytest step is missing"


def test_strict_workflow_targets_main_branch() -> None:
    """The strict workflow targets the main branch on push and pull request."""
    text = STRICT_WORKFLOW.read_text(encoding="utf-8")
    assert re.search(r"branches:\s*\[main\]", text), "main branch trigger is missing"


def test_old_swallow_workflow_is_removed() -> None:
    """The legacy test.yml workflow must not contain the swallow flags."""
    legacy = REPO_ROOT / ".github" / "workflows" / "test.yml"
    if not legacy.exists():
        return
    text = legacy.read_text(encoding="utf-8")
    forbidden_patterns = (
        r"\|\|\s*true",
        r"continue-on-error\s*:\s*true",
    )
    for pattern in forbidden_patterns:
        match = re.search(pattern, text)
        assert match is None, f"forbidden pattern {pattern!r} found in legacy workflow"
