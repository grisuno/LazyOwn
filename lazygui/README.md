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


## v2.0 console contracts (relocated from CLAUDE.md)

## 15j. LazyGUI — v2.0 Operator Console (PySide6 Desktop App)

**Package:** `lazygui/` (entry: `python -m lazygui`)
**Test suite:** `tests/test_lazygui_models.py`, `tests/test_lazygui_backend.py`, `tests/test_lazygui_graph_widget.py` (103 tests)

### Architecture

```
QApplication -> Application -> MainWindow
    ├── Backend (abstract) -- signals: status_changed, terminal_output,
    │       sessions_changed, listeners_changed, topology_changed,
    │       dashboard_updated, beacon_result, campaign_changed
    ├── LocalPtyBackend  -- PTY fork "bash run"
    └── TeamserverBackend -- HTTP REST + Socket.IO to lazyc2.py
────
├── GraphPanel -- Cobalt Strike-style topology (QGraphicsView, force layout)
├── SessionsPanel -- beacon list with right-click context menu (spawn shell,
│       port scan, screenshot, keylog, migrate, download/upload, kill)
├── ListenersPanel -- listener table
├── KillChainPanel -- 8-phase kill-chain progress bar
├── CredentialsPanel -- creds, hashes, loot
├── MarketplacePanel -- YARA rules + Nuclei templates + tools (tabbed)
├── CampaignPanel -- active campaigns with objective tracking
├── CVEPanel -- CVE knowledge base with severity filter
├── TerminalPanel -- ANSI terminal emulator
└── EventLogPanel -- ring buffer event log (5000 records)
────
├── 6 themes: tactical_green (default), tokyo_night, catppuccin_mocha,
│       gruvbox_dark, cobalt_clone, solarized_light
└── Keyboard: Ctrl+K palette, Ctrl+Shift+T cycle theme, Ctrl+1-5 panels
```

### Backend communication contracts

`TeamserverBackend` connects to `lazyc2.py` via:

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/data` | GET | Sessions, listeners, operator (poll 2000ms) |
| `/api/dashboard` | GET | Aggregated beacon count, events, facts |
| `/api/surface_live` | GET | Attack surface graph topology (nodes + edges) |
| `/api/listeners` | GET | C2 listener management |
| `/api/run` | POST | Global shell command |
| `/issue_command` | POST | Beacon-scoped command |
| `/api/output` | GET | Global command stdout |
| `/get_results` | GET | Beacon result cache |
| `/socket.io/` /pty | WS | PTY terminal I/O (real-time) |
| `/socket.io/` /terminal | WS | Beacon terminal I/O |
| `/socket.io/` / | WS | Default command/output channel |

### Domain models

- `GraphNode` — identifier, label, node_type, shape, color, icon, metadata
- `GraphEdge` — source_id, target_id, label, edge_type, color
- `Topology` — nodes sequence + edges sequence (empty sentinel)
- `BeaconResult` — client_id, output, command, OS, hostname, user, IPs
- `DashboardPayload` — beacon_count, events, campaign_state, facts_count
- `CampaignSummary` — identifier, name, status, playbook, objectives
- `Session`, `Listener`, `Operator`, `EventRecord` (unchanged from v1)

---

