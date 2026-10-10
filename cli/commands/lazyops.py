"""Lazy autonomous loop commands (single orchestrator, lazy_* surface).

Every subsystem is invocable individually so the operator sees
what it does, plus ``lazy_loop`` driving the full engine.
The orchestrator auto-invokes every step internally, so a human runs
ONE command and the engine runs scope, asset, enrich, planner,
frontier, worker, guard, traffic, finding, retest, compaction, trace.

Example session (operator-visible, real commands):
    lazy_task create gain initial access on 127.0.0.1
    lazy_scope add ip 127.0.0.1 local test
    lazy_asset add ip 127.0.0.1
    lazy_loop --task t0001 --rounds 6 --workers 2
"""

from __future__ import annotations

import shlex

import cmd2

from cli.commands._base import LazyOwnCommandSet, extract_flag
from utils import ai_category, print_error, print_msg, print_warn


def _engine():
    """Import LazyEngine lazily so the shell boots without it."""
    from modules.lazy_engine import LazyEngine

    return LazyEngine()


class LazyCommandSet(LazyOwnCommandSet):
    """Lazy double-graph autonomous loop: planner, workers, guard, retest."""

    phase = "ai"
    category = "AI Autonomous Loop"

    def _task_id(self, args: list[str]) -> str:
        """Resolve --task flag or fall back to the newest task."""
        explicit = extract_flag(args, "--task")
        if explicit:
            return explicit
        try:
            tasks = _engine().store.list()
            if tasks:
                return tasks[-1]["task_id"]
        except Exception:
            pass
        return ""

    def _require_task(self, args: list[str]) -> str:
        """Return task id or print usage error and empty string."""
        task_id = self._task_id(args)
        if not task_id:
            print_error("No task. Usage: lazy_task create <goal>  (or pass --task T)")
        return task_id

    @staticmethod
    def _free_text(args: list[str]) -> str:
        """Return positional words with flag values stripped."""
        skip = {"--task", "--rounds", "--workers", "--priority", "--limit",
                "--intent", "--format", "--timeout"}
        words: list[str] = []
        idx = 0
        while idx < len(args):
            if args[idx] in skip:
                idx += 2
                continue
            if not args[idx].startswith("--"):
                words.append(args[idx])
            idx += 1
        return " ".join(words).strip()

    @cmd2.with_category(ai_category)
    def do_lazy_task(self, line):
        """Create/list/show/pause/resume/delete tasks. Usage: lazy_task create <goal> | lazy_task list | lazy_task show|pause|resume|delete [--task T]"""
        args = shlex.split(line) if line.strip() else []
        if not args or args[0] == "list":
            for record in _engine().store.list():
                print_msg(f"  [{record['task_id']}] {record['status']} :: {record['goal'][:100]}")
            return
        if args[0] == "create":
            goal = self._free_text(args[1:])
            if not goal:
                goal = f"engage {self.params.get('rhost', 'target')}"
            summary = _engine().create_task(goal)
            print_msg(f"[+] task {summary['task_id']}: {summary['goal'][:120]} "
                      f"({summary['goals']} goals, scope={summary.get('scope', 0)} auto)")
            return
        if args[0] in ("show", "pause", "resume", "delete"):
            task_id = self._require_task(args)
            if not task_id:
                return
            engine = _engine()
            if args[0] == "show":
                status = engine.status(task_id)
                task = status.get("task", {})
                print_msg(f"[*] {task_id} [{task.get('status')}] :: {str(task.get('goal', ''))[:120]}")
                return
            if args[0] == "pause":
                engine.store.pause(task_id)
                print_msg(f"[*] {task_id} paused (planner + workers idle).")
                return
            if args[0] == "resume":
                engine.store.resume(task_id)
                print_msg(f"[*] {task_id} resumed.")
                return
            if args[0] == "delete":
                from modules.lazy_engine import ExplorationGraph
                engine.store.delete(task_id)
                print_msg(f"[*] {task_id} deleted.")
                _ = ExplorationGraph
                return
        print_error("Usage: lazy_task create <goal> | lazy_task list | lazy_task show|pause|resume|delete [--task T]")

    @cmd2.with_category(ai_category)
    def do_lazy_graph(self, line):
        """Show planner-facing graph overview. Usage: lazy_graph [--task T]"""
        args = shlex.split(line) if line.strip() else []
        task_id = self._require_task(args)
        if not task_id:
            return
        view = _engine().graph_overview(task_id)
        print_msg(f"[*] task {task_id}: {view.get('nodes', 0)} nodes")
        for goal in view.get("goals", []):
            print_msg(f"  goal #{goal['id']} [{goal['state']}] {goal['text'][:100]}")
        for intent in view.get("intents", []):
            print_msg(f"  intent #{intent['id']} [{intent['state']}] p{intent['priority']} {intent['text'][:100]}")
        print_msg(f"  facts={view.get('facts', 0)} findings={view.get('findings', 0)} anchors={view.get('anchors', 0)}")
        cov = view.get("coverage", {})
        print_msg(f"  coverage: {cov.get('tested', 0)}/{cov.get('total', 0)} ({cov.get('pct', 0)}%)")
        for item in view.get("constraints", []):
            print_msg(f"  constraint [{item.get('type')}] {item.get('text', '')[:80]}")

    @cmd2.with_category(ai_category)
    def do_lazy_planner(self, line):
        """Run one planner wakeup (emits 0..N intents). Usage: lazy_planner [--task T]"""
        args = shlex.split(line) if line.strip() else []
        task_id = self._require_task(args)
        if not task_id:
            return
        engine = _engine()
        from modules.lazy_engine import ActivityLog, ExplorationGraph, Planner

        graph = ExplorationGraph(task_id)
        planner = Planner(task_id, engine.assets, graph, ActivityLog(task_id), engine.store)
        created = planner.plan()
        if not created:
            print_msg("[*] planner: no new direction (0 intents) — covered or waiting on running work.")
            return
        for node in created:
            print_msg(f"[+] intent #{node.node_id} p{node.priority}: {node.text[:120]}")

    @cmd2.with_category(ai_category)
    def do_lazy_frontier(self, line):
        """Show pending intent queue. Usage: lazy_frontier [--task T]"""
        args = shlex.split(line) if line.strip() else []
        task_id = self._require_task(args)
        if not task_id:
            return
        from modules.lazy_engine import ExplorationGraph, Frontier

        for node in Frontier(ExplorationGraph(task_id)).pending():
            print_msg(f"  #{node.node_id} p{node.priority}: {node.text[:120]}")

    @cmd2.with_category(ai_category)
    def do_lazy_worker(self, line):
        """Claim ONE intent and execute it with real tools. Usage: lazy_worker [--task T] [--intent N]"""
        args = shlex.split(line) if line.strip() else []
        task_id = self._require_task(args)
        if not task_id:
            return
        engine = _engine()
        from modules.lazy_engine import ActivityLog, ExplorationGraph, Frontier, Guard, TrafficLog, Worker

        graph = ExplorationGraph(task_id)
        wanted = extract_flag(args, "--intent")
        if wanted:
            node = graph.get(int(wanted))
            if node is None or node.kind != "intent":
                print_error(f"No such intent: {wanted}")
                return
            graph.set_state(node.node_id, "running")
        else:
            node = Frontier(graph).claim_next()
            if node is None:
                print_msg("[*] frontier empty — nothing to claim.")
                return
        worker = Worker("worker-cli", task_id, engine.assets, graph,
                        ActivityLog(task_id), TrafficLog(task_id), Guard(task_id), engine.store)
        outcome = worker.execute(node)
        print_msg(f"[+] intent #{node.node_id} -> {outcome['state']}: "
                  f"facts={outcome['facts']} assets={outcome['assets']} findings={outcome['findings']}")

    @cmd2.with_category(ai_category)
    def do_lazy_trace(self, line):
        """Worker trace exchange. Usage: lazy_trace list|search <q>|get <intent> [--task T]"""
        args = shlex.split(line) if line.strip() else []
        task_id = self._require_task(args)
        if not task_id or not args:
            print_error("Usage: lazy_trace list|search <q>|get <intent> [--task T]")
            return
        from modules.lazy_engine import ActivityLog, ExplorationGraph

        log = ActivityLog(task_id)
        mode = args[0]
        rest = [a for a in args[1:] if not a.startswith("--")]
        if mode == "list":
            seen: dict[int, int] = {}
            for record in log.read(2000):
                seen[int(record.get("intent_id", 0))] = seen.get(int(record.get("intent_id", 0)), 0) + 1
            for intent_id, count in sorted(seen.items()):
                print_msg(f"  intent #{intent_id}: {count} steps")
        elif mode == "search" and rest:
            for hit in log.search(" ".join(rest))[:20]:
                print_msg(f"  [#{hit.get('intent_id')}/{hit.get('worker')}] {str(hit.get('text', ''))[:160]}")
        elif mode == "get" and rest:
            graph = ExplorationGraph(task_id)
            for record in log.for_intent(int(rest[0])):
                print_msg(f"  [{record.get('kind')}] {str(record.get('text', ''))[:200]}")
            _ = graph
        else:
            print_error("Usage: lazy_trace list|search <q>|get <intent> [--task T]")

    @cmd2.with_category(ai_category)
    def do_lazy_hint(self, line):
        """Inject steering hint. Usage: lazy_hint <text> [--task T]"""
        args = shlex.split(line) if line.strip() else []
        task_id = self._require_task(args)
        text = self._free_text(args)
        if not task_id or not text:
            print_error("Usage: lazy_hint <text> [--task T]")
            return
        node = _engine().add_hint(task_id, text)
        print_msg(f"[+] hint #{node.node_id}: {text[:120]} (planner reads it next round)")

    @cmd2.with_category(ai_category)
    def do_lazy_intent(self, line):
        """Inject high-priority intent. Usage: lazy_intent <summary> [--task T] [--priority N]"""
        args = shlex.split(line) if line.strip() else []
        task_id = self._require_task(args)
        if not task_id:
            return
        priority = 8
        prio = extract_flag(args, "--priority")
        if prio:
            try:
                priority = max(0, min(10, int(prio)))
            except ValueError:
                pass
        summary = self._free_text(args)
        if not summary:
            print_error("Usage: lazy_intent <summary> [--task T] [--priority N]")
            return
        try:
            node = _engine().add_intent(task_id, summary, priority=priority)
        except ValueError as exc:
            print_error(str(exc))
            return
        print_msg(f"[+] intent #{node.node_id} p{priority}: {summary[:120]}")
    @cmd2.with_category(ai_category)
    def do_lazy_goal(self, line):
        """Goals: list|set <t1;t2>|edit <id> <text>|delete <id>|prove <goal> <evidence> <reason>|met <reason>. Usage: lazy_goal ... [--task T]"""
        args = shlex.split(line) if line.strip() else []
        task_id = self._require_task(args)
        if not task_id or not args:
            print_error("Usage: lazy_goal list|set|edit|delete|prove|met ... [--task T]")
            return
        from modules.lazy_engine import ExplorationGraph

        graph = ExplorationGraph(task_id)
        if args[0] == "list":
            for node in graph.list("goal"):
                print_msg(f"  goal #{node.node_id} [{node.state}] {node.text[:120]}")
        elif args[0] == "set":
            specs = [{"text": chunk.strip()} for chunk in self._free_text(args[1:]).split(";") if chunk.strip()]
            if not specs:
                print_error("Usage: lazy_goal set <goal 1> ; <goal 2> [--task T]")
                return
            for node in _engine().set_goals(task_id, specs):
                print_msg(f"[+] goal #{node.node_id}: {node.text[:120]}")
        elif args[0] == "edit" and len(args) >= 3:
            ok = _engine().edit_goal(task_id, int(args[1]), " ".join(args[2:]))
            print_msg("[+] edited." if ok else "[-] edit failed.")
        elif args[0] == "delete" and len(args) >= 2:
            print_msg("[+] deleted." if _engine().delete_goal(task_id, int(args[1])) else "[-] unknown goal.")
        elif args[0] == "met":
            _engine().goal_met(task_id, self._free_text(args[1:]))
            print_msg(f"[*] {task_id} declared complete.")
        elif args[0] == "prove" and len(args) >= 4:
            ok = _engine().prove_goal(task_id, int(args[1]), int(args[2]), " ".join(args[3:]))
            print_msg("[+] goal proven." if ok else "[-] prove failed (need goal + finding/fact ids + reason; quantitative bars enforced).")
        else:
            print_error("Usage: lazy_goal list|set|edit|delete|prove|met ... [--task T]")

    @cmd2.with_category(ai_category)
    def do_lazy_constraint(self, line):
        """Constraints: add <allow|deny> <text> | list. Usage: lazy_constraint ... [--task T]"""
        args = shlex.split(line) if line.strip() else []
        task_id = self._require_task(args)
        if not task_id or not args:
            print_error("Usage: lazy_constraint add <allow|deny> <text> | lazy_constraint list [--task T]")
            return
        engine = _engine()
        if args[0] == "list":
            for item in (engine.store.get(task_id) or {}).get("constraints", []):
                print_msg(f"  [{item.get('type')}] {item.get('text', '')[:120]}")
        elif args[0] == "add" and len(args) >= 3:
            item = engine.store.add_constraint(task_id, args[1], " ".join(args[2:]))
            print_msg(f"[+] constraint [{item['type']}]: {item['text'][:120]}")
        else:
            print_error("Usage: lazy_constraint add <allow|deny> <text> | lazy_constraint list")

    @cmd2.with_category(ai_category)
    def do_lazy_scope(self, line):
        """Scope: add <kind> <value> [reason] | list. Usage: lazy_scope ... [--task T]"""
        args = shlex.split(line) if line.strip() else []
        task_id = self._require_task(args)
        if not task_id or not args:
            print_error("Usage: lazy_scope add <kind> <value> [reason] | lazy_scope list [--task T]")
            return
        engine = _engine()
        if args[0] == "list":
            for item in (engine.store.get(task_id) or {}).get("scope", []):
                print_msg(f"  [{item.get('kind')}] {item.get('value', '')} :: {item.get('reason', '')[:80]}")
        elif args[0] == "add" and len(args) >= 3:
            item = engine.store.add_scope(task_id, args[1], args[2], " ".join(args[3:]))
            print_msg(f"[+] scope [{item['kind']}]: {item['value']}")
        else:
            print_error("Usage: lazy_scope add <kind> <value> [reason] | lazy_scope list")

    @cmd2.with_category(ai_category)
    def do_lazy_todo(self, line):
        """Serial chain todos: add <text> | done <id> | list. Usage: lazy_todo ... [--task T]"""
        args = shlex.split(line) if line.strip() else []
        task_id = self._require_task(args)
        if not task_id or not args:
            print_error("Usage: lazy_todo add <text> | lazy_todo done <id> | lazy_todo list [--task T]")
            return
        from modules.lazy_engine import TodoStore

        todos = TodoStore(task_id)
        if args[0] == "list":
            for item in todos.as_list():
                print_msg(f"  [{item['id']}] {item['state']}: {item['text'][:100]}")
        elif args[0] == "add" and len(args) >= 2:
            item = todos.add(self._free_text(args[1:]))
            print_msg(f"[+] todo [{item['id']}]: {item['text'][:100]}")
        elif args[0] == "done" and len(args) >= 2:
            print_msg("[+] done." if todos.complete(int(args[1])) else "[-] unknown todo.")
        else:
            print_error("Usage: lazy_todo add <text> | lazy_todo done <id> | lazy_todo list")

    @cmd2.with_category(ai_category)
    def do_lazy_asset(self, line):
        """Assets: add <kind> <value> | list [kind] | coverage | untested. Usage: lazy_asset ..."""
        args = shlex.split(line) if line.strip() else []
        if not args:
            print_error("Usage: lazy_asset add <kind> <value> | lazy_asset list [kind] | coverage | untested")
            return
        engine = _engine()
        if args[0] == "add" and len(args) >= 3:
            try:
                node = engine.assets.insert(args[1], args[2])
            except ValueError as exc:
                print_error(str(exc))
                return
            print_msg(f"[+] asset #{node.asset_id} [{node.kind}]: {node.value}")
        elif args[0] == "list":
            kind = args[1] if len(args) > 1 else ""
            for node in engine.assets.list(kind)[:50]:
                flag = "tested" if node.tested else "new"
                print_msg(f"  #{node.asset_id} [{node.kind}/{flag}] {node.value}")
        elif args[0] == "coverage":
            cov = engine.assets.coverage()
            print_msg(f"[*] {cov['tested']}/{cov['total']} ({cov['pct']}%) :: {cov['by_type']}")
        elif args[0] == "untested":
            task_id = self._task_id(args)
            from modules.lazy_engine import ExplorationGraph
            record = (engine.store.get(task_id) or {}) if task_id else {}
            graph = ExplorationGraph(task_id) if task_id else None
            for node in engine.assets.untested_for(graph, record.get("scope", [])):
                print_msg(f"  #{node.asset_id} [{node.kind}] {node.value}")
        else:
            print_error("Usage: lazy_asset add <kind> <value> | lazy_asset list [kind] | coverage | untested")

    @cmd2.with_category(ai_category)
    def do_lazy_enrich(self, line):
        """Enrich asset with DNS/HTTP. Usage: lazy_enrich <host-or-url>"""
        target = line.strip()
        if not target:
            print_error("Usage: lazy_enrich <host-or-url>")
            return
        from modules.lazy_engine import enrich_asset

        result = enrich_asset(target)
        print_msg(f"[*] {result['value']} dns={result['dns']} http={result['http']}")

    @cmd2.with_category(ai_category)
    def do_lazy_traffic(self, line):
        """Traffic: list|search <q>|get <digest>|templates|template <t>|bind <finding> <digest>|export <path>|archive|clear. Usage: lazy_traffic ... [--task T] [--limit N]"""
        args = shlex.split(line) if line.strip() else []
        task_id = self._task_id(args)
        limit = 20
        lim = extract_flag(args, "--limit")
        if lim:
            try:
                limit = max(1, min(200, int(lim)))
            except ValueError:
                pass
        from modules.lazy_engine import ExplorationGraph, TrafficLog

        if not args or args[0] == "list":
            for record in TrafficLog(task_id).read(limit):
                print_msg(f"  [{record.get('kind')}] {str(record.get('command', ''))[:120]}")
        elif args[0] == "search" and len(args) >= 2:
            for record in TrafficLog(task_id).search(" ".join(args[1:]), limit):
                print_msg(f"  [{record.get('digest')}] {str(record.get('command', ''))[:120]}")
        elif args[0] == "get" and len(args) >= 2:
            record = TrafficLog(task_id).get(args[1])
            print_msg(str(record)[:2000] if record else "[-] unknown digest.")
        elif args[0] == "templates":
            for row in TrafficLog(task_id).templates(limit):
                print_msg(f"  x{row['count']} {row['template'][:140]}")
        elif args[0] == "template" and len(args) >= 2:
            for record in TrafficLog(task_id).by_template(" ".join(args[1:]), limit):
                print_msg(f"  [{record.get('digest')}] {str(record.get('command', ''))[:120]}")
        elif args[0] == "bind" and len(args) >= 3:
            ok = TrafficLog(task_id).bind(int(args[1]), args[2], ExplorationGraph(task_id))
            print_msg("[+] bound." if ok else "[-] bind failed.")
        elif args[0] == "export" and len(args) >= 2:
            print_msg(f"[+] {TrafficLog(task_id).export(args[1], limit)}")
        elif args[0] == "archive":
            print_msg(f"[+] {TrafficLog(task_id).archive(label=task_id or 'global')}")
        elif args[0] == "clear":
            print_msg(f"[+] cleared {TrafficLog(task_id).clear()} records.")
        else:
            print_error("Usage: lazy_traffic list|search|get|templates|template|bind|export|archive|clear ...")

    @cmd2.with_category(ai_category)
    def do_lazy_guard(self, line):
        """Guard gate: check <cmd> | rule-add <pattern> <allow|ask|deny> [reason] | rule-del <p> | audit | stats | pending | approve <id> | deny <id>. Usage: lazy_guard ..."""
        args = shlex.split(line) if line.strip() else []
        if not args:
            print_error("Usage: lazy_guard check <cmd> | lazy_guard rule-add ... | lazy_guard rule-del ... | lazy_guard audit | pending | approve <id> | deny <id>")
            return
        from modules.lazy_engine import Guard, InterceptQueue

        guard = Guard(self._task_id(args))
        queue = InterceptQueue(self._task_id(args))
        if args[0] == "check" and len(args) >= 2:
            decision = guard.check("Bash", " ".join(args[1:]))
            print_msg(f"[*] {decision['action']}: {decision.get('reason', '')}")
        elif args[0] == "rule-add" and len(args) >= 4:
            rule = guard.add_rule(args[1], args[2], " ".join(args[3:]))
            print_msg(f"[+] rule [{rule['action']}]: {rule['pattern']}")
        elif args[0] == "rule-del" and len(args) >= 2:
            print_msg("[+] removed." if guard.remove_rule(args[1]) else "[-] no such rule.")
        elif args[0] == "audit":
            for entry in guard.audit()[-20:]:
                print_msg(f"  [{entry.get('action')}] {entry.get('tool')}: {str(entry.get('command', ''))[:100]}")
        elif args[0] == "stats":
            print_msg(f"[*] guard counters: {guard.stats()}")
        elif args[0] == "rules":
            for rule in guard.rules:
                print_msg(f"  [{rule.get('action')}] {rule.get('pattern')} :: {rule.get('reason', '')[:60]}")
        elif args[0] == "pending":
            items = queue.pending()
            if not items:
                print_msg("[*] no pending intercept requests.")
            for item in items:
                print_msg(f"  #{item['id']} [{item['tool']}] {item['command'][:120]} :: {item.get('reason', '')[:60]}")
        elif args[0] in ("approve", "deny") and len(args) >= 2:
            verdict = "approved" if args[0] == "approve" else "denied"
            try:
                ok = queue.decide(int(args[1]), verdict)
            except (ValueError, KeyError) as exc:
                print_error(str(exc))
                return
            print_msg(f"[+] #{args[1]} {verdict}." if ok else f"[-] no such pending #{args[1]}.")
        else:
            print_error("Usage: lazy_guard check|rule-add|rule-del|audit|stats|rules|pending|approve|deny ...")

    @cmd2.with_category(ai_category)
    def do_lazy_finding(self, line):
        """Findings: list [--full] [--limit N]|report <name> :: <summary>|status <id> <st>|context <id>. Usage: lazy_finding ... [--task T] [--severity S] [--vulnclass C]"""
        args = shlex.split(line) if line.strip() else []
        task_id = self._require_task(args)
        if not task_id or not args:
            print_error("Usage: lazy_finding list|report|status|context ... [--task T]")
            return
        from modules.lazy_engine import ActivityLog, ExplorationGraph, FindingService, TrafficLog

        graph = ExplorationGraph(task_id)
        service = FindingService(task_id, graph, ActivityLog(task_id), _engine().store)
        if args[0] == "list":
            full = "--full" in args
            limit = 50
            raw = extract_flag(args, "--limit")
            if raw:
                try:
                    limit = max(1, min(500, int(raw)))
                except ValueError:
                    pass
            for node in service.ranked()[:limit]:
                verdict = (node.meta.get("retest") or {}).get("verdict", "pending")
                print_msg(f"  #{node.node_id} [{node.meta.get('severity', 'info')}/{node.meta.get('status', 'pending')}/{verdict}] {node.text[:140]}")
                if full:
                    print_msg(f"    poc: {str(node.meta.get('poc', ''))[:300]}")
                    print_msg(f"    assets: {graph.anchors_for(node.node_id)} "
                              f"traffic: {(node.meta.get('traffic_refs', []) or [])[:5]}")
        elif args[0] == "report" and len(args) >= 2:
            raw = self._free_text(args[1:])
            name, _, summary = raw.partition("::")
            node = service.report((name or raw)[:200], summary=summary.strip()[:1000],
                                   severity=extract_flag(args, "--severity") or "",
                                   vulnclass=extract_flag(args, "--vulnclass") or "")
            print_msg(f"[+] finding #{node.node_id} [{node.meta.get('severity')}]: {node.text[:140]}")
        elif args[0] == "status" and len(args) >= 3:
            try:
                ok = service.set_status(int(args[1]), args[2])
            except ValueError as exc:
                print_error(str(exc))
                return
            print_msg("[+] status set." if ok else "[-] unknown finding.")
        elif args[0] == "context" and len(args) >= 2:
            from modules.lazy_engine import Retester

            try:
                context = Retester(graph, ActivityLog(task_id), TrafficLog(task_id)).retest_context(int(args[1]))
            except (KeyError, ValueError) as exc:
                print_error(str(exc))
                return
            print_msg(f"[*] finding #{context['finding_id']}: {context['text'][:200]}")
            print_msg(f"    anchors={context['anchors']} evidence={len(context['evidence'])}")
        else:
            print_error("Usage: lazy_finding list|report|status|context ... [--task T]")

    @cmd2.with_category(ai_category)
    def do_lazy_retest(self, line):
        """Retest finding to reproduced/fixed/inconclusive. Usage: lazy_retest <finding_id> [--task T] [--note TEXT]"""
        args = shlex.split(line) if line.strip() else []
        task_id = self._require_task(args)
        rest = [a for a in args if not a.startswith("--")]
        if not task_id or not rest:
            print_error("Usage: lazy_retest <finding_id> [--task T]")
            return
        from modules.lazy_engine import ActivityLog, ExplorationGraph, Retester, TrafficLog

        retester = Retester(ExplorationGraph(task_id), ActivityLog(task_id), TrafficLog(task_id))
        try:
            result = retester.retest(int(rest[0]), note=extract_flag(args, "--note") or "")
        except (KeyError, ValueError) as exc:
            print_error(str(exc))
            return
        print_msg(f"[+] finding #{result['finding_id']}: {result['verdict']} ({result['attempts']} attempts)")

    @cmd2.with_category(ai_category)
    def do_lazy_steer(self, line):
        """Mid-run correction. Usage: lazy_steer <intent> <message> [--task T]"""
        args = shlex.split(line) if line.strip() else []
        task_id = self._require_task(args)
        rest = [a for a in args if not a.startswith("--")]
        if not task_id or len(rest) < 2:
            print_error("Usage: lazy_steer <intent> <message> [--task T]")
            return
        _engine().store.steer(task_id, int(rest[0]), " ".join(rest[1:]))
        print_msg(f"[+] steer attached to intent #{rest[0]} (applies on next step).")

    @cmd2.with_category(ai_category)
    def do_lazy_kill(self, line):
        """Terminate running intent. Usage: lazy_kill <intent> [--task T]"""
        args = shlex.split(line) if line.strip() else []
        task_id = self._require_task(args)
        rest = [a for a in args if not a.startswith("--")]
        if not task_id or not rest:
            print_error("Usage: lazy_kill <intent> [--task T]")
            return
        _engine().store.kill(task_id, int(rest[0]))
        print_msg(f"[+] intent #{rest[0]} flagged for termination.")

    @cmd2.with_category(ai_category)
    def do_lazy_pause(self, line):
        """Pause task loops. Usage: lazy_pause [--task T]"""
        args = shlex.split(line) if line.strip() else []
        task_id = self._require_task(args)
        if not task_id:
            return
        _engine().store.pause(task_id)
        print_msg(f"[*] {task_id} paused.")

    @cmd2.with_category(ai_category)
    def do_lazy_resume(self, line):
        """Resume paused task. Usage: lazy_resume [--task T]"""
        args = shlex.split(line) if line.strip() else []
        task_id = self._require_task(args)
        if not task_id:
            return
        _engine().store.resume(task_id)
        print_msg(f"[*] {task_id} resumed.")

    @cmd2.with_category(ai_category)
    def do_lazy_report(self, line):
        """Export severity-ranked report. Usage: lazy_report [--task T] [--format md|json] [--out PATH]"""
        args = shlex.split(line) if line.strip() else []
        task_id = self._require_task(args)
        if not task_id:
            return
        fmt = (extract_flag(args, "--format") or "md").lower()
        out = extract_flag(args, "--out") or ""
        engine = _engine()
        status = engine.status(task_id)
        from modules.lazy_engine import ActivityLog, ExplorationGraph, FindingService

        graph = ExplorationGraph(task_id)
        ranked = FindingService(task_id, graph, ActivityLog(task_id), engine.store).ranked()
        lines: list[str] = [f"# Lazy report — {task_id}",
                            f"- goal: {(status.get('task') or {}).get('goal', '')[:200]}",
                            f"- findings: {len(ranked)}",
                            "", "## Findings (critical first)", ""]
        for node in ranked:
            verdict = (node.meta.get("retest") or {}).get("verdict", "pending")
            lines.append(f"### [{str(node.meta.get('severity', 'info')).upper()}] "
                         f"{node.meta.get('name', node.text[:80])}")
            lines.append(f"{node.meta.get('summary', node.text)[:400]}")
            if node.meta.get("poc"):
                lines.append(f"PoC: {str(node.meta['poc'])[:500]}")
            lines.append(f"status={node.meta.get('status', 'pending')} retest={verdict}")
            lines.append("")
        cov = status.get("coverage", {})
        lines.append(f"coverage: {cov.get('tested', 0)}/{cov.get('total', 0)} ({cov.get('pct', 0)}%)")
        runtime = status.get("runtime", {}) or {}
        lines.append(f"runtime: status={runtime.get('status', '')} abort={runtime.get('abort_cause', '')} "
                     f"workers={runtime.get('workers', 0)}")
        budget = status.get("budget", {}) or {}
        lines.append(f"budget: used={budget.get('used', {})} limits={budget.get('limits', {})}")
        lines.append(f"intercept pending: {status.get('intercept_pending', 0)} "
                     f"(lazy_guard pending|approve|deny)")
        body = "\n".join(lines)
        if fmt == "json":
            import json as _json

            body = _json.dumps({"task": task_id,
                                "findings": [{"id": n.node_id, "severity": n.meta.get("severity"),
                                              "status": n.meta.get("status"), "text": n.text,
                                              "retest": (n.meta.get("retest") or {}).get("verdict")}
                                             for n in ranked],
                                "overview": status["overview"]}, indent=2, ensure_ascii=False)
        if out:
            from pathlib import Path as _Path

            dest = _Path(out)
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_text(body)
            print_msg(f"[+] report written to {dest}")
            return
        print_msg(body[:4000])

    @cmd2.with_category(ai_category)
    def do_lazy_runtime(self, line):
        """Show/set loop runtime: budgets, deadline, abort cause, heartbeat. Usage: lazy_runtime show [--task T] | lazy_runtime budget <max_toolcalls> <max_findings> <timeout_s> [--task T]"""
        args = shlex.split(line) if line.strip() else []
        task_id = self._require_task(args)
        if not task_id or not args:
            print_error("Usage: lazy_runtime show [--task T] | lazy_runtime budget <toolcalls> <findings> <timeout> [--task T]")
            return
        engine = _engine()
        if args[0] == "show":
            snap = engine.runtime.heartbeat(task_id)
            check = engine.budget.check(task_id)
            print_msg(f"[*] {task_id} [{snap.get('status')}] abort={snap.get('abort_cause', '') or 'none'} "
                      f"workers={snap.get('workers', 0)} deadline={snap.get('deadline', 0.0)}")
            print_msg(f"    budget ok={check.get('ok')} {check.get('reason', '')} "
                      f"used={check.get('used', {})} limits={check.get('limits', {})}")
            print_msg(f"    watermark={snap.get('watermark', 0)}")
        elif args[0] == "budget" and len([a for a in args[1:] if not a.startswith("--")]) >= 3:
            rest = [a for a in args[1:] if not a.startswith("--")]
            try:
                limits = engine.budget.set_limits(task_id, max_toolcalls=int(rest[0]),
                                                  max_findings=int(rest[1]),
                                                  timeout_sec=float(rest[2]))
            except ValueError as exc:
                print_error(str(exc))
                return
            print_msg(f"[+] budget: {limits}")
        else:
            print_error("Usage: lazy_runtime show [--task T] | lazy_runtime budget ... [--task T]")

    @cmd2.with_category(ai_category)
    def do_lazy_payload_keys(self, line):
        """Show worker tool defaults injected into every probe. Usage: lazy_payload_keys [tool]"""
        args = shlex.split(line) if line.strip() else []
        from modules.lazy_engine import TOOL_DEFAULTS

        wanted = args[0].lower() if args else ""
        for name, spec in TOOL_DEFAULTS.items():
            if wanted and wanted not in name:
                continue
            print_msg(f"  {name} [{spec.get('kind', '')}]: {spec.get('cmd', '')} :: {spec.get('desc', '')}")

    @cmd2.with_category(ai_category)
    def do_lazy_fact(self, line):
        """Facts: list [query] [--hot|--cold]|add <text>. Usage: lazy_fact ... [--task T]"""
        args = shlex.split(line) if line.strip() else []
        task_id = self._require_task(args)
        if not task_id or not args:
            print_error("Usage: lazy_fact list [query] [--hot|--cold] | lazy_fact add <text> [--task T]")
            return
        from modules.lazy_engine import ExplorationGraph

        graph = ExplorationGraph(task_id)
        if args[0] == "list":
            if "--hot" in args:
                items = graph.list_facts(self._free_text(args[1:]), hot_full=True)
                print_msg(f"[*] {len(items)} hot facts (never truncated).")
            else:
                items = graph.list_facts(self._free_text(args[1:]))
            if "--cold" in args:
                items = [n for n in items if n.meta.get("cold") or n.state == "exhausted"
                         or n.meta.get("cold_digest")]
            for node in items:
                tag = "cold" if (node.meta.get("cold") or node.state == "exhausted") else "hot"
                print_msg(f"  #{node.node_id} [{node.state}/{tag}] {node.text[:160]}")
        elif args[0] == "add" and len(args) >= 2:
            node = _engine().record_fact(task_id, self._free_text(args[1:]))
            print_msg(f"[+] fact #{node.node_id}: {node.text[:140]}")
        else:
            print_error("Usage: lazy_fact list [query] [--hot|--cold] | lazy_fact add <text> [--task T]")

    @cmd2.with_category(ai_category)
    def do_lazy_node(self, line):
        """Full node detail. Usage: lazy_node <id> [--task T]"""
        args = shlex.split(line) if line.strip() else []
        task_id = self._require_task(args)
        rest = [a for a in args if not a.startswith("--")]
        if not task_id or not rest:
            print_error("Usage: lazy_node <id> [--task T]")
            return
        from modules.lazy_engine import ExplorationGraph

        try:
            detail = ExplorationGraph(task_id).node_detail(int(rest[0]))
        except (KeyError, ValueError) as exc:
            print_error(str(exc))
            return
        print_msg(f"[*] #{detail['id']} [{detail['kind']}/{detail['state']}] p{detail['priority']}")
        print_msg(f"    {detail['text'][:400]}")
        print_msg(f"    children={detail['children']} anchors={detail['anchors']}")

    @cmd2.with_category(ai_category)
    def do_lazy_evidence(self, line):
        """Evidence vault: add <finding> <kind> <body>|list <finding>|verify|gc|export <path>. Usage: lazy_evidence ... [--task T]"""
        args = shlex.split(line) if line.strip() else []
        task_id = self._require_task(args)
        if not task_id or not args:
            print_error("Usage: lazy_evidence add|list|export ... [--task T]")
            return
        from modules.lazy_engine import EvidenceStore

        vault = EvidenceStore(task_id)
        if args[0] == "list" and len(args) >= 2:
            for item in vault.for_finding(int(args[1])):
                print_msg(f"  [{item['id']}/{item['kind']}] {item['body'][:160]}")
        elif args[0] == "add" and len(args) >= 4:
            item = vault.add(int(args[1]), args[2], " ".join(args[3:]))
            print_msg(f"[+] evidence [{item['id']}] attached to finding #{args[1]}.")
        elif args[0] == "export" and len(args) >= 2:
            print_msg(f"[+] {vault.export(args[1])}")
        elif args[0] == "verify":
            bad = vault.verify()
            print_msg("[+] all evidence intact." if not bad else f"[-] tampered: {bad}")
        elif args[0] == "gc":
            print_msg(f"[+] removed {vault.gc()} orphaned records.")
        else:
            print_error("Usage: lazy_evidence add|list|export ... [--task T]")

    @cmd2.with_category(ai_category)
    def do_lazy_ask(self, line):
        """Bounded side question over task context. Usage: lazy_ask <question> [--task T]"""
        args = shlex.split(line) if line.strip() else []
        task_id = self._require_task(args)
        question = self._free_text(args)
        if not task_id or not question:
            print_error("Usage: lazy_ask <question> [--task T]")
            return
        from modules.lazy_engine import LlmPool, SideQuestions

        answer = SideQuestions().ask(task_id, question, LlmPool())
        print_msg(f"[*] {answer['answer'][:1500]} (budget={answer['budget']} chars)")

    @cmd2.with_category(ai_category)
    def do_lazy_company(self, line):
        """Company scope: add <name> [scope]|list|match <value>. Usage: lazy_company ..."""
        args = shlex.split(line) if line.strip() else []
        if not args:
            print_error("Usage: lazy_company add|list|match ...")
            return
        from modules.lazy_engine import CompanyScope

        registry = CompanyScope()
        if args[0] == "list":
            for item in registry.list():
                print_msg(f"  [{item['id']}] {item['name']} :: {item.get('scope', '')}")
        elif args[0] == "add" and len(args) >= 2:
            item = registry.add(args[1], " ".join(args[2:]))
            print_msg(f"[+] company [{item['id']}]: {item['name']}")
        elif args[0] == "match" and len(args) >= 2:
            for item in registry.match(" ".join(args[1:])):
                print_msg(f"  [{item['id']}] {item['name']}")
        else:
            print_error("Usage: lazy_company add|list|match ...")

    @cmd2.with_category(ai_category)
    def do_lazy_tool(self, line):
        """Tool catalog: list [agent]|bind <agent> <tool>|unbind <agent> <tool>. Usage: lazy_tool ..."""
        args = shlex.split(line) if line.strip() else []
        if not args:
            print_error("Usage: lazy_tool list [agent] | lazy_tool bind|unbind <agent> <tool>")
            return
        from modules.lazy_engine import ToolCatalog

        catalog = ToolCatalog()
        if args[0] == "list":
            for agent, tools in catalog.bindings(args[1] if len(args) > 1 else "").items():
                print_msg(f"  {agent}: {', '.join(tools)}")
        elif args[0] in ("bind", "unbind") and len(args) >= 3:
            tools = catalog.bind(args[1], args[2]) if args[0] == "bind" else catalog.unbind(args[1], args[2])
            print_msg(f"[+] {args[1]}: {', '.join(tools)}")
        else:
            print_error("Usage: lazy_tool list|bind|unbind ...")

    @cmd2.with_category(ai_category)
    def do_lazy_notify(self, line):
        """Notify channels: list|add <log|webhook|file> <target> [--min S]|test <severity>. Usage: lazy_notify ... [--task T]"""
        args = shlex.split(line) if line.strip() else []
        if not args:
            print_error("Usage: lazy_notify list|add|test ...")
            return
        from modules.lazy_engine import Notifier

        notifier = Notifier(_engine().store)
        if args[0] == "list":
            for channel in notifier.channels():
                print_msg(f"  [{channel['kind']}] {channel['target']} min={channel.get('min_severity', '')}")
        elif args[0] == "add" and len(args) >= 3:
            item = notifier.add_channel(args[1], args[2], extract_flag(args, "--min") or "")
            print_msg(f"[+] channel [{item['kind']}]: {item['target']}")
        elif args[0] == "test":
            task_id = self._task_id(args) or "manual"
            count = notifier.emit(task_id, "finding_status_changed",
                                  {"severity": (args[1] if len(args) > 1 else "high"), "test": True})
            print_msg(f"[+] fanned out to {count} channels (+ log).")
        else:
            print_error("Usage: lazy_notify list|add|test ...")

    @cmd2.with_category(ai_category)
    def do_lazy_trigger(self, line):
        """Scheduler triggers: list|add <kind> [every_sec]|remove <id>. Usage: lazy_trigger ... [--task T]"""
        args = shlex.split(line) if line.strip() else []
        task_id = self._task_id(args)
        if not args:
            print_error("Usage: lazy_trigger list|add|remove ... [--task T]")
            return
        from modules.lazy_engine import TriggerStore

        table = TriggerStore(task_id or "")
        if args[0] == "list":
            for item in table.list():
                print_msg(f"  [{item['id']}] {item['kind']} every={item.get('every_sec', 0)} enabled={item.get('enabled')}")
        elif args[0] == "add" and len(args) >= 2:
            rest = [a for a in args[1:] if not a.startswith("--")]
            every = 0.0
            try:
                every = float(rest[1]) if len(rest) > 1 else 0.0
            except ValueError:
                pass
            item = table.add(rest[0], every_sec=every)
            print_msg(f"[+] trigger [{item['id']}] kind={item['kind']} (fires inside lazy_loop rounds).")
        elif args[0] == "remove" and len(args) >= 2:
            print_msg("[+] removed." if table.remove(int(args[1])) else "[-] unknown trigger.")
        else:
            print_error("Usage: lazy_trigger list|add|remove ... [--task T]")

    @cmd2.with_category(ai_category)
    def do_lazy_llm(self, line):
        """LLM chain: list|add <name> [model] [--priority N]|remove <name>|usage|health. Usage: lazy_llm ..."""
        args = shlex.split(line) if line.strip() else []
        if not args:
            print_error("Usage: lazy_llm list|add|remove|usage|health ...")
            return
        from modules.lazy_engine import LlmPool

        pool = LlmPool()
        if args[0] == "list":
            for member in pool.members():
                print_msg(f"  {member['name']} :: {member.get('model', '')} p{member.get('priority', 0)}")
            if not pool.members():
                print_msg("[*] no members — planner/worker stay heuristic (never an error).")
        elif args[0] == "add" and len(args) >= 2:
            prio = extract_flag(args, "--priority") or "0"
            try:
                priority = int(prio)
            except ValueError:
                priority = 0
            rest = [a for a in args[1:] if not a.startswith("--")]
            item = pool.add_member(rest[0], rest[1] if len(rest) > 1 else rest[0], priority)
            print_msg(f"[+] member {item['name']} (failover order by priority).")
        elif args[0] == "remove" and len(args) >= 2:
            print_msg("[+] removed." if pool.remove_member(args[1]) else "[-] unknown member.")
        elif args[0] == "usage":
            for call in pool.usage().get("calls", [])[-20:]:
                print_msg(f"  [{call.get('member')}/{'ok' if call.get('ok') else 'fail'}] {str(call.get('text', ''))[:100]}")
        elif args[0] == "health":
            for name, ok in pool.health().items():
                print_msg(f"  {name}: {'healthy' if ok else 'cooldown'}")
            if not pool.members():
                print_msg("[*] no members — planner/worker stay heuristic (never an error).")
        else:
            print_error("Usage: lazy_llm list|add|remove|usage|health ...")

    @cmd2.with_category(ai_category)
    def do_lazy_compact(self, line):
        """Compaction: minor|major [--threshold N]|unfolded [--limit N]|overview|expand <digest>. Usage: lazy_compact ... [--task T]"""
        args = shlex.split(line) if line.strip() else []
        task_id = self._require_task(args)
        if not task_id or not args:
            print_error("Usage: lazy_compact minor|major|unfolded|overview|expand ... [--task T]")
            return
        from modules.lazy_engine import ActivityLog, ColdCompactor, ExplorationGraph

        graph = ExplorationGraph(task_id)
        compactor = ColdCompactor(graph, ActivityLog(task_id))
        if args[0] in ("minor", "major"):
            threshold = 50
            raw = extract_flag(args, "--threshold")
            if raw:
                try:
                    threshold = max(1, int(raw))
                except ValueError:
                    pass
            result = compactor.compact(threshold=threshold, mode=args[0])
            print_msg(f"[+] {result['mode']}: folded {result['compacted']} facts into {len(result.get('digests', []))} digests.")
        elif args[0] == "expand" and len(args) >= 2:
            try:
                revived = compactor.expand(int(args[1]))
            except (KeyError, ValueError) as exc:
                print_error(str(exc))
                return
            print_msg(f"[+] revived {len(revived)} members from digest #{args[1]}.")
        elif args[0] == "overview":
            from modules.lazy_engine import ColdCompactor as _CC

            view = _CC(graph, ActivityLog(task_id)).digest_overview()
            cold = [n for n in graph.list("fact")
                    if n.meta.get("cold") or n.state == "exhausted"]
            print_msg(f"[*] {len(view['digests'])} digests covering {view['covered']} cold facts "
                      f"({len(cold)} cold total); expandable: {view['expandable'] or 'none'}.")
            for digest in view["digests"][-10:]:
                members = digest["members"]
                print_msg(f"  digest #{digest['id']} [{digest['mode']}]: "
                          f"{len(members)} members {members[:8]}")
                print_msg(f"    body: {digest['body'][:160]}")
        elif args[0] == "unfolded":
            limit = 60
            raw = extract_flag(args, "--limit")
            if raw:
                try:
                    limit = max(1, min(500, int(raw)))
                except ValueError:
                    pass
            from modules.lazy_engine import ColdCompactor as _CC2

            unfolded = _CC2(graph, ActivityLog(task_id)).unfolded(limit=limit)
            print_msg(f"[*] {unfolded['total']} cold facts (showing {len(unfolded['facts'])}"
                      f"{', truncated' if unfolded['truncated'] else ''}).")
            for fact in unfolded["facts"]:
                print_msg(f"  #{fact['id']} [{fact['state']}] {fact['text'][:160]}")
        else:
            print_error("Usage: lazy_compact minor|major|unfolded|overview|expand ... [--task T]")

    @cmd2.with_category(ai_category)
    def do_lazy_status(self, line):
        """Full task status. Usage: lazy_status [--task T]"""
        args = shlex.split(line) if line.strip() else []
        task_id = self._require_task(args)
        if not task_id:
            return
        status = _engine().status(task_id)
        task = status.get("task", {})
        print_msg(f"[*] {task_id} [{task.get('status')}] :: {str(task.get('goal', ''))[:120]}")
        print_msg(f"    nodes={status['overview'].get('nodes', 0)} "
                  f"facts={status['overview'].get('facts', 0)} "
                  f"findings={status['overview'].get('findings', 0)}")
        runtime = status.get("runtime", {}) or {}
        print_msg(f"    runtime abort={runtime.get('abort_cause', '') or 'none'} workers={runtime.get('workers', 0)}")
        budget = status.get("budget", {}) or {}
        print_msg(f"    budget used={budget.get('used', {})}")
        for item in status.get("todos", []):
            print_msg(f"    todo [{item['id']}/{item['state']}] {item['text'][:80]}")
        for record in status.get("recent", [])[-5:]:
            print_msg(f"    [{record.get('worker')}/{record.get('kind')}] {str(record.get('text', ''))[:120]}")

    @cmd2.with_category(ai_category)
    def do_lazy_overview(self, line):
        """Alias of lazy_graph. Usage: lazy_overview [--task T]"""
        self.do_lazy_graph(line)

    @cmd2.with_category(ai_category)
    def do_lazy_archive(self, line):
        """Task snapshots: save [--task T]|list|stats|restore <path>. Usage: lazy_archive ..."""
        args = shlex.split(line) if line.strip() else []
        from modules.lazy_engine import TaskArchive
        vault = TaskArchive()
        if not args or args[0] == "list":
            for row in vault.list()[-20:]:
                print_msg(f"  {row['task_id']} n={row['nodes']} :: {row['path']}")
            return
        if args[0] == "stats":
            print_msg(f"[*] {vault.stats()}")
            return
        if args[0] == "save":
            task_id = self._require_task(args)
            if not task_id:
                return
            saved = vault.save(task_id)
            print_msg(f"[+] archived {task_id} n={saved['nodes']} :: {saved['path']}")
            return
        if args[0] == "restore" and len(args) >= 2:
            try:
                new_id = vault.restore(args[1])
            except (OSError, ValueError, KeyError) as exc:
                print_error(str(exc))
                return
            print_msg(f"[+] restored as {new_id} (resume with: lazy_loop --task {new_id})")
            return
        print_error("Usage: lazy_archive save [--task T]|list|stats|restore <path>")

    @cmd2.with_category(ai_category)
    def do_lazy_template(self, line):
        """Goal templates: list|add <name> <goal>|use <name>|remove <name>. Usage: lazy_template ..."""
        args = shlex.split(line) if line.strip() else []
        from modules.lazy_engine import TaskTemplate
        table = TaskTemplate()
        if not args or args[0] == "list":
            for row in table.list():
                print_msg(f"  {row['name']} :: {row['goal'][:100]}")
            return
        if args[0] == "add" and len(args) >= 3:
            row = table.add(args[1], " ".join(args[2:]))
            print_msg(f"[+] template {row['name']}: {row['goal'][:120]}")
            return
        if args[0] == "use" and len(args) >= 2:
            row = table.get(args[1])
            if row is None:
                print_error(f"unknown template: {args[1]}")
                return
            summary = _engine().create_task(row["goal"])
            print_msg(f"[+] task {summary['task_id']} from template {row['name']} "
                      f"({summary['goals']} goals). Run: lazy_loop --task {summary['task_id']}")
            return
        if args[0] == "remove" and len(args) >= 2:
            print_msg("[+] removed." if table.remove(args[1]) else "[-] unknown template.")
            return
        print_error("Usage: lazy_template list|add <name> <goal>|use <name>|remove <name>")

    @cmd2.with_category(ai_category)
    def do_lazy_category(self, line):
        """Task labels: set <name> [--task T]|list [name]. Usage: lazy_category ..."""
        args = shlex.split(line) if line.strip() else []
        from modules.lazy_engine import TaskCategory
        table = TaskCategory()
        if not args or args[0] == "list":
            rest = [a for a in args[1:] if not a.startswith("--")]
            for row in table.list(rest[0] if rest else ""):
                print_msg(f"  {row['task_id']} :: {row['category']}")
            return
        if args[0] == "set" and len(args) >= 2:
            task_id = self._require_task(args)
            if not task_id:
                return
            row = table.set(task_id, args[1])
            print_msg(f"[+] {row['task_id']} :: {row['category']}")
            return
        print_error("Usage: lazy_category set <name> [--task T]|list [name]")

    @cmd2.with_category(ai_category)
    def do_lazy_chat(self, line):
        """Task conversation: say <text>|log|clear. Usage: lazy_chat ... [--task T]"""
        args = shlex.split(line) if line.strip() else []
        task_id = self._require_task(args)
        if not task_id or not args:
            print_error("Usage: lazy_chat say <text>|log|clear [--task T]")
            return
        from modules.lazy_engine import LlmPool, TaskChat
        chat = TaskChat()
        if args[0] == "log":
            for turn in chat.log(task_id):
                print_msg(f"  [{turn.get('role')}] {str(turn.get('text', ''))[:200]}")
            return
        if args[0] == "clear":
            print_msg("[+] cleared." if chat.clear(task_id) else "[-] nothing to clear.")
            return
        if args[0] == "say" and len(args) >= 2:
            try:
                turn = chat.say(task_id, self._free_text(args[1:]), LlmPool())
            except ValueError as exc:
                print_error(str(exc))
                return
            print_msg(f"[*] {turn['answer'][:1500]}")
            return
        print_error("Usage: lazy_chat say <text>|log|clear [--task T]")

    @cmd2.with_category(ai_category)
    def do_lazy_scheduler(self, line):
        """Scheduler state: show|run. Usage: lazy_scheduler ... [--task T]"""
        args = shlex.split(line) if line.strip() else []
        task_id = self._task_id(args)
        from modules.lazy_engine import ActivityLog, ExplorationGraph, TriggerStore
        table = TriggerStore(task_id or "")
        if not args or args[0] == "show":
            for item in table.list():
                print_msg(f"  [{item['id']}] {item['kind']} every={item.get('every_sec', 0)} "
                          f"enabled={item.get('enabled')} watermark={item.get('watermark', 0)}")
            snap = _engine().runtime.heartbeat(task_id) if task_id else {}
            if snap:
                print_msg(f"    watermark={snap.get('watermark', 0)} workers={snap.get('workers', 0)}")
            return
        if args[0] == "run":
            if not task_id:
                print_error("Usage: lazy_scheduler run [--task T]")
                return
            fired = table.due(task_id, ExplorationGraph(task_id), ActivityLog(task_id))
            print_msg(f"[+] fired {len(fired)} triggers (planner consumes them next round).")
            return
        print_error("Usage: lazy_scheduler show|run [--task T]")

    @cmd2.with_category(ai_category)
    def do_lazy_gate(self, line):
        """Asset gate: list|check <target>|block-add <kind> <pattern> [note]|block-del <id>|allow-add <kind> <pattern> [note]|allow-del <id>. Usage: lazy_gate ... [--task T] (allow-* require --task)"""
        args = shlex.split(line) if line.strip() else []
        if not args:
            print_error("Usage: lazy_gate list|check|block-add|block-del|allow-add|allow-del ... [--task T]")
            return
        from modules.lazy_engine import AssetGate

        gate = AssetGate(self._task_id(args))
        if args[0] == "list":
            rows = gate.list()
            for rule in rows.get("global_block", []):
                print_msg(f"  global block [{rule['id']}] {rule['kind']}:{rule['pattern']} :: {rule.get('note', '')}")
            for rule in rows.get("block", []):
                print_msg(f"  task block [{rule['id']}] {rule['kind']}:{rule['pattern']} :: {rule.get('note', '')}")
            for rule in rows.get("allow", []):
                print_msg(f"  task allow [{rule['id']}] {rule['kind']}:{rule['pattern']} :: {rule.get('note', '')}")
            return
        if args[0] == "check" and len(args) >= 2:
            rest = [a for a in args[1:] if not a.startswith("--")]
            verdict = gate.evaluate(" ".join(rest))
            print_msg(f"[*] {'allowed' if verdict['allowed'] else 'denied'}: {verdict['reason'] or 'no rule hit'}")
            return
        if args[0] in ("block-add", "allow-add") and len(args) >= 3:
            action = "block" if args[0] == "block-add" else "allow"
            rest = [a for a in args[1:] if not a.startswith("--")]
            try:
                rule = gate.add(rest[0], rest[1], " ".join(rest[2:]), action)
            except ValueError as exc:
                print_error(str(exc))
                return
            print_msg(f"[+] {action} [{rule['id']}] {rule['kind']}:{rule['pattern']}")
            return
        if args[0] in ("block-del", "allow-del") and len(args) >= 2:
            action = "block" if args[0] == "block-del" else "allow"
            try:
                ok = gate.remove(int(args[1]), action)
            except ValueError as exc:
                print_error(str(exc))
                return
            print_msg("[+] removed." if ok else "[-] unknown rule.")
            return
        print_error("Usage: lazy_gate list|check|block-add|block-del|allow-add|allow-del ... [--task T]")

    @cmd2.with_category(ai_category)
    def do_lazy_loop(self, line):
        """Run the single orchestrator (auto-invokes scope/asset/enrich/planner/frontier/worker/guard/traffic/finding/retest/compact/trace). Usage: lazy_loop [--task T] [--rounds N] [--workers N] [--timeout S] [<goal>]"""
        args = shlex.split(line) if line.strip() else []
        rounds = 6
        workers = 2
        timeout = 0.0
        for flag in ("--rounds", "--workers", "--timeout"):
            value = extract_flag(args, flag)
            if value:
                try:
                    if flag == "--rounds":
                        rounds = max(1, min(20, int(value)))
                    elif flag == "--workers":
                        workers = max(1, min(5, int(value)))
                    else:
                        timeout = max(0.0, float(value))
                except ValueError:
                    pass
        task_id = self._task_id(args)
        engine = _engine()
        goal_text = self._free_text(args)
        target = str(self.params.get("rhost", "") or "")
        if goal_text:
            print_msg(f"[+] lazy_task create: {goal_text[:120]}")
        elif not task_id:
            goal_text = f"engage {target or 'target'}"
            print_msg(f"[+] lazy_task create: {goal_text[:120]}")
        else:
            print_msg(f"[*] resuming task {task_id}.")
        print_msg(f"[*] orchestrator: rounds<={rounds} workers={workers} — auto-invokes "
                  f"{'/'.join(engine.ORCHESTRATOR_CHAIN)}.")
        summary = engine.orchestrate(goal=goal_text, task_id=task_id, target=target,
                                     max_rounds=rounds, workers=workers, timeout_sec=timeout)
        task_id = summary["task_id"]
        print_msg(f"[+] {task_id} [{summary['status']}] rounds={summary['rounds']} "
                  f"chain={'+'.join(summary.get('chain', []))[:120]}")
        for goal in summary["overview"].get("goals", []):
            print_msg(f"    goal #{goal['id']} [{goal['state']}] {goal['text'][:100]}")
        print_msg(f"    intents={len(summary['overview'].get('intents', []))} "
                  f"facts={summary['overview'].get('facts', 0)} "
                  f"findings={summary['overview'].get('findings', 0)}")
        if summary["overview"].get("findings"):
            print_warn("Findings present — inspect with: lazy_finding list / lazy_trace list")


__all__ = ["LazyCommandSet"]
