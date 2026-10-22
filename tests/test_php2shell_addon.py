"""tests/test_php2shell_addon.py

Validation suite for the php2shell lazyaddon.

Locks the structural contract of ``lazyaddons/php2shell.yaml`` (archetype A:
cloned tool, local execute) and the placeholder contract shared by every
addon: single braces only, every token declared and live, no secret carried
as a placeholder, and a command that resolves completely from the shell
params without operator input.

The addon reuses the global ``url`` key, so it must not introduce payload
keys of its own.

No network access, no clone and no exploit run happen here.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

import pytest
import yaml

from core.param_registry import effective_value
from core.payload_schema import SCHEMA
from lazyc2.addon_creator import AddonCreatorConfig, AddonDraft, AddonValidator, ParamSpec
from utils import replace_command_placeholders

REPO_ROOT = Path(__file__).resolve().parent.parent
ADDON_YAML = REPO_ROOT / "lazyaddons" / "php2shell.yaml"

EXPECTED_REPO = "https://github.com/9bie/php2shell-bypass-aslr-exp.git"
EXPECTED_INSTALL_PATH = "external/.exploit/php2shell"
EXPECTED_CATEGORY = "03. Exploitation"
EXPECTED_PARAMS = ("url", "exploit_profile")
NAME_PATTERN = re.compile(r"^[a-z][a-z0-9_]{0,63}$")
VERSION_PATTERN = re.compile(r"^\d+(\.\d+){0,3}$")
CATEGORY_PATTERN = re.compile(r"^\d{2}\. [A-Za-z0-9 /&()+\-]{3,60}$")
PARAM_PATTERN = re.compile(r"^[a-z][a-z0-9_]{0,47}$")
TOKEN_PATTERN = re.compile(r"(?<!\{)\{([a-zA-Z_][a-zA-Z0-9_]*)\}(?!\})")
ALLOWED_OS = {
    "any",
    "linux",
    "windows",
    "macos",
    "network",
    "containers",
    "saas",
    "iaas",
}
SECRET_PARAMS = {"password", "pass", "api_key", "token", "c2_pass", "start_pass", "aes_key"}


@pytest.fixture(scope="module")
def addon() -> dict:
    """Return the parsed addon manifest."""
    return yaml.safe_load(ADDON_YAML.read_text(encoding="utf-8"))


@pytest.fixture(scope="module")
def live_params() -> dict:
    """Return the keys the shell can substitute at runtime."""
    live = json.loads((REPO_ROOT / "payload.json").read_text(encoding="utf-8"))
    for path in sorted((REPO_ROOT / "params").glob("*.yaml")):
        data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        for key, value in data.items():
            live[key] = effective_value(value)
    return live


class TestPhp2ShellAddonExists:
    def test_addon_present(self):
        assert ADDON_YAML.exists(), f"Missing: {ADDON_YAML}"

    def test_addon_parses(self, addon):
        assert isinstance(addon, dict)

    def test_name_matches_file(self, addon):
        assert addon["name"] == ADDON_YAML.stem

    def test_name_pattern(self, addon):
        assert NAME_PATTERN.match(addon["name"]), f"Illegal addon name: {addon['name']}"

    def test_version_pattern(self, addon):
        assert VERSION_PATTERN.match(str(addon["version"])), f"Illegal version: {addon['version']}"

    def test_description_length(self, addon):
        assert len(addon["description"].strip()) <= 500, "description exceeds 500 characters"

    def test_enabled(self, addon):
        assert addon["enabled"] is True

    def test_category(self, addon):
        assert addon["category"] == EXPECTED_CATEGORY

    def test_category_pattern(self, addon):
        assert CATEGORY_PATTERN.match(addon["category"]), f"Illegal category: {addon['category']}"

    def test_os_is_known(self, addon):
        assert addon.get("os", "any") in ALLOWED_OS, f"Unknown os: {addon.get('os')}"

    def test_module_type_is_known(self, addon):
        assert addon.get("module_type", "exploit") in {"scanner", "exploit", "payload", "auxiliary"}

    def test_triggers_are_service_names(self, addon):
        for trigger in addon.get("trigger", []):
            assert re.match(r"^[a-z0-9][a-z0-9\-]{0,63}$", trigger), f"Illegal trigger: {trigger}"

    def test_description_documents_setup_and_assign(self, addon):
        text = addon["description"].lower()
        assert "assign url" in text, "description must document the assign flow"
        assert "external/.exploit/php2shell" in text, "description must document the install path"


class TestPhp2ShellToolSection:
    def test_repo_url(self, addon):
        assert addon["tool"]["repo_url"] == EXPECTED_REPO

    def test_repo_url_ends_with_git(self, addon):
        assert addon["tool"]["repo_url"].endswith(".git")

    def test_install_path(self, addon):
        assert addon["tool"]["install_path"] == EXPECTED_INSTALL_PATH

    def test_install_path_no_traversal(self, addon):
        resolved = (REPO_ROOT / addon["tool"]["install_path"]).resolve()
        assert str(resolved).startswith(str(REPO_ROOT)), "install_path escapes the repo root"

    def test_install_command_creates_out_dir(self, addon):
        assert "mkdir -p out" in addon["tool"]["install_command"]

    def test_execute_command_runs_exploit(self, addon):
        command = addon["tool"]["execute_command"]
        assert command.startswith("python3 exploit.py"), "execute_command must run exploit.py"
        assert "-u {url}" in command, "execute_command must target the configured URL"

    def test_execute_command_is_complete_without_free_args(self, addon):
        command = addon["tool"]["execute_command"]
        assert "{url}" in command and "{exploit_profile}" in command
        assert "{" not in command.replace("{url}", "").replace("{exploit_profile}", "")

    def test_execute_command_uses_shared_profile(self, addon):
        command = addon["tool"]["execute_command"]
        assert "--profile {exploit_profile}" in command, "profile must come from the shared key"


class TestPhp2ShellPlaceholders:
    def test_no_double_braces(self):
        raw = ADDON_YAML.read_text(encoding="utf-8")
        assert "{{" not in raw and "}}" not in raw, "double braces are not substituted at runtime"

    def test_declared_params(self, addon):
        assert tuple(p["name"] for p in addon["params"]) == EXPECTED_PARAMS

    def test_param_names_are_valid(self, addon):
        for param in addon["params"]:
            assert PARAM_PATTERN.match(param["name"]), f"Illegal param name: {param['name']}"
            assert param["type"] in {"string", "integer", "boolean"}
            assert param["description"], f"Param {param['name']} has no description"
            assert len(param["description"]) <= 200

    def test_tokens_are_declared(self, addon):
        declared = {p["name"] for p in addon["params"]}
        tokens = set(TOKEN_PATTERN.findall(addon["tool"]["execute_command"]))
        assert tokens <= declared, f"Undeclared placeholders: {tokens - declared}"

    def test_no_secret_placeholders(self, addon):
        declared = {p["name"] for p in addon["params"]}
        assert not (declared & SECRET_PARAMS), "Secrets must never travel as placeholders"

    def test_no_addon_specific_payload_keys(self, addon):
        declared = {p["name"] for p in addon["params"]}
        assert declared <= set(SCHEMA), "every addon param must live in the payload schema"
        assert declared == {"url", "exploit_profile"}, "the addon must reuse global keys"

    def test_profile_key_is_addon_agnostic(self, addon):
        names = [p["name"] for p in addon["params"]]
        assert not [n for n in names if n.startswith("php2shell_")], "keys must not be addon-scoped"
        assert "exploit_profile" in SCHEMA, "the shared profile key must live in the payload schema"

    def test_params_are_live(self, live_params):
        for key in EXPECTED_PARAMS:
            assert key in live_params, f"{key} must exist in the live shell params"

    def test_live_params_resolve_every_token(self, addon, live_params):
        resolved = replace_command_placeholders(addon["tool"]["execute_command"], live_params)
        assert "{" not in resolved and "}" not in resolved, f"Unresolved token: {resolved}"

    def test_resolved_command_shape(self, addon, live_params):
        resolved = replace_command_placeholders(addon["tool"]["execute_command"], live_params)
        assert resolved.startswith("python3 exploit.py -u "), resolved
        assert "--profile " in resolved, resolved

    def test_resolved_command_with_assigned_url(self, addon, live_params):
        assigned = {**live_params, "url": "http://10.10.10.5/index.php"}
        resolved = replace_command_placeholders(addon["tool"]["execute_command"], assigned)
        assert resolved == ("python3 exploit.py -u http://10.10.10.5/index.php --profile bookworm"), resolved


class TestPhp2ShellSchema:
    def test_schema_has_url(self):
        assert "url" in SCHEMA, "the addon reuses the global url key"
        assert SCHEMA["url"].kind.value == "url"

    def test_schema_has_shared_profile(self):
        spec = SCHEMA["exploit_profile"]
        assert spec.kind.value == "string"
        assert spec.allowed is None, "the profile vocabulary belongs to each addon"
        assert spec.default == "bookworm"

    def test_validator_accepts_the_manifest(self, addon):
        draft = AddonDraft(
            name=addon["name"],
            description=addon["description"].strip(),
            author=addon.get("author", ""),
            version=str(addon["version"]),
            enabled=addon["enabled"],
            os=addon.get("os", "any"),
            triggers=list(addon.get("trigger", [])),
            category=addon["category"],
            module_type=addon.get("module_type", ""),
            params=[
                ParamSpec(
                    name=p["name"],
                    type=p["type"],
                    required=bool(p.get("required", False)),
                    description=p.get("description", ""),
                    default=p.get("default"),
                )
                for p in addon["params"]
            ],
            tool_name=addon["tool"]["name"],
            repo_url=addon["tool"]["repo_url"],
            install_path=addon["tool"]["install_path"],
            install_command=addon["tool"].get("install_command", ""),
            execute_command=addon["tool"]["execute_command"],
        )
        issues = AddonValidator(draft).validate()
        assert issues == [], f"Validator issues: {issues}"

    def test_placeholder_allowlist_knows_the_params(self):
        allowed = AddonCreatorConfig.live_placeholders()
        for key in EXPECTED_PARAMS:
            assert key in allowed, f"{key} must be accepted by the addon creator validator"
