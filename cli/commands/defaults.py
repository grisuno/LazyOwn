"""Build-defaults inspection and override command set.

Phase-scoped home for the ``defaults`` operator command (category
``12. Miscellaneous``). Build-time fallbacks live in
``config/defaults.toml`` and are read through ``core.defaults``;
this command shows effective values and writes per-engagement
overrides into ``payload.json`` through the canonical ``assign``
path, so the TOML file itself is never rewritten at runtime.

Usage:
    defaults show
    defaults show wordlists
    defaults set wordlist /path/to/list.txt
    defaults set lport 4444
    defaults set rport 443
"""

from __future__ import annotations

import os
import shlex

import cmd2

from cli.assign import apply_assign as _apply_assign
from cli.commands._base import LazyOwnCommandSet
from core.config import save_payload as _save_payload
from core.defaults import load_defaults
from utils import RESET, YELLOW, miscellaneous_category, print_error, print_msg, print_succ

_OVERRIDABLE = {
    "wordlist": "wordlist",
    "lport": "lport",
    "rport": "rport",
}


class DefaultsCommandSet(LazyOwnCommandSet):
    """Inspect and override build-time default constants."""

    phase = "config"
    category = miscellaneous_category

    @cmd2.with_category(miscellaneous_category)
    def do_defaults(self, line):
        """Show or override build-time defaults (TOML + payload.json).

        :param line: 'show [section]' or 'set <name> <value>'.
        """
        args = shlex.split(line)
        if not args or args[0] == "show":
            section = args[1] if len(args) > 1 else ""
            self._show(section)
            return
        if args[0] == "set" and len(args) == 3:
            self._set(args[1], args[2])
            return
        print_error(f"{YELLOW} Usage: defaults show [section] | defaults set <wordlist|lport|rport> <value>{RESET}")

    def _show(self, section):
        """Print TOML defaults alongside live payload values."""
        try:
            doc = load_defaults()
        except (FileNotFoundError, ValueError) as exc:
            print_error(f"Cannot load defaults: {exc}")
            return
        sections = [section] if section else sorted(doc)
        if section and section not in doc:
            print_error(f"Unknown section: {section} (try: {', '.join(sorted(doc))})")
            return
        for name in sections:
            print_msg(f"[{name}]")
            for key, value in doc[name].items():
                live = self.params.get(key, "")
                print_msg(f"  {key} = {value}   (live: {live})")

    def _set(self, name, value):
        """Persist an override into payload.json via the assign path."""
        key = _OVERRIDABLE.get(name)
        if key is None:
            print_error(f"Unknown default: {name} (try: {', '.join(sorted(_OVERRIDABLE))})")
            return
        if name == "wordlist" and not os.path.exists(value):
            print_error(f"Wordlist not found: {value}")
            return
        if name in ("lport", "rport"):
            try:
                port = int(value)
            except (TypeError, ValueError):
                print_error(f"Port must be an integer between 1 and 65535: {value!r}")
                return
            if not 1 <= port <= 65535:
                print_error(f"Port must be between 1 and 65535, got {port}")
                return
        issues: list = []
        shell = self._resolve_shell() or self
        updated = _apply_assign(
            self.params,
            key,
            value,
            save=_save_payload,
            on_issue=issues.append,
        )
        if not updated:
            detail = f": {issues[0]}" if issues else ""
            print_error(f"Cannot set {name}{detail}")
            return
        print_succ(f"{name} set to {value} (payload.json updated)")
