"""Tests for modules.db — LazyOwnDB SQLite layer.

Covers workspace lifecycle, host/service insertion, CSV export, and
nmap XML import.
"""

from __future__ import annotations

import csv
import io
import tempfile
from pathlib import Path

import pytest

from modules.db import LazyOwnDB


@pytest.fixture
def fresh_db():
    """Return a LazyOwnDB backed by a temporary SQLite file."""
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = Path(tmpdir) / "test.db"
        db = LazyOwnDB(str(db_path))
        yield db


class TestLazyOwnDB:
    def test_initial_schema(self, fresh_db):
        """Schema tables must exist immediately after construction."""
        with fresh_db._cursor() as cur:
            cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
            names = {r["name"] for r in cur.fetchall()}
        expected = {
            "schema_version",
            "workspaces",
            "hosts",
            "services",
            "vulns",
            "loot",
            "creds",
            "notes",
        }
        assert expected.issubset(names)

    def test_workspace_create_and_list(self, fresh_db):
        """Creating a workspace returns a positive ID and lists correctly."""
        ws_id = fresh_db.workspace_create("eng1", "first engagement")
        assert isinstance(ws_id, int) and ws_id > 0

        workspaces = fresh_db.workspace_list()
        assert any(w["name"] == "eng1" for w in workspaces)

    def test_duplicate_workspace_returns_negative_one(self, fresh_db):
        """Duplicate workspace names return -1 (not crash)."""
        fresh_db.workspace_create("dup")
        result = fresh_db.workspace_create("dup")
        assert result == -1

    def test_host_crud(self, fresh_db):
        """Insert, retrieve, delete hosts."""
        ws = fresh_db.workspace_create("hosts_test")
        host_id = fresh_db.host_add(ws, "10.0.0.1", hostname="dc01")
        assert host_id > 0

        hosts = fresh_db.host_list(ws)
        assert len(hosts) == 1
        assert hosts[0]["address"] == "10.0.0.1"

        fresh_db.host_delete(host_id)
        assert len(fresh_db.host_list(ws)) == 0

    def test_host_upsert_updates_existing(self, fresh_db):
        """Adding the same address twice updates the existing row."""
        ws = fresh_db.workspace_create("upsert_test")
        hid1 = fresh_db.host_add(ws, "10.0.0.1", os="Linux")
        hid2 = fresh_db.host_add(ws, "10.0.0.1", os="Windows")
        assert hid1 == hid2
        hosts = fresh_db.host_list(ws)
        assert hosts[0]["os"] == "Windows"

    def test_service_crud(self, fresh_db):
        """Services can be attached to a host and queried."""
        ws = fresh_db.workspace_create("svc_test")
        hid = fresh_db.host_add(ws, "10.0.0.2")
        sid = fresh_db.service_add(hid, 445, "tcp", name="smb", product="Samba")
        assert sid > 0

        svcs = fresh_db.service_list(hid)
        assert len(svcs) == 1
        assert svcs[0]["port"] == 445
        assert svcs[0]["name"] == "smb"

    def test_credential_storage(self, fresh_db):
        """Credentials are stored per host and retrieved per workspace."""
        ws = fresh_db.workspace_create("cred_test")
        hid = fresh_db.host_add(ws, "10.0.0.3")
        fresh_db.cred_add(hid, "admin", "P@ssw0rd")
        creds = fresh_db.cred_list(ws)
        assert len(creds) >= 1
        matching = [c for c in creds if c["username"] == "admin"]
        assert len(matching) == 1
        assert matching[0]["password"] == "P@ssw0rd"

    def test_csv_export(self, fresh_db):
        """CSV export produces well-formed rows."""
        ws = fresh_db.workspace_create("csv_test")
        fresh_db.host_add(ws, "192.168.1.1", os="Linux")
        csv_str = fresh_db.export_csv("hosts", workspace_id=ws)
        rows = list(csv.DictReader(io.StringIO(csv_str)))
        assert len(rows) == 1
        assert rows[0]["address"] == "192.168.1.1"

    def test_nmap_xml_import(self, fresh_db, tmp_path):
        """Importing a minimal nmap XML populates hosts and services."""
        ws = fresh_db.workspace_create("nmap_test")
        xml_path = tmp_path / "scan.xml"
        xml_path.write_text("""<?xml version="1.0"?>
        <nmaprun>
          <host>
            <status state="up"/>
            <address addr="10.10.10.10" addrtype="ipv4"/>
            <hostnames><hostname name="box.htb" type="user"/></hostnames>
            <ports>
              <port protocol="tcp" portid="80">
                <state state="open"/>
                <service name="http" product="Apache httpd" version="2.4.41"/>
              </port>
            </ports>
            <os><osmatch name="Linux 5.4" accuracy="98"/></os>
          </host>
        </nmaprun>""")
        result = fresh_db.import_nmap_xml(ws, str(xml_path))
        assert result["hosts"] == 1

        hosts = fresh_db.host_list(ws)
        assert hosts[0]["address"] == "10.10.10.10"

        svcs = fresh_db.service_list(hosts[0]["id"])
        assert len(svcs) == 1
        assert svcs[0]["port"] == 80
        assert svcs[0]["product"] == "Apache httpd"

    def test_workspace_delete(self, fresh_db):
        """Deleting a workspace removes its hosts."""
        ws = fresh_db.workspace_create("del_test")
        fresh_db.host_add(ws, "10.0.0.4")
        fresh_db.workspace_delete("del_test")
        assert fresh_db.workspace_get("del_test") is None

    def test_loot_and_notes(self, fresh_db):
        """Loot and notes are stored per workspace."""
        ws = fresh_db.workspace_create("extra_test")
        fresh_db.loot_add(ws, "secret.txt", loot_type="file", path="/tmp/secret.txt")
        fresh_db.note_add(ws, "found credentials in config file")
        loot = fresh_db.loot_list(ws)
        assert len(loot) == 1
        notes = fresh_db.note_list(ws)
        assert len(notes) == 1
