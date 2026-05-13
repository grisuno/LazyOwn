"""APT Playbook Engine — map public APT reports to executable Atomic Red Team chains.

This module reads enriched playbooks from ``playbooks/apt_*.yaml`` and provides
execution, validation, and reporting without touching ``lazyown.py`` internals.

Playbook schema (enriched):
    apt_name: str
    aliases: list[str]
    source_urls: list[str]
    description: str
    platforms: list[str]
    phases:
      - name: str            # e.g. initial_access, persistence, privilege_escalation
        technique_id: str     # MITRE ATT&CK technique (e.g. T1566.001)
        technique_name: str
        description: str
        atomic_tests:
          - atomic_id: str    # ART auto_generated_guid
            name: str
            manual: bool      # If true, operator must paste command interactively
        caldera_abilities:    # Optional CALDERA ability IDs
          - ability_id: str
        detection_hints: list[str]
"""

from __future__ import annotations

import glob
import json
import os
import time
from dataclasses import dataclass, field
from typing import Any

import yaml

from core.console import print_error, print_msg, print_succ, print_warn
from utils import copy2clip, is_binary_present, run_command


@dataclass
class AtomicTestRef:
    atomic_id: str
    name: str = ""
    manual: bool = True


@dataclass
class CalderaAbilityRef:
    ability_id: str
    name: str = ""


@dataclass
class PhaseStep:
    name: str
    technique_id: str
    technique_name: str = ""
    description: str = ""
    atomic_tests: list[AtomicTestRef] = field(default_factory=list)
    caldera_abilities: list[CalderaAbilityRef] = field(default_factory=list)
    detection_hints: list[str] = field(default_factory=list)


@dataclass
class AptPlaybook:
    apt_name: str
    aliases: list[str] = field(default_factory=list)
    source_urls: list[str] = field(default_factory=list)
    description: str = ""
    platforms: list[str] = field(default_factory=list)
    phases: list[PhaseStep] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "AptPlaybook":
        phases = []
        for ph in data.get("phases", []):
            atomic_tests = [
                AtomicTestRef(**t) for t in ph.get("atomic_tests", [])
            ]
            caldera_abilities = [
                CalderaAbilityRef(**a) for a in ph.get("caldera_abilities", [])
            ]
            phases.append(PhaseStep(
                name=ph.get("name", ""),
                technique_id=ph.get("technique_id", ""),
                technique_name=ph.get("technique_name", ""),
                description=ph.get("description", ""),
                atomic_tests=atomic_tests,
                caldera_abilities=caldera_abilities,
                detection_hints=ph.get("detection_hints", []),
            ))
        return cls(
            apt_name=data["apt_name"],
            aliases=data.get("aliases", []),
            source_urls=data.get("source_urls", []),
            description=data.get("description", ""),
            platforms=data.get("platforms", []),
            phases=phases,
        )

    def to_summary(self) -> dict[str, Any]:
        return {
            "apt_name": self.apt_name,
            "aliases": self.aliases,
            "description": self.description,
            "platforms": self.platforms,
            "phases": len(self.phases),
            "atomic_tests": sum(len(p.atomic_tests) for p in self.phases),
            "caldera_abilities": sum(len(p.caldera_abilities) for p in self.phases),
        }


class AptPlaybookEngine:
    """Load, list, validate and execute APT playbooks."""

    def __init__(self, playbook_dir: str = "playbooks"):
        self.playbook_dir = playbook_dir
        self._playbooks: dict[str, AptPlaybook] = {}
        self._load_all()

    def _load_all(self) -> None:
        pattern = os.path.join(self.playbook_dir, "apt_*.yaml")
        for path in glob.glob(pattern):
            try:
                with open(path, "r") as f:
                    data = yaml.safe_load(f)
                pb = AptPlaybook.from_dict(data)
                key = pb.apt_name.lower().replace(" ", "_")
                self._playbooks[key] = pb
            except Exception as e:
                print_warn(f"[apt_playbook] Failed to load {path}: {e}")

    def list_playbooks(self) -> list[dict[str, Any]]:
        return [pb.to_summary() for pb in self._playbooks.values()]

    def get(self, name: str) -> AptPlaybook | None:
        key = name.lower().replace(" ", "_")
        return self._playbooks.get(key)

    def validate(self, pb: AptPlaybook, atomic_path: str | None = None) -> dict[str, Any]:
        """Validate that all referenced atomic tests exist locally."""
        missing_atomic: list[dict] = []
        found_atomic: list[dict] = []
        if atomic_path and os.path.exists(atomic_path):
            atomic_map = self._build_atomic_index(atomic_path)
        else:
            atomic_map = {}

        for phase in pb.phases:
            for test in phase.atomic_tests:
                if test.atomic_id in atomic_map:
                    found_atomic.append({
                        "phase": phase.name,
                        "atomic_id": test.atomic_id,
                        "name": atomic_map[test.atomic_id],
                    })
                else:
                    missing_atomic.append({
                        "phase": phase.name,
                        "atomic_id": test.atomic_id,
                        "name": test.name,
                    })

        return {
            "apt_name": pb.apt_name,
            "phases": len(pb.phases),
            "atomic_tests_found": len(found_atomic),
            "atomic_tests_missing": len(missing_atomic),
            "missing": missing_atomic,
            "found": found_atomic,
        }

    def _build_atomic_index(self, atomic_yaml_path: str) -> dict[str, str]:
        index: dict[str, str] = {}
        yaml_files = glob.glob(os.path.join(atomic_yaml_path, "**", "*.yaml"), recursive=True)
        for file in yaml_files:
            try:
                with open(file, "r") as f:
                    data = yaml.safe_load(f)
                if "atomic_tests" in data:
                    for test in data["atomic_tests"]:
                        index[test["auto_generated_guid"]] = test["name"]
            except Exception:
                continue
        return index

    def generate_attack_plan(self, pb: AptPlaybook, output_path: str) -> None:
        """Generate a legacy ``attack_plan.yaml`` from an enriched APT playbook."""
        steps = []
        for phase in pb.phases:
            for test in phase.atomic_tests:
                steps.append({"atomic_id": test.atomic_id})
        plan = {
            "apt_name": pb.apt_name,
            "description": pb.description,
            "steps": steps,
        }
        with open(output_path, "w") as f:
            yaml.dump(plan, f, default_flow_style=False)
        print_succ(f"[apt_playbook] Attack plan written to {output_path}")

    def report_json(self, pb: AptPlaybook, output_path: str) -> None:
        """Write a structured JSON report of the playbook for the operator."""
        report = {
            "apt_name": pb.apt_name,
            "aliases": pb.aliases,
            "source_urls": pb.source_urls,
            "description": pb.description,
            "platforms": pb.platforms,
            "generated_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
            "phases": [
                {
                    "name": ph.name,
                    "technique_id": ph.technique_id,
                    "technique_name": ph.technique_name,
                    "description": ph.description,
                    "atomic_tests": [
                        {"atomic_id": t.atomic_id, "name": t.name, "manual": t.manual}
                        for t in ph.atomic_tests
                    ],
                    "caldera_abilities": [
                        {"ability_id": a.ability_id, "name": a.name}
                        for a in ph.caldera_abilities
                    ],
                    "detection_hints": ph.detection_hints,
                }
                for ph in pb.phases
            ],
        }
        with open(output_path, "w") as f:
            json.dump(report, f, indent=2)
        print_succ(f"[apt_playbook] Report written to {output_path}")
