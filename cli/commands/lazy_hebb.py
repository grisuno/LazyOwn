"""LazyHebb shell commands: zero-inference synaptic memory for agents."""

from __future__ import annotations

import shlex

import cmd2

from cli.commands._base import LazyOwnCommandSet, extract_flag
from utils import CYAN, GREEN, RESET, miscellaneous_category, print_error, print_msg, print_succ, print_warn


class LazyHebbCommandSet(LazyOwnCommandSet):
    """Expose the LazyHebb memory store to the operator."""

    category = miscellaneous_category

    @cmd2.with_category(miscellaneous_category)
    def do_lazyhebb(self, line):
        """Zero-inference synaptic memory (SQLite FTS5 + hebbian edges).

        Usage:
            lazyhebb add <text> [--sem tags] [--private] [--phase p]   store a memory
            lazyhebb spark <query> [--k N] [--all]                     recall winners
            lazyhebb bridge <topic-a> <topic-b>                        co-activation path
            lazyhebb stats                                             row/edge counters
            lazyhebb export [file]                                     write Markdown with | sem: lines
            lazyhebb import <file>                                     load Markdown bullets
            lazyhebb forget [--hours N] [--topic T] [--all]            prune memories

        Write-time semantic seeding: append ``| sem: a, b, c`` to the text
        (or let auto-seeding map keywords like psexec, nmap, kerberoast).
        Private memories are firewalled from fleet recall and from bridge
        pathfinding. Zero embeddings, zero LLM calls.
        """
        from modules import lazy_hebb

        args = shlex.split(line.strip()) if line.strip() else []
        if not args:
            print_msg("Usage: lazyhebb add|spark|bridge|stats|export|import|forget")
            return
        action = args[0]
        store = lazy_hebb.shared_hebb()
        if action == "add":
            positional: list[str] = []
            for token in args[1:]:
                if token.startswith("--"):
                    break
                positional.append(token)
            text = " ".join(positional).strip()
            if not text:
                print_error("add expects text: lazyhebb add 'credential admin on 10.0.0.5' --sem creds,win")
                return
            sem = extract_flag(args, "--sem") or ""
            phase = extract_flag(args, "--phase") or ""
            private = "--private" in args
            uid = store.store(text, agent_id="operator", phase=phase, sem_tags=sem, private=private)
            if not uid:
                print_error("store failed (db unwritable?)")
                return
            print_succ(f"memory {GREEN}{uid}{RESET} stored")
            tags = lazy_hebb.parse_sem_tags(text)[1] or sem
            seeded = lazy_hebb.auto_seed_tags(lazy_hebb.parse_sem_tags(text)[0])
            if seeded and seeded != tags:
                print_msg(f"  auto-seed: {CYAN}{seeded}{RESET}")
            if private:
                print_warn("row is private: excluded from fleet recall and bridge pathfinding")
            return
        if action == "spark":
            positional = [a for a in args[1:] if not a.startswith("--")]
            query = " ".join(positional).strip()
            if not query:
                print_error("spark expects a query: lazyhebb spark lateral movement psexec")
                return
            top_k = 5
            try:
                top_k = max(1, min(20, int(extract_flag(args, "--k") or 5)))
            except ValueError:
                pass
            winners = store.spark(query, top_k=top_k, include_private="--all" in args)
            if not winners:
                print_msg("no memories match (spark is deterministic: seed with lazyhebb add)")
                return
            for winner in winners:
                marks = f" sem: {winner.get('sem_tags')}" if winner.get("sem_tags") else ""
                hops = f" (+{winner.get('hops', 0)} hop)" if winner.get("hops") else ""
                print_msg(
                    f"  [{winner.get('phase') or 'none'}|{winner.get('agent_id', '?')}]"
                    f" {winner.get('content', '')}{marks} ({winner.get('score', 0.0):.3f}){hops}"
                )
            return
        if action == "bridge":
            positional = [a for a in args[1:] if not a.startswith("--")]
            if len(positional) < 2:
                print_error("bridge expects two topics: lazyhebb bridge 'stripe webhook' 'cloudflare waf'")
                return
            path = store.bridge(positional[0], positional[1])
            if not path:
                print_msg("no co-activation path (memories must fire together first)")
                return
            print_succ(" -> ".join(path))
            return
        if action == "stats":
            stats = store.stats()
            print_msg(f"db: {stats.get('db')}")
            print_msg(f"memories: {stats.get('memories', 0)} (private: {stats.get('private', 0)})")
            print_msg(f"edges: {stats.get('edges', 0)}")
            return
        if action == "export":
            positional = [a for a in args[1:] if not a.startswith("--")]
            path = positional[0] if positional else "sessions/lazy/hebb_export.md"
            count = store.export_markdown(path)
            if not count:
                print_error("export produced no rows")
                return
            print_succ(f"{count} memories -> {CYAN}{path}{RESET}")
            return
        if action == "import":
            positional = [a for a in args[1:] if not a.startswith("--")]
            if not positional:
                print_error("import expects a file path")
                return
            count = store.import_markdown(positional[0])
            print_succ(f"{count} memories imported")
            return
        if action == "forget":
            hours = 0.0
            try:
                hours = float(extract_flag(args, "--hours") or 0.0)
            except ValueError:
                print_error("--hours expects a number")
                return
            topic = extract_flag(args, "--topic") or ""
            if hours <= 0 and not topic:
                print_error("forget expects --hours N and/or --topic T (nothing deleted)")
                return
            count = store.forget(older_than_hours=hours, topic=topic, include_private="--all" in args)
            print_succ(f"{count} memories pruned")
            return
        print_error(f"unknown action: {action}")
