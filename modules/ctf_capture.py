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
from typing import Any

log = logging.getLogger(__name__)

CTF_DIRNAME = "ctf"
RECORD_NAME = "record.json"

ROOT_SHELL_RE = re.compile(r"uid=0\(([^)]*)\)|uid=0 |nt authority\\system|\buname[^\n]*Linux\s+\w+\s+4\.")
SHADOW_LINE_RE = re.compile(r"^[A-Za-z0-9_.-]+:\$[0-9a-zA-Z]+\$", re.MULTILINE)
CRED_LINE_RE = re.compile(r"^([A-Za-z0-9_.-]+)\s*[:|]\s*(\S+)\s*$", re.MULTILINE)
WINDOWS_OS_ENUM_RE = re.compile(r"(?im)^\s*OS:\s*Windows|^\s*OS Name\s*:", re.MULTILINE)
NETBIOS_NAME_RE = re.compile(r"(?im)^\s*NetBIOS computer name:\s*\S+", re.MULTILINE)
DEFENSE_REPORT_RE = re.compile(r"(?i)RealTimeProtection\w*|AntivirusEnabled|AppLocker|HVCI")
EVENTLOG_CSV_RE = re.compile(r"(?im)^\s*Time\s*,\s*Log\s*,\s*Level\s*,\s*Id\s*,\s*Provider|,\s*Security\s*,")
KERBEROS_TICKET_RE = re.compile(r"\$krb5(?:tgs|asrep)\$[0-9]+\$")
DOMAIN_ENUM_RE = re.compile(r"(?im)namingContexts|sAMAccountName|SidType(?:User|Group|Domain)|user:\[")
SMB_SHARE_RE = re.compile(r"(?im)^\s*\S+:\s+(?:Disk|IPC|Printer)\b|Sharename")


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


def _check_windows_os_enum(output: str) -> str:
    """Return Windows OS fingerprint evidence from a scan blob, or empty string.

    Matches the ``smb-os-discovery`` ``OS:`` line and the ``systeminfo``
    ``OS Name:`` format.

    Args:
        output: Raw command/exploit output text.

    Returns:
        The matched evidence string, or "".
    """
    for pattern in (WINDOWS_OS_ENUM_RE, NETBIOS_NAME_RE):
        match = pattern.search(output or "")
        if match:
            return match.group(0).strip()
    return ""


def _check_defense_report(output: str) -> str:
    """Return a Defender/AppLocker/HVCI posture evidence token, or empty string.

    Args:
        output: Raw command/exploit output text.

    Returns:
        The matched evidence string, or "".
    """
    match = DEFENSE_REPORT_RE.search(output or "")
    return match.group(0).strip() if match else ""


def _check_eventlog_rows(output: str) -> str:
    """Return event-log export evidence (CSV header or Security rows), or "".

    Args:
        output: Raw command/exploit output text.

    Returns:
        The matched evidence string, or "".
    """
    match = EVENTLOG_CSV_RE.search(output or "")
    return match.group(0).strip() if match else ""


def _check_kerberos_ticket(output: str) -> str:
    """Return a masked Kerberos hash token (TGS/AS-REP roast), or "".

    Args:
        output: Raw command/exploit output text.

    Returns:
        The abbreviated hash prefix (secret material never stored), or "".
    """
    match = KERBEROS_TICKET_RE.search(output or "")
    return f"{match.group(0)}<masked>" if match else ""


def _check_domain_enum(output: str) -> str:
    """Return domain enumeration evidence (LDAP context, user, RID), or "".

    Args:
        output: Raw command/exploit output text.

    Returns:
        The matched evidence string, or "".
    """
    match = DOMAIN_ENUM_RE.search(output or "")
    return match.group(0).strip() if match else ""


def _check_smb_shares(output: str) -> str:
    """Return SMB share listing evidence, or "".

    Args:
        output: Raw command/exploit output text.

    Returns:
        The matched evidence string, or "".
    """
    match = SMB_SHARE_RE.search(output or "")
    return match.group(0).strip() if match else ""


CHECKERS: tuple[tuple[str, Callable[[str], str]], ...] = (
    ("root_shell", _check_root_shell),
    ("shadow_dump", _check_shadow_dump),
    ("credentials", _check_credentials),
    ("windows_os_enum", _check_windows_os_enum),
    ("defense_report", _check_defense_report),
    ("eventlog_rows", _check_eventlog_rows),
    ("kerberos_ticket", _check_kerberos_ticket),
    ("domain_enum", _check_domain_enum),
    ("smb_shares", _check_smb_shares),
)


def capture(
    vuln_id: str,
    target: str,
    output: str = "",
    sessions_dir: str | Path | None = None,
    catalogue: Any = None,
) -> dict:
    """Verify output evidence for one gym vector and store the record.

    Args:
        vuln_id: Gym vulnerability id from the index playbook.
        target: Attacked host IP.
        output: Raw artifact output to verify.
        sessions_dir: Optional sessions directory override.
        catalogue: Optional gym catalogue module exposing ``get``;
            defaults to the Metasploitable 2 index.

    Returns:
        The stored record dict with ``status`` ``captured`` or ``failed``.

    Raises:
        ValueError: If vuln_id is unknown to the gym index.
    """
    if catalogue is None:
        from modules.metasploitable_gym import get as gym_get

        catalogue = gym_get
    entry = catalogue(vuln_id) or {}
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


def _gather_evidence(candidates: list[Path]) -> str:
    """Concatenate candidate evidence files for checker verification.

    Args:
        candidates: Text files to scan.

    Returns:
        The concatenated text (capped) for :func:`capture`.
    """
    import itertools

    parts: list[str] = []
    budget = 200_000
    for path in itertools.islice(
        sorted(candidates, key=lambda p: p.stat().st_mtime if p.exists() else 0.0, reverse=True), 50
    ):
        try:
            if path.is_file() and path.stat().st_size <= budget:
                parts.append(path.read_text(errors="replace"))
        except OSError:
            continue
    return "\n".join(parts)


def _cli_capture(argv: list[str]) -> int:
    """CLI entry: verify a vector from staged evidence files.

    Usage:
        python3 modules/ctf_capture.py capture <vuln_id> <target>
               [--output-file PATH] [--search-base DIR ...]

    Without ``--output-file`` the command scans ``--search-base`` trees
    (default ``sessions/``) for text files and verifies the aggregate.

    Args:
        argv: Raw CLI arguments after the script name.

    Returns:
        Process exit code (0 captured, 1 failed, 2 usage error).
    """
    import argparse

    parser = argparse.ArgumentParser(prog="ctf_capture")
    sub = parser.add_subparsers(dest="action", required=True)
    cap = sub.add_parser("capture", help="Verify and record one gym vector")
    cap.add_argument("vuln_id")
    cap.add_argument("target")
    cap.add_argument("--output-file", default="", help="Direct evidence text file")
    cap.add_argument("--search-base", action="append", default=[], help="Directory trees to scan")
    cap.add_argument("--sessions-dir", default="sessions")
    cap.add_argument("--json-out", action="store_true")
    rep = sub.add_parser("report", help="Print the capture summary")
    rep.add_argument("--sessions-dir", default="sessions")

    args_parsed = parser.parse_args(argv)
    if args_parsed.action == "report":
        print(json.dumps(summary(args_parsed.sessions_dir), indent=2))
        return 0
    bases = args_parsed.search_base or [args_parsed.sessions_dir]
    output_dir(args_parsed.sessions_dir).mkdir(parents=True, exist_ok=True)
    if args_parsed.output_file:
        blob = (
            Path(args_parsed.output_file).read_text(errors="replace") if Path(args_parsed.output_file).is_file() else ""
        )
    else:
        candidates: list[Path] = []
        for base in bases:
            tree = Path(base)
            if tree.is_file():
                candidates.append(tree)
                continue
            candidates.extend(tree.glob("**/*.txt") if tree.is_dir() else [])
        blob = _gather_evidence(candidates)
    record = capture(
        args_parsed.vuln_id,
        args_parsed.target,
        output=blob,
        sessions_dir=args_parsed.sessions_dir,
    )
    if args_parsed.json_out:
        print(json.dumps(record, indent=2))
    print(f"ctf_capture: {args_parsed.vuln_id} -> {record['status']}")
    return 0 if record["status"] == "captured" else 1


if __name__ == "__main__":
    import sys

    _REPO_ROOT = str(Path(__file__).resolve().parent.parent)
    if _REPO_ROOT not in sys.path:
        sys.path.insert(0, _REPO_ROOT)
    sys.exit(_cli_capture(sys.argv[1:]))
