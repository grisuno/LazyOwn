# lazygui

Desktop GUI application for LazyOwn. Built with a widget toolkit (separate
from the Textual TUI in `cli/dashboard_tui.py`). Provides a graphical
front-end to the most common engagement operations without requiring a
terminal.

## Structure

| Path | Purpose |
|------|---------|
| `app.py` | Application entry point. Initialises the main window and event loop. |
| `__main__.py` | `python -m lazygui` entry point. |
| `version.py` | Version string for the GUI application. |
| `config/` | Configuration schema and default values for the GUI. Separate from `payload.json` — GUI preferences (window size, theme, panel layout) live here. |
| `panels/` | Individual panel modules: target panel, kill-chain panel, config panel, commands panel, ops panel. Each panel is a self-contained widget class. |
| `services/` | Background service layer: reads `payload.json` and `sessions/` to feed data to panels without blocking the UI thread. |
| `theme/` | Colour scheme and font definitions. |
| `widgets/` | Reusable widget components (data tables, progress bars, log viewers). |
| `windows/` | Top-level window classes. |

## Running

```bash
python -m lazygui
# or
python lazygui/app.py
```

Requires the virtualenv to be active (`source env/bin/activate`).

## Design principles

- Panels read from `payload.json` and `sessions/` through the `services/`
  layer — they never import from `lazyown.py` or `lazyc2.py` directly.
- Long-running operations (nmap, gobuster) are dispatched as background
  threads. The panel subscribes to a result queue and updates the display when
  the result arrives.
- The GUI and the CLI shell can run simultaneously against the same
  `payload.json`. Changes made in one are visible to the other after the next
  read cycle (default 5 seconds).
