"""tests/test_doctor.py

Tests for the preflight environment health check in ``cli.doctor``.

The doctor command is the operator's first line of defence against a broken
install, so the contract under test is:

- Every check function is pure and side-effect free: dependency probing is
  injected, never executed against the real environment.
- Required dependencies map to ``fail``; optional ones map to ``warn``; present
  ones map to ``ok``.
- File-presence checks (payload.json, certificates) resolve against an injected
  repository root so the suite never depends on the real working tree.
- :class:`DoctorReport` aggregates the worst status correctly and exposes a
  ``healthy`` flag that ignores warnings but trips on failures.
- SecLists and external-tool detection are delegated to ``cli.wizard`` so the
  framework keeps a single source of truth.
"""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from cli import doctor  # noqa: E402
from cli.wizard import BinarySpec, BinaryStatus  # noqa: E402


class TestPythonVersion:
    def test_supported_version_is_ok(self):
        result = doctor.check_python_version((3, 11, 0))
        assert result.status == doctor.STATUS_OK

    def test_exact_minimum_is_ok(self):
        result = doctor.check_python_version(doctor.MIN_PYTHON_VERSION)
        assert result.status == doctor.STATUS_OK

    def test_old_version_fails(self):
        result = doctor.check_python_version((3, 8, 10))
        assert result.status == doctor.STATUS_FAIL
        assert result.hint

    def test_uses_live_interpreter_by_default(self):
        result = doctor.check_python_version()
        assert result.status == doctor.STATUS_OK


class TestVirtualEnv:
    def test_active_venv_is_ok(self, tmp_path):
        result = doctor.check_virtualenv(
            prefix="/repo/env", base_prefix="/usr", root=tmp_path
        )
        assert result.status == doctor.STATUS_OK

    def test_inactive_with_env_dir_warns_to_activate(self, tmp_path):
        (tmp_path / "env").mkdir()
        result = doctor.check_virtualenv(
            prefix="/usr", base_prefix="/usr", root=tmp_path
        )
        assert result.status == doctor.STATUS_WARN
        assert "activate" in result.hint

    def test_no_venv_anywhere_warns_to_install(self, tmp_path):
        result = doctor.check_virtualenv(
            prefix="/usr", base_prefix="/usr", root=tmp_path
        )
        assert result.status == doctor.STATUS_WARN
        assert "install.sh" in result.hint

    def test_none_base_prefix_collapses_to_prefix(self, tmp_path):
        result = doctor.check_virtualenv(
            prefix="/usr", base_prefix=None, root=tmp_path
        )
        assert result.status == doctor.STATUS_WARN


class TestPackages:
    def test_present_required_package_is_ok(self):
        specs = (doctor.PackageSpec("os", "os", "stdlib", True),)
        results = doctor.check_packages(specs, finder=lambda name: object())
        assert results[0].status == doctor.STATUS_OK

    def test_missing_required_package_fails(self):
        specs = (doctor.PackageSpec("nope", "nope-pkg", "x", True),)
        results = doctor.check_packages(specs, finder=lambda name: None)
        assert results[0].status == doctor.STATUS_FAIL
        assert "pip install nope-pkg" in results[0].hint

    def test_missing_optional_package_warns(self):
        specs = (doctor.PackageSpec("nope", "nope-pkg", "x", False),)
        results = doctor.check_packages(specs, finder=lambda name: None)
        assert results[0].status == doctor.STATUS_WARN

    def test_finder_exception_treated_as_missing(self):
        def boom(name):
            raise ModuleNotFoundError(name)

        specs = (doctor.PackageSpec("nope", "nope-pkg", "x", True),)
        results = doctor.check_packages(specs, finder=boom)
        assert results[0].status == doctor.STATUS_FAIL

    def test_default_registry_has_core_packages(self):
        names = {spec.import_name for spec in doctor._REQUIRED_PACKAGES}
        assert {"cmd2", "flask", "rich", "yaml", "pyarrow"} <= names

    def test_import_name_differs_from_pip_name_where_expected(self):
        by_import = {s.import_name: s for s in doctor._REQUIRED_PACKAGES}
        assert by_import["yaml"].pip_name == "pyyaml"
        assert by_import["Crypto"].pip_name == "pycryptodome"


class TestFileChecks:
    def test_payload_present_is_ok(self, tmp_path):
        (tmp_path / "payload.json").write_text("{}")
        assert doctor.check_payload(tmp_path).status == doctor.STATUS_OK

    def test_payload_missing_fails(self, tmp_path):
        result = doctor.check_payload(tmp_path)
        assert result.status == doctor.STATUS_FAIL
        assert result.hint

    def test_certificates_present_is_ok(self, tmp_path):
        (tmp_path / "cert.pem").write_text("x")
        (tmp_path / "key.pem").write_text("x")
        assert doctor.check_certificates(tmp_path).status == doctor.STATUS_OK

    def test_certificates_partial_warns(self, tmp_path):
        (tmp_path / "cert.pem").write_text("x")
        result = doctor.check_certificates(tmp_path)
        assert result.status == doctor.STATUS_WARN
        assert "key.pem" in result.detail


class TestSecListsAndTools:
    def test_seclists_found_is_ok(self):
        result = doctor.check_seclists(finder=lambda: "/usr/share/seclists")
        assert result.status == doctor.STATUS_OK
        assert result.detail == "/usr/share/seclists"

    def test_seclists_missing_warns(self):
        result = doctor.check_seclists(finder=lambda: None)
        assert result.status == doctor.STATUS_WARN

    def test_external_tools_present_and_missing(self):
        present = BinaryStatus(
            spec=BinarySpec("nmap", "recon", "scan", "apt install nmap"),
            present=True,
            resolved_path="/usr/bin/nmap",
        )
        missing = BinaryStatus(
            spec=BinarySpec("evil-winrm", "ad", "winrm", "gem install evil-winrm"),
            present=False,
        )
        results = doctor.check_external_tools(checker=lambda: [present, missing])
        statuses = {r.name: r.status for r in results}
        assert statuses["nmap"] == doctor.STATUS_OK
        assert statuses["evil-winrm"] == doctor.STATUS_WARN


class TestReportAggregation:
    def test_overall_status_ok_when_all_ok(self):
        report = doctor.DoctorReport(
            checks=[doctor.CheckResult("a", doctor.STATUS_OK, "")]
        )
        assert report.overall_status == doctor.STATUS_OK
        assert report.healthy is True

    def test_overall_status_warn_with_warnings_only(self):
        report = doctor.DoctorReport(
            checks=[
                doctor.CheckResult("a", doctor.STATUS_OK, ""),
                doctor.CheckResult("b", doctor.STATUS_WARN, ""),
            ]
        )
        assert report.overall_status == doctor.STATUS_WARN
        assert report.healthy is True

    def test_overall_status_fail_trips_healthy(self):
        report = doctor.DoctorReport(
            checks=[
                doctor.CheckResult("a", doctor.STATUS_WARN, ""),
                doctor.CheckResult("b", doctor.STATUS_FAIL, ""),
            ]
        )
        assert report.overall_status == doctor.STATUS_FAIL
        assert report.healthy is False
        assert len(report.failures) == 1
        assert len(report.warnings) == 1


class TestGatherAndRun:
    def test_gather_report_populates_all_sections(self, tmp_path):
        (tmp_path / "payload.json").write_text("{}")
        report = doctor.gather_report(tmp_path)
        labels = {c.name for c in report.checks}
        assert "Python version" in labels
        assert "Config file" in labels
        assert "C2 certificates" in labels
        assert len(report.checks) > len(doctor._REQUIRED_PACKAGES)

    def test_run_returns_report_without_raising(self, tmp_path):
        (tmp_path / "payload.json").write_text("{}")
        report = doctor.run(root=tmp_path)
        assert isinstance(report, doctor.DoctorReport)
        assert report.checks
