"""Contract tests for the AD lab gym (Docker Samba DC) matrix and capture."""

from __future__ import annotations

import unittest
from unittest.mock import patch

from modules import ad_gym, ctf_capture, gym_registry, lab_runtime

VECTOR_IDS = ("ad_ldap_enum", "ad_smb_shares", "ad_rid_cycling", "ad_samr_enum", "ad_default_creds")


class AdLabCatalogueSpec(unittest.TestCase):
    """Index/exploit/chain matrix consistency contract."""

    def test_matrix_validates(self):
        self.assertEqual(ad_gym.validate_matrix(), [])

    def test_summary_shape(self):
        summary = ad_gym.summary()
        self.assertEqual(summary["vulnerabilities"], len(VECTOR_IDS))
        self.assertIn("smb", summary["by_service"])
        self.assertEqual(summary["errors"], [])

    def test_all_vectors_resolve(self):
        for vector_id in VECTOR_IDS:
            entry = ad_gym.get(vector_id)
            self.assertIsNotNone(entry, vector_id)
            chain = ad_gym.chain_for(vector_id)
            self.assertIsNotNone(chain, vector_id)
            self.assertEqual(str(chain.defaults.get("exploit", "")), str(entry["exploit"]))
            spec = ad_gym.exploit_for(vector_id)
            self.assertIsNotNone(spec, vector_id)
            self.assertEqual(spec.id, entry["exploit"])

    def test_get_unknown_is_none(self):
        self.assertIsNone(ad_gym.get("nope_not_there"))


class AdLabCaptureSpec(unittest.TestCase):
    """Evidence checkers for the AD vectors."""

    def test_kerberos_ticket_checker_direct(self):
        evidence = ctf_capture._check_kerberos_ticket("$krb5tgs$23$*svc_sql*hashmaterial")
        self.assertIn("$krb5tgs$23$", evidence)
        self.assertNotIn("hashmaterial", evidence)

    def test_domain_enum_capture(self):
        record = ctf_capture.capture(
            "ad_ldap_enum",
            "10.0.0.9",
            output="sAMAccountName: svc_sql\n",
            sessions_dir=":",
            catalogue=ad_gym.get,
        )
        matched = [c["name"] for c in record["checks"] if c["matched"]]
        self.assertIn("domain_enum", matched)
        self.assertEqual(record["status"], "captured")

    def test_smb_shares_capture(self):
        record = ctf_capture.capture(
            "ad_smb_shares",
            "10.0.0.9",
            output="netlogon: Disk\n",
            sessions_dir=":",
            catalogue=ad_gym.get,
        )
        matched = [c["name"] for c in record["checks"] if c["matched"]]
        self.assertIn("smb_shares", matched)
        self.assertEqual(record["status"], "captured")

    def test_credentials_capture_for_default_creds(self):
        record = ctf_capture.capture(
            "ad_default_creds",
            "10.0.0.9",
            output="administrator:LazyOwnAd!Lab42\n",
            sessions_dir=":",
            catalogue=ad_gym.get,
        )
        matched = [c["name"] for c in record["checks"] if c["matched"]]
        self.assertIn("credentials", matched)
        self.assertEqual(record["status"], "captured")

    def test_samr_enum_capture(self):
        record = ctf_capture.capture(
            "ad_samr_enum",
            "10.0.0.9",
            output="user:[svc_sql] rid:[0x44f]\n",
            sessions_dir=":",
            catalogue=ad_gym.get,
        )
        matched = [c["name"] for c in record["checks"] if c["matched"]]
        self.assertIn("domain_enum", matched)
        self.assertEqual(record["status"], "captured")


class AdLabRuntimeSpec(unittest.TestCase):
    """Lab scenario and fixture-provisioning contract."""

    def test_scenario_targets_samba_image(self):
        info = lab_runtime.LAB_SCENARIOS["ad-lab"]
        self.assertEqual(info["image"], "nowsci/samba-domain:latest")
        self.assertEqual(info["env"]["DOMAIN"], lab_runtime.LAB_AD_DOMAIN)
        self.assertIn("DOMAINPASS", info["env"])
        self.assertEqual(info["ports"], {})  # container-IP attack path, no host port conflicts

    def test_start_rejects_unknown_scenario(self):
        result = lab_runtime.start("not-a-scenario")
        self.assertFalse(result["success"])
        self.assertIn("unknown scenario", result["error"])

    def test_ensure_ad_lab_probe_failure_is_quiet(self):
        completed = type("R", (), {"returncode": 1, "stdout": "", "stderr": ""})()
        with (
            patch.object(lab_runtime, "_docker", return_value=completed) as mock_docker,
            patch.object(lab_runtime.time, "sleep"),
            patch.object(lab_runtime.time, "monotonic", side_effect=[0.0, 1.0, 10_000.0]),
        ):
            lab_runtime._ensure_ad_lab("ad-lab", "lazyown-lab-ad-lab")
        self.assertEqual(mock_docker.call_count, 1)

    def test_ensure_ad_lab_creates_fixture_once(self):
        probe = type("R", (), {"returncode": 0, "stdout": "", "stderr": ""})()
        listing = type("R", (), {"returncode": 0, "stdout": "Administrator\nGuest\nkrbtgt\n", "stderr": ""})()

        def fake_docker(*args, **kwargs):
            return listing if args[:2] == ("exec", "samba-tool-args") or True and "user" in args and "list" in args else probe

        calls = []

        def fake_docker2(*args, **kwargs):
            calls.append(args)
            if "user" in args and "list" in args:
                return listing
            return probe

        with patch.object(lab_runtime, "_docker", side_effect=fake_docker2):
            lab_runtime._ensure_ad_lab("ad-lab", "lazyown-lab-ad-lab")
        joined = [" ".join(args) for args in calls]
        self.assertTrue(any("user create" in j for j in joined))
        self.assertTrue(any("spn add" in j for j in joined))

    def test_ensure_ad_lab_skips_existing_fixture(self):
        probe = type("R", (), {"returncode": 0, "stdout": "", "stderr": ""})()
        listing = type("R", (), {"returncode": 0, "stdout": "Administrator\nsvc_sql\n", "stderr": ""})()

        def fake_docker(*args, **kwargs):
            if "user" in args and "list" in args:
                return listing
            return probe

        calls = []

        def fake_docker2(*args, **kwargs):
            calls.append(args)
            return fake_docker(*args, **kwargs)

        with patch.object(lab_runtime, "_docker", side_effect=fake_docker2):
            lab_runtime._ensure_ad_lab("ad-lab", "lazyown-lab-ad-lab")
        joined = [" ".join(args) for args in calls]
        self.assertFalse(any("user create" in j for j in joined))

    def test_readiness_without_docker(self):
        with patch.object(lab_runtime, "docker_available", return_value=False):
            ready = ad_gym.readiness()
        self.assertFalse(ready["running"])
        self.assertEqual(ready["ip"], "")


class AdLabGymDefinitionsSpec(unittest.TestCase):
    """Gym registry wiring for the AD lab challenges."""

    def test_ad_lab_apt_definition_valid(self):
        rows = [row for row in gym_registry.scan_definitions() if row.get("id") == "ad_lab_apt"]
        self.assertEqual(len(rows), 1)
        self.assertTrue(rows[0]["valid"], rows[0].get("error"))
        self.assertEqual(rows[0]["scenario"], "ad-lab")

    def test_ad_domain_enum_definition_valid(self):
        rows = [row for row in gym_registry.scan_definitions() if row.get("id") == "ad_domain_enum"]
        self.assertEqual(len(rows), 1)
        self.assertTrue(rows[0]["valid"], rows[0].get("error"))
        self.assertEqual(rows[0]["chain"], "gym_ad_lab_samr_enum")


if __name__ == "__main__":
    unittest.main()
