"""Spec-Driven Development agent.

The agent lifts a Contract into a Spec. The agent is deterministic so
the orchestrator can replay the same contract and produce the same
spec. The agent uses the LazyOwn LLM factory when a backend identifier
is configured in payload.json. When the backend is missing or fails,
the agent falls back to a structured template that the operator can
review and amend.

The agent writes the spec as YAML. YAML is the lingua franca for the
infrastructure that consumes the spec, including the test agent and the
CI pipeline.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Optional

import yaml

from .config import Config
from .models import Contract, Finding, SadPath, Severity, Spec
from .validators import check_markdown, check_spec, check_source


SAD_PATH_TEMPLATES = (
    ("missing input", "the agent reports a missing input and exits without writing the spec"),
    ("invalid input type", "the agent coerces the value or raises a typed error"),
    ("external dependency offline", "the agent degrades to the template engine"),
    ("caller asks to skip validation", "the agent refuses and logs a blocker"),
    ("concurrent writer", "the agent writes to a tmp path and renames atomically"),
    ("disk full", "the agent raises IOError and the orchestrator stops the cycle"),
)


@dataclass
class SddResult:
    """Outcome of running the spec agent.

    Attributes:
        spec: The spec the agent produced.
        path: Absolute path of the YAML file the agent wrote.
        findings: DoD findings the agent collected while it wrote the
            spec. The orchestrator halts when the list carries a
            blocker.
    """

    spec: Spec
    path: Path
    findings: list[Finding]


def _coerce_scope(scope: list[str]) -> tuple[list[str], list[SadPath]]:
    """Split the contract scope into inputs and a baseline sad path set.

    The parser lifts bullets from the markdown body. The agent does not
    know whether a bullet is an input, an outcome, or a sad path. The
    helper uses a simple heuristic: a bullet that starts with a verb in
    imperative form becomes a happy path step. A bullet that contains
    the words fail, error, or refuse becomes a sad path.
    """
    inputs: list[str] = []
    sad_paths: list[SadPath] = []
    for bullet in scope:
        lowered = bullet.lower()
        if any(token in lowered for token in ("fail", "error", "refuse", "reject", "missing", "absent")):
            sad_paths.append(
                SadPath(
                    condition=bullet,
                    expected="the implementation handles the failure without crashing",
                )
            )
        else:
            inputs.append(bullet)
    return inputs, sad_paths


def _compose_spec(contract: Contract, min_sad_paths: int) -> Spec:
    """Build a deterministic Spec for a Contract.

    Args:
        contract: The contract the spec implements.
        min_sad_paths: Minimum number of sad paths the spec must carry.
    Returns:
        The composed spec. The agent never returns an empty spec.
    """
    inputs, sad_paths = _coerce_scope(contract.scope)
    for condition, expected in SAD_PATH_TEMPLATES:
        sad_paths.append(SadPath(condition=condition, expected=expected))
    if len(sad_paths) < min_sad_paths:
        for idx in range(min_sad_paths - len(sad_paths)):
            sad_paths.append(
                SadPath(
                    condition=f"boundary condition {idx + 1}",
                    expected="the implementation stays within the documented invariants",
                )
            )
    happy_path = [
        "the operator runs the contract through the orchestrator entry point",
        "the spec agent writes the spec to the run directory",
        "the test agent reads the spec and produces failing tests",
        "the implementation agent reads the spec and the tests",
        "the implementation makes every test green",
        "the reviewer approves the contract",
        "the cicd agent cuts the branch and the pipeline",
    ]
    return Spec(
        contract_id=contract.contract_id,
        goal=contract.title,
        trigger=contract.rationale or "the operator starts the cycle",
        inputs=inputs,
        happy_path=happy_path,
        sad_paths=sad_paths[: max(min_sad_paths, len(sad_paths))],
        data_flow=(
            "the contract lands in the parser, the spec agent writes "
            "the spec, the test agent writes the tests, the implementation "
            "agent writes the source, the reviewer runs the checks"
        ),
        observability=(
            "the operator reads the review report and the cycle log; "
            "the cycle halts on the first blocker"
        ),
        out_of_scope=[
            "changes outside the contract scope",
            "deploys without the human gate token",
        ],
    )


def _render_yaml(spec: Spec) -> str:
    """Render the spec as YAML and return the rendered text."""
    payload: dict[str, Any] = {
        "contract_id": spec.contract_id,
        "goal": spec.goal,
        "trigger": spec.trigger,
        "inputs": spec.inputs,
        "happy_path": spec.happy_path,
        "sad_paths": [
            {"condition": sp.condition, "expected": sp.expected}
            for sp in spec.sad_paths
        ],
        "data_flow": spec.data_flow,
        "observability": spec.observability,
        "out_of_scope": spec.out_of_scope,
        "author": spec.author,
        "created_at": spec.created_at,
    }
    return yaml.safe_dump(payload, sort_keys=False, allow_unicode=True)


def _ask_llm(contract: Contract, backend: str) -> Optional[Spec]:
    """Ask the LazyOwn LLM factory to enrich the spec.

    Args:
        contract: The contract the agent is composing.
        backend: Identifier of the LLM backend.
    Returns:
        The enriched spec when the backend answered with a JSON object
        that matches the spec shape. None when the backend is not
        configured or returned an unparsable payload.
    """
    try:
        from modules.llm_factory import try_get_llm_backend
    except Exception:
        return None
    try:
        llm = try_get_llm_backend(backend)
    except Exception:
        return None
    if llm is None:
        return None
    prompt = (
        "Produce a JSON spec with the keys contract_id, goal, trigger, "
        "inputs, happy_path, sad_paths, data_flow, observability, and "
        "out_of_scope. sad_paths must list at least six items with the "
        "shape {condition, expected}. The contract title is "
        f"{contract.title!r}. The rationale is {contract.rationale!r}. "
        "Do not include emojis or comments. Return only JSON."
    )
    try:
        raw = llm.ask(prompt)
    except Exception:
        return None
    match = re.search(r"\{.*\}", raw, flags=re.DOTALL)
    if not match:
        return None
    try:
        data = json.loads(match.group(0))
    except json.JSONDecodeError:
        return None
    if not isinstance(data, dict):
        return None
    sad_paths = [SadPath.from_dict(sp) for sp in data.get("sad_paths", []) if isinstance(sp, dict)]
    return Spec(
        contract_id=str(data.get("contract_id", contract.contract_id)),
        goal=str(data.get("goal", contract.title)),
        trigger=str(data.get("trigger", contract.rationale)),
        inputs=list(data.get("inputs", [])),
        happy_path=list(data.get("happy_path", [])),
        sad_paths=sad_paths,
        data_flow=str(data.get("data_flow", "")),
        observability=str(data.get("observability", "")),
        out_of_scope=list(data.get("out_of_scope", [])),
    )


def run(contract: Contract, config: Config) -> SddResult:
    """Run the spec agent for one contract.

    Args:
        contract: The contract the spec implements.
        config: Active runtime configuration.
    Returns:
        The result the orchestrator persists and validates.
    """
    spec = _compose_spec(contract, config.max_sad_paths)
    if config.llm_backend:
        enriched = _ask_llm(contract, config.llm_backend)
        if enriched is not None and enriched.sad_paths:
            spec = enriched
    findings: list[Finding] = []
    findings.extend(check_spec(spec, config.max_sad_paths))
    findings.extend(check_markdown(spec.trigger + "\n" + spec.goal, "spec"))
    yaml_text = _render_yaml(spec)
    config.specs_dir().mkdir(parents=True, exist_ok=True)
    spec_path = config.specs_dir() / f"{contract.contract_id}.yaml"
    tmp = spec_path.with_suffix(spec_path.suffix + ".tmp")
    tmp.write_text(yaml_text, encoding="utf-8")
    findings.extend(check_markdown(yaml_text, str(spec_path)))
    findings.extend(check_source(yaml_text, str(spec_path)))
    tmp.replace(spec_path)
    has_block = any(f.severity is Severity.BLOCK for f in findings)
    if has_block:
        return SddResult(spec=spec, path=spec_path, findings=findings)
    return SddResult(spec=spec, path=spec_path, findings=findings)
