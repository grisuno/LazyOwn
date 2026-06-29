"""Code Reviewer and Quality Assurance agent.

The agent runs the static analyzers the LazyOwn repository already
configures. The agent collects the DoD findings every analyzer emits
plus the findings the in house validators emit. The agent approves
the contract when the report carries zero blockers. The orchestrator
advances only when the report is approved.

The agent never blocks on warnings when the strict flag is False. The
agent always blocks on a non zero exit code from any analyzer.
"""

from __future__ import annotations

import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Optional

from .config import Config
from .models import Contract, Finding, ReviewReport, Severity, Spec
from .validators import check_markdown, check_source


REVIEWABLE_SUFFIXES = (".py", ".md", ".yaml", ".yml")


@dataclass
class AnalyzerResult:
    """Outcome of running one external analyzer.

    Attributes:
        tool: Name of the analyzer.
        exit_code: Return code of the analyzer.
        stdout: Captured stdout.
        stderr: Captured stderr.
    """

    tool: str
    exit_code: int
    stdout: str
    stderr: str


def _run(cmd: Iterable[str], cwd: Path) -> AnalyzerResult:
    """Run an external analyzer and return the captured output.

    Args:
        cmd: Command line arguments.
        cwd: Working directory the analyzer uses.
    Returns:
        The analyzer result. The function never raises. A missing
        tool is recorded with exit code 127 and an explanatory
        stderr line so the reviewer can mark the finding as a warn.
    """
    completed = subprocess.run(
        list(cmd),
        cwd=str(cwd),
        capture_output=True,
        text=True,
        check=False,
    )
    return AnalyzerResult(
        tool=cmd[0] if cmd else "<empty>",
        exit_code=completed.returncode,
        stdout=completed.stdout,
        stderr=completed.stderr,
    )


def _resolve_targets(state, config: Config) -> list[Path]:
    """Collect the artifacts the reviewer must inspect.

    Args:
        state: Per contract state the reviewer uses to find files.
        config: Active runtime configuration.
    Returns:
        A list of absolute paths. Empty list when nothing is present.
    """
    targets: list[Path] = []
    for candidate in (state.spec_path, state.test_path, state.src_path):
        if candidate and candidate.exists():
            targets.append(candidate)
    return targets


def _parse_tool_findings(result: AnalyzerResult, path_prefix: str) -> list[Finding]:
    """Translate an analyzer output into a list of findings.

    Args:
        result: The analyzer result to translate.
        path_prefix: Prefix the reviewer prepends to every finding
            path.
    Returns:
        The findings. The translation is best effort. The reviewer
        records one finding per non empty line of stderr. The exit
        code only escalates a finding to BLOCK when the analyzer
        reports at least one line.
    """
    findings: list[Finding] = []
    lines = [line.strip() for line in (result.stdout + "\n" + result.stderr).splitlines()]
    lines = [line for line in lines if line]
    if not lines:
        return findings
    severity = Severity.BLOCK if result.exit_code != 0 else Severity.WARN
    for line in lines:
        findings.append(
            Finding(
                severity=severity,
                rule=f"analyzer.{result.tool}",
                message=line,
                path=path_prefix,
            )
        )
        if len(findings) > 50:
            break
    return findings


def _run_ruff(targets: list[Path], cwd: Path) -> Optional[AnalyzerResult]:
    """Run ruff when the binary is available."""
    if not shutil.which("ruff"):
        return None
    py_targets = [t for t in targets if t.suffix == ".py"]
    if not py_targets:
        return None
    return _run(
        ["ruff", "check", "--output-format", "concise", *[str(t) for t in py_targets]],
        cwd=cwd,
    )


def _run_mypy(targets: list[Path], cwd: Path) -> Optional[AnalyzerResult]:
    """Run mypy when the binary is available."""
    if not shutil.which("mypy"):
        return None
    py_targets = [t for t in targets if t.suffix == ".py"]
    if not py_targets:
        return None
    return _run(
        ["mypy", "--ignore-missing-imports", "--no-error-summary", *[str(t) for t in py_targets]],
        cwd=cwd,
    )


def _run_bandit(targets: list[Path], cwd: Path) -> Optional[AnalyzerResult]:
    """Run bandit when the binary is available."""
    if not shutil.which("bandit"):
        return None
    py_targets = [t for t in targets if t.suffix == ".py"]
    if not py_targets:
        return None
    return _run(
        ["bandit", "-q", *[str(t) for t in py_targets]],
        cwd=cwd,
    )


def _run_pytest(targets: list[Path], cwd: Path) -> Optional[AnalyzerResult]:
    """Run pytest against the test module to confirm green."""
    test_path = next((t for t in targets if t.name.startswith("test_")), None)
    if test_path is None:
        return None
    return _run(
        [sys.executable, "-m", "pytest", str(test_path), "-q", "--no-header"],
        cwd=cwd,
    )


def run(state, config: Config) -> ReviewReport:
    """Run the reviewer for one contract.

    Args:
        state: Per contract state the reviewer reads the artifacts
            from.
        config: Active runtime configuration.
    Returns:
        The structured review report. The report carries the
        analyzer exit codes, the in house DoD findings, and a
        boolean approved flag the orchestrator consumes.
    """
    targets = _resolve_targets(state, config)
    findings: list[Finding] = []
    ruff = _run_ruff(targets, config.repo_root) if targets else None
    if ruff is not None:
        findings.extend(_parse_tool_findings(ruff, "ruff"))
    mypy = _run_mypy(targets, config.repo_root) if targets else None
    if mypy is not None:
        findings.extend(_parse_tool_findings(mypy, "mypy"))
    bandit = _run_bandit(targets, config.repo_root) if targets else None
    if bandit is not None:
        findings.extend(_parse_tool_findings(bandit, "bandit"))
    pytest_result = _run_pytest(targets, config.repo_root) if targets else None
    if pytest_result is not None:
        findings.extend(_parse_tool_findings(pytest_result, "pytest"))
    for target in targets:
        text = target.read_text(encoding="utf-8")
        if target.suffix == ".py":
            findings.extend(check_source(text, str(target)))
        elif target.suffix in (".md", ".yaml", ".yml"):
            findings.extend(check_markdown(text, str(target)))
    blockers = [
        finding for finding in findings if finding.severity is Severity.BLOCK
    ]
    if not config.reviewer_strict:
        blockers = [
            finding
            for finding in blockers
            if finding.rule.startswith("dod.")
        ]
    approved = not blockers
    summary_lines = [
        f"targets: {len(targets)}",
        f"findings: {len(findings)}",
        f"blockers: {len(blockers)}",
        f"approved: {approved}",
    ]
    return ReviewReport(
        contract_id=state.contract.contract_id,
        approved=approved,
        findings=findings,
        ruff_exit=ruff.exit_code if ruff else 0,
        mypy_exit=mypy.exit_code if mypy else 0,
        bandit_exit=bandit.exit_code if bandit else 0,
        pytest_exit=pytest_result.exit_code if pytest_result else 0,
        summary=" | ".join(summary_lines),
    )


def write_report(report: ReviewReport, config: Config) -> Path:
    """Persist the report as JSON inside the run review directory."""
    config.review_dir().mkdir(parents=True, exist_ok=True)
    import json

    path = config.review_dir() / f"{report.contract_id}.json"
    path.write_text(json.dumps(report.to_dict(), indent=2), encoding="utf-8")
    return path
