#!/usr/bin/env python3
"""Print the recent engineering journal before a change is written.

This is the read half of the read-before-you-write loop. Run it at the start
of a unit of work, then cite the entry number in the change. The
``read-before-write`` workflow rejects a pull request whose body does not cite
a journal entry.
"""

from __future__ import annotations

import argparse
import json
import sys

from scripts.journal import DEFAULT_CATEGORY, DEFAULT_LIMIT, Journal, JournalConfig, JournalError


def _build_parser() -> argparse.ArgumentParser:
    """Build the command line parser."""
    parser = argparse.ArgumentParser(prog="read_journal")
    parser.add_argument("--repo", help="repository slug owner/name (default: origin remote)")
    parser.add_argument("--category", default=DEFAULT_CATEGORY, help="discussion category")
    parser.add_argument("--limit", type=int, default=DEFAULT_LIMIT, help="number of entries")
    parser.add_argument("--json", action="store_true", help="emit raw JSON")
    return parser


def main(argv: list[str] | None = None) -> int:
    """Print the recent journal entries and return the process exit code.

    Args:
        argv: Optional argument vector. Defaults to ``sys.argv``.
    Returns:
        0 on success, 1 when the journal cannot be read.
    """
    args = _build_parser().parse_args(argv)
    try:
        config = JournalConfig.from_git_remote(remote=args.repo, category=args.category)
        entries = Journal(config).entries(args.limit)
    except JournalError as error:
        print(f"[read_journal] {error}", file=sys.stderr)
        return 1

    if args.json:
        print(json.dumps(entries, indent=2))
        return 0

    if not entries:
        print("[read_journal] no journal entries yet")
        return 0

    print("Recent engineering journal. Cite one entry number as 'Journal: #N' in your change.")
    print()
    for entry in entries:
        print(f"# {entry['number']} {entry['title']} ({entry['updatedAt']})")
        print(entry["body"].strip())
        print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
