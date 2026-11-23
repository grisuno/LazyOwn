"""tests/test_php2shell_poc_addons.py

Validation suite for the ikow/php2shell-poc lazyaddon family
(php2shell_scan, php2shell_a, php2shell_b, php2shell_c).

Locks the structural contract of the four CVE-2026-109618/109619 addons:
archetype A (cloned tool, local execute) for the network-runnable scan
and chains plus the C2-staging remote_command/upload_file pair for the
target-local chain B, and the shared placeholder contract: single
braces, tokens declared and live, and the shared rce_command key.

No network access, no clone and no exploit run happen here.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

import pytest
import yaml

from core.param_registry import effective_value

REPO_ROOT = Path(__file__).resolve().parent.parent
ADDONS_DIR = REPO_ROOT / "lazyaddons"
POC_REPO = "https://github.com/ikow/php2shell-poc.git"
INSTALL_PATH = "external/.exploit/php2shell_poc"

NAME_PATTERN = re.compile(r"^[a-z][a-z0-9_]{0,63}$")
VERSION_PATTERN = re.compile(r"^\d+(\.\d+){0,3}$")
CATEGORY_PATTERN = re.compile(r"^\d{2}\. [A-Za-z0-9 /&()+\-]{3,60}$")
TOKEN_PATTERN = re.compile(r"(?<!\{)\{([a-zA-Z_][a-zA-Z0-9_]*)\}(?!\})")
ALLOWED_OS = {"any", "linux", "windows", "macos", "network", "containers", "saas", "iaas"}
TOOL_FIELDS = (
    "execute_command",
    "install_command",
    "remote_command",
    "lazycommand",
    "upload_file",
    "download_file",
)

ADDON_NAMES = ("php2shell_scan", "php2shell_a", "php2shell_b", "php2shell_c")


def _live_params() -> dict:
    """Return the keys the shell can substitute at runtime."""
    live = json.loads((REPO_ROOT / "payload.json").read_text(encoding="utf-8"))
    for path in sorted((REPO_ROOT / "params").glob("*.yaml")):
        data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        for key, value in data.items():
            live[key] = effective_value(value)
    return live


def _addon(name: str) -> dict:
    """Return one parsed addon manifest."""
    return yaml.safe_load((ADDONS_DIR / f"{name}.yaml").read_text(encoding="utf-8"))


def _tokens(addon: dict) -> list[tuple[str, str]]:
    """Return every (field, token) pair across the tool templates."""
    tool = addon.get("tool", {}) or {}
    found: list[tuple[str, str]] = []
    for field in TOOL_FIELDS:
        value = tool.get(field, "")
        if isinstance(value, str):
            for token in TOKEN_PATTERN.findall(value):
                found.append((field, token))
    return found


class TestPhp2ShellPocAddonsExist:
    @pytest.mark.parametrize("name", ADDON_NAMES)
    def test_addon_present_and_parses(self, name):
        path = ADDONS_DIR / f"{name}.yaml"
        assert path.is_file(), f"Missing: {path}"
        assert isinstance(_addon(name), dict)

    @pytest.mark.parametrize("name", ADDON_NAMES)
    def test_identity_contract(self, name):
        addon = _addon(name)
        assert addon["name"] == name and NAME_PATTERN.fullmatch(name)
        assert VERSION_PATTERN.fullmatch(str(addon["version"]))
        assert CATEGORY_PATTERN.fullmatch(str(addon["category"]))
        assert addon.get("enabled") is True
        assert addon.get("os") in ALLOWED_OS
        assert isinstance(addon.get("trigger", []), list)

    @pytest.mark.parametrize("name", ADDON_NAMES)
    def test_clones_the_ikow_poc(self, name):
        tool = _addon(name)["tool"]
        assert tool["repo_url"] == POC_REPO
        assert tool["repo_url"].endswith(".git")
        assert tool["install_path"] == INSTALL_PATH

    @pytest.mark.parametrize("name", ADDON_NAMES)
    def test_placeholders_single_brace(self, name):
        for field, token in _tokens(_addon(name)):
            assert isinstance(token, str) and token

    @pytest.mark.parametrize("name", ADDON_NAMES)
    def test_tokens_resolve_from_live_params(self, name):
        live = _live_params()
        declared = {p["name"] for p in (_addon(name).get("params") or []) if isinstance(p, dict)}
        for _field, token in _tokens(_addon(name)):
            assert token in live or token in declared, f"{name}: {{{token}}} not live"

    @pytest.mark.parametrize("name", ADDON_NAMES)
    def test_required_params_exist_live(self, name):
        live = _live_params()
        for param in _addon(name).get("params") or []:
            if param.get("required") and "default" not in param:
                assert param["name"] in live, f"{name}: {param['name']} missing"


class TestPhp2ShellScanAddon:
    def test_scanner_primary_usage(self):
        addon = _addon("php2shell_scan")
        assert addon["category"] == "02. Scanning & Enumeration"
        assert addon["module_type"] == "scanner"
        assert addon["tool"]["execute_command"].startswith("python3 scanner/check.py {url}")

    def test_scanner_triggers_on_http(self):
        assert "http" in _addon("php2shell_scan")["trigger"]


class TestChainAddons:
    def test_chain_a_uses_session_lfi_script(self):
        addon = _addon("php2shell_a")
        command = addon["tool"]["execute_command"]
        assert "chain_a_session_lfi.py" in command
        assert "--target {url}" in command
        assert "'{rce_command}'" in command

    def test_chain_c_uses_mismatch_script(self):
        addon = _addon("php2shell_c")
        command = addon["tool"]["execute_command"]
        assert "chain_c_mismatch_rce.py" in command
        assert "--target {url}" in command

    def test_chain_b_is_c2_staged(self):
        tool = _addon("php2shell_b")["tool"]
        assert "chain_b_uaf_rce.php" in tool["execute_command"]
        assert tool["upload_file"] == "sessions/php2shell_chain_b.php"
        assert tool["remote_command"].startswith("no_priv php php2shell_chain_b.php")

    def test_shared_rce_command_key_is_generic(self):
        live = _live_params()
        assert "rce_command" in live
        for name in ("php2shell_a", "php2shell_c"):
            declared = {p["name"] for p in (_addon(name).get("params") or [])}
            assert "rce_command" in declared


class TestAtomicSpecsForAutoPwn:
    def test_specs_load_through_the_bridge(self):
        from modules.atomic_exploit_bridge import EXPLOITS_DIR, load_all

        specs = load_all(EXPLOITS_DIR)
        for spec_id in ("php2shell_chain_a", "php2shell_chain_c"):
            spec = specs.get(spec_id)
            assert spec is not None, f"{spec_id} failed spec validation"
            assert spec.services == ["http"]
            assert "php" in spec.products
            assert spec.enabled

    def test_specs_carry_the_cves(self):
        from modules.atomic_exploit_bridge import EXPLOITS_DIR, load_all

        specs = load_all(EXPLOITS_DIR)
        assert specs["php2shell_chain_a"].cve == "CVE-2026-109618"
        assert specs["php2shell_chain_c"].cve == "CVE-2026-109619"

    def test_specs_match_http_profiles(self):
        from modules.autonomous_exploit_engine import AutonomousExploitEngine, TargetProfile

        engine = AutonomousExploitEngine()
        profile = TargetProfile(
            ip="127.0.0.1",
            open_ports=(8086,),
            services=({"name": "http", "port": "8086", "product": "Apache httpd", "version": "2.4 (PHP/8.1)"},),
        )
        strategies = {c.strategy for c in engine._match_atomic_specs(profile)}
        assert "php2shell_chain_a" in strategies


class TestLabScenario:
    def test_php2shell_lab_scenarios_registered(self):
        from modules import lab_runtime

        s56 = lab_runtime.LAB_SCENARIOS.get("php2shell56")
        s84 = lab_runtime.LAB_SCENARIOS.get("php2shell84")
        assert s56 is not None and "80/tcp" in s56["ports"]
        assert s56["image"].startswith("php:5.6")
        assert s84 is not None and "80/tcp" in s84["ports"]
        assert s84["image"].startswith("php:8.4")

    def test_bootstrap_writes_ini_webroot_and_restarts_apache(self):
        from modules import lab_runtime

        script = lab_runtime.PHP2SHELL56_BOOTSTRAP
        assert "lazyown-php2shell56.ini" in script
        assert "vuln.php" in script
        assert "apachectl" in script
        ini = lab_runtime.PHP2SHELL56_INI
        assert "upload_progress.enabled" in ini
        assert "cleanup = 0" in ini
        assert 'save_path = "/tmp/sessions"' in ini

    def test_noop_for_other_scenarios(self):
        from modules import lab_runtime

        assert lab_runtime._ensure_php2shell56("metasploitable", "lazyown-lab-metasploitable") is None

    def test_gym_definition_loaded(self):
        from modules.gym_registry import load_definitions

        defs = load_definitions()
        assert "php2shell_chain_a" in defs
        assert defs["php2shell_chain_a"]["scenario"] == "php2shell56"


class TestVerbCatalog:
    def test_addon_verbs_registered(self):
        from modules.verb_catalog import entries

        table = entries()
        for verb in ("addon:php2shell_scan", "addon:php2shell_a", "addon:php2shell_b", "addon:php2shell_c"):
            assert verb in table, f"{verb} missing from the verb catalog"
        assert table["addon:php2shell_scan"]["enabled"] is True
        assert table["addon:php2shell_a"]["phase"] == "exploit"
