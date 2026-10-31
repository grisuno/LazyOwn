"""Autofire command set: intelligence closing the loop into chains."""

from __future__ import annotations

import shlex

import cmd2

from cli.commands._base import LazyOwnCommandSet, extract_flag
from utils import CYAN, RESET, miscellaneous_category, print_error, print_msg, print_succ


class AutoFireCommandSet(LazyOwnCommandSet):
    """Exposure fire-tier matches into confirmation chains."""

    phase = "recon"
    category = miscellaneous_category

    @cmd2.with_category(miscellaneous_category)
    def do_lazyautofire(self, line: str) -> None:
        """Turn fire exposure into read-only confirmation chains.

        Usage:
            lazyautofire status
            lazyautofire fire <target> [--report <path>] [--armed|--unarmed] [--json]
            lazyautofire sweep

        Chains are only written when ``payload.json`` says
        ``assign autofire true``; otherwise the chain data papers as a
        proposal and nothing is persisted. ``fire`` reads the saved
        ``sessions/lazy_intel_<target>.json`` report. ``sweep`` prunes
        expired cooldown entries.
        """
        from modules import lazy_autofire as engine

        args = shlex.split(line) if line.strip() else []
        action = next((item for item in args if not item.startswith("--")), "")
        if action == "status":
            armed = engine.autofire_armed(dict(self.params))
            view = engine.status(dict(self.params))
            cooldown = view.get("entries") or {}
            print_msg(f"autofire armed={CYAN}{armed}{RESET} cooldown_entries={view.get('cooldown')}")
            for key, _stamp in list(cooldown.items())[:10]:
                print_msg(f"  cooldown {key}")
            return
        if action == "sweep":
            pruned = engine.sweep_state()
            print_succ(f"pruned {pruned} expired cooldown entries")
            return
        if action == "fire":
            self._fire(engine, args)
            return
        print_error("Usage: lazyautofire status|fire <target> [--report <path>]|sweep")

    def _fire(self, engine, args: list[str]) -> None:
        """Run one consider pass for a target."""
        target = next((item for item in args if not item.startswith("--")), "")
        report_override = extract_flag(args, "--report")
        if not target and not report_override:
            print_error("Usage: lazyautofire fire <target> [--report <path>]")
            return
        json_out = "--json" in args
        armed = True if "--armed" in args else False if "--unarmed" in args else None
        if armed is None:
            armed = engine.autofire_armed(dict(self.params))
        from pathlib import Path

        if report_override:
            import json as _json

            try:
                report = _json.loads(Path(report_override).read_text(encoding="utf-8"))
            except (OSError, _json.JSONDecodeError) as exc:
                print_error(f"lazyautofire: {exc}")
                return
            result = engine.consider_report(report, armed=armed)
        else:
            result = engine.fire_from_file(target, armed=armed)
        if json_out:
            import json as _json2

            print_msg(_json2.dumps(result, indent=2, default=str))
            return
        print_msg(f"autofire action={CYAN}{result['action']}{RESET} reason: {result['reason']}")
        if result.get("path"):
            print_succ(f"chain at {result['path']}")
        if result.get("errors"):
            for error in result["errors"]:
                print_error(f"  {error}")


__all__ = ["AutoFireCommandSet"]
