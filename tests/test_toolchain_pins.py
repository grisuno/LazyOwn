"""Contract: one ruff/mypy version across every tooling surface.

The CI/local divergence that kept main red was three ruff versions
coexisting (requirements-dev, ci.yml hardcode, pre-commit rev). These
tests fail the moment any surface drifts again.
"""

from __future__ import annotations

import re
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent


def _dev_pin(package: str) -> str:
    text = (ROOT / "requirements-dev.txt").read_text(encoding="utf-8")
    match = re.search(rf"^{re.escape(package)}==([0-9.]+)\s*$", text, re.MULTILINE)
    assert match, f"{package} must be pinned ==X.Y.Z in requirements-dev.txt"
    return match.group(1)


def test_ci_yml_does_not_hardcode_ruff() -> None:
    text = (ROOT / ".github/workflows/ci.yml").read_text(encoding="utf-8")
    assert not re.search(r"pip install\s+[\"']?ruff==", text), (
        "ci.yml hardcodes a ruff version; install requirements-dev.txt instead"
    )


def test_pre_commit_ruff_rev_matches_dev_pin() -> None:
    config = yaml.safe_load((ROOT / ".pre-commit-config.yaml").read_text(encoding="utf-8"))
    ruff_repos = [r for r in config["repos"] if "ruff-pre-commit" in r["repo"]]
    assert ruff_repos, "ruff-pre-commit hook missing"
    expected = "v" + _dev_pin("ruff")
    for repo in ruff_repos:
        assert repo["rev"] == expected, (
            f"pre-commit ruff {repo['rev']} != requirements-dev {expected}"
        )


def test_pre_commit_mypy_rev_matches_dev_pin() -> None:
    config = yaml.safe_load((ROOT / ".pre-commit-config.yaml").read_text(encoding="utf-8"))
    mypy_repos = [r for r in config["repos"] if "mirrors-mypy" in r["repo"]]
    assert mypy_repos, "mirrors-mypy hook missing"
    expected = "v" + _dev_pin("mypy")
    for repo in mypy_repos:
        assert repo["rev"] == expected, (
            f"pre-commit mypy {repo['rev']} != requirements-dev {expected}"
        )


def test_lint_workflow_installs_dev_requirements() -> None:
    text = (ROOT / ".github/workflows/lint.yml").read_text(encoding="utf-8")
    assert "requirements-dev.txt" in text
    assert not re.search(r"pip install\s+[\"']?ruff==", text)
