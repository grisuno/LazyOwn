"""Read-only campaign index over the sessions directory.

The operator already has every fact the campaign produced (scans, creds,
findings, outcomes, beacon records, world model) persisted under
``sessions/`` but no navigable surface over them. This module turns that
tree into a classified, host-aggregated index with an opinionated
``scope_frontier``: candidate targets ranked with the reasons and the
backing artefacts, so the next scope decision does not require grepping
by hand.

Design contract:
    - Read-only: no method ever writes under the sessions root.
    - Path safe: every relative path resolves through
      :meth:`SessionIndex.resolve_safe` which fails closed on traversal
      or symlink escapes.
    - Injected I/O: the root directory and the clock are injectable, so
      tests run against synthetic trees without touching a live campaign.
    - Pure data in, plain dicts out: no Flask, no cmd2, no C2 imports.
"""

from __future__ import annotations

import fnmatch
import ipaddress
import json
import os
import re
import time
from collections.abc import Callable
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path, PurePosixPath
from typing import Any

from modules.world_model import read_state_dict
from skills.lazyown_mcp_helpers import DEFAULT_FRESHNESS_THRESHOLD_SECONDS, is_likely_credential

READ_CAP_BYTES = 2 * 1024 * 1024
SEARCH_MAX_FILE_BYTES = 5 * 1024 * 1024
SEARCH_MAX_LINE_CHARS = 240
SEARCH_MAX_PATTERN_CHARS = 256
MAX_REGEX_REPEAT_BOUND = 1000
DEFAULT_MAX_MATCHES = 200
ARTIFACTS_CACHE_TTL_SECONDS = 2.0
BEACON_ACTIVE_SECONDS = 600
FRONTIER_UNWORKED_SERVICE_CAP = 3
FRONTIER_SCORE_NEW_HOST = 2
FRONTIER_SCORE_UNWORKED_SERVICE = 1
FRONTIER_SCORE_STALE_RECON = 1
FRONTIER_SCORE_SUCCESS_FINDING = 2
BINARY_SNIFF_BYTES = 8192

_SEARCH_SKIP_SUFFIXES = frozenset(
    {".pcap", ".exe", ".dll", ".bin", ".png", ".jpg", ".jpeg", ".gif", ".gz", ".zip", ".7z", ".so", ".pyc"}
)

SEVERITY_RANK = {"critical": 4, "high": 3, "medium": 2, "low": 1, "info": 0}

KIND_RULES: tuple[tuple[re.Pattern[str], str], ...] = tuple(
    (re.compile(pattern, re.IGNORECASE), kind)
    for pattern, kind in (
        (r"^scan_(?P<host>[\w.\-]+)\.(nmap|xml|gnmap|partial)$", "scan"),
        (r"^(?:.*/)?findings/(?P<host>[\w.\-]+)\.jsonl$", "findings"),
        (r"(?P<client>[\w.\-]+)\.records\.jsonl$", "beacon_history"),
        (r"credentials(?:_(?P<host>[\w.\-]+))?\.txt$", "creds"),
        (r"hash(?:es)?[\w.\-]*?\.txt$", "hashes"),
        (r"^outcomes\.jsonl$", "outcomes"),
        (r"^world_model\.json(?:\.encrypted)?$", "world_model"),
        (r"^beacons\.json$", "beacons"),
        (r"^tasks\.json$", "tasks"),
        (r"^lazy/activity_(?P<task>t\d+)\.jsonl$", "loop_run"),
        (r"^evidence/", "evidence"),
        (r"^loot/", "loot"),
        (r"^reports/", "report"),
        (r"nuclei.*output\.txt$", "nuclei"),
        (r"^engagement\.log$", "engagement_log"),
        (r"_cli_transcript\.jsonl$", "transcript"),
        (r"^sessions_scan_[\w.\-]+\.json$", "scan_summary"),
    )
)

_HOST_IN_PATH_RE = re.compile(r"(?<![\d.])(\d{1,3}(?:\.\d{1,3}){3})(?![\d.])")

_SAFE_REL_SEGMENT_RE = re.compile(r"^[A-Za-z0-9._\-+=@:,()\[\] ]+$")

_SEARCH_PATTERN_CHARS_RE = re.compile(r"^[\w\s.^$*+?{}\[\]()|\\/@#%&=!:,~\"'<>_-]*$", re.ASCII)
_SEARCH_NESTED_QUANTIFIER_RE = re.compile(r"\((?:[^()\\]|\\.)*(?:[+*]|\{\d+,\})\)(?:[*+]|\{\d+,\})")
_SEARCH_BOUNDED_REPEAT_RE = re.compile(r"\{(\d+)(?:,(\d*))?\}")


def _validate_relative_segments(clean: str, original: str) -> None:
    """Reject sessions-relative paths with unsafe segments or characters.

    Args:
        clean: Normalised relative path (forward slashes, no NULs).
        original: The caller-supplied value, used in error messages.

    Raises:
        PermissionError: On empty, dot, dot-dot or non-allowlist segments.
    """
    for segment in clean.split("/"):
        if segment in ("", ".", ".."):
            raise PermissionError(f"unsafe path segment in sessions path: {original}")
        if not _SAFE_REL_SEGMENT_RE.fullmatch(segment):
            raise PermissionError(f"unsafe characters in sessions path: {original}")


def _validate_search_pattern(pattern: str) -> str | None:
    """Check a user-supplied regex for length, charset and ReDoS hazards.

    Args:
        pattern: Candidate regular expression.

    Returns:
        ``None`` when the pattern is safe, else a short reason string.
    """
    if not pattern or len(pattern) > SEARCH_MAX_PATTERN_CHARS:
        return f"pattern too long (max {SEARCH_MAX_PATTERN_CHARS} chars)"
    if "\x00" in pattern:
        return "pattern contains null byte"
    if not _SEARCH_PATTERN_CHARS_RE.fullmatch(pattern):
        return "pattern contains disallowed characters"
    if _SEARCH_NESTED_QUANTIFIER_RE.search(pattern):
        return "pattern contains nested unbounded quantifier"
    for repeat in _SEARCH_BOUNDED_REPEAT_RE.finditer(pattern):
        low = int(repeat.group(1))
        high = int(repeat.group(2)) if repeat.group(2) else low
        if low > MAX_REGEX_REPEAT_BOUND or high > MAX_REGEX_REPEAT_BOUND:
            return f"pattern repeat bound exceeds {MAX_REGEX_REPEAT_BOUND}"
    return None


@dataclass(frozen=True)
class Artifact:
    """One classified artefact under the sessions root."""

    rel: str
    name: str
    kind: str
    host: str
    size: int
    mtime: float
    age_seconds: int
    stale: bool


def classify(rel: str) -> tuple[str, str]:
    """Classify one relative sessions path.

    Args:
        rel: Path relative to the sessions root, POSIX separators.

    Returns:
        ``(kind, host)`` where host may be empty for campaign-wide artefacts.
    """
    for rx, kind in KIND_RULES:
        match = rx.search(rel)
        if match:
            host = match.groupdict().get("host", "") or ""
            if not host:
                hit = _HOST_IN_PATH_RE.search(rel)
                host = hit.group(1) if hit else ""
            return kind, host
    hit = _HOST_IN_PATH_RE.search(rel)
    if hit:
        return "other", hit.group(1)
    return "other", ""


class SessionIndex:
    """Read-only index and viewer over one sessions directory."""

    def __init__(
        self,
        root: Path | str | None = None,
        *,
        freshness_threshold: int = DEFAULT_FRESHNESS_THRESHOLD_SECONDS,
        now: Callable[[], float] | None = None,
    ) -> None:
        self.root = Path(root) if root is not None else Path("sessions")
        self.freshness_threshold = freshness_threshold
        self._now = now or time.time
        self._artifacts_cache: tuple[float, tuple[Artifact, ...]] | None = None

    def resolve_safe(self, rel: str) -> Path:
        """Resolve a sessions-relative path, refusing escapes.

        Every path segment is validated against a strict allowlist before
        any path expression is built, then the joined path is resolved
        canonically and containment-checked against the root.

        Args:
            rel: Relative path (POSIX separators) under the sessions root.

        Returns:
            The resolved absolute path when it stays inside the root.

        Raises:
            PermissionError: When the path escapes the root via ``..``,
                an absolute form, a symlink or disallowed characters.
            ValueError: When the path is empty.
        """
        clean = str(rel or "").replace("\\", "/").replace("\x00", "").strip()
        if not clean:
            raise ValueError("empty path")
        if PurePosixPath(clean).is_absolute() or clean.startswith("~"):
            raise PermissionError(f"path outside sessions root: {rel}")
        _validate_relative_segments(clean, str(rel))
        candidate = (self.root / clean).resolve()
        if not candidate.is_relative_to(self.root.resolve()):
            raise PermissionError(f"path outside sessions root: {rel}")
        return candidate

    def artifacts(self, *, refresh: bool = False) -> tuple[Artifact, ...]:
        """Walk and classify every artefact, cached briefly.

        Args:
            refresh: Force a fresh walk ignoring the short-lived cache.

        Returns:
            A tuple of :class:`Artifact` sorted by relative path.
        """
        now = self._now()
        if not refresh and self._artifacts_cache is not None:
            built_at, cached = self._artifacts_cache
            if now - built_at < ARTIFACTS_CACHE_TTL_SECONDS:
                return cached
        found: list[Artifact] = []
        for dirpath, _dirnames, filenames in os.walk(self.root, followlinks=False):
            for filename in filenames:
                full = Path(dirpath) / filename
                try:
                    stat = full.stat()
                except OSError:
                    continue
                rel = full.relative_to(self.root).as_posix()
                kind, host = classify(rel)
                age = max(0, int(now - stat.st_mtime))
                found.append(
                    Artifact(
                        rel=rel,
                        name=filename,
                        kind=kind,
                        host=host,
                        size=stat.st_size,
                        mtime=stat.st_mtime,
                        age_seconds=age,
                        stale=age > self.freshness_threshold,
                    )
                )
        result = tuple(sorted(found, key=lambda a: a.rel))
        self._artifacts_cache = (now, result)
        return result

    def read(self, rel: str, *, max_bytes: int = READ_CAP_BYTES) -> dict[str, Any]:
        """Read one artefact as text with a size cap and binary detection.

        Args:
            rel: Sessions-relative path.
            max_bytes: Maximum number of bytes returned.

        Returns:
            A dict with ``path``, ``exists``, ``binary``, ``truncated``,
            ``content``, ``size``. Content is empty for binaries or
            missing files.
        """
        info: dict[str, Any] = {
            "path": str(rel),
            "exists": False,
            "binary": False,
            "truncated": False,
            "content": "",
            "size": 0,
        }
        try:
            path = self.resolve_safe(rel)
        except (PermissionError, ValueError) as exc:
            info["error"] = str(exc)
            return info
        if not path.is_file():
            return info
        stat = path.stat()
        info["exists"] = True
        info["size"] = stat.st_size
        try:
            with path.open("rb") as fh:
                head = fh.read(min(BINARY_SNIFF_BYTES, max_bytes))
                if b"\x00" in head:
                    info["binary"] = True
                    return info
                remaining = max_bytes - len(head)
                if remaining <= 0:
                    info["truncated"] = True
                    info["content"] = head.decode("utf-8", errors="replace")
                    return info
                body = head + fh.read(max_bytes)
            info["truncated"] = stat.st_size > len(body)
            info["content"] = body.decode("utf-8", errors="replace")
        except OSError as exc:
            info["error"] = str(exc)
        return info

    def search(
        self,
        pattern: str,
        *,
        kinds: set[str] | None = None,
        max_matches: int = DEFAULT_MAX_MATCHES,
        max_file_bytes: int = SEARCH_MAX_FILE_BYTES,
        case_insensitive: bool = True,
    ) -> dict[str, Any]:
        """Regex-search the indexed artefacts line by line.

        The pattern is validated (length cap, charset allowlist, no
        nested unbounded quantifiers, bounded repeats) before compilation
        to bound catastrophic-backtracking exposure.

        Args:
            pattern: Python regex to match per line.
            kinds: Optional restriction to artifact kinds.
            max_matches: Hard cap on returned matches.
            max_file_bytes: Files larger than this are skipped.
            case_insensitive: Match case-insensitively by default.

        Returns:
            A dict with ``pattern``, ``scanned``, ``match_count``,
            ``truncated`` and ``matches`` of ``{path, line_no, line}``,
            mirroring ``evidence_grep`` semantics. An ``error`` key with
            an ``unsafe_pattern`` or ``invalid_regex`` prefix replaces the
            other fields when the pattern is rejected.
        """
        pattern = str(pattern or "")
        unsafe_reason = _validate_search_pattern(pattern)
        if unsafe_reason:
            return {
                "pattern": pattern,
                "error": f"unsafe_pattern: {unsafe_reason}",
                "matches": [],
                "scanned": 0,
                "truncated": False,
            }
        flags = re.IGNORECASE if case_insensitive else 0
        try:
            rx = re.compile(pattern, flags)
        except re.error as exc:
            return {
                "pattern": pattern,
                "error": f"invalid_regex: {exc}",
                "matches": [],
                "scanned": 0,
                "truncated": False,
            }
        matches: list[dict[str, Any]] = []
        scanned = 0
        truncated = False
        for artifact in self.artifacts():
            if kinds and artifact.kind not in kinds:
                continue
            if artifact.name.lower().endswith(tuple(_SEARCH_SKIP_SUFFIXES)) or artifact.size > max_file_bytes:
                continue
            path = self.root / artifact.rel
            try:
                with path.open("r", errors="replace") as fh:
                    for line_no, line in enumerate(fh, start=1):
                        if rx.search(line):
                            matches.append(
                                {
                                    "path": artifact.rel,
                                    "line_no": line_no,
                                    "line": line.rstrip("\n")[:SEARCH_MAX_LINE_CHARS],
                                }
                            )
                            if len(matches) >= max_matches:
                                truncated = True
                                break
            except OSError:
                continue
            scanned += 1
            if truncated:
                break
        return {
            "pattern": pattern,
            "scanned": scanned,
            "match_count": len(matches),
            "truncated": truncated,
            "matches": matches,
        }

    def artifacts_for_host(self, host: str) -> list[Artifact]:
        """Return every artefact attributed to one host.

        Args:
            host: IP address or hostname to filter on.

        Returns:
            Artefacts whose host attribution equals ``host``.
        """
        return [a for a in self.artifacts() if a.host == host]

    def host_cards(self) -> list[dict[str, Any]]:
        """Aggregate the campaign state per host.

        Combines the world model (services, state, credentials), the
        findings store, the outcome bus and beacon history into one card
        per known host, plus the artefact inventory attributed to it.

        Returns:
            A list of host card dicts sorted by IP.
        """
        now = self._now()
        world = read_state_dict(self.root / "world_model.json")
        cards: dict[str, dict[str, Any]] = {}

        def _card(ip: str) -> dict[str, Any]:
            return cards.setdefault(
                ip,
                {
                    "ip": ip,
                    "in_world_model": False,
                    "state": "",
                    "os_hint": "",
                    "services": [],
                    "worked_ports": set(),
                    "credentials": [],
                    "findings": {"total": 0, "confirmed": 0, "top_severity": ""},
                    "outcomes": {"total": 0, "success": 0, "shells": 0, "top_severity": ""},
                    "beacons": [],
                    "artifacts": {},
                    "stale_recon": False,
                    "scan_files": [],
                },
            )

        for ip, entry in (world.get("hosts") or {}).items():
            card = _card(str(ip))
            card["in_world_model"] = True
            card["state"] = str(entry.get("state", ""))
            card["os_hint"] = str(entry.get("os_hint", ""))
            card["services"] = [
                {
                    "port": int(port),
                    "name": str(svc.get("name", "")),
                    "version": str(svc.get("version", "")),
                    "protocol": str(svc.get("protocol", "tcp")),
                    "state": str(svc.get("state", "open")),
                }
                for port, svc in sorted((entry.get("services") or {}).items(), key=lambda kv: int(kv[0]))
            ]

        for cred in world.get("credentials") or []:
            host = str(cred.get("host", "") or "")
            value = str(cred.get("value", "") or "")
            if not value or not host:
                continue
            likely, confidence, reason = is_likely_credential(value)
            entry = {
                "display": _mask_credential(value),
                "service": str(cred.get("service", "") or ""),
                "confirmed": bool(cred.get("confirmed", False)),
                "found_at": str(cred.get("found_at", "") or ""),
                "confidence": confidence,
                "reason": reason,
            }
            if likely:
                entry["display"] = f"{entry['display']} (conf {confidence:.2f})"
            _card(host)["credentials"].append(entry)

        for artifact in self.artifacts():
            if artifact.host:
                _card(artifact.host)["artifacts"][artifact.kind] = (
                    _card(artifact.host)["artifacts"].get(artifact.kind, 0) + 1
                )
                if artifact.kind == "scan":
                    _card(artifact.host)["scan_files"].append(artifact.rel)
                    if artifact.stale:
                        _card(artifact.host)["stale_recon"] = True

        for path in sorted(self.root.glob("findings/*.jsonl")):
            host = path.stem
            for record in _read_jsonl(path):
                card = _card(str(record.get("target", "") or host))
                card["findings"]["total"] += 1
                if str(record.get("state", "")) == "confirmed":
                    card["findings"]["confirmed"] += 1
                severity = str(record.get("severity", "") or "").lower()
                if SEVERITY_RANK.get(severity, 0) > SEVERITY_RANK.get(card["findings"]["top_severity"], -1):
                    card["findings"]["top_severity"] = severity

        for record in _read_jsonl(self.root / "outcomes.jsonl"):
            event = record.get("event") or {}
            target = str(event.get("target", "") or "")
            if not target:
                continue
            card = _card(target)
            card["outcomes"]["total"] += 1
            port = str(event.get("port", "") or "")
            if event.get("success") is True or str(event.get("success", "")).lower() in ("true", "1"):
                card["outcomes"]["success"] += 1
                if port:
                    card["worked_ports"].add(port)
            if event.get("shell") is True:
                card["outcomes"]["shells"] += 1
            severity = str(event.get("severity", "") or "").lower()
            if SEVERITY_RANK.get(severity, 0) > SEVERITY_RANK.get(card["outcomes"]["top_severity"], -1):
                card["outcomes"]["top_severity"] = severity

        for artifact in self.artifacts():
            if artifact.kind != "beacon_history":
                continue
            records = _read_jsonl(self.root / artifact.rel)
            if not records:
                continue
            last = records[-1]
            client_id = artifact.rel[: -len(".records.jsonl")]
            for ip in re.findall(_HOST_IN_PATH_RE, str(last.get("ips", ""))):
                card = _card(ip)
                card["beacons"].append(
                    {
                        "client_id": client_id,
                        "user": str(last.get("user", "") or ""),
                        "hostname": str(last.get("hostname", "") or ""),
                        "last_seen_age": _age_of(last.get("timestamp"), now),
                        "active": _age_of(last.get("timestamp"), now) <= BEACON_ACTIVE_SECONDS,
                        "history_rel": artifact.rel,
                    }
                )

        for card in cards.values():
            card["worked_ports"] = sorted(p for p in card["worked_ports"] if p)
        return sorted(cards.values(), key=lambda c: _ip_sort_key(c["ip"]))

    def scope_frontier(self, in_scope: Callable[[str], bool] | set[str] | None) -> list[dict[str, Any]]:
        """Rank candidate targets for the next scope decision.

        Args:
            in_scope: Either a membership predicate or a set of authorized
                entries (IPs, CIDR networks or hostname globs). ``None``
                treats every host as in scope.

        Returns:
            Ranked candidate dicts with ``ip``, ``score``, ``in_scope``,
            ``reasons`` and ``evidence`` (relative artefact paths).
        """
        predicate = _as_scope_predicate(in_scope)
        candidates: list[dict[str, Any]] = []
        for card in self.host_cards():
            ip = card["ip"]
            reasons: list[str] = []
            evidence: list[str] = []
            score = 0
            worked = card["worked_ports"] or [""]
            unworked = [svc for svc in card["services"] if str(svc["port"]) not in worked and str(svc["port"]) != ""]
            if card["outcomes"]["total"] == 0 and card["findings"]["total"] == 0:
                score += FRONTIER_SCORE_NEW_HOST
                if card["services"]:
                    reasons.append(f"{len(card['services'])} unworked services")
                else:
                    reasons.append("unworked host (scan only)")
                evidence.extend(card["scan_files"][:2])
            elif unworked:
                count = min(len(unworked), FRONTIER_UNWORKED_SERVICE_CAP)
                score += count * FRONTIER_SCORE_UNWORKED_SERVICE
                reasons.append(f"{len(unworked)} unworked services")
                evidence.extend(card["scan_files"][:2])
            if card["stale_recon"]:
                score += FRONTIER_SCORE_STALE_RECON
                reasons.append(f"recon stale >{self.freshness_threshold // 86400}d")
                evidence.extend(card["scan_files"][:1])
            top = card["findings"]["top_severity"] or card["outcomes"]["top_severity"]
            if top in ("critical", "high"):
                score += FRONTIER_SCORE_SUCCESS_FINDING
                reasons.append(f"finding {top.upper()}")
            if card["outcomes"]["shells"]:
                reasons.append(f"{card['outcomes']['shells']} shells captured")
            if card["beacons"] and any(b["active"] for b in card["beacons"]):
                reasons.append("live beacon")
            candidates.append(
                {
                    "ip": ip,
                    "score": score,
                    "in_scope": predicate(ip),
                    "state": card["state"],
                    "reasons": reasons,
                    "evidence": sorted(set(evidence)),
                }
            )
        return sorted(candidates, key=lambda c: (-c["score"], c["ip"]))

    def overview(self, in_scope: Callable[[str], bool] | set[str] | None = None) -> dict[str, Any]:
        """Return the full campaign snapshot for one render pass.

        Args:
            in_scope: Scope membership, forwarded to :meth:`scope_frontier`.

        Returns:
            A dict with ``hosts``, ``frontier``, ``totals`` and
            ``artifacts_by_kind``.
        """
        artifacts = self.artifacts()
        by_kind: dict[str, int] = {}
        for artifact in artifacts:
            by_kind[artifact.kind] = by_kind.get(artifact.kind, 0) + 1
        hosts = self.host_cards()
        return {
            "hosts": hosts,
            "frontier": self.scope_frontier(in_scope),
            "totals": {
                "hosts": len(hosts),
                "artifacts": len(artifacts),
                "stale": sum(1 for a in artifacts if a.stale),
                "shells": sum(h["outcomes"]["shells"] for h in hosts),
                "beacons": sum(len(h["beacons"]) for h in hosts),
            },
            "artifacts_by_kind": dict(sorted(by_kind.items(), key=lambda kv: -kv[1])),
        }


def _read_jsonl(path: Path) -> list[dict[str, Any]]:
    """Read a JSONL file best-effort, skipping malformed lines."""
    rows: list[dict[str, Any]] = []
    try:
        with path.open("r", errors="replace") as fh:
            for line in fh:
                line = line.strip()
                if not line:
                    continue
                try:
                    data = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if isinstance(data, dict):
                    rows.append(data)
    except OSError:
        return []
    return rows


def _age_of(iso_timestamp: Any, now: float) -> int:
    """Return the age in seconds of an ISO-8601 timestamp, 0 when unknown."""
    raw = str(iso_timestamp or "").strip()
    if not raw:
        return 0
    try:
        parsed = datetime.fromisoformat(raw.replace("Z", "+00:00"))
        return max(0, int(now - parsed.timestamp()))
    except (ValueError, OSError, OverflowError):
        return 0


def _mask_credential(value: str) -> str:
    """Mask a credential for display, keeping only the username part."""
    if ":" in value:
        user, _, _ = value.partition(":")
        shown = user[:2]
        return f"{shown}{'*' * max(4, len(user) - 2)}"
    if len(value) <= 6:
        return "*" * len(value)
    return f"{value[:3]}{'*' * max(4, len(value) - 3)}"


def _as_scope_predicate(in_scope: Callable[[str], bool] | set[str] | None) -> Callable[[str], bool]:
    """Normalise a scope argument into a membership predicate."""
    if in_scope is None:
        return lambda _ip: True
    if callable(in_scope):
        return in_scope

    def _check(ip: str) -> bool:
        try:
            address = ipaddress.ip_address(ip)
        except ValueError:
            return any(fnmatch.fnmatch(ip, entry) for entry in in_scope)
        for entry in in_scope:
            try:
                network = ipaddress.ip_network(entry, strict=False)
            except ValueError:
                if fnmatch.fnmatch(ip, entry):
                    return True
                continue
            if address in network:
                return True
        return False

    return _check


def _ip_sort_key(ip: str) -> tuple[int, Any]:
    """Sort IPs numerically, hostnames last alphabetically."""
    try:
        return (0, tuple(int(part) for part in str(ip).split(".")))
    except ValueError:
        return (1, str(ip))
