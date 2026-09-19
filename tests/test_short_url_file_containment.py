"""Containment contract for short-URL file serving.

SDD contract: ``resolve_contained_file_path`` accepts a ``file://`` URL or a
bare filesystem path and returns the canonical path only when it stays
within the sessions base directory. Anything else (remote URLs, traversal,
symlink escape, absolute paths outside the base) returns ``None`` so the
``/<short_url>`` route fails closed with 404 instead of disclosing
arbitrary local files.
"""

from __future__ import annotations

import ast
from pathlib import Path

import pytest

from lazyc2.security.validators import resolve_contained_file_path

REPO_ROOT = Path(__file__).resolve().parent.parent
LAZYC2 = REPO_ROOT / "lazyc2.py"


@pytest.fixture()
def sessions_dir(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    monkeypatch.chdir(tmp_path)
    base = tmp_path / "sessions"
    base.mkdir()
    (base / "payload.exe").write_bytes(b"implant")
    (base / "sub").mkdir()
    (base / "sub" / "note.txt").write_text("hi")
    return base


class TestContainedPaths:
    def test_bare_relative_inside_base(self, sessions_dir: Path) -> None:
        resolved = resolve_contained_file_path("sessions/payload.exe", sessions_dir)
        assert resolved == (sessions_dir / "payload.exe").resolve()

    def test_absolute_inside_base(self, sessions_dir: Path) -> None:
        target = str(sessions_dir / "sub" / "note.txt")
        assert resolve_contained_file_path(target, sessions_dir) == Path(target).resolve()

    def test_file_scheme_inside_base(self, sessions_dir: Path) -> None:
        target = sessions_dir / "payload.exe"
        resolved = resolve_contained_file_path(f"file://{target}", sessions_dir)
        assert resolved == target.resolve()


class TestRejectedPaths:
    def test_remote_url_rejected(self, sessions_dir: Path) -> None:
        assert resolve_contained_file_path("https://evil.example/x", sessions_dir) is None

    def test_absolute_outside_rejected(self, sessions_dir: Path) -> None:
        assert resolve_contained_file_path("/etc/passwd", sessions_dir) is None

    def test_file_scheme_outside_rejected(self, sessions_dir: Path) -> None:
        assert resolve_contained_file_path("file:///etc/passwd", sessions_dir) is None

    def test_traversal_rejected(self, sessions_dir: Path) -> None:
        assert resolve_contained_file_path("sessions/../../etc/passwd", sessions_dir) is None

    def test_symlink_escape_rejected(self, sessions_dir: Path, tmp_path: Path) -> None:
        outside = tmp_path / "secret.txt"
        outside.write_text("secret")
        link = sessions_dir / "link.txt"
        try:
            link.symlink_to(outside)
        except OSError:
            pytest.skip("symlinks not permitted")
        assert resolve_contained_file_path(str(link), sessions_dir) is None

    def test_empty_rejected(self, sessions_dir: Path) -> None:
        assert resolve_contained_file_path("", sessions_dir) is None


class TestRouteStatusContract:
    """``redirect_to_file`` must let ``abort()`` propagate as HTTP status.

    A bare ``except Exception`` swallows ``abort(404)`` and turns it into
    500, so victims and operators cannot distinguish dead links from
    server errors. The route must re-raise ``HTTPException``.
    """

    def test_abort_propagates(self) -> None:
        tree = ast.parse(LAZYC2.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef) and node.name == "redirect_to_file":
                handlers = [
                    n for n in ast.walk(node) if isinstance(n, ast.ExceptHandler)
                ]
                reraises = any(
                    (h.type.attr == "HTTPException" if isinstance(h.type, ast.Attribute) else h.type.id == "HTTPException")
                    for h in handlers
                    if h.type is not None
                )
                assert reraises, "redirect_to_file must re-raise HTTPException"
                return
        pytest.fail("redirect_to_file not found")
