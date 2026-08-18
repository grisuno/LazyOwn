"""SQLite database layer for LazyOwn — hosts, services, vulns, loot, creds, notes.

Mirrors the Metasploit ``db_*`` workflow with workspace isolation,
nmap XML import, and queryable tables. Uses SQLite (zero deps) with
a ``sessions/db/`` storage directory under the active session dir.
"""

from __future__ import annotations

import csv
import io
import sqlite3
import threading
import xml.etree.ElementTree as ET
from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path
from typing import Any

SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS schema_version (
    version INTEGER PRIMARY KEY,
    applied_at TEXT DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS workspaces (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL,
    description TEXT DEFAULT '',
    created_at TEXT DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS hosts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    workspace_id INTEGER NOT NULL REFERENCES workspaces(id),
    address TEXT NOT NULL,
    mac TEXT DEFAULT '',
    hostname TEXT DEFAULT '',
    os TEXT DEFAULT '',
    os_cpe TEXT DEFAULT '',
    purpose TEXT DEFAULT '',
    state TEXT DEFAULT 'unknown',
    comments TEXT DEFAULT '',
    created_at TEXT DEFAULT (datetime('now')),
    updated_at TEXT DEFAULT (datetime('now')),
    UNIQUE(workspace_id, address)
);

CREATE TABLE IF NOT EXISTS services (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    host_id INTEGER NOT NULL REFERENCES hosts(id),
    port INTEGER NOT NULL,
    protocol TEXT DEFAULT 'tcp',
    state TEXT DEFAULT 'open',
    name TEXT DEFAULT '',
    product TEXT DEFAULT '',
    version TEXT DEFAULT '',
    extra_info TEXT DEFAULT '',
    created_at TEXT DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS vulns (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    host_id INTEGER REFERENCES hosts(id),
    service_id INTEGER REFERENCES services(id),
    name TEXT NOT NULL,
    severity TEXT DEFAULT 'unknown',
    description TEXT DEFAULT '',
    refs TEXT DEFAULT '',
    exploit_available INTEGER DEFAULT 0,
    matched_at TEXT DEFAULT (datetime('now')),
    matched_by TEXT DEFAULT ''
);

CREATE TABLE IF NOT EXISTS loot (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    workspace_id INTEGER NOT NULL REFERENCES workspaces(id),
    host_id INTEGER REFERENCES hosts(id),
    name TEXT NOT NULL,
    loot_type TEXT DEFAULT 'file',
    path TEXT DEFAULT '',
    content_type TEXT DEFAULT '',
    data TEXT DEFAULT '',
    notes TEXT DEFAULT '',
    created_at TEXT DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS creds (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    host_id INTEGER REFERENCES hosts(id),
    service_id INTEGER REFERENCES services(id),
    username TEXT DEFAULT '',
    password TEXT DEFAULT '',
    realm TEXT DEFAULT '',
    cred_type TEXT DEFAULT 'password',
    origin TEXT DEFAULT 'manual',
    cracked INTEGER DEFAULT 0,
    notes TEXT DEFAULT '',
    created_at TEXT DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS notes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    host_id INTEGER REFERENCES hosts(id),
    workspace_id INTEGER REFERENCES workspaces(id),
    note_type TEXT DEFAULT 'general',
    data TEXT DEFAULT '',
    created_at TEXT DEFAULT (datetime('now'))
);

INSERT OR IGNORE INTO schema_version (version) VALUES (1);
"""

MIGRATIONS: list[tuple[int, str]] = [
    (
        2,
        """
        CREATE INDEX IF NOT EXISTS idx_hosts_address ON hosts(address);
        CREATE INDEX IF NOT EXISTS idx_hosts_workspace ON hosts(workspace_id);
        CREATE INDEX IF NOT EXISTS idx_services_host ON services(host_id);
        CREATE INDEX IF NOT EXISTS idx_services_port ON services(port);
        """,
    ),
    (
        3,
        """
        ALTER TABLE creds ADD COLUMN cracked_at TEXT DEFAULT '';
        """,
    ),
    (
        4,
        """
        CREATE INDEX IF NOT EXISTS idx_loot_workspace ON loot(workspace_id);
        CREATE INDEX IF NOT EXISTS idx_notes_workspace ON notes(workspace_id);
        CREATE INDEX IF NOT EXISTS idx_vulns_host ON vulns(host_id);
        CREATE INDEX IF NOT EXISTS idx_creds_host ON creds(host_id);
        """,
    ),
]


class LazyOwnDB:
    """SQLite database for LazyOwn campaign state.

    Thread-safe per-connection (SQLite serialises writes). Not safe to
    share a single :class:`LazyOwnDB` instance across threads without
    external locking; use one connection per thread instead.

    Args:
        db_path: Path to the SQLite file. Defaults to
            ``sessions/db/lazyown.db``.
    """

    def __init__(self, db_path: str | None = None) -> None:
        if db_path is None:
            sessions_dir = Path("sessions")
            sessions_dir.mkdir(parents=True, exist_ok=True)
            db_dir = sessions_dir / "db"
            db_dir.mkdir(parents=True, exist_ok=True)
            db_path = str(db_dir / "lazyown.db")
        self._db_path = db_path
        self._local = threading.local()
        self._closed = False
        self._init_schema()

    def _get_conn(self) -> sqlite3.Connection:
        """Return a per-thread SQLite connection, creating it on first access."""
        if not hasattr(self._local, "conn") or self._local.conn is None:
            conn = sqlite3.connect(self._db_path)
            conn.row_factory = sqlite3.Row
            conn.execute("PRAGMA journal_mode=WAL")
            conn.execute("PRAGMA foreign_keys=ON")
            self._local.conn = conn
        return self._local.conn

    @property
    def db_path(self) -> str:
        """Path to the SQLite database file."""
        return self._db_path

    def _init_schema(self) -> None:
        conn = self._get_conn()
        conn.executescript(SCHEMA_SQL)
        conn.commit()
        self._run_migrations()

    def _current_version(self) -> int:
        cur = self._get_conn().execute(
            "SELECT MAX(version) FROM schema_version"
        )
        row = cur.fetchone()
        return row[0] if row and row[0] is not None else 0

    def _run_migrations(self) -> list[int]:
        """Apply any pending incremental migrations.

        Returns the list of version numbers that were applied during
        this call (empty when the database is already up to date).
        """
        current = self._current_version()
        applied: list[int] = []
        for version, sql in MIGRATIONS:
            if version <= current:
                continue
            conn = self._get_conn()
            try:
                conn.executescript(sql)
                conn.execute(
                    "INSERT OR REPLACE INTO schema_version (version) VALUES (?)",
                    (version,),
                )
                conn.commit()
                applied.append(version)
            except Exception:
                conn.rollback()
                raise
        return applied

    def migration_status(self) -> dict[str, Any]:
        """Return the current and latest migration versions.

        Returns:
            Dict with keys ``current`` (int), ``latest`` (int), and
            ``pending`` (list[int] of versions not yet applied).
        """
        current = self._current_version()
        latest = max((v for v, _ in MIGRATIONS), default=0)
        pending = [v for v, _ in MIGRATIONS if v > current]
        return {"current": current, "latest": latest, "pending": pending}

    @contextmanager
    def _cursor(self) -> Iterator[sqlite3.Cursor]:
        conn = self._get_conn()
        cur = conn.cursor()
        try:
            yield cur
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            cur.close()

    # ------------------------------------------------------------------
    # Credential encryption helpers
    # ------------------------------------------------------------------

    def _maybe_encrypt(self, value: str) -> str:
        """Encrypt a credential value if the crypto module is available."""
        if not value:
            return value
        try:
            from core.config import resolve_aes_key
            from core.crypto import AESencrypt
            key = resolve_aes_key({}, sessions_dir=Path("sessions"))
            ct, _ = AESencrypt(value.encode("utf-8"), key)
            return ct.hex()
        except ImportError:
            return value

    def _maybe_decrypt(self, value: str) -> str:
        """Decrypt a credential value, falling back to plaintext on error."""
        if not value:
            return value
        try:
            from core.config import resolve_aes_key
            from core.crypto import AESdecrypt
            key = resolve_aes_key({}, sessions_dir=Path("sessions"))
            ct = bytes.fromhex(value)
            return AESdecrypt(ct, key).decode("utf-8")
        except (ImportError, ValueError, Exception):
            return value

    # ------------------------------------------------------------------
    # Workspaces
    # ------------------------------------------------------------------

    def workspace_create(self, name: str, description: str = "") -> int:
        """Create a new workspace.

        Returns the workspace ID, or -1 if the name already exists.
        """
        with self._cursor() as cur:
            try:
                cur.execute(
                    "INSERT INTO workspaces (name, description) VALUES (?, ?)",
                    (name, description),
                )
                return cur.lastrowid
            except sqlite3.IntegrityError:
                return -1

    def workspace_list(self) -> list[dict[str, Any]]:
        """Return all workspaces as dicts."""
        with self._cursor() as cur:
            cur.execute("SELECT * FROM workspaces ORDER BY name")
            return [dict(r) for r in cur.fetchall()]

    def workspace_get(self, name: str) -> dict[str, Any] | None:
        """Get a workspace by name, or None."""
        with self._cursor() as cur:
            cur.execute("SELECT * FROM workspaces WHERE name = ?", (name,))
            r = cur.fetchone()
            return dict(r) if r else None

    def workspace_delete(self, name: str) -> bool:
        """Delete a workspace and all its data. Returns True if deleted."""
        ws = self.workspace_get(name)
        if ws is None:
            return False
        wid = ws["id"]
        with self._cursor() as cur:
            host_ids = [
                r[0]
                for r in cur.execute(
                    "SELECT id FROM hosts WHERE workspace_id = ?", (wid,)
                ).fetchall()
            ]
            for hid in host_ids:
                cur.execute("DELETE FROM services WHERE host_id = ?", (hid,))
                cur.execute("DELETE FROM vulns WHERE host_id = ?", (hid,))
                cur.execute("DELETE FROM creds WHERE host_id = ?", (hid,))
                cur.execute("DELETE FROM notes WHERE host_id = ?", (hid,))
                cur.execute("DELETE FROM loot WHERE host_id = ?", (hid,))
            cur.execute("DELETE FROM hosts WHERE workspace_id = ?", (wid,))
            cur.execute("DELETE FROM loot WHERE workspace_id = ?", (wid,))
            cur.execute("DELETE FROM notes WHERE workspace_id = ?", (wid,))
            cur.execute("DELETE FROM workspaces WHERE id = ?", (wid,))
        return True

    # ------------------------------------------------------------------
    # Hosts
    # ------------------------------------------------------------------

    def host_add(
        self,
        workspace_id: int,
        address: str,
        mac: str = "",
        hostname: str = "",
        os: str = "",
        state: str = "unknown",
        **kwargs: Any,
    ) -> int:
        """Add or update a host. Returns the host ID."""
        with self._cursor() as cur:
            existing = cur.execute(
                "SELECT id, os, hostname FROM hosts WHERE workspace_id = ? AND address = ?",
                (workspace_id, address),
            ).fetchone()
            if existing:
                hid = existing["id"]
                merged_os = os or existing["os"]
                merged_hostname = hostname or existing["hostname"]
                cur.execute(
                    """UPDATE hosts SET mac=?, hostname=?, os=?, state=?,
                       updated_at=datetime('now') WHERE id=?""",
                    (mac, merged_hostname, merged_os, state, hid),
                )
                return hid
            cur.execute(
                """INSERT INTO hosts (workspace_id, address, mac, hostname, os, state)
                   VALUES (?, ?, ?, ?, ?, ?)""",
                (workspace_id, address, mac, hostname, os, state),
            )
            return cur.lastrowid

    def host_delete(self, host_id: int) -> bool:
        """Delete a host and its related data."""
        with self._cursor() as cur:
            cur.execute("DELETE FROM services WHERE host_id = ?", (host_id,))
            cur.execute("DELETE FROM vulns WHERE host_id = ?", (host_id,))
            cur.execute("DELETE FROM creds WHERE host_id = ?", (host_id,))
            cur.execute("DELETE FROM notes WHERE host_id = ?", (host_id,))
            cur.execute("DELETE FROM loot WHERE host_id = ?", (host_id,))
            cur.execute("DELETE FROM hosts WHERE id = ?", (host_id,))
        return True

    def host_list(self, workspace_id: int) -> list[dict[str, Any]]:
        """List all hosts in a workspace."""
        with self._cursor() as cur:
            cur.execute(
                "SELECT * FROM hosts WHERE workspace_id = ? ORDER BY address",
                (workspace_id,),
            )
            return [dict(r) for r in cur.fetchall()]

    def host_find(self, workspace_id: int, query: str) -> list[dict[str, Any]]:
        """Search hosts by address, hostname, or os."""
        like = f"%{query}%"
        with self._cursor() as cur:
            cur.execute(
                """SELECT * FROM hosts WHERE workspace_id = ?
                   AND (address LIKE ? OR hostname LIKE ? OR os LIKE ?)
                   ORDER BY address""",
                (workspace_id, like, like, like),
            )
            return [dict(r) for r in cur.fetchall()]

    # ------------------------------------------------------------------
    # Services
    # ------------------------------------------------------------------

    def service_add(
        self,
        host_id: int,
        port: int,
        protocol: str = "tcp",
        state: str = "open",
        name: str = "",
        product: str = "",
        version: str = "",
        **kwargs: Any,
    ) -> int:
        """Add a service to a host."""
        with self._cursor() as cur:
            cur.execute(
                """INSERT INTO services (host_id, port, protocol, state, name, product, version)
                   VALUES (?, ?, ?, ?, ?, ?, ?)""",
                (host_id, port, protocol, state, name, product, version),
            )
            return cur.lastrowid

    def service_list(self, host_id: int) -> list[dict[str, Any]]:
        """List all services on a host."""
        with self._cursor() as cur:
            cur.execute(
                "SELECT * FROM services WHERE host_id = ? ORDER BY port",
                (host_id,),
            )
            return [dict(r) for r in cur.fetchall()]

    # ------------------------------------------------------------------
    # Vulns
    # ------------------------------------------------------------------

    def vuln_add(
        self,
        host_id: int,
        name: str,
        severity: str = "unknown",
        description: str = "",
        refs: str = "",
        **kwargs: Any,
    ) -> int:
        """Add a vulnerability to a host."""
        with self._cursor() as cur:
            cur.execute(
                """INSERT INTO vulns (host_id, name, severity, description, refs)
                   VALUES (?, ?, ?, ?, ?)""",
                (host_id, name, severity, description, refs),
            )
            return cur.lastrowid

    def vuln_list(
        self,
        workspace_id: int,
        severity: str | None = None,
    ) -> list[dict[str, Any]]:
        """List vulns in workspace, optionally filtered by severity."""
        with self._cursor() as cur:
            if severity:
                cur.execute(
                    """SELECT v.*, h.address FROM vulns v
                       JOIN hosts h ON v.host_id = h.id
                       WHERE h.workspace_id = ? AND v.severity = ?
                       ORDER BY v.matched_at DESC""",
                    (workspace_id, severity),
                )
            else:
                cur.execute(
                    """SELECT v.*, h.address FROM vulns v
                       JOIN hosts h ON v.host_id = h.id
                       WHERE h.workspace_id = ?
                       ORDER BY v.matched_at DESC""",
                    (workspace_id,),
                )
            return [dict(r) for r in cur.fetchall()]

    # ------------------------------------------------------------------
    # Creds
    # ------------------------------------------------------------------

    def cred_add(
        self,
        host_id: int,
        username: str = "",
        password: str = "",
        realm: str = "",
        cred_type: str = "password",
        origin: str = "manual",
        **kwargs: Any,
    ) -> int:
        """Add a credential (password encrypted at rest)."""
        encrypted = self._maybe_encrypt(password)
        with self._cursor() as cur:
            cur.execute(
                """INSERT INTO creds (host_id, username, password, realm, cred_type, origin)
                   VALUES (?, ?, ?, ?, ?, ?)""",
                (host_id, username, encrypted, realm, cred_type, origin),
            )
            return cur.lastrowid

    def cred_list(self, workspace_id: int) -> list[dict[str, Any]]:
        """List all creds in workspace (passwords decrypted)."""
        with self._cursor() as cur:
            cur.execute(
                """SELECT c.*, h.address FROM creds c
                   JOIN hosts h ON c.host_id = h.id
                   WHERE h.workspace_id = ?
                   ORDER BY c.created_at DESC""",
                (workspace_id,),
            )
            results = [dict(r) for r in cur.fetchall()]
            for r in results:
                r["password"] = self._maybe_decrypt(r["password"])
            return results

    # ------------------------------------------------------------------
    # Loot
    # ------------------------------------------------------------------

    def loot_add(
        self,
        workspace_id: int,
        name: str,
        loot_type: str = "file",
        path: str = "",
        notes: str = "",
        host_id: int | None = None,
        **kwargs: Any,
    ) -> int:
        """Add a loot entry."""
        with self._cursor() as cur:
            cur.execute(
                """INSERT INTO loot (workspace_id, host_id, name, loot_type, path, notes)
                   VALUES (?, ?, ?, ?, ?, ?)""",
                (workspace_id, host_id, name, loot_type, path, notes),
            )
            return cur.lastrowid

    def loot_list(self, workspace_id: int) -> list[dict[str, Any]]:
        """List all loot in workspace."""
        with self._cursor() as cur:
            cur.execute(
                """SELECT l.*, h.address FROM loot l
                   LEFT JOIN hosts h ON l.host_id = h.id
                   WHERE l.workspace_id = ?
                   ORDER BY l.created_at DESC""",
                (workspace_id,),
            )
            return [dict(r) for r in cur.fetchall()]

    # ------------------------------------------------------------------
    # Notes
    # ------------------------------------------------------------------

    def note_add(
        self,
        workspace_id: int,
        data: str,
        note_type: str = "general",
        host_id: int | None = None,
        **kwargs: Any,
    ) -> int:
        """Add a note."""
        with self._cursor() as cur:
            cur.execute(
                """INSERT INTO notes (workspace_id, host_id, note_type, data)
                   VALUES (?, ?, ?, ?)""",
                (workspace_id, host_id, note_type, data),
            )
            return cur.lastrowid

    def note_list(self, workspace_id: int) -> list[dict[str, Any]]:
        """List all notes in workspace."""
        with self._cursor() as cur:
            cur.execute(
                """SELECT n.*, h.address FROM notes n
                   LEFT JOIN hosts h ON n.host_id = h.id
                   WHERE n.workspace_id = ?
                   ORDER BY n.created_at DESC""",
                (workspace_id,),
            )
            return [dict(r) for r in cur.fetchall()]

    # ------------------------------------------------------------------
    # Import
    # ------------------------------------------------------------------

    def import_nmap_xml(self, workspace_id: int, xml_path: str) -> dict[str, int]:
        """Import an Nmap XML file into the database.

        Returns a dict with counts of imported hosts, services, and os
        fingerprints.
        """
        counts: dict[str, int] = {"hosts": 0, "services": 0, "os": 0}
        root = ET.parse(xml_path).getroot()

        service_rows: list[tuple[int, int, str, str, str, str, str]] = []

        for host_elem in root.findall("host"):
            status = host_elem.find("status")
            if status is None or status.get("state") != "up":
                continue

            address = ""
            mac = ""
            for addr in host_elem.findall("address"):
                addr_type = addr.get("addrtype", "")
                if addr_type == "ipv4":
                    address = addr.get("addr", "")
                elif addr_type == "mac":
                    mac = addr.get("addr", "")

            if not address:
                continue

            hostnames = host_elem.find("hostnames")
            hostname = ""
            if hostnames is not None:
                hn = hostnames.find("hostname")
                if hn is not None:
                    hostname = hn.get("name", "")

            os_els = host_elem.findall(".//osclass")
            os_name = ""
            for os_el in os_els:
                os_name = os_el.get("osfamily", "") or ""
                if os_name:
                    os_name = os_el.get("osgen", "")
                    break

            hid = self.host_add(
                workspace_id, address, mac=mac, hostname=hostname, os=os_name, state="alive"
            )
            counts["hosts"] += 1
            if os_name:
                counts["os"] += 1

            ports = host_elem.find("ports")
            if ports is None:
                continue
            for port_elem in ports.findall("port"):
                port = int(port_elem.get("portid", "0"))
                protocol = port_elem.get("protocol", "tcp")
                svc = port_elem.find("service")
                svc_name = svc.get("name", "") if svc is not None else ""
                product = svc.get("product", "") if svc is not None else ""
                version = svc.get("version", "") if svc is not None else ""

                state_elem = port_elem.find("state")
                state = state_elem.get("state", "open") if state_elem is not None else "open"

                if port and svc_name:
                    service_rows.append((hid, port, protocol, state, svc_name, product, version))
                    counts["services"] += 1

        if service_rows:
            with self._cursor() as cur:
                cur.executemany(
                    """INSERT INTO services (host_id, port, protocol, state, name, product, version)
                       VALUES (?, ?, ?, ?, ?, ?, ?)""",
                    service_rows,
                )

        return counts

    def export_csv(self, table: str, workspace_id: int | None = None) -> str:
        """Export a table to CSV string.

        Args:
            table: One of ``hosts``, ``services``, ``vulns``, ``creds``,
                ``loot``, ``notes``.
            workspace_id: Filter by workspace (required for workspace-
                scoped tables). If None, exports all data.

        Returns:
            CSV-formatted string with header row.
        """

        with self._cursor() as cur:
            if table == "hosts":
                rows = cur.execute("SELECT * FROM hosts ORDER BY address")
            elif workspace_id is not None:
                rows = cur.execute(
                    f"SELECT * FROM {table} WHERE workspace_id = ? ORDER BY id",
                    (workspace_id,),
                )
            else:
                rows = cur.execute(f"SELECT * FROM {table} ORDER BY id")

            out = io.StringIO()
            writer = csv.writer(out)
            writer.writerow([d[0] for d in rows.description])
            writer.writerows(rows.fetchall())
            return out.getvalue()

    def status(self, workspace_id: int) -> dict[str, int]:
        """Return counts for every entity type in a workspace."""
        with self._cursor() as cur:
            counts = {}
            for table in ("hosts", "services", "vulns", "creds", "loot", "notes"):
                if table == "services":
                    cur.execute(
                        "SELECT COUNT(*) FROM services s JOIN hosts h ON s.host_id = h.id WHERE h.workspace_id = ?",
                        (workspace_id,),
                    )
                elif table == "vulns":
                    cur.execute(
                        "SELECT COUNT(*) FROM vulns v JOIN hosts h ON v.host_id = h.id WHERE h.workspace_id = ?",
                        (workspace_id,),
                    )
                elif table == "creds":
                    cur.execute(
                        "SELECT COUNT(*) FROM creds c JOIN hosts h ON c.host_id = h.id WHERE h.workspace_id = ?",
                        (workspace_id,),
                    )
                else:
                    cur.execute(
                        f"SELECT COUNT(*) FROM {table} WHERE workspace_id = ?",
                        (workspace_id,),
                    )
                counts[table] = cur.fetchone()[0]
            return counts

    def close(self) -> None:
        """Close the database connection for the current thread.

        Idempotent — safe to call multiple times.
        """
        if self._closed:
            return
        self._closed = True
        if hasattr(self._local, "conn") and self._local.conn is not None:
            try:
                self._local.conn.close()
            except Exception:
                pass
            finally:
                self._local.conn = None


def get_db(db_path: str | None = None) -> LazyOwnDB:
    """Get or create a :class:`LazyOwnDB` instance.

    This is a convenience factory. The caller is responsible for calling
    :meth:`LazyOwnDB.close` when done.

    Args:
        db_path: Optional path to the SQLite file.

    Returns:
        A new :class:`LazyOwnDB` instance.
    """
    return LazyOwnDB(db_path)


__all__ = ["LazyOwnDB", "get_db", "MIGRATIONS"]
