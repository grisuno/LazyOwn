"""Documentation agent.

The agent writes the user facing documentation for a contract. The
output is first person scientific English. The agent never uses emoji
or em dash. The agent never uses grand claims that the tests do not
back. The output is a markdown block wrapped in a triple backtick
fence, ready for copy and paste, signed by grisun0.

The agent is deterministic. The LLM enrichment is optional and runs
only when the operator configures a backend. The default template
captures the metadata the orchestrator already knows, so the
documentation is reproducible.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from .config import Config
from .models import Contract, ReviewReport, Spec


SIGNATURE = "grisun0"
FENCE = "```markdown"


@dataclass
class DocResult:
    """Outcome of the documentation agent.

    Attributes:
        path: Absolute path of the doc file the agent wrote.
        body: The rendered markdown body inside the fence.
    """

    path: Path
    body: str


def _format_inputs(spec: Spec) -> str:
    """Render the inputs section as a bullet list."""
    if not spec.inputs:
        return "- none beyond the contract scope"
    return "\n".join(f"- {item}" for item in spec.inputs)


def _format_sad_paths(spec: Spec) -> str:
    """Render the sad paths section as a bullet list."""
    if not spec.sad_paths:
        return "- none documented"
    return "\n".join(
        f"- given {sp.condition}, when it triggers, then {sp.expected}"
        for sp in spec.sad_paths
    )


def _format_review(report: Optional[ReviewReport]) -> str:
    """Render the review summary as a bullet list."""
    if report is None:
        return "- review not yet executed"
    return (
        f"- ruff exit {report.ruff_exit}\n"
        f"- mypy exit {report.mypy_exit}\n"
        f"- bandit exit {report.bandit_exit}\n"
        f"- pytest exit {report.pytest_exit}\n"
        f"- findings {len(report.findings)} blockers {len(report.blockers())}\n"
        f"- approved {report.approved}"
    )


def _render(contract: Contract, spec: Spec, report: Optional[ReviewReport]) -> str:
    """Render the markdown body inside the fence."""
    lines = [
        f"# Contract {contract.contract_id}",
        "",
        "I built this piece to deliver the contract the repository declares. "
        "The contract id is {cid}. The title is {title}. The rationale the "
        "parser lifted is below.".format(cid=contract.contract_id, title=contract.title),
        "",
        "## Rationale",
        "",
        contract.rationale or "the rationale lives in the contract body",
        "",
        "## Trigger",
        "",
        spec.trigger,
        "",
        "## Inputs",
        "",
        _format_inputs(spec),
        "",
        "## Happy path",
        "",
        "\n".join(f"{index}. {step}" for index, step in enumerate(spec.happy_path, start=1)),
        "",
        "## Sad paths",
        "",
        _format_sad_paths(spec),
        "",
        "## Data flow",
        "",
        spec.data_flow,
        "",
        "## Observability",
        "",
        spec.observability,
        "",
        "## Out of scope",
        "",
        "\n".join(f"- {item}" for item in spec.out_of_scope),
        "",
        "## Review",
        "",
        _format_review(report),
        "",
        f"signed by {SIGNATURE}",
    ]
    return "\n".join(lines)


def _wrap(body: str) -> str:
    """Wrap the body in a markdown fence."""
    return f"{FENCE}\n{body}\n```\n"


def run(contract: Contract, spec: Spec, report: Optional[ReviewReport], config: Config) -> DocResult:
    """Run the documentation agent for one contract.

    Args:
        contract: The contract the spec implements.
        spec: The spec the documentation covers.
        report: The review report the documentation summarises.
            Pass None when the reviewer has not run yet.
        config: Active runtime configuration.
    Returns:
        The result the orchestrator persists. The path points at a
        markdown file that the operator can copy and paste into the
        repository docs.
    """
    config.docs_dir().mkdir(parents=True, exist_ok=True)
    body = _render(contract, spec, report)
    fenced = _wrap(body)
    path = config.docs_dir() / f"{contract.contract_id}.md"
    path.write_text(fenced, encoding="utf-8")
    return DocResult(path=path, body=body)
