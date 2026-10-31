"""Internal sentinel command set: provision, dispatch, ingest, checks."""

from __future__ import annotations

import json

import cmd2

from cli.commands._base import LazyOwnCommandSet, extract_flag
from modules import lazy_exposure, lazy_feedmatch, lazy_sentinel
from utils import CYAN, RESET, miscellaneous_category, print_error, print_msg, print_succ


class SentinelCommandSet(LazyOwnCommandSet):
    """Expose the internal-network sentinel to the operator."""

    phase = "recon"
    category = miscellaneous_category

    @cmd2.with_category(miscellaneous_category)
    def do_lazysentinel(self, line: str) -> None:
        """Run the internal sentinel lifecycle.

        Usage:
            lazysentinel provision <cidr>... [--spool-in <path>]
            lazysentinel dispatch <client_id> [--from-provision <id>] [--send]
            lazysentinel ingest <spool path> [--feed <path>] [--json]
            lazysentinel checks <target> [--feed <path>]

        ``provision`` renders one read-only copy-paste blob that sweeps a
        private range from inside the network (beacon, or any box with
        nmap). ``dispatch`` wraps the blob in a c2_exec line. ``ingest``
        parses the spool back into sightings, generates exposure reports
        per host and considers autofire. ``checks`` renders read-only
        validation commands for the ingested services.
        """
        parts = (line or "").strip().split()
        if not parts:
            print_error("Usage: lazysentinel provision|dispatch|ingest|checks ...")
            return
        action, *rest = parts
        if action == "provision":
            self._provision(rest)
        elif action == "dispatch":
            self._dispatch(rest)
        elif action == "ingest":
            self._ingest(rest)
        elif action == "checks":
            self._checks(rest)
        else:
            print_error(f"Unknown lazysentinel action: {action}")

    def _provision(self, rest: list[str]) -> None:
        """Render and record the sweep blob."""
        ranges = [item for item in rest if not item.startswith("--")]
        spool_in = extract_flag(rest, "--spool-in")
        if not ranges:
            print_error("Usage: lazysentinel provision <cidr>...")
            return
        blob = lazy_sentinel.provision_blob(ranges, spool_path=spool_in)
        if blob["errors"]:
            for error in blob["errors"]:
                print_error(f"lazysentinel: {error}")
            return
        print_succ(f"sentinel id {blob['id']} spool {blob['spool_path']}")
        print_msg(blob["script"])
        print_msg("one-liner: sh -c '<blob above>'")

    def _dispatch(self, rest: list[str]) -> None:
        """Print (and optionally run through the shell) the c2_exec line."""
        client_id = next((item for item in rest if not item.startswith("--")), "")
        record_id = extract_flag(rest, "--from-provision")
        record = self._provision_record(record_id)
        client_id = client_id or str((record or {}).get("beacon", ""))
        blob = {"script": str((record or {}).get("script") or "")} if record else None
        if not blob or not blob["script"]:
            print_error("Usage: lazysentinel dispatch <client_id> [--from-provision <id>]  (or provision first)")
            return
        try:
            line = lazy_sentinel.dispatch_line(client_id, blob)
        except ValueError as exc:
            print_error(f"lazysentinel: {exc}")
            return
        print_succ(f"c2_exec line for {client_id}:")
        print_msg(line)
        if "--send" in rest:
            shell = self._resolve_shell()
            if shell is not None:
                shell.onecmd(line)

    def _ingest(self, rest: list[str]) -> None:
        """Parse spool -> sightings -> exposure reports -> autofire."""
        spool_path = next((item for item in rest if not item.startswith("--")), "")
        feed_path = extract_flag(rest, "--feed") or str(
            self.params.get("intel_feed") or lazy_feedmatch.DEFAULT_FEED_PATH
        )
        if not spool_path:
            print_error("Usage: lazysentinel ingest <spool path> [--feed <path>] [--json]")
            return
        parsed = lazy_sentinel.ingest_spool(spool_path)
        sightings = parsed["sightings"]
        if not sightings:
            print_error("lazysentinel: no hosts parsed from the spool")
            return
        saved = lazy_sentinel.save_sightings(sightings)
        entries = lazy_feedmatch.load_feed(feed_path)
        seen_hosts: dict[str, dict] = {}
        for sighting in sightings:
            seen_hosts.setdefault(sighting.host, {})
        reports = []
        for host in list(seen_hosts)[:8]:
            report = lazy_exposure.generate_report(host, entries, sightings=sightings)
            if not entries:
                print_msg(f"  {host}: no local feed, live keyless feeds used")
            reports.append(report)
        if "--json" in rest:
            print_msg(json.dumps(reports, indent=2, default=str))
            return
        for report in reports:
            self._print_brief(report)
            out = lazy_exposure.save_report(report)
            lazy_exposure.publish_report(report)
            if out is not None:
                print_succ(f"report at {out}")
        fired = self._autofire_hook(reports)
        if fired:
            print_succ(f"autofire: {fired['action']} {fired.get('path') or fired['reason']}")
        if saved:
            print_succ(f"sightings at {saved}")

    def _checks(self, rest: list[str]) -> None:
        """Render read-only probes for the last ingested services."""
        target = next((item for item in rest if not item.startswith("--")), "")
        feed_path = extract_flag(rest, "--feed") or str(
            self.params.get("intel_feed") or lazy_feedmatch.DEFAULT_FEED_PATH
        )
        entries = lazy_feedmatch.load_feed(feed_path)
        if not target or not entries:
            print_error("Usage: lazysentinel checks <target> [--feed <path>]")
            return
        sightings = [
            item for item in lazy_sentinel.load_sightings(_latest_sightings_path())
            if target in item.host and item.version
        ]
        if not sightings:
            print_error(f"lazysentinel: no versioned sightings for {target} (ingest first)")
            return
        report = lazy_exposure.generate_report(target, entries, sightings=sightings)
        for check in report.get("checks") or []:
            print_succ(f"{check['cve_id']} -> {check['tool']}")
            print_msg(f"  command: {check['command']}")
            print_msg(f"  expect : {check['expect']}")

    def _print_brief(self, report: dict) -> None:
        """One-line-per-match exposure print."""
        print_msg(f"{CYAN}sentinel host {report.get('target')}{RESET} "
                  f"temperature={report.get('temperature')} score={report.get('score')}")
        for match in report.get("matches") or []:
            print_msg(f"  {match['tier'].upper():<5} {match['cve_id']:<16} {match['product']:<20} v{match['version']:<9} port {match['port']}")

    def _autofire_hook(self, reports: list[dict]):
        """Consider the strongest report for autofire when armed."""
        from modules import lazy_autofire

        armed = bool(self.params.get("autofire"))
        best = max(reports, key=lambda item: lazy_autofire.MAX_FIRE_STEPS if item.get("temperature") == "hot" else 0, default=None)
        if best is None or best.get("temperature") != "hot":
            return None
        return lazy_autofire.consider_report(best, armed=armed)

    def _provision_record(self, record_id: str) -> dict | None:
        """Load a provisioning record by id."""
        if not record_id:
            return None

        path = lazy_sentinel.SPOOL_DIR / f"provision_{record_id}.json"
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            return None


def _latest_sightings_path():
    """Newest saved sightings artefact path."""
    try:
        paths = sorted(lazy_sentinel.SPOOL_DIR.glob("sightings_*.json"))
    except OSError:
        return ""
    return paths[-1] if paths else ""


__all__ = ["SentinelCommandSet"]
