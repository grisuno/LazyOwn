"""Planned-versus-actual deviation ledger for loop and chain runs.

Mined from sapper-v2's explore deviations section and reimplemented
LazyOwn-native as one shared append-only ledger. Whenever the system
changes a plan on purpose — the loop sanitizer rewrites a model-proposed
command, an apt_chain replanner inserts steps or binds variables — the
planned value, the actual value and the reason land here, so handoffs
and reports can show not just what ran but why it differed from what
was planned.

One contract per file (SOLID): this module owns the ledger record
model, storage and rendering. Callers (loop sanitizer, chain replanner)
inject their own scope keys; the ledger never interprets them.

Storage: ``sessions/lazy/deviations.jsonl``, one JSON object per line,
capped at ``DEVIATIONS_MAX_RECORDS`` rows (oldest dropped). Never
raises on read; write errors are swallowed because a lost deviation
note must never kill a step that already succeeded.
"""

from __future__ import annotations

import json
import time
from dataclasses import dataclass
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DEFAULT_LEDGER_PATH = BASE_DIR / "sessions" / "lazy" / "deviations.jsonl"
DEVIATIONS_MAX_RECORDS = 500
DEVIATIONS_TEXT_LIMIT = 400


@dataclass(frozen=True)
class DeviationRecord:
    """One recorded planned-versus-actual deviation.

    Attributes:
        ts: Unix timestamp of the record.
        scope: Free-form grouping key (``loop:<task_id>``,
            ``chain:<name>:<run_id>``).
        planned: What the plan said before the change.
        actual: What actually ran or was inserted.
        reason: Why the plan changed.
        source: Subsystem that recorded the deviation.
    """

    ts: float
    scope: str
    planned: str
    actual: str
    reason: str
    source: str

    def as_dict(self) -> dict:
        """Return the record as a JSON-ready dict."""
        return {
            "ts": self.ts,
            "scope": self.scope,
            "planned": self.planned,
            "actual": self.actual,
            "reason": self.reason,
            "source": self.source,
        }


def _clean(text: str) -> str:
    """Collapse a deviation text to one bounded single line."""
    return " ".join(str(text or "").split())[:DEVIATIONS_TEXT_LIMIT]


class DeviationLedger:
    """Append-only planned-versus-actual ledger shared by loop and chain.

    Args:
        path: Ledger file override (tests); defaults to
            ``sessions/lazy/deviations.jsonl``.
    """

    def __init__(self, path: Path | None = None) -> None:
        """Bind the ledger file path."""
        self._path = Path(path) if path is not None else DEFAULT_LEDGER_PATH

    def record(
        self,
        scope: str,
        planned: str,
        actual: str,
        reason: str,
        source: str = "",
    ) -> DeviationRecord | None:
        """Record one deviation when the plan actually changed.

        Args:
            scope: Grouping key, e.g. ``loop:t0001``.
            planned: Planned command, step or value.
            actual: What replaced it.
            reason: Why it was replaced; empty suppresses the record.
            source: Recording subsystem name.

        Returns:
            The stored record, or None when there is no deviation
            (planned equals actual, or the reason is empty) or the write
            failed.
        """
        planned_text = _clean(planned)
        actual_text = _clean(actual)
        reason_text = _clean(reason)
        if not reason_text or planned_text == actual_text:
            return None
        if self._last_matches(scope, planned_text, actual_text, reason_text):
            return None
        record = DeviationRecord(
            ts=time.time(),
            scope=str(scope or ""),
            planned=planned_text,
            actual=actual_text,
            reason=reason_text,
            source=str(source or ""),
        )
        self._append(record)
        return record

    def list(self, scope: str = "", limit: int = 50) -> list[DeviationRecord]:
        """Return deviations, newest first, optionally scoped.

        Args:
            scope: Grouping key filter; empty returns every scope.
            limit: Maximum rows to return.

        Returns:
            Deviation records, newest first.
        """
        rows = self._read()
        if scope:
            rows = [row for row in rows if row.scope == scope]
        rows.reverse()
        return rows[: max(0, int(limit))]

    def render_markdown(self, records: list[DeviationRecord], title: str = "Deviations") -> str:
        """Render records as the sapper-style deviations block.

        Args:
            records: Records in display order.
            title: Section title.

        Returns:
            Markdown lines; empty string when no records exist.
        """
        if not records:
            return ""
        lines = [f"## {title}", ""]
        for record in records:
            lines.append(
                f"- **Planned:** {record.planned} -> **Actual:** {record.actual}"
                f" — *Reason:* {record.reason}"
            )
        return "\n".join(lines)

    def _last_matches(self, scope: str, planned: str, actual: str, reason: str) -> bool:
        """Whether the newest record for a scope already holds this entry."""
        latest = self.list(scope, limit=1)
        if not latest:
            return False
        latest = latest[0]
        return (
            latest.planned == planned
            and latest.actual == actual
            and latest.reason == reason
        )

    def _read(self) -> list[DeviationRecord]:
        """Read the ledger tolerating missing files and broken lines."""
        try:
            lines = self._path.read_text(encoding="utf-8", errors="replace").splitlines()
        except OSError:
            return []
        out: list[DeviationRecord] = []
        for line in lines:
            try:
                data = json.loads(line)
            except ValueError:
                continue
            if not isinstance(data, dict):
                continue
            try:
                out.append(
                    DeviationRecord(
                        ts=float(data.get("ts", 0.0) or 0.0),
                        scope=str(data.get("scope", "")),
                        planned=str(data.get("planned", "")),
                        actual=str(data.get("actual", "")),
                        reason=str(data.get("reason", "")),
                        source=str(data.get("source", "")),
                    )
                )
            except (TypeError, ValueError):
                continue
        return out

    def _append(self, record: DeviationRecord) -> bool:
        """Append one record and enforce the file cap. Never raises."""
        try:
            self._path.parent.mkdir(parents=True, exist_ok=True)
            try:
                self._path.chmod(0o600)
            except OSError:
                pass
            with open(self._path, "a", encoding="utf-8") as handle:
                handle.write(json.dumps(record.as_dict(), ensure_ascii=False) + "\n")
            self._trim()
            return True
        except OSError:
            return False

    def _trim(self) -> None:
        """Rewrite the ledger keeping only the newest rows."""
        rows = self._read()
        if len(rows) <= DEVIATIONS_MAX_RECORDS:
            return
        keep = rows[-DEVIATIONS_MAX_RECORDS:]
        try:
            tmp = self._path.with_suffix(".tmp")
            with open(tmp, "w", encoding="utf-8") as handle:
                for row in keep:
                    handle.write(json.dumps(row.as_dict(), ensure_ascii=False) + "\n")
            tmp.replace(self._path)
        except OSError:
            pass


__all__ = [
    "DEFAULT_LEDGER_PATH",
    "DEVIATIONS_MAX_RECORDS",
    "DEVIATIONS_TEXT_LIMIT",
    "DeviationLedger",
    "DeviationRecord",
]
