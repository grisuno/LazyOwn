"""tests/test_wizard_binary_check.py

Tests for the wizard binary-readiness check added to ``cli.wizard``.

The check is the only step that touches the operator's environment without
explicit consent, so the contract under test is:

- ``check_binaries`` performs presence detection only; it never spawns a
  subprocess.
- Each :class:`BinarySpec` honours :data:`_BINARY_NAME_RE` so the report
  cannot leak shell metacharacters into the rendered table.
- The default ``_REQUIRED_BINARIES`` table stays in sync with the
  install hints required by the LazyOwn kill chain (recon, web, smb, ad,
  cred, exploit, c2).
- ``run`` always populates ``WizardResult.binaries`` regardless of
  whether the operator changed any payload values.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from cli import wizard  # noqa: E402


class TestBinarySpecRegistry:
    def test_default_registry_is_not_empty(self):
        assert len(wizard._REQUIRED_BINARIES) >= 15

    def test_every_spec_has_required_fields(self):
        for spec in wizard._REQUIRED_BINARIES:
            assert isinstance(spec, wizard.BinarySpec)
            assert spec.name and isinstance(spec.name, str)
            assert spec.category and isinstance(spec.category, str)
            assert spec.purpose and isinstance(spec.purpose, str)
            assert spec.install_hint and isinstance(spec.install_hint, str)

    def test_every_name_matches_safety_regex(self):
        for spec in wizard._REQUIRED_BINARIES:
            assert wizard._BINARY_NAME_RE.match(spec.name), (
                f"Unsafe binary name in registry: {spec.name!r}"
            )

    def test_no_duplicate_binary_names(self):
        names = [s.name for s in wizard._REQUIRED_BINARIES]
        assert len(names) == len(set(names)), f"duplicate spec names: {names}"

    def test_kill_chain_categories_covered(self):
        categories = {s.category for s in wizard._REQUIRED_BINARIES}
        for required in ("recon", "web", "cred", "smb", "ad", "exploit", "c2"):
            assert required in categories, (
                f"missing kill-chain category {required!r} in binary registry"
            )


class TestBinaryNameRegex:
    @pytest.mark.parametrize("name", [
        "nmap", "ffuf", "evil-winrm", "impacket-secretsdump",
        "feroxbuster", "golang-go", "a.b", "go",
    ])
    def test_accepts_known_safe_names(self, name):
        assert wizard._BINARY_NAME_RE.match(name)

    @pytest.mark.parametrize("name", [
        "", "nmap;rm -rf /", "nmap rm", "nmap`whoami`",
        "n$map", "../nmap", "nmap\n", "a" * 65,
    ])
    def test_rejects_unsafe_names(self, name):
        assert wizard._BINARY_NAME_RE.match(name) is None


class TestCheckBinariesContract:
    def test_returns_one_status_per_spec(self):
        specs = (
            wizard.BinarySpec("nmap", "recon", "p", "install nmap"),
            wizard.BinarySpec("hydra", "cred", "p", "install hydra"),
        )
        result = wizard.check_binaries(specs=specs, which=lambda _name: "/usr/bin/" + _name)
        assert len(result) == 2
        assert all(isinstance(item, wizard.BinaryStatus) for item in result)
        assert [item.spec.name for item in result] == ["nmap", "hydra"]

    def test_marks_missing_when_which_returns_none(self):
        spec = wizard.BinarySpec("nmap", "recon", "p", "h")
        result = wizard.check_binaries(specs=(spec,), which=lambda _n: None)
        assert result[0].present is False
        assert result[0].resolved_path is None

    def test_marks_present_when_which_returns_path(self):
        spec = wizard.BinarySpec("nmap", "recon", "p", "h")
        result = wizard.check_binaries(specs=(spec,), which=lambda _n: "/usr/bin/nmap")
        assert result[0].present is True
        assert result[0].resolved_path == "/usr/bin/nmap"

    def test_skips_specs_with_unsafe_names(self):
        unsafe = wizard.BinarySpec("nmap;rm", "recon", "p", "h")
        safe = wizard.BinarySpec("nmap", "recon", "p", "h")
        result = wizard.check_binaries(
            specs=(unsafe, safe), which=lambda _n: "/usr/bin/nmap"
        )
        assert len(result) == 1
        assert result[0].spec.name == "nmap"

    def test_check_does_not_invoke_subprocess(self, monkeypatch):
        import subprocess
        sentinel_calls: list[tuple] = []

        def _fail(*args, **kwargs):
            sentinel_calls.append((args, kwargs))
            raise AssertionError("check_binaries must not spawn subprocesses")

        monkeypatch.setattr(subprocess, "run", _fail)
        monkeypatch.setattr(subprocess, "check_output", _fail)
        monkeypatch.setattr(subprocess, "Popen", _fail)

        wizard.check_binaries(which=lambda _n: None)
        assert sentinel_calls == []

    def test_default_specs_used_when_omitted(self):
        result = wizard.check_binaries(which=lambda _n: None)
        assert len(result) == len(wizard._REQUIRED_BINARIES)


class TestGroupByCategory:
    def test_groups_preserve_order(self):
        statuses = [
            wizard.BinaryStatus(wizard.BinarySpec("nmap", "recon", "p", "h"), True),
            wizard.BinaryStatus(wizard.BinarySpec("ffuf", "web", "p", "h"), False),
            wizard.BinaryStatus(wizard.BinarySpec("curl", "recon", "p", "h"), True),
        ]
        grouped = wizard._group_by_category(statuses)
        assert list(grouped.keys()) == ["recon", "web"]
        assert [s.spec.name for s in grouped["recon"]] == ["nmap", "curl"]
        assert [s.spec.name for s in grouped["web"]] == ["ffuf"]


class TestRunIntegratesBinaryCheck:
    def test_run_populates_binaries_when_nothing_changes(self, monkeypatch):
        captured: dict[str, list] = {}

        def fake_check(*_args, **_kwargs):
            captured["called"] = True
            return [wizard.BinaryStatus(
                wizard.BinarySpec("nmap", "recon", "p", "h"), True, "/usr/bin/nmap"
            )]

        monkeypatch.setattr(wizard, "check_binaries", fake_check)
        monkeypatch.setattr(wizard, "_collect_values", lambda params: {})
        monkeypatch.setattr(wizard, "_print_binary_report", lambda statuses: None)
        monkeypatch.setattr(wizard, "_print_readiness", lambda items: None)

        params = {"rhost": "10.10.10.10", "lhost": "10.0.0.1"}
        result = wizard.run(params, save=lambda _k, _v: None)
        assert captured.get("called") is True
        assert result.binaries
        assert result.binaries[0].spec.name == "nmap"

    def test_run_populates_binaries_after_updates(self, monkeypatch):
        captured: dict[str, list] = {}

        def fake_check(*_args, **_kwargs):
            captured["called"] = True
            return [wizard.BinaryStatus(
                wizard.BinarySpec("nmap", "recon", "p", "h"), False
            )]

        monkeypatch.setattr(wizard, "check_binaries", fake_check)
        monkeypatch.setattr(wizard, "_collect_values", lambda params: {"rhost": "1.2.3.4"})
        monkeypatch.setattr(wizard, "_print_binary_report", lambda statuses: None)
        monkeypatch.setattr(wizard, "_print_readiness", lambda items: None)
        monkeypatch.setattr(wizard, "_print_next_steps", lambda params: None)

        saved: list[tuple] = []
        params: dict = {}
        result = wizard.run(params, save=lambda k, v: saved.append((k, v)))
        assert captured.get("called") is True
        assert result.saved is True
        assert result.binaries[0].present is False
        assert saved == [("rhost", "1.2.3.4")]


class TestPublicSurface:
    def test_check_binaries_in_dunder_all(self):
        assert "check_binaries" in wizard.__all__
        assert "BinarySpec" in wizard.__all__
        assert "BinaryStatus" in wizard.__all__
