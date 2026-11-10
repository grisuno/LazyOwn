"""LazyAdaptive policy inspector for the ``adaptive`` fallback contract.

Read-only operator surface over ``modules.failure_verdict`` and
``modules.lazy_fallback``: shows the verdict taxonomy, the action matrix
and the curated fallback graph with Atomic-catalogue presence marks.
Behaviour arming stays on ``apt_chain ... --adaptive``.
"""

from __future__ import annotations

import cmd2

from cli.commands._base import LazyOwnCommandSet
from utils import print_error, print_msg


@cmd2.with_category("12. Miscellaneous")
class LazyAdaptiveCommandSet(LazyOwnCommandSet):
    """Inspect the failure-verdict policy and the fallback graph."""

    phase = "ai"
    category = "AI Autonomous Loop"

    def do_lazy_adaptive(self, line: str) -> None:
        """LazyAdaptive policy inspector.

        Usage:
            lazy_adaptive              Verdict taxonomy and action matrix
            lazy_adaptive graph        Curated fallback graph + catalogue marks
        """
        tokens = (line or "").split()
        subcommand = tokens[0].lower() if tokens else ""
        if subcommand == "graph":
            self._print_graph()
        elif subcommand:
            print_error("Usage: lazy_adaptive [graph]")
        else:
            self._print_policy()

    def _print_policy(self) -> None:
        """Print the verdict taxonomy and the action it requests."""
        from modules.failure_verdict import CLASS_ACTIONS, FailureClass

        print_msg("lazy_adaptive verdict policy (captured evidence -> class -> action):")
        for failure_class in FailureClass:
            print_msg(f"    {failure_class.value:<14} -> {CLASS_ACTIONS[failure_class].value}")
        print_msg("    gates: lockout and scope never retry; tool_missing skips; auth/permission offer alternatives")
        print_msg("    arm behaviour: apt_chain <chain> <target> --adaptive")

    def _print_graph(self) -> None:
        """Print every fallback family with catalogue presence marks."""
        from modules.lazy_fallback import FALLBACK_GRAPH, catalogue_ids

        catalogue = catalogue_ids()
        if catalogue is None:
            print_error("atomic catalogue unavailable; presence marks shown as unknown")
            catalogue = frozenset()
        for family in FALLBACK_GRAPH:
            print_msg(f"  fits: {' | '.join(family.match)}")
            for alternative in family.alternatives:
                gates = []
                if alternative.requires_services:
                    gates.append("services:" + ",".join(alternative.requires_services))
                if alternative.requires_credentials:
                    gates.append("creds")
                mark = "[in catalogue]" if alternative.technique_id in catalogue else "[MISSING]"
                print_msg(f"    {alternative.technique_id:<24} {mark:<16} {alternative.reason}")
                if gates:
                    print_msg(f"      gates: {'; '.join(gates)}")


__all__ = ["LazyAdaptiveCommandSet"]
