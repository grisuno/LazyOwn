"""Contract tests for gym matrix runner and CTF capture."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from modules import ctf_capture, gym_matrix_runner


class CtfCaptureSpec(unittest.TestCase):
    """Capture verification and persistence contract."""

    def test_root_shell_capture(self):
        with tempfile.TemporaryDirectory() as tmp:
            record = ctf_capture.capture(
                "vsftpd_backdoor",
                "10.0.0.5",
                output="uid=0(root) gid=0(root)\n",
                sessions_dir=tmp,
            )
            self.assertEqual(record["status"], "captured")
            self.assertEqual(record["cve"], "CVE-2011-2523")
            matched = [check for check in record["checks"] if check["matched"]]
            self.assertEqual(matched[0]["name"], "root_shell")

    def test_failed_capture_without_evidence(self):
        with tempfile.TemporaryDirectory() as tmp:
            record = ctf_capture.capture(
                "ms2_smtp_user_enum",
                "10.0.0.5",
                output="VRFY root -> 252 root@local\n",
                sessions_dir=tmp,
            )
            self.assertEqual(record["status"], "failed")

    def test_unknown_vuln_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(ValueError):
                ctf_capture.capture("nope_not_there", "10.0.0.5", sessions_dir=tmp)

    def test_shadow_evidence_masked(self):
        with tempfile.TemporaryDirectory() as tmp:
            record = ctf_capture.capture(
                "vsftpd_backdoor",
                "10.0.0.5",
                output="root:$1$SALT$H4SH:0:0:99999:7:::\n",
                sessions_dir=tmp,
            )
            matched = [c for c in record["checks"] if c["matched"]]
            evidence = matched[0]["evidence"]
            self.assertIn("$MASKED", evidence)
            self.assertNotIn("H4SH", evidence)

    def test_load_artifact(self):
        with tempfile.TemporaryDirectory() as tmp:
            self.assertEqual(ctf_capture.summary(tmp)["total"], 0)


class GymMatrixRunnerSpec(unittest.TestCase):
    """Matrix ordering, execution, and capture contract."""

    def test_plan_ordered_by_severity(self):
        with tempfile.TemporaryDirectory():
            plan = gym_matrix_runner.plan_matrix("10.0.0.5", top_k=6)
            self.assertTrue(plan)
            ranks = [gym_matrix_runner.SEVERITY_ORDER[item["severity"]] for item in plan]
            self.assertEqual(ranks, sorted(ranks))

    def test_plan_isolates_only_filter(self):
        plan = gym_matrix_runner.plan_matrix("10.0.0.5", only=["vsftpd_backdoor"])
        self.assertEqual([item["vuln_id"] for item in plan], ["vsftpd_backdoor"])

    def test_plan_rejects_empty_target(self):
        with self.assertRaises(ValueError):
            gym_matrix_runner.plan_matrix("")

    def test_run_matrix_dry_run_writes_no_capture(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = gym_matrix_runner.run_matrix(
                "10.0.0.5",
                dry_run=True,
                sessions_dir=tmp,
                only=["vsftpd_backdoor"],
            )
            self.assertEqual(result["runs"][0]["capture"], "dry-run")
            self.assertFalse(result["runs"][0].get("run_id"))

    def test_run_matrix_executes_and_captures(self):
        def executor(cmd: str) -> str:
            return "uid=0(root) gid=0(root)\n" if "--id vsftpd_backdoor" in cmd else ""

        with tempfile.TemporaryDirectory() as tmp:
            result = gym_matrix_runner.run_matrix(
                "10.0.0.5",
                executor=executor,
                sessions_dir=tmp,
                only=["vsftpd_backdoor"],
            )
            run = result["runs"][0]
            self.assertEqual(run["status"], "ok")
            self.assertEqual(run["capture"], "captured")
            stored = ctf_capture.list_records(tmp)
            self.assertEqual(stored["vsftpd_backdoor"]["status"], "captured")
            matrix = gym_matrix_runner.load_matrix(tmp)
            self.assertEqual(matrix["stats"]["ok"], 1)

    def test_run_matrix_flags_missing_chain(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = gym_matrix_runner.run_matrix(
                "10.0.0.5",
                sessions_dir=tmp,
                only=[],  # full plan; every entry has a chain in the index
            )
            self.assertTrue(result["stats"]["total"] >= 40)


class ReportIntegrationSpec(unittest.TestCase):
    """CTF captures flow into the professional report."""

    def test_captured_findings_enter_report(self):
        from modules import professional_report as report_module
        from modules.professional_report import RedTeamReportGenerator

        with tempfile.TemporaryDirectory() as tmp:
            sessions = Path(tmp)
            ctf_capture.capture(
                "vsftpd_backdoor",
                "10.0.0.5",
                output="uid=0(root)\n",
                sessions_dir=sessions,
            )
            with patch.object(report_module, "SESSIONS_DIR", sessions):
                generator = RedTeamReportGenerator()
                data = generator.collect_data()
                self.assertEqual(len(data["ctf"]), 1)
                findings = generator.classify_findings(data)
                ctf_findings = [f for f in findings if "Captured attack path" in f.title]
                self.assertEqual(len(ctf_findings), 1)
                self.assertEqual(ctf_findings[0].cve_id, "CVE-2011-2523")
                self.assertEqual(ctf_findings[0].affected_hosts, ["10.0.0.5"])


if __name__ == "__main__":
    unittest.main()
