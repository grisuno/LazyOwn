"""Mutation runner for the orchestrator-governed LLM failover contract.

Applies targeted mutations to the failover chain module and its wiring
points, then verifies that ``tests/test_llm_orchestrator.py`` kills each
one. A surviving mutant means the contract tests are too weak and must
be improved before the change ships.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

MUTATIONS = {
    "chain_weights_inverted": {
        "file": "modules/llm_orchestrator.py",
        "description": "Invert the priority-weight sort so the weakest member is tried first",
        "old": "    return sorted(members, key=_weight, reverse=True)",
        "new": "    return sorted(members, key=_weight, reverse=False)",
        "expected": "test_weights_sort_members_by_descending_priority must fail",
    },
    "fallback_notice_suppressed": {
        "file": "modules/llm_orchestrator.py",
        "description": "Drop the fallback notice so primary failures stay invisible",
        "old": '        result.notice = _notice_fallback(primary, attempts, served["member"])',
        "new": '        result.notice = ""',
        "expected": "test_primary_failure_serves_fallback_with_notice must fail",
    },
    "fallback_flag_inverted": {
        "file": "modules/llm_orchestrator.py",
        "description": "Flip fallback_used so primary success claims failover",
        "old": '        fallback_used=primary is None or str(served["member"].get("name", "")) != str(primary.get("name", "")),',
        "new": '        fallback_used=primary is None or str(served["member"].get("name", "")) == str(primary.get("name", "")),',
        "expected": "test_primary_success_needs_no_fallback must fail",
    },
    "exhausted_help_suppressed": {
        "file": "modules/llm_orchestrator.py",
        "description": "Return empty text on total exhaustion instead of the help message",
        "old": "        text=HELP_MESSAGE,\n        backend=\"error\",\n        notice=notice,\n        attempts=list(attempts),\n        attempted_specs=list(specs),",
        "new": "        text=\"\",\n        backend=\"error\",\n        notice=notice,\n        attempts=list(attempts),\n        attempted_specs=list(specs),",
        "expected": "test_all_members_fail_returns_error_result_without_raising must fail",
    },
    "error_banner_accepted_as_content": {
        "file": "modules/llm_orchestrator.py",
        "description": "Accept backend error banners as operator content",
        "old": "        if is_error_reply(text):",
        "new": "        if False and is_error_reply(text):",
        "expected": "test_error_banner_text_is_a_failure_not_content must fail",
    },
    "breaker_never_parks": {
        "file": "modules/llm_orchestrator.py",
        "description": "Ignore the health breaker so parked members are hammered",
        "old": "                if not health.healthy(name):",
        "new": "                if False and not health.healthy(name):",
        "expected": "test_unhealthy_member_is_skipped_while_others_remain must fail",
    },
    "last_resort_walk_removed": {
        "file": "modules/llm_orchestrator.py",
        "description": "Skip the last-resort pass so parked chains never answer",
        "old": "    if served is None and skipped:",
        "new": "    if False and served is None and skipped:",
        "expected": "test_all_unhealthy_members_still_get_attempted must fail",
    },
    "empty_prompt_guard_removed": {
        "file": "modules/llm_orchestrator.py",
        "description": "Contact the chain for blank prompts",
        "old": '    if not (prompt or "").strip():',
        "new": '    if False and not (prompt or "").strip():',
        "expected": "test_empty_prompt_short_circuits must fail",
    },
    "quota_markers_dropped": {
        "file": "modules/llm_orchestrator.py",
        "description": "Stop treating quota exhaustion prose as a failure",
        "old": "    return any(mark in lowered for mark in LLM_QUOTA_MARKERS)",
        "new": "    return False",
        "expected": "test_quota_wording_reply_is_a_failure must fail",
    },
    "health_success_not_reported": {
        "file": "modules/llm_orchestrator.py",
        "description": "Stop reporting member success to the health registry",
        "old": "                health.report_success(name)",
        "new": "                pass",
        "expected": "test_success_reports_health must fail",
    },
    "groq_env_key_not_published": {
        "file": "modules/llm_orchestrator.py",
        "description": "Drop the payload-to-environment Groq key sync",
        "old": '        os.environ["GROQ_API_KEY"] = candidate',
        "new": "        return None",
        "expected": "test_explicit_api_key_published_to_environment must fail",
    },
    "adapter_chain_fallback_removed": {
        "file": "modules/llm_adapter.py",
        "description": "Bots with no Groq client fail instead of failing over",
        "old": "    if client is None:\n        return _orchestrated(full_prompt, prompt, store)",
        "new": "    if client is None:\n        return _LEGACY_NO_KEY_ERROR",
        "expected": "test_missing_client_serves_from_the_chain must fail",
    },
    "ai_fallback_chain_delegation_removed": {
        "file": "modules/ai_fallback.py",
        "description": "ai_fallback.call ignores the orchestrator chain outcome",
        "old": "    if orch.ok:",
        "new": "    if False and orch.ok:",
        "expected": "test_orchestrator_success_maps_to_ai_result must fail",
    },
    "error_code_marker_dropped": {
        "file": "modules/llm_orchestrator.py",
        "description": "Stop recognizing SDK error-code banners so 401 leaks as content",
        "old": '    "error code: 4",',
        "new": '    "error cod3: 4",',
        "expected": "test_error_replies_detected must fail",
    },
    "placeholder_env_sync_removed": {
        "file": "modules/llm_orchestrator.py",
        "description": "Keep placeholder env keys so groq legs make doomed calls",
        "old": "    if env_value and not is_placeholder_key(env_value):\n        return",
        "new": "    if env_value:\n        return",
        "expected": "test_placeholder_env_replaced_by_payload_key must fail",
    },
    "placeholder_exact_dropped": {
        "file": "modules/llm_orchestrator.py",
        "description": "Stop recognizing the literal api_key placeholder",
        "old": "    if lowered in PLACEHOLDER_KEY_EXACT:",
        "new": "    if False:",
        "expected": "test_placeholder_fragments_recognized must fail",
    },
    "factory_placeholder_accepted": {
        "file": "modules/llm_factory.py",
        "description": "Factory accepts placeholder keys so groq backends 401",
        "old": "    candidate = config.get(CONFIG_KEY_API_KEY)\n    if isinstance(candidate, str) and not _is_placeholder_key(candidate):\n        return candidate",
        "new": "    candidate = config.get(CONFIG_KEY_API_KEY)\n    if isinstance(candidate, str) and candidate:\n        return candidate",
        "expected": "test_model_load_failure_returns_none_not_crash must fail",
    },
    "vulnbot_chain_fallback_removed": {
        "file": "modules/vulnbot.py",
        "description": "VulnBot leaks primary error banners instead of failing over",
        "old": "        if is_error_reply(text):",
        "new": "        if False and is_error_reply(text):",
        "expected": "test_primary_error_banner_triggers_chain must fail",
    },
    "vulnbot_kb_list_format_dropped": {
        "file": "modules/vulnbot.py",
        "description": "VulnBot reads every knowledge base as a legacy dict",
        "old": "        keywords = [word for word in lowered.split() if len(word) > 2]\n        matches: list[str] = []\n        if isinstance(kb, dict):",
        "new": "        keywords = [word for word in lowered.split() if len(word) > 2]\n        matches: list[str] = []\n        if True:",
        "expected": "test_list_format_matches must fail",
    },
    "broad_unauthorized_marker_regressed": {
        "file": "modules/llm_orchestrator.py",
        "description": "Treat the word unauthorized as an error banner so pentest answers fail over",
        "old": '    "error code: 4",',
        "new": '    "unauthorized",',
        "expected": "test_pentest_prose_with_unauthorized_word_is_content must fail",
    },
    "loose_quota_marker_regressed": {
        "file": "modules/llm_orchestrator.py",
        "description": "Treat the word credit as quota exhaustion so phishing answers fail over",
        "old": '    "insufficient_quota",',
        "new": '    "credit",',
        "expected": "test_phishing_prose_with_credit_word_is_content must fail",
    },
}


def backup_files(mutations: dict, base_dir: Path) -> dict[str, str]:
    """Snapshot every mutation target before the run.

    Args:
        mutations: Mutation definitions.
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
    """Write every snapshot back to disk.

    Args:
        backups: Mapping of mutation name to original content.
        base_dir: Repository root.
        mutations: Mutation definitions.
    """
    for name, original in backups.items():
        (base_dir / mutations[name]["file"]).write_text(original)


def run_tests() -> bool:
    """Run the orchestrator contract tests.

    Returns:
        True when the whole suite passes.
    """
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "pytest",
            "tests/test_llm_orchestrator.py",
            "tests/test_vulnbot_fallback.py",
            "-q",
            "-p",
            "no:cacheprovider",
        ],
        capture_output=True,
        text=True,
        timeout=300,
    )
    return result.returncode == 0


def main() -> int:
    """Apply every mutation and verify the tests kill it.

    Returns:
        0 when every mutant is killed, 1 when any survives.
    """
    base_dir = Path(__file__).resolve().parent.parent
    backups = backup_files(MUTATIONS, base_dir)

    print("Mutation Testing — orchestrator LLM failover contract")
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
        print(
            "ALL MUTANTS KILLED — tests are robust."
            if survived == 0
            else "WARNING: mutants survived — improve test coverage."
        )
        print("=" * 60)
        return 0 if survived == 0 else 1
    finally:
        restore_files(backups, base_dir, MUTATIONS)
        if run_tests():
            print("Restored: baseline tests pass.")
        else:
            print("ERROR: restoration failed.")
            sys.exit(2)


if __name__ == "__main__":
    sys.exit(main())
