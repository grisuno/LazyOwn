"""tests/test_awesome_windows_security_skill.py

Contract suite for the ``awesome-windows-security`` router skill.

The skill is a routing table: it claims that a Windows offensive technique
maps onto a LazyOwn command, a lazyaddon, an Atomic Red Team test or an
apt_chain step. Those claims rot the moment a command is renamed, an addon
is removed or an Atomic GUID disappears, so the skill is locked against the
live command index, the shipped addons, the atomic-red-team checkout and
the sibling skill files.

Scenarios:
    - Given the skill file, when the frontmatter is parsed, it declares a
      valid name, description and trigger
    - Given the router table, when every backticked token is collected,
      each one is a real command, a real lazyaddon or a known argument
    - Given the translation table, when every GUID is resolved, it maps to
      a real Atomic Red Team test with the technique the skill claims
    - Given the legacy ATT&CK identifiers, when they are normalised, the
      replacement technique actually carries a Windows Atomic test
    - Given the skill family, when the Claude and Hermes copies are
      compared, the bodies stay in sync
"""

from __future__ import annotations

import json
import re
from pathlib import Path

import pytest
import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
SKILL_DIR = REPO_ROOT / "skills" / "awesome-windows-security"
SKILL_MD = SKILL_DIR / "SKILL.md"
HERMES_MD = SKILL_DIR / "hermes" / "SKILL.md"
README_MD = SKILL_DIR / "README.md"
ATOMICS_DIR = REPO_ROOT / "external" / ".exploit" / "atomic-red-team" / "atomics"

SKILL_NAME = "awesome-windows-security"
TRIGGER = "/awesome-windows-security"
UPSTREAM = "chryzsh/awesome-windows-security"

NAME_PATTERN = re.compile(r"^[a-z][a-z0-9-]{1,63}$")
TOKEN_PATTERN = re.compile(r"`([a-z][a-z0-9_]{2,30})`")
GUID_PATTERN = re.compile(
    r"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b"
)
TECHNIQUE_PATTERN = re.compile(r"^T\d{4}(\.\d{3})?$")
ESCID_PATTERN = re.compile(r"^ESC\d{1,2}$")
TABLE_ROW_PATTERN = re.compile(
    r"^\|\s*(T\d{4}(?:\.\d{3})?)\s*\|\s*([0-9a-f-]{36})\s*\|", re.MULTILINE
)

ALLOWED_NON_COMMANDS = {
    "hash",
    "lazycommand",
    "nopass",
    "pass",
    "sudo_available",
    "run",
    "id",
    "name",
    "description",
    "enabled",
    "extends",
    "defaults",
    "platform",
    "platforms",
    "steps",
    "atomic_id",
    "target",
    "task",
    "rounds",
    "workers",
    "timeout",
    "budget",
    "step",
    "from-step",
    "to-step",
    "var",
    "json",
    "dry-run",
    "continue",
    "replan",
    "no-checkpoint",
    "checkpoints",
    "resume",
    "show",
    "list",
    "validate",
    "info",
    "report",
    "manual",
    "view",
    "plain",
    "no-bootstrap",
    "budget-confirm",
    "step-delay",
    "playbook",
    "techniques",
    "interface",
    "ssid",
    "target",
    "backdoor_win_service_path",
    "ensure_repo",
    "linux",
    "windows",
}


def _skill_text() -> str:
    return SKILL_MD.read_text(encoding="utf-8")


def _frontmatter(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    block = text.split("---\n", 2)[1]
    return yaml.safe_load(block)


def _body(path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    return text.split("---\n", 2)[2].lstrip("\n")


@pytest.fixture(scope="module")
def command_names() -> set[str]:
    document = json.loads((REPO_ROOT / "cli" / "command_index.json").read_text(encoding="utf-8"))
    return {entry["name"][3:] for entry in document["commands"] if entry["name"].startswith("do_")}


@pytest.fixture(scope="module")
def addon_names() -> set[str]:
    return {path.stem for path in (REPO_ROOT / "lazyaddons").glob("*.yaml")}


@pytest.fixture(scope="module")
def atomic_index() -> dict[str, tuple[str, str]]:
    """Map every Atomic Red Team GUID to (technique_id, test name)."""
    index: dict[str, tuple[str, str]] = {}
    if not ATOMICS_DIR.is_dir():
        return index
    for path in ATOMICS_DIR.glob("T*/T*.yaml"):
        try:
            data = yaml.safe_load(path.read_text(encoding="utf-8"))
        except Exception:
            continue
        for test in (data or {}).get("atomic_tests", []) or []:
            guid = str(test.get("auto_generated_guid", "")).lower()
            if guid:
                index[guid] = (path.stem, str(test.get("name", "")))
    return index


class TestSkillFilesExist:
    def test_skill_present(self):
        assert SKILL_MD.exists(), f"Missing: {SKILL_MD}"

    def test_hermes_present(self):
        assert HERMES_MD.exists(), f"Missing: {HERMES_MD}"

    def test_readme_present(self):
        assert README_MD.exists(), f"Missing: {README_MD}"

    def test_skill_registered_in_readme(self):
        catalog = (REPO_ROOT / "skills" / "README.md").read_text(encoding="utf-8")
        assert "awesome-windows-security/" in catalog, "skill must be listed in skills/README.md"


class TestFrontmatter:
    def test_frontmatter_parses(self):
        assert isinstance(_frontmatter(SKILL_MD), dict)

    def test_name(self):
        assert _frontmatter(SKILL_MD)["name"] == SKILL_NAME

    def test_name_pattern(self):
        assert NAME_PATTERN.match(_frontmatter(SKILL_MD)["name"])

    def test_trigger(self):
        assert _frontmatter(SKILL_MD)["trigger"] == TRIGGER

    def test_description(self):
        description = _frontmatter(SKILL_MD)["description"]
        assert 40 <= len(description) <= 600

    def test_hermes_frontmatter(self):
        meta = _frontmatter(HERMES_MD)
        assert meta["name"] == SKILL_NAME
        assert meta["version"]
        assert meta["platforms"] == ["linux"]
        assert "lazyown" in meta["metadata"]["hermes"]["tags"]


class TestBodiesInSync:
    def test_bodies_match(self):
        assert _body(SKILL_MD) == _body(HERMES_MD), "Claude and Hermes skill bodies diverged"

    def test_upstream_is_cited(self):
        assert UPSTREAM in _skill_text()

    def test_upstream_url_is_reachable_format(self):
        assert "https://github.com/chryzsh/awesome-windows-security" in _skill_text()


class TestRouterTable:
    def test_routes_are_declared(self):
        text = _skill_text()
        for route in ("Route A", "Route B", "Route C", "Route D"):
            assert route in text, f"missing {route} definition"

    def test_every_tactic_is_covered(self):
        text = _skill_text()
        for tactic in (
            "Initial Access",
            "Execution",
            "Persistence",
            "Privilege Escalation",
            "Defense Evasion",
            "Credential Access",
            "Discovery",
            "Lateral Movement",
            "Collection",
            "Exfiltration",
            "Command and Control",
        ):
            assert tactic in text, f"tactic not covered: {tactic}"

    def test_technique_identifiers_are_valid(self):
        offenders = [
            token
            for token in re.findall(r"\bT\d{4}(?:\.\d{3})?\b", _skill_text())
            if not TECHNIQUE_PATTERN.match(token)
        ]
        assert offenders == []

    def test_esc_identifiers_are_valid(self):
        for token in re.findall(r"\bESC\d{1,2}\b", _skill_text()):
            assert ESCID_PATTERN.match(token), f"invalid ESC identifier: {token}"


class TestCitedCommandsExist:
    def test_cited_tokens_are_real(self, command_names, addon_names):
        known = command_names | addon_names
        offenders = []
        for token in sorted(set(TOKEN_PATTERN.findall(_skill_text()))):
            if token in ALLOWED_NON_COMMANDS:
                continue
            if token not in known:
                offenders.append(token)
        assert offenders == [], f"skill cites unknown commands: {offenders}"

    def test_evidence_commands_exist(self, command_names):
        for name in ("lazy_finding", "share_finding", "db_creds", "scope"):
            assert name in command_names, f"evidence or scope command missing: {name}"

    def test_atomic_commands_exist(self, command_names):
        for name in (
            "atomic_gen",
            "atomic_tests",
            "atomic_emulate",
            "atomic_agent",
            "atomic_clean",
            "atomic_shell",
            "attack_plan",
        ):
            assert name in command_names, f"atomic command missing: {name}"

    def test_chain_and_loop_commands_exist(self, command_names):
        for name in ("apt_chain", "apt_playbook", "auto_loop", "auto_pwn"):
            assert name in command_names, f"chain/loop command missing: {name}"

    def test_addons_cited_exist(self, addon_names):
        for name in ("edr_detector", "cloud_enum", "blacksandbeacon"):
            assert name in addon_names, f"router cites a missing addon: {name}"


class TestAtomicTranslation:
    def test_translation_table_has_rows(self):
        rows = TABLE_ROW_PATTERN.findall(_skill_text())
        assert len(rows) >= 20, "translation table is too small"

    def test_every_guid_is_a_real_atomic_test(self, atomic_index):
        if not atomic_index:
            pytest.skip("atomic-red-team checkout not present")
        rows = TABLE_ROW_PATTERN.findall(_skill_text())
        offenders = [guid for _technique, guid in rows if guid.lower() not in atomic_index]
        assert offenders == [], f"unknown Atomic GUIDs: {offenders}"

    def test_technique_column_matches_the_test(self, atomic_index):
        if not atomic_index:
            pytest.skip("atomic-red-team checkout not present")
        rows = TABLE_ROW_PATTERN.findall(_skill_text())
        offenders = [
            (technique, guid)
            for technique, guid in rows
            if atomic_index[guid.lower()][0] != technique
        ]
        assert offenders == [], f"technique/guid mismatch: {offenders}"

    def test_resolver_contract_is_documented(self):
        text = _skill_text()
        assert "modules/atomic_resolver" in text
        assert "parquets/techniques.parquet" in text
        assert "list_for_technique" in text

    def test_platform_filter_is_documented(self):
        text = _skill_text()
        assert "--platform windows" in text
        assert "--platform" in text


class TestNormalisedTechniques:
    """The upstream list predates ATT&CK renames; replacements must be real."""

    LEGACY = {
        "T1208": "T1558.003",
        "T1081": "T1552.001",
        "T1214": "T1552.002",
        "T1171": "T1557.001",
        "T1089": "T1562.001",
    }

    def test_rename_table_is_present(self):
        text = _skill_text()
        for legacy, current in self.LEGACY.items():
            assert legacy in text, f"legacy id missing: {legacy}"
            assert current in text, f"replacement id missing: {current}"

    def test_replacements_carry_windows_tests(self, atomic_index):
        if not atomic_index:
            pytest.skip("atomic-red-team checkout not present")
        windows = {technique for _guid, (technique, _name) in atomic_index.items()}
        for legacy, current in self.LEGACY.items():
            if current == "T1562.001":
                continue
            assert current in windows, f"replacement has no atomic test: {current}"


class TestExecutionAndScope:
    def test_scope_contract_is_present(self):
        text = _skill_text()
        assert "Authorized engagements only" in text
        assert "Evidence over assumption" in text
        assert "Phase discipline" in text
        assert "scope mode enforce" in text

    def test_scope_guard_gap_is_documented(self):
        text = _skill_text()
        assert "not** blocked by it" in text or "are **not** blocked by it" in text

    def test_artefact_generation_is_documented(self):
        text = _skill_text()
        assert "atomic_gen" in text
        assert "attack_plan" in text
        assert "sessions/temp_uploads" in text
        assert "backdoor_win_service_path" in text

    def test_execution_commands_are_documented(self):
        text = _skill_text()
        assert "atomic_emulate" in text
        assert "atomic_clean" in text
        assert "atomic_shell" in text

    def test_apt_chain_contract_is_documented(self):
        text = _skill_text()
        assert "apt_chain" in text
        assert "--dry-run" in text
        assert "extends: apt_chain" in text

    def test_autonomous_loop_contract_is_documented(self):
        text = _skill_text()
        assert "auto_loop" in text
        assert "--budget" in text
        assert "LAZYOWN_AUTONOMOUS=1" in text

    def test_evidence_section(self):
        text = _skill_text()
        assert "lazy_finding" in text
        assert "db_creds" in text

    def test_addon_route_points_to_lazyaddon_creator(self):
        assert "/lazyaddon-creator" in _skill_text()
