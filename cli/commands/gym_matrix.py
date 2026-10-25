"""Metasploitable 2 gym matrix commands.

Runs every indexed gym vector against the configured victim in severity
order, verifying each capture into ``sessions/ctf/``, and summarises the
result for the final CVE report.

Usage:
    gym_metasploitable plan [N] [--only a,b]
    gym_metasploitable run [N] [--only a,b] [--dry-run]
    gym_metasploitable report
"""

from __future__ import annotations

import shlex

import cmd2

from cli.commands._base import LazyOwnCommandSet
from modules import ctf_capture, gym_matrix_runner
from utils import (
    BLUE,
    CYAN,
    GREEN,
    RED,
    RESET,
    YELLOW,
    exploitation_category,
    print_error,
    print_msg,
)


def _extract_flag(args: list[str], flag: str) -> str | None:
    """Extract ``--flag <value>`` from tokenised arguments.

    Args:
        args: Tokenised argument list (mutated to remove the pair).
        flag: Flag name without dashes.

    Returns:
        The value or None.
    """
    marker = f"--{flag}"
    try:
        index = args.index(marker)
    except ValueError:
        return None
    if index + 1 < len(args):
        return args[index + 1]
    args.pop(index)
    return ""


def _extract_bool(args: list[str], flag: str) -> bool:
    """Extract a boolean flag from tokenised arguments.

    Args:
        args: Tokenised argument list.
        flag: Flag name without dashes.

    Returns:
        True when the flag was present.
    """
    marker = f"--{flag}"
    if marker in args:
        args.remove(marker)
        return True
    return False


class GymMetasploitableCommandSet(LazyOwnCommandSet):
    """MS2 gym matrix: plan, run and report deterministic attack paths."""

    phase = "exploit"
    category = exploitation_category

    @cmd2.with_category(exploitation_category)
    def do_gym_metasploitable(self, line):
        """Plan, run, and report the Metasploitable 2 gym matrix.

        :param line: 'plan [N] [--only list]' | 'run [N] [--only list] '
                     '[--dry-run]' | 'report' | 'verify <vuln_id>'.
        """
        args = shlex.split(line)
        if not args:
            print_msg(
                f"{BLUE}Usage: gym_metasploitable plan|run|report|verify "
                f"[N] --only v1,v2 --dry-run{RESET}"
            )
            return
        action = args[0].lower()
        rest = args[1:]
        top_k = 0
        if rest and rest[0].isdigit():
            top_k = int(rest.pop(0))
        only_arg = _extract_flag(rest, "only")
        only = [name.strip() for name in (only_arg or "").split(",") if name.strip()] or None
        dry_run = _extract_bool(rest, "dry-run") or action == "plan"
        if action == "plan":
            self._plan(top_k, only)
            return
        if action == "run":
            self._run(top_k, only, dry_run)
            return
        if action == "report":
            self._report()
            return
        if action == "verify":
            self._verify(rest)
            return
        print_error(f"{YELLOW} Unknown gym_metasploitable action: {action}{RESET}")

    def _plan(self, top_k: int, only: list[str] | None) -> None:
        """Render the ordered execution plan.

        Args:
            top_k: Optional cap on the number of entries.
            only: Optional vulnerability id filter.
        """
        try:
            plan = gym_matrix_runner.plan_matrix(
                self._target(),
                only=only,
                top_k=top_k,
            )
        except ValueError as exc:
            print_error(str(exc))
            return
        if not plan:
            print_msg(f"{YELLOW}Empty gym plan.{RESET}")
            return
        print_msg(f"{BLUE}Gym matrix plan ({len(plan)} vector(s)){RESET}")
        for idx, item in enumerate(plan, 1):
            chain = item["chain_name"] or "(no chain)"
            print_msg(
                f"  {CYAN}[{idx}]{RESET} {item['vuln_id']:<28} "
                f"{item['severity']:<8} {chain:<44} {item['cve']}"
            )

    def _run(self, top_k: int, only: list[str] | None, dry_run: bool) -> None:
        """Execute the matrix and verify CTF captures.

        Args:
            top_k: Optional cap on the number of entries.
            only: Optional vulnerability id filter.
            dry_run: Resolve without executing.
        """
        target = self._target()
        checker = getattr(self, "check_rhost", None) or getattr(self._shell(), "check_rhost", None)
        if checker and not checker():
            return
        result = gym_matrix_runner.run_matrix(
            target,
            shell=self._shell(),
            dry_run=dry_run,
            sessions_dir=None,
            only=only,
            top_k=top_k,
            lhost=str(self.params.get("lhost") or ""),
            lport=str(self.params.get("lport") or ""),
        )
        label = "DRY-RUN" if dry_run else "MATRIX"
        print_msg(f"{label} {result['target']} stats={result['stats']}")
        for run in result["runs"]:
            status_color = GREEN if run["status"] == "ok" else RED
            print_msg(
                f"  {status_color}{run['status']:<10}{RESET} {run['vuln_id']:<28} "
                f"capture={run.get('capture', '-')}"
            )

    def _report(self) -> None:
        """Show the aggregated CTF capture summary."""
        summary = ctf_capture.summary()
        if not summary["total"]:
            print_msg(f"{YELLOW}No CTF records yet — run: gym_metasploitable run{RESET}")
            return
        print_msg(f"{BLUE}CTF captures — total={summary['total']} status={summary['status']}{RESET}")
        print_msg(f"  cves: {', '.join(summary['cves']) or '-'}")
        for vuln_id, record in summary["records"].items():
            total = len(record.get("checks") or [])
            matched = sum(1 for check in (record.get("checks") or []) if check.get("matched"))
            print_msg(
                f"  [{record['status']:<8}] {vuln_id:<28} {record['target']:<15} "
                f"{record['severity']:<8} {matched}/{total} checks"
            )

    def _verify(self, rest: list[str]) -> None:
        """Print the stored record of one vulnerability.

        Args:
            rest: Argument list whose first item is the vuln id.
        """
        if not rest:
            print_error("Usage: gym_metasploitable verify <vuln_id>")
            return
        vuln_id = rest[0]
        record = ctf_capture.list_records().get(vuln_id)
        if record is None:
            print_error(f"No record for {vuln_id}")
            return
        print_msg(f"{CYAN}{vuln_id}{RESET} status={record['status']} created={record['captured_at']}")
        for check in record.get("checks") or []:
            mark = GREEN + "yes" + RESET if check["matched"] else RED + "no " + RESET
            print_msg(f"  [{mark}] {check['name']}: {check['evidence'] or '-'}")

    def _target(self) -> str:
        """Return the configured victim host.

        Returns:
            The ``target`` or ``rhost`` value from payload.json.
        """
        return str(self.params.get("target") or self.params.get("rhost") or "")
