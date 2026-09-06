"""Watchdog: core must not depend on the retired legacy Groq LLM scripts.

Encodes the consolidation contract — after the Groq ``process_prompt_*`` family
moved into ``modules.llm_prompts`` / ``modules.llm_adapter``, no module under
the core source tree may import ``modules.legacy.lazygptcli`` or
``modules.legacy.lazygptcli_unified``. Only the standalone C2 bots
(``slack_c2_bot``, ``telegram_c2``, ``discord_c2``) may reference them, and they
are out of the core tree.
"""

from __future__ import annotations

import ast
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

CORE_DIRS = ("modules", "cli", "core", "skills", "poc_tui", "lazygui")
CORE_FILES = ("lazyown.py", "lazyc2.py", "utils.py")

FORBIDDEN_PREFIXES = ("modules.legacy.lazygptcli",)

EXCLUDED_SUBDIRS = {
    "__pycache__",
    ".git",
    "tests",
    "test",
    "legacy",
}


def _core_source_files():
    files = [ROOT / name for name in CORE_FILES if (ROOT / name).exists()]
    for directory in CORE_DIRS:
        base = ROOT / directory
        if not base.is_dir():
            continue
        for dirpath, dirnames, filenames in os.walk(base):
            dirnames[:] = [d for d in dirnames if d not in EXCLUDED_SUBDIRS]
            for filename in filenames:
                if filename.endswith(".py"):
                    files.append(Path(dirpath) / filename)
    return files


def _imported_targets(node):
    targets = []
    for child in ast.walk(node):
        if isinstance(child, ast.ImportFrom):
            module = child.module or ""
            if module.startswith(FORBIDDEN_PREFIXES):
                targets.append(module)
        elif isinstance(child, ast.Import):
            for alias in child.names:
                if alias.name.startswith(FORBIDDEN_PREFIXES):
                    targets.append(alias.name)
    return targets


class TestNoLegacyGroqImportInCore:
    def test_no_core_file_imports_legacy_groq(self):
        offenders = []
        for path in _core_source_files():
            try:
                tree = ast.parse(path.read_text(encoding="utf-8", errors="ignore"))
            except (OSError, SyntaxError):
                continue
            for target in _imported_targets(tree):
                offenders.append(f"{path}:{target}")
        assert not offenders, "Legacy Groq import found in core:\n" + "\n".join(offenders)
