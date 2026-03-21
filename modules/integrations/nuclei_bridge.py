#!/usr/bin/env python3
"""
modules/integrations/nuclei_bridge.py
=======================================
Selects and runs Nuclei templates based on discovered services and CVEs
from WorldModel/ObsParser.

Design (SOLID)
--------------
- Single Responsibility : LocalTemplateIndex indexes templates; NucleiRunner executes
- Open/Closed           : new selectors via TemplateSelector subclass
- Liskov                : any TemplateSelector can replace LocalTemplateIndex
- Interface Segregation : NucleiRunner depends on List[NucleiTemplate], not on selectors
- Dependency Inversion  : NucleiBridge depends on TemplateSelector and NucleiRunner abstractions

Usage
-----
    from modules.integrations.nuclei_bridge import get_bridge

    bridge = get_bridge()
    output = bridge.scan("10.10.11.78", findings)

    # List matching templates without running:
    templates = bridge.list_templates(services=["apache"], cves=["CVE-2021-41773"])

    # CLI:
    python3 modules/integrations/nuclei_bridge.py --target 10.10.11.78 --cve CVE-2021-41773
    python3 modules/integrations/nuclei_bridge.py --target 10.10.11.78 --service apache --dry-run
"""
from __future__ import annotations

import argparse
import logging
import os
import re
import shutil
import subprocess
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

log = logging.getLogger("nuclei_bridge")

_BASE_DIR = Path(__file__).parent.parent.parent
_NUCLEI_TEMPLATES_DIR = _BASE_DIR / "external" / ".exploit" / "nuclei-templates"

_SEVERITY_ORDER: Dict[str, int] = {
    "critical": 0,
    "high": 1,
    "medium": 2,
    "low": 3,
    "info": 4,
    "unknown": 5,
}

try:
    import yaml as _yaml
    _YAML_AVAILABLE = True
except ImportError:
    _YAML_AVAILABLE = False


# ---------------------------------------------------------------------------
# Value object
# ---------------------------------------------------------------------------

@dataclass
class NucleiTemplate:
    """Metadata extracted from a Nuclei template YAML file."""
    id: str
    name: str
    severity: str = "info"
    tags: List[str] = field(default_factory=list)
    cve: str = ""
    path: str = ""


# ---------------------------------------------------------------------------
# Abstract selector
# ---------------------------------------------------------------------------

class TemplateSelector(ABC):
    """Interface for selecting Nuclei templates given service/CVE context."""

    @abstractmethod
    def select(self, services: List[str], cves: List[str]) -> List[NucleiTemplate]:
        """
        Return templates relevant to the provided *services* and *cves*.

        Results are sorted: critical > high > medium > low.
        """


# ---------------------------------------------------------------------------
# Local template index
# ---------------------------------------------------------------------------

class LocalTemplateIndex(TemplateSelector):
    """
    Scans the local nuclei-templates directory and builds an in-memory index.

    Template metadata is parsed from YAML files under
    ``external/.exploit/nuclei-templates/``.  Falls back gracefully when the
    directory does not exist or when PyYAML is not installed (uses regex
    parsing instead).
    """

    def __init__(self, templates_dir: str | Path = _NUCLEI_TEMPLATES_DIR) -> None:
        self._dir = Path(templates_dir)
        self._index: List[NucleiTemplate] = []
        self._built = False

    # -- TemplateSelector ------------------------------------------------------

    def select(self, services: List[str], cves: List[str]) -> List[NucleiTemplate]:
        self._ensure_built()

        service_lower = [s.lower() for s in services]
        cve_upper = [c.upper() for c in cves]

        matched: List[NucleiTemplate] = []
        seen: set = set()

        for tmpl in self._index:
            if tmpl.id in seen:
                continue
            if self._matches(tmpl, service_lower, cve_upper):
                matched.append(tmpl)
                seen.add(tmpl.id)

        return sorted(matched, key=lambda t: _SEVERITY_ORDER.get(t.severity.lower(), 5))

    # -- Public helpers --------------------------------------------------------

    def build(self) -> None:
        """Force a (re)build of the template index."""
        self._index = []
        if not self._dir.exists():
            log.warning("Nuclei templates directory not found: %s", self._dir)
            return

        for yaml_path in self._dir.rglob("*.yaml"):
            tmpl = self._parse_template(yaml_path)
            if tmpl:
                self._index.append(tmpl)

        log.info("LocalTemplateIndex: indexed %d templates from %s", len(self._index), self._dir)
        self._built = True

    # -- Internal --------------------------------------------------------------

    def _ensure_built(self) -> None:
        if not self._built:
            self.build()

    def _parse_template(self, path: Path) -> Optional[NucleiTemplate]:
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            return None

        if _YAML_AVAILABLE:
            return self._parse_yaml(text, path)
        return self._parse_regex(text, path)

    def _parse_yaml(self, text: str, path: Path) -> Optional[NucleiTemplate]:
        try:
            data = _yaml.safe_load(text)
        except Exception:
            return self._parse_regex(text, path)

        if not isinstance(data, dict):
            return None

        tmpl_id = str(data.get("id") or "")
        info: dict = data.get("info", {}) or {}
        name = str(info.get("name") or tmpl_id)
        severity = str(info.get("severity") or "info").lower()
        raw_tags = info.get("tags") or ""
        tags = self._normalise_tags(raw_tags)
        cve = self._extract_cve_from_tags(tags) or self._extract_cve_from_text(text)

        if not tmpl_id:
            return None

        return NucleiTemplate(
            id=tmpl_id,
            name=name,
            severity=severity,
            tags=tags,
            cve=cve,
            path=str(path),
        )

    def _parse_regex(self, text: str, path: Path) -> Optional[NucleiTemplate]:
        tmpl_id = ""
        id_match = re.search(r"^id:\s*(.+)$", text, re.MULTILINE)
        if id_match:
            tmpl_id = id_match.group(1).strip()

        name = tmpl_id
        name_match = re.search(r"^\s+name:\s*(.+)$", text, re.MULTILINE)
        if name_match:
            name = name_match.group(1).strip()

        severity = "info"
        sev_match = re.search(r"^\s+severity:\s*(\w+)", text, re.MULTILINE)
        if sev_match:
            severity = sev_match.group(1).strip().lower()

        tags_raw = ""
        tags_match = re.search(r"^\s+tags:\s*(.+)$", text, re.MULTILINE)
        if tags_match:
            tags_raw = tags_match.group(1).strip()
        tags = self._normalise_tags(tags_raw)

        cve = self._extract_cve_from_tags(tags) or self._extract_cve_from_text(text)

        if not tmpl_id:
            return None

        return NucleiTemplate(
            id=tmpl_id,
            name=name,
            severity=severity,
            tags=tags,
            cve=cve,
            path=str(path),
        )

    @staticmethod
    def _normalise_tags(raw: Any) -> List[str]:
        if isinstance(raw, list):
            return [str(t).strip().lower() for t in raw if t]
        if isinstance(raw, str):
            return [t.strip().lower() for t in re.split(r"[,\s]+", raw) if t.strip()]
        return []

    @staticmethod
    def _extract_cve_from_tags(tags: List[str]) -> str:
        for tag in tags:
            if re.match(r"cve-\d{4}-\d+", tag, re.IGNORECASE):
                return tag.upper()
        return ""

    @staticmethod
    def _extract_cve_from_text(text: str) -> str:
        match = re.search(r"CVE-\d{4}-\d+", text, re.IGNORECASE)
        return match.group(0).upper() if match else ""

    @staticmethod
    def _matches(
        tmpl: NucleiTemplate,
        service_lower: List[str],
        cve_upper: List[str],
    ) -> bool:
        if cve_upper and tmpl.cve.upper() in cve_upper:
            return True
        for svc in service_lower:
            if svc in tmpl.id.lower() or svc in tmpl.name.lower():
                return True
            for tag in tmpl.tags:
                if svc in tag:
                    return True
        return False


# ---------------------------------------------------------------------------
# Nuclei runner
# ---------------------------------------------------------------------------

class NucleiRunner:
    """
    Builds and executes nuclei commands via subprocess.

    Falls back gracefully if nuclei is not installed.
    """

    _NUCLEI_TIMEOUT = 300  # seconds

    def __init__(self) -> None:
        self._binary: Optional[str] = shutil.which("nuclei")
        if not self._binary:
            log.warning("nuclei not found in PATH; NucleiRunner will return error strings")

    def run(
        self,
        target: str,
        templates: List[NucleiTemplate],
        output_dir: Optional[str | Path] = None,
    ) -> str:
        """
        Execute nuclei against *target* using the provided *templates*.

        Returns the combined stdout/stderr output, or an error string if
        nuclei is not installed or execution fails.
        """
        if not self._binary:
            return "ERROR: nuclei binary not found in PATH"
        if not templates:
            return "No templates selected; nothing to run."

        cmd = self._build_command(target, templates, output_dir)
        log.info("Running: %s", " ".join(cmd))
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=self._NUCLEI_TIMEOUT,
            )
            output = (result.stdout or "") + (result.stderr or "")
            return output.strip()
        except subprocess.TimeoutExpired:
            return f"ERROR: nuclei timed out after {self._NUCLEI_TIMEOUT}s"
        except (FileNotFoundError, OSError) as exc:
            return f"ERROR: could not execute nuclei: {exc}"

    def run_for_findings(
        self,
        target: str,
        findings: list,
        output_dir: Optional[str | Path] = None,
        selector: Optional[TemplateSelector] = None,
    ) -> str:
        """
        Convenience: extract services/CVEs from *findings*, select templates, run.
        """
        sel = selector or LocalTemplateIndex()
        services, cves = self._extract_context(findings)
        templates = sel.select(services, cves)
        return self.run(target, templates, output_dir)

    # -- Internal --------------------------------------------------------------

    def _build_command(
        self,
        target: str,
        templates: List[NucleiTemplate],
        output_dir: Optional[str | Path],
    ) -> List[str]:
        cmd = [self._binary, "-target", target, "-silent"]

        # Deduplicate template paths
        paths = list(dict.fromkeys(t.path for t in templates if t.path))
        if paths:
            for p in paths:
                cmd.extend(["-t", p])
        else:
            # Fall back to template ids as tags
            ids = list(dict.fromkeys(t.id for t in templates))
            for tid in ids:
                cmd.extend(["-tags", tid])

        if output_dir:
            out = Path(output_dir) / "nuclei_output.txt"
            out.parent.mkdir(parents=True, exist_ok=True)
            cmd.extend(["-output", str(out)])

        return cmd

    @staticmethod
    def _extract_context(findings: list) -> Tuple[List[str], List[str]]:
        services: List[str] = []
        cves: List[str] = []
        for f in findings:
            ftype = str(getattr(f, "type", "")).lower()
            value = str(getattr(f, "value", ""))
            if "cve" in ftype:
                cves.append(value)
            elif "service" in ftype:
                parts = value.split(" ", 1)
                services.append(parts[0])
        return services, cves


# ---------------------------------------------------------------------------
# Top-level facade
# ---------------------------------------------------------------------------

class NucleiBridge:
    """
    Top-level facade combining TemplateSelector and NucleiRunner.

    Injected dependencies allow easy testing without real nuclei.
    """

    def __init__(
        self,
        selector: Optional[TemplateSelector] = None,
        runner: Optional[NucleiRunner] = None,
    ) -> None:
        self._selector: TemplateSelector = selector or LocalTemplateIndex()
        self._runner: NucleiRunner = runner or NucleiRunner()

    def scan(
        self,
        target: str,
        findings: list,
        dry_run: bool = False,
    ) -> str:
        """
        Select templates from *findings* and run nuclei against *target*.

        When *dry_run* is True, return the command string without executing.
        """
        services, cves = NucleiRunner._extract_context(findings)
        templates = self._selector.select(services, cves)

        if not templates:
            return "No matching templates found for the provided findings."

        if dry_run:
            ids = [t.id for t in templates]
            return f"DRY RUN — would run {len(templates)} template(s): {', '.join(ids)}"

        return self._runner.run(target, templates)

    def list_templates(
        self,
        services: Optional[List[str]] = None,
        cves: Optional[List[str]] = None,
    ) -> List[NucleiTemplate]:
        """Return matching templates without running nuclei."""
        return self._selector.select(services or [], cves or [])


# ---------------------------------------------------------------------------
# Module singleton
# ---------------------------------------------------------------------------

_bridge: Optional[NucleiBridge] = None


def get_bridge() -> NucleiBridge:
    """Return the module-level NucleiBridge singleton."""
    global _bridge
    if _bridge is None:
        _bridge = NucleiBridge()
    return _bridge


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------

def _main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    parser = argparse.ArgumentParser(
        description="Select and run Nuclei templates from LazyOwn findings"
    )
    parser.add_argument("--target", metavar="HOST", required=False, help="Scan target")
    parser.add_argument("--cve", metavar="CVE_ID", help="Match templates by CVE id")
    parser.add_argument("--service", metavar="NAME", help="Match templates by service name")
    parser.add_argument("--list", action="store_true", help="List matched templates, do not run")
    parser.add_argument("--dry-run", action="store_true", help="Print command, do not execute")
    args = parser.parse_args()

    bridge = get_bridge()
    services = [args.service] if args.service else []
    cves = [args.cve] if args.cve else []

    if args.list or not args.target:
        templates = bridge.list_templates(services=services, cves=cves)
        if not templates:
            print("No templates matched.")
        for t in templates:
            print(f"[{t.severity.upper():8s}] {t.id}  {t.name}")
            if t.cve:
                print(f"            CVE: {t.cve}")
        return

    # Build synthetic findings from CLI args for convenience
    class _F:
        def __init__(self, ftype: str, value: str) -> None:
            self.type = ftype
            self.value = value
            self.host = ""

    findings = []
    for cve in cves:
        findings.append(_F("cve", cve))
    for svc in services:
        findings.append(_F("service_version", svc))

    if args.dry_run:
        print(bridge.scan(args.target, findings, dry_run=True))
    else:
        print(bridge.scan(args.target, findings))


if __name__ == "__main__":
    _main()
