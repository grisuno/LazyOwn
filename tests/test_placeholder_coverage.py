"""Placeholder coverage across every registry that resolves ``{tokens}``.

Locks the contract that broke silently in production: a placeholder used by
a shipped lazyaddon must resolve at shell runtime, pass the lazyc2 creator
validator, be coercible by the payload schema, and be documented in the
lazyaddon-creator skill. BDD scenarios:
    - Given the live payload plus params/*.yaml, when compared with the
      validator allowlist, no live key is rejected
    - Given every shipped lazyaddon, when its tool templates are scanned,
      every token is either declared or globally known
    - Given every required param without default, when resolved, its key
      exists in the live params so the command cannot abort
    - Given the skill documentation, when compared with the validator,
      no known key is undocumented
"""

from __future__ import annotations

import json
import re
from pathlib import Path

import yaml

from core.payload_schema import SCHEMA
from lazyc2.addon_creator import AddonCreatorConfig

REPO_ROOT = Path(__file__).resolve().parent.parent
TOKEN_RE = re.compile(r"(?<!\{)\{([a-zA-Z_][a-zA-Z0-9_]*)\}(?!\})")
TOOL_FIELDS = (
    "execute_command",
    "install_command",
    "remote_command",
    "lazycommand",
    "upload_file",
    "download_file",
)


def _live_keys() -> set[str]:
    """Union of payload.json and params/*.yaml (the shell self.params)."""
    live = set(json.loads((REPO_ROOT / "payload.json").read_text()).keys())
    for path in sorted((REPO_ROOT / "params").glob("*.yaml")):
        data = yaml.safe_load(path.read_text()) or {}
        live.update(data.keys())
    return live


def _skill_keys() -> set[str]:
    """Known-keys list from the lazyaddon-creator skill Step 4."""
    text = (REPO_ROOT / "skills" / "lazyaddon-creator" / "SKILL.md").read_text()
    block = re.search(r"Known `payload\.json` keys.*?\n```\n(.*?)\n```", text, re.S)
    assert block, "skill known-keys block not found"
    return set(block.group(1).split())


def test_validator_covers_live_keys() -> None:
    """Validator allowlist must accept every key the shell can substitute."""
    allowed = AddonCreatorConfig().payload_placeholders
    assert _live_keys() <= allowed


def test_schema_covers_live_keys() -> None:
    """Payload schema must coerce every key the shell can substitute."""
    assert _live_keys() <= set(SCHEMA.keys())


def test_skill_documents_validator_keys() -> None:
    """Skill doc must document every key the validator accepts."""
    allowed = AddonCreatorConfig().payload_placeholders
    assert allowed <= _skill_keys()


def test_addon_tokens_resolve() -> None:
    """Every tool token is declared in params or globally known."""
    allowed = AddonCreatorConfig().payload_placeholders
    offenders = []
    for path in sorted((REPO_ROOT / "lazyaddons").glob("*.yaml")):
        data = yaml.safe_load(path.read_text())
        if not isinstance(data, dict):
            continue
        tool = data.get("tool", {}) or {}
        declared = {p["name"] for p in (data.get("params") or []) if isinstance(p, dict)}
        for field in TOOL_FIELDS:
            value = tool.get(field, "")
            if not isinstance(value, str):
                continue
            for token in TOKEN_RE.findall(value):
                if token not in declared and token not in allowed:
                    offenders.append(f"{path.name}:{field}:{{{token}}}")
    assert offenders == []


def test_addon_tokens_resolve_at_runtime() -> None:
    """Every token in an enabled addon exists in live shell params.

    YAML ``default:`` values never reach the shell: the wrapper substitutes
    exclusively from ``self.params`` (payload.json plus params/*.yaml), so a
    token missing there renders literally into the executed command.
    """
    live = _live_keys()
    offenders = []
    for path in sorted((REPO_ROOT / "lazyaddons").glob("*.yaml")):
        data = yaml.safe_load(path.read_text())
        if not isinstance(data, dict) or not data.get("enabled", False):
            continue
        tool = data.get("tool", {}) or {}
        for field in TOOL_FIELDS:
            value = tool.get(field, "")
            if not isinstance(value, str):
                continue
            for token in TOKEN_RE.findall(value):
                if token not in live:
                    offenders.append(f"{path.name}:{field}:{{{token}}}")
    assert offenders == []


def test_required_params_exist_live() -> None:
    """Required params without default must exist in live shell params."""
    live = _live_keys()
    offenders = []
    for path in sorted((REPO_ROOT / "lazyaddons").glob("*.yaml")):
        data = yaml.safe_load(path.read_text())
        if not isinstance(data, dict):
            continue
        for param in data.get("params") or []:
            if param.get("required") and "default" not in param and param["name"] not in live:
                offenders.append(f"{path.name}:{{{param['name']}}}")
    assert offenders == []
