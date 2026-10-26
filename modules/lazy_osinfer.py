"""Target OS inference and OS-aware verb gating.

The autonomous loop must never send a Windows-only verb (a shellcode
loader, an AD privesc tool) against a Linux host. This module:

- infers the target OS from a ping reply's TTL (the loop's first step),
  from service banners (RDP/SMB/MSRPC/SQL names) and from nmap OS lines;
- remembers the inferred OS on the global asset graph and the world
  model so every later decision can read it;
- answers whether a verb's target OS is compatible with the host OS,
  so the worker can block a mismatch with a clear reason instead of
  firing a Windows payload at a Linux box.

Stdlib only. Every entry point degrades safely: an unknown OS never
blocks a verb.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SESSIONS_DIR = REPO_ROOT / "sessions"
OS_HINT_FILENAME = "os.json"

OS_LINUX = "linux"
OS_WINDOWS = "windows"
OS_ANY = "any"
OS_UNKNOWN = ""

_TTL_PATTERNS = (
    re.compile(r"\bttl[=\s]+(\d{1,3})\b", re.IGNORECASE),
    re.compile(r"\bTTL[=\s]+(\d{1,3})\b"),
)

# Windows-only service fingerprints from nmap service names/banners.
_WINDOWS_SERVICE_MARKERS = ("msrpc", "netbios-ssn", "netbios-ns", "microsoft-ds", "ms-wbt-server", "rdp", "iis", "ms-sql", "microsoft", "winrm", "smb")
_WINDOWS_BANNER_MARKERS = ("microsoft", "windows", "iis/", "remote desktop", "netbios")
_LINUX_SERVICE_MARKERS = ("linux", "ubuntu", "debian", "centos", "fedora", "openssh", "apache", "nginx", "postfix", "samba")
_LINUX_BANNER_MARKERS = ("linux", "ubuntu", "debian", "centos", "fedora", "gentoo", "unix")

_ASSET_OS_CACHE: dict[str, dict] = {}


def infer_from_ttl(ttl: int | None) -> str:
    """Infer the remote OS family from a reply's TTL value.

    Initial TTLs: 64 for most Linux/Unix stacks, 128 for Windows,
    255 for some network gear. Fewer hops subtract from the initial
    value, so a nearby value (63/127) keeps its verdict.

    Args:
        ttl: Observed TTL, None when unknown.

    Returns:
        ``linux``/``windows``/``unknown``.
    """
    if ttl is None:
        return OS_UNKNOWN
    value = int(ttl)
    if not 0 < value <= 255:
        return OS_UNKNOWN
    if 61 <= value <= 64 or 33 <= value <= 60:
        return OS_LINUX
    if 125 <= value <= 128 or 65 <= value <= 124:
        return OS_WINDOWS
    return OS_UNKNOWN


def infer_from_ping_output(output: str) -> dict:
    """Read ``ttl=``/``TTL=`` from ping output and classify the OS.

    Args:
        output: Raw ping stdout/stderr.

    Returns:
        ``{"os": ..., "ttl": int|None, "reason": str}``.
    """
    text = str(output or "")
    ttl = None
    for pattern in _TTL_PATTERNS:
        match = pattern.search(text)
        if match:
            try:
                ttl = int(match.group(1))
            except ValueError:
                ttl = None
            break
    if ttl is None:
        return {"os": OS_UNKNOWN, "ttl": None, "reason": "no ttl in ping output"}
    os_name = infer_from_ttl(ttl)
    return {"os": os_name, "ttl": ttl, "reason": f"ping ttl {ttl}"}


def infer_from_banner(text: str) -> dict:
    """Infer the OS family from service names or banner text.

    Args:
        text: Concatenated service names / banners for one host.

    Returns:
        ``{"os": ..., "reason": str}``.
    """
    lowered = str(text or "").lower()
    if not lowered.strip():
        return {"os": OS_UNKNOWN, "reason": ""}
    for marker in _WINDOWS_SERVICE_MARKERS + _WINDOWS_BANNER_MARKERS:
        if marker in lowered:
            return {"os": OS_WINDOWS, "reason": f"banner marker '{marker}'"}
    for marker in _LINUX_BANNER_MARKERS:
        if marker in lowered:
            return {"os": OS_LINUX, "reason": f"banner marker '{marker}'"}
    return {"os": OS_UNKNOWN, "reason": ""}


def merge_os(current: str, new: str) -> str:
    """Merge two inferred OS hints; a confident value wins."""
    if new in (OS_LINUX, OS_WINDOWS):
        return new
    return current if current in (OS_LINUX, OS_WINDOWS) else OS_UNKNOWN


# -----------------------------------------------------------------------------
# Verb target OS
# -----------------------------------------------------------------------------


def addon_target_os(name: str) -> str:
    """Return the ``os:`` field of one lazyaddon manifest.

    Args:
        name: Addon name (``hellbird``).

    Returns:
        ``windows``/``linux``/``any`` (default any, unknown addon any).
    """
    if not str(name or "").strip():
        return OS_ANY
    key = str(name).strip().lower()
    try:
        import yaml

        path = REPO_ROOT / "lazyaddons" / f"{key}.yaml"
        if not path.exists():
            return OS_ANY
        data = yaml.safe_load(path.read_text(encoding="utf-8", errors="replace")) or {}
    except Exception:
        return OS_ANY
    os_field = str(data.get("os", OS_ANY) or OS_ANY).strip().lower()
    if os_field in (OS_WINDOWS, OS_LINUX, OS_ANY):
        return os_field
    return OS_ANY


def verb_target_os(command: str) -> str:
    """Return the OS family one command line targets.

    Understands ``lazy addon <name>`` lines, the agent-minted
    ``lazy_addon run <name>`` form (both read the addon manifest) and
    ``auto <verb>`` lines (reads the built-in verb's ``os`` field).
    Plain shell commands always answer ``any``.

    Args:
        command: Resolved shell command line.

    Returns:
        ``windows``/``linux``/``any``.
    """
    text = str(command or "").strip()
    lowered = text.lower()
    if lowered.startswith(("lazy addon ", "lazy_addon ")):
        flat = lowered.replace("_", " ").split()
        run_idx = flat.index("run") + 1 if "run" in flat else -1
        name_idx = 2
        if 0 <= run_idx < len(flat):
            name_idx = run_idx
        if len(flat) > name_idx:
            return addon_target_os(flat[name_idx])
        return OS_ANY
    if lowered.startswith("auto "):
        try:
            from modules.auto_registry import _verb_row

            row = _verb_row(lowered.split()[1])
            if row is not None:
                return str(getattr(row, "os", OS_ANY) or OS_ANY).lower()
        except Exception:
            return OS_ANY
    return OS_ANY


def os_compatible(verb_os: str, host_os: str) -> bool:
    """Whether a verb's target OS may run against a host's inferred OS.

    Unknown hosts (no inference yet) and ``any`` verbs never block; a
    mismatch (windows verb, linux host or the reverse) does.

    Args:
        verb_os: Verb target OS (``any``/``windows``/``linux``).
        host_os: Inferred host OS (``""`` when unknown).

    Returns:
        True when compatible.
    """
    verb = str(verb_os or OS_ANY).lower()
    host = str(host_os or OS_UNKNOWN).lower()
    if verb in (OS_ANY, "", OS_UNKNOWN):
        return True
    if host not in (OS_LINUX, OS_WINDOWS):
        return True
    return verb == host


def verb_compatible_with_host(command: str, host_os: str) -> tuple[bool, str, str]:
    """Gate one command line against a host's inferred OS.

    Args:
        command: Resolved shell command line.
        host_os: Inferred host OS (``""`` when unknown).

    Returns:
        ``(allowed, verb_os, reason)``; reason is empty when allowed.
    """
    verb_os = verb_target_os(command)
    if os_compatible(verb_os, host_os):
        return True, verb_os, ""
    return False, verb_os, (
        f"target os is {host_os} (inferred); verb targets {verb_os} so it cannot run here"
    )


# -----------------------------------------------------------------------------
# Host OS memory
# -----------------------------------------------------------------------------


def host_os_for_target(target: str) -> str:
    """Return the remembered OS for one target host.

    Reads the loop asset graph first, then the world model, then the
    ``sessions/os.json`` hint file. Empty when nothing is known.

    Args:
        target: Host address.

    Returns:
        ``linux``/``windows``/``""``.
    """
    value = str(target or "").strip()
    if not value:
        return OS_UNKNOWN
    try:
        from modules.lazy_loop import AssetGraph

        assets = AssetGraph()
        for node in assets.list("ip") + assets.list("host") + assets.list("subdomain"):
            if node.value == value:
                os_meta = str((node.meta or {}).get("os", "")).lower()
                if os_meta in (OS_LINUX, OS_WINDOWS):
                    return os_meta
    except Exception:
        pass
    try:
        from modules.world_model import read_state_dict

        world = read_state_dict(SESSIONS_DIR / "world_model.json")
        host = (world.get("hosts", {}) or {}).get(value) or {}
        hint = str(host.get("os_hint", "") or "").lower()
        matched = infer_from_banner(hint)
        if matched["os"]:
            return matched["os"]
    except Exception:
        pass
    try:
        data = json.loads((SESSIONS_DIR / OS_HINT_FILENAME).read_text(encoding="utf-8"))
        hint = str(data.get("os", "") or "").lower() if isinstance(data, dict) else str(data or "").lower()
        matched = infer_from_banner(hint)
        if matched["os"]:
            return matched["os"]
    except Exception:
        pass
    return OS_UNKNOWN


def remember_host_os(target: str, os_name: str, reason: str = "") -> bool:
    """Persist an inferred OS on the asset graph and world model.

    Args:
        target: Host address.
        os_name: Inferred OS (``linux``/``windows``); empty clears nothing.
        reason: Why the OS was inferred (``ping ttl 64``).

    Returns:
        True when something was remembered.
    """
    value = str(target or "").strip()
    if not value or os_name not in (OS_LINUX, OS_WINDOWS):
        return False
    remembered = False
    try:
        from modules.lazy_loop import AssetGraph

        assets = AssetGraph()
        for node in assets.list("ip") + assets.list("host"):
            if node.value == value:
                node.meta = dict(node.meta or {})
                if node.meta.get("os") != os_name:
                    node.meta["os"] = os_name
                    node.meta["os_reason"] = str(reason or "")[:120]
                    assets._persist()
                remembered = True
    except Exception:
        pass
    try:
        from modules.world_model import get_world_model

        wm = get_world_model()
        if os_name == OS_LINUX:
            wm.set_os_hint(value, f"Linux (inferred: {reason or 'heuristic'})")
        else:
            wm.set_os_hint(value, f"Windows (inferred: {reason or 'heuristic'})")
        remembered = True
    except Exception:
        pass
    return remembered


def learn_from_transcripts(target: str, transcripts: list[tuple[str, str]]) -> dict:
    """Infer and remember the host OS from executed step outputs.

    Reads every transcript pair looking for ping TTLs and nmap OS
    lines; the strongest inference wins and is persisted.

    Args:
        target: Host address the steps ran against.
        transcripts: ``[(command, output)]`` pairs.

    Returns:
        The inferred record ``{"os", "ttl", "reason"}`` (os "" when unknown).
    """
    best: dict = {"os": OS_UNKNOWN, "ttl": None, "reason": ""}
    for _cmd, output in transcripts or []:
        text = str(output or "")
        if not text:
            continue
        if "ttl=" in text.lower() or "ttl " in text.lower()[:200]:
            inferred = infer_from_ping_output(text)
            if inferred["os"] and not best["os"]:
                best = inferred
        if not best["os"]:
            banner = infer_from_banner(text[:4000])
            if banner["os"]:
                best = {**banner, "ttl": None}
    if best["os"] and target:
        remember_host_os(target, best["os"], best.get("reason", ""))
    return best


__all__ = [
    "OS_LINUX",
    "OS_WINDOWS",
    "OS_ANY",
    "OS_UNKNOWN",
    "addon_target_os",
    "host_os_for_target",
    "infer_from_banner",
    "infer_from_ping_output",
    "infer_from_ttl",
    "learn_from_transcripts",
    "merge_os",
    "os_compatible",
    "remember_host_os",
    "verb_compatible_with_host",
    "verb_target_os",
]
