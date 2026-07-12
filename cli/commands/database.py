"""Database commands — workspace isolation, host/service/vuln management,
nmap import, export, and status reporting.

Mirrors the Metasploit ``db_*`` workflow. The backing store is
:class:`modules.db.LazyOwnDB` (SQLite in ``sessions/db/lazyown.db``).
"""

from __future__ import annotations

import os

import cmd2

from cli.commands._base import LazyOwnCommandSet
from modules.db import LazyOwnDB
from utils import (
    BLUE,
    CYAN,
    GREEN,
    RED,
    RESET,
    YELLOW,
    miscellaneous_category,
    print_error,
    print_msg,
    print_warn,
)


class DatabaseCommandSet(LazyOwnCommandSet):
    """Database commands for campaign state management."""

    phase = "database"
    category = "12. Miscellaneous"

    def _get_db(self) -> LazyOwnDB:
        shell = self._resolve_shell()
        if shell is None:
            return LazyOwnDB()
        if getattr(shell, "_lazyown_db", None) is None:
            shell._lazyown_db = LazyOwnDB()
        return shell._lazyown_db

    def _active_workspace(self) -> int | None:
        shell = self._resolve_shell()
        if shell is None:
            return None
        ws_name = getattr(shell, "_db_workspace", None) or "default"
        db = self._get_db()
        ws = db.workspace_get(ws_name)
        if ws is None:
            db.workspace_create(ws_name)
            ws = db.workspace_get(ws_name)
        return ws["id"] if ws else None

    # ------------------------------------------------------------------
    # db_init
    # ------------------------------------------------------------------

    @cmd2.with_category(miscellaneous_category)
    def do_db_init(self, line):
        """Initialize the database (creates schema if not exists).

        Usage: db_init [path]
        The database is created at sessions/db/lazyown.db by default.
        """
        db_path = line.strip() or None
        db = LazyOwnDB(db_path)
        shell = self._resolve_shell()
        if shell is not None:
            shell._lazyown_db = db
        print_msg(f"Database initialized at {db.db_path}")

    # ------------------------------------------------------------------
    # db_workspace
    # ------------------------------------------------------------------

    @cmd2.with_category(miscellaneous_category)
    def do_db_workspace(self, line):
        """Manage workspaces (list, create, switch, delete).

        Usage:
            db_workspace             — list workspaces
            db_workspace <name>      — create/switch to workspace
            db_workspace -d <name>   — delete workspace
            db_workspace -r <name>   — rename workspace (not yet supported)
        """
        db = self._get_db()
        args = line.strip().split(maxsplit=2)
        if not line.strip():
            workspaces = db.workspace_list()
            if not workspaces:
                print_msg("No workspaces. Use 'db_workspace <name>' to create one.")
            else:
                shell = self._resolve_shell()
                current = getattr(shell, "_db_workspace", "default") if shell else "default"
                print_msg(f"{'ID':<4} {'Name':<20} {'Description':<30} {'Created'}")
                print_msg("-" * 70)
                for ws in workspaces:
                    marker = "*" if ws["name"] == current else " "
                    print_msg(
                        f"{ws['id']:<4} {marker}{ws['name']:<19} {ws['description']:<30} {ws['created_at']}"
                    )
            return
        if args[0] == "-d" and len(args) >= 2:
            name = args[1]
            if db.workspace_delete(name):
                print_msg(f"Workspace '{name}' deleted.")
            else:
                print_warn(f"Workspace '{name}' not found.")
            return
        if args[0] == "-r":
            print_warn("Rename not yet supported.")
            return
        name = args[0]
        ws = db.workspace_get(name)
        if ws is None:
            db.workspace_create(name)
            print_msg(f"Workspace '{name}' created.")
        shell = self._resolve_shell()
        if shell is not None:
            shell._db_workspace = name
        print_msg(f"Switched to workspace '{name}'.")

    # ------------------------------------------------------------------
    # db_hosts
    # ------------------------------------------------------------------

    @cmd2.with_category(miscellaneous_category)
    def do_db_hosts(self, line):
        """List or add hosts in the active workspace.

        Usage:
            db_hosts                          — list all hosts
            db_hosts -a <ip> [hostname] [os]  — add a host
            db_hosts -d <id>                  — delete a host
            db_hosts -s <query>               — search (by IP, hostname, OS)
        """
        db = self._get_db()
        wid = self._active_workspace()
        if wid is None:
            return
        args = shlex_split(line)

        if not args:
            hosts = db.host_list(wid)
            if not hosts:
                print_msg("No hosts in this workspace.")
            else:
                print_msg(
                    f"{'ID':<4} {'Address':<16} {'Hostname':<25} {'OS':<15} {'State':<10}"
                )
                print_msg("-" * 75)
                for h in hosts:
                    print_msg(
                        f"{h['id']:<4} {h['address']:<16} {h['hostname']:<25} {h['os']:<15} {h['state']:<10}"
                    )
            return

        if args[0] == "-a" and len(args) >= 2:
            address = args[1]
            hostname = args[2] if len(args) > 2 else ""
            os_str = args[3] if len(args) > 3 else ""
            hid = db.host_add(wid, address, hostname=hostname, os=os_str, state="alive")
            print_msg(f"Host '{address}' added (ID: {hid}).")
            return

        if args[0] == "-d" and len(args) >= 2:
            try:
                hid = int(args[1])
                if db.host_delete(hid):
                    print_msg(f"Host ID {hid} deleted.")
                else:
                    print_warn(f"Host ID {hid} not found.")
            except ValueError:
                print_error("Host ID must be a number.")
            return

        if args[0] == "-s" and len(args) >= 2:
            results = db.host_find(wid, args[1])
            if not results:
                print_msg("No matching hosts.")
            else:
                for h in results:
                    print_msg(
                        f"  {h['address']:<16} {h['hostname']:<25} {h['os']:<15} {h['state']}"
                    )
            return

        print_error("Usage: db_hosts [-a <ip> [hostname] [os]] [-d <id>] [-s <query>]")

    # ------------------------------------------------------------------
    # db_services
    # ------------------------------------------------------------------

    @cmd2.with_category(miscellaneous_category)
    def do_db_services(self, line):
        """List all services in the active workspace.

        Usage: db_services [host_id]
        """
        db = self._get_db()
        wid = self._active_workspace()
        if wid is None:
            return
        hosts = db.host_list(wid)
        if not hosts:
            print_msg("No hosts with services.")
            return
        print_msg(f"{'Host':<16} {'Port':<6} {'Proto':<5} {'State':<8} {'Name':<15} {'Product':<20}")
        print_msg("-" * 80)
        for h in hosts:
            services = db.service_list(h["id"])
            for svc in services:
                print_msg(
                    f"{h['address']:<16} {svc['port']:<6} {svc['protocol']:<5} "
                    f"{svc['state']:<8} {svc['name']:<15} {svc['product']:<20}"
                )

    # ------------------------------------------------------------------
    # db_vulns
    # ------------------------------------------------------------------

    @cmd2.with_category(miscellaneous_category)
    def do_db_vulns(self, line):
        """List or add vulnerabilities.

        Usage:
            db_vulns                      — list all vulns
            db_vulns -a <host_id> <name>  — add a vuln
            db_vulns -s <severity>        — filter by severity
        """
        db = self._get_db()
        wid = self._active_workspace()
        if wid is None:
            return
        args = shlex_split(line)

        if not args:
            vulns = db.vuln_list(wid)
            if not vulns:
                print_msg("No vulnerabilities recorded.")
            else:
                print_msg(
                    f"{'ID':<4} {'Host':<16} {'Severity':<10} {'Name':<35} {'Refs'}"
                )
                print_msg("-" * 80)
                for v in vulns:
                    print_msg(
                        f"{v['id']:<4} {v.get('address','?'):<16} {v['severity']:<10} "
                        f"{v['name']:<35} {v.get('refs','')[:25]}"
                    )
            return

        if args[0] == "-a" and len(args) >= 3:
            try:
                hid = int(args[1])
                vname = args[2]
                db.vuln_add(hid, vname)
                print_msg(f"Vulnerability '{vname}' added to host {hid}.")
            except ValueError:
                print_error("Host ID must be a number.")
            return

        if args[0] == "-s" and len(args) >= 2:
            vulns = db.vuln_list(wid, severity=args[1])
            if not vulns:
                print_msg(f"No {args[1]} severity vulnerabilities.")
            else:
                for v in vulns:
                    print_msg(
                        f"  {v.get('address','?'):<16} [{v['severity']:<8}] {v['name']}"
                    )
            return

        print_error("Usage: db_vulns [-a <host_id> <name>] [-s <severity>]")

    # ------------------------------------------------------------------
    # db_creds
    # ------------------------------------------------------------------

    @cmd2.with_category(miscellaneous_category)
    def do_db_creds(self, line):
        """List or add credentials.

        Usage:
            db_creds                          — list all creds
            db_creds -a <host_id> <user> <pass> [type]
        """
        db = self._get_db()
        wid = self._active_workspace()
        if wid is None:
            return
        args = shlex_split(line)

        if not args:
            creds = db.cred_list(wid)
            if not creds:
                print_msg("No credentials stored.")
            else:
                print_msg(f"{'ID':<4} {'Host':<16} {'User':<20} {'Password':<25} {'Type':<12}")
                print_msg("-" * 80)
                for c in creds:
                    print_msg(
                        f"{c['id']:<4} {c.get('address','?'):<16} {c['username']:<20} "
                        f"{'*' * len(c['password']):<25} {c['cred_type']:<12}"
                    )
            return

        if args[0] == "-a" and len(args) >= 4:
            try:
                hid = int(args[1])
                ctype = args[4] if len(args) > 4 else "password"
                db.cred_add(hid, username=args[2], password=args[3], cred_type=ctype)
                print_msg(f"Credential added for host {hid}.")
            except ValueError:
                print_error("Host ID must be a number.")
            return

        print_error("Usage: db_creds [-a <host_id> <user> <pass> [type]]")

    # ------------------------------------------------------------------
    # db_loot
    # ------------------------------------------------------------------

    @cmd2.with_category(miscellaneous_category)
    def do_db_loot(self, line):
        """List or add loot items.

        Usage:
            db_loot                           — list all loot
            db_loot -a <name> <path> [type]   — add a loot entry
        """
        db = self._get_db()
        wid = self._active_workspace()
        if wid is None:
            return
        args = shlex_split(line)

        if not args:
            loot = db.loot_list(wid)
            if not loot:
                print_msg("No loot stored.")
            else:
                print_msg(f"{'ID':<4} {'Name':<25} {'Type':<12} {'Path':<40} {'Notes'}")
                print_msg("-" * 90)
                for l in loot:
                    print_msg(
                        f"{l['id']:<4} {l['name']:<25} {l['loot_type']:<12} "
                        f"{l['path']:<40} {l.get('notes','')[:20]}"
                    )
            return

        if args[0] == "-a" and len(args) >= 3:
            ltype = args[3] if len(args) > 3 else "file"
            db.loot_add(wid, args[1], loot_type=ltype, path=args[2])
            print_msg(f"Loot '{args[1]}' added.")
            return

        print_error("Usage: db_loot [-a <name> <path> [type]]")

    # ------------------------------------------------------------------
    # db_notes
    # ------------------------------------------------------------------

    @cmd2.with_category(miscellaneous_category)
    def do_db_notes(self, line):
        """List or add notes.

        Usage:
            db_notes                      — list all notes
            db_notes -a <text> [type]     — add a note
        """
        db = self._get_db()
        wid = self._active_workspace()
        if wid is None:
            return
        args = shlex_split(line)

        if not args:
            notes = db.note_list(wid)
            if not notes:
                print_msg("No notes.")
            else:
                print_msg(f"{'ID':<4} {'Host':<16} {'Type':<12} {'Data'}")
                print_msg("-" * 70)
                for n in notes:
                    host = n.get("address", "") or "workspace"
                    print_msg(
                        f"{n['id']:<4} {host:<16} {n['note_type']:<12} {n['data'][:50]}"
                    )
            return

        if args[0] == "-a" and len(args) >= 2:
            ntype = args[2] if len(args) > 2 else "general"
            db.note_add(wid, args[1], note_type=ntype)
            print_msg("Note added.")
            return

        print_error("Usage: db_notes [-a <text> [type]]")

    # ------------------------------------------------------------------
    # db_import
    # ------------------------------------------------------------------

    @cmd2.with_category(miscellaneous_category)
    def do_db_import(self, line):
        """Import scan results into the database.

        Usage: db_import <file>
        Supported formats: Nmap XML (.nmap, .xml)
        """
        args = shlex_split(line)
        if not args:
            print_error("Usage: db_import <file>")
            return
        fpath = args[0]
        if not os.path.isfile(fpath):
            print_error(f"File not found: {fpath}")
            return

        db = self._get_db()
        wid = self._active_workspace()
        if wid is None:
            return

        ext = os.path.splitext(fpath)[1].lower()
        if ext in (".nmap", ".xml"):
            try:
                counts = db.import_nmap_xml(wid, fpath)
                print_msg(
                    f"Import complete: {counts['hosts']} hosts, "
                    f"{counts['services']} services, {counts['os']} OS fingerprints."
                )
            except Exception as e:
                print_error(f"Import failed: {e}")
        else:
            print_warn(f"Unsupported format: {ext}. Use .nmap or .xml files.")

    # ------------------------------------------------------------------
    # db_export
    # ------------------------------------------------------------------

    @cmd2.with_category(miscellaneous_category)
    def do_db_export(self, line):
        """Export database table to CSV.

        Usage: db_export <table> [output_file]
        Tables: hosts, services, vulns, creds, loot, notes
        """
        args = shlex_split(line)
        if not args:
            print_error("Usage: db_export <table> [output.csv]")
            return
        table = args[0].lower()
        valid_tables = ("hosts", "services", "vulns", "creds", "loot", "notes")
        if table not in valid_tables:
            print_error(f"Invalid table. Use: {', '.join(valid_tables)}")
            return

        db = self._get_db()
        wid = self._active_workspace()
        csv_data = db.export_csv(table, workspace_id=wid)

        if len(args) >= 2:
            out_path = args[1]
            os.makedirs(os.path.dirname(out_path) or ".", exist_ok=True)
            with open(out_path, "w") as f:
                f.write(csv_data)
            print_msg(f"Exported {table} to {out_path}")
        else:
            print(csv_data)

    # ------------------------------------------------------------------
    # db_status
    # ------------------------------------------------------------------

    @cmd2.with_category(miscellaneous_category)
    def do_db_status(self, line):
        """Show entity counts for the active workspace.

        Usage: db_status
        """
        db = self._get_db()
        wid = self._active_workspace()
        if wid is None:
            return
        counts = db.status(wid)
        print_msg(f"Database: {db.db_path}")
        print_msg(f"Workspace: {getattr(self._resolve_shell(), '_db_workspace', 'default')}")
        print_msg("-" * 35)
        for table in ("hosts", "services", "vulns", "creds", "loot", "notes"):
            print_msg(f"  {table.capitalize():<12}: {counts.get(table, 0)}")


def shlex_split(text: str) -> list:
    """Split text like shlex.split but handle empty strings gracefully."""
    import shlex
    try:
        return shlex.split(text)
    except Exception:
        return text.split()
