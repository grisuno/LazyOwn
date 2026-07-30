"""Collaboration CLI commands — multi-operator teamwork from the shell.

Exposes the real-time collaboration layer (target locks, operator presence,
event sharing) that currently lives only in the C2 web dashboard.
"""

from __future__ import annotations

import cmd2

from cli.commands._base import LazyOwnCommandSet
from utils import (
    miscellaneous_category,
    print_error,
    print_msg,
    print_warn,
)


class CollaborationCommandSet(LazyOwnCommandSet):
    """Multi-operator collaboration commands for the CLI."""

    phase = "collaboration"
    category = "12. Miscellaneous"

    def _get_collab(self):
        """Lazy-load collaboration singletons from modules.collab_bp."""
        try:
            from modules.collab_bp import (
                get_event_bus,
                get_lock_manager,
                get_operator_registry,
            )
        except ImportError:
            return None, None, None
        return get_event_bus(), get_lock_manager(), get_operator_registry()

    def _resolve_target(self, target: str) -> str:
        """Resolve a target argument: explicit IP or rhost from payload."""
        if target:
            return target
        rhost = self.params.get("rhost", "")
        if rhost:
            return rhost
        return ""

    @cmd2.with_category(miscellaneous_category)
    def do_lock_target(self, line):
        """Acquire an advisory lock on a target to prevent tool collisions.

        Usage:
            lock_target [target_ip]
            lock_target 10.10.11.5

        Without an argument, locks the current rhost from payload.json.
        Active locks are visible to all connected operators via 'team_status'.
        Locks auto-expire after 5 minutes unless refreshed.
        """
        target = self._resolve_target(line.strip())
        if not target:
            print_error("No target specified. Use: lock_target <ip>")
            print_error("Or set a target first: assign rhost <ip>")
            return

        _, lock_mgr, _ = self._get_collab()
        if lock_mgr is None:
            print_warn("Collaboration module not available (C2 not running).")
            print_msg("Start the C2 server first: srv start")
            return

        operator = getattr(self._resolve_shell(), "operator_name", None) or "cli-operator"

        if lock_mgr.acquire(target, operator):
            locks = lock_mgr.status()
            print_msg(f"Locked: {target}  (operator: {operator})")
            if target in locks:
                remaining = locks[target].get("remaining_secs", "?")
                print_msg(f"  TTL: {remaining}s (renew with: lock_target {target})")
        else:
            locks = lock_mgr.status()
            if target in locks:
                holder = locks[target].get("operator", "unknown")
                print_warn(f"Target {target} is already locked by: {holder}")
                print_msg("Wait for them to finish, or ask them to: unlock_target")
            else:
                print_error(f"Failed to acquire lock on {target}.")

    @cmd2.with_category(miscellaneous_category)
    def do_unlock_target(self, line):
        """Release an advisory lock on a target.

        Usage:
            unlock_target [target_ip]
            unlock_target 10.10.11.5
        """
        target = self._resolve_target(line.strip())
        if not target:
            print_error("No target specified.")
            return

        _, lock_mgr, _ = self._get_collab()
        if lock_mgr is None:
            print_warn("Collaboration module not available.")
            return

        operator = getattr(self._resolve_shell(), "operator_name", None) or "cli-operator"

        if lock_mgr.release(target, operator):
            print_msg(f"Unlocked: {target}")
        else:
            print_warn(f"Could not unlock {target}. It may not be locked by you.")

    @cmd2.with_category(miscellaneous_category)
    def do_team_status(self, line):
        """Show active operators and target locks.

        Usage:
            team_status

        Displays who is online, which targets are locked, and by whom.
        Requires the C2 server to be running.
        """
        bus, lock_mgr, registry = self._get_collab()

        if registry is None:
            print_warn("Collaboration module not available (C2 not running).")
            print_msg("Start with: srv start")
            return

        operators = registry.active_operators() if registry else []

        print_msg("\nTeam status:\n")

        if operators:
            print_msg("  Online operators:")
            for op in operators:
                name = getattr(op, "name", str(op))
                joined = getattr(op, "joined_at", "")
                print_msg(f"    - {name}  (since {joined})")
        else:
            print_msg("  Online operators: 1 (you)")

        if lock_mgr:
            locks = lock_mgr.all_locks()
            if locks:
                print_msg(f"\n  Active locks ({len(locks)}):")
                for lock in locks:
                    target = getattr(lock, "target", str(lock))
                    operator = getattr(lock, "operator", "?")
                    remaining = getattr(lock, "ttl_secs", "?")
                    print_msg(f"    - {target}  locked by {operator}  (TTL: {remaining}s)")
            else:
                print_msg("\n  Active locks: none")
        else:
            print_msg("\n  Active locks: unavailable")

        if bus:
            recent = bus.recent(3) if hasattr(bus, "recent") else []
            if recent:
                print_msg(f"\n  Recent events ({len(recent)}):")
                for event in recent:
                    etype = getattr(event, "type", str(event))
                    payload = getattr(event, "payload", {})
                    desc = str(payload.get("message", payload))[:80]
                    print_msg(f"    [{etype}] {desc}")
        print_msg("")

    @cmd2.with_category(miscellaneous_category)
    def do_team_chat(self, line):
        """Send a message to all connected operators.

        Usage:
            team_chat <message>
            team_chat Found SMB signing disabled on 10.10.11.5, starting relay

        Messages are broadcast in real-time via the C2 event bus.
        """
        if not line.strip():
            print_msg("Usage: team_chat <message>")
            return

        bus, _, _ = self._get_collab()
        if bus is None:
            print_warn("Collaboration module not available (C2 not running).")
            return

        operator = getattr(self._resolve_shell(), "operator_name", None) or "cli-operator"

        try:
            from modules.collab_bp import publish_event
        except ImportError:
            print_error("Cannot import collab_bp. Is the C2 running?")
            return

        publish_event("chat", {"message": line.strip()}, operator)
        print_msg(f"[team_chat] {operator}: {line.strip()}")

    @cmd2.with_category(miscellaneous_category)
    def do_share_finding(self, line):
        """Share a finding or credential discovery with the team.

        Usage:
            share_finding <text>
            share_finding Default admin:admin credentials on port 8080

        Broadcasts via team event bus for real-time visibility.
        """
        if not line.strip():
            print_msg("Usage: share_finding <description>")
            return

        bus, _, _ = self._get_collab()

        operator = getattr(self._resolve_shell(), "operator_name", None) or "cli-operator"

        if bus:
            try:
                from modules.collab_bp import publish_event
            except ImportError:
                pass
            else:
                publish_event("finding", {"message": line.strip(), "target": self.params.get("rhost", "")}, operator)

        print_msg(f"[shared] {operator}: {line.strip()}")
        try:
            from modules.db import LazyOwnDB
            db = LazyOwnDB()
            ws_id = getattr(self._resolve_shell(), "_db_workspace_id", None)
            db.note_add(f"[{operator}] {line.strip()}", "finding", ws_id)
        except Exception:
            pass
