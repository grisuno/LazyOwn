"""LazyPassGen shell command: target-aware weak password generation."""

from __future__ import annotations

import cmd2

from cli.commands._base import LazyOwnCommandSet
from utils import CYAN, RESET, miscellaneous_category, print_error, print_msg, print_succ

SESSIONS_DIR = "sessions"
WORDLIST_TEMPLATE = "{sessions_dir}/wordlist_{slug}.txt"


class LazyPassGenCommandSet(LazyOwnCommandSet):
    """Expose LazyPassGen to the operator."""

    phase = "credential_access"
    category = miscellaneous_category

    @cmd2.with_category(miscellaneous_category)
    def do_lazypassgen(self, line):
        """Generate a target-aware candidate wordlist.

        Usage:
            lazypassgen <entity> [--export <file>]

        Without --export the list lands in ``sessions/wordlist_<entity>.txt``
        seeded with the most frequent default credentials. Peak combos:
        feed the result to spray or brute force inside the kill chain, the
        generation stops as pure data.
        """
        from modules import lazypassgen

        args = line.strip().split() if line.strip() else []
        if not args:
            print_msg("Usage: lazypassgen <entity> [--export <file>]")
            return
        entity = args[0]
        export_path = ""
        if "--export" in args:
            index = args.index("--export")
            if index + 1 < len(args) and not args[index + 1].startswith("--"):
                export_path = args[index + 1]
        slug = entity.replace("/", "-")
        destination = export_path or WORDLIST_TEMPLATE.format(sessions_dir=SESSIONS_DIR, slug=slug)
        result = lazypassgen.export(entity, destination)
        if result.get("error"):
            print_error(f"generation failed: {result['error']}")
            return
        summary = lazypassgen.generate(entity)
        seeds = summary.get("frequead_seeds", ())
        print_succ(f"Wrote {result['written']} candidates to {destination}")
        if seeds:
            print_msg(f"  Frequent seed pairs from lazycreds: {CYAN}{len(seeds)}{RESET}")
