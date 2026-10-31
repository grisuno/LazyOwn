"""BDD tests for the host-reported inventory contract."""

from __future__ import annotations

from modules import lazy_feedmatch, lazy_inventory

LINUX_CAPTURE = """
#LAZYINVENTORY linux
6.8.0
openssh-server	9.6p1
redis	7.4.1
nginx==1.27.0
LAZYINVENTORY_DONE
ps -ef
"""

WINDOWS_CAPTURE = """
#LAZYINVENTORY windows
OpenSSH for Windows	9.5.0.0
Ruby 3.1	3.1.2.1
LAZYINVENTORY_DONE
"""


class TestBlobs:
    def test_linux_blob_read_only(self):
        story = "the linux blob only queries, never installs or writes outside /tmp"
        blob = lazy_inventory.inventory_blob("linux")
        assert "dpkg-query -W" in blob and "rpm -qa" in blob and "apk info" in blob, story

    def test_windows_blob_read_only(self):
        story = "the windows blob reads the uninstall registry only"
        blob = lazy_inventory.inventory_blob("windows")
        assert "Uninstall" in blob and "Get-ItemProperty" in blob, story
        assert "Set-ItemProperty" not in blob and "Start-Process" not in blob, story

    def test_unknown_platform_empty(self):
        story = "an unknown platform yields no blob"
        assert lazy_inventory.inventory_blob("templeos") == "", story


class TestParse:
    def test_linux_parse(self):
        story = "linux tsv and freeze lines parse; the done marker cuts tail noise"
        entries = lazy_inventory.parse_blob_output(LINUX_CAPTURE, "linux")
        pairs = {item["product"]: item["version"] for item in entries}
        assert pairs.get("openssh-server") == "9.6p1", story
        assert pairs.get("nginx") == "1.27.0", story
        assert "ps -ef" not in str(pairs), story

    def test_windows_parse(self):
        story = "registry display rows parse with the platform tag"
        entries = lazy_inventory.parse_blob_output(WINDOWS_CAPTURE, "windows")
        assert any(item.get("product") == "ruby 3.1" for item in entries), story
        assert all(item.get("source") == "host" for item in entries), story

    def test_source_is_host(self):
        story = "every parsed entry reports the host source"
        entries = lazy_inventory.parse_blob_output(LINUX_CAPTURE, "linux")
        assert all(item["source"] == "host" for item in entries), story


class TestPromotion:
    def test_to_sightings(self):
        story = "entries become host-source sightings without ports"
        entries = lazy_inventory.parse_blob_output(LINUX_CAPTURE, "linux")
        rows = lazy_inventory.to_sightings(entries)
        assert rows[0].source == "host" and rows[0].port == 0, story

    def test_host_source_fills_missing_lead(self):
        story = "a host-reported version promotes a lead into a match the feed can bind"
        feed = lazy_feedmatch.parse_feed([
            {"cve_id": "CVE-2025-2001", "product": "redis", "cvss": 9.8, "kev": True,
             "ranges": [{"introduced": "7.0.0", "fixed": "7.4.2"}]},
        ])
        banner = lazy_feedmatch.Sighting(host="10.66.44.7", port=6379, product="", version="")
        package = lazy_feedmatch.Sighting(host="10.66.44.7", port=0, product="redis", version="7.4.1", source="host")
        assert lazy_feedmatch.bind_sighting(banner, feed) == [], story
        bindings = lazy_feedmatch.bind_sighting(package, feed)
        assert bindings[0].evidence == lazy_feedmatch.EVIDENCE_IN_RANGE, story
        assert bindings[0].source == "host", story

    def test_platform_of(self):
        story = "the entries' own os tag reports the platform"
        entries = lazy_inventory.parse_blob_output(WINDOWS_CAPTURE, "windows")
        assert lazy_inventory.os_platform_of(entries) == "windows", story
