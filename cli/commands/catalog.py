"""Command catalog — browse all registered commands by keyword, phase or category.

Backed by the auto-generated ``cli/command_index.json`` so the listing stays
in sync with the source tree. Addons and plugins registered at runtime are
shown by the ``addons`` view.
"""

from __future__ import annotations

import json
import os

import cmd2

from cli.commands._base import LazyOwnCommandSet
from utils import miscellaneous_category, print_msg


class CatalogCommandSet(LazyOwnCommandSet):
    """Browse the command catalog."""

    phase = "misc"
    category = "12. Miscellaneous"

    def _index(self) -> dict:
        index_path = os.path.join(os.getcwd(), "cli", "command_index.json")
        if not os.path.exists(index_path):
            return {}
        with open(index_path, "r", encoding="utf-8") as handle:
            return json.load(handle)

    @cmd2.with_category(miscellaneous_category)
    def do_catalog(self, line):
        """Browse the command catalog.

        Usage:
          catalog                 show totals and commands by category
          catalog <keyword>       filter commands by keyword
          catalog --phase <p>     list commands in a phase (recon, enum, ...)
          catalog --category <c>  list commands in a category
          catalog --count         show totals only
          catalog --json <kw>     dump matching commands as JSON
        """
        index = self._index()
        commands = index.get("commands", [])
        totals = index.get("totals", {})
        parts = line.split()

        if not line.strip():
            print_msg(
                f"Catalog: {totals.get('unique_commands', len(commands))} commands, "
                f"{totals.get('phases', 0)} phases, {totals.get('categories', 0)} categories"
            )
            by_cat: dict[str, int] = {}
            for entry in commands:
                by_cat[entry.get("category") or entry.get("phase") or "uncategorized"] = (
                    by_cat.get(entry.get("category") or entry.get("phase") or "uncategorized", 0) + 1
                )
            for category, count in sorted(by_cat.items(), key=lambda kv: (-kv[1], kv[0])):
                print_msg(f"  {count:<5}  {category}")
            return

        if parts[0] == "--count":
            print_msg(json.dumps(totals, indent=2))
            return

        if parts[0] == "--json":
            keyword = parts[1] if len(parts) > 1 else ""
            hits = self._filter_commands(commands, keyword=keyword)
            print_msg(json.dumps(hits, indent=2))
            return

        if parts[0] == "--phase":
            phase = parts[1] if len(parts) > 1 else ""
            hits = [c for c in commands if c.get("phase") == phase]
            self._print_hits(hits, f"phase '{phase}'")
            return

        if parts[0] == "--category":
            category = " ".join(parts[1:]) if len(parts) > 1 else ""
            hits = [c for c in commands if (c.get("category") or "") == category]
            self._print_hits(hits, f"category '{category}'")
            return

        hits = self._filter_commands(commands, keyword=line.strip())
        self._print_hits(hits, f"keyword '{line.strip()}'")

    def _filter_commands(self, commands: list[dict], keyword: str) -> list[dict]:
        """Filter *commands* by keyword in name or summary."""
        kw = keyword.lower()
        if not kw:
            return list(commands)
        return [c for c in commands if kw in c.get("name", "").lower() or kw in (c.get("summary") or "").lower()]

    def _print_hits(self, hits: list[dict], label: str) -> None:
        """Print *hits* (grouped by category) under *label*."""
        if not hits:
            print_msg(f"No commands found for {label}.")
            return
        print_msg(f"{len(hits)} commands for {label}:")
        by_cat: dict[str, list[str]] = {}
        for entry in hits:
            bucket = entry.get("category") or entry.get("phase") or "uncategorized"
            by_cat.setdefault(bucket, []).append(entry.get("name", ""))
        for category in sorted(by_cat):
            print_msg(f"  [{category}]")
            for name in sorted(by_cat[category]):
                print_msg(f"    {name}")


def shlex_split(text: str) -> list:
    """Split text like shlex.split but handle empty strings gracefully."""
    import shlex

    try:
        return shlex.split(text)
    except Exception:
        return text.split()
