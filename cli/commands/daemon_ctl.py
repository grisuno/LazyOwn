"""Autonomous daemon control extracted from the miscellaneous cluster.

Pending status: originals deleted from ``cli/commands/misc_migrated.py``;
this set is registered by ``cli.registry``.
"""

from __future__ import annotations

import cmd2

from cli.commands._base import LazyOwnCommandSet
from utils import print_error, print_msg, print_warn

__all__ = ["DaemonControlCommandSet"]


class DaemonControlCommandSet(LazyOwnCommandSet):
    """Autonomous daemon control commands."""

    phase = "misc"
    category = "12. Miscellaneous"

    @cmd2.with_category("12. Miscellaneous")
    def do_daemon_mode(self, line):
        """Switch the autonomous daemon between auto, approval and paused modes.

        Usage:
            daemon_mode auto       Run without operator gating (default).
            daemon_mode approval   Require operator approval per command.
            daemon_mode paused     Block the loop before the next step.

        The selected mode is persisted to
        ``sessions/daemon_control.json`` and read by the daemon before
        every step. No daemon restart is required.

        Args:
            line: Whitespace-stripped mode name.

        Returns:
            None.
        """
        argument = (line or "").strip().lower()
        if not argument:
            try:
                from skills.daemon_control import DaemonControl as _DC
                state = _DC(self.sessions_dir).load()
                print_msg(f"daemon mode: {state.mode}")
            except Exception as exc:
                print_error(f"daemon_mode read failed: {exc}")
            return
        try:
            from skills.daemon_control import DaemonControl as _DC
            state = _DC(self.sessions_dir).set_mode(argument)
            print_msg(f"daemon mode -> {state.mode}")
        except ValueError as exc:
            print_error(str(exc))
        except Exception as exc:
            print_error(f"daemon_mode failed: {exc}")

    @cmd2.with_category("12. Miscellaneous")
    def do_daemon_pause(self, line):
        """Pause the autonomous daemon before its next step.

        Equivalent to ``daemon_mode paused``. The daemon polls the
        control file between steps and resumes once the mode flips back
        to auto or approval.

        Args:
            line: Ignored.
        """
        try:
            from skills.daemon_control import DaemonControl as _DC
            _DC(self.sessions_dir).pause()
            print_msg("daemon paused")
        except Exception as exc:
            print_error(f"daemon_pause failed: {exc}")

    @cmd2.with_category("12. Miscellaneous")
    def do_daemon_resume(self, line):
        """Resume the autonomous daemon (switch mode to auto).

        Args:
            line: Ignored.
        """
        try:
            from skills.daemon_control import DaemonControl as _DC
            _DC(self.sessions_dir).resume()
            print_msg("daemon resumed (mode=auto)")
        except Exception as exc:
            print_error(f"daemon_resume failed: {exc}")

    @cmd2.with_category("12. Miscellaneous")
    def do_daemon_veto(self, line):
        """Add or clear vetoed command first-tokens for the autonomous daemon.

        Usage:
            daemon_veto add <command>       Block <command> on future steps.
            daemon_veto remove <command>    Remove a previously-blocked command.
            daemon_veto clear               Drop every veto entry.
            daemon_veto                     List the current vetoes.

        Args:
            line: Sub-command plus optional command token.
        """
        argument = (line or "").strip()
        try:
            from skills.daemon_control import DaemonControl as _DC
            control = _DC(self.sessions_dir)
            if not argument:
                state = control.load()
                if not state.vetoed_commands:
                    print_msg("no vetoed commands")
                else:
                    print_msg("vetoed commands: " + ", ".join(state.vetoed_commands))
                return
            parts = argument.split(maxsplit=1)
            sub = parts[0].lower()
            target = parts[1].strip() if len(parts) > 1 else ""
            if sub == "add" and target:
                state = control.add_veto(target)
                print_msg("vetoed: " + ", ".join(state.vetoed_commands))
            elif sub == "remove" and target:
                state = control.remove_veto(target)
                print_msg("vetoed: " + (", ".join(state.vetoed_commands) or "(none)"))
            elif sub == "clear":
                control.clear_vetoes()
                print_msg("veto list cleared")
            else:
                print_error("usage: daemon_veto add|remove <command> | clear")
        except ValueError as exc:
            print_error(str(exc))
        except Exception as exc:
            print_error(f"daemon_veto failed: {exc}")

    @cmd2.with_category("12. Miscellaneous")
    def do_daemon_focus(self, line):
        """Restrict the autonomous daemon to a set of focus targets.

        Usage:
            daemon_focus <ip_or_host> [<ip_or_host> ...]
            daemon_focus clear         Drop the focus list (run anywhere).
            daemon_focus               Print the current focus targets.

        Args:
            line: Whitespace-separated list of targets or sub-command.
        """
        argument = (line or "").strip()
        try:
            from skills.daemon_control import DaemonControl as _DC
            control = _DC(self.sessions_dir)
            if not argument:
                state = control.load()
                if not state.focus_targets:
                    print_msg("no focus targets (daemon runs anywhere)")
                else:
                    print_msg("focus targets: " + ", ".join(state.focus_targets))
                return
            if argument.lower() == "clear":
                control.set_focus([])
                print_msg("focus targets cleared")
                return
            targets = argument.split()
            state = control.set_focus(targets)
            print_msg("focus targets: " + ", ".join(state.focus_targets))
        except Exception as exc:
            print_error(f"daemon_focus failed: {exc}")

    @cmd2.with_category("12. Miscellaneous")
    def do_daemon_approve(self, line):
        """Approve or veto the daemon's currently-pending action.

        Usage:
            daemon_approve                   Approve the active pending action.
            daemon_approve veto              Veto the active pending action.
            daemon_approve show              Print the pending action (no decision).

        The active action lives in ``sessions/daemon_control.json``
        under ``pending`` and is created by the daemon when running in
        approval mode.

        Args:
            line: Optional sub-command.
        """
        argument = (line or "").strip().lower()
        try:
            from skills.daemon_control import (
                DECISION_APPROVED as _APPROVED,
            )
            from skills.daemon_control import (
                DECISION_VETOED as _VETOED,
            )
            from skills.daemon_control import (
                DaemonControl as _DC,
            )
            control = _DC(self.sessions_dir)
            state = control.load()
            pending = state.pending
            if pending is None:
                print_warn("no pending daemon action")
                return
            if argument == "show":
                print_msg(
                    f"pending {pending.action_id}: {pending.command} (target={pending.target}, reason={pending.reason})"
                )
                return
            decision = _VETOED if argument == "veto" else _APPROVED
            operator = self.params.get("start_user") or "operator"
            final = control.decide(pending.action_id, decision, operator=operator)
            if final is None:
                print_warn("action no longer pending")
                return
            print_msg(
                f"action {final.action_id} {final.decision} (command={final.command})"
            )
        except Exception as exc:
            print_error(f"daemon_approve failed: {exc}")

