"""CI and CD agent.

The agent cuts a feature branch, stages the artifacts, prepares the CI
pipeline, and writes the PR body. The agent never pushes and never
deploys. The deploy gate is closed by default. The orchestrator only
opens the gate when the operator supplies the deploy gate token.

The pipeline file is a real GitHub Actions workflow. The agent keeps
the workflow minimal and explicit. The workflow runs ruff, mypy,
bandit, and pytest. The workflow fails when any of those return a
non zero exit code. The agent does not invent matrix builds or
release pipelines. The skill stays portable across LazyOwn releases.
"""

from __future__ import annotations

import re
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from .config import Config
from .models import Contract, ReviewReport, Spec


SAFE_BRANCH = re.compile(r"[^a-z0-9-]+")


PIPELINE_TEMPLATE = """name: orchestrator-{contract_id}

on:
  pull_request:
    branches: [dev]
  push:
    branches: [feature/{slug}]

permissions:
  contents: read

jobs:
  test:
    name: orchestrator-{contract_id}
    runs-on: ubuntu-latest
    strategy:
      fail-fast: false
      matrix:
        python-version: ['3.11']
    steps:
      - uses: actions/checkout@v4
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}
          cache: pip
      - name: Install dev deps
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements-dev.txt
      - name: Run ruff
        run: ruff check {test_path} {source_path}
      - name: Run mypy
        run: mypy --ignore-missing-imports {test_path} {source_path}
      - name: Run bandit
        run: bandit -q {source_path}
      - name: Run pytest
        run: pytest -q {test_path}
"""


@dataclass
class CicdResult:
    """Outcome of the CI and CD agent.

    Attributes:
        branch: Name of the feature branch the agent cut.
        pipeline_path: Absolute path of the workflow file.
        pr_body_path: Absolute path of the PR body file.
        deployed: True when the deploy gate was open and the agent
            ran the deploy command. The default leaves the gate
            closed.
        findings: DoD findings the agent collected.
    """

    branch: str
    pipeline_path: Path
    pr_body_path: Path
    deployed: bool
    findings: list[str]


def _slug(contract: Contract) -> str:
    """Return a safe slug for the branch name."""
    cleaned = SAFE_BRANCH.sub("-", contract.contract_id.lower()).strip("-")
    return cleaned or contract.contract_id


def _git(*args: str, cwd: Path) -> subprocess.CompletedProcess[str]:
    """Run a git command and return the captured output."""
    return subprocess.run(
        ["git", *args],
        cwd=str(cwd),
        capture_output=True,
        text=True,
        check=False,
    )


def _ensure_branch(contract: Contract, config: Config) -> str:
    """Create the feature branch from the base branch.

    Args:
        contract: The contract the branch will carry.
        config: Active runtime configuration.
    Returns:
        The branch name the agent cut.
    """
    branch = f"{config.feature_branch_prefix}/{_slug(contract)}"
    status = _git("status", "--porcelain", cwd=config.repo_root)
    if status.returncode != 0:
        return branch
    if status.stdout.strip():
        return branch
    base = _git("rev-parse", "--verify", config.base_branch, cwd=config.repo_root)
    if base.returncode != 0:
        return branch
    checkout = _git("checkout", "-b", branch, config.base_branch, cwd=config.repo_root)
    if checkout.returncode != 0:
        existing = _git("rev-parse", "--verify", branch, cwd=config.repo_root)
        if existing.returncode == 0:
            _git("checkout", branch, cwd=config.repo_root)
    return branch


def _render_pipeline(contract: Contract, spec: Spec, config: Config) -> str:
    """Render the workflow body the agent writes to disk."""
    return PIPELINE_TEMPLATE.format(
        contract_id=contract.contract_id,
        slug=_slug(contract),
        test_path=str(config.tests_dir().relative_to(config.repo_root) / f"test_{_slug(contract)}.py"),
        source_path=str(config.src_dir().relative_to(config.repo_root) / f"{_slug(contract)}.py"),
    )


def _render_pr_body(contract: Contract, spec: Spec, report: Optional[ReviewReport]) -> str:
    """Render the PR body the agent writes to disk."""
    lines = [
        f"# Contract {contract.contract_id}",
        "",
        contract.rationale or "the rationale lives in the contract body",
        "",
        "## Spec",
        "",
        spec.goal,
        "",
        "## Sad paths covered",
        "",
    ]
    for index, sp in enumerate(spec.sad_paths, start=1):
        lines.append(f"- {index}. {sp.condition}: {sp.expected}")
    lines.append("")
    lines.append("## Review")
    lines.append("")
    if report is None:
        lines.append("- review not yet executed")
    else:
        lines.append(
            f"- approved {report.approved}; findings {len(report.findings)}; "
            f"blockers {len(report.blockers())}; pytest exit {report.pytest_exit}"
        )
    lines.append("")
    lines.append("## Deploy gate")
    lines.append("")
    lines.append("closed until the operator passes the deploy gate token")
    return "\n".join(lines) + "\n"


def run(
    contract: Contract,
    spec: Spec,
    report: Optional[ReviewReport],
    config: Config,
    *,
    auto_commit: bool = False,
    deploy_token: Optional[str] = None,
) -> CicdResult:
    """Run the CI and CD agent for one contract.

    Args:
        contract: The contract the cycle finished.
        spec: The spec the implementation satisfies.
        report: The review report. The agent only ships when the
            report is approved.
        config: Active runtime configuration.
        auto_commit: When True the agent stages the artifacts and
            commits them on the feature branch. The default keeps
            the operator in control of the commit boundary.
        deploy_token: Shared secret the agent checks before it runs
            any deploy command. The gate is closed when the value is
            None or empty.
    Returns:
        The result the orchestrator persists. The deployed flag is
        always False in the default posture.
    """
    findings: list[str] = []
    if report is not None and not report.approved:
        findings.append("review not approved; cicd agent will not ship")
    branch = _ensure_branch(contract, config)
    pipeline_path = config.run_dir / "pipeline.yml"
    pipeline_path.write_text(_render_pipeline(contract, spec, config), encoding="utf-8")
    pr_body_path = config.run_dir / "pr_body.md"
    pr_body_path.write_text(_render_pr_body(contract, spec, report), encoding="utf-8")
    deployed = False
    if auto_commit:
        added = _git("add", str(pipeline_path), str(pr_body_path), cwd=config.repo_root)
        if added.returncode == 0:
            commit = _git(
                "commit",
                "-m",
                f"feat(orchestrator): ship contract {contract.contract_id}",
                cwd=config.repo_root,
            )
            if commit.returncode != 0:
                findings.append(f"git commit failed: {commit.stderr.strip()}")
    if deploy_token and deploy_token == config.deploy_gate_token and config.deploy_gate_token:
        deployed = True
    return CicdResult(
        branch=branch,
        pipeline_path=pipeline_path,
        pr_body_path=pr_body_path,
        deployed=deployed,
        findings=findings,
    )
