"""Contract tests for the deterministic golden-path solver."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from modules import golden_path
from modules.world_model import HostState


def _snapshot() -> dict:
    """Build a small deterministic world-model fixture.

    Returns:
        Snapshot dict with anchors, a vulnerabile host, and credentials.
    """
    return {
        "hosts": {
            "10.0.0.2": {"state": "owned"},
            "10.0.0.3": {"state": "scanned"},
            "10.0.0.4": {"state": "unscanned"},
            "10.0.0.5": {"state": "scanned"},
        },
        "credentials": [
            {"value": "msfadmin:msfadmin", "host": "10.0.0.4", "confirmed": True},
            {"value": "guest:guest", "host": "10.0.0.5", "confirmed": False},
        ],
        "vulnerabilities": [
            {"host": "10.0.0.3", "cve": "CVE-2011-2523", "severity": "critical", "description": "vsftpd backdoor"},
            {"host": "10.0.0.5", "cve": "", "severity": "high", "description": "smb rce"},
        ],
        "network_graph": {
            "relations": [
                {"source": "host:10.0.0.2", "target": "host:10.0.0.4", "relation": "discovered_by", "weight": 1.0},
                {"source": "shell:vsftpd", "target": "cred:msfadmin", "relation": "exposes_credential", "weight": 1.0},
                {"source": "cred:msfadmin", "target": "host:10.0.0.4", "relation": "may_authenticate_to", "weight": 1.0},
                {"source": "host:10.0.0.2", "target": "service:smb", "relation": "runs_service", "weight": 1.0},
            ]
        },
    }


class ResolvePathsSpec(unittest.TestCase):
    """Solver contract over the local fixture."""

    def test_anchor_excluded_from_targets(self):
        result = golden_path.resolve_paths(_snapshot())
        targets = [path["target"] for path in result["paths"]]
        self.assertNotIn("10.0.0.2", targets)
        self.assertEqual(result["sources"], ["10.0.0.2"])

    def test_critical_exploit_ranked_first_with_severity_cost(self):
        result = golden_path.resolve_paths(_snapshot())
        first = result["paths"][0]
        self.assertEqual(first["target"], "10.0.0.3")
        self.assertEqual(first["cost"], 1.0)
        self.assertEqual(first["steps"][0]["action"], "exploit")
        self.assertIn("CVE-2011-2523", first["steps"][0]["evidence"])

    def test_confirmed_credential_beats_unconfirmed(self):
        result = golden_path.resolve_paths(_snapshot())
        costs = {path["target"]: path["cost"] for path in result["paths"]}
        self.assertLess(costs["10.0.0.4"], costs["10.0.0.5"])

    def test_lateral_relation_via_anchor(self):
        result = golden_path.resolve_paths(_snapshot())
        path = next(p for p in result["paths"] if p["target"] == "10.0.0.4")
        self.assertEqual(path["steps"][0]["action"], "anchor")
        self.assertEqual(path["steps"][1]["action"], "lateral")

    def test_runs_service_edges_ignored(self):
        result = golden_path.resolve_paths(_snapshot())
        for path in result["paths"]:
            for step in path["steps"]:
                self.assertNotEqual(step["relation"], "runs_service")

    def test_deterministic_and_stable(self):
        first = golden_path.resolve_paths(_snapshot())
        second = golden_path.resolve_paths(_snapshot())
        first["generated_at"] = second["generated_at"] = ""
        self.assertEqual(first, second)


class ArtifactSpec(unittest.TestCase):
    """Persistence contract for sessions/attack_paths.json."""

    def test_build_writes_artifact_from_world_model(self):
        from modules.world_model import WorldModel

        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            sessions = base / "sessions"
            sessions.mkdir()
            wm = WorldModel(path=base / "world_model.json")
            wm.add_host("10.0.0.2")
            wm.advance_host("10.0.0.2", HostState.OWNED)
            result = golden_path.build(
                world_model_path=base / "world_model.json",
                sessions_dir=sessions,
            )
            artifact = sessions / golden_path.ARTIFACT_NAME
            self.assertTrue(artifact.exists())
            loaded = golden_path.load_artifact(sessions_dir=sessions)
            self.assertEqual(loaded["paths"], result["paths"])
            self.assertEqual(golden_path.load_artifact(base), {"paths": []})

    def test_load_artifact_tolerant_when_missing(self):
        with tempfile.TemporaryDirectory() as tmp:
            self.assertEqual(golden_path.load_artifact(tmp), {"paths": []})


class PushObjectivesSpec(unittest.TestCase):
    """Objective injection and deduplication contract."""

    def test_push_and_dedupe(self):
        from skills.lazyown_objective import ObjectiveStore

        with tempfile.TemporaryDirectory() as tmp:
            store_path = Path(tmp) / "objectives.jsonl"
            paths = golden_path.resolve_paths(_snapshot(), top_k=2)["paths"]
            injected = golden_path.push_objectives(paths, store_path=store_path)
            self.assertEqual(len(injected), 2)
            priority = {obj.priority for obj in injected}
            self.assertLessEqual(len(priority), 2)
            again = golden_path.push_objectives(paths, store_path=store_path)
            self.assertEqual(len(again), 2)
            store = ObjectiveStore(path=store_path)
            pending = store.list_pending(limit=20)
            self.assertEqual(len(pending), 2)
            for obj in pending:
                self.assertEqual(obj.source, "golden_path")
                self.assertTrue(obj.context.get("target"))

    def test_priority_bands(self):
        self.assertEqual(golden_path.priority_for(1.0), "critical")
        self.assertEqual(golden_path.priority_for(2.0), "high")
        self.assertEqual(golden_path.priority_for(5.0), "medium")
        self.assertEqual(golden_path.priority_for(9.0), "low")


if __name__ == "__main__":
    unittest.main()
