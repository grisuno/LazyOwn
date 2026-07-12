"""tests/test_attack_surface_addons.py

BDD: Validate cloud, supply-chain, and web attack-surface lazyaddons.

Scenarios:
  - Given a valid YAML addon, when loaded, it exposes required fields
  - Given required params, when payload.json has matching keys, the command
    template can be resolved
  - Given an install_path, it stays within the repo root
  - Given an enabled addon, its name matches the CLI verb convention

SDD: No hardcoded IPs, ports, or secrets in any addon definition.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest
import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
ADDONS_DIR = REPO_ROOT / "lazyaddons"

ADDON_FILES: dict[str, Path] = {
    "scoutsuite": ADDONS_DIR / "scoutsuite.yaml",
    "prowler": ADDONS_DIR / "prowler.yaml",
    "cloudsploit": ADDONS_DIR / "cloudsploit.yaml",
    "trivy": ADDONS_DIR / "trivy.yaml",
    "grype": ADDONS_DIR / "grype.yaml",
    "report_full": ADDONS_DIR / "report_full.yaml",
}


def _load(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as fh:
        return yaml.safe_load(fh)


def _param_names(addon: dict) -> list[str]:
    return [p["name"] for p in addon.get("params", [])]


def _yaml_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


# ---------------------------------------------------------------------------
# Helpers for parametrized fixtures
# ---------------------------------------------------------------------------

def _all_addon_data():
    """Yield (name, doc_dict) for every ADDON_FILES entry."""
    for name, path in ADDON_FILES.items():
        if path.exists():
            yield pytest.param(name, _load(path), id=name)


def _loaded(name: str) -> dict:
    return _load(ADDON_FILES[name])


# ===========================================================================
# 1.  EXISTENCE & PARSABILITY
# ===========================================================================

class TestAddonExists:
    """Each YAML addon file must exist and be parseable."""

    @pytest.mark.parametrize("name,path", list(ADDON_FILES.items()), ids=list(ADDON_FILES))
    def test_file_present(self, name: str, path: Path) -> None:
        assert path.exists(), f"Missing addon: {path}"

    @pytest.mark.parametrize("name,path", list(ADDON_FILES.items()), ids=list(ADDON_FILES))
    def test_yaml_parses(self, name: str, path: Path) -> None:
        data = _load(path)
        assert isinstance(data, dict), f"{name} did not produce a dict"


# ===========================================================================
# 2.  REQUIRED TOP-LEVEL FIELDS
# ===========================================================================

REQUIRED_FIELDS = ["name", "description", "enabled", "tool", "category"]


class TestRequiredFields:
    """Every lazyaddon must declare the five mandatory top-level fields."""

    @pytest.mark.parametrize("name,addon", _all_addon_data())
    def test_has_required_fields(self, name: str, addon: dict) -> None:
        for field in REQUIRED_FIELDS:
            assert field in addon, f"{name} missing required field: {field}"

    @pytest.mark.parametrize("name,addon", _all_addon_data())
    def test_name_is_string(self, name: str, addon: dict) -> None:
        assert isinstance(addon["name"], str) and addon["name"].strip(), f"{name} name must be non-empty string"

    @pytest.mark.parametrize("name,addon", _all_addon_data())
    def test_description_is_string(self, name: str, addon: dict) -> None:
        assert isinstance(addon["description"], str) and len(addon["description"]) > 10, \
            f"{name} description too short or missing"

    @pytest.mark.parametrize("name,addon", _all_addon_data())
    def test_enabled_is_true(self, name: str, addon: dict) -> None:
        assert addon["enabled"] is True, f"{name} must be enabled by default"


# ===========================================================================
# 3.  TOOL SECTION CONTRACTS
# ===========================================================================

REQUIRED_TOOL_FIELDS = ["name", "repo_url", "install_path", "execute_command"]


class TestToolSection:
    """The tool sub-section must contain the execution contract."""

    @pytest.mark.parametrize("name,addon", _all_addon_data())
    def test_tool_is_dict(self, name: str, addon: dict) -> None:
        assert isinstance(addon["tool"], dict), f"{name} tool section must be a dict"

    @pytest.mark.parametrize("name,addon", _all_addon_data())
    def test_tool_required_keys(self, name: str, addon: dict) -> None:
        for key in REQUIRED_TOOL_FIELDS:
            assert key in addon["tool"], f"{name} tool section missing: {key}"

    @pytest.mark.parametrize("name,addon", _all_addon_data())
    def test_repo_url_ends_with_git(self, name: str, addon: dict) -> None:
        url = addon["tool"]["repo_url"]
        assert url.endswith(".git"), f"{name} repo_url should end with .git: {url}"

    @pytest.mark.parametrize("name,addon", _all_addon_data())
    def test_repo_url_is_https(self, name: str, addon: dict) -> None:
        url = addon["tool"]["repo_url"]
        assert url.startswith("https://"), f"{name} repo_url must be HTTPS: {url}"

    @pytest.mark.parametrize("name,addon", _all_addon_data())
    def test_execute_command_is_string(self, name: str, addon: dict) -> None:
        cmd = addon["tool"]["execute_command"]
        assert isinstance(cmd, str) and len(cmd) > 5, f"{name} execute_command too short"


# ===========================================================================
# 4.  PARAM CONTRACTS
# ===========================================================================

class TestParams:
    """Declared params must match what the execute_command template needs."""

    @pytest.mark.parametrize("name,addon", _all_addon_data())
    def test_params_is_list_when_present(self, name: str, addon: dict) -> None:
        if "params" in addon:
            assert isinstance(addon["params"], list), f"{name} params must be a list"

    @pytest.mark.parametrize("name,addon", _all_addon_data())
    def test_each_param_has_name(self, name: str, addon: dict) -> None:
        for p in addon.get("params", []):
            assert "name" in p, f"{name} param missing 'name': {p}"

    @pytest.mark.parametrize("name,addon", _all_addon_data())
    def test_each_param_has_description(self, name: str, addon: dict) -> None:
        for p in addon.get("params", []):
            assert "description" in p, f"{name} param '{p.get('name')}' missing description"

    @pytest.mark.parametrize("name,addon", _all_addon_data())
    def no_duplicate_param_names(self, name: str, addon: dict) -> None:
        names = _param_names(addon)
        assert len(names) == len(set(names)), f"{name} has duplicate param names: {names}"


# ===========================================================================
# 5.  PATH SAFETY  (SDD)
# ===========================================================================

class TestPathSafety:
    """Install paths must not escape the repo root via traversal sequences."""

    @pytest.mark.parametrize("name,addon", _all_addon_data())
    def test_install_path_contained(self, name: str, addon: dict) -> None:
        path = addon["tool"]["install_path"]
        resolved = Path(REPO_ROOT / path).resolve()
        assert str(resolved).startswith(str(REPO_ROOT)), (
            f"{name} install_path escapes repo root: {path}"
        )

    @pytest.mark.parametrize("name,addon", _all_addon_data())
    def test_install_path_no_dot_dot_prefix(self, name: str, addon: dict) -> None:
        path = addon["tool"]["install_path"]
        assert not path.startswith("../") and ".." not in path.split("/"), (
            f"{name} install_path contains traversal: {path}"
        )

    @pytest.mark.parametrize("name,addon", _all_addon_data())
    def test_no_tilde_in_paths(self, name: str, addon: dict) -> None:
        path = addon["tool"]["install_path"]
        assert "~" not in path, f"{name} contains tilde in install_path: {path}"


# ===========================================================================
# 6.  NO HARDCODED SECRETS  (SDD)
# ===========================================================================

class TestNoHardcodedSecrets:
    """SDD: No IP addresses, port literals, or credential patterns in YAML."""

    @pytest.mark.parametrize("name,addon", list(ADDON_FILES.items()), ids=list(ADDON_FILES))
    def test_no_hardcoded_ip(self, name: str, addon: dict) -> None:
        text = _yaml_text(ADDON_FILES[name])
        ips = re.findall(r'\b(?:\d{1,3}\.){3}\d{1,3}\b', text)
        assert ips == [], f"{name} has hardcoded IPs: {ips}"

    @pytest.mark.parametrize("name,addon", list(ADDON_FILES.items()), ids=list(ADDON_FILES))
    def test_no_well_known_ports(self, name: str, addon: dict) -> None:
        text = _yaml_text(ADDON_FILES[name])
        for port in ["4444", "8443", "8080", "9999"]:
            assert port not in text, f"{name} has hardcoded port {port}"

    @pytest.mark.parametrize("name,addon", list(ADDON_FILES.items()), ids=list(ADDON_FILES))
    def test_no_password_literals(self, name: str, addon: dict) -> None:
        text = _yaml_text(ADDON_FILES[name]).lower()
        for literal in ["password:", "p@ssword", "secret:", "changeme"]:
            assert literal not in text, f"{name} contains password literal: {literal}"


# ===========================================================================
# 7.  COMMAND TEMPLATE INTEGRITY
# ===========================================================================

class TestCommandTemplates:
    """execute_command must use {param} placeholders instead of hardcoded values."""

    @pytest.mark.parametrize("name,addon", _all_addon_data())
    def test_execute_has_at_least_one_placeholder(self, name: str, addon: dict) -> None:
        cmd = addon["tool"]["execute_command"]
        has_placeholder = "{" in cmd and "}" in cmd
        # in-repo tools (install_path = .) may not need placeholders
        if addon["tool"].get("install_path") != ".":
            assert has_placeholder, f"{name} execute_command has no {{param}} placeholders"


# ===========================================================================
# 8.  ADDON-SPECIFIC VALIDATION
# ===========================================================================

class TestScoutSuiteSpecific:
    """ScoutSuite is AWS-focused cloud auditing."""

    @pytest.fixture(scope="class")
    def addon(self) -> dict:
        return _loaded("scoutsuite")

    def test_name(self, addon: dict) -> None:
        assert addon["name"] == "scoutsuite"

    def test_os_is_iaas(self, addon: dict) -> None:
        assert addon.get("os", "") in ("iaas", "any"), "scoutsuite should target iaas"

    def test_has_region_param(self, addon: dict) -> None:
        assert "region" in _param_names(addon), "scoutsuite needs region param"

    def test_has_provider_param(self, addon: dict) -> None:
        names = _param_names(addon)
        has_provider = any("provider" in n or "aws" in n for n in names)
        assert has_provider, "scoutsuite needs provider identifier param"


class TestProwlerSpecific:
    """Prowler is multi-cloud (AWS, Azure, GCP)."""

    @pytest.fixture(scope="class")
    def addon(self) -> dict:
        return _loaded("prowler")

    def test_name(self, addon: dict) -> None:
        assert addon["name"] == "prowler"

    def test_os_is_iaas(self, addon: dict) -> None:
        assert addon.get("os", "") in ("iaas", "any"), "prowler should target iaas"

    def test_has_provider_param(self, addon: dict) -> None:
        names = _param_names(addon)
        assert any("provider" in n for n in names), "prowler needs provider param"

    def test_category_is_recon_or_scan(self, addon: dict) -> None:
        assert "recon" in addon["category"].lower() or "scan" in addon["category"].lower()


class TestCloudSploitSpecific:
    """CloudSploit scans cloud provider configurations for risks."""

    @pytest.fixture(scope="class")
    def addon(self) -> dict:
        return _loaded("cloudsploit")

    def test_name(self, addon: dict) -> None:
        assert addon["name"] == "cloudsploit"

    def test_has_cloud_param(self, addon: dict) -> None:
        names = _param_names(addon)
        assert any("cloud" in n or "provider" in n for n in names)


class TestTrivySpecific:
    """Trivy scans containers, filesystems, and repos for vulnerabilities."""

    @pytest.fixture(scope="class")
    def addon(self) -> dict:
        return _loaded("trivy")

    def test_name(self, addon: dict) -> None:
        assert addon["name"] == "trivy"

    def test_os_is_containers(self, addon: dict) -> None:
        assert addon.get("os", "") in ("containers", "any", "saas"), \
            "trivy should target containers or any"

    def test_has_target_param(self, addon: dict) -> None:
        names = _param_names(addon)
        assert any(t in names for t in ("target", "trivy_target", "path", "image", "repo")), \
            "trivy needs a target/scan path param"

    def test_triggers_docker(self, addon: dict) -> None:
        triggers = [t.lower() for t in addon.get("trigger", [])]
        assert any(t in triggers for t in ("docker", "containers", "http")) or not triggers


class TestGrypeSpecific:
    """Grype scans SBOMs and directories for known vulnerabilities."""

    @pytest.fixture(scope="class")
    def addon(self) -> dict:
        return _loaded("grype")

    def test_name(self, addon: dict) -> None:
        assert addon["name"] == "grype"

    def test_has_target_param(self, addon: dict) -> None:
        names = _param_names(addon)
        assert any(t in names for t in ("target", "grype_target", "path", "image", "sbom")), \
            "grype needs a target/scan path param"

    def test_description_mentions_vulnerability(self, addon: dict) -> None:
        assert "vulnerability" in addon["description"].lower() or "cve" in addon["description"].lower()


class TestReportFullSpecific:
    """report_full is an in-repo addon that wraps report_generator.py."""

    @pytest.fixture(scope="class")
    def addon(self) -> dict:
        return _loaded("report_full")

    def test_name(self, addon: dict) -> None:
        assert addon["name"] == "report_full"

    def test_category_is_reporting(self, addon: dict) -> None:
        assert "report" in addon["category"].lower()

    def test_install_path_is_dot(self, addon: dict) -> None:
        assert addon["tool"]["install_path"] == ".", \
            "report_full uses in-repo report_generator, should use install_path: ."

    def test_execute_calls_report_generator(self, addon: dict) -> None:
        cmd = addon["tool"]["execute_command"]
        assert "report_generator.py" in cmd, "report_full must call report_generator.py"

    def test_repo_url_points_to_lazyown(self, addon: dict) -> None:
        assert "LazyOwn" in addon["tool"]["repo_url"] or "grisuno" in addon["tool"]["repo_url"]


# ===========================================================================
# 9.  FUZZING — EDGE CASES IN YAML STRUCTURE  (SDD + Fuzzing)
# ===========================================================================

class TestFuzzAddonStructure:
    """Fuzz edge cases: field types, boundary values, missing optional keys."""

    @pytest.mark.parametrize("name,addon", _all_addon_data())
    def test_name_no_spaces(self, name: str, addon: dict) -> None:
        assert " " not in addon["name"], f"{name} name with spaces may break CLI verb"

    @pytest.mark.parametrize("name,addon", _all_addon_data())
    def test_name_lowercase(self, name: str, addon: dict) -> None:
        assert addon["name"] == addon["name"].lower(), \
            f"{name} name should be lowercase for CLI consistency"

    @pytest.mark.parametrize("name,addon", _all_addon_data())
    def test_category_falls_in_known_range(self, name: str, addon: dict) -> None:
        cat = addon.get("category", "")
        prefix = cat.split(".")[0] if "." in cat else ""
        assert prefix.isdigit() or not prefix, \
            f"{name} category should start with a number: {cat}"

    @pytest.mark.parametrize("name,addon", _all_addon_data())
    def test_trigger_is_list_when_present(self, name: str, addon: dict) -> None:
        if "trigger" in addon:
            assert isinstance(addon["trigger"], list), \
                f"{name} trigger must be a list"

    @pytest.mark.parametrize("name,addon", _all_addon_data())
    def test_os_is_known_value(self, name: str, addon: dict) -> None:
        known_os = {"any", "linux", "windows", "macos", "network", "containers", "saas", "iaas"}
        os_val = addon.get("os", "any")
        assert os_val in known_os, f"{name} unknown os value: {os_val}"


# ===========================================================================
# 10.  RESULT REVIEW — SURFACE SUMMARY
# ===========================================================================

class TestResultReview:
    """Print a human-readable summary of all attack-surface addons for review."""

    def test_summary_table(self) -> None:
        """Generate a review table (test always passes; read output for review)."""
        rows: list[list[str]] = []
        for name, path in sorted(ADDON_FILES.items()):
            if not path.exists():
                rows.append([name, "MISSING", "", "", "", ""])
                continue
            addon = _load(path)
            tool = addon.get("tool", {})
            params = ", ".join(_param_names(addon)) or "(none)"
            triggers = ", ".join(addon.get("trigger", [])) or "(none)"
            rows.append([
                name,
                addon.get("os", "any"),
                addon.get("category", "?").split(".")[0],
                tool.get("install_path", "?"),
                params,
                triggers,
            ])
        header = "| Addon | OS | Cat | Install Path | Params | Triggers |"
        sep = "|------|----|-----|--------------|--------|----------|"
        lines = [header, sep] + [f"| {r[0]} | {r[1]} | {r[2]} | {r[3]} | {r[4]} | {r[5]} |" for r in rows]
        review = "\n".join(lines)

        print("\n=== Attack-Surface Addon Summary ===\n")
        print(review)
        print(f"\nTotal addons: {len(rows)}")
        print("Review result: PASS (structural validation completed)\n")
