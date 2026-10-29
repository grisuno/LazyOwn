"""LazyDorks shell command: render target dork playbooks into session artefacts."""

from __future__ import annotations

import re
import shlex

import cmd2

from cli.commands._base import LazyOwnCommandSet
from utils import CYAN, RESET, miscellaneous_category, print_error, print_msg, print_succ

SESSIONS_DIR = "sessions"
DORK_REPORT_TEMPLATE = "{sessions_dir}/lazydorks_{slug}.md"
_SLUG_PATTERN = re.compile(r"[^a-z0-9._-]+")


def _slug(domain: str) -> str:
    """Return a filesystem-safe slug for a domain.

    Args:
        domain: Raw domain input.

    Returns:
        Lowercase slug with metacharacters collapsed to dashes.
    """
    return _SLUG_PATTERN.sub("-", str(domain or "target").strip().lower()).strip("-") or "target"


class LazyDorksCommandSet(LazyOwnCommandSet):
    """Expose the LazyDorks generator to the operator."""

    phase = "recon"
    category = miscellaneous_category

    @cmd2.with_category(miscellaneous_category)
    def do_lazydork(self, line):
        """Search the dork grammar for one target.

        Usage:
            lazydork <domain> [--org <github-org>] [--cat <category>]
            lazydork <domain> --export <file>

        Without --export the full report is rendered and persisted to
        ``sessions/lazydorks_<domain>.md``. Little data is fetched here:
        the list stays pure text to drive your own engine, review before
        running anything noisy.
        """
        from modules import lazydorks

        args = shlex.split(line.strip()) if line.strip() else []
        if not args:
            print_msg("Usage: lazydork <domain> [--org <github-org>] [--cat <category>] [--export <file>]")
            return
        domain = args[0]
        org = ""
        category = ""
        export_path = ""
        index = 1
        while index < len(args):
            token = args[index]
            if token == "--org" and index + 1 < len(args) and not args[index + 1].startswith("--"):
                org = args[index + 1]
                index += 2
                continue
            if token == "--cat" and index + 1 < len(args) and not args[index + 1].startswith("--"):
                category = args[index + 1]
                index += 2
                continue
            if token == "--export":
                if index + 1 < len(args) and not args[index + 1].startswith("--"):
                    export_path = args[index + 1]
                    index += 2
                else:
                    index += 1
                continue
            print_msg(f"Unknown option: {token}")
            return

        if category:
            rendered = lazydorks.queries(category, domain, org)
            if not rendered:
                print_error(
                    f"No dorks for category {category!r}. Valid categories: {', '.join(lazydorks.categories())}"
                )
                return
            print_msg(f"{len(rendered)} {category} dork(s) for {CYAN}{domain}{RESET}:")
            for item in rendered:
                print(f"  {item}")
            return

        destination = export_path or DORK_REPORT_TEMPLATE.format(sessions_dir=SESSIONS_DIR, slug=_slug(domain))
        result = lazydorks.write_report(destination, domain, org)
        if result.get("error"):
            print_error(f"export failed: {result['error']}")
            return
        print_succ(f"Wrote {result['written']} dorks to {result['path']}")
        for name, items in lazydorks.all_queries(domain, org).items():
            print_msg(f"  {CYAN}{name}{RESET}: {len(items)}")
