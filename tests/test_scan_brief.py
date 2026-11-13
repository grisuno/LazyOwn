"""Tests for the loop scan-reuse layer and the nmap scan brief module."""

from __future__ import annotations

import time

import pytest


@pytest.fixture()
def temp_sessions(tmp_path, monkeypatch):
    """Redirect the sessions directories of the scan-reuse layer."""
    import modules.lazy_loop as lazy_loop
    import modules.scan_brief as scan_brief

    sessions_dir = tmp_path / "sessions"
    sessions_dir.mkdir()
    monkeypatch.setattr(lazy_loop, "SESSIONS_DIR", sessions_dir)
    monkeypatch.setattr(scan_brief, "SESSIONS_DIR", sessions_dir)
    return sessions_dir


@pytest.fixture()
def scan_xml(temp_sessions):
    target = "10.10.11.5"
    scan = temp_sessions / f"scan_{target}.nmap.xml"
    scan.write_text(
        """<nmaprun>
  <host>
    <address addr="10.10.11.5" addrtype="ipv4"/>
    <ports>
      <port protocol="tcp" portid="80">
        <state state="open"/>
        <service name="http" product="nginx" version="1.18.0"/>
      </port>
      <port protocol="tcp" portid="22">
        <state state="open"/>
        <service name="ssh" product="OpenSSH" version="8.2p1"/>
      </port>
    </ports>
  </host>
</nmaprun>""",
        encoding="utf-8",
    )
    return target


def test_fresh_scan_path_returns_recent_scan(scan_xml, temp_sessions):
    from modules.lazy_loop import _fresh_scan_path

    path = _fresh_scan_path(scan_xml, 21600)
    assert path.endswith("scan_10.10.11.5.nmap.xml")


def test_fresh_scan_path_rejects_stale_scan(scan_xml, temp_sessions):
    import os

    from modules.lazy_loop import _fresh_scan_path

    stale = time.time() - 90000
    os.utime(temp_sessions / f"scan_{scan_xml}.nmap.xml", (stale, stale))
    assert _fresh_scan_path(scan_xml, 21600) == ""
    assert _fresh_scan_path(scan_xml, 200000) != ""


def test_fresh_scan_path_empty_target():
    from modules.lazy_loop import _fresh_scan_path

    assert _fresh_scan_path("", 21600) == ""


def test_brief_built_from_scan(scan_xml, temp_sessions):
    from modules.scan_brief import build_brief, focus_summary, intents_from_brief

    brief = build_brief(scan_xml, temp_sessions)
    assert brief is not None
    assert brief["target"] == scan_xml
    services = brief["services"]
    assert {"port": 80, "service": "http", "product": "nginx"} in [
        {"port": row["port"], "service": row["service"], "product": row["product"]} for row in services
    ]
    assert focus_summary(brief).count("/") >= 2
    intents = intents_from_brief(brief)
    assert any("http" in text and "10.10.11.5:80" in text for text in intents)


def test_brief_write_and_reload(scan_xml, temp_sessions):
    from modules.scan_brief import brief_path_for, load_brief, write_brief

    path = write_brief(scan_xml, temp_sessions)
    assert path.endswith(f"loop_brief_{scan_xml}.yaml")
    loaded = load_brief(path)
    assert loaded and loaded["target"] == scan_xml
    assert brief_path_for(scan_xml, temp_sessions).exists()


def test_brief_degrades_without_scan(temp_sessions):
    from modules.scan_brief import build_brief, intents_from_brief

    assert build_brief("10.10.99.99", temp_sessions) is None
    assert intents_from_brief(None) == []
