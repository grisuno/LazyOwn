"""utils as a library: importing it must never parse the importer's argv."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

_ROOT = Path(__file__).parent.parent


def test_import_with_foreign_argv_is_silent() -> None:
    """Headless tools import utils; their flags are not LazyOwn's business."""
    proc = subprocess.run(
        [
            sys.executable,
            "-c",
            "import sys; sys.path.insert(0, '.'); import utils; print('imported clean')",
            "auto",
            "--target",
            "172.17.0.2",
            "--lhost",
            "192.168.1.120",
        ],
        cwd=str(_ROOT),
        capture_output=True,
        text=True,
        timeout=120,
    )
    assert "Wrong argument" not in proc.stdout + proc.stderr
    assert "imported clean" in proc.stdout


def test_lazy_import_chains_stay_silent() -> None:
    """Transitive utils imports (e.g. via lazy_intel at call time) stay silent."""
    proc = subprocess.run(
        [
            sys.executable,
            "-c",
            "import sys; sys.path.insert(0, '.'); sys.path.insert(0, 'modules');"
            " import lazy_intel;"
            " from utils import redact_secrets;"
            " print('chain clean')",
            "auto",
            "--target",
            "172.17.0.2",
        ],
        cwd=str(_ROOT),
        capture_output=True,
        text=True,
        timeout=120,
    )
    assert "Wrong argument" not in proc.stdout + proc.stderr
    assert "chain clean" in proc.stdout
