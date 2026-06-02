"""LazyOwn metrics surface.

Two complementary subsystems live here:

* :class:`MetricsRegistry` (with the :data:`REGISTRY` singleton) — an
  in-memory Prometheus-style counter registry used by the C2 stack to
  expose live operational counters. Kept for backwards compatibility with
  ``lazyc2.py`` and ``modules.c2_builder``.
* :class:`MetricsRecorder` (with the :func:`get_recorder` singleton) — a
  durable append-only telemetry log written to ``sessions/metrics.jsonl``.
  Every command the operator executes through the cmd2 shell (and any
  other caller that opts in) is recorded so post-hoc analysis can answer
  "which commands fail most", "what is the p95 duration of nmap" or
  "where does the autonomous daemon stall".

The recorder splits responsibilities to keep each class small:

* :class:`MetricsWriter` only knows how to append a record to disk.
* :class:`MetricsAggregator` only knows how to compute summary statistics.
* :class:`MetricsRecorder` composes both behind a single public API.

Appends use a process-wide :class:`threading.Lock` so concurrent post-command
hooks (cmd2, autonomous daemon, MCP tool) cannot interleave half-written
lines. Writes are line-atomic but not durable across power loss; that is an
acceptable trade-off for telemetry data.
"""

from __future__ import annotations

import json
import logging
import math
import os
import threading
from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from threading import Lock
from typing import Dict, Iterable, List, Optional


LAZYOWN_DIR: Path = Path(
    os.environ.get("LAZYOWN_DIR", str(Path(__file__).resolve().parent.parent))
)
SESSIONS_DIR: Path = LAZYOWN_DIR / "sessions"
METRICS_FILE: Path = SESSIONS_DIR / "metrics.jsonl"

DEFAULT_TAIL: int = 50
P95_PERCENTILE: float = 0.95
TOP_FAILURE_LIMIT: int = 5
MAX_TAIL_LINES: int = 10_000

_log = logging.getLogger(__name__)


class MetricsRegistry:
    """Thread-safe in-memory counter registry used by the C2 stack.

    Counters are addressed by a name and an optional label dictionary; both
    pieces compose to form a series key. The registry can render itself in
    Prometheus exposition format when a scraper hits the C2 metrics
    endpoint.
    """

    def __init__(self) -> None:
        """Create an empty registry with its own lock."""

        self._counters: Dict[str, Dict[str, int]] = defaultdict(
            lambda: defaultdict(int)
        )
        self._lock = Lock()

    def inc(
        self,
        name: str,
        labels: Optional[Dict[str, str]] = None,
        value: int = 1,
    ) -> None:
        """Increment the named counter for the given labels.

        Args:
            name: Counter name.
            labels: Optional dictionary of label values forming a series.
            value: Amount to add; defaults to ``1``.
        """

        key = _labels_key(labels or {})
        with self._lock:
            self._counters[name][key] += value

    def get(
        self,
        name: str,
        labels: Optional[Dict[str, str]] = None,
    ) -> int:
        """Return the current value of a counter.

        Args:
            name: Counter name.
            labels: Optional label dictionary identifying the series.

        Returns:
            The current integer value (``0`` when the series has never
            been incremented).
        """

        key = _labels_key(labels or {})
        with self._lock:
            return self._counters[name][key]

    def prometheus_text(self) -> str:
        """Render every counter in Prometheus text exposition format.

        Returns:
            A newline-delimited Prometheus payload ready to be served as
            ``text/plain``.
        """

        lines: List[str] = []
        for name, series in self._counters.items():
            lines.append(f"# TYPE {name} counter")
            for label_key, value in series.items():
                if label_key:
                    lines.append(f'{name}{{{label_key}}} {value}')
                else:
                    lines.append(f'{name} {value}')
        return "\n".join(lines)


def _labels_key(labels: Dict[str, str]) -> str:
    """Render a label dictionary as a deterministic Prometheus key fragment.

    Args:
        labels: Label dictionary, possibly empty.

    Returns:
        A comma-separated ``key="value"`` string, or the empty string when
        no labels are provided.
    """

    if not labels:
        return ""
    return ",".join(f'{k}="{v}"' for k, v in sorted(labels.items()))


REGISTRY = MetricsRegistry()


@dataclass(frozen=True)
class MetricRecord:
    """One entry in ``sessions/metrics.jsonl``.

    Attributes:
        ts: ISO-8601 UTC timestamp captured at command completion.
        command: Command verb as typed by the operator (first token).
        args: Remaining argument string. May be empty.
        duration_ms: Wall-clock duration in milliseconds. Non-negative.
        success: Heuristic success flag derived from the caller's exit code.
        exit_code: Underlying process exit code. ``None`` when not measurable.
        source: Coarse origin tag (e.g. ``"cli"``, ``"daemon"``, ``"mcp"``).
    """

    ts: str
    command: str
    args: str
    duration_ms: int
    success: bool
    exit_code: Optional[int]
    source: str

    def to_dict(self) -> Dict[str, object]:
        """Return the record as a JSON-serialisable dictionary."""

        return {
            "ts": self.ts,
            "command": self.command,
            "args": self.args,
            "duration_ms": self.duration_ms,
            "success": self.success,
            "exit_code": self.exit_code,
            "source": self.source,
        }


class MetricsWriter:
    """Thread-safe append-only writer for :data:`METRICS_FILE`.

    The writer owns the lock and the file handle lifecycle but never
    decides *what* to write; callers compose a :class:`MetricRecord` and
    pass it in.
    """

    def __init__(self, path: Path = METRICS_FILE) -> None:
        """Initialise the writer.

        Args:
            path: Destination JSONL file. Parent directory is created on
                first append so empty sessions work too.
        """

        self._path = path
        self._lock = threading.Lock()

    @property
    def path(self) -> Path:
        """Return the JSONL destination path."""

        return self._path

    def append(self, record: MetricRecord) -> None:
        """Append a single record to disk.

        Failures are logged at debug level and swallowed: telemetry must
        never break the calling command.

        Args:
            record: The record to persist.
        """

        line = json.dumps(record.to_dict(), ensure_ascii=False, default=str)
        with self._lock:
            try:
                self._path.parent.mkdir(parents=True, exist_ok=True)
                with self._path.open("a", encoding="utf-8") as handle:
                    handle.write(line + "\n")
            except OSError as exc:
                _log.debug("metrics append error: %s", exc)


class MetricsAggregator:
    """Pure aggregation over an in-memory list of records.

    Separated from the writer so the same statistics can be computed over
    a test fixture without touching disk.
    """

    @staticmethod
    def _percentile(values: List[int], percentile: float) -> int:
        """Return the nearest-rank percentile of *values* in milliseconds.

        Args:
            values: Monotonically increasing list of integer durations.
                The caller is responsible for sorting; this helper does
                not.
            percentile: Target percentile in the closed interval
                ``[0, 1]``.

        Returns:
            The selected duration, or zero when *values* is empty.
        """

        if not values:
            return 0
        rank = max(1, math.ceil(percentile * len(values)))
        return values[rank - 1]

    @classmethod
    def summarize(
        cls,
        records: Iterable[Dict[str, object]],
        window_seconds: Optional[int] = None,
        now_utc: Optional[datetime] = None,
    ) -> Dict[str, object]:
        """Compute aggregate statistics over the supplied records.

        Args:
            records: Iterable of decoded JSONL entries.
            window_seconds: If set, ignore records older than this many
                seconds relative to *now_utc*.
            now_utc: Reference timestamp for the window. Defaults to the
                current UTC time. Supplied explicitly in tests.

        Returns:
            A dictionary with keys ``total``, ``window_seconds``,
            ``by_command`` and ``top_failures``.
        """

        reference = now_utc or datetime.now(timezone.utc)
        cutoff_epoch = (
            reference.timestamp() - window_seconds
            if window_seconds is not None and window_seconds > 0
            else None
        )

        per_command_durations: Dict[str, List[int]] = {}
        per_command_total: Dict[str, int] = {}
        per_command_success: Dict[str, int] = {}
        failure_counter: Dict[str, int] = {}
        total = 0

        for record in records:
            if not isinstance(record, dict):
                continue
            ts_raw = record.get("ts")
            if cutoff_epoch is not None and isinstance(ts_raw, str):
                record_epoch: Optional[float] = None
                try:
                    record_epoch = datetime.fromisoformat(ts_raw).timestamp()
                except ValueError:
                    record_epoch = None
                if record_epoch is not None and record_epoch < cutoff_epoch:
                    continue

            command = str(record.get("command", "")).strip() or "(unknown)"
            duration = int(record.get("duration_ms", 0) or 0)
            success = bool(record.get("success", False))

            per_command_total[command] = per_command_total.get(command, 0) + 1
            per_command_durations.setdefault(command, []).append(duration)
            if success:
                per_command_success[command] = (
                    per_command_success.get(command, 0) + 1
                )
            else:
                failure_counter[command] = failure_counter.get(command, 0) + 1
            total += 1

        by_command: Dict[str, Dict[str, float]] = {}
        for command, durations in per_command_durations.items():
            durations.sort()
            count = per_command_total[command]
            successes = per_command_success.get(command, 0)
            by_command[command] = {
                "count": count,
                "success_rate": (successes / count) if count else 0.0,
                "mean_duration_ms": sum(durations) / count,
                "p95_duration_ms": cls._percentile(durations, P95_PERCENTILE),
            }

        top_failures = sorted(
            failure_counter.items(), key=lambda item: item[1], reverse=True
        )[:TOP_FAILURE_LIMIT]

        return {
            "total": total,
            "window_seconds": window_seconds,
            "by_command": by_command,
            "top_failures": [
                {"command": cmd, "failures": fails}
                for cmd, fails in top_failures
            ],
        }


class MetricsRecorder:
    """Compose a :class:`MetricsWriter` and :class:`MetricsAggregator`.

    Operators interact only with this class through the module-level
    singleton returned by :func:`get_recorder`.
    """

    def __init__(self, writer: Optional[MetricsWriter] = None) -> None:
        """Initialise the recorder.

        Args:
            writer: Writer instance to use. Injected in tests; defaults to
                a writer pointing at :data:`METRICS_FILE`.
        """

        self._writer = writer or MetricsWriter()

    @property
    def path(self) -> Path:
        """Return the JSONL path used by the underlying writer."""

        return self._writer.path

    def record(
        self,
        command: str,
        args: str = "",
        duration_ms: int = 0,
        success: bool = True,
        exit_code: Optional[int] = None,
        source: str = "cli",
    ) -> None:
        """Persist a single command-execution telemetry record.

        Args:
            command: First token of the operator-typed command.
            args: Remaining argument string (may be empty).
            duration_ms: Wall-clock duration in milliseconds, clamped to a
                non-negative integer.
            success: Heuristic success flag.
            exit_code: Underlying process exit code, when known.
            source: Coarse origin tag.
        """

        clean_duration = max(0, int(duration_ms))
        record = MetricRecord(
            ts=datetime.now(timezone.utc).isoformat(),
            command=str(command),
            args=str(args),
            duration_ms=clean_duration,
            success=bool(success),
            exit_code=exit_code if exit_code is None else int(exit_code),
            source=str(source),
        )
        self._writer.append(record)

    def _read_all(self) -> List[Dict[str, object]]:
        """Return every record currently present in the JSONL file.

        Lines that fail to decode are skipped with a debug log entry.

        Returns:
            A list of decoded records, oldest first. Empty when the file
            does not exist or is unreadable.
        """

        path = self._writer.path
        records: List[Dict[str, object]] = []
        if not path.exists():
            return records
        try:
            with path.open("r", encoding="utf-8") as handle:
                for raw in handle:
                    raw = raw.strip()
                    if not raw:
                        continue
                    try:
                        records.append(json.loads(raw))
                    except json.JSONDecodeError as exc:
                        _log.debug("metrics decode error: %s", exc)
        except OSError as exc:
            _log.debug("metrics read error: %s", exc)
        return records

    def summarize(
        self, window_seconds: Optional[int] = None
    ) -> Dict[str, object]:
        """Return aggregate statistics over recorded events.

        Args:
            window_seconds: Restrict the calculation to events from the
                last *N* seconds. ``None`` aggregates the whole file.

        Returns:
            Dictionary as documented in
            :meth:`MetricsAggregator.summarize`.
        """

        return MetricsAggregator.summarize(self._read_all(), window_seconds)

    def tail(self, n: int = DEFAULT_TAIL) -> List[Dict[str, object]]:
        """Return the most recent *n* records, newest first.

        Args:
            n: Number of records to return. Clamped to
                :data:`MAX_TAIL_LINES`.

        Returns:
            A list of records in reverse chronological order.
        """

        capped = max(0, min(int(n), MAX_TAIL_LINES))
        if capped == 0:
            return []
        records = self._read_all()
        return list(reversed(records[-capped:]))


_recorder_lock = threading.Lock()
_recorder: Optional[MetricsRecorder] = None


def get_recorder() -> MetricsRecorder:
    """Return the process-wide :class:`MetricsRecorder` singleton.

    The first call constructs a recorder bound to :data:`METRICS_FILE`.
    Subsequent calls return the same instance. Thread-safe.
    """

    global _recorder
    with _recorder_lock:
        if _recorder is None:
            _recorder = MetricsRecorder()
        return _recorder


def reset_recorder_for_tests(
    writer: Optional[MetricsWriter] = None,
) -> MetricsRecorder:
    """Replace the module-level recorder with a fresh instance.

    Intended exclusively for tests that need to redirect the JSONL path.

    Args:
        writer: Optional writer to inject. When omitted a default writer
            against :data:`METRICS_FILE` is used.

    Returns:
        The newly installed recorder.
    """

    global _recorder
    with _recorder_lock:
        _recorder = MetricsRecorder(writer=writer)
        return _recorder
