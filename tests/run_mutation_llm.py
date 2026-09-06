"""Mutation runner for the LLM subsystem contract.

Applies targeted mutations to the surviving LLM modules and verifies that
``tests/test_llm_contract.py`` detects each one. A surviving mutant means the
contract test is too weak.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

MUTATIONS = {
    "factory_deepseek_identifier_corrupted": {
        "file": "modules/llm_factory.py",
        "description": "Corrupt BACKEND_DEEPSEEK value string",
        "old": 'BACKEND_DEEPSEEK = "deepseek"',
        "new": 'BACKEND_DEEPSEEK = "DEEPSEEK_CORRUPTED"',
        "expected": "test_supported_backends_are_canonical must fail",
    },
    "factory_default_backend_changed": {
        "file": "modules/llm_factory.py",
        "description": "Change DEFAULT_BACKEND away from auto",
        "old": "DEFAULT_BACKEND = BACKEND_AUTO",
        "new": 'DEFAULT_BACKEND = "groq"',
        "expected": "test_backend_constants_exposed must fail",
    },
    "factory_normalize_allows_fallback": {
        "file": "modules/llm_factory.py",
        "description": "Normalize returns fixed backend instead of DEFAULT_BACKEND",
        "old": "        return DEFAULT_BACKEND",
        "new": '        return "groq"',
        "expected": "test_normalize_falls_back_to_auto_on_empty must fail",
    },
    "client_summarize_removed": {
        "file": "modules/llm_client.py",
        "description": "Rename summarize so public API breaks",
        "old": "def summarize(",
        "new": "def summarize_broken(",
        "expected": "test_llm_client_exposes_public_api must fail",
    },
    "fallback_call_removed": {
        "file": "modules/ai_fallback.py",
        "description": "Rename call so public API breaks",
        "old": "def call(",
        "new": "def call_broken(",
        "expected": "test_ai_fallback_exposes_public_api must fail",
    },
    "fallback_detached_from_factory": {
        "file": "modules/ai_fallback.py",
        "description": "Detach ai_fallback constants from factory source of truth",
        "old": "    DEFAULT_OLLAMA_HOST as _OLLAMA_HOST,",
        "new": '    DEFAULT_OLLAMA_HOST as _OLLAMA_HOST, "x",',
        "expected": "test_ai_fallback_reads_factory_constants must fail",
    },
}


def backup_files(mutations: dict, base_dir: Path) -> dict[str, str]:
    backups = {}
    for name, info in mutations.items():
        path = base_dir / info["file"]
        if path.exists():
            backups[name] = path.read_text()
    return backups


def restore_files(backups: dict[str, str], base_dir: Path, mutations: dict) -> None:
    for name, original in backups.items():
        (base_dir / mutations[name]["file"]).write_text(original)


def run_tests() -> bool:
    result = subprocess.run(
        [sys.executable, "-m", "pytest", "tests/test_llm_contract.py", "-q"],
        capture_output=True,
        text=True,
        timeout=60,
    )
    return result.returncode == 0


def main() -> int:
    base_dir = Path(__file__).resolve().parent.parent
    backups = backup_files(MUTATIONS, base_dir)

    print("Mutation Testing — LLM subsystem contract")
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
        print("ALL MUTANTS KILLED — tests are robust." if survived == 0 else
              "WARNING: mutants survived — improve test coverage.")
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
