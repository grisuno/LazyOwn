"""Theme subsystem.

Themes are described by :class:`ThemeTokens` instances. The
:class:`QssBuilder` translates tokens into a Qt stylesheet, and
:class:`ThemeManager` registers palettes, applies them to the running
:class:`QApplication`, and emits a Qt signal when the active theme changes so
widgets can react.
"""

from lazygui.theme.tokens import ThemeTokens
from lazygui.theme.qss_builder import QssBuilder
from lazygui.theme.manager import ThemeManager

__all__ = ["ThemeTokens", "QssBuilder", "ThemeManager"]
