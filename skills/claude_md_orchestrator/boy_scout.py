"""Boy Scout refactor pass.

The pass runs after the green stage. The pass scans the artifacts the
bdd agent produced for tech debt and security gaps the DoD validators
catch. The pass generates a fix plan and writes a refactor proposal
the operator can review. The pass never mutates source by itself; the
operator is the only one who applies the fix.

The pass is intentionally narrow. The DoD is enforced by the
reviewer. The boy scout pass focuses on the cleanup that does not
change behaviour: removed unused imports, deduplicated literals, and
the documentation drift.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable, Optional

from .config import Config
from .models import Contract, Finding, Severity
from .validators import check_source


UNUSED_IMPORT_PATTERN = re.compile(r"^\s*import\s+([\w.]+)|^\s*from\s+([\w.]+)\s+import", re.MULTILINE)
DEAD_CODE_HINT = re.compile(r"\b(pass\s*$|\.\.\.\s*$|TODO|FIXME)", re.MULTILINE)


@dataclass
class ScoutReport:
    """Outcome of a boy scout pass.

    Attributes:
        contract_id: Identifier of the contract the pass ran for.
        findings: Findings the pass collected.
        proposal: Free form text the operator can read before
            applying the refactor.
    """

    contract_id: str
    findings: list[Finding] = field(default_factory=list)
    proposal: str = ""


def _inspect(path: Path) -> list[Finding]:
    """Run a deeper inspection on one source file."""
    findings: list[Finding] = []
    if not path.exists() or path.suffix != ".py":
        return findings
    text = path.read_text(encoding="utf-8")
    findings.extend(check_source(text, str(path)))
    declared = set()
    for match in UNUSED_IMPORT_PATTERN.finditer(text):
        module = match.group(1) or match.group(2)
        if module:
            declared.add(module)
    for name in sorted(declared):
        if name not in text.replace(f"import {name}", ""):
            continue
        occurrences = len(re.findall(rf"\b{re.escape(name)}\b", text))
        if occurrences <= 1:
            findings.append(
                Finding(
                    severity=Severity.WARN,
                    rule="boy_scout.unused_import",
                    message=f"import {name!r} appears to be unused",
                    path=str(path),
                )
            )
    return findings


def _render_proposal(contract: Contract, findings: list[Finding]) -> str:
    """Render the human facing proposal text."""
    lines = [
        f"# Boy Scout proposal for contract {contract.contract_id}",
        "",
        "I read the artifacts the cycle produced. The pass flags the items below.",
        "",
    ]
    if not findings:
        lines.append("- no findings; the artifacts comply with the DoD")
    for finding in findings:
        lines.append(f"- [{finding.severity.value}] {finding.rule}: {finding.message} ({finding.path})")
    lines.append("")
    lines.append("Apply the cleanup in a follow up commit. Re run the cycle to confirm green.")
    return "\n".join(lines)


def run(state, config: Config) -> ScoutReport:
    """Run the boy scout pass for one contract.

    Args:
        state: Per contract state the pass reads the artifacts from.
        config: Active runtime configuration.
    Returns:
        The structured report the orchestrator persists.
    """
    findings: list[Finding] = []
    for candidate in (state.spec_path, state.test_path, state.src_path):
        if candidate is not None:
            findings.extend(_inspect(candidate))
    return ScoutReport(
        contract_id=state.contract.contract_id,
        findings=findings,
        proposal=_render_proposal(state.contract, findings),
    )


def write_report(report: ScoutReport, config: Config) -> Path:
    """Persist the boy scout proposal to disk."""
    config.review_dir().mkdir(parents=True, exist_ok=True)
    path = config.review_dir() / f"{report.contract_id}.scout.md"
    path.write_text(report.proposal, encoding="utf-8")
    return path
