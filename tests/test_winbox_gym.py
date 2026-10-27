"""Contract tests for the WinBox gym catalogue, adapter and matrix runner."""

from __future__ import annotations

import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from modules import ctf_capture, gym_matrix_runner, gym_winbox_runner, winbox_gym


class WinboxCatalogueSpec(unittest.TestCase):
    """Index/exploit/chain matrix consistency contract."""

    def test_matrix_validates(self):
        self.assertEqual(winbox_gym.validate_matrix(), [])

    def test_summary_shape(self):
        summary = winbox_gym.summary()
        self.assertEqual(summary["vulnerabilities"], 5)
        self.assertIn("winbox-agent", summary["by_service"])
        self.assertEqual(summary["errors"], [])

    def test_get_returns_entry(self):
        entry = winbox_gym.get("winbox_system_exec")
        self.assertIsNotNone(entry)
        self.assertEqual(entry["exploit"], "winbox_system_exec")
        self.assertEqual(entry["chain"], "gym_winbox_system_exec")
        self.assertIsNone(winbox_gym.get("nope_not_there"))

    def test_chain_for_resolves(self):
        chain = winbox_gym.chain_for("winbox_smb_enum")
        self.assertIsNotNone(chain)
        self.assertEqual(chain.defaults.get("exploit"), "winbox_smb_enum")

    def test_exploit_for_resolves(self):
        spec = winbox_gym.exploit_for("winbox_system_exec")
        self.assertIsNotNone(spec)
        self.assertEqual(spec.id, "winbox_system_exec")
        self.assertIn("winbox", spec.requires_binaries)

    def test_gym_definitions_load(self):
        from modules.gym_registry import scan_definitions

        rows = [row for row in scan_definitions() if row.get("id", "").startswith("winbox")]
        self.assertEqual(len(rows), 4)
        for row in rows:
            self.assertTrue(row["valid"], row.get("error"))


class WinboxReadinessSpec(unittest.TestCase):
    """Readiness gating and safe CLI adapter contract."""

    def test_readiness_without_binary(self):
        with patch.object(winbox_gym.shutil, "which", return_value=None):
            status = winbox_gym.check_readiness({})
        self.assertFalse(status["ready"])
        self.assertEqual(status["binary"], "")
        self.assertFalse(status["vm_built"])
        self.assertIn("clone", status["setup"])

    def test_readiness_guest_os_fallback(self):
        with patch.object(winbox_gym.shutil, "which", return_value=None):
            status = winbox_gym.check_readiness({"winbox_os": "totally-wrong"})
        self.assertEqual(status["guest_os"], winbox_gym.DEFAULT_GUEST_OS)

    def test_run_cli_rejects_unknown_action(self):
        with self.assertRaises(ValueError):
            winbox_gym.run_cli(["selfdestruct", "-y"])

    def test_run_cli_rejects_empty(self):
        with self.assertRaises(ValueError):
            winbox_gym.run_cli([])

    def test_run_cli_rejects_bad_timeout(self):
        with self.assertRaises(ValueError):
            winbox_gym.run_cli(["status"], timeout="soon")

    def test_run_cli_missing_binary_is_guidance(self):
        with patch.object(winbox_gym.shutil, "which", return_value=None):
            result = winbox_gym.run_cli(["status"])
        self.assertFalse(result["ok"])
        self.assertIn("not installed", result["output"])

    def test_run_cli_uses_list_form(self):
        with tempfile.TemporaryDirectory() as tmp:
            fake = Path(tmp) / "winbox"
            fake.write_text("#!/bin/sh\nexit 0\n")
            fake.chmod(0o755)
            with patch.object(winbox_gym.shutil, "which", return_value=str(fake)):
                result = winbox_gym.run_cli(["exec", "whoami; rm -rf /"], timeout=10)
            self.assertTrue(result["ok"])
            self.assertEqual(result["code"], 0)

    def test_vm_status_missing_binary(self):
        with patch.object(winbox_gym.shutil, "which", return_value=None):
            self.assertEqual(winbox_gym.vm_status(), {})

    def test_status_parsing(self):
        with tempfile.TemporaryDirectory() as tmp:
            fake = Path(tmp) / "winbox"
            fake.write_text("#!/bin/sh\necho 'State: running'\necho 'IP: 192.168.122.50'\n")
            fake.chmod(0o755)
            with patch.object(winbox_gym.shutil, "which", return_value=str(fake)):
                vm = winbox_gym.vm_status()
            self.assertEqual(vm["state"], "running")
            self.assertEqual(vm["ip"], "192.168.122.50")

    def test_record_artifact_sanitised(self):
        with tempfile.TemporaryDirectory() as tmp:
            with patch.object(winbox_gym, "WINBOX_DIR", Path(tmp)):
                path = winbox_gym.record_artifact("exec/../../evil", "data")
            self.assertIsNotNone(path)
            self.assertEqual(path.parent, Path(tmp))
            self.assertEqual(path.suffix, ".log")

    def test_attack_readiness_reasons(self):
        with patch.object(winbox_gym.shutil, "which", return_value=None):
            attack = winbox_gym.attack_readiness({})
        self.assertFalse(attack["attackable"])
        self.assertIn("winbox binary missing", attack["reasons"])

    def test_ensure_installed_already_present(self):
        with patch.object(winbox_gym.shutil, "which", return_value="/usr/bin/winbox"):
            result = winbox_gym.ensure_installed({})
        self.assertTrue(result["success"])
        self.assertFalse(result["installed"])

    def test_ensure_installed_clone_and_pip(self):
        with tempfile.TemporaryDirectory() as tmp:
            clone = type("R", (), {"returncode": 0, "stdout": "", "stderr": ""})()
            install = type("R", (), {"returncode": 0, "stdout": "", "stderr": ""})()
            with (
                patch.object(winbox_gym.shutil, "which", return_value=None),
                patch.object(winbox_gym, "BASE_DIR", Path(tmp)),
                patch("core.safe_exec.safe_git_clone", return_value=clone) as mock_clone,
                patch("core.hardening.safe_subprocess_run", return_value=install) as mock_install,
            ):
                result = winbox_gym.ensure_installed({"winbox_install_path": str(Path(tmp) / "winbox")})
            self.assertFalse(result["success"])
            mock_clone.assert_called_once()
            mock_install.assert_called_once()

    def test_ensure_installed_clone_failure_is_guidance(self):
        with tempfile.TemporaryDirectory() as tmp:
            clone = type("R", (), {"returncode": 128, "stdout": "", "stderr": "fatal: repository not found"})()
            with (
                patch.object(winbox_gym.shutil, "which", return_value=None),
                patch.object(winbox_gym, "BASE_DIR", Path(tmp)),
                patch("core.safe_exec.safe_git_clone", return_value=clone),
            ):
                result = winbox_gym.ensure_installed({})
        self.assertFalse(result["success"])
        self.assertIn("git clone failed", result["message"])


class WinboxBootstrapSpec(unittest.TestCase):
    """One-command lab bootstrap: deps, ISO, build, up, resolve."""

    def test_ensure_prereqs_nothing_missing(self):
        with patch.object(winbox_gym.shutil, "which", return_value="/usr/bin/x"):
            result = winbox_gym.ensure_prereqs()
        self.assertTrue(result["success"])
        self.assertEqual(result["missing"], [])

    def test_ensure_prereqs_maps_binaries_to_packages(self):
        completed = type("R", (), {"returncode": 0, "stdout": "", "stderr": ""})()
        captured = {}
        installed = set()

        def fake_which(name):
            return "/usr/bin/x" if name in installed or name != "virtiofsd" else None

        def fake_run(argv, **kwargs):
            captured["argv"] = list(argv)
            installed.add("virtiofsd")
            return completed

        with (
            patch.object(winbox_gym.shutil, "which", fake_which),
            patch.object(os, "geteuid", return_value=0),
            patch("core.hardening.safe_subprocess_run", side_effect=fake_run),
        ):
            result = winbox_gym.ensure_prereqs()
        self.assertTrue(result["success"])
        self.assertEqual(captured["argv"], ["apt-get", "install", "-y", "virtiofsd"])

    def test_ensure_prereqs_sudo_non_interactive(self):
        completed = type("R", (), {"returncode": 1, "stdout": "", "stderr": "sudo: a password is required"})()
        captured = {}

        def fake_run(argv, **kwargs):
            captured["argv"] = list(argv)
            return completed

        with (
            patch.object(winbox_gym.shutil, "which", lambda name: None if name == "genisoimage" else "/usr/bin/x"),
            patch.object(os, "geteuid", return_value=1000),
            patch("core.hardening.safe_subprocess_run", side_effect=fake_run),
        ):
            result = winbox_gym.ensure_prereqs()
        self.assertFalse(result["success"])
        self.assertEqual(captured["argv"][:4], ["sudo", "-n", "apt-get", "install"])
        self.assertIn("sudo apt-get install -y", result["message"])

    def test_ensure_lab_ready_skips_build_when_vm_built(self):
        with tempfile.TemporaryDirectory() as tmp:
            fake = Path(tmp) / "winbox"
            fake.write_text("#!/bin/sh\necho 'State: running'\necho 'IP: 192.168.122.50'\n")
            fake.chmod(0o755)
            with (
                patch.object(winbox_gym.shutil, "which", return_value=str(fake)),
                patch.object(winbox_gym, "resolve_target", return_value="192.168.122.50") as mock_resolve,
                patch.object(winbox_gym, "ensure_installed", return_value={"success": True, "path": str(fake)}),
                patch.object(winbox_gym, "ensure_prereqs", return_value={"success": True, "missing": []}),
            ):
                result = winbox_gym.ensure_lab_ready({})
        self.assertTrue(result["success"])
        self.assertEqual(result["stage"], "ready")
        self.assertEqual(result["ip"], "192.168.122.50")
        mock_resolve.assert_called_once()
        self.assertNotIn("iso", result["stages"])
        self.assertNotIn("build", result["stages"])

    def test_ensure_lab_ready_runs_iso_and_build_when_unbuilt(self):
        with tempfile.TemporaryDirectory() as tmp:
            fake = Path(tmp) / "winbox"
            fake.write_text("#!/bin/sh\nexit 0\n")
            fake.chmod(0o755)
            calls = []

            def fake_run_cli(args, timeout=0):
                calls.append(args[0])
                return {"ok": True, "code": 0, "output": "done", "stderr": ""}

            with (
                patch.object(winbox_gym.shutil, "which", return_value=str(fake)),
                patch.object(winbox_gym, "vm_status", return_value={}),
                patch.object(winbox_gym, "run_cli", side_effect=fake_run_cli),
                patch.object(
                    winbox_gym, "ensure_vm_running", return_value={"success": True, "ip": "10.0.0.9", "message": "up"}
                ),
                patch.object(winbox_gym, "resolve_target", return_value="10.0.0.9"),
                patch.object(winbox_gym, "ensure_installed", return_value={"success": True, "path": str(fake)}),
                patch.object(winbox_gym, "ensure_prereqs", return_value={"success": True, "missing": []}),
            ):
                result = winbox_gym.ensure_lab_ready({})
        self.assertTrue(result["success"])
        self.assertEqual(result["ip"], "10.0.0.9")
        self.assertIn("iso", calls)
        self.assertIn("setup", calls)

    def test_ensure_lab_ready_fails_fast_on_install(self):
        with (
            patch.object(winbox_gym.shutil, "which", return_value=None),
            patch.object(winbox_gym, "ensure_installed", return_value={"success": False, "message": "clone failed"}),
        ):
            result = winbox_gym.ensure_lab_ready({})
        self.assertFalse(result["success"])
        self.assertEqual(result["stage"], "install")
        self.assertIn("clone failed", result["message"])

    def test_lazyaddon_install_command_covers_prereqs(self):
        import yaml

        addon = yaml.safe_load((Path(winbox_gym.BASE_DIR) / "lazyaddons" / "winbox.yaml").read_text())
        install_command = addon["tool"]["install_command"]
        self.assertIn("apt-get install -y", install_command)
        for package in ("qemu-system-x86", "virtiofsd", "libwin-hivex-perl"):
            self.assertIn(package, install_command)
        self.assertIn("pip install -e .", install_command)


class WinboxMatrixSpec(unittest.TestCase):
    """Matrix plan/run contract through the injected catalogue."""

    def test_plan_ordered_by_severity(self):
        plan = gym_winbox_runner.plan_matrix("10.0.0.9")
        self.assertTrue(plan)
        ranks = [gym_matrix_runner.SEVERITY_ORDER[item["severity"]] for item in plan]
        self.assertEqual(ranks, sorted(ranks))

    def test_plan_rejects_empty_target(self):
        with self.assertRaises(ValueError):
            gym_winbox_runner.plan_matrix("")

    def test_plan_only_filter(self):
        plan = gym_winbox_runner.plan_matrix("10.0.0.9", only=["winbox_smb_enum"])
        self.assertEqual([item["vuln_id"] for item in plan], ["winbox_smb_enum"])

    def test_run_matrix_dry_run(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = gym_winbox_runner.run_matrix("10.0.0.9", dry_run=True, sessions_dir=tmp)
            self.assertEqual(result["target"], "10.0.0.9")
            self.assertEqual(len(result["runs"]), 5)
            for run in result["runs"]:
                self.assertEqual(run["capture"], "dry-run")

    def test_run_matrix_requires_vm_when_live(self):
        with patch.object(
            gym_winbox_runner.winbox_gym, "ensure_lab_ready", return_value={"success": False, "message": "VM off"}
        ):
            result = gym_winbox_runner.run_matrix("10.0.0.9", ensure_vm=True)
        self.assertIn("error", result)
        self.assertEqual(result["runs"], [])

    def test_capture_windows_os_enum(self):
        catalogue = winbox_gym.get
        with tempfile.TemporaryDirectory() as tmp:
            record = ctf_capture.capture(
                "winbox_smb_enum",
                "10.0.0.9",
                output="OS: Windows Server 2022 Standard 20348\n",
                sessions_dir=tmp,
                catalogue=catalogue,
            )
            matched = [c["name"] for c in record["checks"] if c["matched"]]
            self.assertIn("windows_os_enum", matched)
            self.assertEqual(record["status"], "captured")

    def test_capture_system_exec(self):
        with tempfile.TemporaryDirectory() as tmp:
            record = ctf_capture.capture(
                "winbox_system_exec",
                "10.0.0.9",
                output="nt authority\\system\n",
                sessions_dir=tmp,
                catalogue=winbox_gym.get,
            )
            self.assertEqual(record["status"], "captured")

    def test_capture_defense_report(self):
        with tempfile.TemporaryDirectory() as tmp:
            record = ctf_capture.capture(
                "winbox_defender_posture",
                "10.0.0.9",
                output="RealTimeProtectionEnabled : True\n",
                sessions_dir=tmp,
                catalogue=winbox_gym.get,
            )
            self.assertEqual(record["status"], "captured")

    def test_capture_eventlog_rows(self):
        with tempfile.TemporaryDirectory() as tmp:
            record = ctf_capture.capture(
                "winbox_eventlogs_evidence",
                "10.0.0.9",
                output="Time,Log,Level,Id,Provider,Message\n2026-01-01,Security,Information,4624,Microsoft-Windows-Security-Auditing,x\n",
                sessions_dir=tmp,
                catalogue=winbox_gym.get,
            )
            self.assertEqual(record["status"], "captured")

    def test_metasploitable_capture_unchanged(self):
        with tempfile.TemporaryDirectory() as tmp:
            record = ctf_capture.capture(
                "vsftpd_backdoor",
                "10.0.0.5",
                output="uid=0(root) gid=0(root)\n",
                sessions_dir=tmp,
            )
            self.assertEqual(record["status"], "captured")
            self.assertEqual(record["cve"], "CVE-2011-2523")


if __name__ == "__main__":
    unittest.main()
