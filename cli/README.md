# cli

Shell-layer extensions for the LazyOwn cmd2 CLI. Every file here plugs into
`LazyOwnShell` without touching the 27k-line `lazyown.py` core directly. The
layer follows strict Dependency Inversion: each module depends on small
`typing.Protocol` interfaces rather than on the concrete shell class.

## Files

| File | Purpose |
|------|---------|
| `wizard.py` | Guided first-run setup. Walks the operator through rhost, lhost, domain, device, os_id, api_key, and SecLists paths. Auto-detects lhost from the routing table. Zero imports from `lazyown.py` or `lazyc2.py`. |
| `doctor.py` | Preflight environment health check behind the `doctor` command. Validates the *installation* (Python version, active virtualenv, importable packages, C2 certificates, payload.json, SecLists, external tooling) where `wizard --check` validates the *configuration*. Delegates binary and SecLists detection to `wizard.py` (single source of truth); pure check functions return `CheckResult` objects with injected probes so they are unit-testable. Zero imports from `lazyown.py` or `lazyc2.py`. |
| `scope_guard.py` | Authorization scope guard behind the `scope` command. Before every offensive command runs, `ScopeGuard.evaluate` checks the active `rhost` against the authorized scope (`payload.json["scope"]`: CIDR/IP/hostname entries, `*.` wildcards) under the `scope_enforcement` posture (`off`/`warn`/`enforce`). Fail-open: a no-op while the scope is empty or the mode is `off`, so existing campaigns are unaffected until a scope is defined. Offensive/benign classification is pure data (`OFFENSIVE_CATEGORIES`) plus `build_offensive_commands`; the shell injects the predicate. Zero imports from `lazyown.py` or `lazyc2.py`. Wired into `LazyOwnShell.onecmd_plus_hooks` (the single command chokepoint). |
| `aliases.py` | Dynamic alias resolver. Alias templates keep `{rhost}` / `{lhost}` placeholders and are rendered against `self.params` at execution time. `DynamicAliasResolver` + `cli/aliases.yaml` drive this. |
| `aliases.yaml` | Declarative alias definitions consumed by `aliases.py`. |
| `graph_advisor.py` | Reads `graphify-out/graph_lazyown.json` and answers three queries: fuzzy node search, graph neighbour walk, and next-step recommendation weighted by recent activity. Caches by `(path, mtime)`. Consumed by `recommendation_signals.py` as one of four signals. |
| `recommendation.py` | **Single source of truth for "what next".** `RecommendationEngine` fuses every signal (graph proximity, learned policy category priors, nmap trigger-matched recon plan, static kill-chain tables) into one ranked `Recommendation` list with full provenance. Two-tier fusion: concrete-action signals propose commands; the policy signal proposes kill-chain *categories* that up-weight matching actions. Pure module — zero heavy imports, every weight in `EngineWeights`. |
| `recommendation_signals.py` | The four `RecommendationSignal` adapters (`GraphSignal`, `PolicySignal`, `ReconPlanSignal`, `KillChainSignal`) plus `build_default_engine` / `build_context`. Each adapter imports its backend lazily and degrades to an empty proposal list when absent, so the engine is always available. The one entry point every consumer (`recommend_next` CLI verb, MCP `lazyown_recommend_next`) calls. |
| `reactive_hints.py` | `register_postcmd_hook` callback. After every `do_*` fires, prints one dim line of next-step suggestions. The kill-chain tables (`_KILL_CHAIN_NEXT` / `_PHASE_PRIORITY`) it owns are the single source consumed by both `command_chain.py` and the engine's `KillChainSignal`. Controlled by `enable_inline_hints` in `payload.json`. |
| `dashboard_tui.py` | Full-screen Textual TUI dashboard. Launched by the `dashboard` CLI command. Refreshes every 5 seconds. Reads `payload.json`, `sessions/world_model.json`, `sessions/tasks.json`, `sessions/autonomous_events.jsonl`, session CSV, and credential files. Renders the daemon reasoning stream (`reasoning_stream.py`) and the self-populating kill chain (`killchain.py`). |
| `reasoning_stream.py` | Pure parser over `sessions/autonomous_events.jsonl`. Turns daemon `_emit` events into compact `ReasoningEntry` records (command, phase, selector rationale, RL reward) for the dashboard reasoning panel. No rendering, no `lazyown.py`/`lazyc2.py` imports. |
| `killchain.py` | Derives kill-chain phase progress (`done`/`active`/`pending` plus per-phase activity and reward) from the daemon event stream, with a world-model fallback. Centralizes the canonical `DEFAULT_PHASES` order consumed by `dashboard_tui.py`. |
| `surface_graph.py` | Network surface graph reader. Composes the same `c2 → client → host → port → service` taxonomy that `templates/index.html` renders with `vis.js`, but builds it from `sessions/hostsdiscovery.txt`, `sessions/scan_discovery*.csv`, per-implant `sessions/<id>.log`, and `payload.json`. Pure data layer — returns dataclasses + `to_dict()` for any renderer. |
| `surface_tui.py` | Renderer for `surface_graph`. Three modes: `render_static` (Rich tree printed once), `launch_tui` (full-screen Textual explorer with selectable detail pane), and `render_json` (JSON dump). Powers the `surface` cmd2 command. |
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
