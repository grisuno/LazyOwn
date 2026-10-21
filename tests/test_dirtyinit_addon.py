"""tests/test_dirtyinit_addon.py

Validation suite for the dirtyinit lazyaddon and its phone-side driver.

Checks structural integrity, the placeholder contract, the driver script
contract and the path safety of the install location, without touching a
device, the network, or any file outside the repository.
"""

from __future__ import annotations

import re
import subprocess
from pathlib import Path

import pytest
import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
ADDON_YAML = REPO_ROOT / "lazyaddons" / "dirtyinit.yaml"
DRIVER = REPO_ROOT / "scripts" / "dirtyinit_drive.sh"

EXPECTED_REPO = "https://github.com/combeng6th/DirtyInit.git"
EXPECTED_INSTALL_PATH = "external/.exploit/dirtyinit"
EXPECTED_CATEGORY = "03. Exploitation"
EXPECTED_PACKAGE = "com.dirty.init"
NAME_PATTERN = re.compile(r"^[a-z][a-z0-9_]{0,63}$")
VERSION_PATTERN = re.compile(r"^\d+(\.\d+){0,3}$")
CATEGORY_PATTERN = re.compile(r"^\d{2}\. [A-Za-z0-9 /&()+\-]{3,60}$")
TOKEN_PATTERN = re.compile(r"(?<!\{)\{([a-zA-Z_][a-zA-Z0-9_]*)\}(?!\})")


def _load(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as fh:
        return yaml.safe_load(fh)


@pytest.fixture(scope="module")
def addon() -> dict:
    return _load(ADDON_YAML)


@pytest.fixture(scope="module")
def driver_text() -> str:
    return DRIVER.read_text(encoding="utf-8")


class TestDirtyInitAddonExists:
    def test_addon_present(self):
        assert ADDON_YAML.exists(), f"Missing: {ADDON_YAML}"

    def test_driver_present(self):
        assert DRIVER.exists(), f"Missing: {DRIVER}"

    def test_addon_parses(self, addon):
        assert isinstance(addon, dict)

    def test_driver_is_executable(self):
        import os

        assert os.access(DRIVER, os.X_OK), f"Driver is not executable: {DRIVER}"


class TestDirtyInitRequiredFields:
    @pytest.mark.parametrize("field", ["name", "description", "enabled", "tool", "category", "params"])
    def test_addon_has_field(self, addon, field):
        assert field in addon, f"dirtyinit.yaml missing required field: {field}"

    def test_name_matches_file(self, addon):
        assert addon["name"] == ADDON_YAML.stem

    def test_name_pattern(self, addon):
        assert NAME_PATTERN.match(addon["name"]), f"Illegal addon name: {addon['name']}"

    def test_version_pattern(self, addon):
        assert VERSION_PATTERN.match(str(addon["version"])), f"Illegal version: {addon['version']}"

    def test_description_length(self, addon):
        assert len(addon["description"]) <= 500, "description exceeds 500 characters"

    def test_enabled(self, addon):
        assert addon["enabled"] is True

    def test_category(self, addon):
        assert addon["category"] == EXPECTED_CATEGORY

    def test_category_pattern(self, addon):
        assert CATEGORY_PATTERN.match(addon["category"]), f"Illegal category: {addon['category']}"

    def test_os_is_known(self, addon):
        assert addon.get("os", "any") in {
            "any",
            "linux",
            "windows",
            "macos",
            "network",
            "containers",
            "saas",
            "iaas",
        }


class TestDirtyInitToolSection:
    @pytest.mark.parametrize("key", ["name", "repo_url", "install_path", "install_command", "execute_command"])
    def test_tool_has_key(self, addon, key):
        assert key in addon["tool"], f"dirtyinit.yaml tool section missing: {key}"

    def test_repo_url(self, addon):
        assert addon["tool"]["repo_url"] == EXPECTED_REPO

    def test_repo_url_ends_with_git(self, addon):
        assert addon["tool"]["repo_url"].endswith(".git")

    def test_install_path(self, addon):
        assert addon["tool"]["install_path"] == EXPECTED_INSTALL_PATH

    def test_install_path_no_traversal(self, addon):
        resolved = (REPO_ROOT / addon["tool"]["install_path"]).resolve()
        assert str(resolved).startswith(str(REPO_ROOT)), "install_path escapes the repo root"

    def test_install_command_runs_doctor(self, addon):
        assert "dirtyinit_drive.sh doctor" in addon["tool"]["install_command"]

    def test_execute_command_runs_driver(self, addon):
        assert "scripts/dirtyinit_drive.sh" in addon["tool"]["execute_command"]

    def test_execute_command_uses_env_prefix(self, addon):
        command = addon["tool"]["execute_command"]
        assert command.split()[0] == "env", "execute_command must start with env so the addon preflight stays quiet"

    def test_execute_command_is_complete(self, addon):
        assert "bash" in addon["tool"]["execute_command"]


class TestDirtyInitPlaceholders:
    def test_no_double_braces(self, addon):
        raw = ADDON_YAML.read_text(encoding="utf-8")
        assert "{{" not in raw and "}}" not in raw, "double braces are not substituted at runtime"

    def test_declared_params(self, addon):
        names = [p["name"] for p in addon["params"]]
        assert names == ["android_serial", "dirtyinit_device_path"]

    def test_param_names_are_valid(self, addon):
        for param in addon["params"]:
            assert re.match(r"^[a-z][a-z0-9_]{0,47}$", param["name"]), f"Illegal param name: {param['name']}"
            assert param["type"] in {"string", "integer", "boolean"}
            assert param["description"], f"Param {param['name']} has no description"
            assert len(param["description"]) <= 200

    def test_tokens_are_declared(self, addon):
        declared = {p["name"] for p in addon["params"]}
        tokens = set(TOKEN_PATTERN.findall(addon["tool"]["execute_command"]))
        assert tokens <= declared, f"Undeclared placeholders: {tokens - declared}"

    def test_no_secret_placeholders(self, addon):
        forbidden = {"password", "pass", "api_key", "token", "c2_pass", "start_pass"}
        declared = {p["name"] for p in addon["params"]}
        assert not (declared & forbidden), "Secrets must never travel as placeholders"

    def test_no_required_params(self, addon):
        for param in addon["params"]:
            assert not param.get("required", False), f"Param {param['name']} must stay optional"

    def test_params_are_live(self):
        import json

        live = set(json.loads((REPO_ROOT / "payload.json").read_text()).keys())
        for yaml_path in sorted((REPO_ROOT / "params").glob("*.yaml")):
            live.update((yaml.safe_load(yaml_path.read_text()) or {}).keys())
        for key in ("android_serial", "dirtyinit_device_path"):
            assert key in live, f"{key} must exist in the live shell params"


class TestDirtyInitDriverContract:
    def test_driver_syntax(self):
        result = subprocess.run(
            ["bash", "-n", str(DRIVER)],
            capture_output=True,
            text=True,
            check=False,
        )
        assert result.returncode == 0, result.stderr

    def test_driver_resolves_repo_root(self, driver_text):
        assert 'BASH_SOURCE[0]' in driver_text

    @pytest.mark.parametrize(
        "action",
        ["doctor", "build", "install", "launch", "auto", "extract", "stage", "run", "logs", "status"],
    )
    def test_driver_exposes_action(self, driver_text, action):
        assert f"{action})" in driver_text, f"Driver does not expose the {action} action"

    def test_driver_uses_adb(self, driver_text):
        assert "adb" in driver_text

    def test_driver_builds_apk(self, driver_text):
        for tool in ("aapt2", "d8", "zipalign", "apksigner"):
            assert tool in driver_text, f"Driver does not use {tool}"

    def test_driver_targets_expected_package(self, driver_text):
        assert EXPECTED_PACKAGE in driver_text

    def test_driver_falls_back_to_payload(self, driver_text):
        assert "payload_value" in driver_text, "driver must read payload.json so assign survives a restart"
        assert "android_serial" in driver_text

    def test_driver_has_no_hardcoded_host_paths(self, driver_text):
        assert "/home/" not in driver_text, "Driver must not hardcode host paths"
        assert "/Users/" not in driver_text, "Driver must not hardcode host paths"

    def test_driver_help_runs(self):
        result = subprocess.run(
            ["bash", str(DRIVER), "help"],
            capture_output=True,
            text=True,
            check=False,
        )
        assert result.returncode == 0, result.stderr
        assert "dirtyinit_drive.sh" in result.stdout

    def test_driver_status_runs(self):
        result = subprocess.run(
            ["bash", str(DRIVER), "status"],
            capture_output=True,
            text=True,
            check=False,
        )
        assert result.returncode == 0, result.stderr
        assert "DirtyInit status" in result.stdout

    def test_driver_rejects_unknown_action(self):
        result = subprocess.run(
            ["bash", str(DRIVER), "bogus"],
            capture_output=True,
            text=True,
            check=False,
        )
        assert result.returncode == 2
