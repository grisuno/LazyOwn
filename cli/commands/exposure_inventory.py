"""Exploit intelligence feeding command set: lazy_search and lazyinventory."""

from __future__ import annotations

import json
import shlex
from pathlib import Path

import cmd2

from cli.commands._base import LazyOwnCommandSet, extract_flag
from modules import lazy_exposure, lazy_feedmatch, lazy_inventory
from utils import miscellaneous_category, print_error, print_msg, print_succ


class IntelOpsCommandSet(LazyOwnCommandSet):
    """Saved-search grammar and the host-reported inventory.

    ``lazysearch`` runs the Shodan-lite grammar over the engagement
    database. ``lazyinventory`` renders a read-only collector blob (posix
    or PowerShell) and ingests its output back as host-source sightings
    so the feed matcher can promote an unversioned lead into a matched
    with harm evidence.
    """

    phase = "recon"
    category = miscellaneous_category

    @cmd2.with_category(miscellaneous_category)
    def do_lazysearch(self, line: str) -> None:
        """Query the engagement database with the saved-search grammar.

        Usage:
            lazysearch port:3389 -host:vpn tech:"apache tomcat" sev:high
            lazysearch --json --db <path> --workspace <name> <query...>

        Spot keys: host|ip, port, service, product|tech, version, os,
        state, sev|severity, cve, user. Untagged words search any text
        column. Every token AND-composed; ``-`` prefix excludes.
        """
        args = shlex.split(line) if line.strip() else []
        db_path = extract_flag(args, "--db")
        workspace = extract_flag(args, "--workspace") or "default"
        query = " ".join(item for item in args if not item.startswith("--"))
        from modules import lazy_search as engine

        result = engine.execute(None, query, workspace_name=workspace, db_path=db_path)
        if "--json" in args:
            print_msg(json.dumps(result, indent=2, default=str))
            return
        for error in result.get("errors") or []:
            print_error(f"lazysearch: {error}")
        hosts = result.get("hosts") or []
        services = result.get("services") or []
        vulns = result.get("vulns") or []
        creds = result.get("creds") or []
        print_succ(f"matches hosts={len(hosts)} services={len(services)} vulns={len(vulns)} creds={len(creds)}")
        for host in hosts[:10]:
            print_msg(f"  host {host.get('address')} os={host.get('os') or '?'} state={host.get('state') or '?'}")
        for service in services[:10]:
            product = " ".join(
                part for part in (service.get("name"), service.get("product"), service.get("version")) if part
            )
            print_msg(f"  svc {service.get('host')}:{service.get('port')} {product}")
        for vuln in vulns[:10]:
            print_msg(f"  vuln {vuln.get('name')} sev={vuln.get('severity')} host={vuln.get('address') or '?'}")
        for cred in creds[:10]:
            print_msg(f"  cred {cred.get('username')}@{cred.get('address')} type={cred.get('cred_type')}")

    @cmd2.with_category(miscellaneous_category)
    def do_lazyinventory(self, line: str) -> None:
        """Collect and ingest host-reported packages (source=host).

        Usage:
            lazyinventory command [linux|windows] [--export <path>]
            lazyinventory ingest <file> [--target <ip>] [--platform auto|linux|windows] [--feed <path>] [--json]

        ``command`` prints the read-only collector blob to paste into a
        beacon session or a terminal. ``ingest`` parses its stdout back,
        builds ``source: host`` sightings and regenerates the exposure
        report for the target.
        """
        from modules import lazy_inventory as engine

        parts = (line or "").strip()
        args = shlex.split(parts)
        if not args:
            print_error("Usage: lazyinventory command|ingest ...")
            return
        action, *rest = args
        if action == "command":
            platform = next((item for item in rest if not item.startswith("--")), "linux").lower()
            blob = engine.inventory_blob(platform)
            if not blob:
                print_error(f"lazyinventory: unknown platform {platform}")
                return
            export = extract_flag(rest, "--export")
            if export:
                destination = Path(export)
                destination.parent.mkdir(parents=True, exist_ok=True)
                destination.write_text(blob, encoding="utf-8")
                print_succ(f"blob written to {destination}")
            print_succ(f"read-only {platform} collector (paste into a beacon session):")
            print_msg(blob)
            return
        if action == "ingest":
            self._ingest(engine, rest)
        else:
            print_error(f"Unknown lazyinventory action: {action}")

    def _ingest(self, engine, rest: list[str]) -> None:
        """Parse captured output and rebuild the exposure report."""
        capture_path = next((item for item in rest if not item.startswith("--")), "")
        target = extract_flag(rest, "--target") or str(self.params.get("rhost") or "")
        platform = extract_flag(rest, "--platform") or "auto"
        feed_path = extract_flag(rest, "--feed") or str(
            self.params.get("intel_feed") or lazy_feedmatch.DEFAULT_FEED_PATH
        )
        if not capture_path:
            print_error("Usage: lazyinventory ingest <file> [--target <ip>] [--platform ...]")
            return
        if not target:
            print_error("lazyinventory: --target (or payload.json rhost) is required")
            return
        try:
            capture_text = Path(capture_path).read_text(encoding="utf-8", errors="replace")
        except OSError as exc:
            print_error(f"lazyinventory: {exc}")
            return
        entries = engine.parse_blob_output(capture_text, platform)
        entries = self._fill_platform(engine, entries, capture_text)
        if not entries:
            print_error("lazyinventory: no package rows parsed from the capture")
            return
        sighting_rows = engine.to_sightings(entries, target)
        sighting_rows = _merge_port_sightings(engine, target, sighting_rows)
        feed = lazy_feedmatch.load_feed(feed_path)
        if not feed:
            print_msg("lazyinventory: no local feed staged, live keyless feeds will be used")
        report = lazy_exposure.generate_report(target, feed, sightings=sighting_rows)
        out = lazy_exposure.save_report(report, SPOOL_DIR / f"lazy_intel_{target.replace(':', '_')}.json")
        lazy_exposure.publish_report(report)
        if "--json" in rest:
            print_msg(json.dumps(report, indent=2, default=str))
            return
        print_succ(f"{len(entries)} host-reported packages for {target}")
        for match in report.get("matches") or []:
            print_msg(
                f"  {match['tier'].upper():<5} {match['cve_id']:<16} {match['product']:<22} v{match['version']:<10} src={match.get('source', 'scanner')}"
            )
        for learn in report.get("version_unknown") or []:
            print_msg(f"  review {learn['cve_id']} (unbounded) on port {learn['port']}")
        for lead in report.get("leads") or []:
            print_msg(f"  lead {lead['product']} still without a version")
        if out is not None:
            print_succ(f"report at {out}")

    def _fill_platform(self, engine, entries: list[dict], capture_text: str) -> list[dict]:
        """Stamp the platform tag when the capture lacked one."""
        _ = engine
        if not entries:
            return []
        if not any((item or {}).get("os") for item in entries):
            tag = "windows" if capture_text.lstrip().startswith("#LAZYINVENTORY windows") else "linux"
            for item in entries:
                item.setdefault("os", tag)
        return entries


def _merge_port_sightings(engine, target: str, host_rows: list):
    """Port sightings (world model) plus package sightings in one list.

    Packages carry no port, so the report gets both tables: endpoint
    spoofing stays with the scanner values, package versions come from
    the host's own table.
    """
    from modules import lazy_exposure as reporting

    _ = engine
    port_rows = reporting.read_sightings(target)
    return host_rows + port_rows


SPOOL_DIR = lazy_inventory.SPOOL_DIR


__all__ = ["IntelOpsCommandSet"]
