"""Mutation runner for the disposable infra and reporting contracts.

Applies targeted mutations to ``cli/commands/infra.py``,
``modules/c2_builder.py``, ``modules/professional_report.py``, and
``modules/redteam_gym.py``, verifying that
``tests/test_infra_disposable.py`` plus
``tests/test_bdd_infra_range_report.py`` detect each one.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

MUTATIONS = {
    "tunnel_regex_relaxed": {
        "file": "cli/commands/infra.py",
        "description": "Relax tunnel URL regex so non-cloudflare hosts match",
        "old": 'TUNNEL_URL_PATTERN = re.compile(r"https://[-0-9a-z]+\\.trycloudflare\\.com")',
        "new": 'TUNNEL_URL_PATTERN = re.compile(r"https://.+")',
        "expected": "test_parse_tunnel_urls_rejects_non_cloudflare must fail",
    },
    "provider_allowlist_opened": {
        "file": "cli/commands/infra.py",
        "description": "Widen provider allowlist with an unknown provider",
        "old": 'VALID_PROVIDERS = frozenset({"local", "docker", "digitalocean", "aws"})',
        "new": 'VALID_PROVIDERS = frozenset({"local", "docker", "digitalocean", "aws", "evil"})',
        "expected": "test_valid_providers_exact_allowlist must fail",
    },
    "go_empty_list_neutered": {
        "file": "modules/c2_builder.py",
        "description": "Drop the empty fallback guard in Go slice rendering",
        "old": '    if not urls:\n        return \'""\'',
        "new": '    if not urls:\n        return \'"" , ""\'',
        "expected": "test_go_string_list_formats_slice must fail",
    },
    "report_window_relaxed": {
        "file": "modules/professional_report.py",
        "description": "Stretch remediation window from 30 to 90 days",
        "old": "should be remediated within 30 days, Medium",
        "new": "should be remediated within 90 days, Medium",
        "expected": "test_report_template_summary_mentions_remediation_windows must fail",
    },
    "mitre_unknown_tactic_dropped": {
        "file": "cli/commands/report_enhanced.py",
        "description": "Drop unknown tactics from the MITRE matrix again",
        "old": "    for tactic in tactics_order + sorted(set(tactics_present) - set(tactics_order)):",
        "new": "    for tactic in tactics_order:",
        "expected": "test_mitre_matrix_keeps_unknown_tactics must fail",
    },
    "timeline_payload_dumped": {
        "file": "cli/commands/report_enhanced.py",
        "description": "Dump raw payload dict instead of summarizing the command",
        "old": '            details = f"{command} {args}".strip()',
        "new": "            details = str(payload)",
        "expected": "test_format_timeline_event_summarizes_payload must fail",
    },
    "compile_cd_prefix_dropped": {
        "file": "modules/c2_builder.py",
        "description": "Drop the cd prefix so CGO commands bypass bash",
        "old": '        f"cd {sessions_dir} && CGO_ENABLED=0 GOOS={profile.goos} GOARCH={profile.goarch} "',
        "new": '        f"CGO_ENABLED=0 GOOS={profile.goos} GOARCH={profile.goarch} "',
        "expected": "test_compile_commands_route_through_shell must fail",
    },
    "range_tty_dropped": {
        "file": "deploy/range/ad-mini/docker-compose.yml",
        "description": "Drop tty so ws01 falls back into a restart loop",
        "old": "    stdin_open: true\n    tty: true",
        "new": "    stdin_open: true",
        "expected": "test_range_workstation_stays_alive must fail",
    },
    "range_verify_uid_relaxed": {
        "file": "cli/commands/lab.py",
        "description": "Accept any shell answer as root in range verify",
        "old": '        if "uid=0" in answer:',
        "new": '        if "uid=999" in answer:',
        "expected": "test_range_verify_confirms_root must fail",
    },
    "vault_challenge_scenario_swapped": {
        "file": "modules/redteam_gym.py",
        "description": "Move vault_exfil off the ad-mini range scenario",
        "old": '        "description": "Use QuantumVault tradecraft from the range implant to stage and exfiltrate a loot bundle.",\n        "scenario": "ad-mini",',
        "new": '        "description": "Use QuantumVault tradecraft from the range implant to stage and exfiltrate a loot bundle.",\n        "scenario": "metasploitable",',
        "expected": "test_gym_range_challenges_registered must fail",
    },
}

TEST_FILES = ["tests/test_infra_disposable.py", "tests/test_bdd_infra_range_report.py"]


def backup_files(mutations: dict, base_dir: Path) -> dict[str, str]:
    """Snapshot mutated files for restoration.

    Args:
        mutations: Mutation table.
        base_dir: Repository root.

    Returns:
        Mapping of mutation name to original file content.
    """
    backups = {}
    for name, info in mutations.items():
        path = base_dir / info["file"]
        if path.exists():
            backups[name] = path.read_text()
    return backups


def restore_files(backups: dict[str, str], base_dir: Path, mutations: dict) -> None:
    """Restore original file contents.

    Args:
        backups: Original contents by mutation name.
        base_dir: Repository root.
        mutations: Mutation table.
    """
    for name, original in backups.items():
        (base_dir / mutations[name]["file"]).write_text(original)


def run_tests() -> bool:
    """Run the scoped contract suites.

    Returns:
        True when both suites pass.
    """
    result = subprocess.run(
        [sys.executable, "-m", "pytest", *TEST_FILES, "-q", "-p", "no:cacheprovider"],
        capture_output=True,
        text=True,
        timeout=120,
    )
    return result.returncode == 0


def main() -> int:
    """Execute the scoped mutation gate.

    Returns:
        Process exit code, nonzero when a mutant survives.
    """
    base_dir = Path(__file__).resolve().parent.parent
    backups = backup_files(MUTATIONS, base_dir)

    print("Mutation Testing — disposable infra and reporting contracts")
    print("=" * 60)

    if not run_tests():
        print("FAIL: Baseline tests do not pass. Fix tests first.")
        return 1
    print("PASS: Baseline tests all pass.")

    killed = 0
    survived = 0
    skipped = 0

    try:
        for name, info in MUTATIONS.items():
            print(f"\nMutation: {name}")
            print(f"    {info['description']}")
            path = base_dir / info["file"]
            content = path.read_text()

            if info["old"] not in content:
                print("    SKIP: target text not found.")
                skipped += 1
                continue

            path.write_text(content.replace(info["old"], info["new"], 1))

            if run_tests():
                print("    SURVIVED: mutant NOT detected — tests are too weak.")
                print(f"    Expected: {info['expected']}")
                survived += 1
            else:
                print("    KILLED: mutant detected by tests.")
                killed += 1

            path.write_text(content)

        print("\n" + "=" * 60)
        print(f"Results: {killed} killed, {survived} survived, {skipped} skipped")
        print("ALL MUTANTS KILLED — tests are robust." if survived == 0 else "WARNING: mutants survived — improve test coverage.")
        print("=" * 60)
        return 0 if survived == 0 else 1
    finally:
        restore_files(backups, base_dir, MUTATIONS)
        if run_tests():
            print("Restored: baseline tests pass.")
        else:
            print("ERROR: restoration failed.")
            return 2


if __name__ == "__main__":
    sys.exit(main())
