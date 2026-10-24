"""CTF capture verification for gym attack paths.

Turns raw beacon/exploit output into deterministic CTF records under
``sessions/ctf/<vuln_id>/record.json``. A capture succeeds only when a
checker matches the provided evidence output; no manual override exists
so the harness stays replayable.
"""

from __future__ import annotations

import datetime
import json
import logging
import re
from collections.abc import Callable
from pathlib import Path

log = logging.getLogger(__name__)

CTF_DIRNAME = "ctf"
RECORD_NAME = "record.json"

ROOT_SHELL_RE = re.compile(r"uid=0\(([^)]*)\)|uid=0 |nt authority\\system|\buname[^\n]*Linux\s+\w+\s+4\.")
SHADOW_LINE_RE = re.compile(r"^[A-Za-z0-9_.-]+:\$[0-9a-zA-Z]+\$", re.MULTILINE)
CRED_LINE_RE = re.compile(r"^([A-Za-z0-9_.-]+)\s*[:|]\s*(\S+)\s*$", re.MULTILINE)


def output_dir(sessions_dir: str | Path | None = None) -> Path:
    """Resolve the CTF storage directory.

    Args:
        sessions_dir: Optional sessions directory override.

    Returns:
        ``sessions/ctf`` inside the base directory.
    """
    base = Path(sessions_dir) if sessions_dir else Path("sessions")
    return base / CTF_DIRNAME


def _check_root_shell(output: str) -> str:
    """Return root-shell evidence from an output blob, or empty string.

    Args:
        output: Raw command/exploit output text.

    Returns:
        The matched evidence string, or "".
    """
    match = ROOT_SHELL_RE.search(output or "")
    return match.group(0).strip() if match else ""


def _check_shadow_dump(output: str) -> str:
    """Return a password-hash dump evidence line, or empty string.

    Manually created hashes are abbreviated to avoid writing secret
    material into the record.

    Args:
        output: Raw command/exploit output text.

    Returns:
        The masked first matched hash line, or "".
    """
    match = SHADOW_LINE_RE.search(output or "")
    if not match:
        return ""
    line = match.group(0)
    user, _, tail = line.partition(":")
    return f"{user}:$MASKED({tail.count(chr(36))} fields)"


def _check_credentials(output: str) -> str:
    """Return a captured user:pass credential evidence, or empty string.

    Args:
        output: Raw command/exploit output text.

    Returns:
        The first matched ``user:pass`` line, or "".
    """
    for match in CRED_LINE_RE.finditer(output or ""):
        user, password = match.group(1), match.group(2)
        if password in ("x", "!", "*", "bin", "root", "daemon"):
            continue
        if ":" in password or "@" in password or len(password) >= 4:
            return f"{user}:****"
    return ""


CHECKERS: tuple[tuple[str, Callable[[str], str]], ...] = (
    ("root_shell", _check_root_shell),
    ("shadow_dump", _check_shadow_dump),
    ("credentials", _check_credentials),
)


def capture(
    vuln_id: str,
    target: str,
    output: str = "",
    sessions_dir: str | Path | None = None,
) -> dict:
    """Verify output evidence for one gym vector and store the record.

    Args:
        vuln_id: Gym vulnerability id from the index playbook.
        target: Attacked host IP.
        output: Raw artifact output to verify.
        sessions_dir: Optional sessions directory override.

    Returns:
        The stored record dict with ``status`` ``captured`` or ``failed``.

    Raises:
        ValueError: If vuln_id is unknown to the gym index.
    """
    from modules.metasploitable_gym import get as gym_get

    entry = gym_get(vuln_id) or {}
    if not entry:
        raise ValueError(f"Unknown gym vulnerability: {vuln_id}")

    checks: list[dict] = []
    matched = False
    for name, checker in CHECKERS:
        evidence = checker(output)
        checks.append({"name": name, "matched": bool(evidence), "evidence": evidence[:200]})
        matched = matched or bool(evidence)

    record = {
        "vuln_id": vuln_id,
        "cve": str(entry.get("cve") or ""),
        "name": str(entry.get("name") or ""),
        "target": target,
        "mitre": str(entry.get("mitre") or ""),
        "service": str(entry.get("service") or ""),
        "port": str(entry.get("port") or ""),
        "severity": str(entry.get("severity") or "medium"),
        "status": "captured" if matched else "failed",
        "captured_at": datetime.datetime.now(datetime.UTC).isoformat(),
        "checks": checks,
    }
    store_record(record, sessions_dir=sessions_dir)
    log.info("CTF capture %s -> %s", vuln_id, record["status"])
    if record["status"] == "captured":
        _publish_capture_outcome(record)
    return record


def _publish_capture_outcome(record: dict) -> None:
    """Fan the captured path out to the outcome bus listeners.

    Args:
        record: The stored CTF record.
    """
    try:
        from modules.outcome_bus import record_event

        record_event(
            kind="ctf_capture",
            target=str(record.get("target") or ""),
            metadata={
                "vuln_id": record.get("vuln_id"),
                "cve": record.get("cve"),
                "severity": record.get("severity"),
                "artifacts": [str(Path(CTF_DIRNAME) / record.get("vuln_id", "") / RECORD_NAME)],
            },
        )
    except Exception as exc:
        log.debug("ctf_capture outcome skipped: %s", exc)


def record_path(vuln_id: str, sessions_dir: str | Path | None = None) -> Path:
    """Return the record file path for one vulnerability.

    Args:
        vuln_id: Gym vulnerability id.
        sessions_dir: Optional sessions directory override.

    Returns:
        The per-vuln record JSON path.
    """
    return output_dir(sessions_dir) / _safe_dir(vuln_id) / RECORD_NAME


def _safe_dir(vuln_id: str) -> str:
    """Sanitise a vuln id into a directory name.

    Args:
        vuln_id: Raw vulnerability id.

    Returns:
        A slug limited to alphanumerics, dash and underscore.
    """
    slug = re.sub(r"[^a-zA-Z0-9_.-]", "_", str(vuln_id or "unknown"))
    return slug[:80] or "unknown"


def store_record(record: dict, sessions_dir: str | Path | None = None) -> Path:
    """Persist one capture record atomically.

    Args:
        record: Record dict from :func:`capture`.
        sessions_dir: Optional sessions directory override.

    Returns:
        The record file path written.
    """
    path = record_path(str(record.get("vuln_id") or "unknown"), sessions_dir=sessions_dir)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(".tmp")
    tmp.write_text(json.dumps(record, indent=2), encoding="utf-8")
    tmp.replace(path)
    return path


def list_records(sessions_dir: str | Path | None = None) -> dict[str, dict]:
    """Return every stored CTF record keyed by vuln id.

    Args:
        sessions_dir: Optional sessions directory override.

    Returns:
        Mapping ``vuln_id -> record``.
    """
    root = output_dir(sessions_dir)
    records: dict[str, dict] = {}
    if not root.is_dir():
        return records
    for record_file in sorted(root.glob(f"*/{RECORD_NAME}")):
        try:
            data = json.loads(record_file.read_text(encoding="utf-8"))
            if isinstance(data, dict) and data.get("vuln_id"):
                records[str(data["vuln_id"])] = data
        except (OSError, json.JSONDecodeError):
            continue
    return records


def summary(sessions_dir: str | Path | None = None) -> dict:
    """Aggregate capture stats for the report pipeline.

    Args:
        sessions_dir: Optional sessions directory override.

    Returns:
        Dict with count/status/cve/severity breakdowns and the records.
    """
    records = list_records(sessions_dir)
    status_counts: dict[str, int] = {}
    severity_counts: dict[str, int] = {}
    cves: list[str] = []
    for record in records.values():
        status_counts[record["status"]] = status_counts.get(record["status"], 0) + 1
        severity_counts[record["severity"]] = severity_counts.get(record["severity"], 0) + 1
        if record.get("cve"):
            cves.append(record["cve"])
    return {
        "total": len(records),
        "status": status_counts,
        "severity": severity_counts,
        "cves": sorted(set(cves)),
        "records": records,
    }
