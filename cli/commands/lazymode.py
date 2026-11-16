"""Lazymode playbook command set.

Exposes ``lazymode_pb`` so an operator can list and run the lazymode
exploit playbooks (per-vector paths managed in ``playbooks/``) from the
cmd2 shell, mirroring the ``lazyown_lazymode_playbook`` MCP tool. The
command reuses :mod:`modules.lazymode_playbook`; it adds no exploit logic
of its own.
"""

from __future__ import annotations

import json

import cmd2

from cli.commands._base import LazyOwnCommandSet
from utils import exploitation_category, print_error, print_msg, print_warn


class LazymodeCommandSet(LazyOwnCommandSet):
    """List and run lazymode exploit playbooks."""

    phase = "exploit"
    category = "03. Exploitation"

    @cmd2.with_category(exploitation_category)
    def do_lazymode_pb(self, line: str) -> None:
        """List or run lazymode exploit playbooks.

        Usage:
            lazymode_pb list
            lazymode_pb run <name> [target]

        ``list`` prints every lazymode playbook. ``run`` executes one
        against ``target`` (or payload ``rhost`` when omitted) and prints
        the structured outcome. Exploit success is in each step's
        ``session_opened`` field, not the step ``ok`` flag.
        """
        from modules.lazymode_playbook import list_vector_playbooks, run_playbook

        args = (line or "").split()
        action = args[0] if args else "list"
        if action == "list":
            playbooks = list_vector_playbooks()
            if not playbooks:
                print_warn("no lazymode playbooks found in playbooks/")
                return
            for entry in playbooks:
                print_msg(f"{entry['file']:22} {entry['vector']:22} trigger={entry['trigger']}")
            return
        if action == "run":
            if len(args) < 2:
                print_error("usage: lazymode_pb run <name> [target]")
                return
            name = args[1]
            target = args[2] if len(args) > 2 else self.params.get("rhost", "")
            if not target:
                print_error("no target given and rhost is unset")
                return
            print_msg(f"running playbook {name} against {target} ...")
            outcome = run_playbook(name, target=target)
            print_msg(json.dumps(outcome, indent=2))
            return
        print_error("usage: lazymode_pb list | run <name> [target]")
