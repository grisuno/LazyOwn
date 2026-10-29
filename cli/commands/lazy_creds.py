"""LazyCreds shell commands: default-credential knowledge base lookups."""

from __future__ import annotations

import shlex

import cmd2

from cli.commands._base import LazyOwnCommandSet
from utils import (
    CYAN,
    GREEN,
    RESET,
    miscellaneous_category,
    print_error,
    print_msg,
    print_succ,
)


class LazyCredsCommandSet(LazyOwnCommandSet):
    """Expose the default-credential knowledge base to the operator."""

    phase = "credential_access"
    category = miscellaneous_category

    @cmd2.with_category(miscellaneous_category)
    def do_lazycreds(self, line):
        """Search the default-credential knowledge base.

        Usage:
            lazycreds <query>          search vendor/username substring
            lazycreds --top <n>        most repeated user:pass pairs
            lazycreds --export <file>  write user:pass pairs for sprayers
        """
        from modules import lazy_creds

        args = shlex.split(line.strip()) if line.strip() else []
        if not args:
            print_msg(f"Knowledge base rows: {lazy_creds.count()}")
            print_msg("Usage: lazycreds <query> | --top <n> | --export <file>")
            return
        if args[0] == "--top":
            try:
                limit = max(1, min(40, int(args[1]))) if len(args) > 1 else 10
            except ValueError:
                print_error("--top expects a number")
                return
            print_msg(f"Top {limit} credential pairs:")
            for row in lazy_creds.candidates(limit):
                print(f"  {GREEN}{row.username}{RESET}:{CYAN}{row.password}{RESET}")
            return
        if args[0] == "--export":
            if len(args) < 2:
                print_error("--export expects a file path")
                return
            result = lazy_creds.export_pairs(args[1])
            if result.get("error"):
                print_error(f"export failed: {result['error']}")
                return
            print_succ(f"Wrote {result['written']} pairs to {args[1]}")
            return
        query = " ".join(args)
        rows = lazy_creds.search(query)
        if not rows:
            print_msg(f"No default credentials match {query!r}")
            return
        print_msg(f"{len(rows)} match(es) for {query!r}:")
        for text in lazy_creds.as_lines(rows):
            print(f"  {text}")
