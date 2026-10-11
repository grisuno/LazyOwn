"""Legacy shim contract plus referenced-script existence.

SDD contract: ``modules/legacy/*.py`` must stay symlinks into
``contrib/legacy/`` (the documented shim design), never byte-copies
that can drift. Separately, every ``python3 modules/...py`` script
path embedded in migrated commands must resolve to a real file, so
commands like ``seo`` fail loudly in tests instead of at 2am during
an engagement.
"""

from __future__ import annotations

import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
LEGACY = REPO_ROOT / "modules" / "legacy"
CONTRIB = REPO_ROOT / "contrib" / "legacy"

SCRIPT_RE = re.compile(r"python3\s+(modules/[A-Za-z0-9_./-]+\.py)")


class TestLegacyShims:
    def test_no_regular_file_clones(self) -> None:
        clones = [
            p.name
            for p in sorted(LEGACY.glob("*.py"))
            if p.name != "__init__.py" and not p.is_symlink()
        ]
        assert not clones, f"must stay symlinks, found copies: {clones}"

    def test_symlinks_resolve_into_contrib(self) -> None:
        for link in sorted(LEGACY.glob("*.py")):
            if link.name == "__init__.py" or not link.is_symlink():
                continue
            target = link.resolve()
            assert CONTRIB.resolve() in target.parents, (
                f"{link.name} must resolve inside contrib/legacy, got {target}"
            )
            assert target.exists(), f"{link.name} is a dangling symlink"


class TestReferencedScriptsExist:
    def test_exploit_migrated_script_paths(self) -> None:
        source = (REPO_ROOT / "cli" / "commands" / "exploit_migrated.py").read_text(
            encoding="utf-8"
        )
        missing = [
            path
            for path in sorted(set(SCRIPT_RE.findall(source)))
            if not (REPO_ROOT / path).exists()
        ]
        assert not missing, f"referenced scripts missing on disk: {missing}"
