"""End-to-end demo command — MCP registration plus the golden path.

Runs the documented first-shift flow in one shot so a new operator (or a
recorded demo) sees every surface working together:

    mcp add  ->  session init (sitrep)  ->  recommend_next  ->  lazynmap

The MCP step only prints the registration command — the operator runs it
in their AI client (Claude Code / Hermes). The remaining three steps
execute inside this shell via ``onecmd`` delegation, so ``demo`` behaves
exactly like typing each command by hand (and composes with ``&&``).
"""

from __future__ import annotations

import cmd2

from cli.commands._base import LazyOwnCommandSet
from utils import miscellaneous_category, print_error, print_msg, print_warn


class DemoCommandSet(LazyOwnCommandSet):
    """One-shot golden-path demo: MCP wiring plus sitrep/recommend/scan."""

    phase = "recon"
    category = miscellaneous_category

    @cmd2.with_category(miscellaneous_category)
    def do_demo(self, line):
        """Run the end-to-end demo: MCP registration, session init, recommend, scan.

        Usage:
            demo                 — full flow (ends with a live lazynmap scan)
            demo --dry-run       — preview every step without scanning
            demo --skip-scan     — session init + recommend_next only

        Steps:
          1. Prints the MCP registration for AI clients
             (``mcp add lazyown python3 ./skills/lazyown_mcp.py``).
          2. Session init — runs ``sitrep`` (CLI equivalent of the MCP
             tool ``lazyown_session_init``).
          3. Runs ``recommend_next`` (CLI equivalent of
             ``lazyown_recommend_next``).
          4. Runs ``lazynmap`` against the current rhost (CLI equivalent
             of ``lazyown_run_command('lazynmap')``).
        """
        args = (line or "").strip().split()
        dry_run = "--dry-run" in args
        skip_scan = "--skip-scan" in args

        shell = self._resolve_shell()
        if shell is None:
            print_error("No shell context available.")
            return

        print_msg("")
        print_msg("  [1/4] MCP registration (run this in your AI client):")
        print_msg("    mcp add lazyown python3 ./skills/lazyown_mcp.py")
        print_msg("    # Claude Code variant:")
        print_msg("    claude mcp add lazyown -- python3 ./skills/lazyown_mcp.py")
        print_msg("    # Hermes variant: hermes skills install skills/lazyown/SKILL.md")
        print_msg("")

        rhost = self.params.get("rhost", "")
        if not rhost:
            print_error("No target set. Run: assign rhost <ip>  (demo needs a target for lazynmap)")
            return

        print_msg(f"  [2/4] session init — sitrep (target: {rhost})")
        if dry_run:
            print_msg("    (dry-run) would run: sitrep")
        else:
            shell.onecmd("sitrep")

        print_msg("  [3/4] recommend_next")
        if dry_run:
            print_msg("    (dry-run) would run: recommend_next")
        else:
            shell.onecmd("recommend_next")

        print_msg("  [4/4] run lazynmap")
        if dry_run or skip_scan:
            print_msg(f"    (skipped) would run: lazynmap {rhost}")
            print_msg("")
            print_warn("demo preview done — re-run without flags for the live flow.")
            return

        shell.onecmd(f"lazynmap {rhost}")
        print_msg("")
        print_msg("demo done — next: auto_populate && facts_show && pentest_report")


__all__ = ["DemoCommandSet"]
