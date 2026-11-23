"""MITRE ATT&CK coverage CommandSet.

Exposes ``mitre_coverage``: maps the LazyOwn command catalog to the
ATT&CK matrix and intersects it with the commands the autonomous loops
actually executed, producing the adversary-coverage artefacts under
``sessions/reports/``.
"""

from __future__ import annotations

import argparse

from cmd2 import Cmd2ArgumentParser, with_argparser, with_category

from cli.commands._base import LazyOwnCommandSet
from utils import exploitation_category, print_msg


def _build_parser() -> Cmd2ArgumentParser:
    parser = Cmd2ArgumentParser(prog="mitre_coverage")
    parser.add_argument("--no-executed", action="store_true", help="Skip the executed-commands intersection")
    parser.add_argument("--save", action="store_true", help="Write mitre_coverage.md/.html to sessions/reports/")
    return parser


class MitreCoverageCommandSet(LazyOwnCommandSet):
    """Adversary-coverage reporting commands."""

    phase = "exploit"
    category = exploitation_category

    @with_argparser(_build_parser())
    @with_category(exploitation_category)
    def do_mitre_coverage(self, args: argparse.Namespace) -> None:
        """Report the ATT&CK tactics/techniques LazyOwn covers and executed."""
        from modules import mitre_mapper

        report = mitre_mapper.coverage_report(include_executed=not args.no_executed)
        totals = report["totals"]
        print_msg(
            f"\n  MITRE ATT&CK coverage: {totals['techniques']} techniques / "
            f"{totals['commands']} commands | executed: {totals['executed_techniques']} techniques, "
            f"{totals['executed_commands']} commands"
        )
        print_msg(f"  {'Tactic':24s} {'Tech':>5s} {'Cmds':>5s} {'Exec tech':>10s} {'Exec cmds':>10s}")
        print_msg(f"  {'-' * 62}")
        for bucket in report["tactics"].values():
            print_msg(
                f"  {bucket['tactic']:24s} {bucket['techniques']:>5d} {bucket['commands']:>5d} "
                f"{bucket['executed_techniques']:>10d} {bucket['executed_commands']:>10d}"
            )
        if args.save:
            written = mitre_mapper.write_coverage()
            for kind, path in written.items():
                print_msg(f"  Saved {kind}: {path}")
        print_msg("")


__all__ = ["MitreCoverageCommandSet"]
