"""
llm_evaluator.py — Records LLM decisions and their outcomes, computes quality
metrics, and exports fine-tuning datasets for the LazyOwn auto_loop.
"""

from __future__ import annotations

import argparse
import json
import threading
import time
import uuid
from abc import ABC, abstractmethod
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Dict, List, Optional

_JSONL_PATH = Path(__file__).parent.parent / "sessions" / "llm_decisions.jsonl"


@dataclass
class DecisionRecord:
    id: str
    session_id: str
    ts: float
    thought: str
    action: str
    mitre_tactic: str
    expected_outcome: str
    actual_outcome: str
    findings_count: int
    success: bool
    confidence: float


def _new_id() -> str:
    return uuid.uuid4().hex


def _record_from_dict(d: dict) -> DecisionRecord:
    return DecisionRecord(
        id=d.get("id", _new_id()),
        session_id=d.get("session_id", ""),
        ts=float(d.get("ts", 0.0)),
        thought=d.get("thought", ""),
        action=d.get("action", ""),
        mitre_tactic=d.get("mitre_tactic", ""),
        expected_outcome=d.get("expected_outcome", ""),
        actual_outcome=d.get("actual_outcome", ""),
        findings_count=int(d.get("findings_count", 0)),
        success=bool(d.get("success", False)),
        confidence=float(d.get("confidence", 0.0)),
    )


class OutcomeRecorder(ABC):
    @abstractmethod
    def record(self, decision: DecisionRecord) -> None: ...

    @abstractmethod
    def update_outcome(
        self,
        decision_id: str,
        actual: str,
        findings_count: int,
        success: bool,
    ) -> None: ...

    @abstractmethod
    def load_all(self) -> List[DecisionRecord]: ...

    @abstractmethod
    def load_by_session(self, session_id: str) -> List[DecisionRecord]: ...


class JSONLRecorder(OutcomeRecorder):
    def __init__(self, path: Path = _JSONL_PATH) -> None:
        self._path = path
        self._path.parent.mkdir(parents=True, exist_ok=True)
        self._lock = threading.RLock()

    def record(self, decision: DecisionRecord) -> None:
        with self._lock:
            with self._path.open("a", encoding="utf-8") as fh:
                fh.write(json.dumps(asdict(decision), ensure_ascii=False) + "\n")

    def update_outcome(
        self,
        decision_id: str,
        actual: str,
        findings_count: int,
        success: bool,
    ) -> None:
        with self._lock:
            if not self._path.exists():
                return
            lines = self._path.read_text(encoding="utf-8").splitlines(keepends=True)
            updated = False
            new_lines: List[str] = []
            for line in lines:
                line_stripped = line.strip()
                if not line_stripped:
                    new_lines.append(line)
                    continue
                try:
                    d = json.loads(line_stripped)
                except json.JSONDecodeError:
                    new_lines.append(line)
                    continue
                if d.get("id") == decision_id:
                    d["actual_outcome"] = actual
                    d["findings_count"] = findings_count
                    d["success"] = success
                    new_lines.append(json.dumps(d, ensure_ascii=False) + "\n")
                    updated = True
                else:
                    new_lines.append(line)
            if updated:
                self._path.write_text("".join(new_lines), encoding="utf-8")

    def load_all(self) -> List[DecisionRecord]:
        with self._lock:
            if not self._path.exists():
                return []
            records: List[DecisionRecord] = []
            for line in self._path.read_text(encoding="utf-8").splitlines():
                line = line.strip()
                if not line:
                    continue
                try:
                    records.append(_record_from_dict(json.loads(line)))
                except (json.JSONDecodeError, KeyError):
                    continue
            return records

    def load_by_session(self, session_id: str) -> List[DecisionRecord]:
        return [r for r in self.load_all() if r.session_id == session_id]


@dataclass
class QualityMetrics:
    total_decisions: int
    success_rate: float
    avg_findings_per_decision: float
    top_tactics: List[str]
    worst_tactics: List[str]
    avg_confidence_when_correct: float
    avg_confidence_when_wrong: float


def _safe_mean(values: List[float]) -> float:
    return sum(values) / len(values) if values else 0.0


def _tactic_success_rates(records: List[DecisionRecord]) -> Dict[str, float]:
    tactic_success: Dict[str, List[bool]] = {}
    for r in records:
        tactic_success.setdefault(r.mitre_tactic, []).append(r.success)
    return {t: sum(v) / len(v) for t, v in tactic_success.items()}


class LLMEvaluator:
    def __init__(self, recorder: OutcomeRecorder) -> None:
        self._recorder = recorder

    def record_decision(
        self,
        session_id: str,
        thought: str,
        action: str,
        mitre_tactic: str,
        expected_outcome: str,
        confidence: float,
    ) -> str:
        decision_id = _new_id()
        decision = DecisionRecord(
            id=decision_id,
            session_id=session_id,
            ts=time.time(),
            thought=thought,
            action=action,
            mitre_tactic=mitre_tactic,
            expected_outcome=expected_outcome,
            actual_outcome="",
            findings_count=0,
            success=False,
            confidence=confidence,
        )
        self._recorder.record(decision)
        return decision_id

    def record_outcome(
        self,
        decision_id: str,
        actual_outcome: str,
        findings_count: int,
        success: bool,
    ) -> None:
        self._recorder.update_outcome(decision_id, actual_outcome, findings_count, success)

    def compute_metrics(self, session_id: Optional[str] = None) -> QualityMetrics:
        if session_id:
            records = self._recorder.load_by_session(session_id)
        else:
            records = self._recorder.load_all()

        if not records:
            return QualityMetrics(
                total_decisions=0,
                success_rate=0.0,
                avg_findings_per_decision=0.0,
                top_tactics=[],
                worst_tactics=[],
                avg_confidence_when_correct=0.0,
                avg_confidence_when_wrong=0.0,
            )

        total = len(records)
        successes = [r for r in records if r.success]
        failures = [r for r in records if not r.success]
        success_rate = len(successes) / total
        avg_findings = _safe_mean([float(r.findings_count) for r in records])

        rates = _tactic_success_rates(records)
        sorted_tactics = sorted(rates, key=rates.get, reverse=True)
        top_tactics = sorted_tactics[:3]
        worst_tactics = list(reversed(sorted_tactics))[:3]

        avg_conf_correct = _safe_mean([r.confidence for r in successes])
        avg_conf_wrong = _safe_mean([r.confidence for r in failures])

        return QualityMetrics(
            total_decisions=total,
            success_rate=success_rate,
            avg_findings_per_decision=avg_findings,
            top_tactics=top_tactics,
            worst_tactics=worst_tactics,
            avg_confidence_when_correct=avg_conf_correct,
            avg_confidence_when_wrong=avg_conf_wrong,
        )

    def quality_report(self, session_id: Optional[str] = None) -> str:
        m = self.compute_metrics(session_id)
        scope = f"session={session_id}" if session_id else "all sessions"
        lines = [
            f"Quality Report ({scope})",
            f"  Total decisions         : {m.total_decisions}",
            f"  Success rate            : {m.success_rate:.1%}",
            f"  Avg findings/decision   : {m.avg_findings_per_decision:.2f}",
            f"  Top MITRE tactics       : {', '.join(m.top_tactics) or 'n/a'}",
            f"  Worst MITRE tactics     : {', '.join(m.worst_tactics) or 'n/a'}",
            f"  Avg confidence (correct): {m.avg_confidence_when_correct:.3f}",
            f"  Avg confidence (wrong)  : {m.avg_confidence_when_wrong:.3f}",
        ]
        return "\n".join(lines)

    def export_finetuning_dataset(self, path: Optional[Path] = None) -> Path:
        if path is None:
            path = Path(__file__).parent.parent / "sessions" / "llm_finetuning.jsonl"
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        records = self._recorder.load_all()
        with path.open("w", encoding="utf-8") as fh:
            for r in records:
                if not r.success:
                    continue
                user_content = (
                    f"You are a penetration testing AI. "
                    f"Given this context, decide the next action.\n"
                    f"Thought: {r.thought}\n"
                    f"MITRE Tactic: {r.mitre_tactic}\n"
                    f"Expected Outcome: {r.expected_outcome}"
                )
                assistant_content = (
                    f"Action: {r.action}\n"
                    f"Actual Outcome: {r.actual_outcome}\n"
                    f"Findings Count: {r.findings_count}\n"
                    f"Confidence: {r.confidence:.3f}"
                )
                record = {
                    "messages": [
                        {"role": "user", "content": user_content},
                        {"role": "assistant", "content": assistant_content},
                    ]
                }
                fh.write(json.dumps(record, ensure_ascii=False) + "\n")
        return path


_evaluator_instance: Optional[LLMEvaluator] = None
_evaluator_lock = threading.Lock()


def get_evaluator() -> LLMEvaluator:
    global _evaluator_instance
    if _evaluator_instance is None:
        with _evaluator_lock:
            if _evaluator_instance is None:
                _evaluator_instance = LLMEvaluator(JSONLRecorder())
    return _evaluator_instance


def record_decision(
    session_id: str,
    thought: str,
    action: str,
    mitre_tactic: str,
    expected_outcome: str,
    confidence: float,
) -> str:
    return get_evaluator().record_decision(
        session_id, thought, action, mitre_tactic, expected_outcome, confidence
    )


def record_outcome(
    decision_id: str,
    actual_outcome: str,
    findings_count: int,
    success: bool,
) -> None:
    get_evaluator().record_outcome(decision_id, actual_outcome, findings_count, success)


def _cli() -> None:
    parser = argparse.ArgumentParser(
        description="LLM decision evaluator for the LazyOwn auto_loop."
    )
    parser.add_argument(
        "--report", action="store_true", help="Print quality report"
    )
    parser.add_argument(
        "--session", help="Limit report/export to a specific session ID"
    )
    parser.add_argument(
        "--export", metavar="PATH", help="Export fine-tuning JSONL to PATH"
    )
    args = parser.parse_args()

    ev = get_evaluator()

    if args.report:
        print(ev.quality_report(session_id=args.session))

    if args.export:
        out_path = ev.export_finetuning_dataset(Path(args.export))
        print(f"Fine-tuning dataset written to: {out_path}")

    if not args.report and not args.export:
        parser.print_help()


if __name__ == "__main__":
    _cli()
