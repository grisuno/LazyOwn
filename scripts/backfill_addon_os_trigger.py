"""One-shot backfill: add ``os`` and ``trigger`` keys to every lazyaddon.

This script is idempotent. It scans ``lazyaddons/*.yaml``, classifies each
file via a small heuristic table (filename + repo URL + category), then
inserts ``os`` and ``trigger`` immediately before the ``tool:`` block,
preserving the rest of the YAML formatting verbatim. Files that already
declare both keys are skipped.

Run via ``python3 scripts/backfill_addon_os_trigger.py``. The classifier
errs on the conservative side: when uncertain the file is left with the
safe defaults ``os: any`` and ``trigger: []`` so the addon keeps loading.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
ADDONS_DIR = REPO_ROOT / "lazyaddons"


WINDOWS_NAME_HINTS: tuple[str, ...] = (
    "windows",
    "_win_",
    "win.",
    "dll",
    "powershell",
    "demiguise",
    "shadowlink",
    "gopeinjection",
    "gen_dll_rev",
    "gomulti_loader_windows",
    "hack_browser_data",
    "nullgate",
    "shellcode_custom_win_rev_tcp_xored",
    "pyinmemorype",
    "argfuscator",
    "fragnesia",
    "cgoblin",
    "aurorapatch",
    "wspcoerce",
    "watchguard",
    "laps",
    "pretender",
    "ridenum",
    "clematis",
    "kivi_revshell",
    "orpheus",
    "ebird3",
    "override",
)

LINUX_NAME_HINTS: tuple[str, ...] = (
    "_linux",
    "linux_",
    "linux.",
    "blacksandbeacon",
    "hooka_linux",
    "gomulti_loader_linux",
    "oniux",
    "lazybinenc",
)

NETWORK_NAME_HINTS: tuple[str, ...] = (
    "spoonmap",
    "ptmultitools",
    "lazyftpsniff",
    "lazymapd",
    "hostdiscover",
    "sigploit",
    "peeko",
    "pyrit",
    "bbr",
)

IAAS_NAME_HINTS: tuple[str, ...] = ("stratus_",)

CVE_HINTS: tuple[str, ...] = (
    "cve_",
    "cve-",
)


KNOWN_TRIGGERS: dict[str, tuple[str, ...]] = {
    "evilginx2": ("http", "https", "http-proxy"),
    "CVE-2022-22077": ("microsoft-ds", "msrpc"),
    "CVE_2025_24071_PoC": ("microsoft-ds", "smb"),
    "laps": ("ldap", "microsoft-ds"),
    "pretender": ("netbios-ssn", "microsoft-ds"),
    "ridenum": ("microsoft-ds", "netbios-ssn"),
    "wspcoerce": ("microsoft-ds", "msrpc"),
    "spoonmap": ("microsoft-ds",),
    "sigploit": ("sip", "sccp"),
    "lazyftpsniff": ("ftp", "ftps"),
    "social-engineer-toolkit": ("http", "https"),
    "commix2": ("http", "https"),
    "hellbird": ("ssh",),
    "vulnhuntr": ("http", "https"),
}


def classify_os(filename: str) -> str:
    """Return a MITRE-platform string for the addon based on filename."""

    lower = filename.lower()
    if any(token in lower for token in IAAS_NAME_HINTS):
        return "iaas"
    if any(token in lower for token in NETWORK_NAME_HINTS):
        return "network"
    if any(token in lower for token in WINDOWS_NAME_HINTS):
        return "windows"
    if any(token in lower for token in LINUX_NAME_HINTS):
        return "linux"
    if any(token in lower for token in CVE_HINTS):
        return "windows"
    return "any"


def known_trigger(name: str) -> tuple[str, ...]:
    """Return the curated trigger tuple for an addon, or ``()``."""

    return KNOWN_TRIGGERS.get(name, ())


def render_trigger(trigger: tuple[str, ...]) -> str:
    """Render the trigger field as inline YAML matching the project style."""

    if not trigger:
        return "trigger: []"
    inner = ", ".join(trigger)
    return f"trigger: [{inner}]"


_TOOL_HEADER = re.compile(r"^tool:\s*$", re.MULTILINE)
_OS_HEADER = re.compile(r"^os:\s*\S", re.MULTILINE)
_TRIGGER_HEADER = re.compile(r"^trigger:\s*", re.MULTILINE)


def patch(path: Path) -> str:
    """Return the new file content with ``os`` and ``trigger`` inserted.

    Idempotent: when both keys already exist the original text is
    returned unchanged.
    """

    text = path.read_text(encoding="utf-8")
    has_os = bool(_OS_HEADER.search(text))
    has_trigger = bool(_TRIGGER_HEADER.search(text))
    if has_os and has_trigger:
        return text

    match = _TOOL_HEADER.search(text)
    if match is None:
        return text

    addon_name = path.stem
    os_value = classify_os(addon_name) if not has_os else ""
    trigger_value = known_trigger(addon_name)
    trigger_line = render_trigger(trigger_value) if not has_trigger else ""

    insert_lines: list[str] = []
    if os_value:
        insert_lines.append(f"os: {os_value}")
    if trigger_line:
        insert_lines.append(trigger_line)
    if not insert_lines:
        return text

    insert_block = "\n".join(insert_lines) + "\n"
    return text[: match.start()] + insert_block + text[match.start() :]


def main() -> int:
    """Walk every addon and rewrite files that need backfilling."""

    if not ADDONS_DIR.is_dir():
        print(f"missing {ADDONS_DIR}", file=sys.stderr)
        return 1
    changed = 0
    for path in sorted(ADDONS_DIR.glob("*.yaml")):
        new_text = patch(path)
        if new_text != path.read_text(encoding="utf-8"):
            path.write_text(new_text, encoding="utf-8")
            print(f"patched {path.name}")
            changed += 1
    print(f"done — {changed} file(s) updated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
