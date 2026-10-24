"""Beacon recon ingest tests.

Contract — beacon ``discover:``/``portscan:`` payloads no longer stay
display-only: they fold into the world model (hosts, services, graph
relations), the ``hostsdiscovery.txt`` ledger, and one ``discovery``
outcome event that refreshes the intel and attack graph summaries.
"""

from __future__ import annotations

import json
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from modules.beacon_recon import (
    ingest_beacon_recon,
    parse_beacon_portscan,
    parse_discovered_ips,
)
from modules.outcome_bus import OutcomeBus
from modules.world_model import WorldModel


def _fresh_world_model(tmp: Path) -> WorldModel:
    return WorldModel(path=tmp / "world_model.json")


class ParseDiscoveredIpsSpec(unittest.TestCase):
    def test_flat_string(self) -> None:
        self.assertEqual(
            parse_discovered_ips("10.0.0.2 10.0.0.2, 10.0.0.5"),
            ["10.0.0.2", "10.0.0.5"],
        )

    def test_dict_with_list_values(self) -> None:
        self.assertEqual(parse_discovered_ips({"lan": ["10.0.0.3", "10.0.0.4"]}), ["10.0.0.3", "10.0.0.4"])

    def test_skips_non_ips(self) -> None:
        self.assertEqual(parse_discovered_ips("not-an-ip 10.0.0.7 ; foo bar"), ["10.0.0.7"])

    def test_empty_values(self) -> None:
        self.assertEqual(parse_discovered_ips(""), [])
        self.assertEqual(parse_discovered_ips(None), [])
        self.assertEqual(parse_discovered_ips({}), [])


class ParseBeaconPortscanSpec(unittest.TestCase):
    def test_flat_string_credits_default_host(self) -> None:
        pairs = parse_beacon_portscan("22,80", default_host="10.0.0.9")
        self.assertEqual(pairs, [("10.0.0.9", 22), ("10.0.0.9", 80)])

    def test_go_map_string(self) -> None:
        pairs = parse_beacon_portscan('{"10.0.0.2": [22, 80]}', default_host="10.0.0.9")
        self.assertEqual(pairs, [("10.0.0.2", 22), ("10.0.0.2", 80)])

    def test_dict_payload(self) -> None:
        pairs = parse_beacon_portscan({"10.0.0.2": [22], "link-local": "junk,70000"}, default_host="10.0.0.9")
        self.assertEqual(pairs, [("10.0.0.2", 22)])

    def test_noise_and_bounds(self) -> None:
        pairs = parse_beacon_portscan('{"10.0.0.2": [0, 70000, -1, "abc"]} ', default_host="10.0.0.9")
        self.assertEqual(pairs, [])

    def test_host_prefix_string(self) -> None:
        pairs = parse_beacon_portscan("10.0.0.4:22,80", default_host="10.0.0.9")
        self.assertEqual(pairs, [("10.0.0.4", 22), ("10.0.0.4", 80)])

    def test_empty_values(self) -> None:
        self.assertEqual(parse_beacon_portscan(""), [])
        self.assertEqual(parse_beacon_portscan(None, default_host="10.0.0.9"), [])


class IngestBeaconReconSpec(unittest.TestCase):
    def _run(
        self,
        tmp: Path,
        wm: WorldModel,
        discovered: object = "10.0.0.2 10.0.0.9",
        portscan: object = '{"10.0.0.2": [22, 80]}',
    ) -> dict:
        with (
            patch("modules.world_model.get_world_model", return_value=wm),
            patch("modules.outcome_bus.get_bus", return_value=OutcomeBus(ledger_path=tmp / "outcomes.jsonl")),
        ):
            return ingest_beacon_recon(
                primary_ip="10.0.0.9",
                discovered_ips=discovered,
                portscan=portscan,
                hostname="metasploitable",
                client_id="lin",
                sessions_dir=tmp,
            )

    def test_hosts_services_ledger_and_outcome(self) -> None:
        with TemporaryDirectory() as tmp:
            stats, wm = Path(tmp), _fresh_world_model(Path(tmp))
            result = self._run(stats, wm)
            self.assertEqual(result["hosts"], 1)
            self.assertEqual(result["services"], 2)
            self.assertIn("10.0.0.2", wm.get_hosts_summary())
            self.assertIn(22, wm.get_host("10.0.0.2").services)
            self.assertIn(80, wm.get_host("10.0.0.2").services)
            ledger = stats / "hostsdiscovery.txt"
            content = ledger.read_text(encoding="utf-8")
            self.assertEqual(len(content.splitlines()), 1)
            self.assertIn("10.0.0.2", content)
            outcomes = stats / "outcomes.jsonl"
            rows = [json.loads(line) for line in outcomes.read_text(encoding="utf-8").splitlines() if line.strip()]
            self.assertEqual(rows[-1]["event"]["kind"], "discovery")
            self.assertEqual(rows[-1]["event"]["target"], "10.0.0.9")

    def test_rerun_is_idempotent_for_hosts_and_services(self) -> None:
        with TemporaryDirectory() as tmp:
            stats, wm = Path(tmp), _fresh_world_model(Path(tmp))
            first = self._run(stats, wm)
            self.assertEqual(first["hosts"], 1)
            second = self._run(stats, wm)
            self.assertEqual(second["hosts"], 0)
            ledger = stats / "hostsdiscovery.txt"
            self.assertEqual(len(ledger.read_text(encoding="utf-8").splitlines()), 1)

    def test_noop_without_data_and_without_ip(self) -> None:
        with TemporaryDirectory() as tmp:
            wm = _fresh_world_model(Path(tmp))
            stats = self._run(Path(tmp), wm, "", "")
            self.assertEqual(stats["outcomes"], 0)
            self.assertEqual(ingest_beacon_recon(primary_ip="")["outcomes"], 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
