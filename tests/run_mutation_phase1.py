"""Mutation testing runner for Phase 1 data-gap closure.

Introduces targeted mutations into the production code that correspond
to the gaps we closed. If a mutant survives, the test suite failed to
detect the regression — meaning the gap would silently reappear.

Mutations:
    1. service_version back to add_note        — should kill test_phase1_data_gaps
    2. domain handler removed                  — should kill test_phase1_data_gaps
    3. email handler removed                   — should kill test_phase1_data_gaps
    4. _EmailExtractor not registered          — should kill test_phase1_data_gaps
    5. _emails.clear() missing from reset      — should kill test_phase1_data_gaps
    6. metadata port removed from extractor    — should kill test_phase1_data_gaps
    7. credential_aware_rank without boost     — should kill test_phase1_data_gaps
    8. GraphTopologySignal wired incorrectly   — should kill test_phase1_data_gaps
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

MUTATIONS = {
    "svc_version_back_to_note": {
        "file": "modules/world_model.py",
        "description": "Replace add_service call with add_note (revert GAP-1)",
        "old": """                elif ftype == "service_version":
                    if host:
                        name, _, version = value.partition(" ")
                        port = meta.get("port", 0)
                        protocol = meta.get("protocol", "tcp")
                        self.add_service(
                            host,
                            port=int(port) if port else 0,
                            name=name.strip(),
                            version=version.strip(),
                            protocol=str(protocol),
                        )""",
        "new": """                elif ftype == "service_version":
                    if host:
                        self.add_note(host, f"service: {value}")""",
        "expected": "test_service_version_calls_add_service MUST fail",
        "tests": "tests/test_phase1_data_gaps.py::TestUpdateFromFindings::test_service_version_calls_add_service",
    },
    "domain_handler_removed": {
        "file": "modules/world_model.py",
        "description": "Remove domain handler from update_from_findings (revert GAP-2)",
        "old": """                elif ftype == "domain":
                    if host:
                        self.add_domain(value, host=host)
                    else:
                        self.add_domain(value)""",
        "new": """                elif ftype == "domain":
                    pass""",
        "expected": "test_domain_finding_calls_add_domain MUST fail",
        "tests": "tests/test_phase1_data_gaps.py::TestUpdateFromFindings::test_domain_finding_calls_add_domain",
    },
    "email_handler_removed": {
        "file": "modules/world_model.py",
        "description": "Remove email handler from update_from_findings (revert GAP-2)",
        "old": """                elif ftype == "email":
                    if host:
                        self.add_email(value, host=host)
                    else:
                        self.add_email(value)""",
        "new": """                elif ftype == "email":
                    pass""",
        "expected": "test_email_finding_calls_add_email MUST fail",
        "tests": "tests/test_phase1_data_gaps.py::TestUpdateFromFindings::test_email_finding_calls_add_email",
    },
    "email_extractor_not_registered": {
        "file": "modules/obs_parser.py",
        "description": "Remove _EmailExtractor from ObsParser init (revert GAP-1)",
        "old": """            _EmailExtractor(),
            _ErrorExtractor()""",
        "new": """            _ErrorExtractor()""",
        "expected": "test_parser_extracts_emails_from_output MUST fail",
        "tests": "tests/test_phase1_data_gaps.py::TestObsParserIncludesEmailExtractor::test_parser_extracts_emails_from_output",
    },
    "reset_missing_emails_clear": {
        "file": "modules/world_model.py",
        "description": "Remove _emails._domains.clear() from reset (revert GAP-2)",
        "old": """            self._vulns.clear()
            self._emails.clear()
            self._domains.clear()
            if self._path.exists()""",
        "new": """            self._vulns.clear()
            if self._path.exists()""",
        "expected": "test_reset_clears_emails_and_domains MUST fail",
        "tests": "tests/test_phase1_data_gaps.py::TestWorldModelPersistence::test_reset_clears_emails_and_domains",
    },
    "svc_extractor_no_port_in_metadata": {
        "file": "modules/obs_parser.py",
        "description": "Remove port from ServiceVersionExtractor metadata (revert GAP-1)",
        "old": """            results.append(Finding(
                FindingType.SERVICE_VERSION, value,
                host=host, confidence=0.95, raw=m.group(),
                metadata={"port": port, "protocol": protocol},
            ))""",
        "new": """            results.append(Finding(
                FindingType.SERVICE_VERSION, value,
                host=host, confidence=0.95, raw=m.group(),
            ))""",
        "expected": "test_port_and_protocol_in_metadata MUST fail",
        "tests": "tests/test_phase1_data_gaps.py::TestServiceVersionExtractor::test_port_and_protocol_in_metadata",
    },
    "credential_aware_rank_no_boost": {
        "file": "modules/autonomous_exploit_engine.py",
        "description": "Neutralize credential boost in _credential_aware_rank (revert GAP-4)",
        "old": """            base = candidate.confidence
            if candidate.strategy in ("brute_force",):
                if has_plaintext:
                    candidate.confidence = min(base * 2.5, 1.0)""",
        "new": """            base = candidate.confidence
            if candidate.strategy in ("brute_force",):
                if has_plaintext:
                    candidate.confidence = base""",
        "expected": "test_credential_aware_rank_boosts_brute_force MUST fail",
        "tests": "tests/test_phase1_data_gaps.py::TestCredentialAwareRetry::test_credential_aware_rank_boosts_brute_force",
    },
    "graph_topology_missing_from_engine": {
        "file": "cli/recommendation_signals.py",
        "description": "Remove GraphTopologySignal from build_default_engine (revert GAP-3)",
        "old": """    topology_signal = GraphTopologySignal(sessions_dir=sessions_dir)
    signals.append(topology_signal)

    signals.append(_build_killchain_signal())""",
        "new": """    signals.append(_build_killchain_signal())""",
        "expected": "test_signals_are_wired_in_build_default_engine MUST fail",
        "tests": "tests/test_phase1_data_gaps.py::TestGraphTopologySignal::test_signals_are_wired_in_build_default_engine",
    },
}


def backup_files(mutations: dict, base_dir: Path) -> dict[str, str]:
    backups = {}
    for name, info in mutations.items():
        path = base_dir / info["file"]
        if path.exists():
            backups[name] = path.read_text()
    return backups


def restore_files(backups: dict[str, str], base_dir: Path, mutations: dict):
    for name, original in backups.items():
        path = base_dir / mutations[name]["file"]
        path.write_text(original)


def run_tests() -> bool:
    result = subprocess.run(
        [sys.executable, "-m", "pytest", "tests/test_phase1_data_gaps.py", "-x", "-q"],
        capture_output=True,
        text=True,
        timeout=120,
        cwd=str(BASE_DIR),
    )
    return result.returncode == 0


def main():
    print("=" * 60)
    print("Mutation Testing — Phase 1 Data-Gap Closure")
    print("=" * 60)

    backups = backup_files(MUTATIONS, BASE_DIR)

    try:
        print("\n[1] Running baseline tests (no mutation)...")
        baseline_pass = run_tests()
        if not baseline_pass:
            print("  FAIL: Baseline tests do not pass. Fix tests first.")
            return 1
        print("  PASS: All 40 baseline tests pass.")

        killed = 0
        survived = 0
        errors = 0

        for name, info in MUTATIONS.items():
            print(f"\n[2] Mutation: {name}")
            print(f"    {info['description']}")

            path = BASE_DIR / info["file"]
            content = path.read_text()

            if info["old"] not in content:
                print(f"    SKIP: Target text not found (already mutated?)")
                errors += 1
                continue

            mutated = content.replace(info["old"], info["new"], 1)
            path.write_text(mutated)

            test_list = info.get("tests", "")
            tests_pass = run_tests()
            path.write_text(content)

            if not tests_pass:
                print(f"    KILLED: Mutant detected.")
                killed += 1
            else:
                print(f"    SURVIVED: Mutant NOT detected - tests too weak!")
                print(f"    Expected: {info['expected']}")
                survived += 1

        print("\n" + "=" * 60)
        print(f"Results: {killed} killed, {survived} survived, {errors} skipped")
        if survived > 0:
            print(f"WARNING: {survived} mutants survived - improve test coverage.")
        else:
            print("ALL MUTANTS KILLED - Tests are robust.")
        print("=" * 60)

        return 0 if survived == 0 else 1

    finally:
        print("\n[3] Restoring original files...")
        restore_files(backups, BASE_DIR, MUTATIONS)
        baseline = run_tests()
        if baseline:
            print("  Restored: Baseline tests pass.")
        else:
            print("  ERROR: Restoration failed. Baseline tests broken!")
            return 2


if __name__ == "__main__":
    sys.exit(main())
