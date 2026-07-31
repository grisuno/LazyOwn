"""Playbook Executor — bridges MITRE ATT&CK playbooks to the pipeline engine.

Reads YAML playbooks from ``playbooks/``, maps atomic test procedures to
LazyOwn shell commands, and either executes them through the pipeline engine
or generates a runnable pipeline spec for manual review.

Architecture:
    PlaybookLoader   — parses and validates playbook YAML.
    TTPMapper         — resolves technique_id + atomic_test to LazyOwn commands.
    PlaybookEngine    — orchestrates execution via PipelineEngine or dry-run.
"""

from __future__ import annotations

import json
import os
import re
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml

_LAZYOWN_DIR = Path(os.environ.get("LAZYOWN_DIR", str(Path(__file__).resolve().parent.parent)))
PLAYBOOKS_DIR = _LAZYOWN_DIR / "playbooks"
PIPELINES_DIR = _LAZYOWN_DIR / "pipelines"


# ─────────────────────────────────────────────────────────────────────────────
# Value objects
# ─────────────────────────────────────────────────────────────────────────────


@dataclass
class PlaybookTechnique:
    """One technique (sub)phase within a playbook."""

    name: str
    technique_id: str
    technique_name: str
    description: str
    atomic_tests: list[dict[str, Any]] = field(default_factory=list)
    detection_hints: list[str] = field(default_factory=list)


@dataclass
class PlaybookSpec:
    """A loaded, validated playbook document."""

    apt_name: str
    aliases: list[str]
    description: str
    platforms: list[str]
    phases: list[PlaybookTechnique]
    source_urls: list[str] = field(default_factory=list)
    source_path: str = ""


@dataclass
class PlaybookRunResult:
    """Summary of one playbook execution."""

    playbook_name: str
    apt_name: str
    total_techniques: int
    executed_techniques: int
    manual_skipped: int
    automated_passed: int
    automated_failed: int
    pipeline_run_id: str = ""
    errors: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "playbook_name": self.playbook_name,
            "apt_name": self.apt_name,
            "total_techniques": self.total_techniques,
            "executed_techniques": self.executed_techniques,
            "manual_skipped": self.manual_skipped,
            "automated_passed": self.automated_passed,
            "automated_failed": self.automated_failed,
            "pipeline_run_id": self.pipeline_run_id,
            "errors": self.errors,
        }


# ─────────────────────────────────────────────────────────────────────────────
# TTP → LazyOwn command mapping
# ─────────────────────────────────────────────────────────────────────────────


class ITTPMapper(ABC):
    """Resolves a MITRE technique + atomic test to a LazyOwn command."""

    @abstractmethod
    def resolve(self, technique_id: str, atomic_test: dict[str, Any], platform: str) -> str | None:
        """Return a LazyOwn shell command string or None if unmapped."""


class DefaultTTPMapper(ITTPMapper):
    """Maps known technique IDs to LazyOwn commands via a dictionary.

    The mapping is extensible; operators can register additional commands
    at runtime via ``register``.
    """

    _registry: dict[str, dict[str, str]] = {
        "T1003.001": {
            "windows": "mimikatz",
            "linux": "procdump_py",
        },
        "T1059.001": {
            "windows": "powershell_cmd_stager",
            "linux": "",
        },
        "T1041": {
            "any": "exfil_dns",
        },
        "T1547.001": {
            "windows": "persist_registry",
        },
        "T1027": {
            "windows": "obfuscate_powershell",
            "linux": "obfuscate_sh",
        },
        "T1566.001": {
            "any": "phishing_wizard",
        },
        "T1195.002": {
            "any": "supply_chain_scan",
        },
        "T1110": {
            "any": "hydra",
        },
        "T1083": {
            "any": "file_discovery",
        },
        "T1057": {
            "any": "process_discovery",
        },
        "T1018": {
            "any": "remote_system_discovery",
        },
        "T1046": {
            "any": "lazynmap",
        },
        "T1135": {
            "any": "network_share_discovery",
        },
        "T1069": {
            "any": "enum_permissions",
        },
        "T1087": {
            "windows": "enum_users",
            "linux": "enum_users",
        },
        "T1552.001": {
            "windows": "credential_vault",
            "linux": "credential_vault",
        },
        "T1003.002": {
            "windows": "samdump2",
        },
        "T1482": {
            "windows": "domain_trust_discovery",
        },
        "T1558.003": {
            "windows": "kerberoast",
        },
        "T1550.002": {
            "windows": "pth_net",
        },
        "T1570": {
            "any": "lateral_mov_lin",
        },
    }

    @classmethod
    def register(cls, technique_id: str, platform: str, command: str) -> None:
        """Add a new technique-to-command mapping."""
        entry = cls._registry.setdefault(technique_id, {})
        entry[platform.lower()] = command

    def resolve(self, technique_id: str, atomic_test: dict[str, Any], platform: str) -> str | None:
        entry = self._registry.get(technique_id, {})
        platform_lower = platform.lower()
        command = entry.get(platform_lower) or entry.get("any") or entry.get("windows") or entry.get("linux")
        if not command:
            return None
        if atomic_test.get("manual"):
            manual_command = atomic_test.get("manual_command", "")
            if manual_command:
                return manual_command
        return command


# ─────────────────────────────────────────────────────────────────────────────
# Loader
# ─────────────────────────────────────────────────────────────────────────────


class PlaybookLoader:
    """Parses playbook YAML files into PlaybookSpec objects."""

    SUPPORTED_EXTENSIONS = (".yaml", ".yml")

    def __init__(self, playbooks_dir: Path | None = None) -> None:
        self._dir = playbooks_dir or PLAYBOOKS_DIR

    def list(self) -> list[str]:
        """Return every discoverable playbook name."""
        if not self._dir.exists():
            return []
        out: list[str] = []
        for entry in sorted(self._dir.iterdir()):
            if entry.suffix.lower() not in self.SUPPORTED_EXTENSIONS:
                continue
            if entry.stem.lower().startswith(("example", "attack_plan", "lazyown_auto", "readme")):
                continue
            out.append(entry.stem)
        return out

    def load(self, name: str) -> PlaybookSpec:
        """Load and validate a playbook by name."""
        path = self._dir / f"{name}.yaml"
        if not path.exists():
            path = self._dir / f"{name}.yml"
        if not path.exists():
            raise FileNotFoundError(f"playbook {name!r} not found in {self._dir}")
        with path.open(encoding="utf-8") as fh:
            raw = yaml.safe_load(fh)
        return self._validate(raw, str(path))

    def _validate(self, raw: dict[str, Any], source_path: str) -> PlaybookSpec:
        apt_name = raw.get("apt_name", "Unknown")
        aliases = raw.get("aliases", [])
        if isinstance(aliases, str):
            aliases = [aliases]
        platforms = raw.get("platforms", [])
        if isinstance(platforms, str):
            platforms = [platforms]
        source_urls = raw.get("source_urls", [])
        description = raw.get("description", "")
        phases_raw = raw.get("phases", [])
        if not isinstance(phases_raw, list):
            phases_raw = []

        phases: list[PlaybookTechnique] = []
        for phase_data in phases_raw:
            atomic_tests = phase_data.get("atomic_tests", [])
            if isinstance(atomic_tests, dict):
                atomic_tests = [atomic_tests]
            elif not isinstance(atomic_tests, list):
                atomic_tests = []
            detection_hints = phase_data.get("detection_hints", [])
            if isinstance(detection_hints, str):
                detection_hints = [detection_hints]
            phases.append(PlaybookTechnique(
                name=phase_data.get("name", ""),
                technique_id=phase_data.get("technique_id", ""),
                technique_name=phase_data.get("technique_name", ""),
                description=phase_data.get("description", ""),
                atomic_tests=atomic_tests,
                detection_hints=list(detection_hints),
            ))
        return PlaybookSpec(
            apt_name=apt_name,
            aliases=list(aliases),
            description=str(description),
            platforms=list(platforms),
            phases=phases,
            source_urls=list(source_urls),
            source_path=source_path,
        )


# ─────────────────────────────────────────────────────────────────────────────
# Helper: generate a runnable pipeline from a playbook
# ─────────────────────────────────────────────────────────────────────────────


def _build_pipeline_yaml(playbook: PlaybookSpec, mapper: ITTPMapper, platform: str) -> str:
    """Generate a pipelines/<name>.yaml string from a playbook spec."""
    steps: list[dict[str, Any]] = []
    for tech in playbook.phases:
        for test in tech.atomic_tests:
            if test.get("manual"):
                steps.append({
                    "name": f"{tech.name}_{tech.technique_id}",
                    "command": "echo",
                    "args": f"[MANUAL] {tech.technique_name}: {test.get('name', tech.technique_id)} — {test.get('manual_instructions', 'perform manually')}",
                    "on_failure": "continue",
                })
                continue
            command = mapper.resolve(tech.technique_id, test, platform)
            if not command:
                detection = ", ".join(tech.detection_hints[:1]) if tech.detection_hints else ""
                steps.append({
                    "name": f"{tech.name}_{tech.technique_id}",
                    "command": "echo",
                    "args": f"[UNMAPPED] {tech.technique_id}: {tech.technique_name}. Hints: {detection}",
                    "on_failure": "continue",
                })
                continue
            args = test.get("args", "")
            steps.append({
                "name": f"{tech.name}_{tech.technique_id}",
                "command": command,
                "args": str(args),
                "on_failure": "continue",
            })
    pipeline_name = f"playbook_{playbook.apt_name.lower().replace(' ', '_').replace('-', '_')}"
    safe_name = re.sub(r"[^a-z0-9_]", "_", pipeline_name)[:80]
    doc = {
        "name": safe_name,
        "description": f"Auto-generated pipeline from playbook {playbook.apt_name}. Platform: {platform}.",
        "steps": steps,
    }
    return yaml.safe_dump(doc, sort_keys=False, allow_unicode=True)


# ─────────────────────────────────────────────────────────────────────────────
# Engine
# ─────────────────────────────────────────────────────────────────────────────


class PlaybookEngine:
    """Orchestrates playbook analysis, pipeline generation, and execution."""

    def __init__(
        self,
        loader: PlaybookLoader | None = None,
        mapper: ITTPMapper | None = None,
        pipelines_dir: Path | None = None,
    ) -> None:
        self._loader = loader or PlaybookLoader()
        self._mapper = mapper or DefaultTTPMapper()
        self._pipelines_dir = pipelines_dir or PIPELINES_DIR

    @property
    def loader(self) -> PlaybookLoader:
        return self._loader

    def analyze(self, name: str, platform: str = "windows") -> PlaybookRunResult:
        """Analyze a playbook: count techniques, automated vs manual, coverage."""
        playbook = self._loader.load(name)
        result = PlaybookRunResult(
            playbook_name=name,
            apt_name=playbook.apt_name,
            total_techniques=len(playbook.phases),
            executed_techniques=0,
            manual_skipped=0,
            automated_passed=0,
            automated_failed=0,
        )
        for tech in playbook.phases:
            for test in tech.atomic_tests:
                if test.get("manual"):
                    result.manual_skipped += 1
                    continue
                command = self._mapper.resolve(tech.technique_id, test, platform)
                if command:
                    result.automated_passed += 1
                else:
                    result.automated_failed += 1
        result.executed_techniques = result.automated_passed + result.automated_failed
        return result

    def generate_pipeline(self, name: str, platform: str = "windows") -> str:
        """Generate a pipeline YAML file from a playbook.

        Returns the path to the generated pipeline file.
        """
        playbook = self._loader.load(name)
        yaml_content = _build_pipeline_yaml(playbook, self._mapper, platform)
        safe_name = re.sub(r"[^A-Za-z0-9._-]", "_", f"playbook_{name}")[:80]
        pipeline_path = self._pipelines_dir / f"{safe_name}.yaml"
        pipeline_path.write_text(yaml_content, encoding="utf-8")
        return str(pipeline_path)

    def run(self, name: str, platform: str = "windows", target: str = "", onecmd: Any = None) -> PlaybookRunResult:
        """Generate and execute a pipeline from a playbook.

        Requires the pipeline engine to be available. When *onecmd* is
        provided, commands execute inside the caller's shell.
        """
        analysis = self.analyze(name, platform)
        pipeline_path = self.generate_pipeline(name, platform)
        pipeline_name = Path(pipeline_path).stem
        try:
            from modules.pipeline_engine import get_default_engine
            engine = get_default_engine(onecmd=onecmd)
            run = engine.run(pipeline_name, target=target or "")
            analysis.pipeline_run_id = run.run_id
            analysis.errors = [run.error] if run.error else []
        except Exception as exc:
            analysis.errors.append(f"Pipeline execution failed: {exc}")
        return analysis


# ─────────────────────────────────────────────────────────────────────────────
# Public entry points
# ─────────────────────────────────────────────────────────────────────────────


def playbook_list() -> str:
    """Return a JSON array of available playbooks."""
    loader = PlaybookLoader()
    return json.dumps(loader.list(), indent=2)


def playbook_analyze(name: str, platform: str = "windows") -> str:
    """Return a JSON summary of one playbook."""
    engine = PlaybookEngine()
    result = engine.analyze(name, platform)
    return json.dumps(result.to_dict(), indent=2)


def playbook_generate(name: str, platform: str = "windows") -> str:
    """Generate a runnable pipeline from a playbook. Returns the path."""
    engine = PlaybookEngine()
    path = engine.generate_pipeline(name, platform)
    return json.dumps({"status": "ok", "pipeline_path": path}, indent=2)


def playbook_run(name: str, platform: str = "windows", target: str = "", onecmd: Any = None) -> str:
    """Analyze, generate, and execute a playbook. Returns a JSON summary."""
    engine = PlaybookEngine()
    result = engine.run(name, platform=platform, target=target, onecmd=onecmd)
    return json.dumps(result.to_dict(), indent=2)


__all__ = [
    "PlaybookLoader",
    "PlaybookSpec",
    "PlaybookTechnique",
    "PlaybookRunResult",
    "PlaybookEngine",
    "ITTPMapper",
    "DefaultTTPMapper",
    "playbook_list",
    "playbook_analyze",
    "playbook_generate",
    "playbook_run",
]
