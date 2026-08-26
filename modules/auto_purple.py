"""Purple Team Closed-Loop — honest measurement of offensive detection.

Orchestrates the cycle: execute red action -> measure with LazyOwnBT (blue)
-> record real results -> generate ML training datasets -> calibrate oracle.

Every engagement produces a CSV dataset that LazyOwnBT can ingest to improve
its RandomForest detection model. This is a genuine feedback loop, not static
probability guessing.

Design principles
-----------------
- Single Responsibility : purple loop orchestration only
- Open/Closed           : new detection methods added via _DETECTION_METHODS
- Dependency Inversion  : callers depend on IPurpleLoop, not PurpleTeamLoop
- Interface Segregation : read-only IPurpleEvaluator vs read-write IPurpleLoop
- No secrets            : config from payload.json, paths from sessions/

Usage
-----
    from modules.auto_purple import get_loop

    loop = get_loop()
    result = loop.execute_and_measure("mimikatz", "sekurlsa::logonpasswords", "credential")
    print(f"Detected: {result.actually_detected}  Oracle predicted: {result.oracle_prediction:.0%}")
"""
from __future__ import annotations

import csv
import json
import logging
import os
import re
import subprocess
import sys
import time
from abc import ABC, abstractmethod
from dataclasses import asdict, dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any

log = logging.getLogger(__name__)

_SESSIONS_DIR = Path(__file__).resolve().parent.parent / "sessions"
_PURPLE_DIR = _SESSIONS_DIR
_DATASET_FILE = _PURPLE_DIR / "purple_dataset.csv"
_AUDIT_FILE = _PURPLE_DIR / "purple_audit.jsonl"
_FEEDBACK_FILE = _SESSIONS_DIR / "detection_feedback.jsonl"
_SCORE_FILE = _PURPLE_DIR / "purple_score.json"
_REPORT_FILE = _PURPLE_DIR / "purple_report.json"
_BT_LOG_FILE = _PURPLE_DIR / "purple_bt_output.log"

_DATASET_FIELDS = [
    "timestamp", "command", "args", "category",
    "oracle_prediction", "actually_detected", "detection_methods",
    "red_output_hash", "session_id",
]

# ---------------------------------------------------------------------------
# Detection method registry (Open/Closed: extend this list, not the class)
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class DetectionMethod:
    """Describes one LazyOwnBT detection surface."""
    name: str
    bt_command: str
    output_parser: str
    description: str


_DETECTION_METHODS: list[DetectionMethod] = [
    DetectionMethod(
        name="ai_test",
        bt_command="ai_test {command} {args}",
        output_parser="ai_test",
        description="ML model (RandomForest + TF-IDF) prediction",
    ),
    DetectionMethod(
        name="proc_scan",
        bt_command="proc_scan",
        output_parser="keyword_match",
        description="Process anomaly detection",
    ),
    DetectionMethod(
        name="net_scan",
        bt_command="net_scan",
        output_parser="keyword_match",
        description="Network connection anomalies",
    ),
    DetectionMethod(
        name="log_analyze",
        bt_command="log_analyze",
        output_parser="alert_check",
        description="Log pattern analysis for threat indicators",
    ),
    DetectionMethod(
        name="fim_scan",
        bt_command="fim_scan",
        output_parser="fim_check",
        description="File integrity monitoring",
    ),
    DetectionMethod(
        name="redteam_hunt",
        bt_command="redteam_hunt",
        output_parser="keyword_match",
        description="IOC and TTP matching against known red team patterns",
    ),
    DetectionMethod(
        name="memory_scan",
        bt_command="memory_scan",
        output_parser="keyword_match",
        description="Process memory string scanning for shellcode/C2",
    ),
]

# ---------------------------------------------------------------------------
# Value objects
# ---------------------------------------------------------------------------


@dataclass
class PurpleResult:
    """Result of a single red action measurement."""
    command: str
    args: str
    category: str
    oracle_prediction: float
    actually_detected: bool
    detection_methods: dict[str, bool]
    red_output_hash: str
    session_id: str
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    detection_raw: dict[str, str] = field(default_factory=dict)

    def to_csv_row(self) -> dict[str, str]:
        """Serialize to a flat dict suitable for CSV writer."""
        return {
            "timestamp": self.timestamp,
            "command": self.command,
            "args": self.args,
            "category": self.category,
            "oracle_prediction": f"{self.oracle_prediction:.4f}",
            "actually_detected": str(self.actually_detected).lower(),
            "detection_methods": json.dumps(self.detection_methods),
            "red_output_hash": self.red_output_hash,
            "session_id": self.session_id,
        }

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class PurpleScore:
    """Aggregated detection score for an engagement."""
    total: int
    detected: int
    missed: int
    score: float
    by_category: dict[str, dict[str, int]]
    by_method: dict[str, dict[str, int]]


# ---------------------------------------------------------------------------
# Interface
# ---------------------------------------------------------------------------


class IPurpleLoop(ABC):
    """Read-write contract for purple team orchestration."""

    @abstractmethod
    def execute_and_measure(
        self, command: str, args: str, category: str,
    ) -> PurpleResult: ...

    @abstractmethod
    def measure_only(
        self, command: str, args: str, category: str,
    ) -> PurpleResult: ...

    @abstractmethod
    def engagement_score(self) -> PurpleScore: ...

    @abstractmethod
    def export_dataset(self) -> Path: ...

    @abstractmethod
    def export_report(self) -> Path: ...


class IPurpleEvaluator(ABC):
    """Read-only contract for evaluation queries."""

    @abstractmethod
    def last_results(self, n: int = 10) -> list[PurpleResult]: ...

    @abstractmethod
    def category_accuracy(self, category: str) -> dict[str, Any]: ...


# ---------------------------------------------------------------------------
# LazyOwnBT subprocess interface
# ---------------------------------------------------------------------------


def _run_bt_command(bt_path: str, command: str, timeout: int = 30) -> str:
    """Execute a LazyOwnBT CLI command via PTY subprocess.

    Same pattern as skills/lazyownbt_mcp.py._run_lazyownbt_command.
    """
    import fcntl
    import pty
    import select
    import struct
    import termios

    bt_path = os.path.abspath(bt_path)
    bt_app = os.path.join(bt_path, "app.py")
    if not os.path.isfile(bt_app):
        return f"[error] LazyOwnBT app.py not found at {bt_app}"

    bt_venv_python = os.path.join(bt_path, "env", "bin", "python3")
    if not os.path.isfile(bt_venv_python):
        bt_venv_python = sys.executable

    cmd_input = (command.strip() + "\nexit\n").encode()
    argv = [bt_venv_python, "-W", "ignore", bt_app]

    env = os.environ.copy()
    env["TERM"] = "xterm-256color"

    master_fd, slave_fd = pty.openpty()
    winsize = struct.pack("HHHH", 50, 220, 0, 0)
    try:
        fcntl.ioctl(slave_fd, termios.TIOCSWINSZ, winsize)
    except Exception:
        pass

    output_chunks: list[str] = []
    try:
        proc = subprocess.Popen(
            argv,
            stdin=subprocess.PIPE,
            stdout=slave_fd,
            stderr=slave_fd,
            env=env,
            cwd=bt_path,
            start_new_session=True,
        )
        os.close(slave_fd)

        try:
            proc.stdin.write(cmd_input)
            proc.stdin.close()
        except BrokenPipeError:
            pass

        deadline = time.monotonic() + timeout
        while True:
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                proc.kill()
                break
            r, _, _ = select.select([master_fd], [], [], min(remaining, 0.5))
            if r:
                try:
                    data = os.read(master_fd, 8192)
                    if data:
                        output_chunks.append(data.decode("utf-8", errors="replace"))
                except OSError:
                    break
            else:
                if proc.poll() is not None:
                    try:
                        while True:
                            r2, _, _ = select.select([master_fd], [], [], 0.1)
                            if not r2:
                                break
                            data = os.read(master_fd, 8192)
                            if not data:
                                break
                            output_chunks.append(data.decode("utf-8", errors="replace"))
                    except OSError:
                        pass
                    break
        try:
            proc.wait(timeout=3)
        except subprocess.TimeoutExpired:
            proc.kill()
            try:
                proc.wait(timeout=2)
            except subprocess.TimeoutExpired:
                proc.kill(9)
    finally:
        try:
            os.close(master_fd)
        except OSError:
            pass

    output = "".join(output_chunks)
    ansi_escape = re.compile(r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])")
    return ansi_escape.sub("", output).strip()


# ---------------------------------------------------------------------------
# Output parsers (honest detection classification)
# ---------------------------------------------------------------------------


def _parse_ai_test(output: str, command: str, args: str) -> bool:
    """Parse LazyOwnBT ai_test output. Only True if model says 'malicious'."""
    lower = output.lower()
    for line in lower.split('\n'):
        line = line.strip()
        if ('malicioso:' in line or 'malicious:' in line) and 'modelo' not in line and 'model' not in line:
            if 'no' in line and ('❌' in line or line.endswith(' no')):
                return False
            if 'sí' in line or 'si' in line or 'yes' in line:
                return True
    return False


def _parse_keyword_match(output: str, command: str, args: str) -> bool:
    """Check if the command/args appear in the detection output as flagged."""
    if not output.strip():
        return False
    output_lower = output.lower()
    keywords = [command.lower()]
    if args:
        keywords.extend(a.lower() for a in args.split() if len(a) > 2)
    for kw in keywords:
        if kw in output_lower:
            if any(marker in output_lower for marker in [
                "suspicious", "detected", "alert", "malicious",
                "warning", "anomaly", "threat", "ioc", "flagged",
            ]):
                return True
    if "no suspicious" in output_lower or "no threats" in output_lower:
        return False
    if "found" in output_lower and ("suspicious" in output_lower or "alert" in output_lower):
        return True
    return False


def _parse_alert_check(output: str, command: str, args: str) -> bool:
    """Check if log analysis produced alerts related to our action."""
    if not output.strip():
        return False
    output_lower = output.lower()
    has_alert = "alert" in output_lower or "detected" in output_lower
    if not has_alert:
        return False
    keywords = [command.lower()]
    if args:
        keywords.extend(a.lower() for a in args.split() if len(a) > 2)
    return any(kw in output_lower for kw in keywords)


def _parse_fim_check(output: str, command: str, args: str) -> bool:
    """FIM detects only if files were actually modified."""
    lower = output.lower()
    return "modified" in lower or "violation" in lower or "changed" in lower


_PARSERS: dict[str, Any] = {
    "ai_test": _parse_ai_test,
    "keyword_match": _parse_keyword_match,
    "alert_check": _parse_alert_check,
    "fim_check": _parse_fim_check,
}


# ---------------------------------------------------------------------------
# PurpleTeamLoop (L — Liskov-substitutable via IPurpleLoop)
# ---------------------------------------------------------------------------


class PurpleTeamLoop(IPurpleLoop, IPurpleEvaluator):
    """Closed-loop purple team orchestrator.

    Executes red team actions, measures real detection via LazyOwnBT,
    generates CSV datasets for ML training, and calibrates the DetectionOracle.
    """

    def __init__(
        self,
        bt_path: str | None = None,
        detection_delay: int = 5,
        methods: list[str] | None = None,
        auto_feedback: bool = True,
        session_id: str | None = None,
    ) -> None:
        self._bt_path = bt_path or "external/.exploit/LazyOwnBT"
        self._detection_delay = detection_delay
        self._enabled_methods = methods or ["ai_test", "proc_scan", "net_scan", "log_analyze"]
        self._auto_feedback = auto_feedback
        self._session_id = session_id or datetime.now().strftime("%Y%m%d_%H%M%S")
        self._results: list[PurpleResult] = []

        _PURPLE_DIR.mkdir(parents=True, exist_ok=True)

        self._init_dataset()

    def _init_dataset(self) -> None:
        """Create CSV header if dataset file does not exist."""
        if not _DATASET_FILE.exists():
            with open(_DATASET_FILE, "w", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=_DATASET_FIELDS)
                writer.writeheader()
            log.info("PurpleTeamLoop: created dataset at %s", _DATASET_FILE)

    # -- IPurpleLoop --------------------------------------------------------

    def execute_and_measure(
        self, command: str, args: str, category: str,
    ) -> PurpleResult:
        """Execute a red action and measure if LazyOwnBT detects it."""
        from modules.detection_oracle import get_oracle

        oracle = get_oracle()
        assessment = oracle.assess(command, args, category)
        prediction = assessment.probability

        log.info("PurpleTeamLoop: executing '%s %s' (oracle=%.2f)", command, args, prediction)

        red_output = self._execute_red(command, args)
        red_hash = self._hash_output(red_output)

        time.sleep(self._detection_delay)

        detections, raw_outputs = self._query_blue(command, args)
        detected = any(detections.values())

        result = PurpleResult(
            command=command,
            args=args,
            category=category,
            oracle_prediction=prediction,
            actually_detected=detected,
            detection_methods=detections,
            red_output_hash=red_hash,
            session_id=self._session_id,
            detection_raw=raw_outputs,
        )

        self._results.append(result)
        self._write_audit(result)
        self._append_dataset(result)

        if self._auto_feedback:
            self._write_feedback(result)

        log.info(
            "PurpleTeamLoop: '%s' detected=%s (methods=%s)",
            command, detected, detections,
        )
        return result

    def measure_only(
        self, command: str, args: str, category: str,
    ) -> PurpleResult:
        """Measure without executing — test if BT would detect the command."""
        from modules.detection_oracle import get_oracle

        oracle = get_oracle()
        prediction = oracle.probability(command, args, category)

        detections, raw_outputs = self._query_blue(command, args)
        detected = any(detections.values())

        result = PurpleResult(
            command=command,
            args=args,
            category=category,
            oracle_prediction=prediction,
            actually_detected=detected,
            detection_methods=detections,
            red_output_hash="",
            session_id=self._session_id,
            detection_raw=raw_outputs,
        )

        self._results.append(result)
        self._write_audit(result)
        self._append_dataset(result)

        if self._auto_feedback:
            self._write_feedback(result)

        return result

    def engagement_score(self) -> PurpleScore:
        """Aggregate detection score from all results in this session."""
        all_results = self._results or self._load_audit()
        if not all_results:
            return PurpleScore(0, 0, 0, 0.0, {}, {})

        total = len(all_results)
        detected = sum(1 for r in all_results if r.actually_detected)
        missed = total - detected

        by_category: dict[str, dict[str, int]] = {}
        by_method: dict[str, dict[str, int]] = {}

        for r in all_results:
            cat = r.category
            by_category.setdefault(cat, {"total": 0, "detected": 0})
            by_category[cat]["total"] += 1
            if r.actually_detected:
                by_category[cat]["detected"] += 1

            for method, was_detected in r.detection_methods.items():
                by_method.setdefault(method, {"total": 0, "detected": 0})
                by_method[method]["total"] += 1
                if was_detected:
                    by_method[method]["detected"] += 1

        score = PurpleScore(
            total=total,
            detected=detected,
            missed=missed,
            score=detected / total if total > 0 else 0.0,
            by_category=by_category,
            by_method=by_method,
        )

        _SCORE_FILE.write_text(json.dumps(asdict(score), indent=2))
        return score

    def export_dataset(self) -> Path:
        """Return the path to the CSV dataset file."""
        return _DATASET_FILE

    def export_report(self) -> Path:
        """Generate a full engagement report."""
        score = self.engagement_score()
        results = [r.to_dict() for r in self._results]

        oracle_accuracy = self._compute_oracle_accuracy()

        report = {
            "session_id": self._session_id,
            "timestamp": datetime.now().isoformat(),
            "score": asdict(score),
            "oracle_accuracy": oracle_accuracy,
            "total_actions": score.total,
            "detection_rate": f"{score.score:.1%}",
            "results": results,
            "dataset_file": str(_DATASET_FILE),
            "feedback_file": str(_FEEDBACK_FILE),
        }

        _REPORT_FILE.write_text(json.dumps(report, indent=2))
        log.info("PurpleTeamLoop: report exported to %s", _REPORT_FILE)
        return _REPORT_FILE

    # -- IPurpleEvaluator ---------------------------------------------------

    def last_results(self, n: int = 10) -> list[PurpleResult]:
        return self._results[-n:]

    def category_accuracy(self, category: str) -> dict[str, Any]:
        cat_results = [r for r in self._results if r.category == category]
        if not cat_results:
            return {"category": category, "total": 0}
        detected = sum(1 for r in cat_results if r.actually_detected)
        return {
            "category": category,
            "total": len(cat_results),
            "detected": detected,
            "missed": len(cat_results) - detected,
            "detection_rate": f"{detected / len(cat_results):.1%}",
        }

    # -- Internal helpers ---------------------------------------------------

    def _execute_red(self, command: str, args: str) -> str:
        """Execute a red team command via LazyOwn's run_command."""
        try:
            from core.process import run_command
            full_cmd = f"{command} {args}".strip()

            if command == 'lazynmap':
                from core.config import load_payload
                params = load_payload()
                target = params.get('rhost', '127.0.0.1')
                script = os.path.join(os.getcwd(), 'modules', 'lazynmap.sh')
                full_cmd = f'bash {script} -t {target}'

            output = run_command(full_cmd, timeout=120)
            return output if isinstance(output, str) else str(output)
        except Exception as exc:
            log.error("PurpleTeamLoop: red execution failed: %s", exc)
            return f"[error] {exc}"

    def _query_blue(
        self, command: str, args: str,
    ) -> tuple[dict[str, bool], dict[str, str]]:
        """Query each enabled LazyOwnBT detection method."""
        detections: dict[str, bool] = {}
        raw_outputs: dict[str, str] = {}

        available_methods = {m.name: m for m in _DETECTION_METHODS}

        for method_name in self._enabled_methods:
            method = available_methods.get(method_name)
            if method is None:
                log.debug("PurpleTeamLoop: unknown method '%s', skipping", method_name)
                continue

            bt_cmd = method.bt_command.format(command=command, args=args)
            raw = _run_bt_command(self._bt_path, bt_cmd, timeout=30)

            _BT_LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
            with open(_BT_LOG_FILE, "a") as f:
                f.write(f"[{datetime.now().isoformat()}] {method_name}: {bt_cmd}\n")
                f.write(f"  output: {raw[:500]}\n")

            parser = _PARSERS.get(method.output_parser, _parse_keyword_match)
            detected = parser(raw, command, args)

            detections[method_name] = detected
            raw_outputs[method_name] = raw[:2000]

        try:
            bt_path = os.path.abspath(self._bt_path)
            import sys
            sys.path.insert(0, bt_path)
            from lazyownbt.detection import get_engine
            engine = get_engine(os.path.join(bt_path, "lazyown.db"))
            alerts = engine.check_command(command, args)
            if alerts:
                detections["sigma_rules"] = True
                raw_outputs["sigma_rules"] = json.dumps(
                    [{"rule": a.rule_id, "title": a.rule_title, "level": a.level} for a in alerts]
                )
            else:
                detections["sigma_rules"] = False
        except Exception as e:
            log.debug("PurpleTeamLoop: sigma check failed: %s", e)

        return detections, raw_outputs

    def _hash_output(self, output: str) -> str:
        """Hash red output for dataset dedup."""
        import hashlib
        return hashlib.sha256(output.encode()).hexdigest()[:16]

    def _write_audit(self, result: PurpleResult) -> None:
        """Append to JSONL audit log."""
        with open(_AUDIT_FILE, "a") as f:
            f.write(json.dumps(result.to_dict()) + "\n")

    def _append_dataset(self, result: PurpleResult) -> None:
        """Append a row to the CSV dataset for ML training."""
        with open(_DATASET_FILE, "a", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=_DATASET_FIELDS)
            writer.writerow(result.to_csv_row())

    def _write_feedback(self, result: PurpleResult) -> None:
        """Write detection feedback for oracle calibration.

        Format matches detection_feed.py expectations:
            {"rule_id": ..., "detected": bool, "actual": bool}
        """
        oracle_said_detected = result.oracle_prediction >= 0.5
        fb = {
            "rule_id": f"PURPLE-{result.category}",
            "detected": result.actually_detected,
            "actual": oracle_said_detected,
            "prediction": result.oracle_prediction,
            "command": result.command,
            "args": result.args,
            "session_id": self._session_id,
            "timestamp": result.timestamp,
        }
        with open(_FEEDBACK_FILE, "a") as f:
            f.write(json.dumps(fb) + "\n")

    def _load_audit(self) -> list[PurpleResult]:
        """Load results from JSONL audit file."""
        if not _AUDIT_FILE.exists():
            return []
        results = []
        for line in _AUDIT_FILE.read_text().splitlines():
            if not line.strip():
                continue
            try:
                d = json.loads(line)
                results.append(PurpleResult(**{
                    k: d[k] for k in PurpleResult.__dataclass_fields__ if k in d
                }))
            except Exception:
                continue
        return results

    def _compute_oracle_accuracy(self) -> dict[str, Any]:
        """Compute how well oracle predictions match real detections."""
        if not self._results:
            return {"total": 0, "correct": 0, "accuracy": 0.0}

        correct = 0
        for r in self._results:
            oracle_says = r.oracle_prediction >= 0.5
            if oracle_says == r.actually_detected:
                correct += 1

        total = len(self._results)
        return {
            "total": total,
            "correct": correct,
            "accuracy": correct / total if total > 0 else 0.0,
            "underpredicted": sum(
                1 for r in self._results
                if r.actually_detected and r.oracle_prediction < 0.3
            ),
            "overpredicted": sum(
                1 for r in self._results
                if not r.actually_detected and r.oracle_prediction > 0.7
            ),
        }

    def _get_detection_methods(self) -> list[dict[str, str]]:
        """Return available detection methods for display."""
        return [
            {"name": m.name, "description": m.description}
            for m in _DETECTION_METHODS
        ]


# ---------------------------------------------------------------------------
# Factory
# ---------------------------------------------------------------------------


_default_loop: PurpleTeamLoop | None = None


def get_loop(
    bt_path: str | None = None,
    detection_delay: int = 5,
    methods: list[str] | None = None,
    auto_feedback: bool = True,
) -> PurpleTeamLoop:
    """Return (or create) the module-level PurpleTeamLoop singleton."""
    global _default_loop
    if _default_loop is None:
        _default_loop = PurpleTeamLoop(
            bt_path=bt_path,
            detection_delay=detection_delay,
            methods=methods,
            auto_feedback=auto_feedback,
        )
    return _default_loop


def load_config_from_payload(params: dict[str, Any]) -> dict[str, Any]:
    """Extract purple_team config from payload.json params dict.

    Returns a dict with keys: enabled, bt_path, detection_delay,
    methods, auto_feedback, score_threshold.
    """
    pt = params.get("purple_team", {})
    return {
        "enabled": pt.get("enabled", False),
        "bt_path": pt.get("lazyownbt_path", "external/.exploit/LazyOwnBT"),
        "detection_delay": pt.get("detection_delay", 5),
        "methods": pt.get("methods", ["ai_test", "proc_scan", "net_scan", "log_analyze"]),
        "auto_feedback": pt.get("auto_feedback", True),
        "score_threshold": pt.get("score_threshold", 0.7),
    }


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import argparse
    import sys

    parser = argparse.ArgumentParser(
        description="LazyOwn Purple Team — honest detection measurement"
    )
    sub = parser.add_subparsers(dest="action")

    exec_p = sub.add_parser("exec", help="Execute + measure")
    exec_p.add_argument("command", help="Red team command")
    exec_p.add_argument("args", nargs="?", default="", help="Command arguments")
    exec_p.add_argument("--category", default="other", help="Action category")

    measure_p = sub.add_parser("measure", help="Measure only (no execution)")
    measure_p.add_argument("command", help="Command to test")
    measure_p.add_argument("args", nargs="?", default="", help="Command arguments")
    measure_p.add_argument("--category", default="other", help="Action category")

    sub.add_parser("score", help="Show engagement score")
    sub.add_parser("report", help="Generate engagement report")
    sub.add_parser("methods", help="List detection methods")

    cli_args = parser.parse_args()
    loop = get_loop()

    if cli_args.action == "exec":
        result = loop.execute_and_measure(cli_args.command, cli_args.args, cli_args.category)
        print(f"Detected: {result.actually_detected}")
        print(f"Oracle prediction: {result.oracle_prediction:.1%}")
        print(f"Methods: {json.dumps(result.detection_methods, indent=2)}")
    elif cli_args.action == "measure":
        result = loop.measure_only(cli_args.command, cli_args.args, cli_args.category)
        print(f"Detected: {result.actually_detected}")
        print(f"Oracle prediction: {result.oracle_prediction:.1%}")
        print(f"Methods: {json.dumps(result.detection_methods, indent=2)}")
    elif cli_args.action == "score":
        score = loop.engagement_score()
        print(f"Total: {score.total}  Detected: {score.detected}  Missed: {score.missed}")
        print(f"Detection rate: {score.score:.1%}")
        if score.by_category:
            print("\nBy category:")
            for cat, stats in score.by_category.items():
                rate = stats["detected"] / stats["total"] if stats["total"] > 0 else 0
                print(f"  {cat}: {stats['detected']}/{stats['total']} ({rate:.0%})")
        if score.by_method:
            print("\nBy method:")
            for method, stats in score.by_method.items():
                rate = stats["detected"] / stats["total"] if stats["total"] > 0 else 0
                print(f"  {method}: {stats['detected']}/{stats['total']} ({rate:.0%})")
    elif cli_args.action == "report":
        path = loop.export_report()
        print(f"Report exported to: {path}")
    elif cli_args.action == "methods":
        for m in _DETECTION_METHODS:
            print(f"  {m.name:20s} — {m.description}")
    else:
        parser.print_help()
    sys.exit(0)
