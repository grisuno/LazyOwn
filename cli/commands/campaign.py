"""Campaign export/import commands — portable engagement packages.

Package a full campaign (database, sessions, world model, credentials,
notes, loot) into a single portable .zip file.  Import restores everything
into a new workspace so engagements can be shared, archived, or replayed.
"""

from __future__ import annotations

import json
import shutil
import tempfile
import zipfile
from datetime import UTC, datetime
from pathlib import Path

import cmd2

from cli.commands._base import LazyOwnCommandSet
from modules.db import LazyOwnDB
from utils import (
    miscellaneous_category,
    print_error,
    print_msg,
    print_warn,
)

BASE_DIR = Path(__file__).resolve().parent.parent.parent
SESSIONS_DIR = BASE_DIR / "sessions"
DB_PATH = SESSIONS_DIR / "db" / "lazyown.db"
EXPORTS_DIR = SESSIONS_DIR / "exports"

PACKAGE_VERSION = 1


class CampaignCommandSet(LazyOwnCommandSet):
    """Export and import full campaign packages as portable archives."""

    phase = "campaign"
    category = "12. Miscellaneous"

    @cmd2.with_category(miscellaneous_category)
    def do_campaign(self, line):
        """Export or import an entire campaign as a portable package.

        Usage:
            campaign export [name]     — package the current campaign
            campaign import <file>     — restore a campaign from a package
            campaign list              — list exported campaign packages

        Export packages include:
          - SQLite database dump (all workspaces, hosts, services, vulns,
            creds, loot, notes)
          - sessions/ files (nmap scans, world model, objectives, events)
          - payload.json snapshot
          - campaign metadata (timestamp, operator, phase)

        Examples:
            campaign export
            campaign export htb_machine_name
            campaign import sessions/exports/htb_machine_name_20260730.zip
            campaign list
        """
        args = line.strip().split()
        if not args:
            print_msg("Usage: campaign [export|import|list] [name|file]")
            print_msg("Examples:")
            print_msg("  campaign export htb_machine")
            print_msg("  campaign import sessions/exports/htb_machine_20260730.zip")
            print_msg("  campaign list")
            return

        action = args[0].lower()
        arg = args[1] if len(args) > 1 else ""

        if action == "export":
            self._campaign_export(arg)
        elif action == "import":
            if not arg:
                print_error("Specify a package file to import.")
                return
            self._campaign_import(arg)
        elif action == "list":
            self._campaign_list()
        else:
            print_error(f"Unknown action: {action}. Use export, import, or list.")

    def _gather_campaign_manifest(self, name: str) -> dict:
        """Build a manifest describing the current campaign state."""
        now = datetime.now(UTC).isoformat()

        db = LazyOwnDB()
        status = db.status()

        session_files: list[str] = []
        if SESSIONS_DIR.exists():
            for f in sorted(SESSIONS_DIR.rglob("*")):
                if f.is_file() and "exports" not in str(f) and "db" not in str(f):
                    session_files.append(str(f.relative_to(SESSIONS_DIR)))

        world_model = {}
        wm_path = SESSIONS_DIR / "world_model.json"
        if wm_path.exists():
            try:
                world_model = json.loads(wm_path.read_text(encoding="utf-8"))
            except (json.JSONDecodeError, OSError):
                pass

        payload_snapshot = {}
        payload_path = BASE_DIR / "payload.json"
        if payload_path.exists():
            try:
                payload_snapshot = json.loads(payload_path.read_text(encoding="utf-8"))
            except (json.JSONDecodeError, OSError):
                pass

        return {
            "package_version": PACKAGE_VERSION,
            "name": name or "campaign",
            "exported_at": now,
            "entity_counts": status,
            "world_model_phase": world_model.get("phase", "unknown"),
            "session_files": session_files,
            "host_count": status.get("hosts", 0),
            "service_count": status.get("services", 0),
            "vuln_count": status.get("vulns", 0),
            "cred_count": status.get("creds", 0),
        }

    def _campaign_export(self, name: str):
        """Package the current campaign into a portable .zip archive."""
        EXPORTS_DIR.mkdir(parents=True, exist_ok=True)

        manifest = self._gather_campaign_manifest(name)
        timestamp = datetime.now(UTC).strftime("%Y%m%d_%H%M%S")
        safe_name = (name or "campaign").replace(" ", "_").replace("/", "_")
        archive_name = f"{safe_name}_{timestamp}.zip"
        archive_path = EXPORTS_DIR / archive_name

        print_msg(f"Packaging campaign '{safe_name}' ...")

        with zipfile.ZipFile(archive_path, "w", zipfile.ZIP_DEFLATED) as zf:
            zf.writestr("manifest.json", json.dumps(manifest, indent=2, default=str))

            if DB_PATH.exists():
                zf.write(DB_PATH, "lazyown.db")
                print_msg(f"  + database ({DB_PATH.stat().st_size / 1024:.1f} KB)")

            payload_path = BASE_DIR / "payload.json"
            if payload_path.exists():
                zf.writestr(
                    "payload.json",
                    payload_path.read_text(encoding="utf-8"),
                )
                print_msg("  + payload.json")

            session_added = 0
            for rel_path in manifest.get("session_files", []):
                full_path = SESSIONS_DIR / rel_path
                if full_path.is_file():
                    arcname = f"sessions/{rel_path}"
                    zf.write(full_path, arcname)
                    session_added += 1

            if session_added:
                print_msg(f"  + {session_added} session files")

        archive_size = archive_path.stat().st_size
        print_msg(f"Campaign exported: {archive_path}")
        print_msg(f"  Size: {archive_size / 1024:.1f} KB")
        print_msg(
            f"  Hosts: {manifest['host_count']}  "
            f"Services: {manifest['service_count']}  "
            f"Vulns: {manifest['vuln_count']}  "
            f"Creds: {manifest['cred_count']}"
        )
        print_msg(f"  Share with: campaign import {archive_path}")

    def _campaign_import(self, package_path: str):
        """Restore a campaign from an exported .zip archive."""
        archive = Path(package_path)
        if not archive.is_absolute():
            archive = Path.cwd() / archive
        if not archive.exists():
            candidates = sorted(EXPORTS_DIR.glob(f"*{package_path}*"), reverse=True)
            if candidates:
                archive = candidates[0]
                print_msg(f"Found: {archive}")
            else:
                print_error(f"Package not found: {package_path}")
                print_msg("Use 'campaign list' to see available packages.")
                return

        if not archive.suffix == ".zip":
            print_error("Package must be a .zip file.")
            return

        print_msg(f"Importing campaign from: {archive.name}")

        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)

            with zipfile.ZipFile(archive, "r") as zf:
                zf.extractall(tmp)

            manifest_path = tmp / "manifest.json"
            if not manifest_path.exists():
                print_error("Invalid package: manifest.json not found.")
                return

            try:
                manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            except (json.JSONDecodeError, OSError) as exc:
                print_error(f"Invalid manifest: {exc}")
                return

            pkg_version = manifest.get("package_version", 0)
            if pkg_version > PACKAGE_VERSION:
                print_warn(
                    f"Package version {pkg_version} is newer than this "
                    f"LazyOwn version ({PACKAGE_VERSION}). Some data may be skipped."
                )

            name = manifest.get("name", "imported")
            now = datetime.now(UTC).strftime("%Y%m%d_%H%M%S")
            workspace_name = f"{name}_{now}"

            db_path = tmp / "lazyown.db"
            if db_path.exists():
                db = LazyOwnDB()
                db.workspace_create(workspace_name)
                ws = db.workspace_get(workspace_name)
                workspace_id = ws["id"] if ws else None

                import sqlite3

                try:
                    src_conn = sqlite3.connect(str(db_path))
                    src_conn.row_factory = sqlite3.Row

                    tables = ["hosts", "services", "vulns", "creds", "loot", "notes"]
                    imported = 0
                    for table in tables:
                        try:
                            rows = src_conn.execute(f"SELECT * FROM {table}").fetchall()
                        except sqlite3.OperationalError:
                            continue

                        if not rows:
                            continue

                        columns = rows[0].keys()
                        col_str = ", ".join(columns)
                        placeholders = ", ".join(["?" for _ in columns])

                        for row in rows:
                            values = [row[c] for c in columns]
                            if "workspace_id" in columns:
                                idx = list(columns).index("workspace_id")
                                values[idx] = workspace_id
                            if "id" in columns:
                                idx = list(columns).index("id")
                                values[idx] = None

                            db._cursor(
                                f"INSERT OR IGNORE INTO {table} ({col_str}) VALUES ({placeholders})",
                                *values,
                            )
                            imported += 1

                    src_conn.close()

                    if imported:
                        print_msg(f"  + {imported} database rows imported into workspace '{workspace_name}'")
                except Exception as exc:
                    print_warn(f"Database import skipped: {exc}")
            else:
                print_warn("No database found in package. Sessions only.")

            sessions_src = tmp / "sessions"
            if sessions_src.exists() and sessions_src.is_dir():
                session_imported = 0
                for f in sessions_src.rglob("*"):
                    if f.is_file():
                        rel = f.relative_to(sessions_src)
                        dest = SESSIONS_DIR / rel
                        dest.parent.mkdir(parents=True, exist_ok=True)
                        shutil.copy2(f, dest)
                        session_imported += 1
                if session_imported:
                    print_msg(f"  + {session_imported} session files restored")

            payload_src = tmp / "payload.json"
            if payload_src.exists():
                dest = SESSIONS_DIR / f"payload_{workspace_name}.json"
                shutil.copy2(payload_src, dest)
                print_msg(f"  + payload.json snapshot saved to {dest.name}")

        print_msg(f"Campaign imported into workspace: {workspace_name}")
        print_msg(f"  Switch: db_workspace {workspace_name}")
        print_msg("  Verify: facts_show --refresh")

    def _campaign_list(self):
        """List exported campaign packages."""
        EXPORTS_DIR.mkdir(parents=True, exist_ok=True)

        packages = sorted(EXPORTS_DIR.glob("*.zip"), reverse=True)
        if not packages:
            print_msg("No exported campaigns found.")
            print_msg(f"Exports directory: {EXPORTS_DIR}")
            print_msg("Use: campaign export [name]")
            return

        print_msg(f"\nExported campaigns ({len(packages)}):\n")
        for pkg in packages:
            mtime = datetime.fromtimestamp(pkg.stat().st_mtime).strftime("%Y-%m-%d %H:%M")
            size_kb = pkg.stat().st_size / 1024

            try:
                with zipfile.ZipFile(pkg, "r") as zf:
                    with zf.open("manifest.json") as mf:
                        manifest = json.loads(mf.read().decode("utf-8"))
                    name = manifest.get("name", "?")
                    hosts = manifest.get("host_count", "?")
                    phase = manifest.get("world_model_phase", "?")
            except Exception:
                name = pkg.stem
                hosts = "?"
                phase = "?"

            print_msg(f"  {pkg.name:<45} {size_kb:>6.0f} KB  {hosts} hosts  phase={phase}  {mtime}")
        print_msg("")
        print_msg("Use: campaign import <filename>")
