"""Lazy queue and misc command set.

Engine-backed operator surface with ``lazy_`` names. Every command here
reads or writes the single ``modules.lazy_engine`` store, so queue,
findings, verdicts and guard reviews always match what the autonomous
loop (``lazy_loop`` / ``auto_loop``) sees. The per-task engine surface
(status, broadcast, trace, hint, steer, kill, retest) lives in
``cli.commands.lazyops``; no name is duplicated across both sets.
"""

from __future__ import annotations

import json
import shlex

import cmd2

from cli.commands._base import LazyOwnCommandSet, extract_flag
from utils import exploitation_category, print_error, print_msg


def _engine():
    """Return a fresh engine handle over the persisted lazy store."""
    from modules.lazy_engine import LazyEngine

    return LazyEngine()


class LazyQueueCommandSet(LazyOwnCommandSet):
    """Lazy queue controls backed by the loop engine."""

    phase = "exploit"
    category = "16. Artificial Intelligence"

    @cmd2.with_category(exploitation_category)
    def do_lazy_sync(self, line):
        """Run bidirectional LAZY sync into world model and objectives.

        Usage:
            lazy_sync
        """
        try:
            from modules.lazy_bridge import sync_all
        except ImportError as exc:
            print_error(f"Failed to load bridge: {exc}")
            return
        summary = sync_all()
        print_msg(json.dumps(summary, indent=2)[:3000])

    @cmd2.with_category(exploitation_category)
    def do_lazy_intents(self, line):
        """List engine intents for a task, optionally filtered by state.

        Usage:
            lazy_intents <task_id> [state]
        """
        args = shlex.split(line) if line.strip() else []
        if not args:
            print_error("Usage: lazy_intents <task_id> [state]")
            return
        state = args[1] if len(args) > 1 else ""
        from modules.lazy_engine import ExplorationGraph

        graph = ExplorationGraph(args[0])
        rows = [n for n in graph.list("intent") if not state or n.state == state]
        print_msg(f"{len(rows)} intent(s)")
        for node in rows[:40]:
            print_msg(f"  #{node.node_id} [{node.state}] p{node.priority} {node.text[:100]}")

    @cmd2.with_category(exploitation_category)
    def do_lazy_delete(self, line):
        """Delete an engine intent; soft keeps outputs, hard cascades.

        Usage:
            lazy_delete <task_id> <intent_id> --reason <text> [--hard] [--yes]
        """
        args = shlex.split(line) if line.strip() else []
        if len(args) < 2:
            print_error("Usage: lazy_delete <task_id> <intent_id> --reason <text> [--hard] [--yes]")
            return
        try:
            intent_id = int(args[1])
        except ValueError:
            print_error("intent_id must be an integer")
            return
        reason = extract_flag(args, "--reason") or ""
        if not reason:
            print_error("A reason is required: --reason <text>")
            return
        hard = "--hard" in args
        engine = _engine()
        try:
            if hard and "--yes" not in args:
                preview = engine.preview_delete_intent(args[0], intent_id)
                print_msg(
                    f"Hard delete removes {preview['cascade']} node(s), "
                    f"keeps {len(preview['shared'])} shared. Re-run with --yes."
                )
                return
            result = engine.delete_intent(args[0], intent_id, mode="hard" if hard else "soft", reason=reason)
        except (KeyError, ValueError) as exc:
            print_error(str(exc))
            return
        if hard:
            print_msg(f"Hard-deleted: removed {len(result['removed'])}, kept {len(result['shared'])} shared.")
        else:
            print_msg("Soft-deleted, outputs kept.")

    @cmd2.with_category(exploitation_category)
    def do_lazy_findings(self, line):
        """List engine findings for a task, optionally filtered by status.

        Usage:
            lazy_findings <task_id> [status]
        """
        args = shlex.split(line) if line.strip() else []
        if not args:
            print_error("Usage: lazy_findings <task_id> [status]")
            return
        status = args[1] if len(args) > 1 else ""
        from modules.lazy_engine import ExplorationGraph

        graph = ExplorationGraph(args[0])
        rows = [n for n in graph.list("finding") if not status or str(n.meta.get("status", "")) == status]
        rows.sort(key=lambda n: n.node_id)
        print_msg(f"{len(rows)} finding(s)")
        for node in rows[:40]:
            severity = str(node.meta.get("severity", ""))
            print_msg(f"  #{node.node_id} [{node.state}/{severity}] {node.text[:120]}")

    @cmd2.with_category(exploitation_category)
    def do_lazy_verdict(self, line):
        """Record a manual retest verdict on an engine finding.

        Usage:
            lazy_verdict <task_id> <finding_id> <reproduced|fixed|inconclusive> [--note <text>]
        """
        args = shlex.split(line) if line.strip() else []
        if len(args) < 3:
            print_error("Usage: lazy_verdict <task_id> <finding_id> <reproduced|fixed|inconclusive> [--note <text>]")
            return
        try:
            finding_id = int(args[1])
        except ValueError:
            print_error("finding_id must be an integer")
            return
        try:
            result = _engine().record_verdict(args[0], finding_id, args[2], note=extract_flag(args, "--note") or "")
        except (KeyError, ValueError) as exc:
            print_error(str(exc))
            return
        print_msg(f"[+] finding #{result['finding_id']} -> {result['verdict']}")

    @cmd2.with_category(exploitation_category)
    def do_lazy_mention(self, line):
        """Search @ mention candidates with scroll pagination.

        Usage:
            lazy_mention [kind] [query] [--cursor C]
        """
        args = shlex.split(line) if line.strip() else []
        kind = args[0] if args else ""
        query = ""
        cursor = ""
        if "--cursor" in args:
            try:
                cursor = args[args.index("--cursor") + 1]
            except IndexError:
                cursor = ""
            args = [a for a in args if a not in ("--cursor", cursor)]
            kind = args[0] if args else ""
            query = " ".join(args[1:]) if len(args) > 1 else ""
        else:
            query = " ".join(args[1:]) if len(args) > 1 else ""
        try:
            from modules.lazy_mentions import search_mentions_page
        except ImportError as exc:
            print_error(f"Failed to load mentions: {exc}")
            return
        try:
            page = search_mentions_page(kind, query, cursor)
        except ValueError as exc:
            print_error(str(exc))
            return
        print_msg(f"{len(page.items)} mentions cursor={page.next_cursor[:24]}")
        for item in page.items[:20]:
            print_msg(f"  @[{item.kind}#{item.id}] {item.label[:100]}")

    @cmd2.with_category(exploitation_category)
    def do_lazy_approve(self, line):
        """List engine guard reviews filtered by decision and source.

        Usage:
            lazy_approve <task_id> [ALLOW|ASK|DENY] [source]
        """
        args = shlex.split(line) if line.strip() else []
        if not args:
            print_error("Usage: lazy_approve <task_id> [ALLOW|ASK|DENY] [source]")
            return
        action = args[1].lower() if len(args) > 1 else ""
        source = args[2] if len(args) > 2 else ""
        from modules.lazy_engine import Guard

        rows = Guard(args[0]).audit(limit=200, action=action, source=source)
        print_msg(f"{len(rows)} review(s).")
        for row in rows[-15:]:
            print_msg(
                f"  {row.get('tool_use_id')} {row.get('action')} {row.get('source')} {str(row.get('reason', ''))[:100]}"
            )

    @cmd2.with_category(exploitation_category)
    def do_lazy_fleet(self, line):
        """Cross-task fleet: list | graph <task> | findings <task> | traces <task> [query] | node <task> <id> | pause <task> | resume <task> | report <task> <finding> <text...>

        Usage:
            lazy_fleet list
            lazy_fleet graph t0001
            lazy_fleet findings t0001
            lazy_fleet traces t0001 ssh
            lazy_fleet node t0001 12
            lazy_fleet pause t0001
            lazy_fleet report t0001 7 ## Summary ...
        """
        args = shlex.split(line) if line.strip() else []
        action = args[0] if args else "list"
        engine = _engine()
        if action == "list":
            rows = engine.list_tasks()
            print_msg(f"{len(rows)} task(s)")
            for row in rows:
                print_msg(
                    f"  {row['task_id']} [{row['status']}] "
                    f"intents={row['intents_pending']} facts={row['facts']} "
                    f"findings={row['findings']} {row['goal'][:70]}"
                )
            return
        task_id = args[1] if len(args) > 1 else ""
        if not task_id:
            print_error("Usage: lazy_fleet list|graph|findings|traces|node|pause|resume|report ...")
            return
        try:
            if action == "graph":
                print_msg(json.dumps(engine.task_graph(task_id), indent=2)[:4000])
                return
            if action == "findings":
                for row in engine.task_findings(task_id):
                    print_msg(
                        f"  #{row['id']} [{row['severity']}/{row['status']}] "
                        f"v{row['evidence_version']} report={row['report_chars']}c "
                        f"{row['text'][:110]}"
                    )
                return
            if action == "traces":
                query = " ".join(args[2:]) if len(args) > 2 else ""
                for row in engine.task_traces(task_id, query):
                    print_msg(f"  {row.get('worker', '')} {row.get('kind', '')}: {str(row.get('text', ''))[:140]}")
                return
            if action == "node" and len(args) > 2:
                print_msg(json.dumps(engine.task_node_detail(task_id, int(args[2])), indent=2)[:4000])
                return
            if action == "pause":
                print_msg("[+] paused." if engine.pause_task(task_id) else "[-] task was not running.")
                return
            if action == "resume":
                print_msg("[+] resumed." if engine.resume_task(task_id) else "[-] task was not paused.")
                return
            if action == "report" and len(args) > 3:
                version = engine.update_finding_report(task_id, int(args[2]), " ".join(args[3:]))
                print_msg(f"[+] finding #{args[2]} report v{version}" if version else "[-] finding not updated.")
                return
        except (KeyError, ValueError) as exc:
            print_error(str(exc))
            return
        print_error("Usage: lazy_fleet list|graph|findings|traces|node|pause|resume|report ...")

    @cmd2.with_category(exploitation_category)
    def do_lazy_orchestrator(self, line):
        """Admin console for the loop (Textual TUI).

        Tabs: Now (what the orchestrator is executing right now, live
        activity tail and per-worker current command), Config (payload
        knobs the runner reads), Verbs (searchable command picker when
        adding a verb), Playbooks (full CRUD over playbooks/*.yaml with
        preview and raw YAML editing), Gyms (YAML catalogue plus
        persistent active runs; space starts or stops the selected gym),
        Chains (APT chain YAML administration: preview, enable/disable,
        generate from playbook, delete), Profiles (activate orchestration
        profiles), Models (LLM failover chain add/remove), Params (shared
        parameter catalog: declare a reusable parameter once and use it in
        every addon), Guard (intercept rules add/remove). Keys: r refresh,
        s save config, a add, e edit, d delete, space toggle, q quit.

        Usage:
            lazy_orchestrator [task_id]
        """
        args = shlex.split(line) if line.strip() else []
        task_id = args[0] if args else ""
        try:
            from cli.lazy_orchestrator import run_orchestrator_console
        except ImportError as exc:
            print_error(f"Failed to load orchestrator console (textual installed?): {exc}")
            return
        run_orchestrator_console(task_id, shell=self._resolve_shell())

    @cmd2.with_category(exploitation_category)
    def do_lazy_view(self, line):
        """Attach the live worker monitor to a task (or the newest task).

        Split panes per worker plus audit tabs (activity, guard,
        traffic, findings) and operator keys: q quit, p/r pause/resume,
        a/d approve/deny first pending intercept, h hint, s steer,
        k kill. Works from a second terminal while ``lazy_loop`` runs.

        Usage:
            lazy_view [task_id]
        """
        args = shlex.split(line) if line.strip() else []
        task_id = args[0] if args else ""
        try:
            from cli.lazy_monitor import run_monitor_command
        except ImportError as exc:
            print_error(f"Failed to load monitor (textual installed?): {exc}")
            return
        run_monitor_command(task_id)

    do_lazy_monitor = do_lazy_view


__all__ = ["LazyQueueCommandSet"]
