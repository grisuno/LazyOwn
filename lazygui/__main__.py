"""Entry point for ``python -m lazygui``.

Delegates to :class:`lazygui.app.Application` so command-line invocation and
programmatic embedding share the same bootstrap path.
"""

from __future__ import annotations

import sys

from lazygui.app import Application


def main() -> int:
    """Bootstrap the GUI and run the Qt event loop.

    Returns the exit status produced by Qt so it can propagate to the shell.
    """
    application = Application(sys.argv)
    return application.run()


if __name__ == "__main__":
    sys.exit(main())
