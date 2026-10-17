"""Single execution contract for Atomic emulation.

Resolves MITRE techniques or an APT playbook to concrete Atomic tests,
runs each rendered command through one execution primitive, normalizes
the result and publishes one outcome per test. The CLI, MCP, APT chains
and the loop consume this contract instead of reimplementing the loop.
"""

from __future__ import annotations

import json
import logging
import time
from collections.abc import Callable
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

log = logging.getLogger("emulation_runner")

BASE_DIR = Path(__file__).resolve().parent.parent
DEFAULT_SESSIONS = BASE_DIR / "sessions"
MAX_OUTPUT_CHARS = 2000
MAX_COMMAND_CHARS = 1000


@dataclass
class EmulationStep:
    """One already-resolved command to execute."""

    technique_id: str = ""
    name: str = ""
    command: str = ""
    description: str = ""
    manual: bool = False
    guid: str = ""


@dataclass
class EmulationResult:
    """Normalized result of one emulation test."""

    technique: str = ""
    guid: str = ""
    name: str = ""
    command: str = ""
    output: str = ""
    shell_output: bool = False
    status: str = "pending"
    note: str = ""
    duration_ms: float = 0.0

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-serializable view."""
        return {
            "technique": self.technique,
            "guid": self.guid,
            "name": self.name,
            "command": self.command,
            "output": self.output,
            "shell_output": self.shell_output,
            "status": self.status,
            "note": self.note,
            "duration_ms": round(self.duration_ms, 2),
        }


@dataclass
class EmulationReport:
    """Report for one emulation run."""

    target: str = ""
    platform: str = "linux"
    via: str = ""
    results: list[EmulationResult] = field(default_factory=list)
    dry_run: bool = False
    generated_at: str = ""
    staged: str = ""

    @property
    def executed(self) -> int:
        """Return the number of tests that actually ran."""
        return sum(1 for row in self.results if row.status in ("executed", "dry-run"))

    @property
    def shell(self) -> bool:
        """Return True when any test produced a shell signal."""
        return any(row.shell_output for row in self.results)

    def to_dict(self) -> dict[str, Any]:
        """Return the legacy bridge-shaped mapping plus v2 fields."""
        return {
            "target": self.target,
            "via": self.via,
            "platform": self.platform,
            "results": [row.to_dict() for row in self.results],
            "executed": self.executed,
            "shell": self.shell,
            "dry_run": self.dry_run,
            "generated_at": self.generated_at,
            "staged": self.staged,
        }


class EmulationRunner:
    """Resolve and execute Atomic tests through one primitive."""

    def __init__(
        self,
        resolver: Any = None,
        sessions_dir: Path | str | None = None,
        shell_opener: Callable[..., Any] | None = None,
        remote_exec_fn: Callable[..., str] | None = None,
        playbook_loader: Callable[[str], Any] | None = None,
        outcome_recorder: Callable[..., Any] | None = None,
        shell_detector: Callable[..., bool] | None = None,
    ) -> None:
        """Bind optional collaborators; defaults load the shared modules lazily."""
        self._resolver = resolver
        self.sessions_dir = Path(sessions_dir or DEFAULT_SESSIONS)
        self._shell_opener = shell_opener
        self._remote_exec = remote_exec_fn
        self._playbook_loader = playbook_loader
        self._outcome_recorder = outcome_recorder
        self._shell_detector = shell_detector

    def _resolver_obj(self):
        """Return the Atomic resolver."""
        if self._resolver is not None:
            return self._resolver
        from modules.atomic_resolver import get_resolver

        return get_resolver()

    def _playbook(self, name: str):
        """Load one APT playbook."""
        if self._playbook_loader is not None:
            return self._playbook_loader(name)
        from modules.apt_playbooks import AptPlaybookEngine

        return AptPlaybookEngine(playbook_dir=str(BASE_DIR / "playbooks")).get(name)

    def _open_shell(self, target: str, services: list[dict], lhost: str, exploits_dir: Path | str | None):
        """Open the best available shell primitive."""
        if self._shell_opener is not None:
            return self._shell_opener(target, services=services, lhost=lhost)
        from modules.atomic_exploit_bridge import open_shell

        return open_shell(target, services=services, lhost=lhost, exploits_dir=exploits_dir)

    def _exec(self, spec: Any, target: str, command: str, lhost: str) -> str:
        """Run one command through the selected primitive."""
        if self._remote_exec is not None:
            return str(self._remote_exec(spec, target, command, lhost=lhost))
        from modules.atomic_exploit_bridge import remote_exec

        return remote_exec(spec, target, command, lhost=lhost)

    def _detect(self, spec: Any, output: str) -> bool:
        """Detect a shell signal in command output."""
        if self._shell_detector is not None:
            return bool(self._shell_detector(spec, output))
        if spec is None:
            markers = ("uid=", "root@", "meterpreter >", "sh-", "nt authority\\system")
            return any(marker in (output or "").lower() for marker in markers)
        from modules.atomic_exploit_bridge import detect_shell

        return bool(detect_shell(spec, output))

    def _record(self, **kwargs: Any) -> None:
        """Publish one outcome, never raising."""
        try:
            if self._outcome_recorder is not None:
                self._outcome_recorder(**kwargs)
                return
            from modules.outcome_bus import record_event

            record_event(**kwargs)
        except Exception as exc:
            log.debug("emulation outcome skipped: %s", exc)

    def techniques_for_playbook(self, playbook: str, platform: str = "") -> list[str]:
        """Return ordered unique technique IDs for one APT playbook.

        Args:
            playbook: APT playbook key.
            platform: Optional platform filter kept for parity.

        Returns:
            Technique IDs in phase order.
        """
        book = self._playbook(playbook)
        if book is None:
            raise ValueError(f"Unknown playbook: {playbook}")
        seen: list[str] = []
        for phase in getattr(book, "phases", []) or []:
            technique = str(getattr(phase, "technique_id", "") or "").strip().upper()
            if technique and technique not in seen:
                seen.append(technique)
        return seen

    def run(
        self,
        target: str,
        techniques: list[str] | None = None,
        playbook: str = "",
        platform: str = "linux",
        lhost: str = "127.0.0.1",
        per_technique: int = 1,
        include_manual: bool = False,
        dry_run: bool = False,
        executor: Callable[[str], str] | None = None,
        exploits_dir: Path | str | None = None,
        scan_dir: Path | str | None = None,
    ) -> dict[str, Any]:
        """Execute emulation tests and return the staged report.

        Args:
            target: Victim address.
            techniques: Optional technique IDs; playbook supplies them when empty.
            playbook: APT playbook key.
            platform: Atomic platform filter.
            lhost: Attacker address for shell primitives.
            per_technique: Tests to run per technique (1-3).
            include_manual: Execute tests whose executor is manual.
            dry_run: Resolve commands without executing them.
            executor: Optional command executor; replaces the shell primitive.
            exploits_dir: Exploit catalogue directory for the shell opener.
            scan_dir: Sessions directory override.

        Returns:
            Report mapping with normalized results and staged path.

        Raises:
            ValueError: No techniques or unknown playbook.
            RuntimeError: No working shell primitive and no executor.
        """
        sessions = Path(scan_dir or self.sessions_dir)
        if playbook:
            techniques = self.techniques_for_playbook(playbook, platform=platform)
        ordered = [str(item).strip().upper() for item in (techniques or []) if str(item).strip()]
        ordered = list(dict.fromkeys(ordered))
        if not ordered:
            raise ValueError("No techniques to emulate (pass techniques or a playbook).")

        services: list[dict] = []
        scan_path = sessions / f"scan_{target}.nmap.xml"
        try:
            from modules.atomic_exploit_bridge import parse_scan_xml

            rows = parse_scan_xml(scan_path) if scan_path.exists() else []
            services = [
                {
                    "name": row.get("service", ""),
                    "product": row.get("product", ""),
                    "version": row.get("version", ""),
                    "port": row.get("port", ""),
                }
                for row in rows
            ]
        except Exception:
            services = []

        spec = None
        if not dry_run and executor is None:
            spec = self._open_shell(target, services, lhost, exploits_dir)
            if spec is None:
                raise RuntimeError(f"No working shell primitive for {target} (tried exec-capable exploits).")

        report = EmulationReport(
            target=target,
            platform=platform,
            via=str(getattr(spec, "id", "") or ("executor" if executor else "")),
            dry_run=bool(dry_run),
            generated_at=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        )
        resolver = self._resolver_obj()
        try:
            for technique in ordered:
                try:
                    tests = resolver.list_for_technique(technique, platform=platform)[: max(1, min(3, per_technique))]
                except Exception as exc:
                    report.results.append(
                        EmulationResult(
                            technique=technique,
                            status="skipped",
                            note=f"resolver error: {str(exc)[:200]}",
                        )
                    )
                    continue
                if not tests:
                    report.results.append(
                        EmulationResult(technique=technique, status="skipped", note="no test indexed")
                    )
                    continue
                for test in tests:
                    result = self._run_test(
                        test,
                        technique,
                        target,
                        spec,
                        lhost,
                        executor,
                        dry_run,
                        include_manual,
                        report,
                        sessions=sessions,
                    )
                    report.results.append(result)
        finally:
            if spec is not None and executor is None:
                try:
                    from modules.atomic_exploit_bridge import close_sessions

                    close_sessions(target)
                except Exception:
                    pass
        report.staged = self._stage(report, sessions)
        return report.to_dict()

    def run_steps(
        self,
        steps: list[EmulationStep],
        target: str,
        executor: Callable[[str], str],
        platform: str = "linux",
        dry_run: bool = False,
        source: str = "emulation_runner",
    ) -> EmulationReport:
        """Execute already-resolved steps through one executor.

        Args:
            steps: Resolved commands.
            target: Victim address.
            executor: Callable(command) -> output.
            platform: Platform label for the report.
            dry_run: Resolve without executing.
            source: Event source tag.

        Returns:
            Emulation report.
        """
        report = EmulationReport(
            target=target,
            platform=platform,
            via="executor",
            dry_run=bool(dry_run),
            generated_at=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        )
        for step in steps:
            if step.manual:
                report.results.append(
                    EmulationResult(
                        technique=step.technique_id,
                        guid=step.guid,
                        name=step.name,
                        command=step.command,
                        status="skipped",
                        note="manual",
                    )
                )
                continue
            started = time.time()
            if dry_run:
                result = EmulationResult(
                    technique=step.technique_id,
                    guid=step.guid,
                    name=step.name,
                    command=step.command,
                    status="dry-run",
                )
            else:
                try:
                    output = str(executor(step.command) or "")
                    result = EmulationResult(
                        technique=step.technique_id,
                        guid=step.guid,
                        name=step.name,
                        command=step.command,
                        output=output[:MAX_OUTPUT_CHARS],
                        shell_output=self._detect(None, output),
                        status="executed",
                    )
                except Exception as exc:
                    result = EmulationResult(
                        technique=step.technique_id,
                        guid=step.guid,
                        name=step.name,
                        command=step.command,
                        status="error",
                        note=str(exc)[:300],
                    )
            result.duration_ms = (time.time() - started) * 1000
            report.results.append(result)
            if not report.dry_run:
                self._publish(result, target, source, report.dry_run)
        return report

    def _run_test(
        self,
        test: Any,
        technique: str,
        target: str,
        spec: Any,
        lhost: str,
        executor: Callable[[str], str] | None,
        dry_run: bool,
        include_manual: bool,
        report: EmulationReport,
        sessions: Path | None = None,
    ) -> EmulationResult:
        """Execute one Atomic test and publish its outcome."""
        from modules.atomic_resolver import build_variables, render_command

        manual = str(getattr(test, "executor_name", "") or "").lower() == "manual"
        command = render_command(
            str(getattr(test, "command", "") or ""),
            build_variables(test, rhost=target),
        )
        result = EmulationResult(
            technique=technique,
            guid=str(getattr(test, "guid", "") or ""),
            name=str(getattr(test, "name", "") or ""),
            command=command[:MAX_COMMAND_CHARS],
        )
        if manual and not include_manual:
            result.status = "skipped"
            result.note = "manual"
            return result
        if not command.strip():
            result.status = "skipped"
            result.note = "empty command"
            return result
        if dry_run:
            result.status = "dry-run"
            return result
        started = time.time()
        try:
            output = executor(command) if executor is not None else self._exec(spec, target, command, lhost)
            result.output = str(output or "")[:MAX_OUTPUT_CHARS]
            result.shell_output = self._detect(spec, result.output)
            result.status = "executed"
        except Exception as exc:
            result.status = "error"
            result.note = str(exc)[:300]
        result.duration_ms = (time.time() - started) * 1000
        self._publish(result, target, "emulation_runner", dry_run, sessions=sessions)
        return result

    def _publish(
        self,
        result: EmulationResult,
        target: str,
        source: str,
        dry_run: bool,
        sessions: Path | None = None,
    ) -> None:
        """Publish one normalized result to the outcome bus."""
        if dry_run:
            return
        self._record(
            kind="emulation",
            target=target,
            host=target,
            title=result.name or result.technique,
            description=f"{result.technique} {result.status}",
            severity="high" if result.shell_output else "medium",
            mitre_id=result.technique,
            success=result.status == "executed" and not result.note,
            shell=result.shell_output,
            source=source,
            command=result.command,
            output=result.output,
            artifacts=[],
            metadata={
                "sessions_dir": str(sessions or self.sessions_dir),
                "guid": result.guid,
                "status": result.status,
            },
        )

    def _stage(self, report: EmulationReport, sessions: Path) -> str:
        """Write the report JSON under the sessions directory."""
        try:
            sessions.mkdir(parents=True, exist_ok=True)
            stamp = time.strftime("%Y%m%d_%H%M%S", time.gmtime())
            target = Path(sessions) / f"atomic_emulate_{report.target}_{stamp}.json"
            target.write_text(json.dumps(report.to_dict(), indent=2, ensure_ascii=False), encoding="utf-8")
            return str(target)
        except Exception:
            return ""


__all__ = ["EmulationReport", "EmulationResult", "EmulationRunner", "EmulationStep"]
