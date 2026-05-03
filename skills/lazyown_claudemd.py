#!/usr/bin/env python3
"""
LazyOwn CLAUDE.md Hierarchical Loader (Claude Code style)

4-level hierarchy (highest → lowest priority):
  1. managed  — /etc/lazyown/CLAUDE.md         (system policy, read-only)
  2. user     — ~/.lazyown/CLAUDE.md            (user preferences)
  3. project  — ./CLAUDE.md, ./.lazyown/CLAUDE.md, ./.lazyown/rules/*.md
  4. local    — ./CLAUDE.local.md               (gitignored, machine-specific)

All levels are merged into a single instructions string passed to the LLM.
Only project and local files are scanned per session (path-sensitive).
"""

from pathlib import Path
from typing import Optional


_MANAGED_PATH  = Path("/etc/lazyown/CLAUDE.md")
_USER_PATH     = Path.home() / ".lazyown" / "CLAUDE.md"
_LOCAL_SUFFIX  = "CLAUDE.local.md"
_PROJECT_FILES = ["CLAUDE.md", ".lazyown/CLAUDE.md"]
_RULES_GLOB    = ".lazyown/rules/*.md"


class ClaudeMdLoader:
    """
    Load and merge CLAUDE.md instructions from all hierarchy levels.

    Lazy-loads rules directory only when the current working directory
    contains it (avoids scanning unrelated paths).
    """

    def __init__(self, cwd: Optional[Path] = None):
        self.cwd = cwd or Path.cwd()

    def load(self) -> str:
        """Return merged instructions string from all applicable levels."""
        sections: list[tuple[str, str]] = []

        # Level 1: managed (system)
        if _MANAGED_PATH.exists():
            try:
                sections.append(("MANAGED", _MANAGED_PATH.read_text()))
            except OSError:
                pass

        # Level 2: user
        if _USER_PATH.exists():
            try:
                sections.append(("USER", _USER_PATH.read_text()))
            except OSError:
                pass

        # Level 3a: project files
        for rel in _PROJECT_FILES:
            p = self.cwd / rel
            if p.exists():
                try:
                    sections.append((f"PROJECT:{rel}", p.read_text()))
                except OSError:
                    pass

        # Level 3b: rules directory (lazy — only if it exists)
        rules_dir = self.cwd / ".lazyown" / "rules"
        if rules_dir.is_dir():
            for rule_file in sorted(rules_dir.glob("*.md")):
                try:
                    sections.append((f"RULE:{rule_file.stem}", rule_file.read_text()))
                except OSError:
                    pass

        # Level 4: local (gitignored)
        local_path = self.cwd / _LOCAL_SUFFIX
        if local_path.exists():
            try:
                sections.append(("LOCAL", local_path.read_text()))
            except OSError:
                pass

        if not sections:
            return ""

        parts: list[str] = []
        for level_name, content in sections:
            content = content.strip()
            if content:
                parts.append(f"## [{level_name}]\n{content}")

        return "\n\n".join(parts)

    def list_files(self) -> list[dict]:
        """Return metadata for all CLAUDE.md files that exist."""
        found: list[dict] = []
        candidates = [
            ("managed", _MANAGED_PATH),
            ("user",    _USER_PATH),
        ]
        for rel in _PROJECT_FILES:
            candidates.append(("project", self.cwd / rel))
        candidates.append(("local", self.cwd / _LOCAL_SUFFIX))

        rules_dir = self.cwd / ".lazyown" / "rules"
        if rules_dir.is_dir():
            for rf in sorted(rules_dir.glob("*.md")):
                candidates.append(("rule", rf))

        for level, path in candidates:
            if path.exists():
                try:
                    size = path.stat().st_size
                    found.append({"level": level, "path": str(path), "size": size})
                except OSError:
                    pass
        return found

    def create_user_file(self, content: str) -> str:
        """Create/overwrite ~/.lazyown/CLAUDE.md."""
        _USER_PATH.parent.mkdir(parents=True, exist_ok=True)
        _USER_PATH.write_text(content)
        return f"Written: {_USER_PATH}"

    def create_project_file(self, content: str,
                            local: bool = False) -> str:
        """Create CLAUDE.md (or CLAUDE.local.md) in cwd."""
        target = self.cwd / (_LOCAL_SUFFIX if local else "CLAUDE.md")
        target.write_text(content)
        return f"Written: {target}"

    def add_rule(self, rule_name: str, content: str) -> str:
        """Add a named rule file to .lazyown/rules/."""
        rules_dir = self.cwd / ".lazyown" / "rules"
        rules_dir.mkdir(parents=True, exist_ok=True)
        rule_path = rules_dir / f"{rule_name}.md"
        rule_path.write_text(content)
        return f"Rule written: {rule_path}"

    def status_text(self) -> str:
        files = self.list_files()
        if not files:
            return "No CLAUDE.md files found in hierarchy."
        lines = ["CLAUDE.md hierarchy:"]
        for f in files:
            lines.append(f"  [{f['level']:8s}] {f['path']}  ({f['size']:,} bytes)")
        return "\n".join(lines)
