"""Regression guard for pwntomate tool templates (tools/*.tool).

Locks in the contract that broke in production: every ``{placeholder}``
used by a template must be substituted by ``pwntomate._build_substitutions``,
gobuster templates must use valid subcommand syntax, and no rendered command
may contain an empty URL host or a leftover placeholder. Mirrors pwntomate's
own skip rules (empty domain, unresolved placeholder) so the test asserts
exactly the set that would execute.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
TOOLS_DIR = REPO_ROOT / "tools"
PWNTOMATE_PATH = REPO_ROOT / "pwntomate.py"

KNOWN_SUBSTITUTION_KEYS = frozenset(
    {
        "s",
        "ssl_flag",
        "outputdir",
        "ip",
        "port",
        "domain",
        "ext",
        "nameserver",
        "dirworlist",
        "usrwordlist",
        "dnswordlist",
        "baseoutputdir",
        "toolname",
    }
)

CREDENTIAL_MARKERS = frozenset({"username", "password"})

KNOWN_PLACEHOLDERS = KNOWN_SUBSTITUTION_KEYS | CREDENTIAL_MARKERS

_UNRESOLVED_RE = re.compile(r"\{[A-Za-z_]+\}")
_EMPTY_HOST_RE = re.compile(r"https?://(\s|/|:|$)")


def _load_tools() -> dict[str, dict]:
    """Load every tool template keyed by file stem."""
    tools = {}
    for path in sorted(TOOLS_DIR.glob("*.tool")):
        with path.open(encoding="utf-8") as fh:
            tools[path.stem] = json.load(fh)
    assert tools, "no tool templates found under tools/"
    return tools


def _render(template: str, domain: str, tunnel: str) -> str:
    """Render a template the way pwntomate does (minus credentials)."""
    is_ssl = "ssl" in (tunnel or "").lower()
    subs = {
        "s": "s" if is_ssl else "",
        "ssl_flag": " -ssl" if is_ssl else "",
        "outputdir": "/tmp/x/127.0.0.1/8080/t",
        "ip": "127.0.0.1",
        "port": "8080",
        "domain": domain,
        "ext": "com" if domain else "",
        "nameserver": domain.split(".")[0] if domain else "",
        "dirworlist": "/w/dir.txt",
        "usrwordlist": "/w/u.txt",
        "dnswordlist": "/w/d.txt",
        "baseoutputdir": "/tmp/x",
        "toolname": "t",
        "username": "deefbeef",
        "password": "",
    }
    rendered = template
    for key, value in subs.items():
        rendered = rendered.replace("{" + key + "}", value)
    return rendered


def _would_run(template: str, domain: str) -> bool:
    """Mirror pwntomate's skip rules: empty domain / leftover placeholder."""
    if "{domain}" in template and not domain:
        return False
    if _UNRESOLVED_RE.search(_render(template, domain, "")):
        return False
    return True


def test_templates_are_valid_json_with_required_keys():
    """Every template carries toolname/command/trigger/active with sane types."""
    for stem, tool in _load_tools().items():
        assert isinstance(tool.get("toolname"), str) and tool["toolname"], stem
        assert isinstance(tool.get("command"), str) and tool["command"], stem
        assert isinstance(tool.get("active"), bool), stem
        assert isinstance(tool.get("trigger"), list), stem
        if tool["active"]:
            assert tool["trigger"], f"{stem}: active tool needs a trigger"


def test_placeholders_match_pwntomate_substitutions():
    """No template may use a placeholder pwntomate cannot substitute."""
    source = PWNTOMATE_PATH.read_text(encoding="utf-8")
    for key in KNOWN_SUBSTITUTION_KEYS:
        assert f'"{key}"' in source, f"pwntomate lost substitution key: {key}"
    assert "_REDACTOR.render" in source, "pwntomate must render via the credential redactor"
    for stem, tool in _load_tools().items():
        used = set(re.findall(r"\{([A-Za-z_]+)\}", tool["command"]))
        unknown = used - KNOWN_PLACEHOLDERS
        assert not unknown, f"{stem}: unknown placeholders {sorted(unknown)}"


def test_rendered_commands_have_no_empty_host():
    """No executable command may contain an empty URL host (https:/// bug)."""
    for domain in ("", "example.com"):
        for tunnel in ("", "ssl"):
            for stem, tool in _load_tools().items():
                if not _would_run(tool["command"], domain):
                    continue
                rendered = _render(tool["command"], domain, tunnel)
                assert not _EMPTY_HOST_RE.search(rendered), (
                    f"{stem} (domain={domain!r} tunnel={tunnel!r}): empty URL host in: {rendered[:160]}"
                )
                assert not _UNRESOLVED_RE.search(rendered), (
                    f"{stem}: unresolved placeholder in: {rendered[:160]}"
                )


def test_gobuster_templates_use_valid_syntax():
    """gobuster dns takes --domain (never -r URL); dir takes -u with a host."""
    for stem, tool in _load_tools().items():
        command = tool["command"]
        if "gobuster dns" in command:
            assert "-r http" not in command, f"{stem}: gobuster dns must not take -r URL"
            assert "-d " in command, f"{stem}: gobuster dns needs -d/--domain"
        if "gobuster dir" in command:
            assert "-u " in command, f"{stem}: gobuster dir needs -u URL"
            assert "https://{domain}" not in command, (
                f"{stem}: dir URL must not depend on bare {{domain}}"
            )


def test_no_hardcoded_always_ssl_flag():
    """The -ssl flag must be conditional ({ssl_flag}), never hardcoded."""
    for stem, tool in _load_tools().items():
        assert "-ssl {s}" not in tool["command"], (
            f"{stem}: use {{ssl_flag}} so plain ports are not forced through SSL"
        )
