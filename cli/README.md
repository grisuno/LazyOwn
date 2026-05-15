# cli

Shell-layer extensions for the LazyOwn cmd2 CLI. Every file here plugs into
`LazyOwnShell` without touching the 27k-line `lazyown.py` core directly. The
layer follows strict Dependency Inversion: each module depends on small
`typing.Protocol` interfaces rather than on the concrete shell class.

## Files

| File | Purpose |
|------|---------|
| `wizard.py` | Guided first-run setup. Walks the operator through rhost, lhost, domain, device, os_id, api_key, and SecLists paths. Auto-detects lhost from the routing table. Zero imports from `lazyown.py` or `lazyc2.py`. |
| `aliases.py` | Dynamic alias resolver. Alias templates keep `{rhost}` / `{lhost}` placeholders and are rendered against `self.params` at execution time. `DynamicAliasResolver` + `cli/aliases.yaml` drive this. |
| `aliases.yaml` | Declarative alias definitions consumed by `aliases.py`. |
| `graph_advisor.py` | Reads `graphify-out/graph_lazyown.json` and answers three queries: fuzzy node search, graph neighbour walk, and next-step recommendation weighted by recent activity. Caches by `(path, mtime)`. |
| `reactive_hints.py` | `register_postcmd_hook` callback. After every `do_*` fires, prints one dim line of graph-driven next-step suggestions. Controlled by `enable_inline_hints` in `payload.json`. |
| `dashboard_tui.py` | Full-screen Textual TUI dashboard. Launched by the `dashboard` CLI command. Refreshes every 5 seconds. Reads `payload.json`, `sessions/world_model.json`, `sessions/tasks.json`, session CSV, and credential files. |
| `cli_enhancements.py` | Fuzzy command finder (`fz`), interactive parameter form (`form`), live scan tail (`status_tail`), log grep (`grep_log`), hot addon reloader (`reload_addons`), and payload-aware Tab completer. |
| `fuzzy_picker.py` | Curses-driven fuzzy dropdown anchored at the bottom of the terminal. Opens on Tab when two or more completions exist. Navigation: arrow keys, Page Up/Down, Backspace to refine, Enter or Tab to insert. |
| `palette.py` | Phase-aware command palette. Reads the command index and filters by engagement phase. |
| `palette_command.py` | cmd2 command and Tab-completer for the `palette` verb. |
| `palette_graph.py` | Graph-backed palette scoring. Merges fuzzy text rank with graph centrality. |
| `palette_telemetry.py` | Records palette usage to improve future ranking. |
| `banner_config.py` | Powerlevel10k-style prompt segment wizard. Manages the neon-box prompt configuration stored in `payload.json`. |
| `exploit_advisor.py` | Suggests exploits based on discovered service versions. Backed by the parquet knowledge bases. |
| `engagement_hooks.py` | Pre/post-command hooks that update `sessions/world_model.json` after each command. |
| `ops_commands.py` | Operational commands loaded as a cmd2 `CommandSet`. |
| `protips.py` | Context-sensitive tips printed below the prompt. |
| `registry.py` | Central registry of CLI extensions. Used by `lazyown.py` to auto-discover and wire command sets. |
| `show.py` | Display helpers for tabular output inside the shell. |
| `assign.py` | `assign` and `set` command logic extracted for reuse. |
| `command_index.json` | Pre-built index of every `do_*` command, alias, addon, and plugin. Rebuilt by `scripts/build_command_index.py`. |
| `commands/` | cmd2 `CommandSet` subpackage. See `commands/README.md`. |

## Design rules

- No file in `cli/` may import `lazyown.py` or `lazyc2.py`.
- Output goes through `rich.console.Console`, never raw `print()`, so ANSI
  handling is correct on all terminals and piped output.
- Graph-dependent features (`reactive_hints`, `graph_advisor`, `palette_graph`)
  degrade silently when `graphify-out/graph_lazyown.json` is absent — no
  error, no output.
- `wizard.py` takes a `params: dict` and a `save: Callable` injected by the
  caller. It never reads `payload.json` directly.

## Rebuild the command index

```bash
python scripts/build_command_index.py
```

Run this after adding a new `do_*` command, alias, addon, or plugin so Tab
completion and `fz` reflect the change immediately.
