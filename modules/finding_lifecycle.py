"""Finding confirmation lifecycle: pending -> confirmed / rejected.

Faithful to the CAIRN discipline (seed-add, seed validation, dead-end
suppression list): a finding only becomes intel once it carries linked
evidence. Anything else stays pending; disproven leads go to the dead-end
list with a labeled reason instead of being silently dropped.

- explicit states persist in ``sessions/finding_lifecycle.json``;
- ``resolve()`` layers explicit state over the automatic rule
  (2+ independent corroborating sources auto-confirm, like CAIRN's
  multi-signal confirmation), explicit reject always wins;
- the campaign funnel counts only confirmed findings at its narrow end.

Stdlib only.
"""

from __future__ import annotations

import json
import time
from dataclasses import dataclass
from pathlib import Path

PENDING = "pending"
CONFIRMED = "confirmed"
REJECTED = "rejected"

BASE_DIR = Path(__file__).resolve().parent.parent
SESSIONS_DIR = BASE_DIR / "sessions"

STORE_FILENAME = "finding_lifecycle.json"
AUTO_CONFIRM_SOURCES = 2

# Evidence fragments that carry hard proof: a classification may never
# fall below what they set, and they alone justify confirmation even
# with a single source (a model's opinion can never create or dismiss
# them). A "likely false positive" read stays listed, never deleted.
HARD_EVIDENCE_MARKERS = (
    "version in affected range",
    "version matches affected",
    "exploited-in-the-wild",
    "kev",
    "template hit",
    "nuclei matched",
    "answered with no credentials",
    "unauthenticated",
    "reproduced",
    "cve-",
)


def evidence_floor(items: list[str] | None) -> bool:
    """Whether hard evidence is present in a list of evidence strings.

    Args:
        items: Evidence strings (operator notes, OSINT verdicts, PoC output).

    Returns:
        True when at least one item carries hard evidence.
    """
    for item in items or []:
        text = str(item or "").lower()
        if any(marker in text for marker in HARD_EVIDENCE_MARKERS):
            return True
    return False


def _store_path(sessions_dir: str | Path) -> Path:
    """Return the lifecycle store path for a sessions directory."""
    return Path(str(sessions_dir)) / STORE_FILENAME


def _load(sessions_dir: str | Path) -> dict:
    """Load the store, tolerating missing or corrupt files."""
    try:
        data = json.loads(_store_path(sessions_dir).read_text())
    except (OSError, ValueError):
        return {"findings": {}, "dead_ends": []}
    if not isinstance(data, dict):
        return {"findings": {}, "dead_ends": []}
    data.setdefault("findings", {})
    data.setdefault("dead_ends", [])
    return data


def _save(sessions_dir: str | Path, data: dict) -> None:
    """Persist the store best-effort."""
    try:
        _store_path(sessions_dir).write_text(json.dumps(data, indent=2))
    except OSError:
        pass


def confirm(
    finding_id: str, evidence: list[str] | None = None, sessions_dir: str | Path = SESSIONS_DIR, by: str = "operator"
) -> dict:
    """Mark a finding confirmed with linked evidence (CAIRN seed-add).

    Evidence mentioning a CVE id is auto-enriched with keyless OSINT
    (OSV advisory, CISA KEV, EPSS score); enrichment never fails the call.
    """
    store = _load(sessions_dir)
    items = [str(e) for e in (evidence or []) if str(e).strip()]
    try:
        from modules.osint_enrich import enrich_evidence as _enrich
    except Exception:
        _enrich = None
    if _enrich is not None:
        try:
            items = _enrich(items, sessions_dir)
        except Exception:
            pass
    store["findings"][str(finding_id)] = {
        "status": CONFIRMED,
        "evidence": items[:12],
        "by": by,
        "at": time.time(),
    }
    _save(sessions_dir, store)
    return store["findings"][str(finding_id)]


def reject(finding_id: str, reason: str = "", sessions_dir: str | Path = SESSIONS_DIR, by: str = "operator") -> dict:
    """Mark a finding rejected (disproven lead, CAIRN dead-end discipline)."""
    store = _load(sessions_dir)
    store["findings"][str(finding_id)] = {
        "status": REJECTED,
        "evidence": [],
        "by": by,
        "at": time.time(),
        "reason": str(reason)[:200],
    }
    _save(sessions_dir, store)
    return store["findings"][str(finding_id)]


def add_dead_end(kind: str, value: str, reason: str = "", sessions_dir: str | Path = SESSIONS_DIR) -> dict:
    """Suppress a value campaign-wide with a labeled reason (dead_end_hashes)."""
    store = _load(sessions_dir)
    entry = {"kind": str(kind), "value": str(value).strip().lower(), "reason": str(reason)[:200], "at": time.time()}
    store["dead_ends"] = [
        e for e in store["dead_ends"] if not (e.get("kind") == entry["kind"] and e.get("value") == entry["value"])
    ]
    store["dead_ends"].append(entry)
    _save(sessions_dir, store)
    return entry


def is_dead_end(kind: str, value: str, sessions_dir: str | Path = SESSIONS_DIR) -> bool:
    """Return True when a kind/value pair sits on the suppression list."""
    store = _load(sessions_dir)
    needle = str(value).strip().lower()
    return any(e.get("kind") == str(kind) and e.get("value") == needle for e in store["dead_ends"])


def suppressed_values(sessions_dir: str | Path = SESSIONS_DIR) -> list[str]:
    """Return every suppressed value for text-level filtering by the loop."""
    store = _load(sessions_dir)
    return sorted({str(e.get("value", "")) for e in store["dead_ends"] if e.get("value")})


def resolve(node: dict, sessions_dir: str | Path = SESSIONS_DIR) -> str:
    """Resolve a finding node's confirmation state.

    Precedence: dead-end list and explicit reject beat everything;
    explicit confirm beats the automatic multi-source rule; otherwise
    2+ independent sources auto-confirm, single-source stays pending.
    Non-finding nodes always resolve to pending.
    """
    if not str(node.get("kind", "")).startswith("finding"):
        return PENDING
    fid = str(node.get("id", ""))
    store = _load(sessions_dir)
    record = store["findings"].get(fid, {})
    if record.get("status") == REJECTED:
        return REJECTED
    if is_dead_end(str(node.get("kind", "")), str(node.get("value", "")), sessions_dir):
        return REJECTED
    if record.get("status") == CONFIRMED:
        return CONFIRMED
    sources = {str(s) for s in (node.get("sources", []) or [])}
    if len(sources) >= AUTO_CONFIRM_SOURCES:
        return CONFIRMED
    hard = evidence_floor(list(sources) + [str(node.get("text", "")), str((node.get("meta") or {}).get("evidence", ""))])
    if hard:
        return CONFIRMED
    return PENDING


def apply_confirmation(nodes: dict[str, dict], sessions_dir: str | Path = SESSIONS_DIR) -> None:
    """Stamp ``confirmation``/``status`` on every finding node in place."""
    for node in nodes.values():
        if not str(node.get("kind", "")).startswith("finding"):
            continue
        state = resolve(node, sessions_dir)
        node["confirmation"] = state
        node["status"] = state


FINDING_STATUSES = (
    "pending",
    "in_progress",
    "confirmed",
    "resolved",
    "fixed",
    "false_positive",
    "ignored",
    "duplicate",
    "risk_accepted",
)
RETEST_CONCLUSIONS = ("reproducible", "fixed", "inconclusive")
RETEST_STORE_FILENAME = "finding_retests.json"
_STATUS_PREFIX = "status:"
_EVIDENCE_PREFIX = "evidence_version:"


@dataclass
class FindingRecord:
    """One campaign finding as stored on a vuln row."""

    finding_id: str
    host: str
    title: str
    severity: str
    status: str
    description: str = ""
    refs: str = ""


@dataclass
class RetestRecord:
    """One retest request/attempt for a finding."""

    retest_id: str
    finding_id: str
    conclusion: str = ""
    status: str = "running"
    evidence: str = ""


def _token_value(refs: str, prefix: str, default: str = "") -> str:
    """Read a ``prefix:value`` token from a refs string."""
    for token in str(refs or "").split(";"):
        if token.startswith(prefix):
            return token[len(prefix) :]
    return default


def _with_token(refs: str, prefix: str, value: str) -> str:
    """Replace or append a ``prefix:value`` token in a refs string."""
    tokens = [token for token in str(refs or "").split(";") if token and not token.startswith(prefix)]
    tokens.append(f"{prefix}{value}")
    return ";".join(tokens)


def _finding_from_row(row: dict) -> FindingRecord:
    """Build a FindingRecord from one vuln_list row."""
    refs = str(row.get("refs", "") or "")
    return FindingRecord(
        finding_id=str(row.get("id", "")),
        host=str(row.get("address", "")),
        title=str(row.get("name", "")),
        severity=str(row.get("severity", "")),
        status=_token_value(refs, _STATUS_PREFIX, PENDING) or PENDING,
        description=str(row.get("description", "") or ""),
        refs=refs,
    )


def record(db, workspace: int, host: str, title: str, severity: str, summary: str = "", poc: str = "") -> FindingRecord:
    """Record a campaign finding on the DB for one host.

    Args:
        db: Open :class:`modules.db.LazyOwnDB`.
        workspace: Workspace id the host belongs to.
        host: Host address (created on first use).
        title: Finding name.
        severity: Severity label.
        summary: Short description.
        poc: Optional proof-of-concept text appended to the description.

    Returns:
        The stored :class:`FindingRecord` with its ``finding_id``.
    """
    hosts = db.host_find(workspace, host)
    host_id = int(hosts[0]["id"]) if hosts else int(db.host_add(workspace, host))
    description = summary or ""
    if poc:
        description = (description + f"\nPoC: {poc}").strip()
    refs = f"{_STATUS_PREFIX}{PENDING};{_EVIDENCE_PREFIX}0"
    finding_id = int(db.vuln_add(host_id, title, severity=severity or "unknown", description=description, refs=refs))
    return FindingRecord(str(finding_id), host, title, severity or "unknown", PENDING, description, refs)


def findings_for(db, workspace: int) -> list[FindingRecord]:
    """List campaign findings with parsed status markers."""
    return [_finding_from_row(row) for row in db.vuln_list(workspace)]


def set_status(db, finding_id: str, status: str) -> bool:
    """Set the lifecycle status marker on one finding.

    Args:
        db: Open campaign DB.
        finding_id: Vuln row id (string form).
        status: One of :data:`FINDING_STATUSES`.

    Returns:
        True when the row existed and was updated.

    Raises:
        ValueError: Unknown status.
    """
    if status not in FINDING_STATUSES:
        raise ValueError(f"status must be one of {FINDING_STATUSES}")
    row = db.vuln_get(int(finding_id))
    if row is None:
        return False
    refs = _with_token(str(row.get("refs", "") or ""), _STATUS_PREFIX, status)
    return db.vuln_update(int(finding_id), refs=refs)


def _retests_path(sessions_dir: str | Path) -> Path:
    """Return the retest store path for a sessions directory."""
    return Path(sessions_dir) / RETEST_STORE_FILENAME


def _load_retests(sessions_dir: str | Path) -> dict:
    """Load the retest payload, tolerating a missing or corrupt file."""
    try:
        payload = json.loads(_retests_path(sessions_dir).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {"seq": 0, "items": []}
    if not isinstance(payload, dict):
        return {"seq": 0, "items": []}
    return payload


def _save_retests(sessions_dir: str | Path, payload: dict) -> None:
    """Persist the retest payload."""
    path = _retests_path(sessions_dir)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def has_running_retest(finding_id: str, sessions_dir: str | Path = SESSIONS_DIR) -> bool:
    """Return True while a retest for the finding is still running."""
    return any(
        item.get("finding_id") == str(finding_id) and item.get("status") == "running"
        for item in _load_retests(sessions_dir).get("items", [])
    )


def request_retest(db, finding_id: str, sessions_dir: str | Path = SESSIONS_DIR) -> RetestRecord:
    """Queue a retest; an already-running one is returned unchanged."""
    payload = _load_retests(sessions_dir)
    for item in payload.get("items", []):
        if item.get("finding_id") == str(finding_id) and item.get("status") == "running":
            return RetestRecord(str(item["retest_id"]), str(item["finding_id"]), status="running")
    payload["seq"] = int(payload.get("seq", 0)) + 1
    item = {
        "retest_id": f"rt_{payload['seq']:04d}",
        "finding_id": str(finding_id),
        "status": "running",
        "conclusion": "",
        "evidence": "",
        "ts": time.time(),
    }
    payload.setdefault("items", []).append(item)
    _save_retests(sessions_dir, payload)
    return RetestRecord(str(item["retest_id"]), str(item["finding_id"]), status="running")


def resolve_retest(
    db, retest_id: str, conclusion: str, evidence: str = "", sessions_dir: str | Path = SESSIONS_DIR
) -> RetestRecord:
    """Close a retest, bump the evidence version and apply the verdict.

    Args:
        db: Open campaign DB.
        retest_id: Retest to close.
        conclusion: One of :data:`RETEST_CONCLUSIONS`.
        evidence: Optional retest output/evidence snippet.
        sessions_dir: Sessions directory holding the retest store.

    Returns:
        The resolved :class:`RetestRecord`.

    Raises:
        ValueError: Unknown conclusion.
        KeyError: Unknown retest id.
    """
    if conclusion not in RETEST_CONCLUSIONS:
        raise ValueError(f"conclusion must be one of {RETEST_CONCLUSIONS}")
    payload = _load_retests(sessions_dir)
    target = None
    for item in payload.get("items", []):
        if item.get("retest_id") == retest_id:
            item["status"] = "done"
            item["conclusion"] = conclusion
            item["evidence"] = str(evidence or "")[:500]
            target = item
            break
    if target is None:
        raise KeyError(f"unknown retest: {retest_id}")
    _save_retests(sessions_dir, payload)
    row = db.vuln_get(int(target["finding_id"]))
    if row is not None:
        refs = str(row.get("refs", "") or "")
        version = int(_token_value(refs, _EVIDENCE_PREFIX, "0") or 0) + 1
        refs = _with_token(refs, _EVIDENCE_PREFIX, str(version))
        if conclusion == "fixed":
            refs = _with_token(refs, _STATUS_PREFIX, "fixed")
        db.vuln_update(int(target["finding_id"]), refs=refs)
    return RetestRecord(
        retest_id, str(target["finding_id"]), conclusion=conclusion, status="done", evidence=str(evidence or "")
    )


def classify_retest(needle: str, output: str) -> str:
    """Map retest output onto reproducible / fixed / inconclusive.

    A vanished service or an explicit patch report means fixed; the
    original marker still present means reproducible; everything else
    (including errors and unrelated banners) stays inconclusive.
    """
    text = str(output or "").lower()
    marker = str(needle or "").lower()
    if any(
        word in text
        for word in ("refused", "unreachable", "no route", "not found", "patched", "fixed", "resolved", "no longer")
    ):
        return "fixed"
    if marker and marker in text:
        return "reproducible"
    return "inconclusive"


def render_markdown(db, workspace: int, title: str = "Findings") -> str:
    """Render campaign findings as a markdown report."""
    rows = [_finding_from_row(row) for row in db.vuln_list(workspace)]
    lines = [f"# {title}", ""]
    if not rows:
        lines.append("_No findings recorded._")
    for finding in rows:
        lines.append(f"- **{finding.severity}** {finding.title} on {finding.host} ({finding.status})")
        if finding.description:
            lines.append(f"  - {finding.description.splitlines()[0][:200]}")
    return "\n".join(lines) + "\n"


__all__ = [
    "PENDING",
    "CONFIRMED",
    "REJECTED",
    "STORE_FILENAME",
    "AUTO_CONFIRM_SOURCES",
    "FINDING_STATUSES",
    "HARD_EVIDENCE_MARKERS",
    "RETEST_CONCLUSIONS",
    "FindingRecord",
    "RetestRecord",
    "add_dead_end",
    "apply_confirmation",
    "classify_retest",
    "confirm",
    "evidence_floor",
    "findings_for",
    "has_running_retest",
    "is_dead_end",
    "record",
    "reject",
    "render_markdown",
    "request_retest",
    "resolve",
    "resolve_retest",
    "set_status",
    "suppressed_values",
]
