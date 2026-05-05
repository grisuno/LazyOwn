"""Configuration layer.

Centralises every tunable parameter so the rest of the package never embeds a
magic number or a hard-coded path. Three concerns are exposed:

* :class:`lazygui.config.constants.AppConstants` - immutable defaults.
* :class:`lazygui.config.paths.AppPaths` - filesystem layout resolver.
* :class:`lazygui.config.settings.AppSettings` - mutable, persisted overrides.
"""

from lazygui.config.constants import AppConstants
from lazygui.config.paths import AppPaths
from lazygui.config.settings import AppSettings

__all__ = ["AppConstants", "AppPaths", "AppSettings"]
