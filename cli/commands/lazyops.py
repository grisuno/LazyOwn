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

import json
import shlex
from uuid import uuid4

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
        skip = {
            "--task",
            "--rounds",
            "--workers",
            "--priority",
            "--limit",
            "--intent",
            "--format",
            "--timeout",
            "--session",
            "--from",
        }
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
    def do_lazy_dispatch(self, line):
        """Dispatch one detached task to an external agent: opencode|hermes [--in DIR] [--resume S] [--max-turns N] [--run-budget S] [--timeout S] <task...>. Usage: lazy_dispatch ..."""
        args = shlex.split(line) if line.strip() else []
        if len(args) < 2 or args[0] not in ("opencode", "hermes"):
            print_error(
                "Usage: lazy_dispatch opencode|hermes [--in DIR] [--resume S] "
                "[--max-turns N] [--run-budget S] [--timeout S] <task...>"
            )
            return
        runtime = args[0]
        task_words: list[str] = []
        skip_next = False
        for token in args[1:]:
            if skip_next:
                skip_next = False
                continue
            if token in ("--in", "--resume", "--max-turns", "--run-budget", "--timeout"):
                skip_next = True
                continue
            if token.startswith("--"):
                continue
            task_words.append(token)
        task = " ".join(task_words).strip()
        if not task:
            print_error("Usage: lazy_dispatch opencode|hermes [flags] <task...>")
            return
        cwd = extract_flag(args, "--in") or ""
        resume = extract_flag(args, "--resume") or ""
        try:
            max_turns = int(extract_flag(args, "--max-turns") or 0)
        except ValueError:
            max_turns = 0
        try:
            run_budget = int(extract_flag(args, "--run-budget") or 0)
        except ValueError:
            run_budget = 0
        try:
            timeout = float(extract_flag(args, "--timeout") or 0) or 900.0
        except ValueError:
            timeout = 900.0
        from modules import lazy_agent

        if runtime == "opencode":
            result = lazy_agent.run_external_opencode(task, session_id=resume, cwd=cwd, timeout_sec=timeout)
        else:
            result = lazy_agent.run_external_hermes(
                task,
                session_id=resume,
                cwd=cwd,
                timeout_sec=timeout,
                max_turns=max_turns,
                run_budget=run_budget,
            )
        reply = str(result.get("reply", "") or "").strip()
        print_msg(reply[-4000:] if reply else "[*] no reply.")
        if result.get("error"):
            print_error(str(result["error"])[:200])

    @cmd2.with_category(ai_category)
    def do_lazy_task(self, line):
        """Create/list/show/pause/resume/delete/spawn/queue/limit/drain tasks. Usage: lazy_task create <goal> | lazy_task list | lazy_task show|pause|resume|delete [--task T] | lazy_task spawn <goal> --from t0001[,t0002] | lazy_task limit [N] | lazy_task queue | lazy_task drain"""
        args = shlex.split(line) if line.strip() else []
        if not args or args[0] == "list":
            for record in _engine().store.list():
                print_msg(f"  [{record['task_id']}] {record['status']} :: {record['goal'][:100]}")
            return
        if args[0] == "create":
            sources = [s.strip() for s in (extract_flag(args, "--from") or "").split(",") if s.strip()]
            scrubbed: list[str] = []
            skip_next = False
            for token in args[1:]:
                if skip_next:
                    skip_next = False
                    continue
                if token == "--from":
                    skip_next = True
                    continue
                scrubbed.append(token)
            goal = self._free_text(scrubbed)
            if not goal:
                goal = f"engage {self.params.get('rhost', 'target')}"
            if sources:
                summary = _engine().spawn_task(goal, source_task_ids=sources)
                inherited = summary.get("inherited", {})
                print_msg(
                    f"[+] task {summary['task_id']}: {summary['goal'][:120]} "
                    f"({summary['goals']} goals, inherited scope={inherited.get('scope', 0)}"
                    f" facts={inherited.get('facts', 0)} from {','.join(inherited.get('sources', []))})"
                )
            else:
                summary = _engine().create_task(goal)
                print_msg(
                    f"[+] task {summary['task_id']}: {summary['goal'][:120]} "
                    f"({summary['goals']} goals, scope={summary.get('scope', 0)} auto)"
                )
            return
        if args[0] in ("limit", "queue", "drain"):
            engine = _engine()
            if args[0] == "limit":
                if len(args) < 2:
                    print_msg(
                        f"[*] concurrency cap = {engine.max_concurrent} "
                        f"({'admission off' if engine.max_concurrent == 0 else 'on'})"
                    )
                    return
                try:
                    cap = engine.set_concurrency(int(args[1]))
                except ValueError:
                    print_error("limit must be an integer")
                    return
                print_msg(f"[+] concurrency cap = {cap}" + (" (admission off)" if cap == 0 else ""))
                return
            if args[0] == "queue":
                queued = engine.store.queue()
                if not queued:
                    print_msg("[*] queue empty.")
                for record in queued:
                    print_msg(
                        f"  [{record['task_id']}] "
                        f"queued_at={int(record.get('queued_at', 0) or 0)} "
                        f":: {str(record.get('goal', ''))[:100]}"
                    )
                return
            results = engine.drain_queue(max_tasks=3)
            if not results:
                print_msg("[*] nothing to drain (cap blocked or queue empty).")
            for summary in results:
                print_msg(f"  [{summary['task_id']}] {summary['status']} rounds={summary['rounds']}")
            return
        if args[0] == "spawn":
            sources = [s.strip() for s in (extract_flag(args, "--from") or "").split(",") if s.strip()]
            words: list[str] = []
            skip_next = False
            for token in args[1:]:
                if skip_next:
                    skip_next = False
                    continue
                if token == "--from":
                    skip_next = True
                    continue
                if not token.startswith("--"):
                    words.append(token)
            goal = " ".join(words).strip()
            if not sources or not goal:
                print_error("Usage: lazy_task spawn <goal> --from t0001[,t0002]")
                return
            summary = _engine().spawn_task(goal, source_task_ids=sources)
            inherited = summary.get("inherited", {})
            print_msg(
                f"[+] task {summary['task_id']}: {summary['goal'][:120]} "
                f"(inherited scope={inherited.get('scope', 0)}"
                f" facts={inherited.get('facts', 0)} from {','.join(inherited.get('sources', []))})"
            )
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
                result = engine.delete_task(task_id)
                print_msg(f"[*] {task_id} deleted ({len(result.get('removed', []))} store files).")
                return
        print_error(
            "Usage: lazy_task create <goal> [--from t0001,t0002] | lazy_task list | lazy_task show|pause|resume|delete [--task T] | lazy_task spawn <goal> --from t0001[,t0002]"
        )

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
        try:
            ctx = _engine().graph_context(task_id)
        except Exception:
            ctx = {}
        for hub in (ctx.get("hubs", []) or [])[:5]:
            print_msg(f"  hub #{hub['id']} [{hub['kind']}/{hub['state']}] x{hub['degree']} {hub['text'][:90]}")
        for sug in (ctx.get("suggested", []) or [])[:5]:
            print_msg(f"  next [{sug['kind']}] {sug['value'][:90]} (heat {sug['heat']})")
        if ctx.get("islands"):
            print_msg(f"  islands: {len(ctx['islands'])} unlinked assets (see /api/loop_graph?task={task_id})")

    @cmd2.with_category(ai_category)
    def do_lazy_context(self, line):
        """Render the bounded prompt context the planner/worker LLMs receive. Usage: lazy_context [--task T] [--budget N]"""
        args = shlex.split(line) if line.strip() else []
        task_id = self._require_task(args)
        if not task_id:
            print_error("Usage: lazy_context [--task T] [--budget N]")
            return
        budget = 2000
        raw = extract_flag(args, "--budget")
        if raw:
            try:
                budget = max(200, min(20000, int(raw)))
            except ValueError:
                pass
        from modules.lazy_engine import ExplorationGraph, build_prompt_context

        engine = _engine()
        context = build_prompt_context(task_id, ExplorationGraph(task_id), engine.assets, engine.store, budget=budget)
        print_msg(context or "[*] empty context")

    @cmd2.with_category(ai_category)
    def do_lazy_skill(self, line):
        """Skills: list|show <name>|preview|inject <name...>|clear|auto on|off|mirror [name]|register-hermes. Usage: lazy_skill ... [--task T]"""
        args = shlex.split(line) if line.strip() else []
        from modules.lazy_skills import get_skill, list_skills, skills_context

        if not args or args[0] == "list":
            entries = list_skills()
            for entry in entries:
                print_msg(f"  {entry['name']}: {entry['description'][:100]}")
            if not entries:
                print_msg("[*] no skills found.")
            return
        if args[0] == "show" and len(args) >= 2:
            entry = get_skill(args[1])
            if not entry:
                print_error(f"unknown skill: {args[1]}")
                return
            print_msg(f"[*] {entry['name']} :: {entry['path']}")
            print_msg(entry["excerpt"][:2000])
            return
        task_id = self._require_task(args)
        if not task_id:
            print_error("preview/inject/clear/auto need --task T")
            return
        engine = _engine()
        record = engine.store.get(task_id) or {}
        if args[0] == "preview":
            text = skills_context(
                str(record.get("goal", "")),
                explicit=list(record.get("skills", []) or []),
                auto=bool(record.get("skills_auto", True)),
                budget=800,
            )
            print_msg(text or "[*] no skills matched.")
            return
        if args[0] == "inject":
            names = [token for token in args[1:] if not token.startswith("--")]
            unknown = [name for name in names if not get_skill(name)]
            if unknown:
                print_error(f"unknown skill(s): {', '.join(unknown)}")
                return
            state = engine.store.set_skills(task_id, names)
            print_msg(f"[+] skills pinned: {', '.join(state['skills']) or '-'}")
            return
        if args[0] == "clear":
            engine.store.set_skills(task_id, [])
            print_msg("[+] pinned skills cleared.")
            return
        if args[0] == "auto" and len(args) >= 2 and args[1] in ("on", "off"):
            state = engine.store.set_skills(task_id, list(record.get("skills", []) or []), auto=args[1] == "on")
            print_msg(f"[+] skills auto-match {'on' if state['skills_auto'] else 'off'}.")
            return
        if args[0] == "mirror":
            from modules.lazy_skill_mirror import mirror_all, mirror_skill

            names = [token for token in args[1:] if not token.startswith("--")]
            if names:
                for name in names:
                    summary = mirror_skill(name)
                    if summary.get("error"):
                        print_error(f"{name}: {summary['error']}")
                    else:
                        print_msg(f"[+] {name}: {summary['path']}" + ("" if summary.get("changed") else " (unchanged)"))
            else:
                summary = mirror_all()
                print_msg(f"[*] {summary['mirrored']} skill(s) mirrored for Hermes.")
            return
        if args[0] == "register-hermes":
            from modules.lazy_skill_mirror import register_external_dirs

            summary = register_external_dirs()
            if summary.get("error"):
                print_error(summary["error"])
            else:
                print_msg(
                    "[+] hermes external_dirs updated (backup: "
                    f"{summary.get('backup') or 'none — already registered'})."
                )
            return
        print_error(
            "Usage: lazy_skill list|show <name>|preview|inject <name...>|clear|auto on|off|mirror|register-hermes [--task T]"
        )

    @cmd2.with_category(ai_category)
    def do_lazy_workspace(self, line):
        """Confined workspace files: list [path]|read <path>|write <path> <text>|mkdir <path>|rm <path>|path. Usage: lazy_workspace ..."""
        args = shlex.split(line) if line.strip() else []
        from modules import workspace as _ws

        if not args or args[0] == "list":
            rel = args[1] if len(args) > 1 else ""
            try:
                entries = _ws.list_entries(rel)
            except (FileNotFoundError, PermissionError) as exc:
                print_error(str(exc))
                return
            for entry in entries[:200]:
                print_msg(f"  [{entry['kind']}] {entry['name']} ({entry['size']}B)")
            return
        if args[0] == "path":
            print_msg(str(_ws.root()))
            return
        if args[0] == "read" and len(args) >= 2:
            try:
                content = _ws.read_text(args[1])
            except (FileNotFoundError, PermissionError) as exc:
                print_error(str(exc))
                return
            print_msg(content[:6000] if content else "[*] empty file.")
            return
        if args[0] == "write" and len(args) >= 3:
            try:
                written = _ws.write_text(args[1], self._free_text(args[2:]))
            except (ValueError, PermissionError) as exc:
                print_error(str(exc))
                return
            print_msg(f"[+] wrote {written} chars to {args[1]}")
            return
        if args[0] == "mkdir" and len(args) >= 2:
            try:
                _ws.make_dir(args[1])
            except PermissionError as exc:
                print_error(str(exc))
                return
            print_msg(f"[+] {args[1]} created.")
            return
        if args[0] == "rm" and len(args) >= 2:
            try:
                removed = _ws.remove(args[1])
            except PermissionError as exc:
                print_error(str(exc))
                return
            print_msg("[+] removed." if removed else "[-] not found.")
            return
        print_error("Usage: lazy_workspace list [path]|read <path>|write <path> <text>|mkdir <path>|rm <path>|path")

    @cmd2.with_category(ai_category)
    def do_lazy_selfupdate(self, line):
        """Self-update: check [--branch B]|apply [--yes] [--branch B]. Usage: lazy_selfupdate ..."""
        args = shlex.split(line) if line.strip() else []
        from modules.selfupdate import apply as _apply
        from modules.selfupdate import check as _check

        action = args[0] if args else "check"
        branch = extract_flag(args, "--branch") or ""
        if action == "check":
            info = _check(branch)
            if not info.get("ok"):
                print_error(f"selfupdate check failed: {info.get('error')}")
                return
            print_msg(f"[*] {info['branch']} @ {info['head']}: behind={info['behind']} ahead={info['ahead']}")
            if int(info["behind"]) > 0 and int(info["ahead"]) == 0:
                print_msg("    update with: lazy_selfupdate apply --yes")
            return
        if action == "apply":
            result = _apply(branch, confirm="--yes" in args)
            print_msg(
                f"[+] update {result.get('reason')}"
                if result.get("applied")
                else f"[-] not applied: {result.get('reason')}"
            )
            return
        print_error("Usage: lazy_selfupdate check [--branch B] | lazy_selfupdate apply --yes [--branch B]")

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
        worker = Worker(
            "worker-cli",
            task_id,
            engine.assets,
            graph,
            ActivityLog(task_id),
            TrafficLog(task_id),
            Guard(task_id),
            engine.store,
            shell=self._resolve_shell(),
        )
        outcome = worker.execute(node)
        print_msg(
            f"[+] intent #{node.node_id} -> {outcome['state']}: "
            f"facts={outcome['facts']} assets={outcome['assets']} findings={outcome['findings']}"
        )

    @cmd2.with_category(ai_category)
    def do_lazy_trace(self, line):
        """Worker trace exchange. Usage: lazy_trace list|search <q>|search-all <q>|get <intent>|steps <intent> [--q Q]|step <intent> <n> [--task T]"""
        args = shlex.split(line) if line.strip() else []
        task_id = self._require_task(args)
        if not task_id or not args:
            print_error("Usage: lazy_trace list|search|search-all|get|steps|step ... [--task T]")
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
        elif mode == "search-all" and rest:
            for hit in log.search_all(" ".join(rest))[:20]:
                print_msg(f"  [#{hit['intent_id']}:{hit['step']}/{hit.get('worker')}] {str(hit.get('text', ''))[:160]}")
        elif mode == "steps" and rest:
            inline = extract_flag(args, "--q") or ""
            try:
                view = log.trace(int(rest[0]), query=inline)
            except (ValueError, KeyError) as exc:
                print_error(str(exc))
                return
            for step in view["steps"]:
                print_msg(f"  {step['step']}/{view['total']} [{step.get('kind')}] {str(step.get('text', ''))[:200]}")
        elif mode == "step" and len(rest) >= 2:
            try:
                view = log.trace(int(rest[0]), step_id=int(rest[1]))
            except (ValueError, KeyError) as exc:
                print_error(str(exc))
                return
            record = view["step"]
            print_msg(
                f"  [#{view['intent_id']}:{rest[1]}/{record.get('worker')}/{record.get('kind')}]"
                f" {str(record.get('text', ''))[:2000]}"
            )
        else:
            print_error("Usage: lazy_trace list|search|search-all|get|steps|step ... [--task T]")

    @cmd2.with_category(ai_category)
    def do_lazy_broadcast(self, line):
        """Exploration timeline. Usage: lazy_broadcast [--task T] [--kind K] [--q Q] [--asc] [--page N] [--limit N]"""
        args = shlex.split(line) if line.strip() else []
        task_id = self._require_task(args)
        if not task_id:
            return
        kinds: list[str] = []
        idx = 0
        while idx < len(args):
            if args[idx] == "--kind" and idx + 1 < len(args):
                kinds.append(args[idx + 1])
                idx += 2
                continue
            idx += 1
        query = extract_flag(args, "--q") or ""
        page_raw = extract_flag(args, "--page") or "1"
        limit_raw = extract_flag(args, "--limit") or "20"
        order = "asc" if "--asc" in args else "desc"
        try:
            page = max(1, int(page_raw))
        except ValueError:
            page = 1
        try:
            limit = max(1, min(100, int(limit_raw)))
        except ValueError:
            limit = 20
        result = _engine().broadcast(task_id, kinds=kinds or None, query=query, order=order, page=page, per_page=limit)
        for item in result["items"]:
            print_msg(f"  #{item['id']} [{item['kind']}/{item['state']}] {item['day']} {str(item['text'])[:140]}")
        print_msg(
            f"page {result['page']} ({len(result['items'])}/{result['total']})"
            + (" more" if result["has_more"] else " end")
        )

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
    def do_lazy_intent_delete(self, line):
        """Delete an intent. Usage: lazy_intent_delete <id> --reason <text> [--hard] [--task T] [--yes]"""
        args = shlex.split(line) if line.strip() else []
        task_id = self._require_task(args)
        if not task_id or not args:
            print_error("Usage: lazy_intent_delete <id> --reason <text> [--hard] [--task T] [--yes]")
            return
        try:
            intent_id = int(args[0])
        except ValueError:
            print_error("Usage: lazy_intent_delete <id> --reason <text> [--hard] [--task T] [--yes]")
            return
        reason = extract_flag(args, "--reason") or ""
        if not reason:
            print_error("A reason is required: lazy_intent_delete <id> --reason <text>")
            return
        hard = "--hard" in args
        engine = _engine()
        try:
            preview = engine.preview_delete_intent(task_id, intent_id)
        except (KeyError, ValueError) as exc:
            print_error(str(exc))
            return
        if hard and "--yes" not in args:
            print_warn(
                f"Hard delete removes {preview['cascade']} node(s),"
                f" keeps {len(preview['shared'])} shared. Re-run with --yes to confirm."
            )
            return
        try:
            result = engine.delete_intent(task_id, intent_id, mode="hard" if hard else "soft", reason=reason)
        except (KeyError, ValueError) as exc:
            print_error(str(exc))
            return
        if result["mode"] == "soft":
            print_msg(f"[+] intent #{intent_id} soft-deleted (outputs kept). Planner notified.")
        else:
            print_msg(
                f"[+] intent #{intent_id} hard-deleted:"
                f" removed {len(result['removed'])}, kept {len(result['shared'])} shared."
            )

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
            print_msg(
                "[+] goal proven."
                if ok
                else "[-] prove failed (need goal + finding/fact ids + reason; quantitative bars enforced)."
            )
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
        """Assets: add <kind> <value> | list [kind] | scoped [--kind K] | coverage | untested. Usage: lazy_asset ..."""
        args = shlex.split(line) if line.strip() else []
        if not args:
            print_error("Usage: lazy_asset add <kind> <value> | lazy_asset list [kind] | scoped | coverage | untested")
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
        elif args[0] == "scoped":
            task_id = self._task_id(args)
            record = (engine.store.get(task_id) or {}) if task_id else {}
            kind = extract_flag(args, "--kind") or ""
            for node in engine.assets.scoped(record.get("scope", []), kind=kind)[:50]:
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
            print_error("Usage: lazy_asset add <kind> <value> | lazy_asset list [kind] | scoped | coverage | untested")

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
        """Traffic: list|search <q>|search-host <host> [--port P]|get <digest>|body <digest>|blob <digest> [--part req|resp] [--offset N] [--length N]|search-body <q>|templates|template <t>|bind <finding> <digest> [--role R] [--note N]|evidence <finding>|export <path>|archive|clear|start [--port P] [--upstream H:P]|stop|status|ca|trust|ingest|recorder-export <zip> [--task T]|recorder-import <zip>|recorder-inbox|recorder-gc [--days N]. Usage: lazy_traffic ... [--task T] [--limit N]"""
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
        elif args[0] == "search-host" and len(args) >= 2:
            port = extract_flag(args, "--port") or ""
            for record in TrafficLog(task_id).search_host(args[1], port=port, limit=limit):
                print_msg(f"  [{record.get('digest')}] {str(record.get('command', ''))[:120]}")
        elif args[0] == "bind" and len(args) >= 3:
            role = extract_flag(args, "--role") or "supporting"
            note = extract_flag(args, "--note") or ""
            try:
                ok = TrafficLog(task_id).bind(int(args[1]), args[2], ExplorationGraph(task_id), role=role, note=note)
            except ValueError as exc:
                print_error(str(exc))
                return
            print_msg("[+] bound." if ok else "[-] bind failed.")
        elif args[0] == "evidence" and len(args) >= 2:
            try:
                rows = TrafficLog(task_id).evidence(int(args[1]), ExplorationGraph(task_id))
            except (ValueError, KeyError) as exc:
                print_error(str(exc))
                return
            if not rows:
                print_msg("[*] no evidences bound.")
            for pos, ref in enumerate(rows, start=1):
                print_msg(
                    f"  {pos}. [{ref.get('role')}] {ref.get('digest')}"
                    f"{(' :: ' + str(ref.get('note'))[:100]) if ref.get('note') else ''}"
                )
        elif args[0] == "export" and len(args) >= 2:
            print_msg(f"[+] {TrafficLog(task_id).export(args[1], limit)}")
        elif args[0] == "archive":
            print_msg(f"[+] {TrafficLog(task_id).archive(label=task_id or 'global')}")
        elif args[0] == "clear":
            print_msg(f"[+] cleared {TrafficLog(task_id).clear()} records.")
        elif args[0] == "start":
            port = 0
            raw_port = extract_flag(args, "--port")
            if raw_port:
                try:
                    port = int(raw_port)
                except ValueError:
                    port = 0
            status = _engine().proxy_start(
                port=port, task_id=task_id or "", upstream=extract_flag(args, "--upstream") or ""
            )
            trust = status.get("trust") or {}
            trust_note = (
                "trusted" if trust.get("installed") else f"trust pending ({trust.get('reason', 'not attempted')})"
            )
            upstream_note = f", upstream={status['upstream']}" if status.get("upstream") else ""
            print_msg(
                f"[+] recorder proxy on {status['host']}:{status['port']} "
                f"(exchanges={status['exchanges']}, CA {trust_note}{upstream_note})"
            )
            print_msg(f"    CA: {status['ca_path']}")
        elif args[0] == "trust":
            ca_path = _engine().proxy_status().get("ca_path", "")
            if not ca_path:
                print_error("Start the proxy first: lazy_traffic start")
                return
            from modules.lazy_proxy import install_ca_nss, install_ca_trust

            result = install_ca_trust(ca_path)
            if result.get("installed"):
                print_msg(f"[+] CA trust {result['reason']} -> {result['anchor']}")
            else:
                print_error(f"CA trust failed: {result.get('reason')}")
            nss = install_ca_nss(ca_path)
            if nss.get("installed"):
                print_msg(f"[+] NSS trust: {nss['installed']}/{nss['profiles']} profile(s).")
            else:
                print_msg(f"[*] NSS trust skipped: {nss.get('reason')}")
        elif args[0] == "stop":
            status = _engine().proxy_stop()
            print_msg("[+] recorder proxy stopped." if not status.get("running") else "[-] proxy still running.")
        elif args[0] == "status":
            status = _engine().proxy_status()
            print_msg(
                f"  running={status['running']} {status['host']}:{status['port']} "
                f"task={status['task'] or '-'} exchanges={status['exchanges']}"
            )
            print_msg(
                f"  upstream={status.get('upstream') or '-'} ca={status['ca_path'] or '-'} dir={status['traffic_dir']}"
            )
            if status.get("running"):
                print_msg(
                    f"  captures={','.join(status.get('captures', []))} "
                    f"mitm={'on' if status.get('mitm') else 'off'} "
                    f"(HTTPS intercepted via CONNECT)"
                )
        elif args[0] == "ca":
            ca_path = _engine().proxy_status().get("ca_path", "")
            print_msg(ca_path or "[-] no CA yet (start the proxy first).")
        elif args[0] == "body" and len(args) >= 2:
            try:
                body = TrafficLog(task_id).recorder_body(args[1])
            except KeyError as exc:
                print_error(str(exc))
                return
            if not body:
                print_msg("[-] digest has no recorder body (not a proxy exchange).")
            else:
                print_msg(f"  {body.get('req_head', '')}")
                print_msg(f"  status={body.get('status')} host={body.get('host')}:{body.get('port')}")
                print_msg(f"  req: {str(body.get('req_body', ''))[:800]}")
                print_msg(f"  resp: {str(body.get('resp_body', ''))[:800]}")
        elif args[0] == "ingest":
            count = _engine().ingest_proxy_traffic(task_id) if task_id else 0
            print_msg(f"[+] ingested {count} exchange(s).")
        elif args[0] == "blob" and len(args) >= 2:
            part = extract_flag(args, "--part") or "resp"
            if part not in ("req", "resp"):
                print_error("--part must be req|resp")
                return
            offset = 0
            length = 8192
            raw_offset = extract_flag(args, "--offset")
            raw_length = extract_flag(args, "--length")
            try:
                offset = max(0, int(raw_offset)) if raw_offset else 0
                length = max(1, min(1048576, int(raw_length))) if raw_length else 8192
            except ValueError:
                pass
            try:
                chunk = TrafficLog(task_id).recorder_blob(args[1], part=part, offset=offset, length=length)
            except KeyError as exc:
                print_error(str(exc))
                return
            print_msg(
                f"  {chunk['part']} offset={chunk['offset']} len={chunk['length']} "
                f"total={chunk['total']} eof={chunk['eof']}"
            )
            print_msg(str(chunk["data"])[:2000])
        elif args[0] == "search-body" and len(args) >= 2:
            if not task_id:
                print_error("search-body needs --task T (proxy traffic is per task).")
                return
            hits = _engine().search_proxy_body(task_id, " ".join(args[1:]), limit)
            for hit in hits:
                print_msg(
                    f"  [{str(hit.get('exchange_id', ''))[:16]}] {hit.get('status')} {str(hit.get('url', ''))[:120]}"
                )
                print_msg(f"      {str(hit.get('snippet', ''))[:200]}")
            if not hits:
                print_msg("[*] no body hits.")
        elif args[0] in ("recorder-export", "recorder-import") and len(args) >= 2:
            from modules.lazy_proxy import get_proxy
            from modules.traffic_recorder import TrafficRecorder

            controller = get_proxy()
            recorder = controller.recorder() or TrafficRecorder(controller.traffic_dir)
            try:
                if args[0] == "recorder-export":
                    result = recorder.export_archive(args[1], task=extract_flag(args, "--task") or "")
                    print_msg(
                        f"[+] exported {result['exported']} exchange(s) ({result['bodies']} bodies) -> {result['path']}"
                    )
                else:
                    result = recorder.import_archive(args[1])
                    print_msg(
                        f"[+] imported {result['imported']} exchange(s) "
                        f"({result['bodies']} bodies) from {result['path']}"
                    )
            except (OSError, ValueError) as exc:
                print_error(str(exc))
        elif args[0] == "recorder-gc":
            days = 30
            raw_days = extract_flag(args, "--days")
            if raw_days:
                try:
                    days = max(1, int(raw_days))
                except ValueError:
                    days = 30
            from modules.lazy_proxy import get_proxy
            from modules.traffic_recorder import TrafficRecorder

            controller = get_proxy()
            recorder = controller.recorder() or TrafficRecorder(controller.traffic_dir)
            result = recorder.gc(older_than_sec=days * 86400)
            print_msg(f"[+] garbage collected {result['removed']} exchange(s) older than {days}d.")
        elif args[0] == "recorder-inbox":
            from modules.lazy_proxy import get_proxy
            from modules.traffic_recorder import TrafficRecorder

            controller = get_proxy()
            recorder = controller.recorder() or TrafficRecorder(controller.traffic_dir)
            summary = recorder.import_inbox()
            print_msg(f"[+] inbox import: {summary['imported']} exchange(s) from {len(summary['files'])} file(s).")
        else:
            print_error(
                "Usage: lazy_traffic list|search|search-host|get|body|templates|template|"
                "bind|evidence|export|archive|clear|start|stop|status|ca|ingest ..."
            )

    @cmd2.with_category(ai_category)
    def do_lazy_guard(self, line):
        """Guard gate: check <cmd> | rule-add <pattern> <allow|ask|deny> [reason] | rule-del <p> | judge on|off [--fail allow|deny] | judge fail <allow|deny> | judge | audit [--action A] [--source S] [--q Q] [--limit N] | lookup <tool_use_id> | stats | pending | approve <id> | deny <id>. Usage: lazy_guard ..."""
        args = shlex.split(line) if line.strip() else []
        if not args:
            print_error(
                "Usage: lazy_guard check <cmd> | lazy_guard rule-add ... | lazy_guard rule-del ... | lazy_guard audit | lookup <id> | pending | approve <id> | deny <id>"
            )
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
        elif args[0] == "judge":
            rest = [a for a in args[1:] if not a.startswith("--")]
            if rest and rest[0] in ("on", "off"):
                try:
                    config = guard.set_judge(rest[0] == "on", fail_action=extract_flag(args, "--fail") or "allow")
                except ValueError as exc:
                    print_error(str(exc))
                    return
                print_msg(f"[+] judge enabled={config['enabled']} fail={config['fail_action']}")
            elif len(rest) >= 2 and rest[0] == "fail":
                try:
                    config = guard.set_judge(bool(guard.judge.get("enabled", False)), rest[1])
                except ValueError as exc:
                    print_error(str(exc))
                    return
                print_msg(f"[+] judge enabled={config['enabled']} fail={config['fail_action']}")
            else:
                config = guard.judge or {"enabled": False, "fail_action": "allow"}
                print_msg(f"[*] judge enabled={bool(config.get('enabled'))} fail={config.get('fail_action', 'allow')}")
        elif args[0] == "audit":
            action = extract_flag(args, "--action") or ""
            source = extract_flag(args, "--source") or ""
            query = extract_flag(args, "--q") or ""
            limit = 20
            raw = extract_flag(args, "--limit")
            if raw:
                try:
                    limit = max(1, min(500, int(raw)))
                except ValueError:
                    pass
            pending = queue.pending()
            if pending:
                print_msg(f"[*] {len(pending)} pending (independent of history pagination):")
                for item in pending[-5:]:
                    print_msg(f"  ! #{item['id']} [{item['tool']}] {item['command'][:100]}")
            for entry in guard.audit(limit=limit, action=action, source=source, query=query):
                print_msg(
                    f"  [{entry.get('action')}] {entry.get('tool_use_id', '-')}"
                    f" {entry.get('tool')}: {str(entry.get('command', ''))[:100]}"
                )
        elif args[0] == "lookup" and len(args) >= 2:
            try:
                hit = guard.lookup(args[1])
            except KeyError as exc:
                print_error(str(exc))
                return
            entry = hit["audit"]
            print_msg(
                f"[*] {entry.get('tool_use_id')} [{entry.get('action')}]"
                f" {entry.get('tool')}: {entry.get('command', '')[:200]}"
            )
            if hit.get("intercept"):
                item = hit["intercept"]
                print_msg(f"  intercept #{item.get('id')} [{item.get('state')}] :: {str(item.get('reason', ''))[:120]}")
            if hit.get("traffic"):
                print_msg(f"  traffic [{hit['traffic'].get('digest')}] {str(hit['traffic'].get('output', ''))[:200]}")
            for record in hit.get("activity", []):
                print_msg(f"  trace [{record.get('worker')}/{record.get('kind')}] {str(record.get('text', ''))[:160]}")
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
            print_error("Usage: lazy_guard check|rule-add|rule-del|audit|lookup|stats|rules|pending|approve|deny ...")

    @cmd2.with_category(ai_category)
    def do_lazy_finding(self, line):
        """Findings: list [--full] [--limit N]|report <name> :: <summary>|status <id> <st>|update <id> <text>|context <id>. Usage: lazy_finding ... [--task T] [--severity S] [--vulnclass C]"""
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
                print_msg(
                    f"  #{node.node_id} [{node.meta.get('severity', 'info')}/{node.meta.get('status', 'pending')}/{verdict}] {node.text[:140]}"
                )
                if full:
                    print_msg(f"    poc: {str(node.meta.get('poc', ''))[:300]}")
                    print_msg(
                        f"    assets: {graph.anchors_for(node.node_id)} "
                        f"traffic: {TrafficLog(task_id).evidence(node.node_id, graph)[:5]}"
                    )
        elif args[0] == "report" and len(args) >= 2:
            raw = self._free_text(args[1:])
            name, _, summary = raw.partition("::")
            node = service.report(
                (name or raw)[:200],
                summary=summary.strip()[:1000],
                severity=extract_flag(args, "--severity") or "",
                vulnclass=extract_flag(args, "--vulnclass") or "",
            )
            print_msg(f"[+] finding #{node.node_id} [{node.meta.get('severity')}]: {node.text[:140]}")
        elif args[0] == "status" and len(args) >= 3:
            try:
                ok = service.set_status(int(args[1]), args[2])
            except ValueError as exc:
                print_error(str(exc))
                return
            print_msg("[+] status set." if ok else "[-] unknown finding.")
        elif args[0] == "update" and len(args) >= 3:
            version = service.update_report(int(args[1]), self._free_text(args[2:]))
            print_msg(f"[+] report v{version} stored." if version else "[-] unknown finding or empty report.")
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
            print_error("Usage: lazy_finding list|report|status|update|context ... [--task T]")

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
        """Export severity-ranked report. Usage: lazy_report [--task T] [--format md|json|csv] [--out PATH]"""
        args = shlex.split(line) if line.strip() else []
        task_id = self._require_task(args)
        if not task_id:
            return
        fmt = (extract_flag(args, "--format") or "md").lower()
        out = extract_flag(args, "--out") or ""
        result = _engine().export_findings_report(task_id, path=out, fmt=fmt)
        if out:
            print_msg(f"[+] report written to {result['path']} ({result['findings']} findings, {result['format']})")
            return
        from pathlib import Path as _Path

        print_msg(_Path(result["path"]).read_text(encoding="utf-8")[:4000])

    @cmd2.with_category(ai_category)
    def do_lazy_runtime(self, line):
        """Show/set loop runtime: budgets, deadline, abort cause, heartbeat, settlement text. Usage: lazy_runtime show [--task T] | lazy_runtime budget <max_toolcalls> <max_findings> <timeout_s> [--task T] | lazy_runtime settle <agent> <reason> [--task T]"""
        args = shlex.split(line) if line.strip() else []
        task_id = self._require_task(args)
        if not task_id or not args:
            print_error(
                "Usage: lazy_runtime show [--task T] | lazy_runtime budget <toolcalls> <findings> <timeout> [--task T]"
            )
            return
        engine = _engine()
        if args[0] == "show":
            snap = engine.runtime.heartbeat(task_id)
            check = engine.budget.check(task_id)
            print_msg(
                f"[*] {task_id} [{snap.get('status')}] abort={snap.get('abort_cause', '') or 'none'} "
                f"workers={snap.get('workers', 0)} deadline={snap.get('deadline', 0.0)}"
            )
            print_msg(
                f"    budget ok={check.get('ok')} {check.get('reason', '')} "
                f"used={check.get('used', {})} limits={check.get('limits', {})}"
            )
            print_msg(f"    watermark={snap.get('watermark', 0)}")
        elif args[0] == "budget" and len([a for a in args[1:] if not a.startswith("--")]) >= 3:
            rest = [a for a in args[1:] if not a.startswith("--")]
            try:
                limits = engine.budget.set_limits(
                    task_id, max_toolcalls=int(rest[0]), max_findings=int(rest[1]), timeout_sec=float(rest[2])
                )
            except ValueError as exc:
                print_error(str(exc))
                return
            print_msg(f"[+] budget: {limits}")
        elif args[0] == "settle":
            rest = [a for a in args[1:] if not a.startswith("--")]
            if len(rest) < 2:
                print_error("Usage: lazy_runtime settle <worker|planner|main> <timeout|max_turns> [--task T]")
                return
            from modules.lazy_engine import settlement_prompt

            print_msg(settlement_prompt(rest[0], rest[1]))
        else:
            print_error(
                "Usage: lazy_runtime show [--task T] | lazy_runtime budget ... [--task T] "
                "| lazy_runtime settle <agent> <reason> [--task T]"
            )

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
                items = [n for n in items if n.meta.get("cold") or n.state == "exhausted" or n.meta.get("cold_digest")]
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
        """Evidence vault and frozen package.

        Usage:
            lazy_evidence add <finding> <kind> <body> [--task T]
            lazy_evidence list <finding> [--task T]
            lazy_evidence verify|gc [--task T]
            lazy_evidence package [path] [--task T]
            lazy_evidence search <query> [limit] [--task T]
        """
        args = shlex.split(line) if line.strip() else []
        task_id = self._require_task(args)
        if not task_id or not args:
            print_error("Usage: lazy_evidence add|list|verify|gc|package|search ... [--task T]")
            return
        from modules.lazy_engine import EvidenceStore, LazyEngine

        if args[0] == "search":
            if len(args) < 2:
                print_error("Usage: lazy_evidence search <query> [limit]")
                return
            limit = int(args[2]) if len(args) > 2 and args[2].isdigit() else 20
            try:
                from modules import lazy_proxy

                recorder = lazy_proxy.get_proxy().recorder()
                hits = recorder.search_body(args[1], limit=limit) if recorder is not None else []
            except Exception as exc:
                print_error(f"Evidence search failed: {exc}")
                return
            if not hits:
                print_msg("No body match.")
                return
            print_msg(f"{len(hits)} body hit(s)")
            for hit in hits:
                print_msg(f"  {hit.get('exchange_id', '')} [{hit.get('status', 0)}] {str(hit.get('url', ''))[:100]}")
                snippet = str(hit.get("snippet", "")).replace("\n", " ")[:160]
                if snippet:
                    print_msg(f"    {snippet}")
            return
        if args[0] == "package":
            dest = args[1] if len(args) > 1 and not args[1].startswith("--") else None
            try:
                package = LazyEngine().export_evidence(task_id, dest)
            except Exception as exc:
                print_error(f"Evidence package failed: {exc}")
                return
            print_msg(f"Evidence package: {package.get('path', '')} ({package.get('files', 0)} file(s))")
            return
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
            print_error("Usage: lazy_evidence add|list|verify|gc|package|search ... [--task T]")

    @cmd2.with_category(ai_category)
    def do_lazy_ask(self, line):
        """Bounded side question over task context. Usage: lazy_ask <question> [--task T] [--session S] | lazy_ask history [--task T] [--session S]"""
        args = shlex.split(line) if line.strip() else []
        task_id = self._require_task(args)
        if not task_id or not args:
            print_error("Usage: lazy_ask <question> [--task T] [--session S] | lazy_ask history [--task T]")
            return
        from modules.lazy_engine import LlmPool, SideQuestions

        table = SideQuestions()
        if args[0] == "history" and all(a.startswith("--") for a in args[1:]):
            session = extract_flag(args, "--session") or ""
            for item in table.history(task_id, session=session):
                print_msg(
                    f"  [#{item.get('id')}/{item.get('session')}]"
                    f" Q: {str(item.get('question', ''))[:120]}"
                    f" A: {str(item.get('answer', ''))[:160]}"
                )
            return
        question = self._free_text(args)
        if not question:
            print_error("Usage: lazy_ask <question> [--task T] [--session S]")
            return
        answer = table.ask(task_id, question, LlmPool(), session=extract_flag(args, "--session") or "btw")
        print_msg(f"[*] {answer['answer'][:1500]} (budget={answer['budget']} chars)")

    def _agent_main_tools(self, task_id: str) -> list[dict]:
        """Tool registry for the main agent (full tool calling surface)."""
        shell = self._resolve_shell()
        engine = _engine()

        def run_command(command: str = "") -> str:
            """Execute one shell command or LazyOwn verb and return its output."""
            from modules.auto_registry import execute_shell_verb, execute_streaming, is_routable_command
            from modules.lazy_engine import ActivityLog, Guard, TrafficLog

            verdict = Guard(task_id).check("Bash", command, source="main-agent")
            if verdict["action"] == "deny":
                return f"blocked by guard: {verdict.get('reason', '')}"
            if verdict["action"] == "ask":
                return "held for approval (ask rule): run it yourself or add an allow rule with lazy_guard rules-add"
            if shell is not None and is_routable_command(command):
                output = execute_shell_verb(shell, command, timeout_sec=600.0)
            else:
                output = execute_streaming(command, timeout_sec=600.0)
            if task_id:
                try:
                    TrafficLog(task_id).record("bash", command, output, {"worker": "main-agent"})
                    ActivityLog(task_id).emit("main-agent", "tool", f"{command[:160]}", intent_id=0)
                except Exception:
                    pass
            return output or "(no output)"

        def list_tasks() -> str:
            """List every task with status, intents, facts and findings."""
            return json.dumps(engine.list_tasks(), ensure_ascii=False)[:2500]

        def task_graph(task: str = "") -> str:
            """Graph overview of one task (defaults to the active task)."""
            return json.dumps(engine.task_graph(task or task_id), ensure_ascii=False)[:2500]

        def task_findings(task: str = "") -> str:
            """Findings of one task with severity, status and report size."""
            return json.dumps(engine.task_findings(task or task_id), ensure_ascii=False)[:2500]

        def campaign_sitrep() -> str:
            """Campaign summary: tasks, findings and phase counters."""
            rows = engine.list_tasks()
            return json.dumps(
                {
                    "tasks": len(rows),
                    "findings": sum(row.get("findings", 0) for row in rows),
                    "running": [row["task_id"] for row in rows if row.get("status") == "running"],
                    "rows": rows[:20],
                },
                ensure_ascii=False,
            )[:2500]

        def add_hint(text: str = "") -> str:
            """Inject an operator hint into the active task planner."""
            if not task_id:
                return "no active task: pass --task T"
            node = engine.add_hint(task_id, text)
            return f"hint #{node.node_id} queued for the next planner round"

        def steer_intent(intent: str = "", message: str = "") -> str:
            """Send a mid-run course correction to a running intent."""
            if not task_id:
                return "no active task: pass --task T"
            engine.store.steer(task_id, int(intent), message)
            return f"steer queued for intent #{intent}"

        return [
            {
                "name": "run_command",
                "func": run_command,
                "description": "Execute one shell command or LazyOwn verb (guard/audit applied).",
                "parameters": {"command": {"type": "string", "description": "Command line"}},
                "required": ["command"],
            },
            {
                "name": "list_tasks",
                "func": list_tasks,
                "description": "List every task with live counters.",
                "parameters": {},
            },
            {
                "name": "task_graph",
                "func": task_graph,
                "description": "Graph overview of a task.",
                "parameters": {"task": {"type": "string", "description": "Task id"}},
            },
            {
                "name": "task_findings",
                "func": task_findings,
                "description": "Findings of a task.",
                "parameters": {"task": {"type": "string", "description": "Task id"}},
            },
            {
                "name": "campaign_sitrep",
                "func": campaign_sitrep,
                "description": "Campaign summary across tasks.",
                "parameters": {},
            },
            {
                "name": "add_hint",
                "func": add_hint,
                "description": "Queue an operator hint on the active task.",
                "parameters": {"text": {"type": "string", "description": "Hint text"}},
                "required": ["text"],
            },
            {
                "name": "steer_intent",
                "func": steer_intent,
                "description": "Course-correct a running intent.",
                "parameters": {
                    "intent": {"type": "string", "description": "Intent id"},
                    "message": {"type": "string", "description": "Correction"},
                },
                "required": ["intent", "message"],
            },
        ]

    def _agent_main_prompt(self, task_id: str) -> str:
        """Invariant contract of the main agent."""
        return (
            "You are the LazyOwn main agent for an authorized penetration test. "
            "Use the tools to inspect tasks and run commands; prefer read-only "
            "reconnaissance first and explain risky actions before taking them. "
            f"Active task: {task_id or 'none'}. "
            "Answer concisely and in the operator's language."
        )

    @cmd2.with_category(ai_category)
    def do_lazy_agent(self, line):
        """Main agent with full tool calling (native backend or opencode). Usage: lazy_agent new [--title T]|list|show <sid>|say <prompt...> [--session S] [--continue] [--backend native|opencode] [--task T]"""
        args = shlex.split(line) if line.strip() else []
        if not args:
            print_error(
                "Usage: lazy_agent new|list|show <sid>|say <prompt...> [--session S] "
                "[--backend native|opencode] [--task T]"
            )
            return
        from modules.lazy_agent import ConversationStore

        store = ConversationStore("")
        action = args[0]
        if action == "new":
            session_id = uuid4().hex[:12]
            store.save_session(session_id, [], title=extract_flag(args, "--title") or "operator session")
            print_msg(f"[+] session {session_id}")
            return
        if action == "list":
            rows = store.sessions()
            print_msg(f"{len(rows)} session(s)")
            for row in rows:
                print_msg(f"  {row['session_id']} msgs={row['messages']} {row['title'][:70]}")
            return
        if action == "show" and len(args) > 1:
            entry = store.session(args[1])
            messages = entry.get("messages", []) or []
            print_msg(f"session {args[1]}: {len(messages)} message(s)")
            for message in messages[-6:]:
                body = message.get("content") or json.dumps(message.get("tool_calls", ""))
                print_msg(f"  {message.get('role')}: {str(body)[:140]}")
            return
        if action != "say":
            print_error("Usage: lazy_agent new|list|show <sid>|say <prompt...>")
            return
        backend = (
            extract_flag(args, "--backend") or str(self.params.get("agent_backend", "native") or "native")
        ).lower()
        task_id = extract_flag(args, "--task") or self._task_id(args)
        session_flag = extract_flag(args, "--session") or ""
        if not session_flag and "--continue" in args:
            sessions = store.sessions()
            session_flag = sessions[0]["session_id"] if sessions else ""
        session_id = session_flag or uuid4().hex[:12]
        skip_values = {"--backend", "--task", "--session"}
        prompt_parts: list[str] = []
        index = 1
        while index < len(args):
            token = args[index]
            if token in skip_values:
                index += 2
                continue
            if token in ("--continue",):
                index += 1
                continue
            prompt_parts.append(token)
            index += 1
        prompt = " ".join(prompt_parts).strip()
        if not prompt:
            print_error("Usage: lazy_agent say <prompt...> [--session S]")
            return
        if backend == "opencode":
            from modules.lazy_agent import run_external_opencode

            result = run_external_opencode(
                prompt, session_id=session_id, agent=str(self.params.get("opencode_agent", "") or "")
            )
            store.save_session(
                session_id,
                [
                    {"role": "user", "content": prompt},
                    {"role": "assistant", "content": str(result.get("reply", ""))[:6000]},
                ],
                title=prompt[:120],
            )
            if result.get("error"):
                print_warn(f"opencode: {result['error']}")
            print_msg(str(result.get("reply", ""))[:4000] or "(no reply)")
            print_msg(f"[*] session {session_id} (continue with --session {session_id})")
            return
        from modules.lazy_agent import resolve_agentic_model, run_main_session

        model = resolve_agentic_model()
        if model is None:
            print_error(
                "no tool-calling backend available: configure groq/openai/deepseek "
                "with an API key (lazy_llm) or use --backend opencode"
            )
            return
        result = run_main_session(
            model=model,
            session_id=session_id,
            system_prompt=self._agent_main_prompt(task_id),
            prompt=prompt,
            tools=self._agent_main_tools(task_id),
            on_event=lambda kind, name, text: print_msg(f"  [agent-{kind}] {name}: {text[:200]}"),
        )
        print_msg(str(result.get("reply", ""))[:4000] or "(no reply)")
        print_msg(f"[*] session {session_id} (continue with --session {session_id})")

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
        """Tool catalog: list [agent]|bind|unbind <agent> <tool>|custom-add <name> <command|script|http> <target> [--desc D] [--method M] [--body B] [--timeout S] [--trigger http,https]|custom-list|custom-rm <name>|custom-run <name> [arg]. Usage: lazy_tool ..."""
        args = shlex.split(line) if line.strip() else []
        if not args:
            print_error(
                "Usage: lazy_tool list [agent] | lazy_tool bind|unbind <agent> <tool> | "
                "lazy_tool custom-add|custom-list|custom-rm|custom-run ..."
            )
            return
        from modules.lazy_engine import ToolCatalog

        if args[0] in ("custom-add", "custom-list", "custom-rm", "custom-run"):
            from modules.custom_tools import add_tool, list_tools, remove_tool, run_tool

            if args[0] == "custom-list":
                for tool in list_tools():
                    print_msg(f"  {tool['name']} [{tool['kind']}] {tool['target'][:110]}")
                if not list_tools():
                    print_msg("[*] no custom tools registered.")
                return
            if args[0] == "custom-add" and len(args) >= 4:
                timeout = 60.0
                raw_timeout = extract_flag(args, "--timeout")
                if raw_timeout:
                    try:
                        timeout = float(raw_timeout)
                    except ValueError:
                        timeout = 60.0
                try:
                    entry = add_tool(
                        args[1],
                        args[2],
                        args[3],
                        description=extract_flag(args, "--desc") or "",
                        method=extract_flag(args, "--method") or "GET",
                        body=extract_flag(args, "--body") or "",
                        timeout=timeout,
                        trigger=extract_flag(args, "--trigger") or "",
                    )
                except ValueError as exc:
                    print_error(str(exc))
                    return
                print_msg(
                    f"[+] custom tool {entry['name']} [{entry['kind']}]: "
                    f"{entry['target'][:120]}"
                    + (f" trigger={','.join(entry['trigger'])}" if entry.get("trigger") else "")
                )
                return
            if args[0] == "custom-rm" and len(args) >= 2:
                print_msg("[+] removed." if remove_tool(args[1]) else "[-] unknown tool.")
                return
            if args[0] == "custom-run" and len(args) >= 2:
                arg = " ".join(a for a in args[2:] if not a.startswith("--"))
                output = run_tool(args[1], arg)
                print_msg(output[:4000] if output else "[*] no output.")
                return
            print_error(
                "Usage: lazy_tool custom-add <name> <kind> <target> | custom-list | "
                "custom-rm <name> | custom-run <name> [arg]"
            )
            return
        catalog = ToolCatalog()
        if args[0] == "list":
            for agent, tools in catalog.bindings(args[1] if len(args) > 1 else "").items():
                print_msg(f"  {agent}: {', '.join(tools)}")
        elif args[0] in ("bind", "unbind") and len(args) >= 3:
            tools = catalog.bind(args[1], args[2]) if args[0] == "bind" else catalog.unbind(args[1], args[2])
            print_msg(f"[+] {args[1]}: {', '.join(tools)}")
        else:
            print_error("Usage: lazy_tool list|bind|unbind|custom-* ...")

    @cmd2.with_category(ai_category)
    def do_lazy_verb(self, line):
        """Loop verb admin: list [--phase P] [--q Q]|enable|disable <verb>|add <verb> --keywords K [--phase P] [--no-target] [--desc D]|remove <verb>|full-cli [on|off]. Usage: lazy_verb ..."""
        args = shlex.split(line) if line.strip() else []
        if not args:
            print_error(
                "Usage: lazy_verb list [--phase P] [--q Q] | lazy_verb enable|disable <verb> | "
                "lazy_verb add <verb> --keywords K [--phase P] [--no-target] [--desc D] | "
                "lazy_verb remove <verb> | lazy_verb full-cli [on|off]"
            )
            return
        from modules.orchestrator_config import effective_verbs, remove_verb, upsert_verb

        if args[0] == "list":
            phase = extract_flag(args, "--phase") or ""
            query = (extract_flag(args, "--q") or "").lower()
            entries = effective_verbs()
            if phase:
                entries = [e for e in entries if phase.lower() in [p.lower() for p in e.get("phases", [])]]
            if query:
                entries = [
                    e for e in entries if query in e["name"].lower() or query in e.get("description", "").lower()
                ]
            print_msg(f"[*] {len(entries)} verb(s):")
            for entry in entries:
                state = "on" if entry["enabled"] else "off"
                print_msg(f"  {entry['name']} [{state}] ({entry['source']}) :: {entry.get('description', '')[:100]}")
            try:
                from modules.lazy_cli_bridge import cli_verbs, full_cli_enabled

                print_msg(
                    f"[*] full-cli routing: {'on' if full_cli_enabled() else 'off'} ({len(cli_verbs())} shell verbs visible)"
                )
            except Exception:
                pass
            return
        if args[0] in ("enable", "disable") and len(args) >= 2:
            try:
                entry = upsert_verb(args[1], enabled=args[0] == "enable")
            except ValueError as exc:
                print_error(str(exc))
                return
            print_msg(f"[+] {entry['name']}: {'on' if entry['enabled'] else 'off'}")
            return
        if args[0] == "add" and len(args) >= 2:
            import re as _re

            name = args[1].strip()
            if not _re.match(r"^[a-z][a-z0-9_]{0,63}$", name):
                print_error("Verb must match ^[a-z][a-z0-9_]{0,63}$ (same rule as addon names).")
                return
            try:
                from modules.lazy_cli_bridge import is_cli_verb
            except Exception:
                is_cli_verb = lambda _n: False  # noqa: E731
            if not is_cli_verb(name):
                print_error(f"Unknown shell verb '{name}'. Pick a real do_<verb> command or install an addon first.")
                return
            keywords = [w.strip() for w in (extract_flag(args, "--keywords") or "").split(",") if w.strip()]
            phases = [p.strip() for p in (extract_flag(args, "--phase") or "").split(",") if p.strip()]
            needs_target = "--no-target" not in args
            try:
                entry = upsert_verb(
                    name,
                    enabled=True,
                    keywords=keywords or None,
                    phases=phases or None,
                    needs_target=needs_target,
                    description=extract_flag(args, "--desc") or f"operator-defined verb {name}",
                    custom=True,
                )
            except ValueError as exc:
                print_error(str(exc))
                return
            print_msg(f"[+] custom verb {entry['name']}: on")
            return
        if args[0] == "remove" and len(args) >= 2:
            print_msg("[+] removed." if remove_verb(args[1]) else "[-] unknown verb (built-ins disable instead).")
            return
        if args[0] == "full-cli":
            try:
                from modules.lazy_cli_bridge import full_cli_enabled, set_full_cli
            except Exception as exc:
                print_error(f"Bridge unavailable: {exc}")
                return
            rest = [a for a in args[1:] if not a.startswith("--")]
            if not rest:
                print_msg(f"[*] full-cli routing: {'on' if full_cli_enabled() else 'off'}")
                return
            if rest[0].lower() in ("on", "true", "yes", "1"):
                print_msg(f"[+] full-cli routing: {'on' if set_full_cli(True) else 'off'}")
            elif rest[0].lower() in ("off", "false", "no", "0"):
                print_msg(f"[+] full-cli routing: {'on' if set_full_cli(False) else 'off'}")
            else:
                print_error("Usage: lazy_verb full-cli [on|off]")
            return
        print_error("Usage: lazy_verb list|enable|disable|add|remove|full-cli ...")

    @cmd2.with_category(ai_category)
    def do_lazy_stage(self, line):
        """Loop stage admin: list|enable|disable <stage>|reset. Usage: lazy_stage ..."""
        args = shlex.split(line) if line.strip() else []
        if not args:
            print_error("Usage: lazy_stage list | lazy_stage enable|disable <stage> | lazy_stage reset")
            return
        from modules.orchestrator_config import reset, set_stage, stages

        if args[0] == "list":
            for name, stage in stages().items():
                state = "on" if stage["enabled"] else "off"
                print_msg(f"  {name} [{state}] :: {stage['label'][:80]}")
            return
        if args[0] in ("enable", "disable") and len(args) >= 2:
            try:
                stage = set_stage(args[1], args[0] == "enable")
            except KeyError:
                print_error(f"Unknown stage '{args[1]}'. See lazy_stage list.")
                return
            print_msg(f"[+] {stage['name']}: {'on' if stage['enabled'] else 'off'}")
            return
        if args[0] == "reset":
            reset()
            print_msg("[+] orchestrator overrides cleared (back to defaults).")
            return
        print_error("Usage: lazy_stage list|enable|disable|reset ...")

    @cmd2.with_category(ai_category)
    def do_lazy_addon(self, line):
        """Addon trigger runner: list [service]|run <name> [--target T]|update [name|--all] [--dry-run]."""
        args = shlex.split(line) if line.strip() else []
        if not args:
            print_error(
                "Usage: lazy_addon list [service] | lazy_addon run <name> [--target T] | "
                "lazy_addon update [name|--all] [--dry-run]"
            )
            return
        if args[0] == "update":
            from modules.addon_updater import update_all

            names = [token for token in args[1:] if not token.startswith("--") and token != "--all"]
            summary = update_all(names=names or None, dry_run="--dry-run" in args)
            counts = summary.get("counts", {})
            print_msg(
                f"[*] addons: {summary.get('total', 0)} checked "
                f"(updated={counts.get('updated', 0)} skipped={counts.get('skipped', 0)} "
                f"failed={counts.get('failed', 0)} dry-run={counts.get('dry-run', 0)})"
            )
            for row in summary.get("results", []):
                status = row.get("status", "")
                line = f"  [{status}] {row.get('name')}: {row.get('reason', '')}"
                if status in ("failed",):
                    print_error(line)
                elif status in ("updated", "dry-run"):
                    print_msg(line)
                else:
                    print_warn(line)
            return
        from modules.auto_registry import addon_hits_for, iter_addon_triggers

        if args[0] == "list":
            service = " ".join(a for a in args[1:] if not a.startswith("--"))
            if service:
                hits = addon_hits_for(service)
                print_msg(f"[*] {len(hits)} trigger match(es) for '{service[:80]}':")
                for name, source in hits:
                    print_msg(f"  {name} [{source}]")
            else:
                entries = iter_addon_triggers()
                print_msg(f"[*] {len(entries)} trigger-bearing addon(s):")
                for name, triggers in entries[:40]:
                    print_msg(f"  {name}: {', '.join(triggers[:6])}")
            return
        if args[0] == "run" and len(args) >= 2:
            from pathlib import Path as _Path

            import yaml as _yaml

            from core.process import run_command as _run_command

            name = "".join(c for c in args[1] if c.isalnum() or c in ("-", "_"))[:64]
            path = _Path("lazyaddons") / f"{name}.yaml"
            if not path.is_file():
                print_error(f"Unknown addon '{args[1]}'. List with: lazy_addon list")
                return
            try:
                data = _yaml.safe_load(path.read_text(encoding="utf-8")) or {}
            except Exception as exc:
                print_error(f"Cannot parse {path}: {exc}")
                return
            tool = data.get("tool", {}) or {}
            template = str(tool.get("execute_command", "") or "").strip()
            if not template:
                print_error(f"Addon '{name}' has no execute_command.")
                return
            shell = self._resolve_shell()
            params = dict(getattr(shell, "params", {}) or {}) if shell is not None else {}
            flag_target = extract_flag(args, "--target")
            target = flag_target or params.get("rhost", "")
            if not flag_target:
                skip_values = {value for flag in ("--task",) for value in [extract_flag(args, flag)] if value}
                positional = [a for a in args[2:] if not a.startswith("--") and a not in skip_values]
                if positional:
                    target = positional[0]
            subs = dict(params)
            subs.setdefault("target", target)
            subs.setdefault("rhost", target)
            command = template
            for key in (
                "target",
                "rhost",
                "lhost",
                "lport",
                "rport",
                "domain",
                "usrwordlist",
                "dnswordlist",
                "dirworlist",
            ):
                command = command.replace("{" + key + "}", str(subs.get(key, "")))
            if ("{target}" in template or "{rhost}" in template) and not (target or "").strip():
                print_error(f"Addon '{name}' needs a target: pass --target or assign rhost.")
                return
            print_msg(f"[*] lazy_addon run {name}: {command[:200]}")
            try:
                output = _run_command(command) or ""
            except Exception as exc:
                print_error(f"Addon '{name}' failed: {exc}")
                return
            print_msg(str(output)[:3000] or "[*] addon finished with no output.")
            return
        print_error("Usage: lazy_addon list [service] | lazy_addon run <name> [--target T]")

    @cmd2.with_category(ai_category)
    def do_lazy_notify(self, line):
        """Notify channels: list|add <log|webhook|file|slack|email> <target> [--min S] [--to a] [--from f] [--user u] [--pass p] [--no-tls]|remove <n>|test [severity]. Usage: lazy_notify ... [--task T]"""
        args = shlex.split(line) if line.strip() else []
        if not args:
            print_error("Usage: lazy_notify list|add|remove|test ...")
            return
        from modules.lazy_engine import Notifier

        notifier = Notifier(_engine().store)
        if args[0] == "list":
            for index, channel in enumerate(notifier.channels(), start=1):
                print_msg(
                    f"  {index}. [{channel['kind']}] {channel['target']} "
                    f"min={channel.get('min_severity', '')}"
                    f"{(' to=' + str(channel.get('to'))) if channel.get('to') else ''}"
                )
            if not notifier.channels():
                print_msg("[*] no channels (log only).")
        elif args[0] == "add" and len(args) >= 3:
            extra = {
                "to": extract_flag(args, "--to") or "",
                "from_addr": extract_flag(args, "--from") or "",
                "user": extract_flag(args, "--user") or "",
                "password": extract_flag(args, "--pass") or "",
                "tls": "--no-tls" not in args,
            }
            try:
                item = notifier.add_channel(args[1], args[2], extract_flag(args, "--min") or "", extra=extra)
            except ValueError as exc:
                print_error(str(exc))
                return
            print_msg(f"[+] channel [{item['kind']}]: {item['target']}")
        elif args[0] == "remove" and len(args) >= 2:
            try:
                ok = notifier.remove_channel(int(args[1]))
            except ValueError:
                ok = False
            print_msg("[+] removed." if ok else "[-] unknown channel index.")
        elif args[0] == "test":
            task_id = self._task_id(args) or "manual"
            count = notifier.emit(
                task_id, "finding_status_changed", {"severity": (args[1] if len(args) > 1 else "high"), "test": True}
            )
            print_msg(f"[+] fanned out to {count} channels (+ log).")
        else:
            print_error("Usage: lazy_notify list|add|remove|test ...")

    @cmd2.with_category(ai_category)
    def do_lazy_trigger(self, line):
        """Scheduler triggers: list|add <kind> [every_sec]|remove <id>|on <id>|off <id>|seed|policy|addons|sync. Usage: lazy_trigger ... [--task T]"""
        args = shlex.split(line) if line.strip() else []
        task_id = self._task_id(args)
        if not args:
            print_error("Usage: lazy_trigger list|add|remove|on|off|seed|policy|addons|sync ... [--task T]")
            return
        from modules.lazy_engine import TriggerStore

        table = TriggerStore(task_id or "")
        if args[0] == "list":
            for item in table.list():
                print_msg(
                    f"  [{item['id']}] {item['kind']} every={item.get('every_sec', 0)} enabled={item.get('enabled')}"
                )
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
        elif args[0] in ("on", "off") and len(args) >= 2:
            try:
                wanted = int(args[1])
            except ValueError:
                print_error("[-] trigger id must be an integer.")
                return
            if table.set_enabled(wanted, args[0] == "on"):
                print_msg(f"[+] trigger {wanted} is now {args[0]}.")
            else:
                print_error("[-] unknown trigger.")
        elif args[0] == "seed":
            from modules import trigger_policy

            result = trigger_policy.seed_store(store=table)
            print_msg(f"[+] YAML seeds merged into{' task ' + task_id if task_id else ' global'} store: "
                      f"+{result['added']} (total {result['total']}).")
        elif args[0] == "policy":
            from modules import trigger_policy

            policy = trigger_policy.read_policy()
            seeds = policy.get("seeds") or []
            if not seeds:
                print_msg("[*] no declarative triggers in config/orchestrator.yaml.")
                return
            print_msg("[*] declarative triggers (config/orchestrator.yaml):")
            for item in seeds:
                state = "on" if item["enabled"] else "off"
                print_msg(f"  {item['kind']} every={item['every_sec']} arg={item['arg'] or '-'} [{state}]")
        elif args[0] in ("addons", "sync"):
            from modules.auto_registry import addon_hits_for

            tid = self._require_task(args)
            if not tid:
                return
            try:
                services = [n.value for n in _engine().assets.list("service")]
            except Exception:
                services = []
            shown = 0
            for service in services[:10]:
                hits = addon_hits_for(service)
                if not hits:
                    continue
                if args[0] == "sync":
                    for name, _source in hits:
                        try:
                            _engine().add_hint(tid, f"service trigger {service}: run lazy addon {name}")
                            shown += 1
                        except Exception:
                            continue
                else:
                    print_msg(f"  {service[:60]}: {', '.join(n for n, _s in hits)}")
                    shown += len(hits)
            if args[0] == "sync":
                print_msg(f"[+] {shown} service trigger(s) queued as planner hints for {tid}.")
            elif not shown:
                print_msg("[*] no addon/tool trigger matches current services.")
        else:
            print_error("Usage: lazy_trigger list|add|remove|addons|sync ... [--task T]")

    @cmd2.with_category(ai_category)
    def do_lazy_llm(self, line):
        """LLM chain: list|add <name> [model] [--priority N]|priority <name> <N>|remove <name>|usage|health|context [N]|record [on|off]|raw [--limit N]|conformance [--role R]|bind <member...> --task T|chain --task T|failover --task T. Usage: lazy_llm ..."""
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
        elif args[0] == "priority" and len(args) >= 3:
            try:
                rank = int(args[2])
            except ValueError:
                print_error("Usage: lazy_llm priority <name> <N>")
                return
            if pool.set_priority(args[1], rank):
                print_msg(f"[+] {args[1]} priority -> {rank} (failover order updated).")
            else:
                print_error(f"[-] unknown member '{args[1]}'.")
        elif args[0] == "usage":
            for call in pool.usage().get("calls", [])[-20:]:
                print_msg(
                    f"  [{call.get('member')}/{'ok' if call.get('ok') else 'fail'}] {str(call.get('text', ''))[:100]}"
                )
        elif args[0] == "health":
            for name, ok in pool.health().items():
                print_msg(f"  {name}: {'healthy' if ok else 'cooldown'}")
            if not pool.members():
                print_msg("[*] no members — planner/worker stay heuristic (never an error).")
        elif args[0] == "context":
            rest = [a for a in args[1:] if not a.startswith("--")]
            if not rest:
                print_msg(f"[*] context budget = {pool.context_budget()} chars")
                return
            try:
                budget = pool.set_context_budget(int(rest[0]))
            except ValueError:
                print_error("context budget must be an integer")
                return
            print_msg(f"[+] context budget = {budget} chars")
        elif args[0] == "record":
            rest = [a for a in args[1:] if not a.startswith("--")]
            if not rest:
                print_msg(f"[*] raw recording {'on' if pool.record_raw() else 'off'}")
                return
            if rest[0] in ("on", "off"):
                state = pool.set_record_raw(rest[0] == "on")
                print_msg(f"[+] raw recording {'on' if state else 'off'}")
                return
            print_error("Usage: lazy_llm record [on|off]")
        elif args[0] == "raw":
            limit = 10
            raw_limit = extract_flag(args, "--limit")
            if raw_limit:
                try:
                    limit = max(1, min(200, int(raw_limit)))
                except ValueError:
                    limit = 10
            entries = pool.raw_entries(limit)
            for entry in entries:
                print_msg(
                    f"  [{entry.get('member')}/{'ok' if entry.get('ok') else 'fail'}] "
                    f"{str(entry.get('prompt', ''))[:100]}"
                )
            if not entries:
                print_msg("[*] no raw exchanges (enable with: lazy_llm record on)")
        elif args[0] == "conformance":
            from modules.lazy_roles import conformance as _conformance

            summary = _conformance(extract_flag(args, "--role") or "")
            if not summary.get("members"):
                print_msg("[*] no members — planner/worker stay heuristic (never an error).")
                return
            for member, lanes in (summary.get("results") or {}).items():
                marks = " ".join(f"{r}={'ok' if v['ok'] else 'fail'}/{v['ms']}ms" for r, v in lanes.items())
                print_msg(f"  {member}: {marks}")
            for role_name, member in (summary.get("affinity") or {}).items():
                print_msg(f"  affinity {role_name} -> {member or 'none'}")
        elif args[0] in ("bind", "chain", "failover"):
            task_id = self._require_task(args)
            if not task_id:
                print_error("Usage: lazy_llm bind <member...> --task T | chain --task T | failover --task T")
                return
            engine = _engine()
            if args[0] == "bind":
                rest = [a for a in args[1:] if not a.startswith("--")]
                if not rest:
                    print_error("Usage: lazy_llm bind <name[:model]> [...] --task T")
                    return
                members = []
                for spec in rest:
                    name, _, model = spec.partition(":")
                    members.append({"name": name[:120], "model": (model or name)[:120], "priority": 0})
                state = engine.store.set_llm_chain(task_id, members)
                print_msg(f"[+] {task_id} chain bound ({len(state['members'])} members, active={state['active']}).")
                return
            if args[0] == "chain":
                state = engine.store.llm_state(task_id)
                if not state.get("members"):
                    print_msg("[*] no per-task chain (global pool applies).")
                    return
                for index, member in enumerate(state["members"]):
                    marker = "*" if index == int(state.get("active", 0)) else " "
                    print_msg(f" {marker} {index + 1}. {member.get('name')} :: {member.get('model', '')}")
                return
            state = engine.store.advance_llm(task_id)
            if not state:
                print_msg("[*] no per-task chain to fail over.")
            else:
                print_msg(
                    f"[+] active member -> {int(state['active']) + 1}/"
                    f"{len(state['members'])} ({state['members'][int(state['active'])].get('name')})"
                )
            return
        else:
            print_error(
                "Usage: lazy_llm list|add|remove|priority <name> <N>|usage|health|context [N]|conformance [--role R]|"
                "bind <member...> --task T|chain --task T|failover --task T"
            )

    @cmd2.with_category(ai_category)
    def do_lazy_compact(self, line):
        """Compaction: minor|major [--threshold N]|unfolded [--limit N]|overview|noa|expand <digest>. Usage: lazy_compact ... [--task T]"""
        args = shlex.split(line) if line.strip() else []
        task_id = self._require_task(args)
        if not task_id or not args:
            print_error("Usage: lazy_compact minor|major|unfolded|overview|noa|expand ... [--task T]")
            return
        from modules.lazy_engine import ActivityLog, ColdCompactor, ExplorationGraph

        graph = ExplorationGraph(task_id)
        compactor = ColdCompactor(graph, ActivityLog(task_id))
        if args[0] == "noa":
            archives = compactor.noa_archives()
            print_msg(f"{len(archives)} NOA archive(s) for {task_id}")
            for row in archives:
                print_msg(f"  {row['name']} members={row['members']} sig={row['signature']}")
            if not archives:
                print_msg("[*] enable raw archiving with noa_compaction in payload.json")
            return
        if args[0] in ("minor", "major"):
            threshold = 50
            raw = extract_flag(args, "--threshold")
            if raw:
                try:
                    threshold = max(1, int(raw))
                except ValueError:
                    pass
            result = compactor.compact(threshold=threshold, mode=args[0])
            print_msg(
                f"[+] {result['mode']}: folded {result['compacted']} facts into {len(result.get('digests', []))} digests."
            )
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
            cold = [n for n in graph.list("fact") if n.meta.get("cold") or n.state == "exhausted"]
            print_msg(
                f"[*] {len(view['digests'])} digests covering {view['covered']} cold facts "
                f"({len(cold)} cold total); expandable: {view['expandable'] or 'none'}."
            )
            for digest in view["digests"][-10:]:
                members = digest["members"]
                print_msg(f"  digest #{digest['id']} [{digest['mode']}]: {len(members)} members {members[:8]}")
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
            print_msg(
                f"[*] {unfolded['total']} cold facts (showing {len(unfolded['facts'])}"
                f"{', truncated' if unfolded['truncated'] else ''})."
            )
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
        print_msg(
            f"    nodes={status['overview'].get('nodes', 0)} "
            f"facts={status['overview'].get('facts', 0)} "
            f"findings={status['overview'].get('findings', 0)}"
        )
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
            print_msg(
                f"[+] task {summary['task_id']} from template {row['name']} "
                f"({summary['goals']} goals). Run: lazy_loop --task {summary['task_id']}"
            )
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
        """Task conversation: say <text>|log|clear|sessions. Usage: lazy_chat ... [--task T] [--session S]"""
        args = shlex.split(line) if line.strip() else []
        task_id = self._require_task(args)
        if not task_id or not args:
            print_error("Usage: lazy_chat say <text>|log|clear|sessions [--task T] [--session S]")
            return
        from modules.lazy_engine import LlmPool, TaskChat

        chat = TaskChat()
        session = extract_flag(args, "--session") or ""
        if args[0] == "log":
            for turn in chat.log(task_id, session=session):
                print_msg(f"  [{turn.get('session', 'main')}/{turn.get('role')}] {str(turn.get('text', ''))[:200]}")
            return
        if args[0] == "sessions":
            for name in chat.sessions(task_id):
                print_msg(f"  {name}")
            return
        if args[0] == "clear":
            print_msg("[+] cleared." if chat.clear(task_id, session=session) else "[-] nothing to clear.")
            return
        if args[0] == "say" and len(args) >= 2:
            try:
                turn = chat.say(task_id, self._free_text(args[1:]), LlmPool(), session=session or "main")
            except ValueError as exc:
                print_error(str(exc))
                return
            print_msg(f"[*] {turn['answer'][:1500]}")
            return
        print_error("Usage: lazy_chat say <text>|log|clear|sessions [--task T] [--session S]")

    @cmd2.with_category(ai_category)
    def do_lazy_scheduler(self, line):
        """Scheduler state: show|run. Usage: lazy_scheduler ... [--task T]"""
        args = shlex.split(line) if line.strip() else []
        task_id = self._task_id(args)
        from modules.lazy_engine import ActivityLog, ExplorationGraph, TriggerStore

        table = TriggerStore(task_id or "")
        if not args or args[0] == "show":
            for item in table.list():
                print_msg(
                    f"  [{item['id']}] {item['kind']} every={item.get('every_sec', 0)} "
                    f"enabled={item.get('enabled')} watermark={item.get('watermark', 0)}"
                )
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
        """Run the single orchestrator: auto-invokes scope/asset/enrich/planner/frontier/worker/guard/traffic/finding/retest/compact/trace. Usage: lazy_loop [--task T] [--rounds N] [--workers N] [--timeout S] [--budget rounds=N,toolcalls=N,findings=N,timeout_sec=N] [--budget-confirm] [--sandbox [image]] [--view|--plain] [<goal>]"""
        from modules.lazy_runner import parse_loop_line, run_loop

        try:
            config = parse_loop_line(line)
        except ValueError as exc:
            if str(exc) != "usage":
                print_error(f"lazy_loop: {exc}")
            else:
                print_error(
                    "Usage: lazy_loop [--task T] [--rounds N] [--workers N] [--timeout S] "
                    "[--budget rounds=N,toolcalls=N,findings=N,timeout_sec=N] [--budget-confirm] "
                    "[--view] [<goal>]"
                )
            return
        if not config.target:
            config.target = str(self.params.get("rhost", "") or "")
        if not config.goal and not config.task_id and not config.target:
            print_error("Usage: lazy_loop [--task T] <goal>")
            return
        run_loop(self._resolve_shell(), dict(self.params or {}), config)

    @cmd2.with_category(ai_category)
    def do_lazy_sandbox(self, line):
        """Per-task Docker sandbox: status [--task T]|up --task T [--image I]|down --task T|build|exec --task T <verb...>. Usage: lazy_sandbox ..."""
        args = shlex.split(line) if line.strip() else []
        from modules.lazy_sandbox import (
            container_name,
            ensure_container,
            exec_command,
            image_name,
            remove_container,
            status,
        )

        if not args or args[0] == "status":
            info = status(extract_flag(args, "--task") or "")
            print_msg(f"[*] docker={info['docker']} image={info['image']} available={info['image_available']}")
            if "running" in info and isinstance(info["running"], bool):
                print_msg(f"[*] container {info.get('container', '')}: {'up' if info['running'] else 'down'}")
            elif info.get("running"):
                for name in info["running"]:
                    print_msg(f"  {name}")
            else:
                print_msg("[*] no loop containers running.")
            return
        if args[0] == "up":
            task_id = extract_flag(args, "--task") or self._task_id(args)
            if not task_id:
                print_error("Usage: lazy_sandbox up --task T [--image I]")
                return
            name = ensure_container(task_id, extract_flag(args, "--image") or "")
            print_msg(f"[+] container {name}" if not name.startswith("execution failed:") else name)
            return
        if args[0] == "down":
            task_id = extract_flag(args, "--task") or self._task_id(args)
            if not task_id:
                print_error("Usage: lazy_sandbox down --task T")
                return
            print_msg(f"[+] removed {container_name(task_id)}." if remove_container(task_id) else "[-] remove failed.")
            return
        if args[0] == "build":
            import subprocess as _sp

            print_msg(f"[*] building {image_name()} from Dockerfile.sandbox (takes minutes)...")
            proc = _sp.run(
                ["docker", "build", "-f", "Dockerfile.sandbox", "-t", image_name(), "."],
                capture_output=True,
                text=True,
                timeout=1800,
            )
            print_msg(
                "[+] image ready." if proc.returncode == 0 else f"[-] build failed:\n{(proc.stderr or '')[-2000:]}"
            )
            return
        if args[0] == "exec":
            task_id = extract_flag(args, "--task") or self._task_id(args)
            rest = " ".join(a for a in args[1:] if not a.startswith("--") and a != task_id)
            if not task_id or not rest:
                print_error("Usage: lazy_sandbox exec --task T <verb...>")
                return
            print_msg(exec_command(task_id, rest)[:4000] or "[*] no output.")
            return
        print_error("Usage: lazy_sandbox status|up|down|build|exec ...")

    @cmd2.with_category(ai_category)
    def do_lazy_install(self, line):
        """Capability installer: <tool> [--dry-run]|on|off|list. Usage: lazy_install ..."""
        args = shlex.split(line) if line.strip() else []
        if not args:
            print_error("Usage: lazy_install <tool> [--dry-run] | lazy_install on|off|list")
            return
        from modules.lazy_installer import (
            TOOL_INSTALL,
            install_command_for,
            installer_enabled,
            set_installer_enabled,
        )

        if args[0] in ("on", "off"):
            state = set_installer_enabled(args[0] == "on")
            print_msg(f"[+] loop installer: {'on' if state else 'off'}")
            if state:
                print_msg('[*] recommended gate: lazy_guard rule-add "apt-get install" ask installs-write-to-host')
            return
        if args[0] == "list":
            print_msg(f"[*] loop installer: {'on' if installer_enabled() else 'off'} ({len(TOOL_INSTALL)} recipes)")
            for tool, recipe in sorted(TOOL_INSTALL.items()):
                print_msg(f"  {tool}: {recipe[:100]}")
            return
        recipe = install_command_for(args[1] if args[0] == "run" and len(args) > 1 else args[0])
        if recipe is None:
            print_error(f"Unknown tool '{args[0]}'. See lazy_install list (allowlist only, never free-form).")
            return
        if "--dry-run" in args:
            print_msg(f"[*] would run: {recipe}")
            return
        print_msg(f"[*] running: {recipe}")
        import subprocess as _sp

        proc = _sp.run(shlex.split(recipe), capture_output=True, text=True, timeout=600)
        print_msg(((proc.stdout or "") + (proc.stderr or ""))[-3000:] or "[*] no output.")


__all__ = ["LazyCommandSet"]
