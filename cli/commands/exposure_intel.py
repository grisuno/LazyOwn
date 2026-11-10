"""Target-aware exploit-intelligence exposure command set.

``lazyintel`` binds the discovered world-model services to a local exploit
feed with hard-evidence policy, prints the ranked exposure report and
publishes its outcome through the :mod:`modules.outcome_bus` fan-out so
the C2 surfaces, intel graph and reports stay current.

Subcommands:
    lazyintel [target]                  ranked exposure report
    lazyintel [target] --check          rendered read-only validation commands
    lazyintel --feed <path>             feed override for this run
"""

from __future__ import annotations

import shlex

import cmd2

from cli.commands._base import LazyOwnCommandSet
from modules import lazy_feedmatch
from modules.lazy_exposure import (
    generate_report,
    publish_report,
    save_report,
)
from utils import CYAN, RESET, UNDERLINE, check_rhost, miscellaneous_category, print_error, print_msg, print_succ

VALUED_FLAGS = frozenset({"--feed", "--export"})


class LazyIntelCommandSet(LazyOwnCommandSet):
    """Expose lazy_intel to the operator."""

    phase = "recon"
    category = miscellaneous_category

    @cmd2.with_category(miscellaneous_category)
    def do_lazyintel(self, line: str) -> None:
        """Rank discovered services against local exploit intelligence.

        Usage:
            lazyintel [target] [--check] [--feed <path>] [--json] [--quiet]

        Without a target the current ``rhost`` is used. The feed defaults to
        ``sessions/intel/exploit_feed.json`` (or ``intel_feed`` from
        ``payload.json``) and cisa KEV dumps are accepted as-is.
        """
        args = shlex.split(line) if line.strip() else []
        target = _extract_target(args)
        target = target or str(self.params.get("rhost") or "")
        if not target:
            print_error("lazyintel: no target given and payload.json rhost is empty")
            return
        if not check_rhost(target):
            print_error(f"lazyintel: invalid target {target}")
            return
        feed_path = self._flag(args, "--feed") or str(self.params.get("intel_feed") or lazy_feedmatch.DEFAULT_FEED_PATH)
        show_json = "--json" in args
        quiet = "--quiet" in args
        wants_checks = "--check" in args
        entries = lazy_feedmatch.load_feed(feed_path)
        live_note = ""
        if not entries:
            live_note = "no local feed staged, running live keyless feeds (LAZYOWN_CVE_FEEDS gates network)"
        report = generate_report(target, entries)
        path = save_report(report)
        publish_report(report)
        if show_json:
            import json

            print_msg(json.dumps(report, indent=2, default=str))
            return
        if live_note:
            print_msg(live_note)
        self._print_report(report, target, quiet)
        if wants_checks:
            self._print_checks(report)
        fired = self._autofire_hook(report)
        if fired is not None:
            from modules import lazy_autofire as engine

            if fired.get("action") == "generated":
                print_succ(f"autofire: confirmation chain at {fired.get('path')}")
            elif fired.get("action") == "proposed" and fired.get("chain"):
                print_msg("autofire: proposal ready (assign autofire true to write it)")
            print_msg(
                f"autofire: {fired.get('action')} — {engine.status(dict(self.params)).get('cooldown')} cooldown entries"
            )
        if path is not None and not quiet:
            print_succ(f"report at {path}")

    def _flag(self, args: list[str], flag: str) -> str:
        """Return the value following ``flag`` in the argument list."""
        try:
            index = args.index(flag)
            return args[index + 1] if index + 1 < len(args) else ""
        except ValueError:
            return ""

    def _print_report(self, report: dict, target: str, quiet: bool) -> None:
        """Render the human-readable exposure report."""
        label = str(report.get("temperature") or "clean")
        print_msg(f"{UNDERLINE}lazyintel {target}{RESET} temperature={label} score={report.get('score')}")
        for item in report.get("score_detail") or []:
            print_msg(f"  [{item['points']:>2}p] {item['label']}")
        matches = report.get("matches") or []
        if not matches:
            print_msg("  no in-range exploit matches on discovered services")
        elif not quiet:
            for row in matches:
                marker = {"hot": "HOT  ", "warm": "WARM ", "cold": "COLD "}.get(row["tier"], " ")
                print_msg(
                    f"  {marker} {row['cve_id']:<17} {row['product']:<22} {row['version']:<10} "
                    f"port {str(row['port']):<5} cvss {row['cvss']:<4} ({row['evidence']})"
                )
        review = report.get("version_unknown") or []
        if review:
            print_msg(f"  version-unknown review queue: {', '.join(row['cve_id'] for row in review)}")
        leads = report.get("leads") or []
        if leads and not quiet:
            products = ", ".join(str(lead["product"]) for lead in leads)
            print_msg(f"  unversioned products (leads): {CYAN}{products}{RESET}")

    def _print_checks(self, report: dict) -> None:
        """Render the read-only validation commands for top matches."""
        checks = report.get("checks") or []
        if not checks:
            print_msg("  no rendered checks (rendered checks need bounded in-range matches)")
            return
        for check in checks:
            print_succ(f"{check['cve_id']} -> {check['tool']}")
            print_msg(f"    command: {check['command']}")
            print_msg(f"    expect : {check['expect']}")
            print_msg(f"    explain: {check['explain']}")

    def _autofire_hook(self, report: dict) -> dict | None:
        """Consider the report for autofire when it reaches fire temperature.

        Args:
            report: Exposure report just generated and published.

        Returns:
            The :func:`modules.lazy_autofire.consider_report` result, or
            None when the report carries no fire-tier bounded match.
        """
        from modules import lazy_autofire as engine

        if report.get("temperature") != "hot":
            return None
        return engine.consider_report(report, armed=bool(self.params.get("autofire")))


def _extract_target(args: list[str]) -> str:
    """Return the first positional token, skipping valued flags."""
    skip_next = False
    for item in args:
        if skip_next:
            skip_next = False
            continue
        if item in VALUED_FLAGS:
            skip_next = True
            continue
        if item.startswith("--"):
            continue
        return item
    return ""


__all__ = ["LazyIntelCommandSet"]
