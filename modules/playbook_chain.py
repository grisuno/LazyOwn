"""Playbook to chain lowering: one contract, one destination.

Every playbook phase becomes ordered chain steps. Declared
``phases[].steps[]`` actions map by ``kind`` (atomic, command,
lazyscript, lua, plugin, lazyaddon, chain); the phase's ``atomic_tests``
lower to a single ``atomic_emulate`` step per technique, exactly the
contract ``do_atomic_emulate`` already executes. The produced chain
validates through ``chain_registry.validate_chain`` so the runner is
the only executor, and the loop reaches playbooks through the same
``apt_chain`` decision path as every other chain.
"""

from __future__ import annotations

import os
import re
from typing import Any

import yaml

from modules.apt_playbooks import ACTION_KINDS, AptPlaybook, PlaybookAction
from modules.chain_registry import Chain, ChainStep, validate_chain

_CHAIN_NAME_RE = re.compile(r"[^a-z0-9_]+")
_MAX_ACTION_TIMEOUT = 3600
_ATOMIC_EMULATE_TEMPLATE = "atomic_emulate --target {target} --techniques {techniques}"


def slugify(name: str) -> str:
    """Return a chain-safe slug for a playbook name."""
    slug = _CHAIN_NAME_RE.sub("_", str(name or "").strip().lower()).strip("_")
    return slug or "playbook"


def _action_to_step(action: PlaybookAction, phase_name: str, index: int) -> ChainStep | None:
    """Map one playbook action to a chain step (None when not expressible)."""
    run = (action.run or "").strip()
    kind = action.kind if action.kind in ACTION_KINDS else "command"
    if kind in ("lazyscript",) and run and not run.startswith(("lazyscript", "resource")):
        run = f"lazyscript {run}"
    elif kind in ("lua", "plugin"):
        pass
    elif kind == "lazyaddon" and run and not run.startswith("lazy_addon"):
        run = f"lazy_addon run {run}"
    elif kind == "atomic":
        techniques = (run or action.technique_id or "").strip()
        if not techniques:
            return None
        run = _ATOMIC_EMULATE_TEMPLATE.format(target="{target}", techniques=techniques)
    if not run:
        return None
    step_id = f"{slugify(phase_name) or 'phase'}_{index}_{kind}"
    return ChainStep(
        run=run,
        id=step_id,
        phase=phase_name,
        description=action.name or f"{kind} action from phase {phase_name}",
        when=action.when,
        timeout=max(0, min(int(action.timeout or 0), _MAX_ACTION_TIMEOUT)),
        retries=0,
        continue_on_error=bool(action.continue_on_error),
        capture=action.capture,
        sleep=float(action.sleep or 0.0),
        jitter=float(action.jitter or 0.0),
        sinks=[str(value) for value in action.sinks if str(value).strip()],
    )


def playbook_to_chain(
    playbook: AptPlaybook,
    target: str = "",
    playbook_dir: str = "playbooks",
) -> tuple[Chain | None, list[str]]:
    """Lower one playbook into a validated in-memory chain.

    Args:
        playbook: Loaded :class:`AptPlaybook`.
        target: Default target token rendered into every step.
        playbook_dir: Unused hook kept for caller symmetry.

    Returns:
        ``(chain, errors)``; the chain is None when no step survives
        the lowering.
    """
    steps: list[ChainStep] = []
    for phase in playbook.phases:
        phase_index = len(steps)
        for offset, action in enumerate(phase.steps):
            step = _action_to_step(action, phase.name, phase_index + offset)
            if step is not None:
                steps.append(step)
        techniques = [
            test.atomic_id
            for test in phase.atomic_tests
            if (test.atomic_id or "").strip() and not test.manual
        ]
        if techniques:
            step = _action_to_step(
                PlaybookAction(kind="atomic", run=",".join(techniques), technique_id=phase.technique_id),
                phase.name,
                len(steps),
            )
            if step is not None:
                steps.append(step)
    if not steps:
        return (None, ["playbook produced no executable steps"])
    name = f"playbook_{slugify(playbook.apt_name)}"
    chain = Chain(
        name=name,
        description=playbook.description or f"Lowered chain for playbook {playbook.apt_name}",
        version=2,
        tags=[f"playbook:{slugify(playbook.apt_name)}", "playbook"],
        platforms=[str(item) for item in playbook.platforms],
        defaults={"target": str(target or "")} if target else {},
        steps=steps,
    )
    errors = validate_chain(_chain_to_raw(chain), filename=name, chains_dir=None)
    if errors:
        return (None, errors)
    return (chain, [])


def _chain_to_raw(chain: Chain) -> dict[str, Any]:
    """Serialize a chain back to its raw mapping for validation."""
    raw: dict[str, Any] = {
        "name": chain.name,
        "description": chain.description,
        "version": chain.version,
        "tags": list(chain.tags),
        "platforms": list(chain.platforms),
        "defaults": dict(chain.defaults),
        "steps": [
            {
                "id": step.id,
                "run": step.run,
                "phase": step.phase,
                "description": step.description,
                "when": step.when,
                "timeout": step.timeout,
                "continue_on_error": step.continue_on_error,
                "capture": step.capture,
                "sleep": step.sleep,
                "jitter": step.jitter,
                "sinks": list(step.sinks),
            }
            for step in chain.steps
        ],
    }
    return {key: value for key, value in raw.items() if value not in (None, "", [], {}) or key in ("steps",)}


def write_playbook_chain(chain: Chain, chains_dir: str = "chains") -> str:
    """Persist a lowered chain next to the shipped ones.

    Args:
        chain: Validated lowered chain.
        chains_dir: Destination directory (defaults to ``chains/``).

    Returns:
        The written file path.
    """
    path = os.path.join(chains_dir, f"{chain.name}.yaml")
    os.makedirs(chains_dir, exist_ok=True)
    document = _chain_to_raw(chain)
    document["enabled"] = True
    with open(path, "w", encoding="utf-8") as handle:
        yaml.safe_dump(document, handle, sort_keys=False)
    return path
