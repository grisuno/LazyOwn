"""Chain-aware loop execution: one contract, two transport modes.

When the autonomous planner emits an ``apt_chain <chain> <target>``
decision, this module decides how the chain executes:

- ``stepwise`` (default when eligible): a :class:`ChainRunner` runs the
  chain in-process and every chain step is routed through the worker's
  own :meth:`Worker._guard_step`, so each step inherits scope, deny,
  OS-gate, OPSEC, detection, missing-tool and budget guardrails and is
  recorded in the task traffic log individually. Per-step pacing comes
  from the shared EdrPacer plus the step's own ``sleep``/``jitter``.
- ``subprocess`` (fallback): the whole chain runs through the existing
  shell verb path exactly as before; stepwise is refused when a step
  is not loop-routable or a nested chain exceeds the depth budget.

The mode is chosen by ``payload.json -> orchestrator.chain_mode``
(``auto`` default, or forced ``stepwise``/``subprocess``). Everything
reuses existing contracts: ``chain_registry`` resolves, ``chain_runner``
executes, ``chain_facts`` spools, ``chain_state`` names runs.
"""

from __future__ import annotations

import threading
from collections.abc import Callable
from typing import Any

CHAIN_COMMAND_PREFIX = "apt_chain"
_MAX_CHAIN_NESTING = 2
_MODES = ("auto", "stepwise", "subprocess")

_DEPTH = threading.local()


def chain_mode() -> str:
    """Return the configured chain transport mode for loop runs.

    Returns:
        ``auto``, ``stepwise`` or ``subprocess`` from the payload
        ``orchestrator.chain_mode`` key; unknown values fall back to
        ``auto``.
    """
    try:
        from core.config import load_payload

        section = (load_payload() or {}).get("orchestrator") or {}
        mode = str((section or {}).get("chain_mode", "") or "").strip().lower()
    except Exception:
        return "auto"
    return mode if mode in _MODES else "auto"


def is_chain_command(command: str) -> bool:
    """True when the command line invokes the apt_chain verb."""
    return (command or "").strip().lower().startswith(CHAIN_COMMAND_PREFIX)


def parse_chain_invocation(command: str) -> tuple[str, str, dict[str, str]]:
    """Split one ``apt_chain`` command line into name, target and vars.

    Delegates classification to the shared CLI resolver
    (:func:`cli.apt_chain_support.resolve_invocation`) so the loop and the
    shell accept the exact same chain/target/playbook syntax.

    Args:
        command: Raw command line beginning with ``apt_chain``.

    Returns:
        ``(chain_name, target, vars)`` where the name defaults to the
        base chain and the target may be empty (the worker target wins
        in ``run_chain_stepwise``). A disabled chain file yields the base
        chain name instead.
    """
    try:
        from cli.apt_chain_support import parse_chain_args, resolve_invocation

        rest = command.strip().split(None, 1)
        args = parse_chain_args(rest[1] if len(rest) > 1 else "")
    except Exception:
        return ("", "", {})
    if args.errors or args.admin_action:
        return ("", "", {})
    positionals = [token for token in args.positional if token.lower() != CHAIN_COMMAND_PREFIX]
    chain_name, target, _playbook_override, _disabled = resolve_invocation(
        positionals,
        target_seed=args.target,
        preset_target=args.target,
        policy="lenient",
    )
    return (chain_name or "apt_chain", (target or "").strip(), dict(args.vars))


def stepwise_eligible(chain: Any, routable: Callable[[str], bool] | None = None) -> tuple[bool, str]:
    """Decide whether one chain can run stepwise inside the worker.

    A chain is eligible when every step's command routes through the
    loop executor (registry verbs, shell verbs or CLI verbs). Interactive
    steps are allowed: the worker's intercept queue gates them.

    Args:
        chain: Resolved :class:`modules.chain_registry.Chain`.
        routable: Routability probe (default
            :func:`modules.auto_registry.is_routable_command`).

    Returns:
        ``(eligible, reason)`` with an empty reason when eligible.
    """
    probe = routable
    if probe is None:
        try:
            from modules.auto_registry import is_routable_command as probe  # type: ignore[no-redef]
        except Exception:
            probe = lambda line: False  # noqa: E731
    for step in chain.steps:
        command = (step.run or "").strip()
        if not command:
            return (False, f"step {step.identifier}: empty run")
        if command.lower().startswith(CHAIN_COMMAND_PREFIX) or not probe(command):
            return (False, f"step {step.identifier}: {command[:80]} not loop-routable")
    return (True, "")


class ChainStepBlocked(RuntimeError):
    """A chain step was refused by the worker guardrails (blocked/skipped)."""

    def __init__(self, status: str, detail: str) -> None:
        """Record the guard status and reason.

        Args:
            status: ``blocked`` or ``skipped``.
            detail: Guard reason string.
        """
        super().__init__(f"{status}: {detail}")
        self.status = status
        self.detail = detail


def run_chain_stepwise(
    worker: Any,
    intent: Any,
    command: str,
    executor: Callable[[str], str],
    budget: Any,
    intercept: Any,
    retry_state: dict,
) -> tuple[str, str, str] | None:
    """Run one ``apt_chain`` decision step-by-step inside the worker.

    Every chain step passes through the worker's own
    :meth:`Worker._guard_step`, so guardrails, traffic recording and
    budget accounting apply per step; the shared EdrPacer paces between
    steps and per-step ``sleep``/``jitter`` overrides apply on top.

    Args:
        worker: Live loop worker (needs ``_guard_step``, ``activity``,
            ``_target_for``, ``task_id``).
        intent: Executed intent node.
        command: The ``apt_chain ...`` decision line.
        executor: Worker executor callable for leaf commands.
        budget: Loop budget tracker.
        intercept: Worker intercept queue.
        retry_state: Worker retry state for the current intent.

    Returns:
        ``(output, status, detail)`` exactly like
        :meth:`Worker._guard_step`, or ``None`` when the decision must
        fall through to the whole-chain verb path (unknown chain,
        subprocess mode, or an ineligible chain in auto mode).
    """
    if _DEPTH.__dict__.get("count", 0) >= _MAX_CHAIN_NESTING:
        worker.activity.emit(
            worker.name,
            "block",
            f"chain nesting exceeds {_MAX_CHAIN_NESTING}; refusing: {command[:120]}",
            intent_id=intent.node_id,
        )
        return "", "blocked", "chain nesting limit"
    name, target, extra_vars = parse_chain_invocation(command)
    if not name:
        return None
    try:
        from modules.chain_registry import get as get_chain

        chain = get_chain(name) or get_chain(f"apt_{name}")
    except Exception:
        chain = None
    if chain is None:
        return None
    target = target or worker._target_for(intent)
    mode = chain_mode()
    eligible, reason = stepwise_eligible(chain)
    if not eligible or mode == "subprocess":
        if mode == "stepwise":
            worker.activity.emit(
                worker.name,
                "block",
                f"chain {chain.name}: stepwise forced but ineligible ({reason})",
                intent_id=intent.node_id,
            )
            return "", "blocked", "chain stepwise ineligible"
        return None
    run_id = ""
    try:
        from modules.chain_state import new_run_id

        run_id = new_run_id(f"{worker.task_id}_{chain.name}")
    except Exception:
        run_id = f"{chain.name}_run"

    def guarded(step_command: str) -> str:
        """Route one chain step through the worker's guard path."""
        output, status, detail = worker._guard_step(intent, step_command, executor, budget, intercept, retry_state)
        if status == "ok":
            return output
        raise ChainStepBlocked(status, detail)

    tokens: dict[str, str] = {"target": target, "task_id": str(worker.task_id or "")}
    tokens.update(extra_vars)
    total_timeout = float(chain.total_timeout or 0)
    try:
        runner = _build_runner(chain, guarded, tokens, total_timeout, run_id, worker, intent)
        _DEPTH.count = _DEPTH.__dict__.get("count", 0) + 1
        try:
            result = runner.run()
        finally:
            _DEPTH.count = max(0, _DEPTH.count - 1)
    except ChainStepBlocked as exc:
        worker.activity.emit(
            worker.name,
            "chain",
            f"chain {chain.name} aborted: {exc}",
            intent_id=intent.node_id,
        )
        return "", "blocked", f"chain {chain.name}: {exc.detail}"
    except Exception as exc:
        worker.activity.emit(
            worker.name,
            "chain",
            f"chain {chain.name} error: {exc}",
            intent_id=intent.node_id,
        )
        return f"chain {chain.name} error: {exc}", "ok", ""
    _spool(result)
    summary = _render_summary(result, chain.name)
    worker.activity.emit(
        worker.name,
        "chain",
        f"chain {chain.name} {'ok' if result.ok else 'failed'} "
        f"({sum(1 for s in result.steps if s.ok)}/{len(result.steps)} steps) run_id={result.run_id or run_id}",
        intent_id=intent.node_id,
    )
    return summary, "ok", ""


def _build_runner(
    chain: Any,
    guarded: Callable[[str], str],
    tokens: dict[str, str],
    total_timeout: float,
    run_id: str,
    worker: Any,
    intent: Any,
) -> Any:
    """Build the ChainRunner with per-step telemetry wired to the activity log."""
    from modules.chain_runner import ChainRunner

    def on_step(outcome: Any) -> None:
        """Emit one chain_step telemetry event."""
        worker.activity.emit(
            worker.name,
            "chain_step",
            f"{chain.name}/{outcome.id} [{outcome.status}] {outcome.run[:100]} "
            f"({outcome.duration_ms:.0f}ms)",
            intent_id=intent.node_id,
        )

    replanners: list[Any] = []
    try:
        from cli.apt_chain_support import build_adaptive_replanner, compose_replanners

        replanners.append(build_adaptive_replanner())
    except Exception:
        replanners = []
    return ChainRunner(
        chain,
        tokens=tokens,
        executor=guarded,
        pace=True,
        total_timeout=total_timeout,
        run_id=run_id,
        on_step=on_step,
        replanner=compose_replanners(replanners),
    )


def _spool(result: Any) -> None:
    """Persist chain outputs as facts (best effort)."""
    try:
        from modules.chain_facts import spool_chain_outputs

        spool_chain_outputs(result)
    except Exception:
        pass


def _render_summary(result: Any, chain_name: str) -> str:
    """Render a compact one-block summary of the chain run."""
    try:
        from cli.apt_chain_support import render_result

        lines = render_result(result)
        return "\n".join(lines)
    except Exception:
        statuses = ", ".join(f"{step.id}:{step.status}" for step in result.steps[:12])
        return f"chain {chain_name} ok={result.ok} steps=[{statuses}]"
