"""Caldera-style command set — operation lifecycle, TTP coverage, and planner.

Wires the new ``modules/operation``, ``modules/planner``, and
``modules/ttp_coverage`` modules into the LazyOwn shell.

Commands:
    op_list                  — list all operations
    op_create <name> <target> [apt]
    op_plan <id> [playbook]  — populate steps via playbook YAML or MITRE derive
    op_start <id>            — run all pending steps (no-op executor by default)
    op_pause <id>            — pause a running operation
    op_resume <id>           — resume a paused operation
    op_stop <id>             — stop a running operation
    op_status <id>           — show progress, coverage, fact count
    op_timeline <id>         — chronological event log
    op_report <id>           — full post-mortem

    ttp_matrix               — coverage matrix across all operations
    ttp_rebuild              — re-walk operations dir to refresh
    ttp_show <technique_id>  — detail for one technique

    plan <target>            — pick the next best technique to run
    plan_detail <target>     — full ranked list with scores
"""

from __future__ import annotations

import shlex
import time

import cmd2

from cli.commands._base import LazyOwnCommandSet
from modules.operation import (
    OperationManager,
    OperationStep,
    get_manager,
)
from modules.planner import Planner, get_planner
from modules.ttp_coverage import TTPCoverage, get_coverage
from utils import (
    miscellaneous_category,
    print_error,
    print_msg,
    print_warn,
)


def _resolve_manager() -> OperationManager:
    return get_manager()


def _resolve_coverage() -> TTPCoverage:
    cov = get_coverage()
    cov.rebuild_from_operations()
    return cov


def _resolve_planner(shell) -> Planner:
    api_key = ""
    if shell is not None:
        api_key = shell.params.get("api_key", "") or ""
    return get_planner(api_key=api_key)


class CalderaCommandSet(LazyOwnCommandSet):
    """Operation lifecycle, TTP coverage, and fact-based planner."""

    phase = "caldera"
    category = "12. Miscellaneous"

    def _shell(self):
        return self._resolve_shell()

    # ==================================================================
    # op_*
    # ==================================================================

    @cmd2.with_category(miscellaneous_category)
    def do_op_list(self, line):
        """List all operations.

        Usage: op_list
        """
        mgr = _resolve_manager()
        ops = mgr.list()
        if not ops:
            print_msg("No operations. Use 'op_create <name> <target>' to start one.")
            return
        print_msg(f"{'ID':<10} {'Name':<25} {'Target':<18} {'Status':<12} {'Created'}")
        print_msg("-" * 80)
        for op in ops:
            print_msg(
                f"{op.id:<10} {op.name[:24]:<25} {op.target[:17]:<18} "
                f"{op.status:<12} {op.created_at[:19]}"
            )

    @cmd2.with_category(miscellaneous_category)
    def do_op_create(self, line):
        """Create a new planned operation.

        Usage: op_create <name> <target> [apt_name] [description]
        """
        args = shlex.split(line.strip())
        if len(args) < 2:
            print_error("Usage: op_create <name> <target> [apt_name] [description]")
            return
        name = args[0]
        target = args[1]
        apt_name = args[2] if len(args) > 2 else "LazyOwn_auto"
        description = " ".join(args[3:]) if len(args) > 3 else ""
        mgr = _resolve_manager()
        op = mgr.create(name=name, target=target, apt_name=apt_name, description=description)
        print_msg(f"Operation {op.id} created (planned). Use 'op_plan {op.id}' to populate steps.")

    @cmd2.with_category(miscellaneous_category)
    def do_op_plan(self, line):
        """Populate operation steps from a playbook YAML or via MITRE derive.

        Usage: op_plan <op_id> [path/to/playbook.yaml]
        """
        args = shlex.split(line.strip())
        if not args:
            print_error("Usage: op_plan <op_id> [playbook.yaml]")
            return
        op_id = args[0]
        pb_path = args[1] if len(args) > 1 else None
        mgr = _resolve_manager()
        op = mgr.get(op_id)
        if op is None:
            print_error(f"operation {op_id} not found")
            return
        try:
            op = mgr.plan_from_apt(op, playbook_yaml_path=pb_path)
            print_msg(f"Operation {op_id} planned with {len(op.steps)} steps.")
            for s in op.steps[:5]:
                print_msg(f"  [{s.technique_id:<10}] {s.name}")
            if len(op.steps) > 5:
                print_msg(f"  ... and {len(op.steps) - 5} more")
        except Exception as e:
            print_error(f"planning failed: {e}")

    @cmd2.with_category(miscellaneous_category)
    def do_op_start(self, line):
        """Start (or resume) an operation.

        Usage: op_start <op_id>
        Steps with empty commands run as no-ops. Wire the
        ``executor(callable)`` from outside the shell to actually
        execute payloads (see ``modules/operation.py``).
        """
        op_id = line.strip()
        if not op_id:
            print_error("Usage: op_start <op_id>")
            return
        mgr = _resolve_manager()
        try:
            op = mgr.start(op_id)
            st = mgr.status(op_id)
            print_msg(
                f"Operation {op_id} → {op.status} "
                f"({st['steps']['completed']}/{st['steps']['total']} steps, "
                f"{st['facts_produced']} facts)"
            )
        except Exception as e:
            print_error(f"start failed: {e}")

    @cmd2.with_category(miscellaneous_category)
    def do_op_pause(self, line):
        """Pause a running operation.

        Usage: op_pause <op_id>
        """
        op_id = line.strip()
        if not op_id:
            print_error("Usage: op_pause <op_id>")
            return
        mgr = _resolve_manager()
        try:
            mgr.pause(op_id)
            print_msg(f"Operation {op_id} paused.")
        except Exception as e:
            print_error(f"pause failed: {e}")

    @cmd2.with_category(miscellaneous_category)
    def do_op_resume(self, line):
        """Resume a paused operation.

        Usage: op_resume <op_id>
        """
        op_id = line.strip()
        if not op_id:
            print_error("Usage: op_resume <op_id>")
            return
        mgr = _resolve_manager()
        try:
            mgr.resume(op_id)
            print_msg(f"Operation {op_id} resumed.")
        except Exception as e:
            print_error(f"resume failed: {e}")

    @cmd2.with_category(miscellaneous_category)
    def do_op_stop(self, line):
        """Stop a running operation.

        Usage: op_stop <op_id>
        """
        op_id = line.strip()
        if not op_id:
            print_error("Usage: op_stop <op_id>")
            return
        mgr = _resolve_manager()
        try:
            mgr.stop(op_id)
            print_msg(f"Operation {op_id} stopped.")
        except Exception as e:
            print_error(f"stop failed: {e}")

    @cmd2.with_category(miscellaneous_category)
    def do_op_status(self, line):
        """Show the status of an operation.

        Usage: op_status <op_id>
        """
        op_id = line.strip()
        if not op_id:
            print_error("Usage: op_status <op_id>")
            return
        mgr = _resolve_manager()
        st = mgr.status(op_id)
        if "error" in st:
            print_error(st["error"])
            return
        print_msg(f"Operation {st['id']}: {st['name']}")
        print_msg(f"  Target       : {st['target']}")
        print_msg(f"  Threat actor : {st['apt_name']}")
        print_msg(f"  Status       : {st['status']}")
        print_msg(f"  Created      : {st['created_at']}")
        print_msg(f"  Started      : {st['started_at'] or '-'}")
        print_msg(f"  Finished     : {st['finished_at'] or '-'}")
        s = st["steps"]
        print_msg(
            f"  Steps        : {s['completed']}/{s['total']} completed, "
            f"{s['failed']} failed, {s['pending']} pending"
        )
        print_msg(f"  Facts        : {st['facts_produced']}")
        if st["ttp_coverage"]:
            print_msg("  TTP coverage :")
            for tid, status in st["ttp_coverage"].items():
                print_msg(f"    {tid:<10} {status}")

    @cmd2.with_category(miscellaneous_category)
    def do_op_timeline(self, line):
        """Show the event timeline of an operation.

        Usage: op_timeline <op_id>
        """
        op_id = line.strip()
        if not op_id:
            print_error("Usage: op_timeline <op_id>")
            return
        mgr = _resolve_manager()
        events = mgr.timeline(op_id)
        if not events:
            print_warn(f"no events for operation {op_id}")
            return
        print_msg(f"{'Timestamp':<20} {'Step':<5} {'Name':<25} {'Status':<11} {'Summary'}")
        print_msg("-" * 100)
        for ev in events:
            print_msg(
                f"{ev['timestamp']:<20} {ev['step_index']:>5} {ev['step_name'][:24]:<25} "
                f"{ev['status']:<11} {ev['summary'][:50]}"
            )

    @cmd2.with_category(miscellaneous_category)
    def do_op_report(self, line):
        """Generate a full report for an operation.

        Usage: op_report <op_id>
        """
        op_id = line.strip()
        if not op_id:
            print_error("Usage: op_report <op_id>")
            return
        mgr = _resolve_manager()
        report = mgr.report(op_id)
        print_msg(report)

    # ==================================================================
    # ttp_*
    # ==================================================================

    @cmd2.with_category(miscellaneous_category)
    def do_ttp_matrix(self, line):
        """Render the MITRE ATT&CK coverage matrix across all operations.

        Usage: ttp_matrix
        """
        cov = _resolve_coverage()
        print_msg(cov.matrix())

    @cmd2.with_category(miscellaneous_category)
    def do_ttp_rebuild(self, line):
        """Re-walk the operations directory to refresh the coverage matrix.

        Usage: ttp_rebuild
        """
        cov = get_coverage()
        n = cov.rebuild_from_operations()
        print_msg(f"TTP coverage rebuilt: {n} techniques indexed.")

    @cmd2.with_category(miscellaneous_category)
    def do_ttp_show(self, line):
        """Show details for a single MITRE technique.

        Usage: ttp_show <T1234.001>
        """
        tid = line.strip().upper()
        if not tid:
            print_error("Usage: ttp_show <technique_id>")
            return
        cov = _resolve_coverage()
        row = cov.status_by_id(tid)
        if row is None:
            print_warn(f"no coverage data for {tid}")
            return
        print_msg(f"Technique: {row.technique_id}")
        print_msg(f"  Name      : {row.name}")
        print_msg(f"  Tactic    : {row.tactic}")
        print_msg(f"  Status    : {row.status}")
        print_msg(f"  Last run  : {row.last_run}")
        print_msg(f"  Operations: {', '.join(row.operations)}")
        print_msg(f"  Findings  : {row.findings_count}")

    # ==================================================================
    # plan_*
    # ==================================================================

    @cmd2.with_category(miscellaneous_category)
    def do_plan(self, line):
        """Pick the next best technique to run for a target.

        Usage: plan <target>
        Shows the chosen technique, its score, and a one-line rationale.
        """
        target = line.strip()
        if not target:
            print_error("Usage: plan <target>")
            return
        planner = _resolve_planner(self._shell())
        result = planner.plan(target)
        if result.chosen is None:
            print_warn(result.rationale)
            return
        c = result.chosen
        print_msg(f"Target: {result.target}")
        print_msg(f"  Facts observed: {len(result.facts_observed)}")
        print_msg(f"  Chosen technique: {c.technique_id} — {c.name}")
        print_msg(f"    Tactic : {c.tactic}")
        print_msg(f"    Score  : {c.score:.0f}")
        print_msg(f"    Risk   : {c.risk}")
        print_msg(f"    Matched: {', '.join(c.matched_facts) or 'none'}")
        if c.command:
            print_msg(f"    Command: {c.command[:120]}")
        print_msg(f"  Rationale: {result.rationale}")

    @cmd2.with_category(miscellaneous_category)
    def do_plan_detail(self, line):
        """Show the full ranked plan (all candidates) for a target.

        Usage: plan_detail <target>
        """
        target = line.strip()
        if not target:
            print_error("Usage: plan_detail <target>")
            return
        planner = _resolve_planner(self._shell())
        result = planner.plan(target, max_candidates=15)
        if not result.candidates:
            print_warn(f"no candidates for {target} — populate facts first")
            return
        print_msg(f"Plan for {target} ({len(result.candidates)} candidates, "
                  f"{len(result.facts_observed)} facts observed):")
        print_msg(f"  {'Rank':<5} {'TechID':<10} {'Name':<35} {'Score':<7} {'Risk':<7} {'Matched'}")
        print_msg("-" * 95)
        for i, c in enumerate(result.candidates, 1):
            print_msg(
                f"  {i:<5} {c.technique_id:<10} {c.name[:34]:<35} {c.score:<7.0f} "
                f"{c.risk:<7} {','.join(c.matched_facts)[:25]}"
            )
        print_msg(f"\nRationale: {result.rationale}")

    @cmd2.with_category(miscellaneous_category)
    def do_plan_apply(self, line):
        """Run the planner, then auto-create and start an operation.

        Usage: plan_apply <target> [op_name] [apt_name]
        """
        args = shlex.split(line.strip())
        if not args:
            print_error("Usage: plan_apply <target> [op_name] [apt_name]")
            return
        target = args[0]
        op_name = args[1] if len(args) > 1 else f"auto_{int(time.time())}"
        apt_name = args[2] if len(args) > 2 else "LazyOwn_auto"

        planner = _resolve_planner(self._shell())
        result = planner.plan(target)
        if result.chosen is None:
            print_warn(f"planner found no candidates for {target}")
            return

        mgr = _resolve_manager()
        op = mgr.create(name=op_name, target=target, apt_name=apt_name)
        from modules.playbook_engine import PlaybookEngine
        engine = PlaybookEngine()
        try:
            pb = engine.derive(target, phase=None, apt_name=apt_name)
            for i, st in enumerate(pb.steps):
                op.steps.append(OperationStep(
                    step_index=i,
                    name=st.name,
                    technique_id=st.technique_id,
                    tactic=st.tactic,
                    command=st.command,
                    description=st.description,
                ))
            for s in op.steps:
                op.ttp_coverage[s.technique_id] = "pending"
            op.save()
        except Exception as exc:
            print_warn(f"plan_apply: could not load playbook steps: {exc}")
        print_msg(f"Operation {op.id} created from planner output.")
        print_msg(f"  Chosen technique: {result.chosen.technique_id} — {result.chosen.name}")
        print_msg(f"  Use 'op_start {op.id}' to begin execution.")
