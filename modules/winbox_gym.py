"""WinBox gym catalogue and control-plane bridge.

WinBox (https://github.com/totekuh/winbox) turns a headless Windows VM
(Server Core 2022/2025, Windows 11 or Windows 10) into an isolated
vulnerability-research lab controlled from the operator host. This module
mirrors :mod:`modules.metasploitable_gym` for the gym catalogue (index
playbook, exploit specs, chains) and adds a safe subprocess adapter for
the ``winbox`` CLI so the shell command, the gym matrix runner, the
autonomous loop and the MCP surface share one control plane.

The lab is dual-use and confined by design: the adapter only drives the
operator's own WinBox lab VM (libvirt domain managed by the winbox CLI)
and refuses to run when the binary is missing, falling back to
guidance-only readiness reporting like :mod:`modules.exploitgym_gym`.
"""

from __future__ import annotations

import json
import logging
import os
import re
import shutil
from pathlib import Path
from typing import Any

import yaml

log = logging.getLogger("winbox_gym")

BASE_DIR = Path(__file__).resolve().parent.parent
INDEX_PATH = BASE_DIR / "playbooks" / "gym_winbox.yaml"
EXPLOITS_DIR = BASE_DIR / "exploits"
CHAINS_DIR = BASE_DIR / "chains"
MAX_INDEX_BYTES = 200_000
ID_RE = re.compile(r"^[a-z][a-z0-9_]{0,63}$")
REQUIRED = ("id", "name", "mitre", "port", "service", "severity", "exploit", "chain")

WINBOX_DIR = BASE_DIR / "sessions" / "winbox"
WINBOX_BIN = "winbox"
INSTALL_PATH_DEFAULT = "external/.exploit/winbox"
REPO_URL = "https://github.com/totekuh/winbox.git"
DEFAULT_GUEST_OS = "server2022"
GUEST_OS_OPTIONS = ("server2022", "server2025", "win11", "win10")

STATUS_TIMEOUT_SEC = 60
UP_TIMEOUT_SEC = 900
CLI_TIMEOUT_SEC = 300
EXE_TIMEOUT_MAX = 600
MAX_OUTPUT_CHARS = 20_000
MIN_TIMEOUT_SEC = 5
MAX_TIMEOUT_SEC = 7200
ISO_TIMEOUT_SEC = 3600
BUILD_TIMEOUT_SEC = 2700
INSTALL_TIMEOUT_SEC = 600

PREREQ_BINARIES = (
    "qemu-system-x86_64",
    "virsh",
    "virtiofsd",
    "sshpass",
    "genisoimage",
    "7z",
    "wget",
    "hivexregedit",
)

APT_PACKAGES_FOR: dict[str, str] = {
    "qemu-system-x86_64": "qemu-system-x86",
    "virsh": "libvirt-daemon-system libvirt-clients",
    "virtiofsd": "virtiofsd",
    "sshpass": "sshpass",
    "genisoimage": "genisoimage",
    "7z": "p7zip-full",
    "wget": "wget",
    "hivexregedit": "libwin-hivex-perl",
}

# Distributions ship some daemons outside PATH; vacancy probes try these too.
PREREQ_FALLBACK_PATHS: dict[str, tuple[str, ...]] = {
    "virtiofsd": ("/usr/libexec/virtiofsd", "/usr/lib/virtiofsd"),
}

SETUP_PACKAGES = (
    "qemu-system-x86 qemu-utils libvirt-daemon-system virtinst libguestfs-tools "
    "virtiofsd p7zip-full genisoimage sshpass wget libwin-hivex-perl"
)

_CLI_ACTIONS = (
    "applocker",
    "autologin",
    "av",
    "binfmt",
    "capture",
    "detonate",
    "dns",
    "domain",
    "down",
    "eventlogs",
    "exec",
    "hosts",
    "iso",
    "jobs",
    "kdbg",
    "msi",
    "net",
    "office",
    "provision",
    "restore",
    "setup",
    "snapshot",
    "ssh",
    "status",
    "suspend",
    "tools",
    "up",
    "upload",
    "vnc",
)
ALLOWED_ACTIONS = frozenset(_CLI_ACTIONS)

_STATE_RE = re.compile(r"(?im)^\s*(?:state|vm\s*state)\s*[:=]\s*([A-Za-z][A-Za-z0-9_ -]{0,39})$")
_IP_RE = re.compile(r"(?i)\bip(?:address)?\s*[:=]\s*(\d{1,3}(?:\.\d{1,3}){3})")
_ANY_IP_RE = re.compile(r"\b(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\b")


def _load_yaml(path: Path) -> dict:
    """Read a YAML mapping with a size cap."""
    if not path.is_file() or path.stat().st_size > MAX_INDEX_BYTES:
        return {}
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8", errors="replace"))
    except Exception as exc:
        log.warning("winbox gym index unreadable: %s", exc)
        return {}
    return data if isinstance(data, dict) else {}


# ---------------------------------------------------------------------------
# Gym catalogue (same contract as metasploitable_gym)
# ---------------------------------------------------------------------------


def load_index(path: Path | str = INDEX_PATH) -> dict:
    """Load the gym index, returning an empty mapping on failure."""
    return _load_yaml(Path(path))


def vulnerabilities(path: Path | str = INDEX_PATH) -> list[dict]:
    """Return every indexed lab vector."""
    entries = load_index(path).get("vulnerabilities") or []
    return [dict(item) for item in entries if isinstance(item, dict)]


def get(vuln_id: str, path: Path | str = INDEX_PATH) -> dict | None:
    """Return one lab vector by id, or None."""
    wanted = str(vuln_id or "").strip()
    for item in vulnerabilities(path):
        if item.get("id") == wanted:
            return item
    return None


def chain_for(vuln_id: str, path: Path | str = INDEX_PATH):
    """Return the resolved chain for one lab vector, or None."""
    item = get(vuln_id, path)
    if item is None:
        return None
    from modules.chain_registry import get as get_chain

    return get_chain(str(item.get("chain", "")), CHAINS_DIR)


def exploit_for(vuln_id: str, path: Path | str = INDEX_PATH):
    """Return the exploit spec for one lab vector, or None."""
    item = get(vuln_id, path)
    if item is None:
        return None
    from modules.atomic_exploit_bridge import load_all

    return load_all(EXPLOITS_DIR).get(str(item.get("exploit", "")))


def validate_matrix(path: Path | str = INDEX_PATH) -> list[str]:
    """Validate the index, exploit files and chains as one matrix."""
    errors: list[str] = []
    index = load_index(path)
    if not index:
        return [f"index unreadable or missing: {path}"]
    if index.get("version") != 1:
        errors.append(f"unsupported index version: {index.get('version')!r}")
    entries = index.get("vulnerabilities")
    if not isinstance(entries, list) or not entries:
        return ["vulnerabilities must be a non-empty list"]
    try:
        from modules.atomic_exploit_bridge import load_all as load_exploits
        from modules.chain_registry import get as get_chain

        exploits = load_exploits(EXPLOITS_DIR)
    except Exception as exc:
        return [f"catalogue unavailable: {exc}"]
    seen: set[str] = set()
    for entry in entries:
        if not isinstance(entry, dict):
            errors.append("vulnerability entry must be a mapping")
            continue
        vuln_id = str(entry.get("id", "") or "")
        for key in REQUIRED:
            if not str(entry.get(key, "") or "").strip():
                errors.append(f"{vuln_id}: missing {key}")
        if not ID_RE.match(vuln_id):
            errors.append(f"invalid vulnerability id: {vuln_id!r}")
            continue
        if vuln_id in seen:
            errors.append(f"duplicate vulnerability id: {vuln_id!r}")
        seen.add(vuln_id)
        exploit_id = str(entry.get("exploit", "") or "")
        chain_id = str(entry.get("chain", "") or "")
        if exploit_id and exploit_id not in exploits:
            errors.append(f"{vuln_id}: exploit {exploit_id!r} not loaded")
        if chain_id:
            chain = get_chain(chain_id, CHAINS_DIR)
            if chain is None:
                errors.append(f"{vuln_id}: chain {chain_id!r} not loaded")
            else:
                if str(chain.defaults.get("exploit", "")) != exploit_id:
                    errors.append(f"{vuln_id}: chain exploit default does not match {exploit_id!r}")
                if str(chain.defaults.get("vuln", "")) != vuln_id:
                    errors.append(f"{vuln_id}: chain vuln default does not match")
    return errors


def summary(path: Path | str = INDEX_PATH) -> dict[str, Any]:
    """Return counts by severity and service for operators."""
    entries = vulnerabilities(path)
    by_severity: dict[str, int] = {}
    by_service: dict[str, int] = {}
    for item in entries:
        severity = str(item.get("severity", "unknown") or "unknown")
        service = str(item.get("service", "unknown") or "unknown")
        by_severity[severity] = by_severity.get(severity, 0) + 1
        by_service[service] = by_service.get(service, 0) + 1
    return {
        "target": load_index(path).get("target", ""),
        "vulnerabilities": len(entries),
        "by_severity": dict(sorted(by_severity.items())),
        "by_service": dict(sorted(by_service.items())),
        "errors": validate_matrix(path),
    }


# ---------------------------------------------------------------------------
# WinBox CLI adapter
# ---------------------------------------------------------------------------


def binary_path() -> str | None:
    """Resolve the winbox executable or None."""
    return shutil.which(WINBOX_BIN)


def ensure_installed(params: dict[str, Any] | None = None, timeout: int = 600) -> dict[str, Any]:
    """Clone and pip-install the upstream WinBox repo when the binary is missing.

    Args:
        params: Live shell params (``winbox_install_path`` override).
        timeout: Wall-clock timeout for the clone and the install.

    Returns:
        Mapping with ``success``, ``path`` and ``message``.
    """
    existing = binary_path()
    if existing:
        return {"success": True, "installed": False, "path": existing}
    params = params or {}
    install_path = Path(str(params.get("winbox_install_path") or Path(BASE_DIR / INSTALL_PATH_DEFAULT)))
    from core.hardening import safe_subprocess_run
    from core.safe_exec import safe_git_clone

    if not install_path.is_dir():
        clone = safe_git_clone(REPO_URL, install_path, timeout=timeout)
        if clone.returncode != 0:
            return {
                "success": False,
                "path": "",
                "message": f"git clone failed: {(clone.stderr or clone.stdout or '').strip()[-300:]}",
            }
    install = safe_subprocess_run(
        ["python3", "-m", "pip", "install", "-e", str(install_path)],
        timeout=timeout,
        capture_output=True,
        reason="winbox lab pip install -e",
    )
    if install.returncode != 0:
        install = safe_subprocess_run(
            ["python3", "-m", "pip", "install", "-e", str(install_path), "--break-system-packages"],
            timeout=timeout,
            capture_output=True,
            reason="winbox lab pip install -e (PEP 668 externally managed fallback)",
        )
    if install.returncode != 0:
        return {
            "success": False,
            "path": str(install_path),
            "message": f"pip install -e failed: {(install.stderr or install.stdout or '').strip()[-300:]}",
        }
    resolved = binary_path()
    if not resolved:
        return {"success": False, "path": str(install_path), "message": "installed but 'winbox' still not in PATH"}
    record_artifact("install", f"installed at {install_path}")
    return {"success": True, "installed": True, "path": resolved}


def _prereq_path(name: str) -> str:
    """Resolve one prerequisite on PATH or at a documented non-PATH location."""
    resolved = shutil.which(name)
    if resolved:
        return resolved
    for candidate in PREREQ_FALLBACK_PATHS.get(name, ()):
        path = Path(candidate)
        try:
            if path.is_file() and os.access(str(path), os.X_OK):
                return str(path)
        except OSError:
            continue
    return ""


def _missing_prereqs() -> list[str]:
    """Return lab host prerequisites that are not installed."""
    return [name for name in PREREQ_BINARIES if not _prereq_path(name)]


def check_readiness(params: dict[str, Any] | None = None) -> dict[str, Any]:
    """Report WinBox lab readiness without installing anything.

    Args:
        params: Live shell params (payload.json plus params/*.yaml).

    Returns:
        Mapping with ``ready``, ``binary``, ``prereqs``, ``vm_built``,
        ``guest_os``, ``install_path`` and ``vm`` state when queryable.
    """
    params = params or {}
    binary = binary_path()
    install_path = str(params.get("winbox_install_path") or Path(BASE_DIR / INSTALL_PATH_DEFAULT))
    guest_os = str(params.get("winbox_os") or DEFAULT_GUEST_OS).strip().lower()
    if guest_os not in GUEST_OS_OPTIONS:
        guest_os = DEFAULT_GUEST_OS
    missing_prereqs = _missing_prereqs()
    vm = vm_status() if binary else {}
    vm_built = bool(binary) and _vm_built_from(vm)
    ready = bool(binary) and not missing_prereqs and vm_built
    return {
        "ready": ready,
        "binary": binary or "",
        "prereqs": {name: bool(_prereq_path(name)) for name in PREREQ_BINARIES},
        "missing_prereqs": missing_prereqs,
        "vm_built": vm_built,
        "guest_os": guest_os,
        "guest_os_options": list(GUEST_OS_OPTIONS),
        "install_path": install_path,
        "repo_url": REPO_URL,
        "vm": vm,
        "setup": {
            "packages": f"sudo apt-get install -y {SETUP_PACKAGES}",
            "clone": f"git clone {REPO_URL} {install_path}",
            "install": f"cd {install_path} && pip install -e '.[mcp]'",
            "iso": "winbox iso download",
            "build": f"winbox setup -y --os {guest_os}",
        },
    }


def ensure_prereqs(timeout: int = INSTALL_TIMEOUT_SEC) -> dict[str, Any]:
    """Install missing lab host prerequisites through apt-get.

    Non-interactive: ``sudo -n`` (fails instead of prompting) when not
    running as root, so the caller can surface manual guidance.

    Args:
        timeout: Wall-clock timeout for apt-get.

    Returns:
        Mapping with ``success``, ``installed`` (packages) and ``missing``
        (binaries still absent).
    """
    missing = _missing_prereqs()
    if not missing:
        return {"success": True, "installed": [], "missing": []}
    packages = sorted({pkg for name in missing for pkg in APT_PACKAGES_FOR.get(name, name).split()})
    if os.geteuid() == 0:
        argv = ["apt-get", "install", "-y", *packages]
    else:
        argv = ["sudo", "-n", "apt-get", "install", "-y", *packages]
    from core.hardening import safe_subprocess_run

    try:
        completed = safe_subprocess_run(
            argv,
            timeout=timeout,
            capture_output=True,
            reason="winbox lab host prerequisites",
        )
    except Exception as exc:
        return {
            "success": False,
            "installed": [],
            "missing": missing,
            "message": f"apt-get failed: {exc}. Run manually: sudo apt-get install -y {SETUP_PACKAGES}",
        }
    if completed.returncode != 0:
        tail = (completed.stderr or completed.stdout or "").strip()[-300:]
        return {
            "success": False,
            "installed": [],
            "missing": missing,
            "message": f"apt-get needs the operator (sudo password?). Run manually: "
            f"sudo apt-get install -y {SETUP_PACKAGES}. Details: {tail}",
        }
    still_missing = _missing_prereqs()
    return {
        "success": not still_missing,
        "installed": packages,
        "missing": still_missing,
        "message": "" if not still_missing else f"binaries still missing: {', '.join(still_missing)}",
    }


def ensure_lab_ready(
    params: dict[str, Any] | None = None,
    *,
    build_timeout: int = BUILD_TIMEOUT_SEC,
    install_timeout: int = INSTALL_TIMEOUT_SEC,
    build_vm: bool = True,
) -> dict[str, Any]:
    """Bring the WinBox lab to attackable state in one idempotent call.

    Stages (each skipped when already satisfied): clone+pip-install the
    upstream repo, apt-get the missing host prerequisites, download the
    guest ISO, build and provision the VM, boot it and bind ``rhost``
    to the VM IP. One-time work (ISO ~4.7 GB, setup ~20 min) happens
    only while the VM is unbuilt.

    Args:
        params: Live shell params (``winbox_install_path``, ``winbox_os``).
        build_timeout: Wall-clock timeout for ``winbox setup -y``.
        install_timeout: Wall-clock timeout for clone/pip/apt.
        build_vm: Whether to run the ISO download + VM build when the VM
            is not built yet.

    Returns:
        Mapping with ``success``, ``stage``, ``ip``, ``message`` and a
        per-stage ``stages`` detail mapping.
    """
    stages: dict[str, Any] = {}
    params = params or {}
    install = ensure_installed(params, timeout=install_timeout)
    stages["install"] = install
    if not install.get("success"):
        return {"success": False, "stage": "install", "stages": stages, "message": install.get("message", "")}
    prereqs = ensure_prereqs(timeout=install_timeout)
    stages["prereqs"] = prereqs
    if not prereqs.get("success"):
        return {"success": False, "stage": "prereqs", "stages": stages, "message": prereqs.get("message", "")}
    vm_built = _vm_built_from(vm_status())
    if build_vm and not vm_built:
        iso = run_cli(["iso", "download"], timeout=ISO_TIMEOUT_SEC)
        stages["iso"] = {"ok": iso.get("ok"), "output": iso.get("output", "")[-800:]}
        if not iso.get("ok"):
            return {"success": False, "stage": "iso", "stages": stages, "message": "winbox iso download failed"}
        build = run_cli(["setup", "-y"], timeout=build_timeout)
        stages["build"] = {"ok": build.get("ok"), "output": build.get("output", "")[-800:]}
        if not build.get("ok"):
            return {"success": False, "stage": "build", "stages": stages, "message": "winbox setup -y failed"}
    up = ensure_vm_running()
    stages["up"] = up
    if not up.get("success"):
        return {"success": False, "stage": "up", "stages": stages, "message": up.get("message", "")}
    ip = str(up.get("ip") or "") or vm_ip()
    if ip:
        resolve_target()
    return {
        "success": bool(ip),
        "stage": "ready" if ip else "resolve",
        "ip": ip,
        "stages": stages,
        "message": f"WinBox lab ready on {ip}" if ip else "WinBox VM up but IP unknown (winbox resolve)",
    }


def run_cli(args: list[str], timeout: int = CLI_TIMEOUT_SEC) -> dict[str, Any]:
    """Run one allowlisted winbox CLI action without a shell.

    Args:
        args: Argument list; ``args[0]`` must be an allowlisted action.
        timeout: Wall-clock timeout in seconds (clamped to
            ``[MIN_TIMEOUT_SEC, MAX_TIMEOUT_SEC]``).

    Returns:
        Mapping with ``ok``, ``code``, ``output`` and ``stderr``.

    Raises:
        ValueError: On empty args, unknown action or oversized timeout.
    """
    if not args or not str(args[0]).strip():
        raise ValueError("args must start with a winbox action")
    action = str(args[0]).strip().lower()
    if action not in ALLOWED_ACTIONS:
        raise ValueError(f"winbox action not allowed: {action!r}")
    try:
        timeout = int(timeout)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"invalid timeout: {timeout!r}") from exc
    timeout = max(MIN_TIMEOUT_SEC, min(MAX_TIMEOUT_SEC, timeout))
    binary = binary_path()
    if not binary:
        return {
            "ok": False,
            "code": 127,
            "output": f"[skip] '{WINBOX_BIN}' is not installed; run the setup steps from winbox status.",
            "stderr": "",
        }
    from core.hardening import safe_subprocess_run

    try:
        completed = safe_subprocess_run(
            [binary] + [str(arg) for arg in args],
            timeout=timeout,
            capture_output=True,
            reason=f"winbox lab action {action}",
        )
    except Exception as exc:
        return {"ok": False, "code": -1, "output": "", "stderr": str(exc)}
    output = ((completed.stdout or "") + "\n" + (completed.stderr or ""))[:MAX_OUTPUT_CHARS]
    record_artifact(action, output)
    return {
        "ok": completed.returncode == 0,
        "code": completed.returncode,
        "output": output,
        "stderr": (completed.stderr or "")[:2000],
    }


def vm_status(timeout: int = STATUS_TIMEOUT_SEC) -> dict[str, Any]:
    """Query the WinBox VM state and address.

    Returns:
        Mapping with ``state``, ``ip`` and ``raw``; empty when the CLI
        is unavailable.
    """
    binary = binary_path()
    if not binary:
        return {}
    from core.hardening import safe_subprocess_run

    try:
        completed = safe_subprocess_run(
            [binary, "status"],
            timeout=max(MIN_TIMEOUT_SEC, min(MAX_TIMEOUT_SEC, timeout)),
            capture_output=True,
            reason="winbox vm status",
        )
    except Exception as exc:
        log.debug("winbox status failed: %s", exc)
        return {}
    raw = (completed.stdout or "") + "\n" + (completed.stderr or "")
    state = ""
    match = _STATE_RE.search(raw)
    if match:
        state = match.group(1).strip().lower()
    ip = ""
    match = _IP_RE.search(raw)
    if match:
        ip = match.group(1)
    return {"state": state, "ip": ip, "raw": raw[:MAX_OUTPUT_CHARS]}


def vm_ip() -> str:
    """Return the lab VM IPv4 address, or an empty string."""
    status = vm_status()
    ip = str(status.get("ip") or "")
    if ip:
        return ip
    for candidate in _ANY_IP_RE.findall(status.get("raw") or ""):
        parts = candidate.split(".")
        if all(0 <= int(part) <= 255 for part in parts) and candidate not in ("127.0.0.1", "0.0.0.0"):
            return candidate
    return ""


_NO_VM_STATES = ("", "not found", "unknown")


def _vm_built_from(status: dict[str, Any]) -> bool:
    """Return True when a VM domain exists (any state other than missing)."""
    state = str(status.get("state") or "").strip().lower()
    return state not in _NO_VM_STATES


def resolve_target() -> str:
    """Return the lab VM IP and mirror it into ``payload.json`` rhost."""
    ip = vm_ip()
    if not ip:
        return ""
    try:
        from utils import lazyown_set_config

        lazyown_set_config("rhost", ip)
    except Exception as exc:
        log.debug("rhost mirror skipped: %s", exc)
    return ip


def ensure_vm_running(timeout: int = UP_TIMEOUT_SEC) -> dict[str, Any]:
    """Start the lab VM when it is not running.

    Args:
        timeout: Wall-clock timeout for ``winbox up``.

    Returns:
        Mapping with ``success``, ``ip`` and ``message``.
    """
    if not binary_path():
        return {
            "success": False,
            "ip": "",
            "message": "winbox is not installed; run 'winbox status' for setup guidance.",
        }
    status = vm_status()
    state = str(status.get("state") or "").lower()
    if state == "running":
        ip = str(status.get("ip") or "")
        return {"success": True, "ip": ip, "message": "WinBox VM already running"}
    result = run_cli(["up"], timeout=timeout)
    if not result.get("ok"):
        return {"success": False, "ip": "", "message": (result.get("output") or "winbox up failed").strip()}
    ip = vm_ip()
    return {"success": True, "ip": ip, "message": "WinBox VM is up"}


def record_artifact(name: str, output: str) -> Path | None:
    """Persist one CLI transcript under ``sessions/winbox``.

    Args:
        name: Stable artifact stem (sanitised).
        output: Raw transcript text.

    Returns:
        The written path, or None when nothing was written.
    """
    from core.hardening import sanitize_filename

    stem = sanitize_filename(str(name or "artifact"), max_length=64) or "artifact"
    try:
        WINBOX_DIR.mkdir(parents=True, exist_ok=True)
        path = WINBOX_DIR / f"{stem}.log"
        path.write_text(output or "", encoding="utf-8")
        return path
    except Exception as exc:
        log.debug("winbox artifact write failed: %s", exc)
        return None


def attack_readiness(params: dict[str, Any] | None = None) -> dict[str, Any]:
    """Report whether the autonomous loop can attack the lab right now.

    Args:
        params: Live shell params.

    Returns:
        Mapping with ``attackable``, ``target`` (VM IP when known) and
        ``reasons`` listing what is missing.
    """
    readiness = check_readiness(params)
    reasons: list[str] = []
    if not readiness.get("binary"):
        reasons.append("winbox binary missing")
    if readiness.get("missing_prereqs"):
        reasons.append("missing prereqs: " + ", ".join(readiness["missing_prereqs"]))
    if not readiness.get("vm_built"):
        reasons.append("lab VM not built (winbox setup -y)")
    target = str((readiness.get("vm") or {}).get("ip") or "")
    if readiness.get("vm_built") and not target:
        reasons.append("VM IP unknown (winbox resolve)")
    return {
        "attackable": bool(readiness.get("ready")) and bool(target),
        "target": target,
        "reasons": reasons,
    }


def main() -> None:
    """CLI: list | validate | summary | readiness."""
    import argparse

    parser = argparse.ArgumentParser(description="WinBox gym catalogue")
    sub = parser.add_subparsers(dest="cmd")
    sub.add_parser("list")
    sub.add_parser("validate")
    sub.add_parser("summary")
    sub.add_parser("readiness")
    args = parser.parse_args()
    if args.cmd in ("list", "summary"):
        print(json.dumps(summary(), indent=2))
        return
    if args.cmd == "validate":
        errors = validate_matrix()
        print("OK" if not errors else "\n".join(errors))
        raise SystemExit(0 if not errors else 1)
    if args.cmd == "readiness":
        print(json.dumps(check_readiness(), indent=2))
        return
    parser.print_help()


__all__ = [
    "ALLOWED_ACTIONS",
    "APT_PACKAGES_FOR",
    "BUILD_TIMEOUT_SEC",
    "binary_path",
    "chain_for",
    "ensure_installed",
    "ensure_lab_ready",
    "ensure_prereqs",
    "ensure_vm_running",
    "CHAINS_DIR",
    "DEFAULT_GUEST_OS",
    "EXPLOITS_DIR",
    "GUEST_OS_OPTIONS",
    "INDEX_PATH",
    "REPO_URL",
    "attack_readiness",
    "check_readiness",
    "chain_for",
    "ensure_vm_running",
    "exploit_for",
    "get",
    "load_index",
    "record_artifact",
    "resolve_target",
    "run_cli",
    "summary",
    "validate_matrix",
    "vulnerabilities",
    "vm_ip",
    "vm_status",
]


if __name__ == "__main__":
    main()
