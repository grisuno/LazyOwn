"""TTP coverage matrix — real-time MITRE ATT&CK technique tracking.

Aggregates executed techniques from all operations, playbooks, and
atomic tests into a single matrix view.

Statuses:
    tested   — technique was executed and produced output
    failed   — technique was attempted but produced no useful output
    blocked  — technique is gated by unmet facts (planner couldn't run it)
    queued   — technique is scheduled but not yet executed
    ready    — all required facts are present, technique is runnable
    untested — technique is available but never attempted
"""

from __future__ import annotations

import json
import logging
from collections import defaultdict
from dataclasses import asdict, dataclass, field
from datetime import datetime
from pathlib import Path

log = logging.getLogger("ttp_coverage")

_BASE_DIR     = Path(__file__).parent.parent
_OPS_DIR      = _BASE_DIR / "sessions" / "operations"
_TTP_PATH     = _BASE_DIR / "sessions" / "ttp_coverage.json"
_APT_DIR      = _BASE_DIR / "playbooks"


# ---------------------------------------------------------------------------
# MITRE tactic ordering (kill chain)
# ---------------------------------------------------------------------------

TACTIC_ORDER = [
    "reconnaissance",
    "resource-development",
    "initial-access",
    "execution",
    "persistence",
    "privilege-escalation",
    "defense-evasion",
    "credential-access",
    "discovery",
    "lateral-movement",
    "collection",
    "command-and-control",
    "exfiltration",
    "impact",
]


@dataclass
class TTPRow:
    technique_id: str
    name: str
    tactic: str
    status: str = "untested"
    last_run: str = ""
    operations: list[str] = field(default_factory=list)
    findings_count: int = 0


class TTPCoverage:
    """Aggregate TTP execution data across all operations."""

    def __init__(self) -> None:
        self.rows: dict[str, TTPRow] = {}
        self._load_state()

    # ------------------------------------------------------------------
    # Aggregation
    # ------------------------------------------------------------------

    def rebuild_from_operations(self) -> int:
        """Re-walk every operation on disk and refresh the matrix.

        Returns the number of techniques covered.
        """
        self.rows.clear()
        ops_path = _OPS_DIR
        if not ops_path.is_dir():
            return 0
        n = 0
        for op_file in sorted(ops_path.glob("*.json")):
            try:
                with open(op_file) as f:
                    data = json.load(f)
            except Exception:
                continue
            op_id = data.get("id", op_file.stem)
            steps = data.get("steps", [])
            step_lookup = {s.get("technique_id", ""): s for s in steps if s.get("technique_id")}
            for tid, status in data.get("ttp_coverage", {}).items():
                if not tid:
                    continue
                step = step_lookup.get(tid, {})
                step_name = step.get("name", "")
                step_tactic = step.get("tactic", "").replace("_", "-")
                if tid not in self.rows:
                    self.rows[tid] = TTPRow(
                        technique_id=tid,
                        name=step_name,
                        tactic=step_tactic,
                    )
                row = self.rows[tid]
                if not row.name and step_name:
                    row.name = step_name
                if not row.tactic and step_tactic:
                    row.tactic = step_tactic
                if op_id not in row.operations:
                    row.operations.append(op_id)
                if status in ("tested", "completed"):
                    row.status = "tested"
                elif status == "failed" and row.status != "tested":
                    row.status = "failed"
                elif status == "ready" and row.status not in ("tested",):
                    row.status = "ready"
                row.last_run = data.get("finished_at") or data.get("started_at", "")
                n += 1
        self._save_state()
        return n

    def add(self, technique_id: str, name: str = "", tactic: str = "",
            status: str = "tested", operation_id: str = "") -> None:
        if technique_id not in self.rows:
            self.rows[technique_id] = TTPRow(
                technique_id=technique_id, name=name, tactic=tactic,
            )
        row = self.rows[technique_id]
        if name:
            row.name = name
        if tactic:
            row.tactic = tactic
        row.status = status
        row.last_run = datetime.now().isoformat(timespec="seconds")
        if operation_id and operation_id not in row.operations:
            row.operations.append(operation_id)
        self._save_state()

    # ------------------------------------------------------------------
    # Planning
    # ------------------------------------------------------------------

    def compute_ready(self, available_facts: list[str]) -> list[TTPRow]:
        """Return the techniques that could run given available facts.

        A technique is ``ready`` if no blocking fact is missing. The
        rule used here is conservative — the technique is considered
        ready if it is ``untested`` and at least one fact matches the
        technique's tactic (e.g. ``service.found`` is enough for
        ``T1021.*``). Operators should refine this with their own
        ability dependency data when available.
        """
        ready: list[TTPRow] = []
        for row in self.rows.values():
            if row.status not in ("untested", "blocked"):
                continue
            if any(f in available_facts for f in self._blocking_facts(row.tactic)):
                row.status = "ready"
                ready.append(row)
        return ready

    def _blocking_facts(self, tactic: str) -> list[str]:
        if not tactic:
            return ["host.found"]
        m = {
            "reconnaissance":     ["host.found", "ip.discovered"],
            "discovery":          ["host.found", "service.found"],
            "initial-access":     ["service.found"],
            "execution":          ["host.found", "session.created"],
            "persistence":        ["session.created"],
            "privilege-escalation": ["session.created"],
            "credential-access":  ["host.found"],
            "lateral-movement":   ["credential.valid", "session.created"],
            "collection":         ["session.created"],
            "exfiltration":       ["file.found"],
            "command-and-control": ["session.created"],
        }
        return m.get(tactic, ["host.found"])

    # ------------------------------------------------------------------
    # Reporting
    # ------------------------------------------------------------------

    def matrix(self) -> str:
        """Render a coloured-by-tactic table of all techniques."""
        if not self.rows:
            return "No TTP coverage data. Run 'op_plan' and 'op_start' to populate."

        status_mark = {
            "tested":   "[x]",
            "failed":   "[!]",
            "blocked":  "[B]",
            "queued":   "[Q]",
            "ready":    "[R]",
            "untested": "[ ]",
        }

        groups: dict[str, list[TTPRow]] = defaultdict(list)
        for row in self.rows.values():
            tac = row.tactic or "unmapped"
            groups[tac].append(row)

        lines = [
            f"TTP coverage: {len(self.rows)} techniques tracked",
            f"  Tested   : {sum(1 for r in self.rows.values() if r.status == 'tested')}",
            f"  Ready    : {sum(1 for r in self.rows.values() if r.status == 'ready')}",
            f"  Failed   : {sum(1 for r in self.rows.values() if r.status == 'failed')}",
            f"  Untested : {sum(1 for r in self.rows.values() if r.status == 'untested')}",
            "",
        ]
        for tactic in TACTIC_ORDER:
            if tactic not in groups:
                continue
            lines.append(f"--- {tactic.upper()} ---")
            for row in sorted(groups[tactic], key=lambda r: r.technique_id):
                mark = status_mark.get(row.status, "[?]")
                lines.append(
                    f"  {mark} {row.technique_id:<10} {row.name:<50} "
                    f"op={','.join(row.operations[:2])}"
                )
        if "unmapped" in groups:
            lines.append("--- UNMAPPED ---")
            for row in sorted(groups["unmapped"], key=lambda r: r.technique_id):
                mark = status_mark.get(row.status, "[?]")
                lines.append(f"  {mark} {row.technique_id:<10} {row.name}")
        return "\n".join(lines)

    def status_by_id(self, technique_id: str) -> TTPRow | None:
        return self.rows.get(technique_id)

    def to_dict(self) -> dict:
        return {tid: asdict(r) for tid, r in self.rows.items()}

    # ------------------------------------------------------------------
    # Persistence
    # ------------------------------------------------------------------

    def _save_state(self) -> None:
        try:
            with open(_TTP_PATH, "w") as f:
                json.dump(self.to_dict(), f, indent=2, default=str)
        except Exception as exc:
            log.debug("ttp save failed: %s", exc)

    def _load_state(self) -> None:
        if not _TTP_PATH.exists():
            return
        try:
            with open(_TTP_PATH) as f:
                data = json.load(f)
            for tid, row in data.items():
                self.rows[tid] = TTPRow(**row)
        except Exception as exc:
            log.debug("ttp load failed: %s", exc)


def get_coverage() -> TTPCoverage:
    """Return a fresh :class:`TTPCoverage`."""
    return TTPCoverage()


__all__ = ["TTPCoverage", "TTPRow", "TACTIC_ORDER", "get_coverage"]
