# Migration Plan: cmd2 -> Textual TUI

## Current State

- **Framework**: cmd2 (Python `cmd.Cmd` wrapper)
- **Commands**: 724+ `do_*` methods on `LazyOwnShell` class
- **CommandSets**: 74 files in `cli/commands/` using `cmd2.CommandSet`
- **Plugins**: 207 loaded (132 YAML addons, 25 Lua, 50 .tool files)
- **Output**: Raw ANSI prints + Rich Console
- **TUI Overlays**: 7 Textual Apps (dashboard, palette, graph, etc.) — launched as separate apps

## Target State

A single **Textual App** that replaces the cmd2 loop entirely:
- Input at the bottom, scrollable output in the center
- Persistent dashboard sidebar (left)
- Plugin browser sidebar (right)
- All existing plugins (YAML, Lua, .tool) work without changes
- Textual overlays integrate as in-app screens rather than separate apps

---

## Phased Migration Plan

### Phase 0: POC Validation (CURRENT)
**Status**: DONE
**Location**: `poc_tui/`

Validates that:
- Textual app renders correctly
- Plugin loader works with all 207 plugins
- Dashboard sidebar shows live config
- Output panel accumulates results
- Command input with history + tab completion works

### Phase 1: Core Shell Bridge
**Goal**: Run the Textual app ON TOP of the existing cmd2 shell (hybrid mode)

| Task | Details | Effort |
|------|---------|--------|
| 1.1 Create `TextualBridge` adapter | Wraps `LazyOwnShell.onecmd()` inside Textual's `run_worker` | 1 day |
| 1.2 Async command execution | Use `self.run_worker()` to avoid blocking the Textual event loop | 1 day |
| 1.3 Output capture | Redirect `self.stdout` to a Textual `RichLog` widget | 0.5 day |
| 1.4 Prompt integration | Textual `Input` replaces cmd2's readline prompt | 0.5 day |

**Key pattern**:
```python
class TextualBridge(App):
    def __init__(self, shell: LazyOwnShell):
        self.shell = shell

    def execute_command(self, cmd: str):
        def _run():
            self.shell.onecmd(cmd)
        self.run_worker(_run, thread=True)
```

### Phase 2: Native CommandSet Migration
**Goal**: Migrate `cli/commands/` CommandSets to Textual widgets

| CommandSet | File | Migration Strategy |
|------------|------|--------------------|
| `db_*` | `cli/commands/database.py` | Textual DataTable + Input form |
| `search/use/back` | `cli/commands/search.py` | Fuzzy list with preview panel |
| `generate` | `cli/commands/generate.py` | Form with parameter inputs |
| `resource` | `cli/commands/resource.py` | Syntax-highlighted code viewer |
| `scan_*` | `cli/commands/scan.py` | Progress bar + live output |
| `exploit_*` | `cli/commands/exploit.py` | Status cards with results |

**Migration pattern per CommandSet**:
```python
# OLD: cmd2 CommandSet
class ScanCommands(LazyOwnCommandSet):
    @with_category("02. Scanning")
    def do_nmap(self, args):
        run_command(f"nmap {args}")

# NEW: Textual widget + command handler
class ScanPanel(Static):
    """Textual widget for scan commands."""

    def compose(self):
        yield DataTable(id="scan-results")
        yield Input(placeholder="Target...", id="scan-input")

    def on_nmap(self, target: str):
        """Called when user types 'nmap <target>'"""
        self.run_worker(self._run_nmap, target, thread=True)
```

### Phase 3: Full TUI Replacement
**Goal**: Remove cmd2 dependency entirely

| Task | Details | Effort |
|------|---------|--------|
| 3.1 Replace `cmd2.Cmd` base | `LazyOwnShell` becomes `Textual.App` subclass | 2 days |
| 3.2 Migrate `default()` handler | Alias resolution + "did you mean" suggestions | 0.5 day |
| 3.3 Migrate hooks | `precmd`, `postcmd` -> Textual `on_mount`, `on_key`, workers | 1 day |
| 3.4 Migrate arg parsers | `argparse` -> Textual `CommandPalette` + forms | 1 day |
| 3.5 Migrate history | cmd2 `PersistentHistory` -> Textual `DataTable` | 0.5 day |
| 3.6 Remove cmd2 dependency | Clean up imports, update requirements | 0.5 day |

### Phase 4: Advanced TUI Features
**Goal**: Leverage Textual capabilities fully

| Feature | Implementation |
|---------|---------------|
| Split panes | `Horizontal`/`Vertical` containers with `Header`/`Footer` |
| Live widgets | `DataTable` for scan results, `Tree` for file browser |
| Modal dialogs | Textual `ModalScreen` for confirmations, wizards |
| CSS theming | Existing `cli/themes.py` -> Textual CSS variables |
| Mouse support | Textual native — click to select, scroll panels |
| Screen stacking | `push_screen()` for overlays (palette, dashboard) |
| Worker threads | `run_worker(thread=True)` for long-running commands |

---

## Backward Compatibility Strategy

### Phase 1-2: Hybrid Mode
- cmd2 shell runs in a background thread
- Textual app sends commands via `shell.onecmd(cmd)`
- Output captured via `io.StringIO` redirect
- All 207 plugins work unchanged (they call `self.cmd()` internally)

### Phase 3: Full Replacement
- Plugins that call `self.cmd()` need update to use Textual's `run_worker`
- Plugin API changes: `app.params` stays, `app.one_cmd()` -> `app.execute()`
- Lua `register_command` bridge remains identical
- YAML addon `execute_command` stays the same (runs via subprocess)

### Plugin Compatibility Matrix

| Plugin Type | Phase 1-2 | Phase 3 | Changes Needed |
|-------------|-----------|---------|----------------|
| YAML addons | Works as-is | Works as-is | None — subprocess execution |
| Lua plugins | Works as-is | Works as-is | None — `app.params` + `register_command` bridge |
| .tool files | Works as-is | Works as-is | None — subprocess execution |
| Native `do_*` | Needs bridge | Migrated | Each method -> command handler |

---

## Risk Mitigation

1. **Don't break the working shell**: Phase 1 is hybrid — cmd2 still runs underneath
2. **Plugin isolation**: All 207 plugins use subprocess or Lua — they don't depend on cmd2 internals
3. **Incremental migration**: Each phase is independently deployable
4. **Rollback**: Keep cmd2 as fallback import until Phase 3 is stable

---

## File Structure After Migration

```
poc_tui/
  app.py              # Main Textual App (LazyOwnTUI)
  plugin_loader.py    # Unified plugin loader (YAML/Lua/.tool)
  config.py           # PayloadConfig reader
  run.py              # Symlink launcher
  __main__.py         # Entry point
  
  # Future (Phase 2+):
  widgets/
    dashboard.py      # Left sidebar (campaign state)
    output.py         # Center output panel
    plugins.py        # Right sidebar (plugin browser)
    command_input.py  # Bottom input with autocomplete
    forms.py          # Parameter input forms
  
  commands/           # Migrated CommandSets
    scan.py
    exploit.py
    recon.py
    ...
```

---

## Estimated Timeline

| Phase | Duration | Deliverable |
|-------|----------|-------------|
| Phase 0: POC | DONE | Working proof of concept |
| Phase 1: Bridge | 3 days | Textual app wrapping cmd2 |
| Phase 2: CommandSets | 1-2 weeks | Native Textual widgets per phase |
| Phase 3: Full replacement | 1 week | Remove cmd2 entirely |
| Phase 4: Advanced | 1-2 weeks | Split panes, modals, screens |
| **Total** | **~5 weeks** | **Full TUI shell** |
