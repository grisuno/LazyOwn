"""Git update contract for lazyaddons.

An addon opts in with ``update: true``. The updater only touches an
existing git worktree inside the repository, refuses dirty trees, never
follows ``..`` or absolute install paths, never clones over a missing
directory and never runs through a shell. Every decision is audited to
``sessions/addon_updates.jsonl``.
"""

from __future__ import annotations

import json
import logging
import os
import subprocess
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

log = logging.getLogger("addon_updater")

BASE_DIR = Path(__file__).resolve().parent.parent
LAZYADDONS_DIR = BASE_DIR / "lazyaddons"
AUDIT_PATH = BASE_DIR / "sessions" / "addon_updates.jsonl"
GIT_TIMEOUT = 120
MAX_YAML_BYTES = 200_000


@dataclass
class AddonUpdateResult:
    """Outcome of one addon update attempt."""

    name: str = ""
    status: str = "skipped"
    reason: str = ""
    path: str = ""
    repo_url: str = ""
    branch: str = ""
    before: str = ""
    after: str = ""
    duration_ms: float = 0.0

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-serializable view."""
        return {
            "name": self.name,
            "status": self.status,
            "reason": self.reason,
            "path": self.path,
            "repo_url": self.repo_url,
            "branch": self.branch,
            "before": self.before,
            "after": self.after,
            "duration_ms": round(self.duration_ms, 2),
        }


def _read_addon(path: Path) -> dict:
    """Read one addon YAML with a size cap."""
    try:
        if not path.is_file() or path.stat().st_size > MAX_YAML_BYTES:
            return {}
        data = yaml.safe_load(path.read_text(encoding="utf-8", errors="replace"))
    except Exception as exc:
        log.debug("addon unreadable %s: %s", path, exc)
        return {}
    return data if isinstance(data, dict) else {}


def load_addons(lazyaddons_dir: Path | str = LAZYADDONS_DIR) -> list[dict]:
    """Load every lazyaddon with its update metadata.

    Args:
        lazyaddons_dir: Directory holding one YAML per addon.

    Returns:
        List of mappings with name, path, enabled, update, repo_url and
        install_path.
    """
    directory = Path(lazyaddons_dir)
    out: list[dict] = []
    for path in sorted(directory.glob("*.yaml")):
        data = _read_addon(path)
        if not data:
            continue
        tool = data.get("tool") or {}
        if not isinstance(tool, dict):
            tool = {}
        out.append(
            {
                "name": str(data.get("name", path.stem) or path.stem),
                "file": path.stem,
                "path": path,
                "enabled": bool(data.get("enabled", True)),
                "update": bool(data.get("update", False)),
                "repo_url": str(tool.get("repo_url", "") or ""),
                "install_path": str(tool.get("install_path", "") or ""),
                "install_type": str(data.get("install_type", "") or ""),
            }
        )
    return out


def _safe_target(install_path: str, root: Path) -> tuple[Path | None, str]:
    """Resolve an install path inside the repository.

    Args:
        install_path: Declared relative path.
        root: Repository root.

    Returns:
        Tuple of resolved path (or None) and a rejection reason.
    """
    text = str(install_path or "").strip()
    if not text:
        return None, "empty install_path"
    candidate = Path(text)
    if candidate.is_absolute():
        return None, "absolute install_path"
    if ".." in candidate.parts:
        return None, "install_path traversal"
    try:
        resolved = (root / candidate).resolve()
        resolved.relative_to(root.resolve())
    except (OSError, ValueError):
        return None, "install_path escapes repository"
    if resolved == root.resolve():
        return None, "install_path is the LazyOwn repository"
    return resolved, ""


def _git(path: Path, *args: str, timeout: int = GIT_TIMEOUT) -> subprocess.CompletedProcess:
    """Run git without a shell and without interactive prompts."""
    env = dict(os.environ)
    env["GIT_TERMINAL_PROMPT"] = "0"
    env["GIT_ASKPASS"] = "/bin/true"
    return subprocess.run(
        ["git", "-C", str(path), *args],
        capture_output=True,
        text=True,
        timeout=timeout,
        env=env,
        check=False,
    )


def _worktree_root(path: Path, repository_root: Path) -> tuple[Path | None, str]:
    """Return the git worktree root for a path, or a reason."""
    if not path.is_dir():
        return None, "not installed"
    try:
        result = _git(path, "rev-parse", "--show-toplevel")
    except (OSError, subprocess.SubprocessError) as exc:
        return None, f"git unavailable: {exc}"
    if result.returncode != 0:
        return None, "not a git worktree"
    root = Path(result.stdout.strip()).resolve()
    if root == repository_root.resolve():
        return None, "part of the LazyOwn repository"
    return root, ""


def update_addon(
    name: str,
    lazyaddons_dir: Path | str = LAZYADDONS_DIR,
    root: Path | str = BASE_DIR,
    dry_run: bool = False,
) -> AddonUpdateResult:
    """Update one addon through ``git pull --ff-only``.

    Args:
        name: Addon name or filename stem.
        lazyaddons_dir: Addon directory.
        root: Repository root.
        dry_run: Report what would happen without pulling.

    Returns:
        Structured result. Never raises for expected conditions.
    """
    started = time.time()
    wanted = str(name or "").strip()
    addons = load_addons(lazyaddons_dir)
    entry = next(
        (item for item in addons if item["name"] == wanted or item["file"] == wanted),
        None,
    )
    if entry is None:
        return AddonUpdateResult(name=wanted, status="failed", reason="unknown addon")
    result = AddonUpdateResult(name=entry["name"], repo_url=entry["repo_url"])
    if not entry["update"]:
        result.reason = "update disabled"
        result.duration_ms = (time.time() - started) * 1000
        return result
    if not entry["enabled"]:
        result.reason = "addon disabled"
        result.duration_ms = (time.time() - started) * 1000
        return result
    if not entry["repo_url"]:
        result.reason = "no repo_url"
        result.duration_ms = (time.time() - started) * 1000
        return result
    target, reason = _safe_target(entry["install_path"], Path(root))
    if target is None:
        result.reason = reason
        result.duration_ms = (time.time() - started) * 1000
        return result
    result.path = str(target)
    worktree, reason = _worktree_root(target, Path(root))
    if worktree is None:
        result.reason = reason
        result.duration_ms = (time.time() - started) * 1000
        return result
    try:
        branch_result = _git(worktree, "rev-parse", "--abbrev-ref", "HEAD")
        before_result = _git(worktree, "rev-parse", "HEAD")
        status_result = _git(worktree, "status", "--porcelain")
    except (OSError, subprocess.SubprocessError) as exc:
        result.status = "failed"
        result.reason = f"git unavailable: {exc}"
        result.duration_ms = (time.time() - started) * 1000
        return result
    result.branch = branch_result.stdout.strip()
    result.before = before_result.stdout.strip()[:12]
    if status_result.stdout.strip():
        result.reason = "dirty worktree"
        result.duration_ms = (time.time() - started) * 1000
        return result
    if result.branch in ("", "HEAD"):
        result.reason = "detached HEAD"
        result.duration_ms = (time.time() - started) * 1000
        return result
    if dry_run:
        result.status = "dry-run"
        result.reason = f"would pull {result.branch}"
        result.duration_ms = (time.time() - started) * 1000
        return result
    try:
        pull = _git(worktree, "pull", "--ff-only")
    except (OSError, subprocess.SubprocessError) as exc:
        result.status = "failed"
        result.reason = f"git unavailable: {exc}"
        result.duration_ms = (time.time() - started) * 1000
        return result
    if pull.returncode != 0:
        result.status = "failed"
        result.reason = (pull.stderr or pull.stdout or "git pull failed").strip()[:300]
        result.duration_ms = (time.time() - started) * 1000
        return result
    after_result = _git(worktree, "rev-parse", "HEAD")
    result.after = after_result.stdout.strip()[:12]
    result.status = "updated" if result.after != result.before else "skipped"
    result.reason = "already current" if result.status == "skipped" else "fast-forward"
    result.duration_ms = (time.time() - started) * 1000
    return result


def update_all(
    names: list[str] | None = None,
    lazyaddons_dir: Path | str = LAZYADDONS_DIR,
    root: Path | str = BASE_DIR,
    dry_run: bool = False,
    audit_path: Path | str = AUDIT_PATH,
) -> dict[str, Any]:
    """Update every opted-in addon or an explicit name list.

    Args:
        names: Optional names; empty means every addon.
        lazyaddons_dir: Addon directory.
        root: Repository root.
        dry_run: Report without pulling.
        audit_path: JSONL audit destination.

    Returns:
        Summary with results and counts.
    """
    entries = load_addons(lazyaddons_dir)
    if names:
        wanted = {str(name).strip() for name in names if str(name).strip()}
        entries = [item for item in entries if item["name"] in wanted or item["file"] in wanted]
    results: list[AddonUpdateResult] = []
    seen_paths: dict[str, str] = {}
    for item in entries:
        install_path = str(item.get("install_path", "") or "")
        if install_path and install_path in seen_paths:
            results.append(
                AddonUpdateResult(
                    name=item["name"],
                    status="skipped",
                    reason=f"shares install path with {seen_paths[install_path]}",
                    repo_url=str(item.get("repo_url", "") or ""),
                )
            )
            continue
        if install_path:
            seen_paths[install_path] = str(item["name"])
        results.append(
            update_addon(item["name"], lazyaddons_dir=lazyaddons_dir, root=root, dry_run=dry_run)
        )
    counts: dict[str, int] = {}
    for result in results:
        counts[result.status] = counts.get(result.status, 0) + 1
    summary = {
        "total": len(results),
        "counts": counts,
        "dry_run": bool(dry_run),
        "results": [result.to_dict() for result in results],
    }
    _audit(summary, audit_path)
    return summary


def _audit(summary: dict, path: Path | str) -> None:
    """Append one update summary to the audit ledger."""
    try:
        target = Path(path)
        target.parent.mkdir(parents=True, exist_ok=True)
        row = {"ts": time.strftime("%Y-%m-%dT%H:%M:%S"), **summary}
        with target.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")
    except Exception as exc:
        log.debug("addon update audit skipped: %s", exc)


__all__ = [
    "AddonUpdateResult",
    "AUDIT_PATH",
    "GIT_TIMEOUT",
    "LAZYADDONS_DIR",
    "load_addons",
    "update_addon",
    "update_all",
]
