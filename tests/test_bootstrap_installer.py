"""Integration tests for the installer scripts (no network, no apt).

Exercises ``bootstrap.sh`` and ``install.sh`` end to end with local
``file://`` git fixtures and stub payloads, so the one-liner flows are
covered in CI without touching the real ``~/LazyOwn`` or package managers.
"""

from __future__ import annotations

import os
import shutil
import stat
import subprocess
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
BOOTSTRAP = REPO_ROOT / "bootstrap.sh"
INSTALL = REPO_ROOT / "install.sh"

GIT = shutil.which("git")
BASH = shutil.which("bash")

needs_git = pytest.mark.skipif(GIT is None, reason="git is required")
needs_bash = pytest.mark.skipif(BASH is None, reason="bash is required")


def _run_bootstrap(args: list[str], env: dict[str, str], cwd: Path) -> subprocess.CompletedProcess[str]:
    full_env = dict(os.environ)
    full_env.update(env)
    full_env.pop("LAZYOWN_PROFILE", None)
    return subprocess.run(
        [BASH, str(BOOTSTRAP), *args],
        capture_output=True,
        text=True,
        timeout=60,
        cwd=cwd,
        env=full_env,
        stdin=subprocess.DEVNULL,
    )


def _git(args: list[str], cwd: Path) -> None:
    subprocess.run(
        [GIT, "-c", "user.email=test@test", "-c", "user.name=test", *args],
        check=True,
        capture_output=True,
        cwd=cwd,
        timeout=60,
    )


@needs_bash
def test_bootstrap_help_lists_options() -> None:
    proc = subprocess.run([BASH, str(BOOTSTRAP), "--help"], capture_output=True, text=True, timeout=30)
    assert proc.returncode == 0
    for flag in ("--dir", "--branch", "--with-tools", "--profile", "--existing", "--run-mode", "--no-run", "--debug"):
        assert flag in proc.stdout


@needs_bash
def test_bootstrap_rejects_unknown_flag() -> None:
    proc = subprocess.run(
        [BASH, str(BOOTSTRAP), "--bogus"],
        capture_output=True,
        text=True,
        timeout=30,
        stdin=subprocess.DEVNULL,
    )
    assert proc.returncode != 0


@needs_bash
def test_bootstrap_rejects_bad_modes() -> None:
    for flag in (["--existing", "bogus"], ["--run-mode", "bogus"]):
        proc = subprocess.run(
            [BASH, str(BOOTSTRAP), *flag],
            capture_output=True,
            text=True,
            timeout=30,
            stdin=subprocess.DEVNULL,
        )
        assert proc.returncode != 0


@needs_bash
def test_install_pipe_guard(tmp_path: Path) -> None:
    """install.sh outside a checkout must refuse and point at bootstrap."""
    lonely = tmp_path / "lonely"
    lonely.mkdir()
    shutil.copy2(INSTALL, lonely / "install.sh")
    proc = subprocess.run(
        [BASH, str(lonely / "install.sh")],
        capture_output=True,
        text=True,
        timeout=30,
        cwd=lonely,
        stdin=subprocess.DEVNULL,
    )
    assert proc.returncode == 2
    assert "bootstrap.sh" in proc.stderr


def _make_stub_repo(path: Path) -> None:
    path.mkdir(parents=True)
    (path / "install.sh").write_text("#!/usr/bin/env bash\necho STUB_INSTALL_OK\n", encoding="utf-8")
    (path / "payload.example.json").write_text("{}\n", encoding="utf-8")
    for name in ("run", "fast_run_as_r00t.sh", "bootstrap.sh"):
        (path / name).write_text("x\n", encoding="utf-8")
    _git(["init", "-q", "-b", "main", "."], path)
    _git(["add", "-A"], path)
    _git(["commit", "-qm", "init"], path)


@needs_git
@needs_bash
def test_existing_checkout_abort_changes_nothing(tmp_path: Path) -> None:
    _make_stub_repo(tmp_path / "stub")
    target = tmp_path / "LazyOwn"
    subprocess.run([GIT, "clone", "-q", f"file://{tmp_path / 'stub'}", str(target)], check=True, timeout=60)
    marker = target / "operator-note.txt"
    marker.write_text("untouched\n", encoding="utf-8")
    proc = _run_bootstrap(
        ["--existing", "abort", "--no-run"],
        {"LAZYOWN_DIR": str(target), "LAZYOWN_REPO": f"file://{tmp_path / 'stub'}", "TERM": "dumb"},
        tmp_path,
    )
    assert proc.returncode == 0
    assert "Aborted" in proc.stdout
    assert "Checking for an existing install" in proc.stdout
    assert "Found an existing LazyOwn checkout." in proc.stdout
    assert marker.read_text(encoding="utf-8") == "untouched\n"


@needs_git
@needs_bash
def test_debug_flag_traces_execution(tmp_path: Path) -> None:
    _make_stub_repo(tmp_path / "stub")
    target = tmp_path / "LazyOwn"
    subprocess.run([GIT, "clone", "-q", f"file://{tmp_path / 'stub'}", str(target)], check=True, timeout=60)
    proc = _run_bootstrap(
        ["--debug", "--existing", "abort", "--no-run"],
        {"LAZYOWN_DIR": str(target), "LAZYOWN_REPO": f"file://{tmp_path / 'stub'}", "TERM": "dumb"},
        tmp_path,
    )
    assert proc.returncode == 0
    assert "resolve_target_dir" in proc.stderr


@needs_git
@needs_bash
def test_existing_checkout_update_reinstalls(tmp_path: Path) -> None:
    _make_stub_repo(tmp_path / "stub")
    target = tmp_path / "LazyOwn"
    subprocess.run([GIT, "clone", "-q", f"file://{tmp_path / 'stub'}", str(target)], check=True, timeout=60)
    (target / "payload.json").write_text('{"k": "v"}\n', encoding="utf-8")
    proc = _run_bootstrap(
        ["--existing", "update", "--run-mode", "none"],
        {"LAZYOWN_DIR": str(target), "LAZYOWN_REPO": f"file://{tmp_path / 'stub'}", "TERM": "dumb"},
        tmp_path,
    )
    assert proc.returncode == 0
    assert "STUB_INSTALL_OK" in proc.stdout
    assert (target / "payload.json").read_text(encoding="utf-8") == '{"k": "v"}\n'


@needs_git
@needs_bash
def test_existing_checkout_clean_backs_up_payload(tmp_path: Path) -> None:
    _make_stub_repo(tmp_path / "stub")
    target = tmp_path / "LazyOwn"
    subprocess.run([GIT, "clone", "-q", f"file://{tmp_path / 'stub'}", str(target)], check=True, timeout=60)
    (target / "payload.json").write_text('{"k": "v"}\n', encoding="utf-8")
    backups = tmp_path / "backups"
    backups.mkdir()
    proc = _run_bootstrap(
        ["--existing", "clean", "--run-mode", "none"],
        {
            "LAZYOWN_DIR": str(target),
            "LAZYOWN_REPO": f"file://{tmp_path / 'stub'}",
            "LAZYOWN_BACKUP_DIR": str(backups),
            "TERM": "dumb",
        },
        tmp_path,
    )
    assert proc.returncode == 0
    assert "STUB_INSTALL_OK" in proc.stdout
    saved = list(backups.glob("lazyown-payload-backup-*.json"))
    assert len(saved) == 1
    assert "k" in saved[0].read_text(encoding="utf-8")


@needs_bash
def test_non_checkout_path_fails_without_tty(tmp_path: Path) -> None:
    plain = tmp_path / "plain"
    plain.mkdir()
    proc = _run_bootstrap(
        ["--run-mode", "none"],
        {"LAZYOWN_DIR": str(plain), "TERM": "dumb"},
        tmp_path,
    )
    assert proc.returncode != 0
    assert "not a git checkout" in proc.stderr


@needs_bash
def test_install_uses_supported_pip_flags() -> None:
    """install.sh must not pass pip options removed from modern pip.

    ``--resolver`` was dropped by pip, which turned the pinned lock
    install into a guaranteed failure (silent fallback to unpinned
    packages). Caught by a real install run.
    """
    text = (REPO_ROOT / "install.sh").read_text(encoding="utf-8")
    assert "--resolver" not in text


@needs_bash
def test_scripts_are_executable_and_clean() -> None:
    for script in (BOOTSTRAP, INSTALL, REPO_ROOT / "scripts" / "publish_wiki.sh"):
        assert script.is_file()
        assert script.stat().st_mode & stat.S_IXUSR, f"{script} is not executable"
