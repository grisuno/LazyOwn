"""Estorides integration commands — bidirectional feedback loop with passive OSINT.

Commands:
    estorides_seed     Feed LazyOwn hosts into Estorides for passive discovery.
    estorides_import   Import Estorides-discovered entities into LazyOwn DB/scope.
    estorides_loop     Run the full bidirectional feedback loop (N iterations).
    estorides_surface  Show the combined active + passive attack surface.
"""

from __future__ import annotations

import json
import os

import cmd2

from cli.commands._base import LazyOwnCommandSet
from modules.estorides_importer import (
    ESTORIDES_CASES_DB,
    ESTORIDES_CLI,
    ESTORIDES_DIR,
    EstoridesCaseReader,
    EstoridesStixParser,
    EstoridesToLazyOwnBridge,
    FeedbackLoop,
    extract_seeds_from_db,
    extract_seeds_from_hosts_file,
    extract_seeds_from_scope,
    extract_seeds_from_world_model,
    run_estorides_discover,
)
from utils import (
    GREEN,
    RESET,
    YELLOW,
    print_msg,
    print_warn,
    recon_category,
)


def _yellow(text: str) -> str:
    return f"{YELLOW}{text}{RESET}"


def _green(text: str) -> str:
    return f"{GREEN}{text}{RESET}"


class EstoridesCommandSet(LazyOwnCommandSet):
    """Bidirectional Estorides <-> LazyOwn integration commands."""

    phase = "recon"
    category = "01. Reconnaissance"

    def _check_estorides(self) -> bool:
        """Check that estorides is cloned and available."""
        if not ESTORIDES_DIR.exists():
            print_warn("Estorides is not installed. Run:  estorides  (lazyaddon)")
            print_msg(f"Expected at: {ESTORIDES_DIR}")
            return False
        if not ESTORIDES_CLI.exists():
            print_warn(f"estorides CLI not found at {ESTORIDES_CLI}")
            return False
        return True

    # ------------------------------------------------------------------
    # estorides_seed
    # ------------------------------------------------------------------

    @cmd2.with_category(recon_category)
    def do_estorides_seed(self, line: str) -> None:
        """Feed LazyOwn hosts/domains into Estorides for passive OSINT discovery.

        Usage:
            estorides_seed [--source <src>] [--max-depth <n>] [--max-steps <n>]

        Seed sources:
            all          - All available sources (default)
            world_model  - From sessions/world_model.json
            hosts_file   - From sessions/hostsdiscovery.txt
            db           - From lazyown.db hosts table
            scope        - From payload.json scope list
            <ip/domain>  - Manual seed value

        Examples:
            estorides_seed                          # seed all sources
            estorides_seed --source hosts_file      # only from hostsdiscovery.txt
            estorides_seed --source scope --max-depth 3
            estorides_seed 10.10.14.141             # manual seed
        """
        if not self._check_estorides():
            return

        args = line.strip().split()
        max_depth = 2
        max_steps = 10
        sources: str | None = None
        manual_seeds: list[str] = []

        i = 0
        while i < len(args):
            if args[i] == "--source" and i + 1 < len(args):
                sources = args[i + 1]
                i += 2
            elif args[i] == "--max-depth" and i + 1 < len(args):
                try:
                    max_depth = int(args[i + 1])
                except ValueError:
                    pass
                i += 2
            elif args[i] == "--max-steps" and i + 1 < len(args):
                try:
                    max_steps = int(args[i + 1])
                except ValueError:
                    pass
                i += 2
            else:
                manual_seeds.append(args[i])
                i += 1

        seeds: list[tuple[str, str]] = []

        if manual_seeds:
            for s in manual_seeds:
                from modules.estorides_importer import ipaddress as _ip

                try:
                    _ip.ip_address(s)
                    seeds.append(("ipv4", s))
                except ValueError:
                    seeds.append(("domain", s))

        if not manual_seeds:
            source = sources or "all"
            if source in ("all", "world_model"):
                seeds.extend(extract_seeds_from_world_model())
            if source in ("all", "hosts_file"):
                seeds.extend(extract_seeds_from_hosts_file())
            if source in ("all", "db"):
                seeds.extend(extract_seeds_from_db())
            if source in ("all", "scope"):
                seeds.extend(extract_seeds_from_scope())

        if not seeds:
            print_warn("No seeds found. Run lazynmap first or add hosts via db_hosts -a.")
            return

        print_msg(f"{_green('Feeding')} {len(seeds)} seeds into Estorides...")
        cases_created: list[str] = []
        total_domains = 0
        total_entities = 0

        for seed_type, seed_value in seeds:
            out_path = os.path.join("sessions", f"estorides_seed_{seed_value.replace('/', '_').replace(':', '_')}.json")
            surface = run_estorides_discover(
                seed_type=seed_type,
                seed_value=seed_value,
                max_depth=max_depth,
                max_steps=max_steps,
                out_json=out_path,
            )
            if surface is None:
                print_warn(f"  Failed: {seed_type}:{seed_value}")
                continue

            case_id = surface.get("case_id", "")
            if case_id:
                cases_created.append(case_id)
            domains = surface.get("domains", [])
            entities = surface.get("entities_seen", 0)
            total_domains += len(domains)
            total_entities += entities

            print_msg(f"  {_green(seed_value):<30}  +{len(domains)} domains  +{entities} entities  case={case_id}")

        print_msg(f"\n{_green('Done.')} {len(cases_created)} cases created.")
        print_msg(f"  Total domains discovered:  {total_domains}")
        print_msg(f"  Total entities seen:       {total_entities}")
        if cases_created:
            print_msg(f"  Run 'estorides_import --from case {cases_created[0]}' to import into LazyOwn.")

    # ------------------------------------------------------------------
    # estorides_import
    # ------------------------------------------------------------------

    @cmd2.with_category(recon_category)
    def do_estorides_import(self, line: str) -> None:
        """Import Estorides-discovered entities into LazyOwn database and scope.

        Usage:
            estorides_import [--from <source>] [--case-id <id>] [--no-scope] [--no-db]

        Import sources:
            case        - Read from estorides case store (SQLite)
            stix        - Parse STIX 2.1 bundles from estorides data/
            all         - All available sources (default)

        Options:
            --from <s>      Source to import from (case, stix, all)
            --case-id <id>  Import a specific case by ID
            --no-scope      Do not add discovered assets to payload.json scope
            --no-db         Do not add discovered assets to lazyown.db
            --preview       Preview entities only, do not import

        Examples:
            estorides_import                          # import all
            estorides_import --from stix              # from STIX bundles
            estorides_import --from case --case-id a1b2c3d4
            estorides_import --preview                # preview only
        """
        if not self._check_estorides():
            return

        args = line.strip().split()
        source = "all"
        case_id: str | None = None
        add_scope = True
        add_db = True
        preview = False

        i = 0
        while i < len(args):
            if args[i] == "--from" and i + 1 < len(args):
                source = args[i + 1]
                i += 2
            elif args[i] == "--case-id" and i + 1 < len(args):
                case_id = args[i + 1]
                i += 2
            elif args[i] == "--no-scope":
                add_scope = False
                i += 1
            elif args[i] == "--no-db":
                add_db = False
                i += 1
            elif args[i] == "--preview":
                preview = True
                i += 1
            else:
                i += 1

        all_entities = []

        if source in ("all", "case"):
            reader = EstoridesCaseReader()
            if reader.available:
                stats = reader.stats()
                print_msg(f"Case store: {stats.get('cases', 0)} cases, {stats.get('entities', 0)} entities")
                entities = reader.get_host_entities(case_id=case_id)
                all_entities.extend(entities)
                reader.close()
            else:
                print_warn(f"Case store not found at {ESTORIDES_CASES_DB}")

        if source in ("all", "stix"):
            parser = EstoridesStixParser()
            if parser.available:
                entities = parser.parse()
                all_entities.extend(entities)
                grouped = parser.parse_by_type()
                for etype, values in sorted(grouped.items()):
                    print_msg(f"  STIX {etype}: {len(values)} unique")
            else:
                print_warn("No STIX bundles found. Run 'estorides stix --out data/...' first.")

        if not all_entities:
            print_warn("No entities found to import.")
            print_msg("Run 'estorides_seed' first to populate data, then import.")
            return

        print_msg(f"\n{len(all_entities)} total entities found.")

        if preview:
            self._preview_entities(all_entities)
            return

        bridge = EstoridesToLazyOwnBridge()
        result = bridge.import_entities(
            all_entities,
            add_to_scope=add_scope,
            add_to_db=add_db,
        )

        print_msg(f"\n{_green('Import complete:')}")
        print_msg(f"  Entities processed: {result.entities_total}")
        print_msg(f"  New hosts in DB:    {result.hosts_added}")
        print_msg(f"  Existing hosts:     {result.hosts_existing}")
        print_msg(f"  New scope entries:  {result.scope_entries_added}")
        print_msg(f"  IPs found:          {result.ips_found}")
        print_msg(f"  Domains found:      {result.domains_found}")
        print_msg(f"  CVEs found:         {result.cves_found}")
        print_msg(f"  Emails/contacts:    {result.emails_found}")

        if result.errors:
            for err in result.errors:
                print_warn(f"  Error: {err}")

        if result.hosts_added > 0 or result.scope_entries_added > 0:
            print_msg("\nNext: 'scope' to review, 'lazynmap' or 'nuclei' on new targets.")

    def _preview_entities(self, entities) -> None:
        """Show a preview of entities grouped by type."""
        grouped: dict[str, list[str]] = {}
        for ent in entities:
            grouped.setdefault(ent.entity_type, []).append(ent.value)

        print_msg(f"\n{_yellow('Preview')} — entities by type:")
        for etype in sorted(grouped):
            values = grouped[etype][:10]
            print_msg(f"  {etype:<12} ({len(grouped[etype])}): {', '.join(values)}")
            if len(grouped[etype]) > 10:
                print_msg(f"           ... and {len(grouped[etype]) - 10} more")

    # ------------------------------------------------------------------
    # estorides_loop
    # ------------------------------------------------------------------

    @cmd2.with_category(recon_category)
    def do_estorides_loop(self, line: str) -> None:
        """Run the bidirectional Estorides <-> LazyOwn feedback loop.

        Each iteration:
          1. Extract seeds from LazyOwn (world model, scope, DB, hosts files)
          2. Feed each seed into Estorides discover for passive OSINT
          3. Import new entities back into LazyOwn DB + scope
          4. New entities become seeds for the next iteration
          5. Runs lazynmap / nuclei if operator opts in on new targets

        The loop converges when no new assets are discovered or max
        iterations is reached.

        Usage:
            estorides_loop [--iter <n>] [--depth <n>] [--auto-scan]

        Options:
            --iter <n>       Max iterations (default: 3)
            --depth <n>      Discovery depth per seed (default: 2)
            --auto-scan      Automatically run lazynmap on new IPs discovered
                             by Estorides (requires active scanning permission)

        Examples:
            estorides_loop                    # 3 iterations, passive only
            estorides_loop --iter 5 --depth 3 # 5 iterations, deeper discovery
            estorides_loop --auto-scan        # auto-scan new IPs from OSINT
        """
        if not self._check_estorides():
            return

        args = line.strip().split()
        max_iter = 3
        max_depth = 2
        auto_scan = False

        i = 0
        while i < len(args):
            if args[i] == "--iter" and i + 1 < len(args):
                try:
                    max_iter = int(args[i + 1])
                except ValueError:
                    pass
                i += 2
            elif args[i] == "--depth" and i + 1 < len(args):
                try:
                    max_depth = int(args[i + 1])
                except ValueError:
                    pass
                i += 2
            elif args[i] == "--auto-scan":
                auto_scan = True
                i += 1
            else:
                i += 1

        print_msg(f"{_green('Estorides Feedback Loop')} — up to {max_iter} iterations")
        print_msg(f"  Depth per seed: {max_depth}")

        loop = FeedbackLoop(max_iterations=max_iter, max_depth=max_depth)
        result = loop.run(seed_methods=["world_model", "hosts_file", "scope"])

        print_msg(f"\n{_green('Loop complete.')}")
        print_msg(f"  Iterations:      {result['iterations_completed']}")
        print_msg(f"  Total seeds:     {result['total_seeds']}")
        print_msg(f"  Unique seeds:    {result['total_unique_seeds']}")
        print_msg(f"  New entities:    {result['total_entities_discovered']}")

        surface = result.get("combined_surface", {})
        print_msg(f"  Combined surface: {surface.get('total_unique', 0)} unique assets")
        print_msg(f"    from DB:        {len(surface.get('from_db', []))}")
        print_msg(f"    from scope:     {len(surface.get('from_scope', []))}")
        print_msg(f"    from world_model: {len(surface.get('from_world_model', []))}")

        for it in result.get("history", []):
            print_msg(
                f"  Iter {it['iteration']}: "
                f"{it['seeds_processed']} seeds, "
                f"+{it['entities_discovered']} entities, "
                f"+{len(it['new_assets'])} new assets"
            )

        if auto_scan and surface.get("from_scope"):
            new_ips = [
                e
                for e in surface["from_scope"]
                if not e.startswith("*")
                and not any(c.isalpha() for c in e.replace(".", "").replace("/", "").replace(":", ""))
            ]
            if new_ips:
                print_msg(f"\n{_yellow('Auto-scan:')} {len(new_ips)} new IPs for lazynmap")
                for ip in new_ips[:10]:
                    shell = self._resolve_shell()
                    if shell:
                        shell.onecmd(f"set rhost {ip}")
                        shell.onecmd("lazynmap --quick")
                        print_msg(f"  Scanned: {ip}")

        print_msg(f"\nReview with: {_green('estorides_surface')} and {_green('scope')}")

    # ------------------------------------------------------------------
    # estorides_surface
    # ------------------------------------------------------------------

    @cmd2.with_category(recon_category)
    def do_estorides_surface(self, line: str) -> None:
        """Show the combined active + passive attack surface.

        Aggregates targets from:
          - LazyOwn database (lazyown.db hosts table)
          - LazyOwn scope (payload.json)
          - LazyOwn world model (sessions/world_model.json)
          - Estorides case store (estorides_cases.sqlite)
          - Estorides STIX bundles

        Usage:
            estorides_surface [--json] [--export <path>]

        Options:
            --json          Output as JSON
            --export <path> Export combined surface to JSON file

        Examples:
            estorides_surface
            estorides_surface --json
            estorides_surface --export sessions/combined_surface.json
        """
        args = line.strip().split()
        output_json = False
        export_path: str | None = None

        i = 0
        while i < len(args):
            if args[i] == "--json":
                output_json = True
                i += 1
            elif args[i] == "--export" and i + 1 < len(args):
                export_path = args[i + 1]
                i += 2
            else:
                i += 1

        bridge = EstoridesToLazyOwnBridge()
        surface = bridge.get_combined_surface()

        estorides_entities: dict[str, list[str]] = {}
        if self._check_estorides():
            reader = EstoridesCaseReader()
            if reader.available:
                entities = reader.get_host_entities()
                for ent in entities:
                    estorides_entities.setdefault(ent.entity_type, []).append(ent.value)
                reader.close()

            parser = EstoridesStixParser()
            if parser.available:
                stix_by_type = parser.parse_by_type()
                for etype, values in sorted(stix_by_type.items()):
                    existing = set(estorides_entities.get(etype, []))
                    existing.update(values)
                    estorides_entities[etype] = sorted(existing)

        all_assets: set[str] = set()
        for lst in surface.values():
            if isinstance(lst, list):
                all_assets.update(lst)
        for vals in estorides_entities.values():
            all_assets.update(vals)

        result = {
            "generated_at": __import__("time").strftime("%Y-%m-%dT%H:%M:%S"),
            "total_unique_assets": len(all_assets),
            "lazyown": {
                "db_hosts": len(surface.get("from_db", [])),
                "scope_entries": len(surface.get("from_scope", [])),
                "world_model_hosts": len(surface.get("from_world_model", [])),
            },
            "estorides": {k: len(v) for k, v in sorted(estorides_entities.items())},
            "all_assets": sorted(all_assets),
        }

        if output_json or export_path:
            json_output = json.dumps(result, indent=2, ensure_ascii=False)
            if output_json:
                print_msg(json_output)
            if export_path:
                with open(export_path, "w", encoding="utf-8") as fh:
                    fh.write(json_output)
                print_msg(f"Exported to {export_path}")
            return

        print_msg(f"\n{_green('Combined Attack Surface')}")
        print_msg(f"  Total unique assets: {result['total_unique_assets']}")
        print_msg(f"\n  {_yellow('LazyOwn (active):')}")
        print_msg(f"    DB hosts:          {result['lazyown']['db_hosts']}")
        print_msg(f"    Scope entries:     {result['lazyown']['scope_entries']}")
        print_msg(f"    World model hosts: {result['lazyown']['world_model_hosts']}")

        if surface.get("from_scope"):
            print_msg(f"\n  {_yellow('Scope entries:')}")
            for e in surface["from_scope"][:15]:
                print_msg(f"    {e}")
            if len(surface["from_scope"]) > 15:
                print_msg(f"    ... and {len(surface['from_scope']) - 15} more")

        if self._check_estorides() and estorides_entities:
            print_msg(f"\n  {_yellow('Estorides (passive):')}")
            for etype in sorted(estorides_entities):
                vals = estorides_entities[etype]
                print_msg(f"    {etype:<12} ({len(vals)}): {', '.join(vals[:5])}")
                if len(vals) > 5:
                    print_msg(f"           ... and {len(vals) - 5} more")

        print_msg(f"\nAdd to scope: {_green('scope add <asset>')}")
        print_msg(f"Scan new IPs: {_green('lazynmap <ip>')}")
        print_msg(f"Run loop:     {_green('estorides_loop')}")
