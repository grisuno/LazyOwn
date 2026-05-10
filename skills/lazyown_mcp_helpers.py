"""LazyOwn MCP helper functions — pure logic, no MCP server imports.

This module hosts the analytical / file-system primitives used by the MCP
high-impact tools (target_context, tasks_cleanup, evidence_grep, session_diff,
freshness reporting, dry-run pre-flight, async jobs). Keeping them here makes
the MCP server thin and the logic unit-testable in isolation.
"""

from __future__ import annotations

import csv
import fnmatch
import glob
import json
import os
import re
import shutil
import subprocess
import threading
import time
import uuid
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

DEFAULT_FRESHNESS_THRESHOLD_SECONDS = 7 * 24 * 3600

OS_ID_LINUX = 1
OS_ID_WINDOWS = 2

_TIME_LIKE_RE = re.compile(r"^\d{1,2}:\d{2}(:\d{2}(?:[.,]\d+)?)?$")
_URL_LIKE_RE = re.compile(r"^[a-z][a-z0-9+.-]*://", re.IGNORECASE)
_IP_LIKE_RE = re.compile(r"^\d{1,3}(\.\d{1,3}){3}(:\d+)?$")
_HEX_HASH_RE = re.compile(r"^[a-f0-9]{16,}$", re.IGNORECASE)
_USER_PASS_RE = re.compile(r"^[A-Za-z0-9._@+\-]{1,64}:[^\s]{1,128}$")
_NTLM_PAIR_RE = re.compile(r"^[a-f0-9]{32}:[a-f0-9]{32}$", re.IGNORECASE)


def is_likely_credential(value: str) -> tuple[bool, float, str]:
    """Score whether a string is plausibly a real credential.

    Returns:
        (is_likely, confidence_in_[0,1], reason).
        - timestamps, URLs, bare IPs, and empty values score 0.
        - user:pass and NTLM hash pairs score >=0.85.
        - hex strings of hash length score 0.6 (could be hash).
        - everything else scores 0.3 (unknown).
    """
    if not isinstance(value, str):
        return (False, 0.0, "non_string")
    s = value.strip()
    if not s:
        return (False, 0.0, "empty")
    if _TIME_LIKE_RE.match(s):
        return (False, 0.0, "timestamp")
    if _URL_LIKE_RE.match(s):
        return (False, 0.0, "url")
    if _IP_LIKE_RE.match(s):
        return (False, 0.0, "ip_address")
    if _NTLM_PAIR_RE.match(s):
        return (True, 0.95, "ntlm_pair")
    if _USER_PASS_RE.match(s):
        return (True, 0.9, "user_pass")
    if _HEX_HASH_RE.match(s):
        return (True, 0.6, "hex_hash")
    return (True, 0.3, "unknown")


def evidence_freshness(
    path: Path | str,
    threshold_seconds: int = DEFAULT_FRESHNESS_THRESHOLD_SECONDS,
    now: float | None = None,
) -> dict[str, Any]:
    """Return age + stale flag for an evidence file.

    Args:
        path: Path to a session artefact.
        threshold_seconds: Anything older than this is marked stale.
        now: Override current time (for tests).

    Returns:
        {exists, size, mtime, age_seconds, age_human, stale, threshold_seconds}.
        If the file does not exist all numeric fields are 0 and exists=False.
    """
    p = Path(path)
    if not p.exists():
        return {
            "path": str(p),
            "exists": False,
            "size": 0,
            "mtime": 0,
            "mtime_iso": "",
            "age_seconds": 0,
            "age_human": "",
            "stale": False,
            "threshold_seconds": threshold_seconds,
        }
    st = p.stat()
    cur = now if now is not None else time.time()
    age = max(0, int(cur - st.st_mtime))
    return {
        "path": str(p),
        "exists": True,
        "size": st.st_size,
        "mtime": int(st.st_mtime),
        "mtime_iso": datetime.fromtimestamp(st.st_mtime, tz=timezone.utc).isoformat(),
        "age_seconds": age,
        "age_human": _format_age(age),
        "stale": age > threshold_seconds,
        "threshold_seconds": threshold_seconds,
    }


def _format_age(seconds: int) -> str:
    """Return a compact human age string (e.g. '3h12m', '4d')."""
    if seconds < 60:
        return f"{seconds}s"
    if seconds < 3600:
        return f"{seconds // 60}m"
    if seconds < 86400:
        return f"{seconds // 3600}h{(seconds % 3600) // 60}m"
    days = seconds // 86400
    hours = (seconds % 86400) // 3600
    return f"{days}d{hours}h" if hours else f"{days}d"


def parse_task_value(title: str) -> dict[str, Any] | None:
    """Extract the embedded JSON-ish payload from a task title.

    Tasks created by the WorldModelWatcher have titles like:
      'Leverage new credential: {"value": "...", "host": "...", ...}'
    The string can be truncated. This helper returns whatever fields it can
    parse (best-effort), or None if nothing structured is found.
    """
    m = re.search(r"\{.*", title)
    if not m:
        return None
    chunk = m.group(0)
    try:
        return json.loads(chunk)
    except json.JSONDecodeError:
        pass
    fields: dict[str, Any] = {}
    for key in ("value", "host", "service", "confirmed"):
        rx = re.search(rf'"{key}"\s*:\s*"([^"]*)"', chunk)
        if rx:
            fields[key] = rx.group(1)
    rx_bool = re.search(r'"confirmed"\s*:\s*(true|false)', chunk)
    if rx_bool:
        fields["confirmed"] = rx_bool.group(1) == "true"
    return fields or None


@dataclass
class TaskAudit:
    """Outcome of evaluating a single task entry."""

    task_id: Any
    title: str
    status: str
    keep: bool
    reason: str
    confidence: float
    parsed_value: str | None = None


def audit_tasks(tasks: list[dict[str, Any]], min_confidence: float = 0.5) -> list[TaskAudit]:
    """Classify each task as keep/drop with a reason.

    Tasks whose embedded credential value parses as a timestamp / URL / IP
    are flagged drop. Generic recon and objective tasks are kept.
    """
    out: list[TaskAudit] = []
    seen_titles: set[str] = set()
    for t in tasks:
        title = (t.get("title") or "").strip()
        tid = t.get("id")
        status = t.get("status", "?")
        if title in seen_titles and status not in ("Done", "Qa"):
            out.append(TaskAudit(tid, title, status, False, "duplicate_title", 0.0))
            continue
        seen_titles.add(title)

        if "Leverage new credential" in title:
            parsed = parse_task_value(title)
            value = parsed.get("value", "") if parsed else ""
            ok, conf, reason = is_likely_credential(value)
            if ok and conf >= min_confidence:
                out.append(TaskAudit(tid, title, status, True, f"cred_{reason}", conf, value))
            else:
                out.append(TaskAudit(tid, title, status, False, f"bogus_cred_{reason}", conf, value))
            continue

        out.append(TaskAudit(tid, title, status, True, "non_credential_task", 1.0))
    return out


def find_credential_provenance(
    value: str,
    sessions_dir: Path | str,
    csv_name: str = "LazyOwn_session_report.csv",
) -> dict[str, Any] | None:
    """Locate where a credential was first observed.

    Searches sessions/credentials*.txt and the session CSV log for the
    value. Returns {source_file, line_no, captured_at, command} or None.
    """
    base = Path(sessions_dir)
    if not value:
        return None
    needle = value.strip()

    for fp in sorted(base.glob("credentials*.txt")):
        try:
            with fp.open("r", errors="replace") as fh:
                for i, line in enumerate(fh, start=1):
                    if needle in line:
                        st = fp.stat()
                        return {
                            "source_file": str(fp),
                            "line_no": i,
                            "captured_at": datetime.fromtimestamp(
                                st.st_mtime, tz=timezone.utc
                            ).isoformat(),
                            "command": "",
                        }
        except OSError:
            continue

    csv_path = base / csv_name
    if csv_path.exists():
        try:
            with csv_path.open(newline="", errors="replace") as fh:
                rdr = csv.DictReader(fh)
                for i, row in enumerate(rdr, start=1):
                    blob = " ".join(str(v) for v in row.values() if v)
                    if needle in blob:
                        return {
                            "source_file": str(csv_path),
                            "line_no": i,
                            "captured_at": row.get("timestamp") or row.get("ts") or "",
                            "command": row.get("command") or row.get("cmd") or "",
                        }
        except OSError:
            return None
    return None


_GREP_SCOPES: dict[str, list[str]] = {
    "loot": [
        "credentials*.txt",
        "hash*.txt",
        "passwords*.txt",
        "*/loot/**/*",
    ],
    "nmap": [
        "scan_*.nmap",
        "vulns_*.nmap",
        "scan_*.nmap.xml",
        "*/nmap/**/*",
    ],
    "http": [
        "*/gobuster_*/**/*",
        "*/ffuf_*/**/*",
        "*/nuclei_*/**/*",
        "*/nikto_*/**/*",
        "*/whatweb_*/**/*",
        "*/subwfuzz_*/**/*",
    ],
    "logs": [
        "logs/**/*",
        "LazyOwn_session_report.csv",
    ],
}

_GREP_SKIP_EXT = {
    ".png", ".jpg", ".jpeg", ".gif", ".pdf", ".ico", ".bin",
    ".db", ".sqlite", ".pyc", ".tar", ".gz", ".zip", ".kdbx",
    ".woff", ".woff2", ".ttf", ".eot", ".mp3", ".mp4",
}


def evidence_grep(
    pattern: str,
    sessions_dir: Path | str,
    scope: str = "all",
    max_matches: int = 200,
    max_file_bytes: int = 5 * 1024 * 1024,
    case_insensitive: bool = True,
) -> dict[str, Any]:
    """Grep through session artefacts.

    Args:
        pattern: Regex pattern to search for.
        sessions_dir: Root sessions directory.
        scope: 'all' | 'loot' | 'nmap' | 'http' | 'logs'.
        max_matches: Cap on returned matches.
        max_file_bytes: Skip files larger than this to avoid OOM on dumps.
        case_insensitive: Default True.

    Returns:
        {pattern, scope, scanned, truncated, matches: [{path, line_no, line}]}.
    """
    base = Path(sessions_dir)
    flags = re.IGNORECASE if case_insensitive else 0
    try:
        rx = re.compile(pattern, flags)
    except re.error as e:
        return {"error": f"invalid_regex: {e}", "matches": []}

    if scope == "all":
        globs = sum(_GREP_SCOPES.values(), [])
    else:
        globs = _GREP_SCOPES.get(scope, [])

    seen: set[Path] = set()
    matches: list[dict[str, Any]] = []
    scanned = 0
    truncated = False

    for g in globs:
        for fp in base.glob(g):
            if not fp.is_file() or fp in seen:
                continue
            seen.add(fp)
            if fp.suffix.lower() in _GREP_SKIP_EXT:
                continue
            try:
                if fp.stat().st_size > max_file_bytes:
                    continue
                scanned += 1
                with fp.open("r", errors="replace") as fh:
                    for i, line in enumerate(fh, start=1):
                        if rx.search(line):
                            matches.append({
                                "path": str(fp.relative_to(base)),
                                "line_no": i,
                                "line": line.rstrip("\n")[:240],
                            })
                            if len(matches) >= max_matches:
                                truncated = True
                                break
            except OSError:
                continue
            if truncated:
                break
        if truncated:
            break

    return {
        "pattern": pattern,
        "scope": scope,
        "scanned": scanned,
        "match_count": len(matches),
        "truncated": truncated,
        "matches": matches,
    }


def collect_pwntomate_evidence(rhost: str, sessions_dir: Path | str) -> list[dict[str, Any]]:
    """List pwntomate output dirs for a target with per-dir freshness.

    Returns one entry per discovered tool directory:
      {host, port, tool, files, age_seconds, stale}.
    """
    base = Path(sessions_dir)
    out: list[dict[str, Any]] = []
    if not rhost:
        return out
    target_root = base / rhost
    if not target_root.is_dir():
        return out
    for port_dir in sorted(target_root.iterdir()):
        if not port_dir.is_dir():
            continue
        for tool_dir in sorted(port_dir.iterdir()):
            if not tool_dir.is_dir():
                continue
            files = list(tool_dir.rglob("*"))
            if not files:
                continue
            newest = max((f.stat().st_mtime for f in files if f.is_file()), default=0)
            age = max(0, int(time.time() - newest)) if newest else 0
            out.append({
                "host": rhost,
                "port": port_dir.name,
                "tool": tool_dir.name,
                "files": sum(1 for f in files if f.is_file()),
                "age_seconds": age,
                "age_human": _format_age(age),
                "stale": age > DEFAULT_FRESHNESS_THRESHOLD_SECONDS,
            })
    return out


def build_target_context(
    host: str,
    port: int | None,
    sessions_dir: Path | str,
    payload: dict[str, Any] | None = None,
    world_model: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Aggregate everything known about (host, port) into one structure.

    Reads from sessions/, world_model.json, scan_<host>.nmap, pwntomate
    outputs, credentials*.txt. Designed to replace 4-5 separate lookups
    when an LLM is deciding on next steps for a target.
    """
    base = Path(sessions_dir)
    payload = payload or {}
    wm = world_model or {}

    nmap_scan = base / f"scan_{host}.nmap"
    nmap_vulns = base / f"vulns_{host}.nmap"
    nmap_xml = base / f"scan_{host}.nmap.xml"

    open_ports: list[dict[str, Any]] = []
    if nmap_scan.exists():
        try:
            for line in nmap_scan.read_text(errors="replace").splitlines():
                stripped = line.strip()
                if "/tcp" in stripped and "open" in stripped:
                    parts = stripped.split()
                    p_proto = parts[0] if parts else ""
                    p_num = p_proto.split("/")[0] if "/" in p_proto else p_proto
                    try:
                        p_int = int(p_num)
                    except ValueError:
                        continue
                    open_ports.append({
                        "port": p_int,
                        "protocol": "tcp",
                        "service": parts[2] if len(parts) > 2 else "",
                        "raw": stripped[:200],
                    })
        except OSError:
            pass

    if port is not None:
        open_ports = [p for p in open_ports if p["port"] == int(port)]

    creds: list[dict[str, Any]] = []
    for c in wm.get("credentials", []):
        if c.get("host") and c["host"] != host:
            continue
        if port is not None and c.get("port") and int(c.get("port") or 0) != int(port):
            continue
        ok, conf, reason = is_likely_credential(str(c.get("value", "")))
        item = dict(c)
        item.update({
            "is_likely_credential": ok,
            "confidence": conf,
            "classification": reason,
        })
        prov = find_credential_provenance(str(c.get("value", "")), base)
        if prov:
            item["provenance"] = prov
        creds.append(item)

    pwn = collect_pwntomate_evidence(host, base)
    if port is not None:
        pwn = [e for e in pwn if str(e["port"]) == str(port)]

    vulns: list[dict[str, Any]] = []
    for v in wm.get("vulnerabilities", []):
        if v.get("host") and v["host"] != host:
            continue
        vulns.append(v)

    nmap_evidence = {
        "scan": evidence_freshness(nmap_scan),
        "vulns": evidence_freshness(nmap_vulns),
        "xml": evidence_freshness(nmap_xml),
    }

    return {
        "host": host,
        "port": port,
        "open_ports": open_ports,
        "credentials": creds,
        "vulnerabilities": vulns,
        "pwntomate_evidence": pwn,
        "nmap_evidence": nmap_evidence,
        "phase": wm.get("current_phase", "recon"),
        "host_state": (wm.get("hosts", {}).get(host, {}) or {}).get("state", "unknown"),
    }


_DUPE_COMMAND_ARTIFACTS: dict[str, list[str]] = {
    "lazynmap": ["scan_{rhost}.nmap", "scan_{rhost}.nmap.xml"],
    "nmap": ["scan_{rhost}.nmap", "scan_{rhost}.nmap.xml"],
    "vulnscan": ["vulns_{rhost}.nmap"],
    "pyautomate": ["{rhost}/"],
    "pwntomate": ["{rhost}/"],
}

_OS_REQUIRED: dict[str, int] = {
    "evil": OS_ID_WINDOWS,
    "evil-winrm": OS_ID_WINDOWS,
    "secretsdump": OS_ID_WINDOWS,
    "bloodhound": OS_ID_WINDOWS,
    "psexec": OS_ID_WINDOWS,
    "winpeas": OS_ID_WINDOWS,
    "linpeas": OS_ID_LINUX,
    "linenum": OS_ID_LINUX,
    "getcap": OS_ID_LINUX,
}

_BINARY_LOOKUP: dict[str, str] = {
    "lazynmap": "nmap",
    "nmap": "nmap",
    "gobuster": "gobuster",
    "ffuf": "ffuf",
    "nikto": "nikto",
    "evil": "evil-winrm",
    "evil-winrm": "evil-winrm",
    "secretsdump": "impacket-secretsdump",
    "crackmapexec": "crackmapexec",
    "cme": "crackmapexec",
    "hashcat": "hashcat",
    "john": "john",
    "linpeas": "linpeas.sh",
    "winpeas": "winpeas.exe",
    "bloodhound": "bloodhound-python",
    "responder": "responder",
    "pyautomate": "pwntomate",
    "pwntomate": "pwntomate",
}


def preflight_command(
    command: str,
    payload: dict[str, Any],
    sessions_dir: Path | str,
) -> dict[str, Any]:
    """Pre-flight a LazyOwn command without executing it.

    Returns a structured assessment:
      {command, base_command, binary, binary_present, os_required, os_match,
       would_duplicate, duplicate_artifacts, missing_payload_keys, ok}.
    Used by lazyown_run_command(dry_run=True) and the CLI dry-run alias.
    """
    base = Path(sessions_dir)
    parts = (command or "").strip().split()
    base_cmd = parts[0] if parts else ""
    rhost = payload.get("rhost", "")
    os_id = payload.get("os_id")
    try:
        os_id_int = int(os_id) if os_id not in (None, "") else None
    except (TypeError, ValueError):
        os_id_int = None

    binary = _BINARY_LOOKUP.get(base_cmd, base_cmd)
    binary_present = shutil.which(binary) is not None if binary else False

    os_required = _OS_REQUIRED.get(base_cmd)
    os_match = True
    if os_required is not None and os_id_int is not None:
        os_match = (os_required == os_id_int)

    duplicate_artifacts: list[dict[str, Any]] = []
    artifacts = _DUPE_COMMAND_ARTIFACTS.get(base_cmd, [])
    for tmpl in artifacts:
        rendered = tmpl.format(rhost=rhost or "?")
        ap = base / rendered.rstrip("/")
        if rendered.endswith("/"):
            if ap.is_dir() and any(ap.iterdir()):
                duplicate_artifacts.append({"path": str(ap), "kind": "dir"})
        else:
            if ap.exists() and ap.stat().st_size > 100:
                duplicate_artifacts.append({
                    "path": str(ap),
                    "kind": "file",
                    "size": ap.stat().st_size,
                })

    missing_keys: list[str] = []
    cmd_lower = base_cmd.lower()
    for key, triggers in (
        ("rhost", {"nmap", "lazynmap", "gobuster", "ffuf", "nikto", "evil",
                   "evil-winrm", "secretsdump", "crackmapexec", "cme",
                   "responder", "pyautomate", "pwntomate", "linpeas", "winpeas"}),
        ("domain", {"bloodhound", "windapsearch", "kerbrute", "ldapsearch", "dig"}),
        ("dirwordlist", {"gobuster", "ffuf"}),
    ):
        if cmd_lower in triggers and not payload.get(key):
            missing_keys.append(key)

    ok = (
        binary_present
        and os_match
        and not duplicate_artifacts
        and not missing_keys
    )

    return {
        "command": command,
        "base_command": base_cmd,
        "binary": binary,
        "binary_present": binary_present,
        "os_required": os_required,
        "os_match": os_match,
        "would_duplicate": bool(duplicate_artifacts),
        "duplicate_artifacts": duplicate_artifacts,
        "missing_payload_keys": missing_keys,
        "ok": ok,
    }


# ── Async job store ──────────────────────────────────────────────────────────

@dataclass
class JobRecord:
    """In-memory record for a backgrounded shell job."""

    job_id: str
    command: str
    state: str = "running"
    started_at: float = field(default_factory=time.time)
    finished_at: float | None = None
    exit_code: int | None = None
    stdout: str = ""
    stderr: str = ""
    timeout: int = 0


class JobStore:
    """Thread-safe in-memory store for run_command_async jobs."""

    def __init__(self, max_jobs: int = 64) -> None:
        self._jobs: dict[str, JobRecord] = {}
        self._lock = threading.Lock()
        self._max = max_jobs

    def submit(self, command: str, runner, timeout: int = 300) -> str:
        """Start a runner(command, timeout) in a background thread."""
        job_id = uuid.uuid4().hex[:12]
        rec = JobRecord(job_id=job_id, command=command, timeout=timeout)
        with self._lock:
            self._jobs[job_id] = rec
            if len(self._jobs) > self._max:
                drop = sorted(
                    self._jobs.values(),
                    key=lambda r: r.finished_at or r.started_at,
                )[: len(self._jobs) - self._max]
                for r in drop:
                    if r.state in ("done", "failed"):
                        self._jobs.pop(r.job_id, None)

        def _worker() -> None:
            try:
                out = runner(command, timeout)
                with self._lock:
                    rec.stdout = out if isinstance(out, str) else str(out)
                    rec.state = "done"
                    rec.exit_code = 0
                    rec.finished_at = time.time()
            except Exception as exc:
                with self._lock:
                    rec.stderr = repr(exc)
                    rec.state = "failed"
                    rec.exit_code = 1
                    rec.finished_at = time.time()

        threading.Thread(target=_worker, daemon=True, name=f"mcp-job-{job_id}").start()
        return job_id

    def status(self, job_id: str) -> dict[str, Any] | None:
        with self._lock:
            rec = self._jobs.get(job_id)
            return asdict(rec) if rec else None

    def list(self, limit: int = 20) -> list[dict[str, Any]]:
        with self._lock:
            ordered = sorted(
                self._jobs.values(),
                key=lambda r: r.started_at,
                reverse=True,
            )
            return [asdict(r) for r in ordered[:limit]]


# ── Session diff snapshots ───────────────────────────────────────────────────

SNAPSHOT_FILE_NAME = "_mcp_session_snapshot.json"


def take_snapshot(
    sessions_dir: Path | str,
    payload: dict[str, Any] | None = None,
    world_model: dict[str, Any] | None = None,
    tasks: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    """Capture a lightweight snapshot of the campaign state.

    Stored at sessions/_mcp_session_snapshot.json. Includes file inventory
    plus credential/task counts so a later diff can show what changed.
    """
    base = Path(sessions_dir)
    base.mkdir(parents=True, exist_ok=True)
    inventory: dict[str, int] = {}
    for fp in base.rglob("*"):
        if not fp.is_file():
            continue
        rel = str(fp.relative_to(base))
        if rel.startswith("__pycache__"):
            continue
        try:
            st = fp.stat()
            inventory[rel] = f"{st.st_mtime:.6f}:{st.st_size}"
        except OSError:
            continue

    snap = {
        "taken_at": int(time.time()),
        "taken_at_iso": datetime.now(tz=timezone.utc).isoformat(),
        "payload_keys": sorted(list((payload or {}).keys())),
        "rhost": (payload or {}).get("rhost", ""),
        "credentials": [
            str(c.get("value", "")) for c in (world_model or {}).get("credentials", [])
        ],
        "task_ids": [t.get("id") for t in (tasks or [])],
        "files": inventory,
    }
    out = base / SNAPSHOT_FILE_NAME
    tmp = out.with_suffix(".tmp")
    try:
        tmp.write_text(json.dumps(snap, indent=2))
        os.replace(tmp, out)
    except OSError:
        pass
    return snap


def diff_snapshot(
    sessions_dir: Path | str,
    payload: dict[str, Any] | None = None,
    world_model: dict[str, Any] | None = None,
    tasks: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    """Return what changed since the last snapshot.

    If no prior snapshot exists, returns {first_run: True, ...} so callers
    can choose whether to take one and report nothing.
    """
    base = Path(sessions_dir)
    snap_path = base / SNAPSHOT_FILE_NAME
    if not snap_path.exists():
        return {"first_run": True, "added_files": [], "modified_files": [],
                "removed_files": [], "new_credentials": [], "new_task_ids": []}
    try:
        prev = json.loads(snap_path.read_text())
    except (OSError, json.JSONDecodeError):
        return {"first_run": True, "added_files": [], "modified_files": [],
                "removed_files": [], "new_credentials": [], "new_task_ids": []}

    cur_inventory: dict[str, int] = {}
    for fp in base.rglob("*"):
        if not fp.is_file():
            continue
        rel = str(fp.relative_to(base))
        if rel.startswith("__pycache__") or rel == SNAPSHOT_FILE_NAME:
            continue
        try:
            st = fp.stat()
            cur_inventory[rel] = f"{st.st_mtime:.6f}:{st.st_size}"
        except OSError:
            continue

    prev_files = prev.get("files", {})
    added = sorted(set(cur_inventory) - set(prev_files))
    removed = sorted(set(prev_files) - set(cur_inventory))
    modified = sorted(
        f for f in cur_inventory
        if f in prev_files and cur_inventory[f] != prev_files[f]
    )

    prev_creds = set(prev.get("credentials", []))
    cur_creds = set(str(c.get("value", "")) for c in (world_model or {}).get("credentials", []))
    new_creds = sorted(cur_creds - prev_creds)

    prev_task_ids = set(prev.get("task_ids", []))
    cur_task_ids = set(t.get("id") for t in (tasks or []))
    new_task_ids = sorted(
        i for i in (cur_task_ids - prev_task_ids) if i is not None
    )

    return {
        "first_run": False,
        "snapshot_taken_at": prev.get("taken_at_iso", ""),
        "added_files": added[:200],
        "modified_files": modified[:200],
        "removed_files": removed[:200],
        "added_count": len(added),
        "modified_count": len(modified),
        "removed_count": len(removed),
        "new_credentials": new_creds,
        "new_task_ids": new_task_ids,
    }


# ── Confirmation gate ────────────────────────────────────────────────────────

DESTRUCTIVE_TOOLS: set[str] = {
    "lazyown_c2_command",
    "lazyown_c2_redop",
    "lazyown_c2_adversary",
}


def needs_confirmation(tool_name: str, arguments: dict[str, Any]) -> bool:
    """Return True if tool should require an explicit confirm=True flag."""
    if tool_name in DESTRUCTIVE_TOOLS:
        return not bool(arguments.get("confirm"))
    cmd = (arguments.get("command") or "").lower()
    if cmd and any(k in cmd for k in (
        "rm -rf", "format c:", "shutdown", "reboot",
        "exfil", "wipe", "encrypt-file",
    )):
        return not bool(arguments.get("confirm"))
    return False
