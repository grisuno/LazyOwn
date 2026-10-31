"""Engagement timeline command set: snapshots, diffs and zombies."""

from __future__ import annotations

import json
import shlex

import cmd2

from cli.commands._base import LazyOwnCommandSet, extract_flag
from modules import lazy_timeline
from utils import CYAN, RESET, miscellaneous_category, print_error, print_msg, print_succ

CHANGE_STYLE = {
    lazy_timeline.KIND_HOST_NEW: f"{CYAN}new    {RESET}",
    lazy_timeline.KIND_HOST_GONE: f"{CYAN}gone   {RESET}",
    lazy_timeline.KIND_PORT_OPENED: f"{CYAN}open   {RESET}",
    lazy_timeline.KIND_PORT_CLOSED: f"{CYAN}closed {RESET}",
    lazy_timeline.KIND_VERSION_CHANGED: f"{CYAN}ver    {RESET}",
    lazy_timeline.KIND_STATE_CHANGED: f"{CYAN}state  {RESET}",
}


class TimelineCommandSet(LazyOwnCommandSet):
    """World-model snapshots worth reading between rounds."""

    phase = "recon"
    category = miscellaneous_category

    @cmd2.with_category(miscellaneous_category)
    def do_lazytimeline(self, line: str) -> None:
        """Record world-model snapshots and read their diffs.

        Usage:
            lazytimeline record [--dns <domain>]... [--dir <path>] [--state <path>] [--json]
            lazytimeline show [--last N]
            lazytimeline diff [--dir <path>] [--a <path> --b <path>] [--json]
            lazytimeline zombie [--dir <path>]

        ``record`` snapshots the world model (optionally tracking DNS
        names for zombie detection). ``diff`` compares the two most
        recent snapshots unless overridden. ``zombie`` lists hosts whose
        DNS stopped resolving while services still answer.
        """
        from modules import lazy_timeline as engine

        args = shlex.split(line) if line.strip() else []
        action = next((item for item in args if not item.startswith("--")), "")
        json_out = "--json" in args
        if action == "record":
            self._record(engine, args, json_out)
            return
        if action == "show":
            self._show(engine, args, json_out)
            return
        if action == "diff":
            self._diff(engine, args, json_out)
            return
        if action == "zombie":
            self._zombie(engine, json_out, args)
            return
        print_error("Usage: lazytimeline record|show|diff|zombie")

    def _record(self, engine, args: list[str], json_out: bool) -> None:
        """Snapshot now, with optional DNS tracking and state override."""
        dns_domains = [value for index, item in enumerate(args) if item == "--dns" and index + 1 < len(args) for value in [args[index + 1]]]
        directory = extract_flag(args, "--dir")
        state_path = extract_flag(args, "--state")
        resolved = engine.resolve_hostnames(dns_domains) if dns_domains else {}
        result = engine.record(snaps_dir=directory, dns=resolved, state_path=state_path)
        if json_out:
            print_msg(json.dumps(result, indent=2, default=str))
            return
        if result.get("path"):
            print_succ(f"snapshot {result['hosts']} hosts at {result['path']}")
            for name, address in (resolved or {}).items():
                state = "resolved" if address else f"{CYAN}unresolved{RESET}"
                print_msg(f"  dns {name}: {state}")
        else:
            print_error("lazytimeline: could not write a snapshot")

    def _show(self, engine, args: list[str], json_out: bool) -> None:
        """Print the newest snapshot summaries."""
        try:
            last = max(1, int(extract_flag(args, "--last") or "3"))
        except ValueError:
            last = 3
        rows = engine.show(last=last)
        if json_out:
            print_msg(json.dumps(rows, indent=2, default=str))
            return
        for row in rows:
            print_msg(f"  snap {row['ts']} hosts={row['hosts']} services={row['services']} ({row['path']})")

    def _diff(self, engine, args: list[str], json_out: bool) -> None:
        """Diff two snapshots (default: two newest, ``--dir`` scoped)."""
        directory = extract_flag(args, "--dir")
        path_a = extract_flag(args, "--a")
        path_b = extract_flag(args, "--b")
        if not (path_a and path_b):
            snapshots = engine.find_snapshots(directory)
            if len(snapshots) < 2:
                print_error("lazytimeline: need two snapshots (record twice, or pass --a/--b)")
                return
            path_a, path_b = str(snapshots[-2]), str(snapshots[-1])
        result = engine.diff(path_a, path_b)
        if json_out:
            print_msg(json.dumps(result, indent=2, default=str))
            return
        changes = result.get("changes") or []
        name_a = path_a.rsplit("/", 1)[-1]
        name_b = path_b.rsplit("/", 1)[-1]
        print_succ(f"{len(changes)} change(s) between {name_a} and {name_b}")
        for change in changes[:25]:
            marker = CHANGE_STYLE.get(change["kind"], change["kind"])
            port = f" port {change['port']}" if change.get("port") else ""
            print_msg(f"  {marker} {change['host']}{port} {change['detail']}")
        zombies = result.get("zombies") or []
        if zombies:
            print_succ(f"zombie hosts: {', '.join(zombies)}")

    def _zombie(self, engine, json_out: bool, args=None) -> None:
        """Zombie hosts from the two most recent ``--dir`` snapshots."""
        directory = extract_flag(args or [], "--dir")
        snapshots = engine.find_snapshots(directory)
        if len(snapshots) < 2:
            print_error("lazytimeline: need two snapshots (record twice)")
            return
        result = engine.diff(str(snapshots[-2]), str(snapshots[-1]))
        zombies = result.get("zombies") or []
        if json_out:
            print_msg(json.dumps({"zombies": zombies}, indent=2))
            return
        if zombies:
            print_succ(f"zombie hosts: {CYAN}{', '.join(zombies)}{RESET}")
        else:
            print_msg("no zombie hosts detected")


__all__ = ["TimelineCommandSet"]
