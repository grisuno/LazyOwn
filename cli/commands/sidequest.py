"""Side-question CommandSet: read-only review of loop decision checkpoints.

Exposes the :mod:`modules.sidequest` engine to the operator shell. Every
decision the autonomous loop records is an immutable checkpoint; these commands
let an operator list them and ask the model a question about one without
touching the running loop. The engine never mutates loop state, so these
commands are safe to run against a live campaign.
"""

from __future__ import annotations

from cmd2 import with_category

from cli.commands._base import LazyOwnCommandSet
from utils import print_error, print_msg, print_warn


class SidequestCommandSet(LazyOwnCommandSet):
    """Operator-facing side-question commands over the decision ledger."""

    phase = "diagnostics"
    category = "Diagnostics"

    @with_category("Diagnostics")
    def do_sidequest(self, statement) -> None:
        """Review frozen loop decisions read-only: sidequest list | ask.

        Usage:
            sidequest list [run_id]
            sidequest ask <checkpoint_id> <question...>

        ``list`` prints recent decision checkpoints with their ordinal id.
        ``ask`` answers a question about one checkpoint using only that frozen
        decision, never running a command or changing loop state.
        """
        from modules import sidequest

        tokens = str(getattr(statement, "args", statement) or "").split()
        if not tokens or tokens[0] not in ("list", "ask"):
            print_warn("usage: sidequest list [run_id] | sidequest ask <checkpoint_id> <question>")
            return
        if tokens[0] == "list":
            run_id = tokens[1] if len(tokens) > 1 else ""
            checkpoints = sidequest.list_checkpoints(run_id=run_id)
            if not checkpoints:
                print_warn("no decision checkpoints recorded yet")
                return
            for row in checkpoints:
                flag = "llm" if row["model_fallback"] else row["source"]
                print_msg(f"{row['checkpoint_id']}  [{flag}] step {row['step']}  {row['chosen'][:80]}")
            return
        if len(tokens) < 3:
            print_warn("usage: sidequest ask <checkpoint_id> <question>")
            return
        ordinal = tokens[1]
        question = " ".join(tokens[2:])
        result = sidequest.ask(ordinal, question)
        if not result.get("ok"):
            print_error(f"sidequest failed: {result.get('error', 'unknown error')}")
            return
        print_msg(result["answer"])


__all__ = ["SidequestCommandSet"]
