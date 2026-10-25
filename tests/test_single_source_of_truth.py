"""Single-source-of-truth contract tests.

Contract 1 — ``KillChain.advance_phase`` is the only writer of phase
keys in ``world_model.json``. Consumers (``cli.lazynmap_post``) must
delegate to it.
Contract 2 — ``UnifiedStateManager._sync_world_model_cache`` merges
into the campaign world model (never truncates ``network_graph``,
phase keys, or campaign-only host fields).
Contract 3 — ``policy_facts.json`` is host-keyed; every consumer uses
``modules.factsio`` and therefore ingests real on-disk facts instead
of silently reading zero records.
"""

from __future__ import annotations

import json
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from modules.factsio import canonical_policy_facts, iter_flat_facts, load_policy_facts
from modules.killchain import KillChain
from modules.world_model import HostEntry, read_state_dict


def _write(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2), encoding="utf-8")


class AdvancePhaseSingleWriterSpec(unittest.TestCase):
    """The canonical phase writer preserves unknown keys and extras."""

    def test_extras_and_unknown_keys_are_preserved(self) -> None:
        with TemporaryDirectory() as tmp:
            wm = Path(tmp) / "world_model.json"
            _write(wm, {"network_graph": {"nodes": ["10.0.0.1"], "relations": []}, "phase": "recon"})
            ok = KillChain.advance_phase(
                "enum",
                world_model_path=wm,
                host="",
                extras={"target": "10.0.0.1", "phase_updated_at": 1700000000.0},
            )
            self.assertTrue(ok)
            raw = read_state_dict(wm)
            self.assertEqual(raw["current_phase"], "enum")
            self.assertEqual(raw["phase"], "enum")
            self.assertEqual(
                raw["network_graph"],
                {"nodes": ["10.0.0.1"], "relations": []},
            )
            self.assertEqual(raw["target"], "10.0.0.1")
            self.assertEqual(raw["phase_updated_at"], 1700000000.0)
            self.assertIn("scan", raw.get("completed_phases", []))

    def test_extras_reapplied_after_host_advance(self) -> None:
        with TemporaryDirectory() as tmp:
            wm = Path(tmp) / "world_model.json"
            _write(
                wm,
                {
                    "phase": "recon",
                    "hosts": {
                        "10.0.0.1": {
                            "ip": "10.0.0.1",
                            "state": "scanned",
                            "os_hint": "",
                            "services": {},
                            "notes": [],
                            "cloud_metadata": {},
                            "last_updated": "",
                        }
                    },
                },
            )
            ok = KillChain.advance_phase(
                "enum",
                world_model_path=wm,
                host="10.0.0.1",
                extras={"target": "10.0.0.1", "phase_updated_at": 1700000000.0},
            )
            self.assertTrue(ok)
            raw = read_state_dict(wm)
            self.assertEqual(raw["current_phase"], "enum")
            self.assertEqual(raw["target"], "10.0.0.1")
            self.assertEqual(raw["phase_updated_at"], 1700000000.0)
            self.assertEqual(raw["hosts"]["10.0.0.1"]["state"], "enumerated")

    def test_invalid_phase_leaves_file_untouched(self) -> None:
        with TemporaryDirectory() as tmp:
            wm = Path(tmp) / "world_model.json"
            _write(wm, {"campaign_id": "keep"})
            ok = KillChain.advance_phase("not_a_phase", world_model_path=wm)
            self.assertFalse(ok)
            raw = read_state_dict(wm)
            self.assertEqual(raw, {"campaign_id": "keep"})


class LazynmapPostSingleWriterSpec(unittest.TestCase):
    """Post-scan phase bump goes through KillChain and preserves state."""

    def test_post_scan_bumps_phase_via_killchain(self) -> None:
        from cli.lazynmap_post import PostScanConfig
        from cli.lazynmap_post import run_post_scan

        with TemporaryDirectory() as tmp:
            sessions = Path(tmp) / "sessions"
            sessions.mkdir()
            _write(sessions / "world_model.json", {"campaign_id": "abc"})
            result = run_post_scan(
                target="10.10.10.5",
                payload={"enable_recon_plan": False, "rhost": "10.10.10.5"},
                config=PostScanConfig(sessions_dir=str(sessions)),
            )
            self.assertTrue(result.skipped)
            _write(
                sessions / "world_model.json",
                {"campaign_id": "abc", "phase": "recon"},
            )
            result = run_post_scan(
                target="10.10.10.5",
                payload={"rhost": "10.10.10.5"},
                config=PostScanConfig(sessions_dir=str(sessions)),
            )
            self.assertFalse(result.skipped)
            self.assertTrue(result.world_model_updated)
            raw = json.loads((sessions / "world_model.json").read_text(encoding="utf-8"))
            self.assertEqual(raw["campaign_id"], "abc")
            self.assertEqual(raw["phase"], "enum")
            self.assertEqual(raw["current_phase"], "enum")
            self.assertEqual(raw["target"], "10.10.10.5")
            self.assertIn("phase_updated_at", raw)


class StateManagerMergeSpec(unittest.TestCase):
    """The DB cache sync merges into the campaign world model."""

    def _make_manager(self, tmp: Path):
        from modules.state_manager import StateManager

        sessions = tmp / "sessions"
        sessions.mkdir(parents=True, exist_ok=True)
        wm_path = sessions / "world_model.json"
        mgr = StateManager(
            db_path=tmp / "db.sqlite",
            sessions_dir=sessions,
            world_model_path=wm_path,
        )
        return mgr, wm_path

    def test_sync_preserves_network_graph_and_campaign_fields(self) -> None:
        with TemporaryDirectory() as tmp:
            mgr, wm_path = self._make_manager(Path(tmp))
            prior = {
                "phase": "enum",
                "current_phase": "enum",
                "network_graph": {"nodes": ["10.0.0.1"], "relations": []},
                "hosts": {
                    "10.0.0.1": {
                        "ip": "10.0.0.1",
                        "state": "owned",
                        "os_hint": "linux",
                        "notes": ["foothold via vsftpd"],
                        "services": {"6200": {"port": 6200, "protocol": "tcp", "name": "shell"}},
                    }
                },
                "credentials": [{"value": "root:pwd", "host": "10.0.0.1", "confirmed": True}],
            }
            _write(wm_path, prior)

            mgr.add_host("10.0.0.1")
            mgr.add_service("10.0.0.1", 80, "http")
            mgr.add_credential("10.0.0.1", "msfadmin", "msfadmin")
            mgr._sync_world_model_cache()

            merged = read_state_dict(wm_path)
            self.assertEqual(merged["phase"], "enum")
            self.assertEqual(merged["current_phase"], "enum")
            self.assertEqual(merged["network_graph"]["nodes"], ["10.0.0.1"])
            host_entry = merged["hosts"]["10.0.0.1"]
            self.assertEqual(host_entry["state"], "owned")
            self.assertEqual(host_entry["os_hint"], "linux")
            self.assertEqual(host_entry["notes"], ["foothold via vsftpd"])
            self.assertIn("6200", {str(p) for p in host_entry["services"]})
            self.assertIn("80", {str(p) for p in host_entry["services"]})
            cred_values = {c["value"] for c in merged["credentials"]}
            self.assertIn("root:pwd", cred_values)
            self.assertIn("msfadmin:msfadmin", cred_values)
            service_entry = host_entry["services"]["80"]
            self.assertEqual(
                set(service_entry.keys()),
                {"port", "protocol", "name", "version", "state"},
            )
            h = HostEntry.from_dict(host_entry)
            self.assertEqual(int(h.services[80].port), 80)
            self.assertEqual(h.state.value, "owned")


class FactsIoCanonicalSpec(unittest.TestCase):
    """factsio resolves both shapes to host-keyed canonical records."""

    CANONICAL = {
        "10.0.0.9": {
            "services": [
                {
                    "host": "10.0.0.9",
                    "port": 21,
                    "protocol": "tcp",
                    "service": "vsftpd",
                    "product": "vsftpd 2.3.4",
                    "version": "2.3.4",
                    "state": "open",
                }
            ],
            "credentials": [
                {
                    "host": "10.0.0.9",
                    "username": "root",
                    "password": "toor",
                    "source_file": "x.txt",
                    "hash_value": "",
                    "hash_type": "",
                }
            ],
            "vulnerabilities": [
                {
                    "host": "10.0.0.9",
                    "vuln_id": "CVE-2011-2523",
                    "severity": "critical",
                    "title": "vsftpd backdoor",
                    "url": "",
                    "source_tool": "nuclei",
                    "source_file": "y.txt",
                }
            ],
            "os_hint": "linux",
        }
    }

    def test_canonical_passes_through(self) -> None:
        self.assertEqual(canonical_policy_facts(self.CANONICAL), self.CANONICAL)

    def test_legacy_wrapped_shape_resolves(self) -> None:
        legacy = {
            "hosts": {"10.1.1.1": {"services": [{"port": 22, "name": "ssh"}]}},
            "credentials": [{"value": "admin:realpass", "host": "10.1.1.1"}],
        }
        host_keyed = canonical_policy_facts(legacy)
        self.assertIn("10.1.1.1", host_keyed)

    def test_flat_records_derive_observables(self) -> None:
        records = list(iter_flat_facts(self.CANONICAL))
        types = [r["type"] for r in records]
        self.assertEqual(types.count("service"), 1)
        self.assertEqual(types.count("credential"), 1)
        self.assertEqual(types.count("vulnerability"), 1)
        cred = next(r for r in records if r["type"] == "credential")
        self.assertEqual(cred["observable"], "root:toor")
        vuln = next(r for r in records if r["type"] == "vulnerability")
        self.assertEqual(vuln["observable"], "CVE-2011-2523")
        svc = next(r for r in records if r["type"] == "service")
        self.assertEqual(svc["observable"], "vsftpd")

    def test_load_reads_real_file(self) -> None:
        with TemporaryDirectory() as tmp:
            path = Path(tmp) / "policy_facts.json"
            _write(path, self.CANONICAL)
            self.assertEqual(load_policy_facts(path), self.CANONICAL)


class ConsumePolicyFactsSpec(unittest.TestCase):
    """WorldModel ingests canonical host-keyed facts (was zero before)."""

    def test_consume_ingests_real_shape(self) -> None:
        from modules.world_model import WorldModel

        with TemporaryDirectory() as tmp:
            facts_path = Path(tmp) / "policy_facts.json"
            _write(
                facts_path,
                {
                    "10.1.1.5": {
                        "services": [
                            {"port": 21, "name": "vsftpd", "protocol": "tcp"}
                        ],
                        "os_hint": "linux",
                        "credentials": [
                            {"username": "root", "password": "toor", "hash_value": ""}
                        ],
                        "vulnerabilities": [
                            {"vuln_id": "CVE-2011-2523", "severity": "critical", "title": "vsftpd"}
                        ],
                    }
                },
            )
            wm = WorldModel(path=Path(tmp) / "world_model.json")
            ingested = wm.consume_policy_facts(facts_path)
            self.assertGreaterEqual(ingested, 3)
            summary = wm.get_hosts_summary()
            self.assertIn("10.1.1.5", summary)


class IntelligenceFactstoreSpec(unittest.TestCase):
    """collect_from_factstore ingests services, creds and vulns."""

    def test_collects_creds_and_vulns_from_canonical(self) -> None:
        from modules.intelligence_engine import IntelligenceConfig
        from modules.intelligence_engine import IntelligenceEngine

        with TemporaryDirectory() as tmp:
            facts_path = Path(tmp) / "policy_facts.json"
            _write(
                facts_path,
                {
                    "10.2.2.5": {
                        "services": [{"port": 21, "service": "vsftpd", "protocol": "tcp"}],
                        "credentials": [{"username": "msfadmin", "password": "msfadmin"}],
                        "vulnerabilities": [
                            {"vuln_id": "CVE-2011-2523", "severity": "critical", "title": "vsftpd"}
                        ],
                    }
                },
            )
            engine = IntelligenceEngine(IntelligenceConfig(sessions_dir=Path(tmp)))
            facts = engine.collect_from_factstore()
            types = [f.fact_type for f in facts]
            self.assertIn("service", types)
            self.assertIn("credential", types)
            self.assertIn("vulnerability", types)
            cred = next(f for f in facts if f.fact_type == "credential")
            self.assertEqual(cred.value, "msfadmin:msfadmin")
            self.assertEqual(cred.host, "10.2.2.5")


class ComplianceFactsSpec(unittest.TestCase):
    """Compliance findings derive from canonical host-keyed facts."""

    def test_findings_from_canonical(self) -> None:
        from modules.compliance import ComplianceEngine

        with TemporaryDirectory() as tmp:
            _write(
                Path(tmp) / "policy_facts.json",
                {
                    "10.3.3.5": {
                        "services": [{"port": 21, "service": "vsftpd", "protocol": "tcp"}],
                        "credentials": [{"username": "root", "password": "toor"}],
                        "vulnerabilities": [
                            {"vuln_id": "CVE-2011-2523", "severity": "critical", "title": "vsftpd"}
                        ],
                    }
                },
            )
            engine = ComplianceEngine(sessions_dir=Path(tmp))
            findings = engine._load_findings()
            categories = {f.category for f in findings if f.category in ("service", "credential", "vulnerability")}
            self.assertEqual(categories, {"service", "credential", "vulnerability"})
            vuln = next(f for f in findings if f.category == "vulnerability")
            self.assertEqual(vuln.severity, "CRITICAL")
            self.assertIn("CVE-2011-2523", vuln.description)


class MispFactRecordsSpec(unittest.TestCase):
    """MISP importer recognises FactStore fact records."""

    def test_fact_records_produce_findings(self) -> None:
        from modules.integrations.misp_export import MISPExporter

        self.assertEqual(len(MISPExporter._dict_to_findings(_host_map_facts())), 3)

    def test_cve_record(self) -> None:
        from modules.integrations.misp_export import MISPExporter

        findings = MISPExporter._dict_to_findings(
            {"vuln_id": "CVE-2011-2523", "severity": "critical", "title": "vsftpd", "host": "10.0.0.9"}
        )
        self.assertEqual(findings[0].type, "cve")
        self.assertEqual(findings[0].value, "CVE-2011-2523")
        self.assertEqual(findings[0].host, "10.0.0.9")

    def test_host_map_resolves_nested_records(self) -> None:
        from modules.integrations.misp_export import MISPExporter

        findings = MISPExporter._dict_to_findings(
            {
                "10.0.0.9": {
                    "services": [{"port": 21, "service": "vsftpd", "protocol": "tcp"}],
                    "credentials": [{"username": "root", "password": "toor"}],
                    "vulnerabilities": [{"vuln_id": "CVE-2011-2523"}],
                }
            }
        )
        values = {(f.type, f.value) for f in findings}
        self.assertIn(("service", "vsftpd"), values)
        self.assertIn(("credential", "root:toor"), values)
        self.assertIn(("cve", "CVE-2011-2523"), values)


def _host_map_facts() -> dict:
    return {
        "10.0.0.9": {
            "services": [{"port": 21, "service": "vsftpd", "protocol": "tcp"}],
            "credentials": [{"username": "root", "password": "toor"}],
            "vulnerabilities": [{"vuln_id": "CVE-2011-2523"}],
        }
    }


if __name__ == "__main__":
    unittest.main(verbosity=2)
