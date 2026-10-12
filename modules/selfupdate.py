"""Guarded self-update for the LazyOwn working tree.

``check`` fetches the configured branch and reports how far behind the
tree is; ``apply`` only fast-forwards when the tree is clean and has no
local commits, never runs remote code beyond a merge and never touches
the branch without ``--yes``. The loop runs a throttled ``check`` (once
a day) and reports an activity line when an update is available.
"""

from __future__ import annotations

import hashlib
import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DEFAULT_BRANCH = "dev"
GIT_TIMEOUT_SEC = 120


@dataclass(frozen=True)
class ReleaseArtifact:
    """One release candidate: bytes plus their expected digest.

    Attributes:
        data: Raw binary payload.
        sha256: Expected lowercase hex digest of ``data``.
        version: Human version label carried into logs.
    """

    data: bytes
    sha256: str
    version: str = ""


class Updater:
    """Verify, stage and roll back a single binary path.

    Used by the guarded self-update path for release artifacts that are
    downloaded instead of git-merged: a bad checksum never reaches the
    live file, staging writes beside it first, and rollback restores the
    ``<name>.old`` snapshot left by the previous apply.
    """

    def __init__(self, live_path: str | Path) -> None:
        """Bind the updater to the binary that may be replaced."""
        self.live = Path(live_path)
        self.backup = self.live.with_name(self.live.name + ".old")

    def verify(self, artifact: ReleaseArtifact) -> bool:
        """Return True when the payload matches its recorded digest."""
        digest = hashlib.sha256(artifact.data).hexdigest()
        return digest == str(artifact.sha256).strip().lower()

    def stage(self, artifact: ReleaseArtifact, directory: str | Path) -> str:
        """Write a verified payload into ``directory``.

        Args:
            artifact: Verified release candidate.
            directory: Destination directory for the staged binary.

        Returns:
            Path of the staged file.

        Raises:
            ValueError: Checksum mismatch; the live binary is untouched.
        """
        if not self.verify(artifact):
            raise ValueError("checksum mismatch: artifact rejected")
        destination = Path(directory) / self.live.name
        destination.write_bytes(artifact.data)
        destination.chmod(0o755)
        return str(destination)

    def rollback(self) -> bool:
        """Restore the ``<name>.old`` snapshot over the live binary."""
        if not self.backup.exists():
            return False
        shutil.copy2(self.backup, self.live)
        return True


def _run(argv: list[str], cwd: Path, timeout: int = GIT_TIMEOUT_SEC):
    """Run one git command capturing output; injection point for tests."""
    return subprocess.run(argv, cwd=str(cwd), capture_output=True, text=True, timeout=timeout)


def _git(args: list[str], runner=None, cwd: Path | None = None, timeout: int = GIT_TIMEOUT_SEC):
    """Run ``git <args>`` in the repository root."""
    run = runner or _run
    return run(["git", *args], cwd or BASE_DIR, timeout)


def current_branch(runner=None) -> str:
    """Return the checked-out branch name (empty on failure)."""
    result = _git(["rev-parse", "--abbrev-ref", "HEAD"], runner=runner)
    return str(getattr(result, "stdout", "") or "").strip()


def dirty(runner=None) -> bool:
    """Return True when the working tree has uncommitted changes."""
    result = _git(["status", "--porcelain"], runner=runner)
    return bool(str(getattr(result, "stdout", "") or "").strip())


def check(branch: str = "", runner=None) -> dict:
    """Fetch the branch and report ahead/behind counts.

    Args:
        branch: Branch to compare (defaults to the current branch).
        runner: Injected git runner.

    Returns:
        Dict with ok, branch, behind, ahead and head hash.
    """
    target = (branch or current_branch(runner) or DEFAULT_BRANCH).strip()
    fetch = _git(["fetch", "--quiet", "origin", target], runner=runner)
    if getattr(fetch, "returncode", 1) != 0:
        return {
            "ok": False,
            "branch": target,
            "error": str(getattr(fetch, "stderr", "") or "git fetch failed").strip()[:300],
        }
    counts = _git(["rev-list", "--left-right", "--count", f"HEAD...origin/{target}"], runner=runner)
    if getattr(counts, "returncode", 1) != 0:
        return {
            "ok": False,
            "branch": target,
            "error": str(getattr(counts, "stderr", "") or "git rev-list failed").strip()[:300],
        }
    parts = str(getattr(counts, "stdout", "") or "").split()
    ahead = int(parts[0]) if len(parts) > 0 and parts[0].isdigit() else 0
    behind = int(parts[1]) if len(parts) > 1 and parts[1].isdigit() else 0
    head = str(getattr(_git(["rev-parse", "--short", "HEAD"], runner=runner), "stdout", "") or "").strip()
    return {"ok": True, "branch": target, "behind": behind, "ahead": ahead, "head": head}


def apply(branch: str = "", confirm: bool = False, runner=None) -> dict:
    """Fast-forward the tree to origin/<branch> when safe.

    Args:
        branch: Branch to update from.
        confirm: Must be True; the CLI requires ``--yes``.
        runner: Injected git runner.

    Returns:
        Dict with applied flag, reason and the check summary.
    """
    if not confirm:
        return {"applied": False, "reason": "confirmation required (--yes)"}
    if dirty(runner):
        return {"applied": False, "reason": "working tree not clean; commit or stash first"}
    info = check(branch, runner)
    if not info.get("ok"):
        return {"applied": False, "reason": info.get("error", "check failed"), **info}
    if info["ahead"] > 0:
        return {"applied": False, "reason": "local commits ahead; manual merge required", **info}
    if info["behind"] == 0:
        return {"applied": False, "reason": "already up to date", **info}
    merge = _git(["merge", "--ff-only", f"origin/{info['branch']}"], runner=runner)
    applied = getattr(merge, "returncode", 1) == 0
    reason = (
        str(getattr(merge, "stdout", "") or "").strip()
        or str(getattr(merge, "stderr", "") or "").strip()
        or ("fast-forwarded" if applied else "merge failed")
    )
    return {"applied": applied, "reason": reason[:300], **info}


__all__ = ["DEFAULT_BRANCH", "ReleaseArtifact", "Updater", "apply", "check", "current_branch", "dirty"]
