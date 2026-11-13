"""Loop audit shell commands: navigate the campaign timeline of a loop.

One timeline answers the operator's audit question: what did the loop
do, when, which module triggered it, with what confidence (guard
verdict, judge source, opsec cost), and what came out of it. The
timeline merges the audit JSONL written by the runner/worker executor
with guard decisions and engine lifecycle activity.
"""

from __future__ import annotations

import cmd2

from cli.commands._base import LazyOwnCommandSet
from utils import miscellaneous_category, print_error, print_msg, print_warn


class LoopAuditCommandSet(LazyOwnCommandSet):
    """Expose the loop audit timeline to the operator."""

    phase = "recon"
    category = miscellaneous_category

    @cmd2.with_category(miscellaneous_category)
    def do_loop_audit(self, line):
        """Audit what an autonomous loop actually did.

        Usage:
            loop_audit list                summarize every recorded run
            loop_audit latest              timeline of the newest run
            loop_audit <task> [--limit N] [--json]   one task's timeline
            loop_audit show <task>         raw audit JSONL path and head

        Every executed command lands with when it ran, the module/verb
        that triggered it, the worker that ran it, the guard verdict
        behind it (allow/ask/deny plus judge source and reason), the
        opsec gate and detection probability, the duration and a bounded
        output tail. Blocked steps (guard/opsec/approval/sudo) appear as
        DENY rows so nothing the loop considered is invisible.
        """
        from modules import loop_audit

        args = (line or "").split()
        if not args:
            runs = loop_audit.list_runs(limit=1)
            if not runs:
                print_warn("no loop audits recorded yet — run auto_loop and come back")
                return
            task = runs[0]["task"]
        elif args[0] == "list":
            print_msg(loop_audit.render_summary(loop_audit.list_runs(limit=50)))
            return
        elif args[0] == "latest":
            runs = loop_audit.list_runs(limit=1)
            if not runs:
                print_warn("no loop audits recorded yet — run auto_loop and come back")
                return
            task = runs[0]["task"]
        elif args[0] == "show":
            if len(args) < 2:
                print_error("usage: loop_audit show <task>")
                return
            task = args[1]
            path = loop_audit.audit_path(task)
            if not path.exists():
                print_error(f"no audit file for {task}: {path}")
                return
            print_msg(f"[*] audit file: {path}")
            return
        else:
            task = args[0]

        limit = 100
        if "--limit" in args:
            try:
                limit = max(1, int(args[args.index("--limit") + 1]))
            except (IndexError, ValueError):
                print_error("--limit expects a number")
                return
        if "--json" in args:
            import json

            events = loop_audit.timeline(task)
            print_msg(json.dumps(events[-limit:], ensure_ascii=False, indent=2))
            return
        if not loop_audit.audit_path(task).exists():
            print_error(f"no audit file for {task}: {loop_audit.audit_path(task)}")
            return
        timeline_text = loop_audit.render(task, limit=limit)
        if not timeline_text:
            print_warn(f"audit for {task} is empty")
            return
        print_msg(timeline_text)
        runs = {item["task"]: item for item in loop_audit.list_runs(limit=50)}
        summary = runs.get(task)
        if summary:
            print_msg(
                f"[*] summary: commands {summary['ok']} ok / {summary['failed']} failed "
                f"— status {summary['status'] or '-'} verdict {summary['verdict'] or '-'}"
            )
        print_msg(f"[*] full command traffic: sessions/lazy/traffic_{task}.jsonl · report: sessions/lazy/report_{task}.md")


__all__ = ["LoopAuditCommandSet"]
