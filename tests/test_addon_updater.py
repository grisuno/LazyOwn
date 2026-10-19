"""Lazyaddon update BDD contract: opt-in, path-safe, dirty-tree aware.

Every scenario states Given, When, Then. Real git repositories prove the
fast-forward path; the shipped catalogue proves every addon opted in.
"""

from __future__ import annotations

import subprocess
from pathlib import Path

import yaml

from modules.addon_updater import load_addons, update_addon, update_all


def _git(cwd: Path, *args: str) -> subprocess.CompletedProcess:
    """Run git with a deterministic identity for tests."""
    env = {
        "GIT_AUTHOR_NAME": "Test",
        "GIT_AUTHOR_EMAIL": "test@example.com",
        "GIT_COMMITTER_NAME": "Test",
        "GIT_COMMITTER_EMAIL": "test@example.com",
        "PATH": "/usr/bin:/bin",
    }
    return subprocess.run(["git", "-C", str(cwd), *args], capture_output=True, text=True, env=env, check=True)


def _repo_with_remote(tmp_path: Path) -> tuple[Path, Path]:
    """Create a bare remote, a seed clone and a working clone."""
    remote = tmp_path / "remote.git"
    seed = tmp_path / "seed"
    work = tmp_path / "work"
    subprocess.run(["git", "init", "--bare", str(remote)], capture_output=True, check=True)
    subprocess.run(["git", "clone", str(remote), str(seed)], capture_output=True, check=True)
    _git(seed, "config", "user.email", "test@example.com")
    _git(seed, "config", "user.name", "Test")
    (seed / "payload.txt").write_text("one\n", encoding="utf-8")
    _git(seed, "add", "payload.txt")
    _git(seed, "commit", "-m", "one")
    _git(seed, "push", "origin", "HEAD")
    subprocess.run(["git", "clone", str(remote), str(work)], capture_output=True, check=True)
    return seed, work


def _addon(path: Path, *, update: bool = True, install_path: str = "work", repo_url: str = "https://example.invalid/repo.git") -> None:
    """Write one addon YAML."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        yaml.safe_dump(
            {
                "name": path.stem,
                "enabled": True,
                "update": update,
                "tool": {"repo_url": repo_url, "install_path": install_path, "execute_command": "true"},
            }
        ),
        encoding="utf-8",
    )


def test_every_shipped_addon_opts_in():
    """Given the catalogue, When loaded, Then every addon opts in unless it has no git repo."""
    addons = load_addons()
    assert len(addons) >= 180
    assert all(
        item["update"] is True or not str((item.get("tool") or {}).get("repo_url", "") or "").strip()
        for item in addons
    )


def test_update_disabled_is_skipped(tmp_path: Path):
    """Given update: false, When updated, Then git never runs."""
    addons = tmp_path / "lazyaddons"
    _addon(addons / "off.yaml", update=False)
    result = update_addon("off", lazyaddons_dir=addons, root=tmp_path)
    assert result.status == "skipped" and result.reason == "update disabled"


def test_missing_repo_url_is_skipped(tmp_path: Path):
    """Given no repo_url, When updated, Then the updater refuses."""
    addons = tmp_path / "lazyaddons"
    _addon(addons / "nourl.yaml", repo_url="")
    result = update_addon("nourl", lazyaddons_dir=addons, root=tmp_path)
    assert result.status == "skipped" and result.reason == "no repo_url"


def test_path_traversal_is_rejected(tmp_path: Path):
    """Given a traversal path, When updated, Then the install path never leaves the repository."""
    addons = tmp_path / "lazyaddons"
    _addon(addons / "evil.yaml", install_path="../outside")
    result = update_addon("evil", lazyaddons_dir=addons, root=tmp_path)
    assert result.status == "skipped" and "traversal" in result.reason


def test_repository_root_is_rejected(tmp_path: Path):
    """Given install_path '.', When updated, Then the LazyOwn tree is never pulled."""
    addons = tmp_path / "lazyaddons"
    _addon(addons / "root.yaml", install_path=".")
    result = update_addon("root", lazyaddons_dir=addons, root=tmp_path)
    assert result.status == "skipped" and result.reason == "install_path is the LazyOwn repository"


def test_not_installed_is_skipped(tmp_path: Path):
    """Given a missing install path, When updated, Then nothing is cloned over it."""
    addons = tmp_path / "lazyaddons"
    _addon(addons / "missing.yaml", install_path="missing")
    result = update_addon("missing", lazyaddons_dir=addons, root=tmp_path)
    assert result.status == "skipped" and result.reason == "not installed"


def test_fast_forward_update(tmp_path: Path):
    """Given a behind worktree, When updated, Then git fast-forwards it."""
    seed, work = _repo_with_remote(tmp_path)
    addons = tmp_path / "lazyaddons"
    _addon(addons / "work.yaml")
    (seed / "payload.txt").write_text("two\n", encoding="utf-8")
    _git(seed, "add", "payload.txt")
    _git(seed, "commit", "-m", "two")
    _git(seed, "push", "origin", "HEAD")
    result = update_addon("work", lazyaddons_dir=addons, root=tmp_path)
    assert result.status == "updated", result.reason
    assert result.after and result.after != result.before
    assert (work / "payload.txt").read_text(encoding="utf-8") == "two\n"


def test_dirty_worktree_is_skipped(tmp_path: Path):
    """Given local edits, When updated, Then the updater refuses to touch them."""
    _seed, work = _repo_with_remote(tmp_path)
    addons = tmp_path / "lazyaddons"
    _addon(addons / "dirty.yaml")
    (work / "payload.txt").write_text("local\n", encoding="utf-8")
    result = update_addon("dirty", lazyaddons_dir=addons, root=tmp_path)
    assert result.status == "skipped" and result.reason == "dirty worktree"


def test_update_all_audits_summary(tmp_path: Path):
    """Given mixed addons, When update_all runs, Then the summary and audit agree."""
    addons = tmp_path / "lazyaddons"
    _addon(addons / "on.yaml", install_path="missing")
    _addon(addons / "off.yaml", update=False)
    audit = tmp_path / "audit.jsonl"
    summary = update_all(lazyaddons_dir=addons, root=tmp_path, audit_path=audit)
    assert summary["total"] == 2
    assert summary["counts"]["skipped"] == 2
    assert audit.read_text(encoding="utf-8").strip()


def test_unknown_addon_fails(tmp_path: Path):
    """Given an unknown name, When updated, Then the result says so."""
    result = update_addon("ghost", lazyaddons_dir=tmp_path, root=tmp_path)
    assert result.status == "failed" and result.reason == "unknown addon"
