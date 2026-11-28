"""Deterministic, context-ranked Nuclei sweep for autonomous runs.

The framework ships a Nuclei marketplace and a template index, but the
autonomous loop never used them. This module closes that gap: it reads the
target's observed services and CVEs, ranks the installed templates by the
probability that they actually apply, and runs the bounded winner set with
``nuclei -jsonl``. Findings are published through the outcome bus so the
world model, findings ledger and reports stay consistent.

Design contract:
    - Read-only context: world model, nmap XML, findings ledger and the
      ``ss_cve_context`` artifact are only read.
    - Bounded execution: every run is capped by template count, request
      timeout, rate limit and a hard wall-clock deadline.
    - Non-interactive: no prompts, no template updates, no network calls
      other than the scan itself. Safe for MCP and ``auto_loop``.
    - Injected I/O: template directory, binary name, runner, clock and
      sessions directory are injectable so tests never touch a live scan.
"""

from __future__ import annotations

import json
import re
import shutil
import subprocess
import time
from collections.abc import Callable
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from modules.integrations.nuclei_bridge import LocalTemplateIndex, NucleiTemplate
from modules.nmap_fingerprint import find_nmap_xml, parse_nmap_xml
from modules.outcome_bus import record_event
from modules.world_model import read_state_dict

BASE_DIR = Path(__file__).resolve().parent.parent
SESSIONS_DIR = BASE_DIR / "sessions"
TEMPLATE_DIR = BASE_DIR / "external" / ".exploit" / "nuclei-templates"

NUCLEI_BINARY = "nuclei"
DEFAULT_SEVERITIES = ("critical", "high")
DEFAULT_EXCLUDED_TAGS = frozenset({"dos", "fuzz", "brute-force", "intrusive", "default-login"})
DEFAULT_MAX_TEMPLATES = 40
DEFAULT_MAX_TARGETS = 8
DEFAULT_TIMEOUT_SEC = 900
DEFAULT_REQUEST_TIMEOUT_SEC = 10
DEFAULT_RATE_LIMIT = 150
DEFAULT_RETRIES = 1
DEFAULT_CONFIDENCE = 0.9
OUTPUT_TAIL_CHARS = 4000
SEVERITY_ORDER = {"critical": 0, "high": 1, "medium": 2, "low": 3, "info": 4, "unknown": 5}
SEVERITY_SCORE = {"critical": 40, "high": 25, "medium": 10, "low": 2}
WEB_SERVICE_NAMES = frozenset(
    {
        "http",
        "https",
        "http-proxy",
        "http-alt",
        "ssl/http",
        "https-alt",
        "http-mgmt",
        "http-rpc-epmap",
        "web",
        "webproxy",
    }
)
WEB_PORTS = frozenset({80, 443, 8000, 8008, 8080, 8081, 8082, 8443, 8888, 9000, 9090, 9443})
TLS_PORTS = frozenset({443, 8443, 9443})
CVE_RE = re.compile(r"CVE-\d{4}-\d{4,7}", re.IGNORECASE)
SAFE_HOST_RE = re.compile(r"[^A-Za-z0-9_.-]+")
URL_SCHEME_HTTP = "http"
URL_SCHEME_HTTPS = "https"


@dataclass(frozen=True)
class NucleiContext:
    """Observed target facts used to rank templates."""

    host: str
    services: tuple[dict[str, Any], ...] = ()
    cves: tuple[str, ...] = ()
    web_targets: tuple[str, ...] = ()

    def service_tokens(self) -> tuple[str, ...]:
        """Return lowercase service/product tokens for template matching."""
        tokens: set[str] = set()
        for service in self.services:
            for key in ("name", "product"):
                value = str(service.get(key, "") or "").strip().lower()
                if value:
                    tokens.add(value)
                    tokens.update(part for part in re.split(r"[^a-z0-9]+", value) if len(part) >= 3)
        return tuple(sorted(tokens))


@dataclass(frozen=True)
class SelectedTemplate:
    """One template with its certainty score and the reasons behind it."""

    template: NucleiTemplate
    score: int
    reasons: tuple[str, ...] = ()


@dataclass
class AutoNucleiResult:
    """Outcome of one auto_nuclei run."""

    target: str
    context: NucleiContext
    templates: list[SelectedTemplate] = field(default_factory=list)
    findings: list[dict[str, Any]] = field(default_factory=list)
    command: list[str] = field(default_factory=list)
    stdout: str = ""
    stderr: str = ""
    error: str = ""
    duration_sec: float = 0.0
    artifact: str = ""
    dry_run: bool = False

    def summary(self) -> dict[str, Any]:
        """Return a JSON-serializable summary for CLI and MCP surfaces."""
        by_severity: dict[str, int] = {}
        for finding in self.findings:
            severity = str(finding.get("severity", "info") or "info").lower()
            by_severity[severity] = by_severity.get(severity, 0) + 1
        return {
            "target": self.target,
            "error": self.error,
            "dry_run": self.dry_run,
            "templates": [
                {
                    "id": item.template.id,
                    "name": item.template.name,
                    "severity": item.template.severity,
                    "cve": item.template.cve,
                    "score": item.score,
                    "reasons": list(item.reasons),
                    "path": item.template.path,
                }
                for item in self.templates
            ],
            "template_count": len(self.templates),
            "findings": self.findings,
            "finding_count": len(self.findings),
            "findings_by_severity": by_severity,
            "command": self.command,
            "duration_sec": round(self.duration_sec, 3),
            "artifact": self.artifact,
            "context": {
                "host": self.context.host,
                "services": list(self.context.services),
                "cves": list(self.context.cves),
                "web_targets": list(self.context.web_targets),
            },
        }


Runner = Callable[[list[str], float], subprocess.CompletedProcess[str]]


class AutoNucleiEngine:
    """Rank installed Nuclei templates against a target and run the best ones."""

    def __init__(
        self,
        *,
        template_dir: str | Path | None = None,
        sessions_dir: str | Path | None = None,
        binary: str = NUCLEI_BINARY,
        runner: Runner | None = None,
        clock: Callable[[], float] | None = None,
    ) -> None:
        """Bind injectable collaborators.

        Args:
            template_dir: Installed nuclei-templates directory.
            sessions_dir: Campaign sessions directory for context and artifacts.
            binary: Nuclei executable name or absolute path.
            runner: Callable executing the argv with a timeout. Defaults to
                :func:`subprocess.run` in text mode.
            clock: Monotonic clock used for duration reporting.
        """
        self.template_dir = Path(template_dir) if template_dir else TEMPLATE_DIR
        self.sessions_dir = Path(sessions_dir) if sessions_dir else SESSIONS_DIR
        self.binary = binary
        self._runner = runner
        self._clock = clock or time.monotonic
        self._index: LocalTemplateIndex | None = None

    def available(self) -> bool:
        """Return True when the nuclei binary can be executed."""
        if self._runner is not None:
            return True
        return bool(shutil.which(self.binary) or Path(self.binary).is_file())

    def templates_ready(self) -> bool:
        """Return True when the local template directory exists."""
        return self.template_dir.is_dir()

    def _template_index(self) -> LocalTemplateIndex:
        if self._index is None:
            self._index = LocalTemplateIndex(self.template_dir)
        return self._index

    def build_context(self, target: str) -> NucleiContext:
        """Collect services, CVEs and web targets for one host.

        Args:
            target: IP address or hostname.

        Returns:
            Context with deduplicated services, CVE ids and web URLs.
        """
        services: dict[int, dict[str, Any]] = {}
        for service in self._world_model_services(target):
            port = int(service.get("port", 0) or 0)
            if port:
                services[port] = service
        for service in self._nmap_services(target):
            port = int(service.port or 0)
            if port:
                services[port] = {
                    "port": port,
                    "name": service.name,
                    "product": service.product,
                    "version": service.version,
                    "protocol": service.protocol,
                }
        ordered = tuple(services[port] for port in sorted(services))
        cves = tuple(sorted(self._collect_cves(target)))
        web_targets = self._web_targets(target, ordered)
        return NucleiContext(host=target, services=ordered, cves=cves, web_targets=web_targets)

    def _world_model_services(self, target: str) -> list[dict[str, Any]]:
        state = read_state_dict(self.sessions_dir / "world_model.json")
        entry = (state.get("hosts") or {}).get(target) or {}
        rows: list[dict[str, Any]] = []
        for port, service in (entry.get("services") or {}).items():
            if not isinstance(service, dict):
                continue
            rows.append(
                {
                    "port": int(service.get("port", port) or port),
                    "name": str(service.get("name", "") or ""),
                    "product": str(service.get("product", "") or ""),
                    "version": str(service.get("version", "") or ""),
                    "protocol": str(service.get("protocol", "tcp") or "tcp"),
                }
            )
        return rows

    def _nmap_services(self, target: str) -> list[Any]:
        files = find_nmap_xml(target, sessions_dir=str(self.sessions_dir))
        if not files:
            return []
        try:
            return parse_nmap_xml(files[0])
        except Exception:
            return []

    def _collect_cves(self, target: str) -> set[str]:
        found: set[str] = set()
        context_path = self.sessions_dir / f"ss_cve_context_{target}.json"
        try:
            payload = json.loads(context_path.read_text(encoding="utf-8"))
            for service in payload.get("services") or []:
                for hit in service.get("cves") or []:
                    cve = str(hit.get("cve", "") or "").upper()
                    if CVE_RE.fullmatch(cve):
                        found.add(cve)
        except (OSError, ValueError):
            pass
        for name in (f"scan_{target}.nmap", f"vulns_{target}.txt", f"nse_{target}.txt"):
            path = self.sessions_dir / name
            try:
                found.update(match.upper() for match in CVE_RE.findall(path.read_text(errors="replace")))
            except OSError:
                continue
        findings_path = self.sessions_dir / "findings" / f"{target}.jsonl"
        try:
            for line in findings_path.read_text(encoding="utf-8", errors="replace").splitlines():
                try:
                    row = json.loads(line)
                except ValueError:
                    continue
                cve = str(row.get("cve", "") or "").upper()
                if CVE_RE.fullmatch(cve):
                    found.add(cve)
                found.update(match.upper() for match in CVE_RE.findall(str(row.get("title", "") or "")))
        except OSError:
            pass
        return found

    @staticmethod
    def _web_targets(target: str, services: tuple[dict[str, Any], ...]) -> tuple[str, ...]:
        targets: list[str] = []
        for service in services:
            name = str(service.get("name", "") or "").lower()
            port = int(service.get("port", 0) or 0)
            if name not in WEB_SERVICE_NAMES and port not in WEB_PORTS:
                continue
            scheme = URL_SCHEME_HTTPS if port in TLS_PORTS or "https" in name or "ssl" in name else URL_SCHEME_HTTP
            url = f"{scheme}://{target}:{port}" if port not in (80, 443) else f"{scheme}://{target}"
            if url not in targets:
                targets.append(url)
        if not targets:
            targets.extend([f"{URL_SCHEME_HTTP}://{target}", f"{URL_SCHEME_HTTPS}://{target}"])
        return tuple(targets[:DEFAULT_MAX_TARGETS])

    def select_templates(
        self,
        context: NucleiContext,
        *,
        severities: tuple[str, ...] = DEFAULT_SEVERITIES,
        exclude_tags: frozenset[str] = DEFAULT_EXCLUDED_TAGS,
        allow_generic: bool = False,
        max_templates: int = DEFAULT_MAX_TEMPLATES,
    ) -> list[SelectedTemplate]:
        """Rank installed templates by likelihood of applying to the target.

        Args:
            context: Observed services, CVEs and web targets.
            severities: Accepted severities, highest first.
            exclude_tags: Template tags that are never run unattended.
            allow_generic: When True, uncontextualised CVE templates are
                eligible; when False only service/CVE-matched templates run.
            max_templates: Hard cap on the returned set.

        Returns:
            Selected templates sorted by descending score.
        """
        allowed = tuple(severity.lower() for severity in severities)
        services = context.service_tokens()
        cves = {cve.upper() for cve in context.cves}
        selected: list[SelectedTemplate] = []
        for template in self._template_index().all_templates():
            severity = str(template.severity or "info").lower()
            if severity not in allowed:
                continue
            tags = {tag.lower() for tag in template.tags}
            if tags & exclude_tags:
                continue
            score, reasons = self._score_template(template, services, cves, severity, allow_generic)
            if score <= 0:
                continue
            selected.append(SelectedTemplate(template=template, score=score, reasons=tuple(reasons)))
        selected.sort(
            key=lambda item: (
                -item.score,
                SEVERITY_ORDER.get(str(item.template.severity).lower(), 5),
                item.template.id,
            )
        )
        return selected[: max(1, int(max_templates))]

    @staticmethod
    def _score_template(
        template: NucleiTemplate,
        services: tuple[str, ...],
        cves: set[str],
        severity: str,
        allow_generic: bool,
    ) -> tuple[int, list[str]]:
        reasons: list[str] = []
        score = SEVERITY_SCORE.get(severity, 0)
        template_id = str(template.id or "").lower()
        template_name = str(template.name or "").lower()
        tags = {tag.lower() for tag in template.tags}
        cve = str(template.cve or "").upper()
        cve_match = bool(cve and cve in cves)
        if cve_match:
            score += 100
            reasons.append(f"cve:{cve}")
        elif cve:
            score += 10
            reasons.append("cve-template")
        service_match = False
        for token in services:
            if token and (token in template_id or token in template_name or token in tags):
                service_match = True
                reasons.append(f"service:{token}")
                break
        if service_match:
            score += 50
        if "cve" in tags:
            score += 5
            reasons.append("tag:cve")
        if not (cve_match or service_match or (allow_generic and cve)):
            return 0, []
        return score, reasons

    def build_command(
        self,
        context: NucleiContext,
        templates: list[SelectedTemplate],
        *,
        request_timeout: int = DEFAULT_REQUEST_TIMEOUT_SEC,
        rate_limit: int = DEFAULT_RATE_LIMIT,
        retries: int = DEFAULT_RETRIES,
        no_interactsh: bool = True,
    ) -> list[str]:
        """Build the bounded nuclei argv for the selected templates."""
        command = [
            self.binary,
            "-jsonl",
            "-silent",
            "-no-color",
            "-disable-update-check",
            "-timeout",
            str(max(1, int(request_timeout))),
            "-retries",
            str(max(0, int(retries))),
            "-rate-limit",
            str(max(1, int(rate_limit))),
        ]
        if no_interactsh:
            command.append("-no-interactsh")
        for item in templates:
            if item.template.path:
                command.extend(["-t", item.template.path])
        for url in context.web_targets:
            command.extend(["-u", url])
        return command

    def run(
        self,
        target: str,
        *,
        severities: tuple[str, ...] = DEFAULT_SEVERITIES,
        exclude_tags: frozenset[str] = DEFAULT_EXCLUDED_TAGS,
        allow_generic: bool = False,
        max_templates: int = DEFAULT_MAX_TEMPLATES,
        timeout_sec: int = DEFAULT_TIMEOUT_SEC,
        request_timeout: int = DEFAULT_REQUEST_TIMEOUT_SEC,
        rate_limit: int = DEFAULT_RATE_LIMIT,
        no_interactsh: bool = True,
        dry_run: bool = False,
    ) -> AutoNucleiResult:
        """Rank templates and execute the bounded nuclei sweep.

        Args:
            target: IP address or hostname to scan.
            severities: Accepted severities.
            exclude_tags: Tags excluded from unattended execution.
            allow_generic: Allow CVE templates without a service/CVE match.
            max_templates: Maximum templates passed to nuclei.
            timeout_sec: Hard wall-clock deadline for the nuclei process.
            request_timeout: Per-request nuclei timeout.
            rate_limit: Nuclei requests per second.
            no_interactsh: Disable out-of-band interactsh callbacks.
            dry_run: Only build the command and return the ranked templates.

        Returns:
            Result with selected templates, parsed findings and artifact path.
        """
        started = self._clock()
        context = self.build_context(target)
        result = AutoNucleiResult(target=target, context=context, dry_run=dry_run)
        if not self.available():
            result.error = (
                "nuclei binary not found; install it with: "
                "go install -v github.com/projectdiscovery/nuclei/v3/cmd/nuclei@latest"
            )
            result.duration_sec = self._clock() - started
            return result
        if not self.templates_ready():
            result.error = (
                f"nuclei templates not found in {self.template_dir}; "
                "run: download_nuclei_templates (or nuclei_marketplace install)"
            )
            result.duration_sec = self._clock() - started
            return result
        result.templates = self.select_templates(
            context,
            severities=severities,
            exclude_tags=exclude_tags,
            allow_generic=allow_generic,
            max_templates=max_templates,
        )
        if not result.templates:
            result.error = (
                "no high-certainty templates matched the observed services or CVEs; "
                "run download_nuclei_templates, scan the target first, or pass --allow-generic"
            )
            result.duration_sec = self._clock() - started
            return result
        result.command = self.build_command(
            context,
            result.templates,
            request_timeout=request_timeout,
            rate_limit=rate_limit,
            no_interactsh=no_interactsh,
        )
        if dry_run:
            result.duration_sec = self._clock() - started
            return result
        try:
            completed = self._execute(result.command, float(timeout_sec))
        except subprocess.TimeoutExpired:
            result.error = f"nuclei exceeded the {timeout_sec}s wall-clock deadline"
            result.duration_sec = self._clock() - started
            result.artifact = str(self._write_artifacts(result))
            return result
        except OSError as exc:
            result.error = f"could not execute nuclei: {exc}"
            result.duration_sec = self._clock() - started
            return result
        result.stdout = completed.stdout or ""
        result.stderr = completed.stderr or ""
        result.findings = self._parse_output(result.stdout)
        result.artifact = str(self._write_artifacts(result))
        self._record_findings(result)
        if completed.returncode not in (0, None) and not result.findings:
            result.error = f"nuclei exited with status {completed.returncode}: {result.stderr.strip()[:300]}"
        result.duration_sec = self._clock() - started
        return result

    def _execute(self, command: list[str], timeout: float) -> subprocess.CompletedProcess[str]:
        if self._runner is not None:
            return self._runner(command, timeout)
        return subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )

    @staticmethod
    def _parse_output(stdout: str) -> list[dict[str, Any]]:
        findings: list[dict[str, Any]] = []
        for line in str(stdout or "").splitlines():
            line = line.strip()
            if not line or not line.startswith("{"):
                continue
            try:
                payload = json.loads(line)
            except ValueError:
                continue
            if not isinstance(payload, dict):
                continue
            info = payload.get("info") or {}
            classification = info.get("classification") or {}
            cve_ids = classification.get("cve-id") or []
            if isinstance(cve_ids, str):
                cve_ids = [cve_ids]
            cve = next((str(value).upper() for value in cve_ids if CVE_RE.fullmatch(str(value))), "")
            tags = info.get("tags") or []
            if isinstance(tags, str):
                tags = [part.strip() for part in tags.split(",") if part.strip()]
            findings.append(
                {
                    "template_id": str(payload.get("template-id", "") or ""),
                    "name": str(info.get("name", "") or payload.get("template-id", "") or ""),
                    "severity": str(info.get("severity", "info") or "info").lower(),
                    "cve": cve,
                    "tags": [str(tag) for tag in tags],
                    "matched_at": str(payload.get("matched-at", "") or payload.get("host", "") or ""),
                    "host": str(payload.get("host", "") or ""),
                    "matcher": str(payload.get("matcher-name", "") or ""),
                    "extracted": payload.get("extracted-results") or [],
                    "raw": payload,
                }
            )
        return findings

    def _record_findings(self, result: AutoNucleiResult) -> None:
        command = " ".join(result.command)
        for finding in result.findings:
            try:
                record_event(
                    kind="finding",
                    target=result.target,
                    host=finding.get("host") or result.target,
                    title=f"{finding.get('name')} ({finding.get('template_id')})",
                    description=f"nuclei template {finding.get('template_id')} matched at {finding.get('matched_at')}",
                    severity=str(finding.get("severity", "info") or "info"),
                    cve=str(finding.get("cve", "") or ""),
                    success=True,
                    confidence=DEFAULT_CONFIDENCE,
                    source="auto_nuclei",
                    command=command,
                    output=json.dumps(finding.get("raw", {}), default=str)[:OUTPUT_TAIL_CHARS],
                    metadata={
                        "template_id": finding.get("template_id", ""),
                        "matched_at": finding.get("matched_at", ""),
                        "tags": finding.get("tags", []),
                    },
                )
            except Exception:
                continue

    def _write_artifacts(self, result: AutoNucleiResult) -> Path:
        self.sessions_dir.mkdir(parents=True, exist_ok=True)
        safe_host = SAFE_HOST_RE.sub("_", result.target) or "target"
        raw_path = self.sessions_dir / f"nuclei_auto_{safe_host}_output.txt"
        summary_path = self.sessions_dir / f"auto_nuclei_{safe_host}.json"
        try:
            raw_path.write_text(result.stdout or "", encoding="utf-8")
        except OSError:
            pass
        try:
            summary_path.write_text(json.dumps(result.summary(), indent=2, default=str), encoding="utf-8")
        except OSError:
            pass
        return summary_path


__all__ = [
    "AutoNucleiEngine",
    "AutoNucleiResult",
    "NucleiContext",
    "SelectedTemplate",
]
