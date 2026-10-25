"""Attack-surface operations: confirmed discovery scans, estorides fusion.

``scandiscovery`` lists every IP found in the sessions discovery files
and only launches ``lazynmap`` after the operator confirms — scans never
fire blind. ``estorides_intel`` refreshes the estorides OSINT export and
fuses it into the campaign graphs (intel + attack 3D, circular,
spherical), where matching IPs/values merge nodes instead of duplicating
them, and refreshes the loop summary.
"""

from __future__ import annotations

from pathlib import Path

import cmd2

from cli.commands._base import LazyOwnCommandSet, extract_flag
from utils import (
    print_error,
    print_msg,
    print_warn,
    recon_category,
    scanning_category,
)

BASE_DIR = Path(__file__).resolve().parent.parent.parent
SESSIONS_DIR = BASE_DIR / "sessions"

from modules.surface_ops import (  # noqa: E402
    discovery_targets,
    parse_confirm,
    write_world_model_hosts,
)


class SurfaceCommandSet(LazyOwnCommandSet):
    """Discovery scans and OSINT fusion for the attack surface."""

    phase = "recon"
    category = "01. Reconnaissance"

    @cmd2.with_category(scanning_category)
    def do_scandiscovery(self, line):
        """Scan every discovery IP with operator confirmation.

        Usage: scandiscovery [--yes]

        Lists the IPs collected in ``sessions/hostsdiscovery.txt`` and
        ``sessions/hosts_*_discovery.txt``, asks for confirmation (skipped
        with ``--yes``), then runs ``lazynmap`` once per IP. Aborts
        cleanly on EOF/non-interactive shells.
        """
        args = (line or "").strip().split()
        pre_approved = "--yes" in args
        sessions = str(SESSIONS_DIR)
        try:
            targets = discovery_targets(sessions)
        except Exception as exc:
            print_error(f"cannot read discovery files: {exc}")
            return
        if not targets:
            print_warn("no discovery IPs found under sessions/.")
            return
        print_msg(f"discovery targets ({len(targets)}): {', '.join(targets)}")
        if not pre_approved:
            try:
                answer = input("Launch lazynmap against these IPs? [y/N] ")
            except (EOFError, KeyboardInterrupt):
                print_warn("aborted (no confirmation).")
                return
            if not parse_confirm(answer):
                print_warn("aborted by operator.")
                return
        shell = self._resolve_shell()
        if shell is None or not hasattr(shell, "onecmd"):
            print_error("no shell context to launch scans.")
            return
        for ip in targets:
            print_msg(f"[*] lazynmap {ip}")
            try:
                shell.onecmd(f"lazynmap {ip}")
            except Exception as exc:
                print_error(f"scan failed for {ip}: {exc}")

    @cmd2.with_category(recon_category)
    def do_estorides_intel(self, line):
        """Fuse estorides OSINT entities into the campaign intel graphs.

        Usage: estorides_intel [--run] [--world-model] [--cap N] [--cli PATH]

        Refreshes ``sessions/estorides_lazyown.json`` from the estorides
        checkout (``--run`` forces re-export), merges entities into the
        intel + attack graphs (matching IPs/values fuse nodes, new ones
        arrive tagged), refreshes ``intel_summary.json`` for the
        autonomous loop, and optionally writes new hosts into
        ``world_model.json`` (``--world-model``, feeds the killchain).
        """
        args = (line or "").strip().split()
        force_run = "--run" in args
        write_world = "--world-model" in args
        cap = 300
        cli_path = extract_flag(args, "--cli")
        raw_cap = extract_flag(args, "--cap")
        if raw_cap:
            try:
                cap = max(0, int(raw_cap))
            except ValueError:
                print_error("--cap expects an integer.")
                return
        try:
            from modules.estorides_fusion import (
                find_export,
                load_export,
                run_export,
            )
        except ImportError as exc:
            print_error(f"estorides fusion unavailable: {exc}")
            return
        sessions = str(SESSIONS_DIR)
        export_path = find_export(sessions)
        if export_path is None or force_run:
            print_msg("refreshing estorides export (graph --export lazyown) ...")
            export_path = run_export(sessions, cli_path=cli_path) or find_export(sessions)
        if export_path is None:
            print_error("no estorides export found and refresh failed. Run estorides discovery first.")
            return
        document = load_export(export_path)
        print_msg(
            f"estorides export: {export_path} ({len(document['nodes'])} entities, {len(document['edges'])} relations)"
        )
        if write_world:
            try:
                added = write_world_model_hosts(document, sessions)
            except OSError as exc:
                print_error(f"cannot write world_model.json: {exc}")
                return
            print_msg(f"world_model.json: {added} new host(s) from estorides.")
        try:
            from modules.attack_surface3d import build_attack_graph, refresh_summary
        except ImportError as exc:
            print_error(f"fusion rebuild failed: {exc}")
            return
        try:
            attack = build_attack_graph(sessions, est_cap=cap)
            summary = refresh_summary(attack, sessions)
        except Exception as exc:
            print_error(f"fusion rebuild failed: {exc}")
            return
        fused = sum(1 for n in attack["nodes"] if "estorides" in (n.get("sources") or []))
        funnel = " > ".join(f"{s['stage']}:{s['hosts']}" for s in summary.get("funnel", []))
        print_msg(
            f"[+] attack graph: {len(attack['nodes'])} nodes, {len(attack['edges'])} edges, {fused} estorides-fused."
        )
        if funnel:
            print_msg(f"funnel {funnel}")
        top = summary.get("top_exposed", [])[:3]
        for entry in top:
            print_msg(f"top {entry['host']} exposure {entry['score']}")
