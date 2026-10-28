"""AD lab gym catalogue (Docker Samba DC): index, exploits, chains.

Mirrors :mod:`modules.metasploitable_gym` for the ``ad-lab`` scenario: a
single disposable Samba Active Directory DC container (fast to start,
destroyed with ``lab stop ad-lab``). The catalogue binds the
``playbooks/gym_ad_lab.yaml`` index to per-vector exploit specs and
chains so ``gym start`` can auto-launch the golden path.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

import yaml

BASE_DIR = Path(__file__).resolve().parent.parent
INDEX_PATH = BASE_DIR / "playbooks" / "gym_ad_lab.yaml"
EXPLOITS_DIR = BASE_DIR / "exploits"
CHAINS_DIR = BASE_DIR / "chains"
MAX_INDEX_BYTES = 200_000
ID_RE = re.compile(r"^[a-z][a-z0-9_]{0,63}$")
REQUIRED = ("id", "name", "mitre", "port", "service", "severity", "exploit", "chain")


def _load_yaml(path: Path) -> dict:
    """Read a YAML mapping with a size cap."""
    if not path.is_file() or path.stat().st_size > MAX_INDEX_BYTES:
        return {}
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8", errors="replace"))
    except Exception:
        return {}
    return data if isinstance(data, dict) else {}


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
            errors.append(f"{vuln_id}: duplicate vulnerability id: {vuln_id!r}")
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


def readiness() -> dict[str, Any]:
    """Report whether the AD lab container is attackable right now.

    Returns:
        Mapping with ``scenario``, ``container``, ``running`` and
        ``ip`` (empty when Docker is unavailable).
    """
    from modules import lab_runtime

    running = lab_runtime.container_ip(lab_runtime.container_name("ad-lab")) if lab_runtime.docker_available() else ""
    return {
        "scenario": "ad-lab",
        "container": lab_runtime.container_name("ad-lab"),
        "running": bool(running),
        "ip": running,
        "start_hint": "lab start ad-lab",
        "stop_hint": "lab stop ad-lab",
    }


def main() -> None:
    """CLI: list | validate | summary | readiness."""
    import argparse
    import json

    parser = argparse.ArgumentParser(description="AD lab gym catalogue")
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
        print(json.dumps(readiness(), indent=2))
        return
    parser.print_help()


if __name__ == "__main__":
    main()
