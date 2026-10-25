#!/usr/bin/env python3
"""Sync community Nuclei template collections into the LazyOwn marketplace.

Clones each registered source into a temporary staging directory, removes
every ``.git`` trace to avoid mixed-repository contamination, then replaces
the canonical destination with the fresh working tree.

New template collections are registered in ``SOURCES`` (skill
``/marketplace-contributor`` Step 4c). Single-file tools, implants, and
runnable scanners are NOT sources here; they ship as plain lazyaddons.

Usage:
    python3 nuclei_templates_sync.py
    python3 nuclei_templates_sync.py --source nuclei-templates --refresh-existing
    python3 nuclei_templates_sync.py --source nuclei-templates --dest ~/nuclei-templates
"""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

SOURCES: dict[str, dict[str, str]] = {
    "nuclei-templates": {
        "repo": "https://github.com/projectdiscovery/nuclei-templates.git",
        "subdir": "nuclei-templates",
        "validate_subset": str(Path("http") / "cves"),
    },
}
MIN_EXPECTED_TEMPLATES = 1000
CLONE_TIMEOUT = 600
VALIDATE_TIMEOUT = 120


def repo_root() -> Path:
    """Return the LazyOwn repository root derived from this file location.

    Returns:
        Repository root path (parent of the ``modules/`` directory).
    """
    return Path(__file__).resolve().parent.parent


def canonical_dest(subdir: str) -> Path:
    """Return the canonical marketplace destination for a source.

    Args:
        subdir: Source subdirectory under ``external/.exploit``.

    Returns:
        ``<repo>/external/.exploit/<subdir>`` path.
    """
    return repo_root() / "external" / ".exploit" / subdir


def run(argv: list[str], cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
    """Run a subprocess capturing output as text without raising.

    Args:
        argv: Command and arguments to execute.
        cwd: Optional working directory.

    Returns:
        Completed process handle with captured stdout and stderr.
    """
    return subprocess.run(argv, cwd=str(cwd) if cwd else None, capture_output=True, text=True, check=False)


def ensure_git_available() -> None:
    """Abort with a clear message when the git binary is missing.

    Raises:
        SystemExit: Always raised with code 1 when git is not on PATH.
    """
    if shutil.which("git") is None:
        print("ERROR: git binary not found on PATH.", file=sys.stderr)
        raise SystemExit(1)


def clone_templates(repo: str, staging: Path) -> tuple[Path, str]:
    """Shallow-clone the template repository into the staging directory.

    Args:
        repo: Git URL of the template collection.
        staging: Empty staging directory that receives the clone.

    Returns:
        Tuple of the cloned tree path and its HEAD commit hash.

    Raises:
        SystemExit: Raised with code 1 when the clone fails.
    """
    tree = staging / "repo"
    proc = subprocess.run(
        ["git", "clone", "--depth", "1", repo, str(tree)],
        capture_output=True,
        text=True,
        check=False,
        timeout=CLONE_TIMEOUT,
    )
    if proc.returncode != 0 or not tree.is_dir():
        print(f"ERROR: git clone failed for {repo}.", file=sys.stderr)
        print(proc.stderr.strip()[-500:], file=sys.stderr)
        raise SystemExit(1)
    head = run(["git", "rev-parse", "--short", "HEAD"], cwd=tree)
    return tree, head.stdout.strip()


def strip_git_traces(tree: Path) -> int:
    """Remove every .git file or directory under the staged tree.

    Args:
        tree: Staged working tree to clean.

    Returns:
        Number of .git traces removed.
    """
    removed = 0
    for candidate in list(tree.rglob(".git")):
        if candidate.is_dir() and not candidate.is_symlink():
            shutil.rmtree(candidate, ignore_errors=True)
        else:
            candidate.unlink(missing_ok=True)
        removed += 1
    return removed


def count_templates(tree: Path) -> int:
    """Count Nuclei template files under a directory tree.

    Args:
        tree: Directory tree to scan.

    Returns:
        Number of ``*.yaml`` files found.
    """
    return sum(1 for _ in tree.glob("**/*.yaml"))


def replace_dest(src: Path, dest: Path, expected: str) -> None:
    """Atomically replace the destination with the staged tree contents.

    Args:
        src: Staged clean tree acting as the source.
        dest: Destination directory to replace.
        expected: Expected destination directory name guard.

    Raises:
        SystemExit: Raised with code 1 when the destination name guard fails
            or the staged tree holds fewer templates than expected.
    """
    if dest.name != expected:
        print(f"ERROR: refusing to replace unexpected destination {dest}.", file=sys.stderr)
        raise SystemExit(1)
    total = count_templates(src)
    if total < MIN_EXPECTED_TEMPLATES:
        print(f"ERROR: staged tree holds only {total} templates, aborting.", file=sys.stderr)
        raise SystemExit(1)
    if dest.exists():
        shutil.rmtree(dest)
    shutil.copytree(src, dest)


def same_remote(path: Path, repo: str) -> bool:
    """Check whether an existing clone points at the expected remote.

    Args:
        path: Local clone to inspect.
        repo: Expected upstream repository URL.

    Returns:
        True when the clone origin matches the expected remote.
    """

    def normalize(url: str) -> str:
        return url.strip().rstrip("/").removesuffix(".git")

    proc = run(["git", "-C", str(path), "remote", "get-url", "origin"])
    if proc.returncode != 0:
        return False
    return normalize(proc.stdout) == normalize(repo)


def refresh_existing_clone(path: Path, repo: str) -> bool:
    """Fast-forward an existing clean clone of the same remote.

    Args:
        path: Local clone candidate.
        repo: Expected upstream repository URL.

    Returns:
        True when the clone was fast-forwarded successfully.
    """
    if not (path / ".git").exists():
        return False
    status = run(["git", "-C", str(path), "status", "--porcelain"])
    if status.returncode != 0 or status.stdout.strip():
        return False
    if not same_remote(path, repo):
        return False
    pull = run(["git", "-C", str(path), "pull", "--ff-only"])
    return pull.returncode == 0


def validate_subset(dest: Path, subset: str) -> bool | None:
    """Validate a template subset with the nuclei binary when available.

    Args:
        dest: Destination directory holding the synced templates.
        subset: Relative subset directory to validate.

    Returns:
        True on success, False on validation failure, None when the nuclei
        binary or the subset directory is unavailable.
    """
    if shutil.which("nuclei") is None:
        return None
    subset_path = dest / subset
    if not subset_path.is_dir():
        return None
    try:
        proc = subprocess.run(
            ["nuclei", "-t", str(subset_path), "-validate", "-silent"],
            capture_output=True,
            text=True,
            check=False,
            timeout=VALIDATE_TIMEOUT,
        )
    except (OSError, subprocess.TimeoutExpired):
        return False
    return proc.returncode == 0


def build_parser() -> argparse.ArgumentParser:
    """Build the command line parser for the sync script.

    Returns:
        Configured argument parser.
    """
    parser = argparse.ArgumentParser(description="Sync Nuclei template sources into the LazyOwn marketplace.")
    parser.add_argument(
        "--source",
        action="append",
        default=[],
        choices=sorted(SOURCES),
        help="Source to sync (repeatable, default: all registered sources).",
    )
    parser.add_argument("--repo", default="", help="Override the source git URL (single source only).")
    parser.add_argument("--dest", default="", help="Override the destination directory (single source only).")
    parser.add_argument(
        "--refresh-existing",
        action="store_true",
        help="Fast-forward existing clean clones of the same remote too.",
    )
    parser.add_argument("--skip-validate", action="store_true", help="Skip nuclei -validate check.")
    return parser


def sync(name: str, repo: str, dest: Path, refresh_existing: bool, skip_validate: bool) -> dict[str, object]:
    """Clone, clean, and install one template source.

    Args:
        name: Registered source name.
        repo: Template collection git URL.
        dest: Destination directory to replace.
        refresh_existing: Fast-forward existing clean clones as well.
        skip_validate: Skip the nuclei validation step.

    Returns:
        Summary dictionary with source, commit, counts, destination,
        refreshed clones, removed git traces, and validation outcome.
    """
    ensure_git_available()
    subdir = SOURCES[name]["subdir"]
    with tempfile.TemporaryDirectory(prefix=f"{subdir}-ingest-") as tmp:
        tree, commit = clone_templates(repo, Path(tmp))
        removed = strip_git_traces(tree)
        total = count_templates(tree)
        replace_dest(tree, dest, subdir)
    refreshed: list[str] = []
    if refresh_existing:
        candidates = {(repo_root().parent / subdir).resolve(), (Path.home() / subdir).resolve()}
        for candidate in sorted(candidates):
            if candidate == dest.resolve():
                continue
            if refresh_existing_clone(candidate, repo):
                refreshed.append(str(candidate))
    validation: bool | None = None
    if not skip_validate:
        validation = validate_subset(dest, SOURCES[name]["validate_subset"])
    return {
        "source": name,
        "repo": repo,
        "commit": commit,
        "templates": count_templates(dest),
        "staged": total,
        "dest": str(dest),
        "git_traces_removed": removed,
        "refreshed": refreshed,
        "validation": validation,
    }


def resolve_plan(args: argparse.Namespace) -> list[tuple[str, str, Path]]:
    """Resolve the requested sources into (name, repo, dest) work items.

    Args:
        args: Parsed command line arguments.

    Returns:
        Work item list, one tuple per source to sync.

    Raises:
        SystemExit: Raised with code 2 on unknown sources or overrides
            combined with multiple sources.
    """
    names = args.source or sorted(SOURCES)
    unknown = [name for name in names if name not in SOURCES]
    if unknown:
        print(f"ERROR: unknown sources: {', '.join(unknown)}.", file=sys.stderr)
        raise SystemExit(2)
    if (args.repo or args.dest) and len(names) != 1:
        print("ERROR: --repo/--dest require exactly one --source.", file=sys.stderr)
        raise SystemExit(2)
    plan = []
    for name in names:
        repo = args.repo or SOURCES[name]["repo"]
        dest = Path(args.dest).expanduser() if args.dest else canonical_dest(SOURCES[name]["subdir"])
        plan.append((name, repo, dest))
    return plan


def main(argv: list[str] | None = None) -> int:
    """Entry point for the template sync script.

    Args:
        argv: Optional argument list for testing.

    Returns:
        Process exit code, 0 on success.
    """
    args = build_parser().parse_args(argv)
    code = 0
    for name, repo, dest in resolve_plan(args):
        summary = sync(name, repo, dest, args.refresh_existing, args.skip_validate)
        print(
            f"[{summary['source']}] templates synced: {summary['templates']} from {summary['repo']}@{summary['commit']}"
        )
        print(
            f"[{summary['source']}] destination: {summary['dest']} (git traces removed: {summary['git_traces_removed']})"
        )
        for path in summary["refreshed"]:
            print(f"[{summary['source']}] refreshed existing clone: {path}")
        if summary["validation"] is True:
            print(f"[{summary['source']}] validation: nuclei -validate OK")
        elif summary["validation"] is False:
            print(f"[{summary['source']}] WARNING: nuclei -validate reported errors.")
            code = 1
    return code


if __name__ == "__main__":
    raise SystemExit(main())
