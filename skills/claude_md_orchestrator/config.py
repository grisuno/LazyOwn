"""Centralized configuration for the claude_md_orchestrator skill.

The orchestrator reads every runtime value from this module. Tests and
runtime both consume the same dataclass. The defaults point to a local
run directory inside the skill so a fresh checkout is runnable without
external state. The orchestrator may override any field at construction
time.
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional


REPO_ROOT_ENV = "LAZYOWN_REPO_ROOT"
RUN_DIR_ENV = "LAZYOWN_ORCH_RUN_DIR"
CLAUDE_MD_ENV = "LAZYOWN_CLAUDE_MD_PATH"
DEPLOY_GATE_ENV = "LAZYOWN_DEPLOY_GATE_TOKEN"


def _repo_root() -> Path:
    """Return the absolute path of the LazyOwn repository root.

    The skill lives at skills/claude_md_orchestrator/. The repository root
    is two parents above the package directory. The orchestrator may
    override this value through the LAZYOWN_REPO_ROOT environment variable
    so the same code runs in CI and in a developer checkout.
    """
    override = os.environ.get(REPO_ROOT_ENV)
    if override:
        return Path(override).expanduser().resolve()
    here = Path(__file__).resolve()
    return here.parents[2]


def _default_run_dir() -> Path:
    """Return the absolute path of the orchestrator run directory.

    The directory holds specs, tests, sources, reviews, docs, and the
    cycle state file. The path is computed from the repository root so
    the skill stays portable across checkouts. The orchestrator may
    override the value through the LAZYOWN_ORCH_RUN_DIR environment
    variable.
    """
    override = os.environ.get(RUN_DIR_ENV)
    if override:
        return Path(override).expanduser().resolve()
    return _repo_root() / "skills" / "claude_md_orchestrator" / "runs" / "current"


def _default_claude_md() -> Path:
    """Return the absolute path of the CLAUDE.md that the parser consumes.

    The default points at the canonical LazyOwn CLAUDE.md. The orchestrator
    may override the value through the LAZYOWN_CLAUDE_MD_PATH environment
    variable so the same skill can drive a feature on any markdown file
    that follows the same shape.
    """
    override = os.environ.get(CLAUDE_MD_ENV)
    if override:
        return Path(override).expanduser().resolve()
    return _repo_root() / "CLAUDE.md"


@dataclass
class Config:
    """Runtime configuration for the orchestrator.

    Attributes:
        repo_root: Absolute path of the LazyOwn repository.
        run_dir: Absolute path of the working directory for the active
            cycle. The orchestrator creates the subdirectories specs,
            tests, src, review, docs, and logs under this root.
        claude_md_path: Absolute path of the markdown file the parser
            consumes.
        base_branch: Branch from which the cicd agent cuts the feature
            branch. The default follows the LazyOwn branching model.
        feature_branch_prefix: Prefix the cicd agent prepends to every
            feature branch it cuts.
        max_sad_paths: Minimum number of sad paths the spec writer must
            document. The DoD enforces six.
        test_min_red_seconds: Lower bound the orchestrator enforces on
            the red stage so a flaky runner cannot race through.
        reviewer_strict: When True the reviewer treats every warning as
            a blocker. When False the reviewer reports non blockers and
            lets the operator decide.
        llm_backend: Identifier of the LLM backend the agents use. The
            value comes from the LazyOwn llm_factory module when
            available. The orchestrator falls back to the mock template
            engine when the value is empty or unknown.
        deploy_gate_token: Shared secret the cicd agent checks before it
            calls any deploy tool. The orchestrator reads the value from
            the LAZYOWN_DEPLOY_GATE_TOKEN environment variable. A
            missing token keeps the gate closed by design.
        verbose: When True the orchestrator prints a stage banner to
            stderr after every transition.
    """

    repo_root: Path = field(default_factory=_repo_root)
    run_dir: Path = field(default_factory=_default_run_dir)
    claude_md_path: Path = field(default_factory=_default_claude_md)
    base_branch: str = "dev"
    feature_branch_prefix: str = "feature"
    max_sad_paths: int = 6
    test_min_red_seconds: float = 0.0
    reviewer_strict: bool = True
    llm_backend: str = ""
    deploy_gate_token: str = field(
        default_factory=lambda: os.environ.get(DEPLOY_GATE_ENV, "")
    )
    verbose: bool = True

    def ensure(self) -> None:
        """Create the run subdirectories if they do not exist.

        The orchestrator calls this method before it dispatches the
        first agent so downstream agents can write without checking the
        filesystem.
        """
        for sub in ("specs", "tests", "src", "review", "docs", "logs"):
            (self.run_dir / sub).mkdir(parents=True, exist_ok=True)

    def state_path(self) -> Path:
        """Return the absolute path of the cycle state file."""
        return self.run_dir / "state.json"

    def specs_dir(self) -> Path:
        """Return the absolute path of the spec directory."""
        return self.run_dir / "specs"

    def tests_dir(self) -> Path:
        """Return the absolute path of the test directory."""
        return self.run_dir / "tests"

    def src_dir(self) -> Path:
        """Return the absolute path of the implementation directory."""
        return self.run_dir / "src"

    def review_dir(self) -> Path:
        """Return the absolute path of the review directory."""
        return self.run_dir / "review"

    def docs_dir(self) -> Path:
        """Return the absolute path of the documentation directory."""
        return self.run_dir / "docs"

    def logs_dir(self) -> Path:
        """Return the absolute path of the log directory."""
        return self.run_dir / "logs"

    def log_path(self) -> Path:
        """Return the absolute path of the JSONL log for the active run."""
        return self.logs_dir() / "cycle.jsonl"


def load_config() -> Config:
    """Build a Config from environment variables and return it.

    The function never mutates global state. It exists so the test
    suite and the CLI entry point share the same resolution path.
    """
    return Config()


def resolve_optional(config: Config, key: str) -> Optional[str]:
    """Return the environment value for a key or None when missing.

    The helper keeps the call sites free of repeated os.environ lookups
    so the production code reads as a single conditional.
    """
    return os.environ.get(key) or None
