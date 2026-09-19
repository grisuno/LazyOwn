"""Docs drift workflow contract tests.

SDD contract: ``.github/workflows/docs-drift.yml`` must regenerate every
auto-generated reference (command index, COMMANDS.md + HTML, UTILS.md)
and fail on any drift. Auto-generated docs are treated as ground truth
by AI operators, so a vacuous check (regenerating one artefact while
diffing another) is a correctness bug, not a nit.
"""

from __future__ import annotations

from pathlib import Path

import pytest
import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
WORKFLOW_PATH = REPO_ROOT / ".github" / "workflows" / "docs-drift.yml"


@pytest.fixture(scope="module")
def workflow_text() -> str:
    return WORKFLOW_PATH.read_text(encoding="utf-8")


@pytest.fixture(scope="module")
def workflow_steps(workflow_text: str) -> list[str]:
    document = yaml.safe_load(workflow_text)
    steps: list[str] = []
    for job in document.get("jobs", {}).values():
        for step in job.get("steps", []):
            run = step.get("run", "")
            if run:
                steps.append(run)
    return steps


def _runs_command(step: str, command: str) -> bool:
    """Match a generator invocation, not a mention inside an echo message."""
    return step.strip().startswith(command)


def test_workflow_exists() -> None:
    assert WORKFLOW_PATH.exists()


def test_regenerates_command_index(workflow_steps: list[str]) -> None:
    assert any(
        _runs_command(step, "python3 scripts/build_command_index.py")
        for step in workflow_steps
    ), "workflow must rebuild cli/command_index.json (write mode, not --check)"


def test_regenerates_commands_reference(workflow_steps: list[str]) -> None:
    assert any(
        _runs_command(step, "python3 readmeneitor.py lazyown.py")
        for step in workflow_steps
    ), "workflow must regenerate COMMANDS.md via readmeneitor.py lazyown.py"


def test_regenerates_utils_reference(workflow_steps: list[str]) -> None:
    assert any(
        _runs_command(step, "python3 readmeneitor.py utils.py")
        for step in workflow_steps
    ), "workflow must regenerate UTILS.md via readmeneitor.py utils.py"


def test_diffs_command_index(workflow_steps: list[str]) -> None:
    assert any(
        "cli/command_index.json" in step and "diff" in step
        for step in workflow_steps
    ), "workflow must fail on cli/command_index.json drift"


def test_diffs_commands_reference(workflow_steps: list[str]) -> None:
    assert any(
        "COMMANDS.md" in step and "diff" in step for step in workflow_steps
    ), "workflow must fail on COMMANDS.md drift"


def test_diffs_utils_reference(workflow_steps: list[str]) -> None:
    assert any(
        "UTILS.md" in step and "diff" in step for step in workflow_steps
    ), "workflow must fail on UTILS.md drift"


def test_trigger_watches_generator_inputs(workflow_text: str) -> None:
    document = yaml.safe_load(workflow_text)
    triggers = document.get("on", document.get(True, {}))
    watched: set[str] = set()
    for trigger in ("pull_request", "push"):
        paths = triggers.get(trigger, {}).get("paths", [])
        watched.update(paths)
    joined = "\n".join(watched)
    assert "cli/commands/" in joined
    assert "utils.py" in joined
