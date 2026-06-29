"""Pytest bootstrap for the claude_md_orchestrator test suite.

The test suite lives next to the package, not inside the project test
tree. The conftest inserts the parent skills directory into sys.path
so the import resolver finds the package under the project root.
"""

from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
SKILLS_ROOT = PROJECT_ROOT / "skills"
if str(SKILLS_ROOT) not in sys.path:
    sys.path.insert(0, str(SKILLS_ROOT))
