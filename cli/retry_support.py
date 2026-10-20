"""Retry support - resume logic shared by the ``retry`` CLI surface.

The CommandSet (``cli.commands.retry_ops``) stays thin: argument parsing,
checkpoint selection, variable overrides, elevated-sudo arming and the
actual relaunch live here, mirroring the ``apt_chain`` support split.

Relaunch semantics:

- chain: :func:`modules.retry_session.newest_failed_checkpoint` picks
  the freshest aborted/failed checkpoint (chain-name or run-id selector),
  the recorded variables rehydrate as tokens and every ``--var
  key=value`` wins over them. The ChainRunner keeps the same run id, so
  the resumed attempt is auditable against the stored checkpoint.
- loop: the last non-complete task (TaskStore) or an explicit task id
  re-enters :func:`modules.lazy_runner.run_loop` with the ordinary
  ``auto_loop`` flags, so the operator can vary rounds, target, budget.
- elevation: ``--sudo`` arms :mod:`modules.retry_session` after a
  warned confirmation; command lines flow through
  :func:`modules.retry_session.apply_sudo_askpass` so bare ``sudo``
  invocations switch to ``sudo -A`` without touching operators' code.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from cli.apt_chain_support import build_cli_approver
from modules.chain_registry import CHAINS_DIR
from modules.chain_registry import get as get_chain
from modules.chain_runner import ChainRunner
from modules.retry_session import (
    apply_sudo_askpass,
    newest_failed_checkpoint,
    resolve_sudo_consent,
    set_sudo_secret,
    sudo_gate_open,
)
from utils import print_msg

RUN_ID_PARTS_MIN = 2
_FAILED_TASK_HINT_STATUSES = ("failed", "timeout", "exhausted", "paused")
_MAX_REASON_CHARS = 300


def looks_like_run_id(token: str) -> bool:
    """Return True when the token reads as a chain run id, not a name.

    Args:
        token: Operator-provided selector.

    Returns:
        True when the token carries the ``<slug>_<date>_<pid>`` shape
        rather than a plain chain name.
    """
    raw = str(token or "").strip()
    if not raw or raw.isdigit():
        return False
    return raw.count("_") >= RUN_ID_PARTS_MIN and any(part.isdigit() for part in raw.split("_"))


@dataclass
class LastTask:
    """One non-complete loop task candidate for ``retry loop``.

    Args:
        task_id: Task id (``tNNNN``).
        status: TaskStore status (failed, timeout, exhausted, paused).
        goal: The goal text the task chased.
    """

    task_id: str = ""
    status: str = ""
    goal: str = ""

    @property
    def known(self) -> bool:
        """Return True when a task record exists."""
        return bool(self.task_id)


def last_loop_task() -> LastTask:
    """Return the last non-complete task from the TaskStore.

    Returns:
        LastTask; ``known`` False when the store has no candidate.
    """
    try:
        from modules.lazy_loop import TaskStore

        rows = TaskStore().list()
    except Exception:
        return LastTask()
    for row in reversed(rows):
        status = str(row.get("status", ""))
        if status in _FAILED_TASK_HINT_STATUSES:
            return LastTask(
                task_id=str(row.get("task_id", "")),
                status=status,
                goal=str(row.get("goal", ""))[:160],
            )
    return LastTask()


def status_snapshot(limit: int = 5) -> dict:
    """Collect retry-relevant state: failed checkpoints + last task.

    Args:
        limit: Rows per listing.

    Returns:
        Mapping with ``checkpoint_rows`` (newest failed first),
        ``last_task`` and ``sudo_armed`` for the operator summary.
    """
    from modules.chain_state import checkpoint_dir, list_checkpoints

    scan_limit = max(128, limit * 16)
    rows = [
        row
        for row in list_checkpoints(directory=checkpoint_dir(), limit=scan_limit)
        if row.get("state") == "aborted" or not row.get("ok", True)
    ][: max(1, limit)]
    return {
        "checkpoint_rows": rows,
        "last_task": last_loop_task(),
        "sudo_armed": sudo_gate_open(),
    }


def consent_to_elevate(rest: list[str], confirmer) -> tuple[bool, str]:
    """Resolve ``--sudo`` for one retry invocation.

    Args:
        rest: Token list of the retry subcommand; ``--sudo`` toggles.
        confirmer: Warned-confirmation callable returning the answer
            ( ``(str) -> str`` ); None refuses the mode fail-closed.

    Returns:
        (armed, note). ``armed`` True only when the warning was accepted
        and a password was provided; the note explains refusals.

    Raises:
        ValueError: Never surfaced; getpass EOF yields a note instead.
    """
    if "--sudo" not in rest:
        return False, ""
    armed, note = resolve_sudo_consent(confirmer, True)
    if not armed:
        return False, note
    import getpass

    try:
        secret = getpass.getpass("sudo password for this retry session: ")
    except (EOFError, KeyboardInterrupt):
        return False, "--sudo aborted while reading the password"
    if not secret.strip():
        return False, "--sudo aborted: no password provided"
    set_sudo_secret(secret)
    if not sudo_gate_open():
        return False, "elevation arming failed; communication stayed unprivileged"
    return True, "elevated retry session armed; secret file removed on shell exit"


@dataclass
class RetryChainReport:
    """Outcome of one chain relaunch attempt.

    Args:
        chain: Resumed chain name.
        run_id: Checkpoint run id (kept identical to the failed run).
        next_index: Step index the run resumed at.
        ok: True when every step ended ok / skipped / dry-run.
        reason: Failure reason of the relaunch (empty on success).
        executed: Resolved step lines executed this attempt.
        skipped: Step ids skipped (already done / guards).
        error: Checkpoint or registry problem that blocked the relaunch.
        variables: Starting tokens after user overrides.
    """

    chain: str = ""
    run_id: str = ""
    next_index: int = 0
    ok: bool = True
    reason: str = ""
    executed: list[str] = field(default_factory=list)
    skipped: list[str] = field(default_factory=list)
    error: str = ""
    variables: dict[str, str] = field(default_factory=dict)

    def to_dict(self) -> dict:
        """Return a JSON-serializable view."""
        return {
            "chain": self.chain,
            "run_id": self.run_id,
            "next_index": self.next_index,
            "ok": self.ok,
            "reason": self.reason,
            "executed": list(self.executed),
            "skipped": list(self.skipped),
            "error": self.error,
            "variables": dict(self.variables),
        }


def retry_chain(
    chain_or_run: str,
    shell=None,
    extra_vars: dict[str, str] | None = None,
    dry_run: bool = False,
) -> RetryChainReport:
    """Resume a failed chain, applying user-varied tokens.

    Args:
        chain_or_run: Chain name (newest failed) or explicit run id.
        shell: Live shell for verb steps (None keeps raw execution).
        extra_vars: ``--var key=value`` overrides on recorded variables.
        dry_run: Resolve without executing (verify a varied config first).

    Returns:
        RetryChainReport; ``error`` explains selection/registry issues.
    """
    extra_vars = {str(key): str(value) for key, value in (extra_vars or {}).items()}
    selector = str(chain_or_run or "").strip()
    if looks_like_run_id(selector):
        state = newest_failed_checkpoint(run_id=selector)
    else:
        state = newest_failed_checkpoint(chain=selector)
    if not state:
        return RetryChainReport(error="no failed checkpoint for: " + (selector or "(newest)"))
    chain_name = str(state.get("chain", "") or "")
    chain = get_chain(chain_name, chains_dir=CHAINS_DIR)
    if chain is None:
        source = _chain_state_when_disabled(chain_name)
        if source == "disabled":
            return RetryChainReport(chain=chain_name, error=f"chain disabled: apt_chain enable {chain_name}")
        return RetryChainReport(chain=chain_name, error="chain file no longer validates")
    tokens = {str(key): str(value) for key, value in (state.get("variables") or {}).items()}
    tokens.update(extra_vars)
    try:
        start_at = int(state.get("next_index", 0))
    except (TypeError, ValueError):
        return RetryChainReport(
            chain=chain_name, run_id=str(state.get("run_id", "")), error="checkpoint next_index unreadable"
        )
    runner = ChainRunner(
        chain,
        tokens=tokens,
        shell=shell,
        dry_run=dry_run,
        approver=build_cli_approver(print_msg),
        checkpoint_dir=None,
        run_id=str(state.get("run_id", "")),
        resume_state=state,
        command_filter=apply_sudo_askpass if sudo_gate_open() else None,
    )
    result = runner.run()
    return RetryChainReport(
        chain=result.name,
        run_id=result.run_id,
        next_index=start_at,
        ok=result.ok,
        reason=str(result.reason or "")[:_MAX_REASON_CHARS],
        executed=[step.run for step in result.steps if step.status == "ok"],
        skipped=[f"{step.id}: {step.reason}" for step in result.steps if step.status == "skipped"],
        variables=tokens,
    )


def _chain_state_when_disabled(chain_name: str) -> str:
    """Inspect the registry scan for a missing chain name.

    Args:
        chain_name: Chain name looked up.

    Returns:
        ``disabled`` when present but switched off, empty otherwise.
    """
    from modules.chain_registry import scan_all

    for row in scan_all(chains_dir=CHAINS_DIR):
        if str(row.get("name", "")) == chain_name:
            return "" if row.get("enabled", False) else "disabled"
    return ""
