"""Golden-path solver commands.

Builds deterministic attack paths from the current world model, stores
them in ``sessions/attack_paths.json``, and pushes each path into the
objective queue for the autonomous loop.

Usage:
    golden_paths build [N]
    golden_paths show
    golden_paths push
"""

from __future__ import annotations

import json
import shlex

import cmd2

from cli.commands._base import LazyOwnCommandSet
from modules import golden_path
from utils import (
    BLUE,
    CYAN,
    GREEN,
    RESET,
    YELLOW,
    print_error,
    print_msg,
    print_succ,
    reporting_category,
)


class GoldenPathsCommandSet(LazyOwnCommandSet):
    """Deterministic attack-path solver commands."""

    phase = "exploit"
    category = reporting_category

    @cmd2.with_category(reporting_category)
    def do_golden_paths(self, line):
        """Build, show, or push attack paths from the world model.

        :param line: 'build [top_k]' | 'show' | 'push'.
        """
        args = shlex.split(line)
        verb = args[0] if args else "show"
        if verb == "build":
            try:
                top_k = int(args[1]) if len(args) > 1 else 5
            except ValueError:
                print_error(f"{YELLOW} golden_paths build [N] expects an integer{RESET}")
                return
            self._build(top_k)
            return
        if verb == "show":
            self._show()
            return
        if verb == "push":
            self._push()
            return
        print_error(f"{YELLOW} Usage: golden_paths build [N] | show | push{RESET}")

    def _build(self, top_k: int) -> None:
        """Solve paths from the live world model and persist them.

        Args:
            top_k: Maximum number of paths to render.
        """
        try:
            result = golden_path.build(top_k=top_k)
        except Exception as exc:
            print_error(f"golden_path build failed: {exc}")
            return
        paths = result.get("paths") or []
        if not paths:
            print_msg(
                f"{YELLOW}No reachable attack paths (hosts={result['stats']['hosts']}, vulns={result['stats']['vulnerabilities']}, creds={result['stats']['credentials']}){RESET}"
            )
            return
        print_succ(f"{GREEN}Solved {len(paths)} attack path(s) -> sessions/{golden_path.ARTIFACT_NAME}{RESET}")
        for idx, path in enumerate(paths, 1):
            print_msg(f"  {CYAN}[{idx}]{RESET} {path['target']} cost={path['cost']} :: {path['summary']}")

    def _show(self) -> None:
        """Render the persisted attack-path artifact."""
        data = golden_path.load_artifact()
        paths = data.get("paths") or []
        if not paths:
            print_msg(f"{YELLOW}No attack paths yet — run: golden_paths build{RESET}")
            return
        generated = data.get("generated_at") or ""
        print_msg(f"{BLUE}Attack paths (generated {generated}){RESET}")
        for idx, path in enumerate(paths, 1):
            print_msg(f"  {CYAN}[{idx}]{RESET} {path['target']} cost={path['cost']} :: {path['summary']}")
            for step in path.get("steps") or []:
                print_msg(f"        {step['from']} -> {step['to']} [{step['action']}] {step['evidence']}")

    def _push(self) -> None:
        """Push the persisted paths into sessions/objectives.jsonl."""
        data = golden_path.load_artifact()
        paths = data.get("paths") or []
        if not paths:
            print_msg(f"{YELLOW}No attack paths yet — run: golden_paths build{RESET}")
            return
        objectives = golden_path.push_objectives(paths)
        priority_counts: dict[str, int] = {}
        for obj in objectives:
            priority_counts[obj.priority] = priority_counts.get(obj.priority, 0) + 1
        print_succ(f"Queued {len(objectives)} objective(s): " + json.dumps(priority_counts))
