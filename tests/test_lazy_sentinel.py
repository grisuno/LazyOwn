"""BDD tests for the internal sentinel contract."""

from __future__ import annotations

import shlex

from modules import lazy_sentinel
from modules.lazy_feedmatch import Sighting

GREPABLE = "Host: 10.66.44.9 () Status: Up\n"
GREPABLE_PORTS = (
    "Host: 10.66.44.9 () Ports: 22/open/tcp//ssh//OpenSSH 9.6p1/, 8080/open/tcp//http//Apache Tomcat 9.0.45/\n"
)
TSV = "10.66.44.9\t6379\tredis\t7.4.1\n"


class TestRangeGuards:
    def test_private_bounded_range_ok(self):
        story = "a /28 lab subnet is accepted"
        assert lazy_sentinel.validate_ranges(["10.66.44.0/28"]) == [], story

    def test_public_range_rejected(self):
        story = "public ranges never ride the sentinel"
        assert any("not a private range" in item for item in lazy_sentinel.validate_ranges(["8.8.8.0/24"])), story

    def test_wide_range_rejected(self):
        story = "ranges wider than the host cap are rejected"
        assert any("wider than" in item for item in lazy_sentinel.validate_ranges(["10.0.0.0/8"])), story

    def test_loopback_rejected(self):
        story = "loopback is never scanned by sentinel"
        assert any("loopback" in item for item in lazy_sentinel.validate_ranges(["127.0.0.1/32"])), story

    def test_invalid_cidr_rejected(self):
        story = "garbage cidr fails loudly"
        assert any("invalid CIDR" in item for item in lazy_sentinel.validate_ranges(["banana"])), story

    def test_too_many_ranges(self):
        story = "more ranges than the cap is one error"
        errors = lazy_sentinel.validate_ranges([f"10.0.{i}.0/24" for i in range(10)])
        assert any("more than" in item for item in errors), story


class TestProvision:
    def test_blob_contains_sweep_and_marker(self, tmp_path):
        story = "the blob sweeps the range and prints the done marker"
        blob = lazy_sentinel.provision_blob(["10.66.44.0/28"], spool_dir=tmp_path)
        assert blob["errors"] == [], story
        assert "nmap -Pn -sV" in blob["script"], story
        assert "SENTINEL_DONE" in blob["script"], story
        assert shlex.quote("10.66.44.0/28") in blob["script"] or "10.66.44.0/28" in blob["script"], story

    def test_failed_ranges_give_empty_blob(self, tmp_path):
        story = "a guarded range yields an errors-only result"
        blob = lazy_sentinel.provision_blob(["8.8.8.0/24"], spool_dir=tmp_path)
        assert blob["id"] == "" and blob["errors"], story

    def test_record_kept_in_spool_dir(self, tmp_path):
        story = "provision stores the blob record next to the spool dir"
        blob = lazy_sentinel.provision_blob(["10.66.44.0/28"], spool_dir=tmp_path)
        assert (tmp_path / f"provision_{blob['id']}.json").exists(), story


class TestDispatch:
    def test_c2_exec_line(self, tmp_path):
        story = "the dispatch line embeds the blob shell-quoted"
        blob = lazy_sentinel.provision_blob(["10.66.44.0/28"], spool_dir=tmp_path)
        line = lazy_sentinel.dispatch_line("beaconX", blob)
        assert line.startswith("c2_exec beaconX sh -c "), story
        assert shlex.split(line)[2:] == ["sh", "-c", blob["script"]], story

    def test_dispatch_needs_input(self):
        story = "empty client or blob raises"
        import pytest

        with pytest.raises(ValueError):
            lazy_sentinel.dispatch_line("", {})
        with pytest.raises(ValueError):
            lazy_sentinel.dispatch_line("beaconX", {"script": ""})


class TestIngest:
    def test_grepable_parse(self, tmp_path):
        story = "nmap -oG output parses into sightings with products and versions"
        spool = tmp_path / "spool.gmap"
        spool.write_text(GREPABLE + GREPABLE_PORTS, encoding="utf-8")
        parsed = lazy_sentinel.ingest_spool(spool)
        services = parsed["hosts"][0]["services"]
        ports = sorted(svc["port"] for svc in services)
        assert ports == [22, 8080], story
        tomcat = next(svc for svc in services if svc["port"] == 8080)
        assert tomcat["product"] == "Apache Tomcat" and tomcat["version"] == "9.0.45", story

    def test_tsv_fallback_parse(self, tmp_path):
        story = "plain tsv rows parse too"
        spool = tmp_path / "spool.txt"
        spool.write_text(TSV, encoding="utf-8")
        parsed = lazy_sentinel.ingest_spool(spool)
        sweep = parsed["sightings"][0]
        assert sweep.product == "redis" and sweep.version == "7.4.1", story

    def test_missing_file_degrades(self, tmp_path):
        story = "an unreadable spool yields empty results"
        parsed = lazy_sentinel.ingest_spool(tmp_path / "none")
        assert parsed == {"hosts": [], "sightings": []}, story

    def test_sightings_roundtrip(self, tmp_path):
        story = "save/load sightings roundtrip preserves rows"
        rows = [Sighting(host="10.66.44.9", port=22, product="OpenSSH", version="9.6p1")]
        out = lazy_sentinel.save_sightings(rows, tmp_path / "s.json")
        back = lazy_sentinel.load_sightings(out)
        assert back[0].product == "OpenSSH" and back[0].port == 22, story
