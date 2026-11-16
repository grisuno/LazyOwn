"""Beacon kind classification — one home for implant family logic.

Classifies connected implants into runtime families (BlackSandBeacon,
LazyOwn Go agent, Windows C beacon or generic shell implant) and maps
each family to its capability set, BOF catalog slice and capability
command catalog. Both the C2 (``/api/beacon_menu``) and the autonomous
beacon loop consume this contract so menu rendering and loop planning
never disagree about what an implant can do.
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any

GO_BINARY_EXTS = ("", ".exe", ".go")

BEACON_COMMAND_CATALOG: dict[str, list[dict[str, str]]] = {
    "go": [
        {"cmd": "discover:", "label": "Host discovery sweep", "args": ""},
        {"cmd": "portscan:", "label": "Port scan from the beacon", "args": "22,80,443,445,3389"},
        {"cmd": "softenum:", "label": "Software/service enumeration", "args": ""},
        {"cmd": "netconfig:", "label": "Network configuration dump", "args": ""},
        {"cmd": "exfil:", "label": "Exfiltrate a path", "args": ""},
        {"cmd": "download:", "label": "Pull a file from the C2", "args": ""},
        {"cmd": "upload:", "label": "Push a file to the C2", "args": ""},
        {"cmd": "migrate:", "label": "Process migration", "args": ""},
        {"cmd": "shellcode:", "label": "Load shellcode from URL", "args": ""},
        {"cmd": "amsi:", "label": "AMSI bypass (Windows)", "args": ""},
        {"cmd": "persist:", "label": "Persistence", "args": ""},
        {"cmd": "escalatelin:", "label": "Linux escalation", "args": ""},
        {"cmd": "cleanlogs:", "label": "Clear event logs", "args": ""},
    ],
    "bsb": [
        {"cmd": "shell", "label": "Shell command", "args": ""},
    ],
    "c_win": [
        {"cmd": "shell", "label": "Shell command", "args": ""},
    ],
    "linux": [
        {"cmd": "shell", "label": "Shell command", "args": ""},
    ],
    "unknown": [
        {"cmd": "shell", "label": "Shell command", "args": ""},
    ],
}


def detect_beacon_type(
    safe_id: str,
    platform: str,
    bsb_clients: set[str],
    sessions_dir: Path,
) -> tuple[str, str]:
    """Classify one connected implant by its runtime family.

    Args:
        safe_id: Sanitized beacon client id.
        platform: Platform string reported by the beacon ("windows"/"linux").
        bsb_clients: Set of ids known to speak the BlackSandBeacon protocol.
        sessions_dir: Sessions directory holding compiled Go agents.

    Returns:
        Tuple ``(type, label)`` where type is one of ``bsb``, ``go``,
        ``c_win``, ``linux`` or ``unknown``.
    """
    if safe_id in bsb_clients:
        return "bsb", "BlackSandBeacon (C, Linux, BOF/RunELF)"
    for name in (f"{safe_id}", f"l_{safe_id}"):
        for ext in GO_BINARY_EXTS:
            if (Path(sessions_dir) / f"{name}{ext}").is_file():
                goos = (platform or "").strip().lower()
                return "go", f"LazyOwn Go agent ({goos or 'native'})"
    normalized = (platform or "").strip().lower()
    if normalized == "windows":
        return "c_win", "Windows C beacon (COFF BOFs)"
    if normalized == "linux":
        return "linux", "Linux implant (shell)"
    return "unknown", "Unknown implant (shell)"


def beacon_capabilities(beacon_type: str) -> dict[str, Any]:
    """Return the capability flags for one beacon family.

    Args:
        beacon_type: Family from :func:`detect_beacon_type`.

    Returns:
        Dict with ``bof``/``bof_platform``/``shellcode``/``dll``/
        ``atomic``/``loop`` flags.
    """
    if beacon_type == "bsb":
        return {
            "bof": True,
            "bof_platform": "linux",
            "shellcode": False,
            "dll": False,
            "atomic": True,
            "loop": True,
        }
    if beacon_type in ("go", "c_win"):
        return {
            "bof": beacon_type == "c_win",
            "bof_platform": "windows",
            "shellcode": beacon_type == "go",
            "dll": beacon_type == "go",
            "atomic": True,
            "loop": True,
        }
    return {
        "bof": False,
        "bof_platform": "",
        "shellcode": False,
        "dll": False,
        "atomic": True,
        "loop": True,
    }


def beacon_commands(beacon_type: str) -> list[dict[str, str]]:
    """Return the capability command catalog for one beacon family.

    Args:
        beacon_type: Family from :func:`detect_beacon_type`.

    Returns:
        List of ``{cmd, label, args}`` rows (empty for unknown types).
    """
    return list(BEACON_COMMAND_CATALOG.get(beacon_type, []))


def beacon_menu_bofs(capabilities: dict[str, Any], sessions_dir: Path) -> list[dict[str, Any]]:
    """List catalog BOFs compatible with one beacon platform.

    Args:
        capabilities: Flags from :func:`beacon_capabilities`.
        sessions_dir: Sessions directory for the BOF marketplace registry.

    Returns:
        List of BOF summary dicts (name, description, platform, mitre).
    """
    if not capabilities.get("bof"):
        return []
    wanted = str(capabilities.get("bof_platform") or "").strip().lower()
    try:
        from modules.bof_registry import BofMarketplace

        catalog = BofMarketplace(sessions_dir=str(sessions_dir)).catalog
        rows: list[dict[str, Any]] = []
        for entry in catalog.list_all():
            platform = str(getattr(entry, "platform", "")).split(".")[-1].lower()
            if wanted and platform and platform != wanted:
                continue
            rows.append(
                {
                    "name": entry.name,
                    "description": entry.description,
                    "platform": platform,
                    "mitre_technique": entry.mitre_technique,
                    "category": entry.category,
                    "required_args": entry.required_args,
                }
            )
        return rows
    except Exception as exc:
        logging.debug(f"beacon menu bof listing failed: {exc}")
        return []


def beacon_menu_playbooks(repo_root: Path) -> list[dict[str, Any]]:
    """List the APT adversarial playbooks available for chains.

    Args:
        repo_root: Repository root holding ``playbooks/apt_*.yaml``.

    Returns:
        List of playbook summary dicts, empty when the engine is absent.
    """
    try:
        from modules.apt_playbooks import AptPlaybookEngine

        engine = AptPlaybookEngine(playbook_dir=str(Path(repo_root) / "playbooks"))
        return engine.list_playbooks()
    except Exception as exc:
        logging.debug(f"beacon menu playbook listing failed: {exc}")
        return []


__all__ = [
    "BEACON_COMMAND_CATALOG",
    "GO_BINARY_EXTS",
    "beacon_capabilities",
    "beacon_commands",
    "beacon_menu_bofs",
    "beacon_menu_playbooks",
    "detect_beacon_type",
]
