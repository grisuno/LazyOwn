"""Consolidated mutation gate for LazyOwn.

Runs the curated mutation runners under tests/ with one interface.
Each runner introduces targeted faults and requires the matching suite
to fail. A surviving mutant means the tests are too weak.

Usage:
    python scripts/mutation_gate.py --list
    python scripts/mutation_gate.py --all
    python scripts/mutation_gate.py tests/run_mutation_killchain.py
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
RUNNER_PATTERN = "run_mutation_*.py"
DEFAULT_TIMEOUT_S = 1800


def discover_runners() -> list[Path]:
    """Return sorted curated mutation runners.

    Returns:
        Sorted list of runner paths under tests/.
    """
    return sorted((REPO_ROOT / "tests").glob(RUNNER_PATTERN))


def run_runner(path: Path, timeout_s: int) -> int:
    """Execute one mutation runner.

    Args:
        path: Runner script path.
        timeout_s: Per-runner timeout in seconds.

    Returns:
        Runner exit code, 2 when the runner times out.
    """
    try:
        result = subprocess.run(
            [sys.executable, str(path)],
            cwd=str(REPO_ROOT),
            capture_output=True,
            text=True,
            check=False,
            timeout=timeout_s,
        )
    except subprocess.TimeoutExpired:
        print(f"[TIMEOUT] {path.name} after {timeout_s}s")
        return 2
    if result.stdout:
        print(result.stdout[-2000:])
    if result.returncode != 0 and result.stderr:
        print(result.stderr[-2000:])
    return result.returncode


def main(argv: list[str] | None = None) -> int:
    """Entry point for the mutation gate.

    Args:
        argv: CLI arguments, defaults to process args.

    Returns:
        Zero when every mutant is killed, nonzero otherwise.
    """
    parser = argparse.ArgumentParser(description="Run curated mutation runners.")
    parser.add_argument("--list", action="store_true", help="List available runners.")
    parser.add_argument("--all", action="store_true", help="Run every runner.")
    parser.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT_S, help="Per-runner timeout seconds.")
    parser.add_argument("runners", nargs="*", help="Explicit runner paths.")
    args = parser.parse_args(argv)

    runners = discover_runners()
    if args.list:
        for runner in runners:
            print(f"tests/{runner.name}")
        return 0

    if args.all:
        selected = runners
    elif args.runners:
        selected = [REPO_ROOT / item if not Path(item).is_absolute() else Path(item) for item in args.runners]
    else:
        print("No runners selected. Use --all, --list, or explicit paths.")
        return 2

    failures: list[str] = []
    for runner in selected:
        print(f"[MUTATION] {runner.name}")
        code = run_runner(Path(runner), args.timeout)
        status = "KILLED" if code == 0 else "SURVIVED"
        print(f"[{status}] {runner.name} exit={code}")
        if code != 0:
            failures.append(Path(runner).name)

    if failures:
        print(f"Surviving mutants in: {', '.join(failures)}")
        return 1
    print("All mutants killed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
