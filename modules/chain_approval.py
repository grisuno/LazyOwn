"""Human-in-the-loop approval gate for confirm chain steps.

ARTEX intercept doctrine, adapted: every ``confirm`` step surfaces a
pending request instead of relying on a lone CLI prompt, a dashboard
operator decides from the C2 surface, and every transition is audited
with a SHA-256 command fingerprint. The approver is always
failure-closed: an expired request, a missing store, a malformed row or
a callback error denies the step.

State: ``sessions/chain_pending.json`` holds the pending registry and
``sessions/chain_audit.jsonl`` is the append-only decision trail.
"""

from __future__ import annotations

import hashlib
import json
import os
import secrets
import time
from pathlib import Path
from typing import Any

PENDING_FILENAME = "chain_pending.json"
AUDIT_FILENAME = "chain_audit.jsonl"

STATUS_PENDING = "pending"
STATUS_APPROVED = "approved"
STATUS_DENIED = "denied"
STATUS_EXPIRED = "expired"
STATUSES = (STATUS_PENDING, STATUS_APPROVED, STATUS_DENIED, STATUS_EXPIRED)

DEFAULT_TIMEOUT_SEC = 300.0
_MIN_TIMEOUT = 1.0
_MAX_TIMEOUT = 5400.0
_MAX_PENDING_ROWS = 2000
_MAX_COMMAND_CHARS = 4096
_MAX_NOTE_CHARS = 300
_MAX_AUDIT_LINES = 5000
_DEFAULT_POLL_INTERVAL = 0.25

_ENV_BACKEND = "LAZYOWN_APPROVAL_BACKEND"
_ENV_TIMEOUT = "LAZYOWN_APPROVAL_TIMEOUT"
_BACKEND_C2 = "c2"


def _now() -> float:
    """Return current epoch seconds."""
    return time.time()


def _clamp_timeout(value: Any) -> float:
    """Return a bounded approval timeout value.

    Args:
        value: Raw timeout candidate (seconds).

    Returns:
        Float clamped to [_MIN_TIMEOUT, _MAX_TIMEOUT], default fallback.
    """
    try:
        num = float(value)
    except (TypeError, ValueError):
        return DEFAULT_TIMEOUT_SEC
    return max(_MIN_TIMEOUT, min(_MAX_TIMEOUT, num))


def _store_path(sessions_dir: str | Path) -> Path:
    """Return the pending-store path for a sessions directory."""
    return Path(str(sessions_dir or "sessions")) / PENDING_FILENAME


def _audit_path(sessions_dir: str | Path) -> Path:
    """Return the audit log path for a sessions directory."""
    return Path(str(sessions_dir or "sessions")) / AUDIT_FILENAME


def command_fingerprint(command: str) -> str:
    """Return the SHA-256 fingerprint of one command line.

    Args:
        command: Raw command text.

    Returns:
        Lowercase hex digest of the first 4096 characters.
    """
    material = str(command or "")[:_MAX_COMMAND_CHARS].encode("utf-8", errors="replace")
    return hashlib.sha256(material).hexdigest()


def _audit(sessions_dir: str | Path, event: dict) -> None:
    """Append one audit line, trimming the log at the cap.

    Args:
        sessions_dir: Sessions base directory.
        event: JSON-serializable audit payload.
    """
    path = _audit_path(sessions_dir)
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        try:
            os.chmod(path.parent, 0o700)
        except OSError:
            pass
        lines = path.read_text(encoding="utf-8", errors="replace").splitlines() if path.exists() else []
        lines.append(json.dumps(event, ensure_ascii=False, sort_keys=True))
        if len(lines) > _MAX_AUDIT_LINES:
            lines = lines[-_MAX_AUDIT_LINES:]
        path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    except OSError:
        return


class PendingStore:
    """Atomic pending-approval registry shared by CLI and C2 surface."""

    def __init__(self, sessions_dir: str | Path | None = None) -> None:
        """Bind the store to one sessions directory.

        Args:
            sessions_dir: Sessions base directory (default ``sessions``).
        """
        self.sessions_dir = Path(str(sessions_dir or "sessions"))

    def _load(self) -> dict:
        """Load the registry tolerating missing or corrupt files.

        Returns:
            ``{"requests": {id: record}}``; corrupt payloads reset empty.
        """
        path = _store_path(self.sessions_dir)
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            return {"requests": {}}
        if not isinstance(payload, dict) or not isinstance(payload.get("requests", {}), dict):
            return {"requests": {}}
        rows = {str(k): v for k, v in payload.get("requests", {}).items() if isinstance(v, dict)}
        return {"requests": rows}

    def _save(self, payload: dict) -> None:
        """Atomically persist the registry.

        Args:
            payload: Full registry payload.
        """
        path = _store_path(self.sessions_dir)
        path.parent.mkdir(parents=True, exist_ok=True)
        tmp = path.with_suffix(".tmp")
        tmp.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True), encoding="utf-8")
        os.replace(tmp, path)

    def create(
        self,
        chain: str,
        step_id: str,
        command: str,
        timeout: float | None = None,
        run_id: str = "",
        now_override: float | None = None,
    ) -> dict:
        """Register one pending approval request.

        Args:
            chain: Chain name asking for approval.
            step_id: Chain step identifier.
            command: Rendered command awaiting execution.
            timeout: Optional approval window override in seconds.
            run_id: Optional chain run identifier.
            now_override: Optional creation timestamp (test clocks).

        Returns:
            The created record mapping.
        """
        context = self.sessions_dir
        window = _clamp_timeout(timeout if timeout is not None else os.environ.get(_ENV_TIMEOUT))
        now = _now() if now_override is None else float(now_override)
        request_id = secrets.token_hex(8)
        record = {
            "id": request_id,
            "chain": str(chain or "")[:120],
            "step_id": str(step_id or "")[:80],
            "command": str(command or "")[:_MAX_COMMAND_CHARS],
            "command_sha256": command_fingerprint(command),
            "ts": now,
            "deadline": now + window,
            "timeout": window,
            "status": STATUS_PENDING,
            "decided_by": "",
            "decided_ts": 0.0,
            "note": "",
            "run_id": str(run_id or "")[:80],
        }
        payload = self._load()
        requests = payload["requests"]
        requests[request_id] = record
        if len(requests) > _MAX_PENDING_ROWS:
            for stale in sorted(requests, key=lambda key: float(requests[key].get("ts", 0.0)))[: len(requests) - _MAX_PENDING_ROWS]:
                requests.pop(stale, None)
        self._save(payload)
        _audit(context, {"event": "requested", "ts": now, **{k: record[k] for k in ("id", "chain", "step_id", "command_sha256")}})
        return dict(record)

    def get(self, request_id: str) -> dict | None:
        """Return one request record or None.

        Args:
            request_id: Request identifier.

        Returns:
            Record mapping when present.
        """
        return self._load()["requests"].get(str(request_id or ""))

    def list(self, status: str | None = None) -> list[dict]:
        """Return request records newest first, optionally by status.

        Args:
            status: Optional status filter.

        Returns:
            List of record mappings sorted by ``ts`` descending.
        """
        rows = list(self._load()["requests"].values())
        if status:
            rows = [row for row in rows if row.get("status") == status]
        return sorted(rows, key=lambda row: float(row.get("ts", 0.0)), reverse=True)

    def decide(
        self,
        request_id: str,
        allowed: bool,
        decided_by: str = "",
        note: str = "",
        expired: bool = False,
    ) -> dict | None:
        """Record one decision or expiry, audited, idempotent-fail.

        Args:
            request_id: Request identifier.
            allowed: True approves, False denies (ignored when expired).
            decided_by: Actor label (``c2``, ``cli``, ``system``).
            note: Optional operator note.
            expired: True marks the record expired regardless of verdict.

        Returns:
            Updated record, or None when the id is unknown or already
            decided (no silent double-decide).
        """
        payload = self._load()
        requests = payload["requests"]
        record = requests.get(str(request_id or ""))
        if not isinstance(record, dict):
            return None
        if record.get("status") != STATUS_PENDING:
            return None
        now = _now()
        if expired:
            record["status"] = STATUS_EXPIRED
            note = note or "expired"
            record["decided_by"] = decided_by or "system"
        else:
            record["status"] = STATUS_APPROVED if allowed else STATUS_DENIED
            record["decided_by"] = str(decided_by or "operator")[:80]
        record["decided_ts"] = now
        record["note"] = str(note or "")[:_MAX_NOTE_CHARS]
        self._save(payload)
        _audit(
            self.sessions_dir,
            {
                "event": record["status"],
                "ts": now,
                "id": record.get("id", ""),
                "chain": record.get("chain", ""),
                "step_id": record.get("step_id", ""),
                "command_sha256": record.get("command_sha256", ""),
                "decided_by": record.get("decided_by", ""),
            },
        )
        return dict(record)

    def expire_stale(self, now: float | None = None) -> int:
        """Expire every pending request past its deadline.

        Args:
            now: Optional clock override for tests.

        Returns:
            Count of records expired by this sweep.
        """
        moment = _now() if now is None else float(now)
        payload = self._load()
        count = 0
        for record in payload["requests"].values():
            if record.get("status") == STATUS_PENDING and moment >= float(record.get("deadline", 0.0)):
                record["status"] = STATUS_EXPIRED
                record["decided_ts"] = moment
                record["decided_by"] = "system"
                record["note"] = "expired"
                count += 1
                _audit(
                    self.sessions_dir,
                    {
                        "event": STATUS_EXPIRED,
                        "ts": moment,
                        "id": record.get("id", ""),
                        "chain": record.get("chain", ""),
                        "step_id": record.get("step_id", ""),
                        "command_sha256": record.get("command_sha256", ""),
                        "decided_by": "system",
                    },
                )
        if count:
            self._save(payload)
        return count


def approval_backend() -> str:
    """Return the configured approval backend.

    Returns:
        ``c2`` when ``LAZYOWN_APPROVAL_BACKEND=c2``; anything else
        keeps the interactive CLI approver.
    """
    return "c2" if os.environ.get(_ENV_BACKEND, "").strip().lower() == _BACKEND_C2 else "cli"


def build_c2_approver(
    printer=None,
    chain_name: str = "",
    run_id: str = "",
    timeout: float | None = None,
    poll_interval: float = _DEFAULT_POLL_INTERVAL,
    sessions_dir: str | Path | None = None,
    clock=None,
) -> Any:
    """Return an approver that routes confirm steps to the C2 pending list.

    The callback creates one pending record, then polls the shared store
    until an operator approves or denies it from the dashboard or CLI.
    Deadline expiry sweeps the record and votes deny (failure-closed);
    any store or callback error denies as well.

    Args:
        printer: Optional progress printer.
        chain_name: Chain name recorded in the request.
        run_id: Optional chain run identifier.
        timeout: Optional approval window override in seconds.
        poll_interval: Seconds between store re-reads.
        sessions_dir: Optional sessions directory override.
        clock: Optional ``time.time`` replacement for tests.

    Returns:
        ``approve(step_id, command) -> bool``.
    """
    tick = clock or _now

    def approve(step_id: str, command: str) -> bool:
        region = sessions_dir
        try:
            store = PendingStore(region)
            record = store.create(chain_name, step_id, command, timeout=timeout, run_id=run_id, now_override=tick())
            if printer is not None:
                printer(
                    f"[apt_chain] approval requested: id={record['id']} step={step_id}"
                    f" sha256={record['command_sha256'][:12]} window={record['timeout']:.0f}s"
                )
            deadline = float(record["deadline"])
            while tick() < deadline:
                store.expire_stale(tick())
                current = store.get(record["id"]) or {}
                status = str(current.get("status", ""))
                if status == STATUS_APPROVED:
                    return True
                if status in (STATUS_DENIED, STATUS_EXPIRED):
                    return False
                if poll_interval > 0:
                    time.sleep(min(poll_interval, max(0.0, deadline - tick())))
            store.expire_stale(tick())
            final = store.get(record["id"]) or {}
            if final.get("status") != STATUS_DENIED and printer is not None:
                printer(f"[apt_chain] approval expired: id={record['id']} step={step_id}")
            return False
        except Exception:
            if printer is not None:
                printer(f"[apt_chain] approval gate failed-closed for step {step_id}")
            return False

    return approve
