"""Orchestrator that wires the agents into a deterministic pipeline.

The orchestrator walks every contract through the same six stages:
spec, test red, implementation green, review, cicd, and done. The
state is persisted to disk after every stage so a crash resumes the
cycle from the last green stage. The orchestrator never blocks on
deploy. The deploy gate stays closed by design.
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from . import bdd_agent, boy_scout, cicd_agent, documentation_agent
from . import parser as parser_mod
from . import reviewer_agent, sdd_agent, tdd_agent
from .config import Config, load_config
from .models import (
    CicleState,
    CicleStateFile,
    Contract,
    Severity,
    Stage,
    write_jsonl,
)
from .parser import load_contracts


@dataclass
class CycleSummary:
    """Top level result of running the orchestrator.

    Attributes:
        run_id: Identifier of the run.
        contracts: Per contract state after the cycle.
        halted_at: Identifier of the contract the orchestrator halted
            on. None when every contract reached the DONE stage.
        halt_reason: Free form text the operator reads to understand
            why the orchestrator halted.
    """

    run_id: str
    contracts: dict[str, CicleState]
    halted_at: Optional[str] = None
    halt_reason: str = ""


def _banner(message: str, config: Config) -> None:
    """Print a stage banner to stderr when verbose mode is on."""
    if not config.verbose:
        return
    print(f"[orchestrator] {message}", file=sys.stderr)


def _halt(summary: CycleSummary, contract_id: str, reason: str) -> CycleSummary:
    """Stamp the summary with a halt reason and return it."""
    summary.halted_at = contract_id
    summary.halt_reason = reason
    return summary


def _persist(state: CicleStateFile, config: Config) -> None:
    """Persist the run state to disk and append a JSONL event."""
    state.updated_at = state.updated_at or ""
    import datetime as _dt

    state.updated_at = _dt.datetime.now(_dt.timezone.utc).isoformat()
    state.save(config.state_path())
    write_jsonl(
        config.log_path(),
        {
            "run_id": state.run_id,
            "contract_id": next(
                iter(state.contracts), ""
            ),
            "stage": (
                next(iter(state.contracts.values())).stage.value
                if state.contracts
                else "pending"
            ),
            "timestamp": state.updated_at,
        },
    )


def _load_state(config: Config) -> CicleStateFile:
    """Read the persisted state and return it."""
    return CicleStateFile.load(config.state_path())


def _seed_state(contracts: list[Contract], state: CicleStateFile) -> None:
    """Add new contracts to the state without overwriting existing ones."""
    for contract in contracts:
        if contract.contract_id in state.contracts:
            continue
        state.contracts[contract.contract_id] = CicleState(contract=contract)


def _run_spec(state: CicleState, config: Config) -> CicleState:
    """Run the spec agent and update the state."""
    _banner(f"spec: {state.contract.contract_id}", config)
    result = sdd_agent.run(state.contract, config)
    state.spec_path = result.path
    state.stage = Stage.SDD
    blockers = [f for f in result.findings if f.severity is Severity.BLOCK]
    if blockers:
        state.stage = Stage.PENDING
        raise RuntimeError(
            f"spec blockers for {state.contract.contract_id}: "
            + ", ".join(f.message for f in blockers)
        )
    return state


def _run_test(state: CicleState, config: Config) -> CicleState:
    """Run the test agent and update the state."""
    from .models import Spec

    _banner(f"test red: {state.contract.contract_id}", config)
    if state.spec_path is None:
        raise RuntimeError("spec path missing; cannot run tdd agent")
    spec = _load_spec(state.spec_path)
    result = tdd_agent.run(state.contract, spec, config)
    state.test_path = result.suite.test_path
    state.stage = Stage.TDD
    if not result.red:
        raise RuntimeError(
            f"tdd stage did not reach red for {state.contract.contract_id}"
        )
    return state


def _run_implementation(state: CicleState, config: Config) -> CicleState:
    """Run the implementation agent and update the state."""
    from .models import Spec, TestSuite

    _banner(f"implementation green: {state.contract.contract_id}", config)
    if state.spec_path is None or state.test_path is None:
        raise RuntimeError("spec or test path missing; cannot run bdd agent")
    spec = _load_spec(state.spec_path)
    suite = TestSuite(
        contract_id=state.contract.contract_id,
        test_path=state.test_path,
        expected_outcome="GREEN",
    )
    result = bdd_agent.run(state.contract, spec, suite, config)
    state.src_path = result.source_path
    state.stage = Stage.BDD
    if not result.green:
        raise RuntimeError(
            f"bdd stage did not reach green for {state.contract.contract_id}"
        )
    return state


def _run_review(state: CicleState, config: Config) -> CicleState:
    """Run the reviewer and update the state."""
    _banner(f"review: {state.contract.contract_id}", config)
    report = reviewer_agent.run(state, config)
    state.review_path = reviewer_agent.write_report(report, config)
    state.stage = Stage.REVIEW
    state.approved = report.approved
    if not report.approved:
        raise RuntimeError(
            f"reviewer blocked {state.contract.contract_id}: "
            + report.summary
        )
    return state


def _run_documentation(state: CicleState, config: Config) -> CicleState:
    """Run the documentation agent and update the state."""
    from .models import ReviewReport

    _banner(f"docs: {state.contract.contract_id}", config)
    if state.spec_path is None:
        raise RuntimeError("spec path missing; cannot document")
    spec = _load_spec(state.spec_path)
    report: Optional[ReviewReport] = None
    if state.review_path is not None and state.review_path.exists():
        report = ReviewReport.from_dict(
            json.loads(state.review_path.read_text(encoding="utf-8"))
        )
    result = documentation_agent.run(state.contract, spec, report, config)
    state.doc_path = result.path
    return state


def _run_scout(state: CicleState, config: Config) -> CicleState:
    """Run the boy scout pass and update the state."""
    _banner(f"scout: {state.contract.contract_id}", config)
    report = boy_scout.run(state, config)
    boy_scout.write_report(report, config)
    return state


def _run_cicd(
    state: CicleState,
    config: Config,
    *,
    auto_commit: bool,
    deploy_token: Optional[str],
) -> CicleState:
    """Run the cicd agent and update the state."""
    from .models import ReviewReport

    _banner(f"cicd: {state.contract.contract_id}", config)
    if state.spec_path is None or state.review_path is None:
        raise RuntimeError("spec or review path missing; cannot run cicd agent")
    spec = _load_spec(state.spec_path)
    report = ReviewReport.from_dict(
        json.loads(state.review_path.read_text(encoding="utf-8"))
    )
    if not report.approved:
        raise RuntimeError("review not approved; cicd agent will not ship")
    result = cicd_agent.run(
        state.contract,
        spec,
        report,
        config,
        auto_commit=auto_commit,
        deploy_token=deploy_token,
    )
    state.branch_name = result.branch
    state.pipeline_path = result.pipeline_path
    state.pr_body_path = result.pr_body_path
    state.stage = Stage.CICD
    state.deployed = result.deployed
    if result.findings:
        raise RuntimeError(
            f"cicd blockers for {state.contract.contract_id}: "
            + ", ".join(result.findings)
        )
    return state


def _load_spec(path) -> "Spec":
    """Load a spec file as YAML and return a Spec dataclass.

    Args:
        path: Absolute path of the spec file. The file is expected
            to be valid YAML that maps to the Spec dataclass shape.
    Returns:
        The loaded Spec.
    """
    import yaml as _yaml

    from .models import Spec

    data = _yaml.safe_load(path.read_text(encoding="utf-8"))
    return Spec.from_dict(data)


def _advance(state: CicleStateFile, contract_id: str, config: Config, options: dict) -> None:
    """Walk one contract through every stage.

    Args:
        state: Run state the orchestrator mutates.
        contract_id: Identifier of the contract the stage runs for.
        config: Active runtime configuration.
        options: CLI options the orchestrator forwards to the cicd
            agent.
    """
    cycle_state = state.contracts[contract_id]
    if cycle_state.stage in (Stage.DONE, Stage.CICD):
        return
    if cycle_state.stage in (Stage.PENDING,):
        _run_spec(cycle_state, config)
        _persist(state, config)
    if cycle_state.stage in (Stage.SDD,):
        _run_test(cycle_state, config)
        _persist(state, config)
    if cycle_state.stage in (Stage.TDD,):
        _run_implementation(cycle_state, config)
        _persist(state, config)
    if cycle_state.stage in (Stage.BDD,):
        _run_review(cycle_state, config)
        _persist(state, config)
    if cycle_state.stage in (Stage.REVIEW,):
        _run_documentation(cycle_state, config)
        _run_scout(cycle_state, config)
        _persist(state, config)
    if cycle_state.stage in (Stage.REVIEW,):
        _run_cicd(
            cycle_state,
            config,
            auto_commit=options.get("auto_commit", False),
            deploy_token=options.get("deploy_token"),
        )
        _persist(state, config)
    cycle_state.stage = Stage.DONE
    _persist(state, config)


def run(config: Config, options: dict) -> CycleSummary:
    """Run the orchestrator for the current run directory.

    Args:
        config: Active runtime configuration.
        options: CLI options the orchestrator forwards to the cicd
            agent.
    Returns:
        The cycle summary the CLI prints.
    """
    config.ensure()
    contracts = load_contracts(config, seeds=options.get("seeds"))
    if not contracts:
        raise RuntimeError("no contracts found; add CONTRACT headings to CLAUDE.md")
    state = _load_state(config)
    _seed_state(contracts, state)
    _persist(state, config)
    summary = CycleSummary(run_id=state.run_id, contracts=state.contracts)
    for contract in contracts:
        try:
            _advance(state, contract.contract_id, config, options)
        except RuntimeError as error:
            return _halt(summary, contract.contract_id, str(error))
    return summary


def _print_summary(summary: CycleSummary) -> None:
    """Print the cycle summary to stdout."""
    print(json.dumps(summary_to_dict(summary), indent=2))


def summary_to_dict(summary: CycleSummary) -> dict:
    """Return a JSON friendly view of the summary."""
    return {
        "run_id": summary.run_id,
        "halted_at": summary.halted_at,
        "halt_reason": summary.halt_reason,
        "contracts": {
            cid: {
                "stage": state.stage.value,
                "approved": state.approved,
                "deployed": state.deployed,
                "branch": state.branch_name,
            }
            for cid, state in summary.contracts.items()
        },
    }


def _build_parser() -> argparse.ArgumentParser:
    """Build the CLI argument parser and return it."""
    parser = argparse.ArgumentParser(prog="claude_md_orchestrator")
    parser.add_argument("--claude-md", help="absolute path of the CLAUDE.md to parse")
    parser.add_argument("--run-dir", help="absolute path of the run directory")
    parser.add_argument(
        "--auto-commit",
        action="store_true",
        help="commit the artifacts on the feature branch",
    )
    parser.add_argument(
        "--deploy-token",
        default=None,
        help="shared secret the cicd agent checks before it deploys",
    )
    parser.add_argument(
        "--seed",
        action="append",
        default=[],
        metavar="ID",
        help="seed contract id to inject when CLAUDE.md has none",
    )
    parser.add_argument(
        "--no-parse",
        action="store_true",
        help="skip the markdown parser and run only the seeded contracts",
    )
    parser.add_argument(
        "--contract-file",
        action="append",
        default=[],
        help="path of a markdown file that holds a single CONTRACT block",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="treat every blocker as a halt trigger (default is non strict)",
    )
    return parser


def _load_seed_contracts(args, options: dict) -> list[Contract]:
    """Build the seeded contracts the CLI requested.

    Args:
        args: Parsed CLI arguments.
        options: Options dict the orchestrator passes to the agents.
    Returns:
        The list of contracts the operator asked for. The function
        combines the explicit --seed ids and the --contract-file
        content the operator supplied.
    """
    seeds: list[Contract] = []
    for seed_id in options.get("seeds", []):
        seeds.append(
            Contract(
                contract_id=seed_id["contract_id"],
                title=seed_id.get("title", seed_id["contract_id"]),
                rationale=seed_id.get("rationale", "seeded contract"),
            )
        )
    for path_str in args.contract_file:
        path = Path(path_str).expanduser().resolve()
        if path.exists():
            text = path.read_text(encoding="utf-8")
            seeds.extend(parser_mod.parse_claude_md(path))
    return seeds


def main(argv: Optional[list[str]] = None) -> int:
    """Run the orchestrator CLI and return the process exit code."""
    parser = _build_parser()
    args = parser.parse_args(argv)
    config = load_config()
    if args.claude_md:
        config.claude_md_path = Path(args.claude_md).expanduser().resolve()
    if args.run_dir:
        config.run_dir = Path(args.run_dir).expanduser().resolve()
    if not args.strict:
        config.reviewer_strict = False
    options = {
        "auto_commit": args.auto_commit,
        "deploy_token": args.deploy_token,
        "seeds": [
            {"contract_id": seed, "title": seed, "rationale": "seeded contract"}
            for seed in args.seed
        ],
    }
    if args.no_parse:
        config.claude_md_path = Path("/dev/null")
        if not options["seeds"] and not args.contract_file:
            raise SystemExit("--no-parse requires --seed or --contract-file")
        for path_str in args.contract_file:
            path = Path(path_str).expanduser().resolve()
            if not path.exists():
                continue
            for contract in parser_mod.parse_claude_md(path):
                options["seeds"].append(
                    {
                        "contract_id": contract.contract_id,
                        "title": contract.title,
                        "rationale": contract.rationale,
                    }
                )
    summary = run(config, options)
    _print_summary(summary)
    if summary.halted_at is not None:
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
