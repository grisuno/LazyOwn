"""tests/test_blacksandbeacon_addon.py

Validation suite for the blacksandbeacon and blacksandbeacon_bof lazyaddons.

Checks structural integrity, required fields, URL correctness, parameter
contracts, path safety, and command template substitution without touching
the network or filesystem beyond the repo root.
"""

from pathlib import Path

import pytest
import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
ADDONS_DIR = REPO_ROOT / "lazyaddons"

BEACON_YAML = ADDONS_DIR / "blacksandbeacon.yaml"
BOF_YAML = ADDONS_DIR / "blacksandbeacon_bof.yaml"

EXPECTED_REPO = "https://github.com/grisuno/blacksandbeacon.git"
EXPECTED_INSTALL_PATH = "external/.exploit/blacksandbeacon"
EXPECTED_CATEGORY = "10. Command & Control"


def _load(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as fh:
        return yaml.safe_load(fh)


@pytest.fixture(scope="module")
def beacon() -> dict:
    return _load(BEACON_YAML)


@pytest.fixture(scope="module")
def bof() -> dict:
    return _load(BOF_YAML)


class TestBeaconYamlExists:
    def test_beacon_yaml_present(self):
        assert BEACON_YAML.exists(), f"Missing: {BEACON_YAML}"

    def test_bof_yaml_present(self):
        assert BOF_YAML.exists(), f"Missing: {BOF_YAML}"

    def test_beacon_yaml_parses(self, beacon):
        assert isinstance(beacon, dict)

    def test_bof_yaml_parses(self, bof):
        assert isinstance(bof, dict)


class TestBeaconRequiredFields:
    """Every lazyaddon must have name, description, enabled, tool, category."""

    @pytest.mark.parametrize("field", ["name", "description", "enabled", "tool", "category"])
    def test_beacon_has_field(self, beacon, field):
        assert field in beacon, f"blacksandbeacon.yaml missing required field: {field}"

    @pytest.mark.parametrize("field", ["name", "description", "enabled", "tool", "category"])
    def test_bof_has_field(self, bof, field):
        assert field in bof, f"blacksandbeacon_bof.yaml missing required field: {field}"


class TestBeaconToolSection:
    """The tool sub-section must define repo, install path, and both commands."""

    @pytest.mark.parametrize("key", ["repo_url", "install_path", "install_command", "execute_command"])
    def test_beacon_tool_has_key(self, beacon, key):
        assert key in beacon["tool"], f"blacksandbeacon.yaml tool section missing: {key}"

    @pytest.mark.parametrize("key", ["repo_url", "install_path", "install_command", "execute_command"])
    def test_bof_tool_has_key(self, bof, key):
        assert key in bof["tool"], f"blacksandbeacon_bof.yaml tool section missing: {key}"

    def test_beacon_repo_url(self, beacon):
        assert beacon["tool"]["repo_url"] == EXPECTED_REPO

    def test_bof_repo_url(self, bof):
        assert bof["tool"]["repo_url"] == EXPECTED_REPO

    def test_beacon_install_path(self, beacon):
        assert beacon["tool"]["install_path"] == EXPECTED_INSTALL_PATH

    def test_bof_install_path(self, bof):
        assert bof["tool"]["install_path"] == EXPECTED_INSTALL_PATH

    def test_beacon_install_command_is_make(self, beacon):
        assert beacon["tool"]["install_command"].strip() == "make"

    def test_bof_install_command_is_make(self, bof):
        assert bof["tool"]["install_command"].strip() == "make"


class TestBeaconPathSafety:
    """Install paths must not escape the repo root via traversal sequences."""

    def test_beacon_install_path_no_traversal(self, beacon):
        path = beacon["tool"]["install_path"]
        resolved = Path(REPO_ROOT / path).resolve()
        assert str(resolved).startswith(str(REPO_ROOT)), (
            f"blacksandbeacon install_path escapes repo root: {path}"
        )

    def test_bof_install_path_no_traversal(self, bof):
        path = bof["tool"]["install_path"]
        resolved = Path(REPO_ROOT / path).resolve()
        assert str(resolved).startswith(str(REPO_ROOT)), (
            f"blacksandbeacon_bof install_path escapes repo root: {path}"
        )


class TestBeaconCategory:
    def test_beacon_category(self, beacon):
        assert beacon["category"] == EXPECTED_CATEGORY

    def test_bof_category(self, bof):
        assert bof["category"] == EXPECTED_CATEGORY


class TestBeaconEnabled:
    def test_beacon_enabled(self, beacon):
        assert beacon["enabled"] is True

    def test_bof_enabled(self, bof):
        assert bof["enabled"] is True


class TestBeaconParams:
    """Both addons must declare lhost; the main beacon also requires lport and c2_port."""

    def _param_names(self, addon: dict) -> list:
        return [p["name"] for p in addon.get("params", [])]

    def test_beacon_has_lhost_param(self, beacon):
        assert "lhost" in self._param_names(beacon)

    def test_beacon_has_lport_param(self, beacon):
        assert "lport" in self._param_names(beacon)

    def test_beacon_has_c2_port_param(self, beacon):
        assert "c2_port" in self._param_names(beacon)

    def test_bof_has_lhost_param(self, bof):
        assert "lhost" in self._param_names(bof)

    def test_bof_has_lport_param(self, bof):
        assert "lport" in self._param_names(bof)

    def test_beacon_lhost_required(self, beacon):
        params = {p["name"]: p for p in beacon.get("params", [])}
        assert params["lhost"]["required"] is True

    def test_bof_lhost_required(self, bof):
        params = {p["name"]: p for p in bof.get("params", [])}
        assert params["lhost"]["required"] is True


class TestBeaconCommandTemplates:
    """Commands must reference {lhost} and {lport} for dynamic substitution."""

    def test_beacon_lazycommand_has_lhost(self, beacon):
        cmd = beacon["tool"].get("lazycommand", "")
        assert "{lhost}" in cmd, "lazycommand must include {lhost} placeholder"

    def test_beacon_lazycommand_has_lport(self, beacon):
        cmd = beacon["tool"].get("lazycommand", "")
        assert "{lport}" in cmd, "lazycommand must include {lport} placeholder"

    def test_bof_lazycommand_has_lhost(self, bof):
        cmd = bof["tool"].get("lazycommand", "")
        assert "{lhost}" in cmd

    def test_bof_lazycommand_has_lport(self, bof):
        cmd = bof["tool"].get("lazycommand", "")
        assert "{lport}" in cmd

    def test_beacon_execute_stages_to_sessions(self, beacon):
        cmd = beacon["tool"]["execute_command"]
        assert "sessions/blacksandbeacon" in cmd

    def test_bof_execute_stages_to_sessions(self, bof):
        assert "sessions/bof_loader" in bof["tool"]["execute_command"]

    def test_beacon_execute_resets_before_pull(self, beacon):
        cmd = beacon["tool"]["execute_command"]
        assert "git restore" in cmd and "git pull" in cmd

    def test_bof_execute_resets_before_pull(self, bof):
        cmd = bof["tool"]["execute_command"]
        assert "git restore" in cmd and "git pull" in cmd


class TestBeaconDescriptionQuality:
    """Descriptions must mention key differentiators."""

    def test_beacon_description_mentions_bof(self, beacon):
        desc = beacon["description"].lower()
        assert "bof" in desc or "beacon object" in desc

    def test_beacon_description_mentions_linux(self, beacon):
        assert "linux" in beacon["description"].lower()

    def test_bof_description_mentions_linux_bof(self, bof):
        desc = bof["description"].lower()
        assert "linux" in desc and ("bof" in desc or "beacon object" in desc)

    def test_bof_description_mentions_elf(self, bof):
        desc = bof["description"].lower()
        assert "elf" in desc or "shared" in desc

    def test_beacon_name_is_correct(self, beacon):
        assert beacon["name"] == "blacksandbeacon"

    def test_bof_name_is_correct(self, bof):
        assert bof["name"] == "blacksandbeacon_bof"


class TestBeaconNoHardcodedSecrets:
    """Neither YAML must contain IP addresses, ports, or credential literals."""

    def _yaml_text(self, path: Path) -> str:
        return path.read_text(encoding="utf-8")

    def test_beacon_no_hardcoded_ip(self):
        import re
        text = self._yaml_text(BEACON_YAML)
        ips = re.findall(r'\b(?:\d{1,3}\.){3}\d{1,3}\b', text)
        assert ips == [], f"Hardcoded IPs found in blacksandbeacon.yaml: {ips}"

    def test_bof_no_hardcoded_ip(self):
        import re
        text = self._yaml_text(BOF_YAML)
        ips = re.findall(r'\b(?:\d{1,3}\.){3}\d{1,3}\b', text)
        assert ips == [], f"Hardcoded IPs found in blacksandbeacon_bof.yaml: {ips}"

    def test_beacon_no_hardcoded_port_numbers(self):
        text = self._yaml_text(BEACON_YAML)
        assert "4444" not in text and "8080" not in text and "443 " not in text

    def test_bof_no_hardcoded_port_numbers(self):
        text = self._yaml_text(BOF_YAML)
        assert "4444" not in text and "8080" not in text and "443 " not in text
