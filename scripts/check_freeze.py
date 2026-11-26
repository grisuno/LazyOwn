#!/usr/bin/env python3
"""Freeze gate: fail when the framework surface grows during a freeze.

Reads the committed baseline in ``scripts/freeze_baseline.json`` and the
live counts (command index, lazyaddons, pwntomate tools). An increase in
any count fails the gate; a decrease only requires rebasing the baseline
downward via ``--update``. ``feat`` work during a freeze needs a signed
exception and a baseline bump in the same PR.

Usage::

    python3 scripts/check_freeze.py            # gate
    python3 scripts/check_freeze.py --update   # rebase baseline
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BASELINE_PATH = ROOT / "scripts" / "freeze_baseline.json"
INDEX_PATH = ROOT / "cli" / "command_index.json"

_METRIC_SOURCES = {
    "commands": ("index", "totals", "unique_commands"),
    "addons": ("glob", "lazyaddons", "*.yaml"),
    "tools": ("glob", "tools", "*.tool"),
}


def _live_counts() -> dict[str, int]:
    """Compute the current surface counts."""
    counts: dict[str, int] = {}
    for metric, source in _METRIC_SOURCES.items():
        if source[0] == "index":
            data = json.loads(INDEX_PATH.read_text(encoding="utf-8"))
            node: object = data
            for key in source[1:]:
                node = node[key]
            counts[metric] = int(node)
        else:
            counts[metric] = len(list((ROOT / source[1]).glob(source[2])))
    return counts


def main() -> int:
    """Run the freeze gate.

    Returns:
        0 when no metric grew beyond the baseline, 1 otherwise.
    """
    parser = argparse.ArgumentParser(description="LazyOwn surface freeze gate")
    parser.add_argument("--update", action="store_true", help="rewrite the baseline with current counts")
    args = parser.parse_args()

    live = _live_counts()
    if args.update:
        BASELINE_PATH.write_text(json.dumps(live, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        print(f"baseline updated: {live}")
        return 0

    baseline = json.loads(BASELINE_PATH.read_text(encoding="utf-8"))
    grown = {m: (baseline.get(m, 0), live[m]) for m in live if live[m] > baseline.get(m, 0)}
    if grown:
        print("FREEZE VIOLATION — surface grew during freeze:")
        for metric, (old, new) in sorted(grown.items()):
            print(f"  {metric}: {old} -> {new}")
        print("A signed exception plus a --update baseline bump is required for feat work.")
        return 1
    print(f"freeze gate ok: {live}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
