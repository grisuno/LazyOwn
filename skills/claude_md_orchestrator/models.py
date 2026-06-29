"""Data models for the claude_md_orchestrator skill.

The orchestrator is a pure data pipeline. Every agent reads its inputs
from disk, mutates an immutable dataclass, and writes the result back to
disk. The shape of those dataclasses is the contract between the
agents.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any, Optional


def _now_iso() -> str:
    """Return the current UTC time as an ISO 8601 string.

    The helper centralises timestamp formatting so the JSONL log stays
    consistent across agents and runs.
    """
    return datetime.now(timezone.utc).isoformat()


class Stage(str, Enum):
    """Pipeline stages the orchestrator walks through in order.

    Members:
        PENDING: the contract has been parsed but no agent has run.
        SDD: the spec agent has produced the spec.
        TDD: the test agent has produced the failing tests.
        BDD: the implementation agent has produced the source.
        REVIEW: the reviewer agent has produced the report.
        CICD: the cicd agent has produced the branch and the pipeline.
        DONE: every stage finished and the human signalled deploy.
    """

    PENDING = "pending"
    SDD = "sdd"
    TDD = "tdd"
    BDD = "bdd"
    REVIEW = "review"
    CICD = "cicd"
    DONE = "done"


class Severity(str, Enum):
    """Severity levels the reviewer emits.

    Members:
        INFO: cosmetic note. Never a blocker.
        WARN: deviation from the DoD that the boy scout can fix in a
            follow up. The reviewer reports it but lets the cycle
            continue when reviewer_strict is False.
        BLOCK: violation of the DoD. The cycle halts until the agent
            fixes the artifact.
    """

    INFO = "info"
    WARN = "warn"
    BLOCK = "block"


@dataclass
class Contract:
    """A single actionable contract parsed from CLAUDE.md.

    Attributes:
        contract_id: Stable identifier the orchestrator uses to wire
            the files together. The parser derives the value from the
            markdown section number when present.
        title: Short label the agents log with.
        rationale: One paragraph that explains why the contract exists.
        scope: Bullet list of what the contract must deliver.
        source_section: Heading path inside CLAUDE.md the parser
            extracted the contract from.
        raw_text: Verbatim markdown the parser used. Kept so the
            documentation agent can quote the source.
    """

    contract_id: str
    title: str
    rationale: str
    scope: list[str] = field(default_factory=list)
    source_section: str = ""
    raw_text: str = ""

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON friendly view of the contract."""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Contract":
        """Build a Contract from a JSON friendly dictionary."""
        return cls(
            contract_id=str(data.get("contract_id", "")),
            title=str(data.get("title", "")),
            rationale=str(data.get("rationale", "")),
            scope=list(data.get("scope", [])),
            source_section=str(data.get("source_section", "")),
            raw_text=str(data.get("raw_text", "")),
        )


@dataclass
class SadPath:
    """A single failure scenario a spec must cover.

    Attributes:
        condition: Human readable trigger.
        expected: Expected behaviour the implementation must produce.
    """

    condition: str
    expected: str

    def to_dict(self) -> dict[str, str]:
        """Return a JSON friendly view of the sad path."""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict[str, str]) -> "SadPath":
        """Build a SadPath from a JSON friendly dictionary."""
        return cls(
            condition=str(data.get("condition", "")),
            expected=str(data.get("expected", "")),
        )


@dataclass
class Spec:
    """Spec-Driven Development output for one contract.

    Attributes:
        contract_id: Contract this spec implements.
        goal: One line summary.
        trigger: Observable trigger the spec covers.
        inputs: List of inputs the implementation consumes.
        happy_path: Ordered steps the implementation must follow on
            the happy path.
        sad_paths: At least six failure scenarios.
        data_flow: Free form description of the data flow.
        observability: Free form description of how the operator
            observes success.
        out_of_scope: Bullet list of what the contract does not
            cover.
        author: Author of the spec. Defaults to the orchestrator.
        created_at: ISO 8601 timestamp.
    """

    contract_id: str
    goal: str
    trigger: str
    inputs: list[str] = field(default_factory=list)
    happy_path: list[str] = field(default_factory=list)
    sad_paths: list[SadPath] = field(default_factory=list)
    data_flow: str = ""
    observability: str = ""
    out_of_scope: list[str] = field(default_factory=list)
    author: str = "claude_md_orchestrator"
    created_at: str = field(default_factory=_now_iso)

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON friendly view of the spec."""
        data = asdict(self)
        data["sad_paths"] = [sp.to_dict() for sp in self.sad_paths]
        return data

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Spec":
        """Build a Spec from a JSON friendly dictionary."""
        return cls(
            contract_id=str(data.get("contract_id", "")),
            goal=str(data.get("goal", "")),
            trigger=str(data.get("trigger", "")),
            inputs=list(data.get("inputs", [])),
            happy_path=list(data.get("happy_path", [])),
            sad_paths=[SadPath.from_dict(sp) for sp in data.get("sad_paths", [])],
            data_flow=str(data.get("data_flow", "")),
            observability=str(data.get("observability", "")),
            out_of_scope=list(data.get("out_of_scope", [])),
            author=str(data.get("author", "claude_md_orchestrator")),
            created_at=str(data.get("created_at", _now_iso())),
        )

    def validate(self, min_sad_paths: int) -> list[str]:
        """Return the list of DoD violations the spec carries.

        Args:
            min_sad_paths: Minimum number of sad paths the spec must
                document.
        Returns:
            A list of human readable violation messages. Empty list
            means the spec is compliant.
        """
        violations: list[str] = []
        if not self.goal.strip():
            violations.append("spec.goal is empty")
        if not self.trigger.strip():
            violations.append("spec.trigger is empty")
        if not self.happy_path:
            violations.append("spec.happy_path is empty")
        if len(self.sad_paths) < min_sad_paths:
            violations.append(
                f"spec.sad_paths has {len(self.sad_paths)} entries, expected at least {min_sad_paths}"
            )
        for idx, sp in enumerate(self.sad_paths):
            if not sp.condition.strip() or not sp.expected.strip():
                violations.append(f"spec.sad_paths[{idx}] is incomplete")
        if not self.observability.strip():
            violations.append("spec.observability is empty")
        return violations


@dataclass
class TestSuite:
    """Test-Driven Development output for one contract.

    Attributes:
        contract_id: Contract this test suite covers.
        test_path: Absolute path of the pytest module.
        expected_outcome: Outcome the agent expects from pytest. The
            orchestrator checks the value before advancing. The value
            is RED for the tdd agent and GREEN for the bdd agent.
        test_names: Names of the test functions the agent produced.
        duration_seconds: Wall clock duration of the pytest run.
    """

    contract_id: str
    test_path: Path
    expected_outcome: str
    test_names: list[str] = field(default_factory=list)
    duration_seconds: float = 0.0

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON friendly view of the test suite."""
        data = asdict(self)
        data["test_path"] = str(self.test_path)
        return data

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "TestSuite":
        """Build a TestSuite from a JSON friendly dictionary."""
        return cls(
            contract_id=str(data.get("contract_id", "")),
            test_path=Path(str(data.get("test_path", ""))),
            expected_outcome=str(data.get("expected_outcome", "RED")),
            test_names=list(data.get("test_names", [])),
            duration_seconds=float(data.get("duration_seconds", 0.0)),
        )


@dataclass
class Finding:
    """Single review finding.

    Attributes:
        severity: Severity of the finding.
        rule: Identifier of the rule the agent broke.
        message: Human readable description.
        path: Relative path of the file the finding refers to.
    """

    severity: Severity
    rule: str
    message: str
    path: str = ""

    def to_dict(self) -> dict[str, str]:
        """Return a JSON friendly view of the finding."""
        return {
            "severity": self.severity.value,
            "rule": self.rule,
            "message": self.message,
            "path": self.path,
        }

    @classmethod
    def from_dict(cls, data: dict[str, str]) -> "Finding":
        """Build a Finding from a JSON friendly dictionary."""
        return cls(
            severity=Severity(str(data.get("severity", "info"))),
            rule=str(data.get("rule", "")),
            message=str(data.get("message", "")),
            path=str(data.get("path", "")),
        )


@dataclass
class ReviewReport:
    """Reviewer agent output for one contract.

    Attributes:
        contract_id: Contract this report covers.
        approved: True when the reviewer has no blockers. The orchestrator
            advances to the next stage only when approved is True.
        findings: List of findings the reviewer collected.
        ruff_exit: Exit code of the ruff run.
        mypy_exit: Exit code of the mypy run.
        bandit_exit: Exit code of the bandit run.
        pytest_exit: Exit code of the pytest run.
        summary: Short text the operator reads first.
    """

    contract_id: str
    approved: bool
    findings: list[Finding] = field(default_factory=list)
    ruff_exit: int = 0
    mypy_exit: int = 0
    bandit_exit: int = 0
    pytest_exit: int = 0
    summary: str = ""

    def blockers(self) -> list[Finding]:
        """Return the list of blocker findings."""
        return [f for f in self.findings if f.severity is Severity.BLOCK]

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON friendly view of the report."""
        return {
            "contract_id": self.contract_id,
            "approved": self.approved,
            "findings": [f.to_dict() for f in self.findings],
            "ruff_exit": self.ruff_exit,
            "mypy_exit": self.mypy_exit,
            "bandit_exit": self.bandit_exit,
            "pytest_exit": self.pytest_exit,
            "summary": self.summary,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "ReviewReport":
        """Build a ReviewReport from a JSON friendly dictionary."""
        return cls(
            contract_id=str(data.get("contract_id", "")),
            approved=bool(data.get("approved", False)),
            findings=[Finding.from_dict(f) for f in data.get("findings", [])],
            ruff_exit=int(data.get("ruff_exit", 0)),
            mypy_exit=int(data.get("mypy_exit", 0)),
            bandit_exit=int(data.get("bandit_exit", 0)),
            pytest_exit=int(data.get("pytest_exit", 0)),
            summary=str(data.get("summary", "")),
        )


@dataclass
class CicleState:
    """State of a single contract through the pipeline.

    Attributes:
        contract: The contract the cycle processes.
        stage: The stage the contract is currently in.
        spec_path: Absolute path of the spec file.
        test_path: Absolute path of the test file.
        src_path: Absolute path of the source file.
        review_path: Absolute path of the review report.
        doc_path: Absolute path of the documentation file.
        branch_name: Name of the feature branch the cicd agent cut.
        pipeline_path: Absolute path of the CI pipeline file.
        pr_body_path: Absolute path of the PR body file.
        approved: True when the reviewer approved the contract.
        deployed: True when the human signalled deploy.
        started_at: ISO 8601 timestamp when the cycle started.
        updated_at: ISO 8601 timestamp when the last stage finished.
    """

    contract: Contract
    stage: Stage = Stage.PENDING
    spec_path: Optional[Path] = None
    test_path: Optional[Path] = None
    src_path: Optional[Path] = None
    review_path: Optional[Path] = None
    doc_path: Optional[Path] = None
    branch_name: str = ""
    pipeline_path: Optional[Path] = None
    pr_body_path: Optional[Path] = None
    approved: bool = False
    deployed: bool = False
    started_at: str = field(default_factory=_now_iso)
    updated_at: str = field(default_factory=_now_iso)

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON friendly view of the state."""
        data = asdict(self)
        data["contract"] = self.contract.to_dict()
        data["stage"] = self.stage.value
        for key in (
            "spec_path",
            "test_path",
            "src_path",
            "review_path",
            "doc_path",
            "pipeline_path",
            "pr_body_path",
        ):
            if data[key] is not None:
                data[key] = str(data[key])
        return data

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "CicleState":
        """Build a CicleState from a JSON friendly dictionary."""
        contract_data = data.get("contract") or {}
        return cls(
            contract=Contract.from_dict(contract_data),
            stage=Stage(str(data.get("stage", Stage.PENDING.value))),
            spec_path=Path(p) if (p := data.get("spec_path")) else None,
            test_path=Path(p) if (p := data.get("test_path")) else None,
            src_path=Path(p) if (p := data.get("src_path")) else None,
            review_path=Path(p) if (p := data.get("review_path")) else None,
            doc_path=Path(p) if (p := data.get("doc_path")) else None,
            branch_name=str(data.get("branch_name", "")),
            pipeline_path=Path(p) if (p := data.get("pipeline_path")) else None,
            pr_body_path=Path(p) if (p := data.get("pr_body_path")) else None,
            approved=bool(data.get("approved", False)),
            deployed=bool(data.get("deployed", False)),
            started_at=str(data.get("started_at", _now_iso())),
            updated_at=str(data.get("updated_at", _now_iso())),
        )


@dataclass
class CicleStateFile:
    """Top level state the orchestrator persists to disk.

    Attributes:
        run_id: Identifier of the run. Defaults to the run directory
            name so a developer can tell runs apart at a glance.
        started_at: ISO 8601 timestamp when the run started.
        updated_at: ISO 8601 timestamp when the last transition ran.
        contracts: Per contract state keyed by contract_id.
    """

    run_id: str
    started_at: str = field(default_factory=_now_iso)
    updated_at: str = field(default_factory=_now_iso)
    contracts: dict[str, CicleState] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON friendly view of the state file."""
        return {
            "run_id": self.run_id,
            "started_at": self.started_at,
            "updated_at": self.updated_at,
            "contracts": {k: v.to_dict() for k, v in self.contracts.items()},
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "CicleStateFile":
        """Build a CicleStateFile from a JSON friendly dictionary."""
        return cls(
            run_id=str(data.get("run_id", "current")),
            started_at=str(data.get("started_at", _now_iso())),
            updated_at=str(data.get("updated_at", _now_iso())),
            contracts={
                k: CicleState.from_dict(v)
                for k, v in data.get("contracts", {}).items()
            },
        )

    def save(self, path: Path) -> None:
        """Persist the state to disk as pretty JSON."""
        path.parent.mkdir(parents=True, exist_ok=True)
        tmp = path.with_suffix(path.suffix + ".tmp")
        tmp.write_text(json.dumps(self.to_dict(), indent=2), encoding="utf-8")
        tmp.replace(path)

    @classmethod
    def load(cls, path: Path) -> "CicleStateFile":
        """Read the state from disk.

        Args:
            path: Absolute path of the state file.
        Returns:
            The loaded state. Empty when the file does not exist.
        """
        if not path.exists():
            return cls(run_id=path.parent.name)
        return cls.from_dict(json.loads(path.read_text(encoding="utf-8")))


def write_jsonl(path: Path, event: dict[str, Any]) -> None:
    """Append a single JSONL event to the log file.

    Args:
        path: Absolute path of the log file.
        event: JSON friendly dictionary.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(event, ensure_ascii=False) + "\n")
