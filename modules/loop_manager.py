"""Parallel autonomous loop orchestration for the LazyOwn C2 dashboard.

Contract: this module owns every autonomous loop started from the web
dashboard. Each loop is an isolated ``lazyown.py`` subprocess (argv form,
``shell=False``, own process session) with a dedicated workspace under
``sessions/loops/<loop_id>/`` holding its YAML profile, live output log
and metadata. A single JSON registry (``sessions/loops/registry.json``)
is the durable source of truth so loops survive dashboard restarts.

Invariants:

1. Every user-supplied field is strictly validated before it can reach
   a subprocess: the target must parse as an IP address, the goal must
   match a fixed safe charset, and numeric knobs are clamped to the
   ranges supported by :mod:`modules.lazy_runner`.
2. Subprocesses are never started through a shell. ``argv`` lists only,
   ``shell=False``, ``stdin=DEVNULL`` and ``start_new_session=True`` so
   a loop can be stopped as a whole process group.
3. Log reads are path-safe: the loop id must match a strict hex pattern
   and the resolved log path must stay inside the loops directory.
4. The number of concurrently running loops is capped so the dashboard
   can never exhaust host processes.
5. Stop uses SIGTERM on the process group, waits a grace period, then
   escalates to SIGKILL. A stored process start-time counter prevents
   acting on a recycled PID.

Config keys owned: none (all knobs are module constants).
"""

from __future__ import annotations

import ipaddress
import json
import os
import re
import signal
import subprocess
import sys
import threading
import time
import uuid
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

LOOPS_DIR = Path("sessions/loops")
REGISTRY_FILENAME = "registry.json"
LOG_FILENAME = "output.log"
PROFILE_FILENAME = "profile.yaml"
METADATA_FILENAME = "metadata.json"

KIND_AUTO_LOOP = "auto_loop"
KIND_LAZY_NMAP = "lazynmap"
LOOP_KINDS = frozenset({KIND_AUTO_LOOP, KIND_LAZY_NMAP})

DEFAULT_ROUNDS = 6
DEFAULT_WORKERS = 2
MAX_ROUNDS = 50
MAX_WORKERS = 5
MAX_TIMEOUT_SECONDS = 86400.0

MAX_CONCURRENT_LOOPS = 5
MAX_REGISTRY_ENTRIES = 200
MAX_GOAL_LENGTH = 200
MAX_LOG_CHUNK_BYTES = 65536
STOP_GRACE_SECONDS = 5.0
PRUNE_AFTER_DAYS = 7

DEFAULT_GOAL = "gain initial access"

GOAL_PATTERN = re.compile(r"^[A-Za-z0-9 .,_()\-]+$")
LOOP_ID_PATTERN = re.compile(r"^[0-9a-f]{32}$")

STATUS_RUNNING = "running"
STATUS_FINISHED = "finished"
STATUS_FAILED = "failed"
STATUS_STOPPED = "stopped"
STATUS_LOST = "lost"
STATUS_STOPPING = "stopping"

_ORPHAN_EXIT_CODE = -1
_PROC_STAT_STARTTIME_FIELD = 22
_BOOT_TICKS = os.sysconf("SC_CLK_TCK")


class LoopValidationError(ValueError):
    """Raised when a loop request field fails validation."""

    def __init__(self, field: str, message: str) -> None:
        """Store the offending field alongside the human message."""
        super().__init__(message)
        self.field = field


class LoopNotFoundError(KeyError):
    """Raised when a loop id is unknown to the registry."""


def validate_target(raw: object) -> str:
    """Return the canonical string form of a validated IP address target.

    Args:
        raw: Candidate target value from an HTTP request.

    Returns:
        The canonical IP string.

    Raises:
        LoopValidationError: The value is not a valid IPv4/IPv6 address.
    """
    if not isinstance(raw, str):
        raise LoopValidationError("target", "target must be a string")
    candidate = raw.strip()
    if not candidate:
        raise LoopValidationError("target", "target is required")
    try:
        return str(ipaddress.ip_address(candidate))
    except ValueError as exc:
        raise LoopValidationError("target", "target must be a valid IP address") from exc


def sanitize_goal(raw: object) -> str:
    """Return a safe goal string accepted by the loop parser.

    Args:
        raw: Candidate goal value from an HTTP request.

    Returns:
        The sanitized goal. Empty input yields :data:`DEFAULT_GOAL`.

    Raises:
        LoopValidationError: The goal exceeds the length cap or contains
            characters outside the safe charset.
    """
    if raw is None:
        return DEFAULT_GOAL
    if not isinstance(raw, str):
        raise LoopValidationError("goal", "goal must be a string")
    candidate = re.sub(r"\s+", " ", raw.strip())
    if not candidate:
        return DEFAULT_GOAL
    if len(candidate) > MAX_GOAL_LENGTH:
        raise LoopValidationError("goal", f"goal must be at most {MAX_GOAL_LENGTH} characters")
    if not GOAL_PATTERN.match(candidate):
        raise LoopValidationError("goal", "goal contains forbidden characters")
    return candidate


def clamp_int(raw: object, field: str, default: int, minimum: int, maximum: int) -> int:
    """Parse and clamp an integer knob to the supported range.

    Args:
        raw: Candidate integer value (string or number).
        field: Field name used in the validation error.
        default: Value used when ``raw`` is None or empty.
        minimum: Inclusive lower bound.
        maximum: Inclusive upper bound.

    Returns:
        The parsed and clamped integer.

    Raises:
        LoopValidationError: The value is not numeric.
    """
    if raw is None or (isinstance(raw, str) and not raw.strip()):
        return default
    try:
        value = int(str(raw).strip())
    except (TypeError, ValueError) as exc:
        raise LoopValidationError(field, f"{field} must be an integer") from exc
    return max(minimum, min(maximum, value))


def clamp_float(raw: object, field: str, default: float, minimum: float, maximum: float) -> float:
    """Parse and clamp a float knob to the supported range.

    Args:
        raw: Candidate float value (string or number).
        field: Field name used in the validation error.
        default: Value used when ``raw`` is None or empty.
        minimum: Inclusive lower bound.
        maximum: Inclusive upper bound.

    Returns:
        The parsed and clamped float.

    Raises:
        LoopValidationError: The value is not numeric.
    """
    if raw is None or (isinstance(raw, str) and not raw.strip()):
        return default
    try:
        value = float(str(raw).strip())
    except (TypeError, ValueError) as exc:
        raise LoopValidationError(field, f"{field} must be a number") from exc
    return max(minimum, min(maximum, value))


def validate_loop_id(loop_id: object) -> str:
    """Validate a loop id and return its normalized hex form.

    Args:
        loop_id: Candidate loop identifier from an HTTP request.

    Returns:
        The validated 32-character hex loop id.

    Raises:
        LoopNotFoundError: The id does not match the strict hex pattern.
    """
    if not isinstance(loop_id, str) or not LOOP_ID_PATTERN.match(loop_id.strip()):
        raise LoopNotFoundError(loop_id if isinstance(loop_id, str) else "<non-string>")
    return loop_id.strip()


def _now_iso() -> str:
    """Return the current UTC time in ISO-8601 format."""
    return datetime.now(UTC).isoformat()


def _process_start_ticks(pid: int) -> int | None:
    """Return the process start-time counter, or None when unavailable.

    Args:
        pid: Process identifier to inspect.

    Returns:
        The field-22 start ticks from ``/proc/<pid>/stat`` or ``None``
        when the process no longer exists.
    """
    try:
        stat = Path(f"/proc/{pid}/stat").read_text(encoding="utf-8", errors="replace")
    except OSError:
        return None
    close = stat.rfind(")")
    if close < 0:
        return None
    fields = stat[close + 2 :].split()
    try:
        return int(fields[_PROC_STAT_STARTTIME_FIELD - 3])
    except (IndexError, ValueError):
        return None


def _pid_alive(pid: int, start_ticks: int) -> bool:
    """Return True when ``pid`` is alive and is the same process recorded.

    Args:
        pid: Process identifier stored in the registry.
        start_ticks: Start-time counter recorded when the loop started.

    Returns:
        True only when the PID exists and its start ticks match, which
        guards against recycled PIDs.
    """
    if pid <= 0:
        return False
    current = _process_start_ticks(pid)
    return current is not None and current == start_ticks


@dataclass(frozen=True)
class LoopSpec:
    """Validated request to start one autonomous loop.

    Attributes:
        kind: Either ``auto_loop`` or ``lazynmap``.
        target: Validated IP address string.
        goal: Sanitized natural-language goal (auto_loop only).
        rounds: Maximum orchestrator rounds (auto_loop only).
        workers: Worker pool size (auto_loop only).
        timeout: Optional wall-clock timeout in seconds (0 = none).
    """

    kind: str
    target: str
    goal: str = DEFAULT_GOAL
    rounds: int = DEFAULT_ROUNDS
    workers: int = DEFAULT_WORKERS
    timeout: float = 0.0


def _loop_command(spec: LoopSpec) -> str:
    """Build the LazyOwn shell command line for one loop kind.

    Args:
        spec: Validated loop specification.

    Returns:
        The command string passed to ``lazyown.py -c``.

    Raises:
        LoopValidationError: The loop kind is unknown.
    """
    if spec.kind == KIND_AUTO_LOOP:
        parts = [
            KIND_AUTO_LOOP,
            "--no-progress",
            "--target",
            spec.target,
            "--rounds",
            str(spec.rounds),
            "--workers",
            str(spec.workers),
        ]
        if spec.timeout > 0:
            parts.extend(["--timeout", str(int(spec.timeout))])
        parts.append(spec.goal)
        return " ".join(parts)
    if spec.kind == KIND_LAZY_NMAP:
        return KIND_LAZY_NMAP
    raise LoopValidationError("kind", "unknown loop kind")


class LoopManager:
    """Owns the lifecycle of autonomous loops started from the dashboard.

    Args:
        loops_dir: Root directory holding the registry and loop workspaces.
        python_executable: Interpreter used to launch ``lazyown.py``;
            defaults to the current interpreter.
        max_concurrent: Upper bound of simultaneously running loops.
        repo_root: Repository root passed as the subprocess cwd.
    """

    def __init__(
        self,
        loops_dir: Path | str = LOOPS_DIR,
        python_executable: str | None = None,
        max_concurrent: int = MAX_CONCURRENT_LOOPS,
        repo_root: Path | str | None = None,
        lazyown_script: Path | str | None = None,
    ) -> None:
        """Create the manager and its persistence lock."""
        self._loops_dir = Path(loops_dir)
        self._registry_path = self._loops_dir / REGISTRY_FILENAME
        self._python = python_executable or sys.executable
        self._max_concurrent = max(1, int(max_concurrent))
        self._repo_root = Path(repo_root) if repo_root else Path(__file__).resolve().parent.parent
        self._lazyown_script = (
            Path(lazyown_script) if lazyown_script else self._repo_root / "lazyown.py"
        )
        self._lock = threading.Lock()
        self._popen: dict[str, subprocess.Popen] = {}
        self._stopping: dict[str, bool] = {}

    @property
    def loops_dir(self) -> Path:
        """Return the root directory for loop workspaces."""
        return self._loops_dir

    def start(self, spec: LoopSpec, operator: str = "") -> dict[str, Any]:
        """Validate, spawn and register one autonomous loop.

        Args:
            spec: Validated loop specification.
            operator: Authenticated username starting the loop.

        Returns:
            The registry record for the new loop.

        Raises:
            LoopValidationError: Any field failed validation or the
                concurrency cap is reached.
            OSError: The subprocess could not be spawned.
        """
        if spec.kind not in LOOP_KINDS:
            raise LoopValidationError("kind", "unknown loop kind")
        target = validate_target(spec.target)
        goal = sanitize_goal(spec.goal) if spec.kind == KIND_AUTO_LOOP else ""
        rounds = clamp_int(spec.rounds, "rounds", DEFAULT_ROUNDS, 1, MAX_ROUNDS)
        workers = clamp_int(spec.workers, "workers", DEFAULT_WORKERS, 1, MAX_WORKERS)
        timeout = clamp_float(spec.timeout, "timeout", 0.0, 0.0, MAX_TIMEOUT_SECONDS)
        with self._lock:
            self._prune_locked()
            records = self._load_registry_locked()
            running = sum(1 for r in records if r.get("status") == STATUS_RUNNING)
            if running >= self._max_concurrent:
                raise LoopValidationError(
                    "concurrency",
                    f"at most {self._max_concurrent} loops may run concurrently",
                )
            if len(records) >= MAX_REGISTRY_ENTRIES:
                raise LoopValidationError("registry", "loop registry is full")
            record = self._spawn_locked(
                LoopSpec(spec.kind, target, goal, rounds, workers, timeout),
                operator=operator,
            )
            records.append(record)
            self._save_registry_locked(records)
            return record

    def _spawn_locked(self, spec: LoopSpec, operator: str) -> dict[str, Any]:
        """Create the loop workspace, profile and subprocess.

        Args:
            spec: Validated loop specification.
            operator: Authenticated username starting the loop.

        Returns:
            The registry record for the new loop.
        """
        loop_id = uuid.uuid4().hex
        workspace = self._loops_dir / loop_id
        workspace.mkdir(parents=True, exist_ok=True)
        profile_path = workspace / PROFILE_FILENAME
        profile_path.write_text(f"rhost: {spec.target}\n", encoding="utf-8")
        log_path = workspace / LOG_FILENAME
        command = _loop_command(spec)
        argv = [
            self._python,
            str(self._lazyown_script),
            "--no-banner",
            "--profile",
            str(profile_path),
            "-c",
            command,
        ]
        env = os.environ.copy()
        env["LAZYOWN_AUTONOMOUS"] = "1"
        env["PYTHONUNBUFFERED"] = "1"
        started_at = _now_iso()
        record: dict[str, Any] = {
            "id": loop_id,
            "kind": spec.kind,
            "target": spec.target,
            "goal": spec.goal,
            "rounds": spec.rounds,
            "workers": spec.workers,
            "timeout": spec.timeout,
            "command": command,
            "argv": argv,
            "pid": 0,
            "start_ticks": 0,
            "status": STATUS_RUNNING,
            "exit_code": None,
            "started_at": started_at,
            "finished_at": None,
            "started_by": operator or "unknown",
            "log_path": str(log_path),
            "log_bytes": 0,
        }
        try:
            log_handle = log_path.open("wb")
            process = subprocess.Popen(  # noqa: S603 - argv form, no shell
                argv,
                shell=False,
                cwd=str(self._repo_root),
                stdin=subprocess.DEVNULL,
                stdout=log_handle,
                stderr=subprocess.STDOUT,
                start_new_session=True,
                env=env,
            )
        except OSError:
            log_path.unlink(missing_ok=True)
            raise
        log_handle.close()
        record["pid"] = process.pid
        record["start_ticks"] = _process_start_ticks(process.pid) or 0
        self._popen[loop_id] = process
        self._stopping[loop_id] = False
        (workspace / METADATA_FILENAME).write_text(
            json.dumps(record, indent=2), encoding="utf-8"
        )
        threading.Thread(target=self._reap, args=(loop_id, process), daemon=True).start()
        return record

    def _reap(self, loop_id: str, process: subprocess.Popen) -> None:
        """Wait for one loop subprocess and finalize its registry record.

        Args:
            loop_id: Loop identifier.
            process: The Popen handle for the loop subprocess.
        """
        exit_code = process.wait()
        with self._lock:
            self._popen.pop(loop_id, None)
            was_stopping = self._stopping.pop(loop_id, False)
            records = self._load_registry_locked()
            for record in records:
                if record.get("id") != loop_id:
                    continue
                record["exit_code"] = _ORPHAN_EXIT_CODE if was_stopping else exit_code
                record["status"] = STATUS_STOPPED if was_stopping else (
                    STATUS_FINISHED if exit_code == 0 else STATUS_FAILED
                )
                record["finished_at"] = _now_iso()
                break
            self._save_registry_locked(records)

    def list_loops(self) -> list[dict[str, Any]]:
        """Return every registry record with refreshed live status.

        Returns:
            Records sorted newest first.
        """
        with self._lock:
            records = self._load_registry_locked()
            changed = False
            for record in records:
                if record.get("status") != STATUS_RUNNING:
                    continue
                pid = int(record.get("pid", 0) or 0)
                start_ticks = int(record.get("start_ticks", 0) or 0)
                if not _pid_alive(pid, start_ticks):
                    record["status"] = STATUS_LOST
                    record["exit_code"] = _ORPHAN_EXIT_CODE
                    record["finished_at"] = record.get("finished_at") or _now_iso()
                    changed = True
                self._refresh_log_bytes(record)
            if changed:
                self._save_registry_locked(records)
            return sorted(records, key=lambda r: str(r.get("started_at", "")), reverse=True)

    def _refresh_log_bytes(self, record: dict[str, Any]) -> None:
        """Update the cached log byte count for one record.

        Args:
            record: Registry record to refresh in place.
        """
        try:
            record["log_bytes"] = Path(record["log_path"]).stat().st_size
        except (OSError, KeyError):
            record["log_bytes"] = 0

    def get_loop(self, loop_id: object) -> dict[str, Any]:
        """Return one registry record by id.

        Args:
            loop_id: Candidate loop identifier.

        Returns:
            The matching registry record.

        Raises:
            LoopNotFoundError: Unknown or malformed loop id.
        """
        normalized = validate_loop_id(loop_id)
        with self._lock:
            for record in self._load_registry_locked():
                if record.get("id") == normalized:
                    return dict(record)
        raise LoopNotFoundError(normalized)

    def read_log(self, loop_id: object, offset: object = 0) -> dict[str, Any]:
        """Read one chunk of a loop's output log.

        Args:
            loop_id: Candidate loop identifier.
            offset: Byte offset to read from (defaults to 0).

        Returns:
            Dict with ``loop_id``, ``offset`` (next read offset),
            ``size``, ``chunk`` (decoded text) and ``truncated`` flag.

        Raises:
            LoopNotFoundError: Unknown loop id.
            LoopValidationError: Negative or oversized offset.
        """
        record = self.get_loop(loop_id)
        normalized = record["id"]
        start = clamp_int(offset, "offset", 0, 0, 2**48)
        log_path = self._resolve_log_path(record)
        try:
            size = log_path.stat().st_size
        except OSError:
            size = 0
        if start > size:
            start = size
        end = min(start + MAX_LOG_CHUNK_BYTES, size)
        chunk = ""
        try:
            with log_path.open("rb") as fh:
                fh.seek(start)
                chunk = fh.read(end - start).decode("utf-8", errors="replace")
        except OSError:
            chunk = ""
        return {
            "loop_id": normalized,
            "offset": end,
            "size": size,
            "chunk": chunk,
            "truncated": (end - start) >= MAX_LOG_CHUNK_BYTES,
        }

    def _resolve_log_path(self, record: dict[str, Any]) -> Path:
        """Resolve and confinement-check the log path for one record.

        Args:
            record: Registry record.

        Returns:
            The validated log file path.

        Raises:
            LoopNotFoundError: The path escapes the loops directory.
        """
        raw = str(record.get("log_path", ""))
        base = self._loops_dir.resolve()
        candidate = Path(raw)
        if not candidate.is_absolute():
            candidate = self._repo_root / candidate
        try:
            resolved = candidate.resolve()
            resolved.relative_to(base)
        except (ValueError, OSError) as exc:
            raise LoopNotFoundError(record.get("id", "?")) from exc
        if resolved.name != LOG_FILENAME:
            raise LoopNotFoundError(record.get("id", "?"))
        return resolved

    def stop(self, loop_id: object) -> dict[str, Any]:
        """Stop one running loop by terminating its process group.

        Args:
            loop_id: Candidate loop identifier.

        Returns:
            The updated registry record.

        Raises:
            LoopNotFoundError: Unknown loop id.
            LoopValidationError: The loop is not running.
        """
        record = self.get_loop(loop_id)
        normalized = record["id"]
        status = str(record.get("status", ""))
        if status not in (STATUS_RUNNING, STATUS_STOPPING):
            raise LoopValidationError("status", f"loop is not running (status={status})")
        pid = int(record.get("pid", 0) or 0)
        start_ticks = int(record.get("start_ticks", 0) or 0)
        with self._lock:
            self._stopping[normalized] = True
            self._update_status_locked(normalized, STATUS_STOPPING)
        if _pid_alive(pid, start_ticks):
            try:
                os.killpg(os.getpgid(pid), signal.SIGTERM)
            except (ProcessLookupError, PermissionError):
                try:
                    os.kill(pid, signal.SIGKILL)
                except (ProcessLookupError, PermissionError):
                    pass
        deadline = time.monotonic() + STOP_GRACE_SECONDS
        process = self._popen.get(normalized)
        while process is not None and time.monotonic() < deadline:
            if process.poll() is not None:
                break
            time.sleep(0.1)
        if process is not None and process.poll() is None and _pid_alive(pid, start_ticks):
            try:
                os.killpg(os.getpgid(pid), signal.SIGKILL)
            except (ProcessLookupError, PermissionError):
                pass
        if process is None:
            with self._lock:
                self._stopping.pop(normalized, None)
                self._update_status_locked(normalized, STATUS_STOPPED)
        return self.get_loop(normalized)

    def _update_status_locked(self, loop_id: str, status: str) -> None:
        """Persist a status change for one loop.

        Args:
            loop_id: Loop identifier.
            status: New status value.
        """
        records = self._load_registry_locked()
        for record in records:
            if record.get("id") != loop_id:
                continue
            record["status"] = status
            if status in (STATUS_STOPPED, STATUS_LOST):
                record["finished_at"] = _now_iso()
            break
        self._save_registry_locked(records)

    def summary(self) -> dict[str, Any]:
        """Return an aggregate view of loop activity for the report.

        Returns:
            Dict with total/running/finished counts, per-kind counts,
            per-target counts and the most recent records.
        """
        records = self.list_loops()
        by_status: dict[str, int] = {}
        by_kind: dict[str, int] = {}
        by_target: dict[str, int] = {}
        for record in records:
            by_status[str(record.get("status", ""))] = by_status.get(str(record.get("status", "")), 0) + 1
            by_kind[str(record.get("kind", ""))] = by_kind.get(str(record.get("kind", "")), 0) + 1
            target = str(record.get("target", ""))
            if target:
                by_target[target] = by_target.get(target, 0) + 1
        return {
            "total": len(records),
            "by_status": by_status,
            "by_kind": by_kind,
            "by_target": by_target,
            "recent": [
                {
                    "id": record.get("id", ""),
                    "kind": record.get("kind", ""),
                    "target": record.get("target", ""),
                    "goal": record.get("goal", ""),
                    "status": record.get("status", ""),
                    "started_at": record.get("started_at", ""),
                    "started_by": record.get("started_by", ""),
                }
                for record in records[:10]
            ],
        }

    def _prune_locked(self) -> None:
        """Drop finished records older than the retention window.

        Called with the lock held before admitting a new loop.
        """
        records = self._load_registry_locked()
        cutoff = time.time() - PRUNE_AFTER_DAYS * 86400.0
        kept: list[dict[str, Any]] = []
        for record in records:
            status = str(record.get("status", ""))
            if status == STATUS_RUNNING:
                kept.append(record)
                continue
            finished = record.get("finished_at") or record.get("started_at") or ""
            try:
                ts = datetime.fromisoformat(str(finished)).timestamp()
            except (TypeError, ValueError):
                ts = 0.0
            if ts and ts < cutoff:
                self._remove_workspace(str(record.get("id", "")))
                continue
            kept.append(record)
        if len(kept) != len(records):
            self._save_registry_locked(kept)

    def _remove_workspace(self, loop_id: str) -> None:
        """Delete one loop workspace directory.

        Args:
            loop_id: Loop identifier whose workspace is removed.
        """
        if not LOOP_ID_PATTERN.match(loop_id):
            return
        workspace = self._loops_dir / loop_id
        try:
            resolved = workspace.resolve()
            resolved.relative_to(self._loops_dir.resolve())
        except (ValueError, OSError):
            return
        for entry in (METADATA_FILENAME, PROFILE_FILENAME, LOG_FILENAME):
            try:
                (resolved / entry).unlink(missing_ok=True)
            except OSError:
                continue
        try:
            resolved.rmdir()
        except OSError:
            pass

    def _load_registry_locked(self) -> list[dict[str, Any]]:
        """Load the registry, tolerating a missing or corrupt file.

        Returns:
            The list of registry records.
        """
        try:
            raw = self._registry_path.read_text(encoding="utf-8")
            data = json.loads(raw)
        except (OSError, json.JSONDecodeError):
            return []
        if not isinstance(data, list):
            return []
        return [record for record in data if isinstance(record, dict)]

    def _save_registry_locked(self, records: list[dict[str, Any]]) -> None:
        """Persist the registry atomically.

        Args:
            records: Registry records to write.
        """
        self._loops_dir.mkdir(parents=True, exist_ok=True)
        tmp_path = self._registry_path.with_suffix(".tmp")
        tmp_path.write_text(
            json.dumps(records, indent=2, ensure_ascii=False), encoding="utf-8"
        )
        os.replace(tmp_path, self._registry_path)


__all__ = [
    "DEFAULT_GOAL",
    "DEFAULT_ROUNDS",
    "DEFAULT_WORKERS",
    "KIND_AUTO_LOOP",
    "KIND_LAZY_NMAP",
    "LOOP_KINDS",
    "LoopManager",
    "LoopNotFoundError",
    "LoopSpec",
    "LoopValidationError",
    "MAX_CONCURRENT_LOOPS",
    "MAX_ROUNDS",
    "MAX_WORKERS",
    "clamp_float",
    "clamp_int",
    "sanitize_goal",
    "validate_target",
]
