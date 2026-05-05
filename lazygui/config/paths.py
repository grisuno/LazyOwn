"""Filesystem layout resolver.

The application stores user-specific data under the platform-appropriate
config directory and reads project-relative resources from the repository
root. All path resolution flows through :class:`AppPaths` so tests can swap
locations and so nothing downstream embeds an absolute path.
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path

from lazygui.config.constants import AppConstants


@dataclass(frozen=True, slots=True)
class AppPaths:
    """Resolved filesystem locations for runtime artefacts.

    The constructor derives every path from the supplied :class:`AppConstants`
    and the current environment, so a test can override ``home_dir`` or the
    ``project_root`` without monkey-patching the rest of the application.
    """

    constants: AppConstants
    project_root: Path = field(default_factory=lambda: _detect_project_root())
    home_dir: Path = field(default_factory=Path.home)

    @property
    def config_dir(self) -> Path:
        """User config directory respecting ``XDG_CONFIG_HOME`` when set."""
        xdg = os.environ.get("XDG_CONFIG_HOME")
        base = Path(xdg) if xdg else self.home_dir / ".config"
        return base / self.constants.ids.organization_name.lower() / "operator-console"

    @property
    def settings_file(self) -> Path:
        """Absolute path of the persisted settings JSON file."""
        return self.config_dir / self.constants.ids.settings_filename

    @property
    def layout_file(self) -> Path:
        """Absolute path of the persisted Qt layout binary blob."""
        return self.config_dir / self.constants.ids.layout_filename

    @property
    def project_run_script(self) -> Path:
        """Absolute path to the ``run`` shell launcher in the repository."""
        return self.project_root / "run"

    @property
    def lazyc2_script(self) -> Path:
        """Absolute path to the Flask backend ``lazyc2.py``."""
        return self.project_root / "lazyc2.py"

    def ensure_config_dir(self) -> Path:
        """Create the config directory if missing and return it."""
        self.config_dir.mkdir(parents=True, exist_ok=True)
        return self.config_dir


def _detect_project_root() -> Path:
    """Walk upwards from this file looking for the LazyOwn project markers.

    The detection considers a directory the project root when it contains
    both the ``run`` launcher and ``lazyown.py``. Falls back to the directory
    two levels above this module if no marker is found, matching the
    repository layout (``<root>/lazygui/config/paths.py``).
    """
    here = Path(__file__).resolve()
    for candidate in [here, *here.parents]:
        if (candidate / "run").is_file() and (candidate / "lazyown.py").is_file():
            return candidate
    return here.parents[2]
