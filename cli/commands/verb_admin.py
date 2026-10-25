"""Operator administration of the autonomous-loop verb catalog.

The catalog (``modules/verb_catalog``) decides which shell commands the
autonomous loop may propose or execute. Operators browse and toggle it
here instead of editing ``config/verbs.yaml`` by hand: writes are
validated against the live shell catalogue and persisted atomically.
Today's on verbs stay on; everything the operator has not chosen stays
off, so loops never reach a command the operator did not enable.
"""

from __future__ import annotations

import shlex
from dataclasses import dataclass

import cmd2

from cli.commands._base import LazyOwnCommandSet
from utils import print_error, print_msg, print_warn


@dataclass(frozen=True)
class VerbAdminConfig:
    """Display knobs for catalog listing (single place for widths)."""

    name_width: int = 28
    phase_width: int = 10
    risk_width: int = 8
    description_cap: int = 60


VERB_ADMIN = VerbAdminConfig()


def _row_text(entry: dict) -> str:
    """Render one catalog entry as an operator line."""
    state = "on " if entry["enabled"] else "off"
    return (
        f"  [{state}] {entry['name']:<{VERB_ADMIN.name_width}} "
        f"phase={entry['phase']:<{VERB_ADMIN.phase_width}} risk={entry['risk']:<{VERB_ADMIN.risk_width}}"
        f" {entry['description'][: VERB_ADMIN.description_cap]}"
    )


class VerbCommandSet(LazyOwnCommandSet):
    """Browse, toggle and refresh the loop verb catalog."""

    phase = "misc"
    category = "12. Miscellaneous"

    @cmd2.with_category("12. Miscellaneous")
    def do_verb(self, line):
        """Manage the autonomous-loop verb catalog.

        Usage:
          verb                     show stats and enabled verbs
          verb list [keyword] [--phase P] [--state on|off]
          verb on <name>           enable one shell command for the loop
          verb off <name>          disable one shell command for the loop
          verb sync                refresh the catalog from the shell scan
        """
        args = shlex.split(line) if line.strip() else []
        action = args[0] if args else ""
        if action == "sync":
            try:
                from modules.verb_catalog import sync

                stats = sync()
            except Exception as exc:
                print_error(f"verb sync failed: {exc}")
                return
            print_msg(
                f"[+] catalog synced: {stats['total']} verbs "
                f"(on={stats['on']}, off={stats['off']}, added={stats['added']}, removed={stats['removed']})"
            )
            return
        if action in ("on", "off"):
            if len(args) < 2:
                print_error(f"Usage: verb {action} <name>")
                return
            try:
                from modules.verb_catalog import set_enabled

                entry = set_enabled(args[1], action == "on")
            except KeyError:
                print_error(f"[-] unknown shell verb: {args[1]} (run 'verb sync' first)")
                return
            except ValueError as exc:
                print_error(f"[-] {exc}")
                return
            state = "on" if entry["enabled"] else "off"
            print_msg(f"[+] verb {entry['name']} is now {state}")
            return
        if action in ("list", ""):
            keyword = ""
            phase = ""
            state: bool | None = None
            rest = args[1:] if action == "list" else args
            index = 0
            while index < len(rest):
                token = rest[index]
                if token == "--phase" and index + 1 < len(rest):
                    phase = rest[index + 1]
                    index += 2
                    continue
                if token == "--state" and index + 1 < len(rest):
                    raw = rest[index + 1].strip().lower()
                    state = raw in ("on", "true", "1", "enabled")
                    index += 2
                    continue
                if not token.startswith("--"):
                    keyword = token
                index += 1
            try:
                from modules.verb_catalog import search, stats

                overview = stats()
            except Exception as exc:
                print_error(f"verb list failed: {exc}")
                return
            print_msg(f"Catalog: {overview['total']} verbs, on={overview['on']}, off={overview['off']}")
            rows = search(keyword, phase=phase, enabled=state)
            for entry in rows:
                print_msg(_row_text(entry))
            if not rows:
                print_msg("[*] no verbs matched")
            return
        print_warn("Usage: verb [list|on|off|sync] ...")
