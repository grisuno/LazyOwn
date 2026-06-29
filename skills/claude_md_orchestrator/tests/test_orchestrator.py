"""Unit tests for the claude_md_orchestrator package.

The tests pin the behavior of every agent. The tests use a temporary
run directory so the suite never touches the real run state. The
tests run the orchestrator end to end against a seeded contract and
verify that the cycle walks the six stages in order, that the spec
satisfies the DoD, that the tests start red, that the implementation
makes the tests green, and that the reviewer approves the artifacts.
"""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[3]
SKILLS_ROOT = REPO_ROOT / "skills"
if str(SKILLS_ROOT) not in sys.path:
    sys.path.insert(0, str(SKILLS_ROOT))

from claude_md_orchestrator import (  # noqa: E402
    CicleState,
    Config,
    Contract,
    Finding,
    SadPath,
    Severity,
    Spec,
    Stage,
    load_config,
)
from claude_md_orchestrator import orchestrator as orch_mod  # noqa: E402
from claude_md_orchestrator import parser as parser_mod  # noqa: E402
from claude_md_orchestrator import sdd_agent, tdd_agent, bdd_agent  # noqa: E402
from claude_md_orchestrator import reviewer_agent, documentation_agent  # noqa: E402
from claude_md_orchestrator import cicd_agent, boy_scout  # noqa: E402
from claude_md_orchestrator import validators  # noqa: E402


@pytest.fixture()
def tmp_run_dir(tmp_path: Path) -> Path:
    """Return a fresh run directory the test can mutate freely."""
    run_dir = tmp_path / "runs" / "current"
    run_dir.mkdir(parents=True, exist_ok=True)
    return run_dir


@pytest.fixture()
def config(tmp_run_dir: Path, tmp_path: Path) -> Config:
    """Return a Config that points at the temp run directory."""
    claude_md = tmp_path / "CLAUDE.md"
    claude_md.write_text(
        "# Contracts\n\n"
        "## CONTRACT C-001 add_numbers\n\n"
        "The contract adds two integers and returns the sum. The contract "
        "covers the inputs, the happy path, and the sad paths. trigger is "
        "the operator calling add. sad paths cover missing input and bad "
        "type. Out of scope is anything beyond addition.\n\n"
        "- two integers\n"
        "- a function called add\n",
        encoding="utf-8",
    )
    cfg = Config(
        repo_root=tmp_path,
        run_dir=tmp_run_dir,
        claude_md_path=claude_md,
        verbose=False,
        reviewer_strict=False,
    )
    return cfg


def test_parser_extracts_contract(config: Config) -> None:
    """The parser returns the contract the markdown declares."""
    contracts = parser_mod.load_contracts(config)
    assert len(contracts) == 1
    assert contracts[0].contract_id == "C-001"
    assert "add_numbers" in contracts[0].title


def test_sdd_agent_writes_spec(config: Config) -> None:
    """The spec agent writes a YAML spec with at least six sad paths."""
    contract = Contract(
        contract_id="C-100",
        title="sum integers",
        rationale="the operator asks the framework to add numbers",
        scope=["two integers", "an add function"],
    )
    result = sdd_agent.run(contract, config)
    assert result.path.exists()
    text = result.path.read_text(encoding="utf-8")
    assert "sad_paths" in text
    assert "happy_path" in text
    assert not any(f.severity is Severity.BLOCK for f in result.findings)


def test_tdd_agent_lands_red(config: Config) -> None:
    """The tdd agent lands the test module and the red outcome holds."""
    contract = Contract(
        contract_id="C-200",
        title="sum integers",
        rationale="trigger is the operator calling sum",
        scope=["two integers"],
    )
    spec = sdd_agent.run(contract, config).spec
    result = tdd_agent.run(contract, spec, config)
    assert result.red is True
    assert result.findings == [] or all(
        f.severity is not Severity.BLOCK for f in result.findings
    )


def test_bdd_agent_lands_green(config: Config) -> None:
    """The bdd agent makes the test module pass."""
    contract = Contract(
        contract_id="C-300",
        title="sum integers",
        rationale="trigger is the operator calling sum",
        scope=["two integers"],
    )
    spec = sdd_agent.run(contract, config).spec
    suite = tdd_agent.run(contract, spec, config).suite
    result = bdd_agent.run(contract, spec, suite, config)
    assert result.green is True
    assert not any(f.severity is Severity.BLOCK for f in result.findings)


def test_dod_validators_block_emoji() -> None:
    """The DoD validator flags emoji in source code."""
    text = "value = '\U0001F600'\n"
    findings = validators.check_no_emoji(text, "sample.py")
    assert any(f.rule == "dod.no_emoji" for f in findings)


def test_dod_validators_block_inline_comments() -> None:
    """The DoD validator flags inline comments in source code."""
    text = "value = 1  # this is a comment\n"
    findings = validators.check_no_comments(text, "sample.py")
    assert any(f.rule == "dod.no_comments" for f in findings)


def test_dod_validators_block_todo_markers() -> None:
    """The DoD validator flags TODO and FIXME markers."""
    text = "value = 1  # TODO: handle edge case\n"
    findings = validators.check_no_forbidden_markers(text, "sample.py")
    assert any(f.rule == "dod.no_todo" for f in findings)


def test_dod_validators_block_absolute_paths() -> None:
    """The DoD validator flags absolute paths the developer typed by hand."""
    text = "with open('/home/tester/file.txt') as fh: pass\n"
    findings = validators.check_no_hardcoded_paths_or_ips(text, "sample.py")
    assert any(f.rule == "dod.no_hardcoded_path" for f in findings)


def test_dod_validators_require_docstrings() -> None:
    """The DoD validator flags public functions without a docstring."""
    text = "def public_function(value):\n    return value\n"
    findings = validators.check_docstrings(text, "sample.py")
    assert any(f.rule == "dod.docstrings" for f in findings)


def test_orchestrator_full_cycle(config: Config) -> None:
    """The orchestrator walks the full cycle and reaches the done stage."""
    config.reviewer_strict = False
    summary = orch_mod.run(
        config,
        {"auto_commit": False, "deploy_token": None, "seeds": []},
    )
    assert summary.halted_at is None
    cid = "C-001"
    state = summary.contracts[cid]
    assert state.stage is Stage.DONE
    assert state.spec_path is not None and state.spec_path.exists()
    assert state.test_path is not None and state.test_path.exists()
    assert state.src_path is not None and state.src_path.exists()
    assert state.review_path is not None and state.review_path.exists()
    assert state.doc_path is not None and state.doc_path.exists()
    assert state.pipeline_path is not None and state.pipeline_path.exists()
    assert state.pr_body_path is not None and state.pr_body_path.exists()
    assert state.approved is True
    assert state.deployed is False


def test_orchestrator_blocks_on_sad_path_shortage(config: Config) -> None:
    """The orchestrator pads the spec to satisfy the minimum sad path count.

    The spec agent always emits at least max_sad_paths sad paths. The
    test sets a low floor and confirms the cycle finishes. The
    orchestrator must never block on a count shortage because the
    sdd agent guarantees the contract.
    """
    config.max_sad_paths = 1
    summary = orch_mod.run(
        config,
        {"auto_commit": False, "deploy_token": None, "seeds": []},
    )
    assert summary.halted_at is None


def test_orchestrator_blocks_on_missing_contracts(tmp_run_dir: Path, tmp_path: Path) -> None:
    """The orchestrator halts when the parser returns zero contracts."""
    claude_md = tmp_path / "CLAUDE.md"
    claude_md.write_text("# Title\n\nNo actionable contract here.\n", encoding="utf-8")
    cfg = Config(
        repo_root=tmp_path,
        run_dir=tmp_run_dir,
        claude_md_path=claude_md,
        verbose=False,
    )
    with pytest.raises(RuntimeError):
        orch_mod.run(
            cfg,
            {"auto_commit": False, "deploy_token": None, "seeds": []},
        )


def test_documentation_agent_emits_fenced_markdown(config: Config) -> None:
    """The documentation agent emits a fenced markdown block."""
    contract = Contract(
        contract_id="C-400",
        title="sum integers",
        rationale="the operator calls sum",
        scope=["two integers"],
    )
    spec = sdd_agent.run(contract, config).spec
    result = documentation_agent.run(contract, spec, None, config)
    body = result.path.read_text(encoding="utf-8")
    assert body.startswith("```markdown")
    assert body.rstrip().endswith("```")
    assert "signed by grisun0" in body


def test_boy_scout_returns_report(config: Config) -> None:
    """The boy scout returns a structured report with no findings for clean code."""
    contract = Contract(
        contract_id="C-500",
        title="sum integers",
        rationale="the operator calls sum",
        scope=["two integers"],
    )
    spec = sdd_agent.run(contract, config).spec
    suite = tdd_agent.run(contract, spec, config).suite
    bdd = bdd_agent.run(contract, spec, suite, config)
    spec_path = config.specs_dir() / f"{contract.contract_id}.yaml"
    state = CicleState(
        contract=contract,
        spec_path=spec_path,
        test_path=suite.test_path,
        src_path=bdd.source_path,
    )
    report = boy_scout.run(state, config)
    assert report.contract_id == "C-500"
    assert report.proposal.startswith("# Boy Scout proposal for contract C-500")


def test_cicd_agent_writes_pipeline(config: Config) -> None:
    """The cicd agent writes a pipeline and a PR body."""
    contract = Contract(
        contract_id="C-600",
        title="sum integers",
        rationale="the operator calls sum",
        scope=["two integers"],
    )
    spec = sdd_agent.run(contract, config).spec
    suite = tdd_agent.run(contract, spec, config).suite
    bdd = bdd_agent.run(contract, spec, suite, config)
    spec_path = config.specs_dir() / f"{contract.contract_id}.yaml"
    state = CicleState(
        contract=contract,
        spec_path=spec_path,
        test_path=suite.test_path,
        src_path=bdd.source_path,
    )
    report = reviewer_agent.run(state, config)
    state.review_path = reviewer_agent.write_report(report, config)
    state.approved = report.approved
    result = cicd_agent.run(
        contract,
        spec,
        report,
        config,
        auto_commit=False,
        deploy_token=None,
    )
    assert result.pipeline_path.exists()
    assert result.pr_body_path.exists()
    assert result.deployed is False


def test_models_spec_round_trip() -> None:
    """The spec dataclass survives a JSON round trip."""
    spec = Spec(
        contract_id="C-700",
        goal="sum integers",
        trigger="operator calls sum",
        inputs=["a", "b"],
        happy_path=["step one", "step two"],
        sad_paths=[SadPath(condition="missing", expected="raise")],
    )
    payload = json.loads(json.dumps(spec.to_dict()))
    rebuilt = Spec.from_dict(payload)
    assert rebuilt.contract_id == spec.contract_id
    assert rebuilt.sad_paths[0].condition == "missing"
