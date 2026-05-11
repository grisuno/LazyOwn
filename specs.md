# LazyOwn Operator UX Specs

Spec-driven design for the two operator-experience features added in
`release/0.2.108`: **inline reactive hints** and the **TUI dashboard**.

---

## Feature A — Inline reactive hints

### Goal

Print a single dim next-step suggestion line between every command's output
and the next cmd2 prompt, without blocking operator input.

### Happy path

**Trigger:** operator executes any `do_*` command that is not on
`SKIP_COMMANDS`.

**Inputs:**
- `enable_inline_hints` in `payload.json` (default `true`).
- `graphify-out/graph_lazyown.json` loaded by `GraphAdvisor` (mtime-cached).
- Last executed command string from `cmd2.plugin.PostcommandData.statement`.

**Successful outcome:**
One rich-formatted line appears below the command output before the next
prompt renders. Format: `  ↳ label_a · label_b · label_c`.

**Observable signal:** operator sees the hint and may type the suggested
command directly, or ignore it and continue.

### Sad paths

| Condition | Behaviour |
|-----------|-----------|
| `enable_inline_hints` is `false` | `render_inline_hints` returns immediately. No output. |
| Graph file absent (`/graphify .` not yet run) | `advisor.is_available()` returns `False`. Hook skips render silently. |
| `GraphAdvisor.suggest_next()` raises | `except Exception: pass` in hook. No output, no traceback. |
| Command is on `SKIP_COMMANDS` | `render_inline_hints` returns on first token check. |
| Graph returns empty suggestions | No hint line rendered. |
| `register_postcmd_hook` fails (wrong cmd2 version) | `try/except` in `__init__` emits `print_warn` and continues. |
| No labels extractable from suggestions | `_extract_labels` returns `[]`; render skipped. |

### Implementation contract

- Module: `cli/reactive_hints.py`
- Public API: `render_inline_hints(advisor, last_command, limit, enabled) → None`
- Hook registration: `self.register_postcmd_hook(self._inline_hint_hook)` in
  `LazyOwnShell.__init__` (guarded by try/except).
- The hook method `_inline_hint_hook` reads `self.params["enable_inline_hints"]`
  at call time so changes via `set` take effect immediately.
- Output via `rich.console.Console` — never `print()` directly.
- Zero coupling to Flask, MCP, or autonomous daemon.

### Tests

File: `tests/test_reactive_hints.py`

| Test | Assertion |
|------|-----------|
| `test_disabled_flag_skips_render` | Console.print not called when `enabled=False`. |
| `test_skip_command_skips_render` | No output for every command in `SKIP_COMMANDS`. |
| `test_empty_command_skips_render` | No output for whitespace input. |
| `test_empty_suggestions_skips_render` | No output when advisor returns `[]`. |
| `test_normal_command_renders_hint` | Console.print called once for `lazynmap`. |
| `test_advisor_called_with_correct_command` | Advisor receives first token only. |
| `test_exception_in_advisor_does_not_propagate` | RuntimeError swallowed, no output. |
| `test_all_skip_commands_are_skipped` | Full `SKIP_COMMANDS` set never renders. |
| `test_limit_is_passed_to_advisor` | `limit` parameter flows through correctly. |

---

## Feature B — Operator TUI dashboard

### Goal

Full-screen Textual TUI showing live campaign state: target, kill chain
phase, recent commands, objectives, credentials, beacons, graph hints.
Launched with `dashboard` in the cmd2 shell; returns to shell on Q.

### Happy path

**Trigger:** operator runs `dashboard` in the cmd2 shell.

**Inputs:**
- `payload.json` → target IP, attacker IP, domain, OS, C2 port.
- `sessions/world_model.json` → current phase, completed phases, objective.
- `sessions/tasks.json` → task list.
- `sessions/LazyOwn_session_report.csv` → last 10 commands.
- `sessions/credentials*.txt` → line count → credential count.
- `sessions/hash*.txt` → line count → hash count.
- `sessions/beacons.json` → beacon count.
- `graphify-out/graph_lazyown.json` → top-5 graph suggestions.

**Successful outcome:**
Full-screen TUI renders. Panels auto-refresh every 5 seconds.
Q or Ctrl-C closes the app and returns to the cmd2 prompt.

**Observable signal:** operator can monitor campaign state in real time
without opening a browser or reading raw JSON files.

### Sad paths

| Condition | Behaviour |
|-----------|-----------|
| `textual` not installed | `do_dashboard` catches `ImportError`, prints install hint, returns. |
| `payload.json` missing | `_read_json` returns `{}`. Panels show `—` placeholders. |
| `sessions/world_model.json` missing | Same as above. Kill chain shows all phases uncompleted. |
| `sessions/LazyOwn_session_report.csv` missing | `_read_recent_commands` returns `[]`. Commands panel shows placeholder. |
| Graph absent | `_graph_hints` returns `[]`. Hint bar shows guidance to run `/graphify .`. |
| `sessions/beacons.json` missing or malformed | `_beacon_count` returns `0`. |
| Any `_do_refresh` call raises | Textual renders last-known data; next interval retries. |
| Terminal too narrow | Textual handles layout gracefully via `min-width` CSS. |
| Q pressed mid-refresh | Textual exits cleanly; in-flight interval is cancelled by the event loop. |
| SIGINT (Ctrl-C) | Textual `App.run()` catches it and exits. cmd2 prompt returns. |

### Widget architecture

```
LazyOwnDashboard(App)
├── Header               (built-in Textual)
├── TargetPanel          (Static, docked top, 3 rows)
├── Horizontal#main-area
│   ├── Vertical#left-col  (28 cols)
│   │   ├── KillChainPanel (Static)
│   │   └── ConfigPanel    (Static)
│   ├── Vertical#center-col (1fr)
│   │   └── CommandsPanel  (Static)
│   └── Vertical#right-col (30 cols)
│       └── OpsPanel       (Static)
├── HintBar              (Static, docked bottom, 2 rows)
└── Footer               (built-in Textual)
```

Each widget exposes a single `update_data(**typed_args) → None` method that
receives plain Python dicts / lists from `_do_refresh`. No widget reads files
directly — all I/O is in the module-level helpers.

### Data helper contracts

| Helper | Inputs | Returns | Error behaviour |
|--------|--------|---------|-----------------|
| `_read_json(path)` | file path | `dict` | `{}` on OSError / JSONDecodeError |
| `_read_recent_commands(limit)` | int | `list[dict]` | `[]` when file absent or malformed |
| `_count_lines_in_glob(pattern)` | glob pattern | `int` | `0` when no files match |
| `_beacon_count()` | — | `int` | `0` when file absent or malformed |
| `_graph_hints(limit)` | int | `list[str]` | `[]` on any exception |

### Refresh cycle

1. `on_mount` → calls `_do_refresh()` once.
2. `set_interval(REFRESH_INTERVAL, _do_refresh)` → repeating timer.
3. Operator presses **R** → `action_refresh_data` → `_do_refresh()`.
4. Each `_do_refresh` call is synchronous; it reads all sources and calls
   each widget's `update_data`. Textual invalidates and re-renders changed
   widgets automatically.

### Tests

File: `tests/test_dashboard_tui.py`

| Test | Assertion |
|------|-----------|
| `test_reads_valid_file` | `_read_json` returns parsed dict. |
| `test_missing_file_returns_empty_dict` | Returns `{}` on absent file. |
| `test_invalid_json_returns_empty_dict` | Returns `{}` on bad JSON. |
| `test_counts_non_empty_lines` | `_count_lines_in_glob` counts correctly. |
| `test_empty_file_returns_zero` | Empty file → 0. |
| `test_no_matching_files_returns_zero` | No glob matches → 0. |
| `test_multiple_files_summed` | Lines across multiple files summed. |
| `test_reads_recent_commands` | CSV rows parsed into dicts. |
| `test_missing_file_returns_empty` | Absent CSV → `[]`. |
| `test_respects_window_limit` | Only last N rows returned. |
| `test_skips_empty_tool_rows` | Rows with empty `tool` column skipped. |
| `test_all_phases_present` | Kill chain has all 8 expected phase keys. |
| `test_phases_ordered` | Recon precedes exploit precedes lateral. |
| `test_graph_hints_returns_list` | Returns list even when advisor unavailable. |

---

## Payload keys added

| Key | Type | Default | Purpose |
|-----|------|---------|---------|
| `enable_inline_hints` | bool | `true` | Enable/disable postcmd hint rendering. |

---

## Dependencies added

| Package | Version constraint | Added to |
|---------|--------------------|---------|
| `textual` | ≥ 0.50.0 | `install.sh`, `requirements.txt` (if present) |

`rich` was already a dependency; `textual` depends on it and a compatible
version will be resolved by pip automatically.

---

## Files changed

| File | Change |
|------|--------|
| `cli/reactive_hints.py` | New module — hint renderer |
| `cli/dashboard_tui.py` | New module — Textual dashboard |
| `tests/test_reactive_hints.py` | New — 9 unit tests |
| `tests/test_dashboard_tui.py` | New — 14 unit tests |
| `lazyown.py` | Import `_render_inline_hints`; register postcmd hook; add `do_dashboard` |
| `payload.json` | Add `enable_inline_hints: true` |
| `install.sh` | Add `pip3 install textual` |
| `README.md` | Add sections for inline hints and TUI dashboard |
| `CLAUDE.md` | Add section 15b covering both features |
| `specs.md` | This file |
