"""CVE local snapshot CommandSet.

Exposes ``cve_sync`` (NVD + Exploit-DB snapshot refresh) and ``cve_search``
(instant offline lookup) backed by :mod:`modules.cve_local`. Registered
automatically by :func:`cli.registry.register_command_sets`.
"""

from __future__ import annotations

import argparse

from cmd2 import Cmd2ArgumentParser, with_argparser, with_category

from cli.commands._base import LazyOwnCommandSet
from utils import ai_category, print_error, print_msg


def _build_sync_parser() -> Cmd2ArgumentParser:
    parser = Cmd2ArgumentParser(prog="cve_sync")
    parser.add_argument("--full", action="store_true", help="Ignore the incremental window and page the whole NVD")
    parser.add_argument("--pages", type=int, default=0, help="Max NVD pages this run (default: config)")
    parser.add_argument("--api-key", default="", help="NVD API key (optional, raises the rate limit)")
    return parser


def _build_search_parser() -> Cmd2ArgumentParser:
    parser = Cmd2ArgumentParser(prog="cve_search")
    parser.add_argument("keyword", help="Product name or CVE id")
    parser.add_argument("version", nargs="?", default="", help="Optional version filter")
    parser.add_argument("--limit", "-n", type=int, default=15, help="Max rows")
    parser.add_argument("--rhost", action="store_true", help="Also print the ss-captured context for the target")
    return parser


class CveLocalCommandSet(LazyOwnCommandSet):
    """Offline CVE snapshot commands."""

    phase = "exploit"
    category = ai_category

    @with_argparser(_build_sync_parser())
    @with_category(ai_category)
    def do_cve_sync(self, args: argparse.Namespace) -> None:
        """Refresh the local NVD/Exploit-DB snapshot for instant searches."""
        from modules import cve_local

        print_msg("Syncing local CVE snapshot (Exploit-DB CSV + NVD API)...")
        report = cve_local.sync(api_key=args.api_key)
        status = cve_local.status()
        print_msg(f"  exploitdb rows: {report.get('exploits', 0)}")
        print_msg(f"  nvd pages this run: {report.get('pages', 0)} (cves: {report.get('cves', 0)})")
        print_msg(
            f"  snapshot totals: {status['cves']} cves, {status['exploits']} exploits, {status['contexts']} ss contexts"
        )
        print_msg("Next runs page only what changed since the last sync (incremental).")

    @with_argparser(_build_search_parser())
    @with_category(ai_category)
    def do_cve_search(self, args: argparse.Namespace) -> None:
        """Instant offline CVE search over the local snapshot."""
        from modules import cve_local

        keyword = args.keyword.strip()
        if not keyword:
            print_error("Pass a product or CVE id.")
            return
        hits = cve_local.search(keyword, version=args.version, max_results=args.limit)
        if not hits:
            print_msg(f"No snapshot hits for '{keyword}'. Run `cve_sync` first.")
            return
        print_msg(f"\n  {'CVE':22s} {'CVSS':5s} {'Published':11s} {'EDB':8s} Description")
        print_msg(f"  {'-' * 96}")
        for hit in hits:
            edb = ",".join(hit["exploitdb"][:3]) or "-"
            description = hit["description"][:52].replace("\n", " ")
            print_msg(f"  {hit['id']:22s} {hit['cvss']:<5.1f} {hit['published'][:10]:11s} {edb:8s} {description}")
        if args.rhost:
            host = self.params.get("rhost", "")
            context = cve_local.context_for_host(host)
            if context:
                print_msg(f"\n  ss context for {host} ({len(context)} services):")
                for service in context:
                    cves = ",".join(service["cves"][:4]) or "-"
                    print_msg(
                        f"    {service['service']:12s} {service['product'][:24]:24s} {service['version']:14s} {cves}"
                    )
            else:
                print_msg(f"\n  No ss context stored for {host or 'unset rhost'} yet.")
        print_msg("")


__all__ = ["CveLocalCommandSet"]
