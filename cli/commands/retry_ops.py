"""``retry`` - relaunch a failed chain or failed loop from where it stopped.

Three operator actions after a failure:

- ``retry status`` shows the freshest failed chain checkpoint, the last
  non-complete loop task and the elevated-retry state.
- ``retry chain <chain_name|run_id> [--var key=value ...] [--sudo]``
  resumes the stored checkpoint under the same run id; every ``--var``
  overrides a recorded variable, so the relaunch runs with the
  user-varied configuration.
- ``retry loop [task_id] [auto_loop flags] [--sudo]`` re-enters the
  orchestrator for the last (or given) task id; flags are the ordinary
  ``auto_loop`` flags, so the operator can also vary them.

Elevated mode: when a failure was caused by a missing sudo password,
``--sudo`` arms an askpass session after a warned, explicit
confirmation. Destructive steps configured by you (destructive chains,
playbooks and gym scenarios) may execute with root privileges once the
mode is armed; see :data:`modules.retry_session.SUDO_WARNING`. The
secret stays inside this process and its children only: a 0600 file
under ``sessions/retry/`` with a 0700 askpass helper, both removed on
shell exit or immediately on abort. Nothing reaches logs, history or
transcripts.
"""

from __future__ import annotations

import shlex

from cmd2 import with_category

from cli.commands._base import LazyOwnCommandSet
from cli.retry_support import (
    consent_to_elevate,
    retry_chain,
    status_snapshot,
)
from utils import print_error, print_msg, print_succ, print_warn

RETRY_CATEGORY = "11. Orchestration"


def _confirmer(warning: str) -> str:
    """Prompt the operator with the warned elevation text (no TTY: abort).

    Args:
        warning: The full consent text to display.

    Returns:
        The operator answer; empty string when no interactive terminal
        is attached (fail-closed).
    """
    import sys

    if not (sys.stdin and sys.stdin.isatty()):
        return ""
    print(warning)
    return input("accept and continue? [type YES to arm] ")


class RetryOpsCommandSet(LazyOwnCommandSet):
    """Operator-facing retry surface for chains and the orchestrator."""

    phase = "command_and_control"
    category = RETRY_CATEGORY

    @with_category(RETRY_CATEGORY)
    def do_retry(self, line: str) -> None:
        """Relaunch failed work: retry status | chain | loop.

        Usage:
            retry status [limit]
            retry chain [chain_name|run_id] [--var key=value ...] [--sudo]
            retry loop [task_id] [auto_loop flags] [--sudo]

        ``retry status`` prints the newest failed chain checkpoint and
        the last interrupted loop task so no failure stays hidden after
        a run. ``retry chain`` continues the recorded checkpoint (same
        run id, resumes past the failed step) while ``--var`` entries
        override recorded variables for the relaunch - that is the
        user-varied configuration path, e.g. fixing a port, tool path
        or wordlist that failed last time. Pass a run id (from
        ``retry status``) instead of a chain name to retry an older
        attempt. ``retry loop`` re-enters the orchestrator for the last
        failed/paused/exhausted task; any ``auto_loop`` flag is
        accepted and a task id pins the selection.

        ``--sudo`` arms an askpass-assisted elevated retry after a
        warned confirmation: commands may run with root privileges and
        destructive steps configured by you can now actually execute;
        the sudo password never enters a command line, history or log -
        it is held in a session-internal file revoked on shell exit.
        """
        parts = shlex.split(line)
        if not parts:
            parts = ["status"]
        action, rest = parts[0], parts[1:]
        if action == "status":
            self._retry_status(rest)
            return
        if action == "chain":
            self._retry_chain(rest)
            return
        if action == "loop":
            self._retry_loop(rest)
            return
        print_error(
            "Usage: retry status | retry chain <name|run_id> [--var k=v] [--sudo] | retry loop [task_id] [--sudo]"
        )

    def _arm_elevation(self, rest: list[str]) -> bool:
        """Arm ``--sudo`` when requested; False when it should abort.

        Args:
            rest: Tokens of the retry subcommand.

        Returns:
            True to continue; False aborts the subcommand when --sudo
            was requested but refused/aborted.
        """
        armed, note = consent_to_elevate(rest, _confirmer)
        if armed:
            print_warn(note)
            return True
        if note:
            print_warn(note)
        return "--sudo" not in rest

    def _retry_status(self, rest: list[str]) -> None:
        """Print the freshest failed checkpoint plus the last loop task."""
        limit = 5
        if rest and rest[0].isdigit():
            limit = max(1, min(20, int(rest[0])))
        snapshot = status_snapshot(limit=limit)
        print_msg(f"elevated retry: {'armed' if snapshot['sudo_armed'] else 'off'}")
        if not snapshot["checkpoint_rows"]:
            print_warn("no failed chain checkpoints (chain checkpoints belong to apt_chain runs)")
        for row in snapshot["checkpoint_rows"]:
            print_msg(
                f"chain {str(row.get('chain', ''))[:24]:<24} "
                f"run {str(row.get('run_id', ''))[:44]:<44} "
                f"state={str(row.get('state', '')):<10} "
                f"steps={row.get('steps', 0)} reason={str(row.get('reason', ''))[:36]}"
            )
        task = snapshot.get("last_task")
        if task is not None and task.known:
            print_msg(f"loop  {task.task_id:<8} status={task.status:<10} goal={task.goal[:64]}")
        else:
            print_warn("no failed/paused/exhausted loop task in the task store")
        print_msg("relaunch: retry chain <chain_name|run_id> [--var k=v] [--sudo] | retry loop [task_id] [--sudo]")

    def _retry_chain(self, rest: list[str]) -> None:
        """Resume one chain from its newest failed checkpoint."""
        if not self._arm_elevation(rest):
            return
        tokens = [tok for tok in rest if tok != "--sudo"]
        selector = ""
        if tokens and not tokens[0].startswith("--"):
            selector = tokens[0]
            tokens = tokens[1:]
        extra_vars = _collect_vars(tokens)
        try:
            report = retry_chain(
                chain_or_run=selector,
                shell=self._resolve_shell(),
                extra_vars=extra_vars,
            )
        except Exception as exc:  # noqa: BLE001 - relay any failure loudly
            print_error(f"retry chain failed: {exc}")
            return
        if report.error:
            print_error(f"retry chain: {report.error}")
            return
        print_succ(
            f"[retry] chain={report.chain} run={report.run_id} "
            f"executed={len(report.executed)} skipped={len(report.skipped)} ok={report.ok}"
        )
        if not report.ok:
            print_warn(f"[retry] failed again: {report.reason}")
            print_warn(f"vary the configuration and relaunch: retry chain {report.chain} --var key=value --sudo")
            return
        print_msg("[retry] full outcome inspection: apt_chain checkpoints")

    def _retry_loop(self, rest: list[str]) -> None:
        """Re-enter the orchestrator for the last or named task."""
        if not self._arm_elevation(rest):
            return
        tokens = [tok for tok in rest if tok != "--sudo"]
        if tokens and (tokens[0].isdigit() or tokens[0].lower().startswith("t") and tokens[0][1:].isdigit()):
            task_token = tokens[0]
            tokens = [f"--task {task_token}"] + tokens[1:]
        latest = status_snapshot(1)["last_task"]
        if not any("task" in tok for tok in tokens):
            if latest is not None and latest.known:
                print_msg(f"[retry] resuming last task {latest.task_id} ({latest.status}) {latest.goal[:54]}")
                tokens.append(f"--task {latest.task_id}")
            else:
                print_error("retry loop: no task id given and the task store has none to resume")
                return
        from modules.lazy_runner import parse_loop_line, run_loop

        try:
            config = parse_loop_line(" ".join(tokens))
        except ValueError as exc:
            print_error(f"retry loop: {exc}")
            return
        result = run_loop(self._resolve_shell(), dict(self.params or {}), config)
        if result.get("error"):
            print_warn("[retry] loop ended in error; vary the flags (rounds/target) and retry once more")
        elif result.get("cancelled"):
            print_warn("[retry] loop interrupted; partial state saved: retry loop resumes it")
        elif not result.get("ok", True):
            print_warn("[retry] loop ended incomplete; inspect with lazy_status, then retry loop")
        else:
            print_succ("[retry] loop finished")


def _collect_vars(tokens: list[str]) -> dict[str, str]:
    """Extract ``--var key=value`` pairs from the token stream.

    Args:
        tokens: Tokens after the selector.

    Returns:
        Mapping var -> value (last occurrence wins).
    """
    overrides: dict[str, str] = {}
    index = 0
    while index < len(tokens):
        token = tokens[index]
        if token == "--var" and index + 1 < len(tokens):
            body = tokens[index + 1]
            if "=" in body:
                key, value = body.split("=", 1)
                overrides[key.strip()] = value.strip()
            index += 2
            continue
        index += 1
    return overrides
