"""Single execution engine for YAML orchestration chains.

``chain_registry`` resolves and validates; this module executes. It owns
step conditions, timeouts, retries, error policy, output capture (text,
regex and JSON), post-step verification, pre-step LLM-predicted
pre-checks, parallel step groups, branching, approval gates, checkpoints
and the structured result every caller (CLI, loop, MCP) consumes. It
never retries a successful step, never hides a failure unless the YAML
asked for it, and never writes to the graph directly: sink tags travel
in the result so the outcome bus can fan them out.
"""

from __future__ import annotations

import concurrent.futures as futures
import glob
import json
import os
import re
import shlex
import subprocess
import time
from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Any

from modules.chain_registry import Chain, ChainStep, evaluate_when
from modules.chain_state import new_run_id, write_checkpoint

_TOKEN_RE = re.compile(r"\{([A-Za-z_][A-Za-z0-9_]*)\}")
_SHELL_META = re.compile(r"[;&|<>`$]")
_MAX_CAPTURE_CHARS = 2000
_DEFAULT_TIMEOUT = 300.0
_MAX_RETRIES = 5
_MAX_TOTAL_TIMEOUT = 86_400.0
_VERIFY_TIMEOUT = 120.0
_MAX_STEP_RUNS = 3
_MAX_REPLAN_INSERTS = 3
_MAX_EXPECT_EXITS = 8
_EXPECT_EXIT_MAX = 255
_MAX_PARALLEL_GROUP = 8
_MAX_FALLBACK_DEPTH = 1


@dataclass
class StepOutcome:
    """One executed or skipped step."""

    id: str = ""
    run: str = ""
    phase: str = ""
    status: str = "pending"
    output: str = ""
    reason: str = ""
    attempts: int = 0
    captured: str = ""
    verify_output: str = ""
    artifacts: list[str] = field(default_factory=list)
    sinks: list[str] = field(default_factory=list)
    duration_ms: float = 0.0

    @property
    def ok(self) -> bool:
        """Return True for success, dry-run and skipped steps."""
        return self.status in ("ok", "dry-run", "skipped")

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-serializable view."""
        return {
            "id": self.id,
            "run": self.run,
            "phase": self.phase,
            "status": self.status,
            "output": self.output,
            "reason": self.reason,
            "attempts": self.attempts,
            "captured": bool(self.captured),
            "verify_output": self.verify_output,
            "artifacts": list(self.artifacts),
            "sinks": list(self.sinks),
            "duration_ms": round(self.duration_ms, 2),
        }


@dataclass
class ChainRunResult:
    """Structured result of one chain execution."""

    name: str = ""
    target: str = ""
    ok: bool = True
    aborted: bool = False
    reason: str = ""
    run_id: str = ""
    steps: list[StepOutcome] = field(default_factory=list)
    variables: dict[str, str] = field(default_factory=dict)
    artifacts: list[str] = field(default_factory=list)
    branches: list[str] = field(default_factory=list)
    filtered: int = 0
    started_at: float = 0.0
    finished_at: float = 0.0
    plan_warnings: list[str] = field(default_factory=list)
    fallback_used: str = ""
    fallback_depth: int = 0

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-serializable view."""
        return {
            "name": self.name,
            "target": self.target,
            "ok": self.ok,
            "aborted": self.aborted,
            "reason": self.reason,
            "run_id": self.run_id,
            "steps": [step.to_dict() for step in self.steps],
            "variables": dict(self.variables),
            "artifacts": list(self.artifacts),
            "branches": list(self.branches),
            "filtered": self.filtered,
            "started_at": self.started_at,
            "finished_at": self.finished_at,
            "plan_warnings": list(self.plan_warnings),
            "fallback_used": self.fallback_used,
            "fallback_depth": self.fallback_depth,
            "duration_ms": round(max(0.0, self.finished_at - self.started_at) * 1000, 2),
        }


@dataclass
class ReplanContext:
    """What one replanner may do after a step executes.

    The runner owns the context: a replanner records desired changes and
    the runner applies them under its own caps, so a misbehaving advice
    source cannot break the chain invariants.
    """

    chain_name: str = ""
    target: str = ""
    outcome: StepOutcome | None = None
    executed_ids: list[str] = field(default_factory=list)
    variables: dict[str, str] = field(default_factory=dict)
    _vars: dict[str, str] = field(default_factory=dict)
    _inserts: list[ChainStep] = field(default_factory=list)
    _skip_rest: bool = False

    def set_var(self, name: str, value: str) -> None:
        """Record a variable the next steps should see."""
        if _TOKEN_RE.fullmatch(f"{{{name}}}") is not None:
            self._vars[name] = str(value)[:_MAX_CAPTURE_CHARS]

    def insert_step(self, step: ChainStep) -> None:
        """Record one step to execute right after the finished step."""
        if isinstance(step, ChainStep) and str(step.run).strip():
            self._inserts.append(step)

    def skip_rest(self) -> None:
        """Record that remaining steps must not execute."""
        self._skip_rest = True

    @property
    def applied_vars(self) -> dict[str, str]:
        """Return recorded variable changes."""
        return dict(self._vars)

    @property
    def inserted(self) -> list[ChainStep]:
        """Return recorded steps to insert."""
        return list(self._inserts)

    @property
    def skip_rest_flag(self) -> bool:
        """Return True when remaining steps should be skipped."""
        return self._skip_rest


def render_text(template: str, variables: dict[str, str]) -> str:
    """Substitute single-brace tokens in one pass."""
    text = str(template or "")
    for key, value in variables.items():
        text = text.replace("{" + key + "}", str(value))
    return text


class ChainRunner:
    """Execute one chain with per-step policy and structured outcomes."""

    def __init__(
        self,
        chain: Chain,
        tokens: dict[str, str] | None = None,
        shell: Any = None,
        executor: Callable[[str], str] | None = None,
        default_timeout: float = _DEFAULT_TIMEOUT,
        dry_run: bool = False,
        on_step: Callable[[StepOutcome], None] | None = None,
        retry_backoff: float = 0.5,
        total_timeout: float = 0.0,
        approver: Callable[[str, str], bool] | None = None,
        checkpoint_dir: str | os.PathLike | None = None,
        run_id: str = "",
        resume_state: dict[str, Any] | None = None,
        step_filter: set[str] | None = None,
        replanner: Callable[[ReplanContext], None] | None = None,
        command_filter: Callable[[str], str] | None = None,
        fallback_loader: Callable[[str], Chain | None] | None = None,
        max_fallback_depth: int = _MAX_FALLBACK_DEPTH,
        fallback_depth: int = 0,
    ) -> None:
        """Bind the chain, the execution primitive and operator switches.

        Args:
            chain: Chain to execute.
            tokens: Chain tokens (target, playbook, artefact paths...).
            shell: Live cmd2 shell for verb steps (None uses raw exec).
            executor: Optional alternative execution primitive.
            default_timeout: Per-step wall clock fallback.
            dry_run: Resolve without executing anything.
            on_step: Optional per-step observer callback.
            retry_backoff: Base seconds between retry attempts.
            total_timeout: Whole-chain wall clock cap (0 disables).
            approver: Callback for ``confirm`` steps (None: denied).
            checkpoint_dir: When set, persist resumable checkpoints.
            run_id: Explicit run id (else generated with checkpointing).
            resume_state: Previously saved checkpoint to continue from.
            step_filter: Restrict execution to these step ids.
            replanner: Optional after-step advice hook.
            command_filter: Optional transform applied to every command
                (run and verify) right before execution, such as the
                retry-session ``sudo -A`` askpass rewrite. A filter
                error keeps the original command instead of aborting.
            fallback_loader: Resolver for the chain's ``fallback``
                name (default: ``chain_registry.get``).
            max_fallback_depth: How many fallback hops one run may take.
            fallback_depth: Current fallback depth (internal).
        """
        self.chain = chain
        self.tokens = {str(key): str(value) for key, value in (tokens or {}).items()}
        self.shell = shell
        self.executor = executor
        self.default_timeout = max(1.0, float(default_timeout or _DEFAULT_TIMEOUT))
        self.dry_run = bool(dry_run)
        self.on_step = on_step
        self.retry_backoff = max(0.0, float(retry_backoff))
        self.total_timeout = min(_MAX_TOTAL_TIMEOUT, max(0.0, float(total_timeout or 0.0)))
        self.approver = approver
        self.checkpoint_dir = checkpoint_dir
        self.run_id = str(run_id or "")
        self.step_filter = {str(item) for item in (step_filter or set()) if str(item)}
        self.replanner = replanner
        self.command_filter = command_filter
        self.fallback_loader = fallback_loader
        self.max_fallback_depth = max(0, int(max_fallback_depth))
        self.fallback_depth = max(0, int(fallback_depth))
        self.resume_state = resume_state if isinstance(resume_state, dict) else None
        self._replan_inserts_total = 0

    def run(self) -> ChainRunResult:
        """Execute the chain in order and return every step outcome."""
        started = time.time()
        state = self.resume_state if isinstance(self.resume_state, dict) else {}
        state_variables = {str(key): str(value) for key, value in (state.get("variables") or {}).items()}
        variables = {**self.chain.defaults, **self.chain.vars, **state_variables, **self.tokens}
        captured_keys: set[str] = {str(key) for key in (state.get("captured_keys") or [])}
        resumed_ok = {
            str(entry.get("id"))
            for entry in (state.get("steps") or [])
            if isinstance(entry, dict) and entry.get("status") in ("ok", "dry-run", "skipped")
        }
        steps = list(self.chain.steps)
        filtered = 0
        if self.step_filter:
            filtered = sum(1 for step in steps if step.identifier not in self.step_filter)
            steps = [step for step in steps if step.identifier in self.step_filter]
        if not self.run_id and self.checkpoint_dir:
            self.run_id = new_run_id(self.chain.name)
            result_run_id = self.run_id
        else:
            result_run_id = self.run_id
        result = ChainRunResult(
            name=self.chain.name,
            target=str(self.tokens.get("target", "") or ""),
            started_at=started,
            run_id=result_run_id,
            filtered=filtered,
        )
        self._save_checkpoint(result, variables, captured_keys, 0, "running")
        step_index: dict[str, int] = {step.identifier: pos for pos, step in enumerate(steps)}
        executions: dict[str, int] = {}
        index = 0
        while 0 <= index < len(steps):
            if self.total_timeout and (time.time() - started) > self.total_timeout:
                result.steps.extend(self._skip_remaining(steps, index, "total timeout"))
                result.ok = False
                result.aborted = True
                result.reason = f"total timeout exceeded ({self.total_timeout:.0f}s)"
                break
            step = steps[index]
            executions[step.identifier] = executions.get(step.identifier, 0) + 1
            if executions[step.identifier] > _MAX_STEP_RUNS and not self.dry_run:
                outcome = StepOutcome(
                    id=step.identifier,
                    run=render_text(step.run, variables),
                    phase=step.phase,
                    status="skipped",
                    reason="loop guard: step already ran three times",
                )
                result.steps.append(outcome)
                result.ok = False
                result.aborted = True
                result.reason = f"loop guard: {step.identifier} exceeded {_MAX_STEP_RUNS} runs"
                break
            if step.identifier in resumed_ok:
                outcome = StepOutcome(
                    id=step.identifier,
                    run=render_text(step.run, variables),
                    phase=step.phase,
                    status="skipped",
                    reason="resumed (already completed)",
                )
                result.steps.append(outcome)
                self._notify(outcome)
                index += 1
                continue
            if step.parallel and not self.dry_run:
                group = [step]
                cursor = index + 1
                while cursor < len(steps) and steps[cursor].parallel and len(group) < _MAX_PARALLEL_GROUP:
                    group.append(steps[cursor])
                    cursor += 1
                outcomes, group_failure = self._run_parallel_group(group, executions, resumed_ok, variables, captured_keys)
                result.steps.extend(outcomes)
                for group_outcome in outcomes:
                    for artifact in group_outcome.artifacts:
                        if artifact and artifact not in result.artifacts:
                            result.artifacts.append(artifact)
                    self._notify(group_outcome)
                replan_skip = False
                for group_outcome in outcomes:
                    if self._apply_replanner(result, cursor - 1, group_outcome, steps, step_index, variables, captured_keys):
                        replan_skip = True
                        break
                self._save_checkpoint(result, variables, captured_keys, cursor, "running")
                if replan_skip:
                    break
                if group_failure:
                    result.ok = False
                    result.aborted = True
                    result.reason = group_failure
                    break
                index = cursor
                continue
            outcome = self._run_step(step, variables, captured_keys)
            result.steps.append(outcome)
            for artifact in outcome.artifacts:
                if artifact and artifact not in result.artifacts:
                    result.artifacts.append(artifact)
            self._notify(outcome)
            replan_skip = self._apply_replanner(result, index, outcome, steps, step_index, variables, captured_keys)
            self._save_checkpoint(result, variables, captured_keys, index + 1, "running")
            if replan_skip:
                break
            if not outcome.ok:
                if outcome.status == "denied":
                    if not step.continue_on_error:
                        result.ok = False
                        result.aborted = True
                        result.reason = f"{outcome.id}: {outcome.reason or 'denied'}"
                        break
                    index += 1
                elif outcome.status != "skipped" and step.on_fail:
                    target_index = step_index.get(step.on_fail, -1)
                    if target_index >= 0:
                        result.branches.append(f"{step.identifier} --fail--> {step.on_fail}")
                        index = target_index
                        continue
                    if not step.continue_on_error:
                        result.ok = False
                        result.aborted = True
                        result.reason = f"{outcome.id}: {outcome.reason or 'failed'}"
                        break
                    index += 1
                else:
                    if not step.continue_on_error:
                        result.ok = False
                        result.aborted = True
                        result.reason = f"{outcome.id}: {outcome.reason or 'failed'}"
                        break
                    index += 1
            elif outcome.status == "ok" and step.on_success:
                target_index = step_index.get(step.on_success, -1)
                if target_index >= 0:
                    result.branches.append(f"{step.identifier} --success--> {step.on_success}")
                    index = target_index
                    continue
                index += 1
            else:
                index += 1
        result.ok = all(step.ok for step in result.steps) and not result.aborted
        if (
            not result.ok
            and not self.dry_run
            and self.chain.fallback
            and self.chain.fallback != self.chain.name
            and self.fallback_depth < self.max_fallback_depth
        ):
            pre_fallback_count = len(result.steps)
            self._run_fallback_chain(result, variables, captured_keys, started)
            fallback_outcomes = result.steps[pre_fallback_count:]
            if result.fallback_used and fallback_outcomes:
                if all(outcome.ok for outcome in fallback_outcomes):
                    result.ok = True
                    result.aborted = False
                    result.reason = ""
        if self.dry_run:
            try:
                from modules.verb_manifest import plan_check

                result.plan_warnings = plan_check(steps, dict(variables))
            except Exception:
                result.plan_warnings = []
        result.variables = dict(variables)
        result.finished_at = time.time()
        state_name = "aborted" if result.aborted else "finished"
        self._save_checkpoint(result, variables, captured_keys, index, state_name)
        return result

    def _skip_remaining(self, steps: list[ChainStep], start: int, reason: str) -> list[StepOutcome]:
        """Build skipped outcomes for steps that will not execute."""
        skipped: list[StepOutcome] = []
        for step in steps[start:]:
            skipped.append(
                StepOutcome(
                    id=step.identifier,
                    run=render_text(step.run, {}),
                    phase=step.phase,
                    status="skipped",
                    reason=reason,
                )
            )
        return skipped

    def _run_parallel_group(
        self,
        group: list[ChainStep],
        executions: dict[str, int],
        resumed_ok: set[str],
        variables: dict[str, str],
        captured_keys: set[str],
    ) -> tuple[list[StepOutcome], str]:
        """Execute consecutive ``parallel`` steps concurrently.

        Every step runs through the same ``_run_step`` policy path in its
        own worker thread; the runner waits for the whole group before
        the next sequential step. Outcomes come back in declaration
        order. Parallel steps never capture or branch (registry
        validation forbids it), so threads never race on shared state.

        Args:
            group: Consecutive parallel steps in declaration order.
            executions: Per-step execution counters (loop guard).
            resumed_ok: Step ids already completed in a resumed run.
            variables: Shared variable map (read-only for the group).
            captured_keys: Untrusted-capture key set (read-only).

        Returns:
            Tuple of (outcomes in declaration order, failure reason).
            The failure reason is empty unless a step failed without
            ``continue_on_error``.
        """
        outcomes: list[StepOutcome] = []
        runnable: list[ChainStep] = []
        for step in group:
            executions[step.identifier] = executions.get(step.identifier, 0) + 1
            if step.identifier in resumed_ok:
                outcomes.append(
                    StepOutcome(
                        id=step.identifier,
                        run=render_text(step.run, variables),
                        phase=step.phase,
                        status="skipped",
                        reason="resumed (already completed)",
                    )
                )
            else:
                runnable.append(step)
        exceeded = [step for step in runnable if executions[step.identifier] > _MAX_STEP_RUNS]
        if exceeded:
            for step in runnable:
                outcomes.append(
                    StepOutcome(
                        id=step.identifier,
                        run=render_text(step.run, variables),
                        phase=step.phase,
                        status="skipped",
                        reason="loop guard: step already ran three times",
                    )
                )
            return outcomes, f"loop guard: {exceeded[0].identifier} exceeded {_MAX_STEP_RUNS} runs"
        thread_outcomes: dict[str, StepOutcome] = {}
        if runnable:
            pool = futures.ThreadPoolExecutor(max_workers=min(len(runnable), _MAX_PARALLEL_GROUP))
            scheduled = [
                (step, pool.submit(self._run_step, step, dict(variables), set(captured_keys)))
                for step in runnable
            ]
            try:
                for step, future in scheduled:
                    try:
                        thread_outcomes[step.identifier] = future.result()
                    except Exception as exc:
                        thread_outcomes[step.identifier] = StepOutcome(
                            id=step.identifier,
                            run=render_text(step.run, variables),
                            phase=step.phase,
                            status="failed",
                            reason=str(exc)[:300],
                        )
            finally:
                pool.shutdown(wait=False, cancel_futures=True)
        by_id = {step.identifier: step for step in group}
        for step in group:
            executed = thread_outcomes.get(step.identifier)
            if executed is not None:
                outcomes.append(executed)
        failure = ""
        for outcome in outcomes:
            step = by_id.get(outcome.id)
            if outcome.ok or step is None or step.continue_on_error:
                continue
            failure = f"{outcome.id}: {outcome.reason or 'failed'}"
            break
        return outcomes, failure

    def _run_fallback_chain(
        self,
        result: ChainRunResult,
        variables: dict[str, str],
        captured_keys: set[str],
        started: float,
    ) -> None:
        """Execute the chain's ``fallback`` chain after a failed run.

        The fallback runs with the same tokens and run id so
        checkpoints, sinks and downstream correlation stay in one
        bucket. Depth is capped by ``max_fallback_depth`` so a fallback
        loop cannot recurse forever; a total-timeout overrun skips the
        fallback entirely instead of exceeding the operator budget.
        """
        loader = self.fallback_loader
        if loader is None:
            try:
                from modules.chain_registry import get as _registry_get

                loader = _registry_get
            except Exception:
                return
        name = (self.chain.fallback or "").strip()
        if not name:
            return
        try:
            fallback_chain = loader(name)
        except Exception:
            fallback_chain = None
        if fallback_chain is None or fallback_chain.name == self.chain.name:
            return
        remaining = self.total_timeout - (time.time() - started) if self.total_timeout else 0.0
        if self.total_timeout and remaining <= 0.0:
            return
        sub = ChainRunner(
            fallback_chain,
            tokens=self.tokens,
            shell=self.shell,
            executor=self.executor,
            default_timeout=self.default_timeout,
            dry_run=False,
            on_step=self.on_step,
            retry_backoff=self.retry_backoff,
            total_timeout=max(0.0, remaining),
            approver=self.approver,
            checkpoint_dir=self.checkpoint_dir,
            run_id=self.run_id,
            replanner=self.replanner,
            command_filter=self.command_filter,
            fallback_loader=self.fallback_loader,
            max_fallback_depth=self.max_fallback_depth,
            fallback_depth=self.fallback_depth + 1,
        )
        try:
            sub_result = sub.run()
        except Exception:
            return
        result.fallback_used = fallback_chain.name
        result.fallback_depth = self.fallback_depth + 1
        result.branches.append(f"{self.chain.name} --fail--> {fallback_chain.name}")
        result.steps.extend(sub_result.steps)
        for artifact in sub_result.artifacts:
            if artifact and artifact not in result.artifacts:
                result.artifacts.append(artifact)
        result.branches.extend(sub_result.branches)
        result.variables.update(sub_result.variables)
        if not result.reason:
            result.reason = sub_result.reason

    def _notify(self, outcome: StepOutcome) -> None:
        """Invoke the on_step callback, swallowing its errors."""
        if self.on_step is None:
            return
        try:
            self.on_step(outcome)
        except Exception:
            pass

    def _apply_replanner(
        self,
        result: ChainRunResult,
        index: int,
        outcome: StepOutcome,
        steps: list[ChainStep],
        step_index: dict[str, int],
        variables: dict[str, str],
        captured_keys: set[str],
    ) -> bool:
        """Consult the replanner after an executed step; returns skip flag."""
        if self.replanner is None or outcome.status in ("skipped", "denied"):
            return False
        context = ReplanContext(
            chain_name=self.chain.name,
            target=result.target,
            outcome=outcome,
            executed_ids=[entry.id for entry in result.steps],
            variables=dict(variables),
        )
        try:
            self.replanner(context)
        except Exception:
            return False
        if context.skip_rest_flag:
            result.steps.extend(self._skip_remaining(steps, index + 1, "skip_rest (replanner)"))
            index_end = len(steps)
            self._save_checkpoint(
                result,
                variables,
                captured_keys,
                index_end,
                "finished",
            )
            return True
        for position, inserted in enumerate(context.inserted):
            if self._replan_inserts_total >= _MAX_REPLAN_INSERTS:
                break
            if inserted.identifier in step_index:
                continue
            self._replan_inserts_total += 1
            steps.insert(index + 1 + position, inserted)
            for join, later_step in enumerate(steps):
                step_index[later_step.identifier] = join
        for name, value in context.applied_vars.items():
            variables[name] = value
            captured_keys.add(name)
        return False

    def _save_checkpoint(
        self,
        result: ChainRunResult,
        variables: dict[str, str],
        captured_keys: set[str],
        next_index: int,
        state_name: str,
    ) -> None:
        """Persist a resumable snapshot when checkpointing is enabled."""
        if not self.checkpoint_dir or self.dry_run or not self.run_id:
            return
        try:
            write_checkpoint(
                self.checkpoint_dir,
                {
                    "run_id": self.run_id,
                    "chain": self.chain.name,
                    "target": result.target,
                    "state": state_name,
                    "variables": {**result.variables, **variables} if state_name != "running" else dict(variables),
                    "captured_keys": sorted(captured_keys),
                    "steps": [
                        {"id": entry.id, "status": entry.status, "reason": entry.reason} for entry in result.steps
                    ],
                    "next_index": int(next_index),
                    "started_at": result.started_at,
                    "ok": bool(result.ok),
                    "aborted": bool(result.aborted),
                    "reason": result.reason,
                    "branches": result.branches,
                },
            )
        except Exception:
            pass

    def _run_step(
        self,
        step: ChainStep,
        variables: dict[str, str],
        captured_keys: set[str],
    ) -> StepOutcome:
        """Resolve and run one step according to its policy."""
        rendered = self._render_command(step.run, variables, captured_keys)
        outcome = StepOutcome(
            id=step.identifier,
            run=rendered,
            phase=step.phase,
            artifacts=list(step.artifacts),
            sinks=list(step.sinks),
        )
        if step.when and not evaluate_when(step.when, variables):
            outcome.status = "skipped"
            outcome.reason = "when false"
            return outcome
        skip_path = render_text(step.skip_if_exists, variables) if step.skip_if_exists else ""
        if skip_path and os.path.exists(skip_path):
            outcome.status = "skipped"
            outcome.reason = f"exists: {skip_path}"
            return outcome
        if step.resolve_newest_glob and step.resolve_newest_as:
            matches = sorted(glob.glob(render_text(step.resolve_newest_glob, variables)), key=os.path.getmtime)
            if not matches:
                outcome.status = "skipped"
                outcome.reason = "no newest match"
                return outcome
            variables[step.resolve_newest_as] = os.path.abspath(matches[-1])
            rendered = self._render_command(step.run, variables, captured_keys)
            outcome.run = rendered
        unresolved = _TOKEN_RE.search(rendered)
        if unresolved:
            outcome.status = "skipped"
            outcome.reason = f"unresolved token: {unresolved.group(0)}"
            return outcome
        outcome.run = rendered
        if self.dry_run:
            outcome.status = "dry-run"
            return outcome
        if step.pre_check:
            pre_ok, pre_out, pre_reason = self._execute(
                self._render_command(step.pre_check, variables, captured_keys),
                self._pre_check_timeout(step),
            )
            if not pre_ok:
                outcome.status = "skipped"
                outcome.reason = f"pre_check failed: {pre_reason or 'no output'}"
                outcome.verify_output = pre_out[:_MAX_CAPTURE_CHARS]
                return outcome
        if step.confirm:
            if self.approver is None:
                outcome.status = "denied"
                outcome.reason = "confirm step and no approver bound"
                return outcome
            if not self._ask_approval(step.identifier, rendered):
                outcome.status = "denied"
                outcome.reason = "approval denied"
                return outcome
        started = time.time()
        attempts = 0
        attempts_allowed = max(0, min(_MAX_RETRIES, int(step.retries or 0))) + 1
        while attempts < attempts_allowed:
            attempts += 1
            ok, output, reason = self._execute(rendered, step.timeout, tuple(step.expect_exit))
            outcome.attempts = attempts
            outcome.output = output
            outcome.reason = reason
            if ok and step.expect and step.expect not in output:
                ok = False
                outcome.reason = f"expected text missing: {step.expect[:80]}"
            if ok and step.verify:
                verify_ok, verify_out, verify_reason = self._execute(
                    self._render_command(step.verify, variables, captured_keys),
                    self._verify_timeout(step),
                )
                outcome.verify_output = verify_out
                if not verify_ok:
                    ok = False
                    outcome.reason = f"verify failed: {verify_reason or 'no output'}"
            if ok:
                outcome.status = "ok"
                outcome.duration_ms = (time.time() - started) * 1000
                self._store_capture(step, output, outcome, variables, captured_keys)
                outcome.artifacts = [
                    render_text(path, variables) for path in step.artifacts if render_text(path, variables)
                ]
                return outcome
            if attempts < attempts_allowed and self.retry_backoff:
                time.sleep(min(self.retry_backoff * attempts, 3.0))
        outcome.status = "timeout" if outcome.reason == "timeout" else "failed"
        outcome.duration_ms = (time.time() - started) * 1000
        return outcome

    def _ask_approval(self, step_id: str, command: str) -> bool:
        """Ask the bound approver, failure-closed."""
        if self.approver is None:
            return False
        try:
            return bool(self.approver(step_id, command))
        except Exception:
            return False

    def _verify_timeout(self, step: ChainStep) -> float:
        """Return the wall clock budget for one verification command."""
        if step.timeout:
            return float(step.timeout)
        return min(self.default_timeout, _VERIFY_TIMEOUT)

    def _pre_check_timeout(self, step: ChainStep) -> float:
        """Return the wall clock budget for one pre-check command."""
        return self._verify_timeout(step)

    def _store_capture(
        self,
        step: ChainStep,
        output: str,
        outcome: StepOutcome,
        variables: dict[str, str],
        captured_keys: set[str],
    ) -> None:
        """Fill ``captured`` and derived variables from raw output.

        Capture order: regex (named groups become variables, the first
        value also lands in ``capture``), then JSON keys. Everything a
        capture produces becomes an untrusted key, so later raw shell
        steps re-render it quoted.
        """
        captured = ""
        if step.capture_regex:
            try:
                match = re.search(step.capture_regex, output)
            except re.error:
                match = None
            if match is not None:
                extracted = match.group(1) if match.groups else match.group(0)
                captured = str(extracted or "")[:_MAX_CAPTURE_CHARS]
                for name, value in (match.groupdict() or {}).items():
                    if value is not None and name:
                        variables[str(name)] = str(value)[:_MAX_CAPTURE_CHARS]
                        captured_keys.add(str(name))
        if step.capture_json:
            parsed = self._first_json(output)
            if isinstance(parsed, dict):
                keys = [key.strip() for key in step.capture_json.split(",") if key.strip()]
                for key in keys:
                    if key in parsed and parsed[key] is not None:
                        variables[key] = str(parsed[key])[:_MAX_CAPTURE_CHARS]
                        captured_keys.add(key)
                if not captured:
                    try:
                        captured = json.dumps(parsed)[:_MAX_CAPTURE_CHARS]
                    except (TypeError, ValueError):
                        captured = ""
        if step.capture:
            if captured:
                variables[step.capture] = captured
                captured_keys.add(step.capture)
            elif output.strip():
                captured = output.strip()[:_MAX_CAPTURE_CHARS]
                variables[step.capture] = captured
                captured_keys.add(step.capture)
        outcome.captured = captured

    @staticmethod
    def _first_json(output: str) -> Any:
        """Return the first JSON object embedded in the output, or None."""
        text = str(output or "")
        decoder = json.JSONDecoder()
        for position, char in enumerate(text):
            if char != "{":
                continue
            try:
                value, _ = decoder.raw_decode(text[position:])
            except ValueError:
                continue
            return value
        return None

    def _render_command(self, template: str, variables: dict[str, str], captured_keys: set[str]) -> str:
        """Render a command, quoting values produced by earlier captures.

        Captured output is untrusted (banners, HTTP bodies, tool output).
        Raw shell steps receive it single-quoted so shell metacharacters
        cannot escape into the operator host. cmd2 verbs keep the raw
        string because the verb owns its own argument handling.
        """
        text = str(template or "")
        quote = not self._is_verb(text)
        for key, value in variables.items():
            replacement = shlex.quote(str(value)) if quote and key in captured_keys else str(value)
            text = text.replace("{" + key + "}", replacement)
        return text

    def _execute(
        self,
        command: str,
        timeout: int,
        expect_exits: tuple[int, ...] = (),
    ) -> tuple[bool, str, str]:
        """Run one command with an optional timeout and return (ok, output, reason).

        The bound ``command_filter`` (retry sessions) rewrites the line
        first; a filter failure keeps the original command.
        """
        if self.command_filter is not None:
            try:
                command = str(self.command_filter(command))
            except Exception:
                pass
        limit = float(timeout or self.default_timeout)
        allowed = {
            code
            for code in expect_exits[:_MAX_EXPECT_EXITS]
            if isinstance(code, int) and 0 <= code <= _EXPECT_EXIT_MAX
        }
        if self.executor is not None:
            return self._call(lambda: self.executor(command), limit)
        if self.shell is None:
            return False, "", "no executor or shell"
        if self._is_verb(command):
            try:
                return True, self._run_shell_verb(command, limit), ""
            except TimeoutError as exc:
                return False, (str(exc) or "verb timeout")[:200], "timeout"
            except Exception as exc:
                return False, "", str(exc)[:300]
        return self._call(lambda: self._run_raw(command, limit, allowed), limit)

    def _is_verb(self, command: str) -> bool:
        """Return True when the first token is a live cmd2 verb or alias."""
        aliases = getattr(self.shell, "aliases", {}) or {}
        try:
            token = shlex.split(command)[0]
        except (ValueError, IndexError):
            return False
        if not token or _SHELL_META.search(command):
            return False
        return callable(getattr(self.shell, f"do_{token}", None)) or token in aliases

    def _run_shell_verb(self, command: str, timeout: float = 0.0) -> str:
        """Run a cmd2 verb on the calling thread and capture its stdout.

        Verbs stay on the operator thread (cmd2 is not thread-safe). The
        step timeout is enforced with a ``SIGALRM`` watchdog on the main
        thread when available; a hung verb raises ``TimeoutError`` so
        :meth:`_execute` can fail the step instead of stalling the chain.

        LazyOwn ``do_*`` methods print through Rich and usually return
        ``None``; capturing the buffer is what makes ``capture:`` and
        ``expect:`` work for verb steps.

        Args:
            command: The rendered verb line to execute.
            timeout: Wall-clock limit in seconds (0 disables).

        Returns:
            The captured stdout/stderr text.

        Raises:
            TimeoutError: When the watchdog fires before completion.
        """
        import contextlib
        import io
        import math
        import signal
        import threading

        alarm_seconds = max(0, int(math.ceil(float(timeout or 0.0))))
        use_alarm = (
            alarm_seconds > 0
            and threading.current_thread() is threading.main_thread()
            and hasattr(signal, "SIGALRM")
        )

        def _raise_timeout(_signum: int, _frame: Any) -> None:
            raise TimeoutError(f"verb timeout after {alarm_seconds}s: {command[:80]}")

        buffer = io.StringIO()
        previous_handler = None
        if use_alarm:
            previous_handler = signal.signal(signal.SIGALRM, _raise_timeout)
            signal.alarm(alarm_seconds)
        try:
            with contextlib.redirect_stdout(buffer), contextlib.redirect_stderr(buffer):
                result = self.shell.onecmd(command)
        finally:
            if use_alarm:
                signal.alarm(0)
                signal.signal(signal.SIGALRM, previous_handler or signal.SIG_DFL)
        text = buffer.getvalue()
        if not text.strip() and result not in (None, True, False):
            text = str(result)
        return text

    def _run_raw(self, command: str, timeout: float, allowed: frozenset[int] | set[int] = frozenset()) -> str:
        """Run an ordinary command through the shared safe shell primitive."""
        from core.safe_exec import safe_run_shell

        completed = safe_run_shell(
            command,
            allow=True,
            reason=f"YAML chain step: {command[:80]}",
            timeout=timeout,
        )
        output = ((completed.stdout or "") + (completed.stderr or "")).strip()
        if completed.returncode != 0 and completed.returncode not in allowed:
            extra = "" if not allowed else f" (expected one of {sorted(allowed)})"
            raise RuntimeError(f"exit {completed.returncode}{extra}: {output[-300:]}")
        return output

    @staticmethod
    def _call(callback: Callable[[], Any], timeout: float) -> tuple[bool, str, str]:
        """Run a callback in a worker thread and enforce the timeout."""
        executor = futures.ThreadPoolExecutor(max_workers=1)
        future = executor.submit(callback)
        try:
            output = future.result(timeout=timeout)
            text = "" if output is None else str(output)
            return True, text, ""
        except (futures.TimeoutError, subprocess.TimeoutExpired):
            future.cancel()
            return False, "", "timeout"
        except Exception as exc:
            return False, "", str(exc)[:300]
        finally:
            executor.shutdown(wait=False, cancel_futures=True)


__all__ = ["ChainRunResult", "ChainRunner", "ReplanContext", "StepOutcome", "render_text"]
