### Audit-mode MCP improvements

Added in `skills/lazyown_mcp_helpers.py` to make autonomous audits more
efficient and less error-prone. Logic lives in a pure-function module so it
is unit-testable in isolation (`tests/test_mcp_improvements.py`).

| Tool / Param | What it does | Why it matters |
|--------------|--------------|----------------|
| `lazyown_session_init(format='json', include_recommend=true)` | Returns the SITREP as a structured dict instead of a banner; optionally embeds the top-3 ranked recommended actions. | Saves ~5KB of decorated text per call; agents can filter before consuming. |
| `lazyown_campaign_sitrep(format='json')` | Same JSON option for the master shift report. | Consistent format across both situation tools. |
| `lazyown_target_context(host, port=N)` | Aggregates open ports, world-model credentials (with provenance + confidence), vulnerabilities, pwntomate evidence freshness, and nmap freshness for one (host, port) tuple. | Replaces 4-5 separate lookups when deciding the next action on a target. |
| `lazyown_tasks_cleanup(dry_run=true, min_confidence=0.5)` | Audits `sessions/tasks.json` and flags entries where the embedded credential is actually a timestamp / URL / IP / duplicate. Pass `dry_run=false` to rewrite the file (a `.bak` is written first). | The watcher commonly turns log timestamps into "credentials"; on a real campaign this drops 100+ noise tasks. |
| `lazyown_evidence_grep(pattern, scope='all|loot|nmap|http|logs')` | Regex search across `sessions/` artefacts with binary-skip and size caps. Returns `path:line` matches. | Avoids dropping out to the shell for cross-evidence queries. |
| `lazyown_run_command(command, dry_run=true)` | Pre-flight: returns base command, binary path, OS-required vs OS-current, would-duplicate artefacts, missing payload keys — without executing. | Stops repeat-runs of 30-min scans by mistake; flags Windows-only tools against a Linux target before launch. |
| `lazyown_run_command_async(command, timeout)` + `lazyown_job_status(job_id)` | Background-job pattern for long commands (lazynmap, pwntomate, auto_loop). Returns a `job_id` immediately. | Frees the agent from blocking on commands documented as ≥30 min. |
| `lazyown_session_diff(take=true)` | Reports added / modified / removed files in `sessions/` plus new credentials / task IDs since the last snapshot. | Makes shift handoffs explicit; works well as the first call of every new session. |
| Confirmation gate (`confirm=true`) | `lazyown_c2_command`, `lazyown_c2_redop`, `lazyown_c2_adversary`, and any `run_command` whose body matches `rm -rf` / `exfil` / `wipe` / `encrypt-file` now require an explicit `confirm=true` argument. | Prevents accidental destructive actions from autonomous loops. |
| Provenance + confidence on credentials | Each credential exposed via `target_context` includes `is_likely_credential`, `confidence`, `classification`, and a `provenance` block (`source_file`, `line_no`, `captured_at`) when found. | Required for chain-of-custody in pentest reports. |
| Freshness annotations | Every evidence file in the JSON SITREP and `target_context` carries `age_seconds`, `age_human`, and `stale=true` once it exceeds `freshness_threshold_seconds` (default 7 days; configurable per-call). | Stops the agent from exploiting on top of stale recon evidence. |

### Audit-mode CLI enhancements

A SOLID extension layer in `cli/cli_enhancements.py` plugs into the cmd2 shell
via the existing CommandSet auto-discovery (`cli/commands/audit.py`). No
edits to the 27k-line `lazyown.py` core were required beyond two small hooks
(lazy alias loading, `completedefault` fallback).

| Command / hook | What it does | Backed by |
|----------------|--------------|-----------|
| `fz [query]` | Fuzzy command finder over every `do_*`, alias, plugin and addon. Scores exact > prefix > substring > sequence-similarity. | `FuzzyCommandIndex` |
| `form <command>` | Walks the operator through an interactive parameter form for commands with many flags (currently `phishing`, `venom`, `evil`). Validates required fields and `options` enums; falls back to defaults under non-interactive IO. | `InteractiveForm`, `FormSpec` |
| `status_tail [target]` | Parses the latest `sessions/scan_<target>.partial`/`.nmap` and prints open ports, percent complete and last line so the operator can monitor a long scan without leaving the shell. | `LiveStatusTail` |
| `grep_log <pattern> [--cmd <name>]` | Regex search across the recent transcript of executed commands and their outputs. Persists across restarts (`sessions/_cli_transcript.jsonl`). | `TranscriptStore` |
| `reload_addons` | Polls `lazyaddons/` and `plugins/` and re-registers anything that changed since the last sweep, without restarting the shell. | `AddonHotReloader` |
| `audit_complete_keys <command> [partial]` | Surfaces what the payload-aware completer would suggest for a given command. Useful to verify completion behaviour. | `PayloadAwareCompleter` |
| `completedefault` (Tab) | Cmd2 hook now falls through to a payload-aware completer that suggests payload keys for `set`/`assign`, IP values for `target`, wordlist keys for `gobuster`/`ffuf`, addon names for `run`, plugin names for `plugin`, and captured credentials for `evil`/`cme`/`secretsdump`. | `PayloadAwareCompleter` |
| Dynamic alias resolution | `cli/aliases.py` now defaults to `lazy=True`: alias templates keep their `{rhost}`/`{lhost}`/etc. placeholders and are rendered against `self.params` at execution time. `set rhost X` propagates to every alias on the next keystroke (no shell restart). Pre-substitution is still available with `lazy=False`. | `DynamicAliasResolver`, `cli/aliases.py` |

The primitives are framework-agnostic and depend on small `typing.Protocol`
interfaces (`PayloadProvider`, `CommandLister`, `TerminalIO`) so they can be
unit-tested in isolation. See `tests/test_cli_enhancements.py` (36 tests).

### Fuzzy dropdown autocomplete

The cmd2 shell installs a curses-driven fuzzy picker on top of GNU readline
(`cli/fuzzy_picker.py`). On a single **Tab** press, when two or more
completions are available, the picker opens a bordered dropdown anchored at
the bottom of the terminal showing every match alongside its description.
The scorer favours exact, prefix and subsequence matches over substring and
similarity (the same ranking the standalone `fz` command uses), and the
matched characters of the query are highlighted in each row so the operator
can see *why* a candidate is in the list.

Navigation: **↑ / ↓** to move, **Page Up / Page Down** to jump, **Home /
End** to seek, **Backspace** to edit the query in place, **Tab** or
**Enter** to insert the highlighted command into the prompt, **Esc** or
**Ctrl-C** to cancel. When only one candidate matches, readline's normal
auto-insert behaviour is preserved so the picker never gets in the way of a
fast operator. Geometry, colors and glyphs are driven by `PickerConfig`,
and an optional `fuzzy_picker` block in `payload.json` can override any of
its fields (e.g. `"max_visible_rows": 8`) without touching code.

### Configurable Neon Box prompt — `config_banner`

The cmd2 shell renders a three-line *Neon Box* prompt assembled from a
canonical set of segments (`user_host`, `iface`, `lhost`, `rhost`,
`domain`, `public_ip`, `cwd`, `git`, `venv`, `time`, `kernel`, `version`,
`battery_load`). The renderer is implemented in `cli/banner_config.py` as
a small SOLID stack: one `SegmentRenderer` per piece of information, a
`SegmentRegistry`, a `BannerSettings` value object, and a `BannerRenderer`
that emits ANSI-colored output. Public IP, kernel release and the LazyOwn
version are TTL-cached so the prompt stays sub-millisecond after the first
render.

The `config_banner` shell command opens a **Powerlevel10k-style curses
wizard** with three tabs — **Segments**, **Colors**, **Glyphs** — and a
live preview of the resulting prompt anchored at the bottom of the panel.
**Tab / Shift+Tab** cycle tabs; **↑ / ↓** move within the active tab;
**Enter** saves to `payload.json` under the `banner` block; **Escape**
cancels. Per-tab bindings:

| Tab | Action keys |
|-----|-------------|
| **Segments** | `Space` toggles a segment on/off; `a` enables every segment; `n` disables every segment; `d` restores factory defaults. |
| **Colors** | `Space` / `→` cycles to the next named color (`bright_green`, `bright_cyan`, `bright_magenta`, …); `←` cycles back; `d` restores that segment's default color. |
| **Glyphs** | `Space` / `→` cycles to the next character for the focused slot (`top_left`, `vertical`, `bullet_primary`, `arrow`, `prompt_char_user`, …); `←` cycles back; `d` restores that slot's default glyph. |

The shell prompt refreshes immediately after save — no restart needed.
Operators with no TTY (CI, scripts) can still drive the system with
`config_banner show` and `config_banner reset`, or hand-edit the payload:

```json
"banner": {
  "enabled": ["user_host", "iface", "rhost", "domain", "cwd", "git", "venv", "time"],
  "colors":  {"user_host": "bright_green", "rhost": "bright_red", "domain": "bright_yellow"},
  "glyphs":  {"top_left": "┌", "bottom_left": "└", "horizontal": "─", "vertical": "│",
              "bullet_primary": "❯", "arrow": "→"}
}
```

Color names are validated against `ColorRegistry` and glyph characters
against `GlyphRegistry`; anything unknown silently falls back to the
factory default so a malformed payload never breaks the prompt.

### Graph-aware navigation — operator + agent UX from graphify

`cli/graph_advisor.py` loads the knowledge graph produced by
[`/graphify`](https://graphify.dev) over the LazyOwn source tree
(`graphify-out/graph_lazyown.json` — ~1500 nodes, ~2900 edges, 14
communities) and exposes it to both the cmd2 shell and the MCP server. The
advisor is a single-file SOLID stack — `GraphLoader` (mtime-cached file
IO), `GraphIndex` (in-memory adjacency / degree / community indexes),
`GraphScorer` (pure ranking primitive), `GraphAdvisor` (orchestrator) —
with every constant kept on the `GraphAdvisorConfig` dataclass.

**Operator commands (cmd2 shell)**

| Command | Purpose |
|---------|---------|
| `graph_search <query> [limit]` | Fuzzy search nodes by label, id or source file. |
| `neighbors <node> [depth] [limit]` | Walk the graph outward from a node with edge relation / confidence. |
| `god_nodes [N]` | Show the most-connected nodes — the framework's core abstractions. |
| `suggest_next [seeds…] [N]` | Recommend the next commands by walking outward from recent activity. With no seeds it reads `sessions/LazyOwn_session_report.csv` and seeds from there. |

The shell's `default()` hook now feeds unknown `do_*` commands through the
same advisor + the existing `FuzzyCommandIndex` so an operator who types
`ddo_lazynmap` instantly sees *"Did you mean: do_lazynmap, do_lazynmap_quick, …?"*
before the toast.

**MCP tools (Claude Code, Claude web, any MCP agent)**

| Tool | Purpose |
|------|---------|
| `lazyown_graph_summary` | Node / edge / community counts and the resolved graph path. |
| `lazyown_graph_search` | Fuzzy node search with a `budget_tokens` cap so the JSON response never blows the agent's context window. |
| `lazyown_graph_neighbors` | Layered adjacency walk with edge relation and confidence — the canonical "what does X depend on?" query. |
| `lazyown_graph_suggest_next` | Next-step recommendation; takes an explicit `recent` list or reads the session transcript. |

Every MCP graph tool trims list fields in place to fit `budget_tokens`
(default 1500). When the graph is missing, every tool returns
`{"available": false, "reason": "..."}` instead of crashing — the operator
is told to run `/graphify .` once and everything starts working.

The advisor caches by `(path, mtime)` so a fresh `/graphify` rebuild is
picked up automatically on the next CLI command or MCP call without
restarting the shell or the MCP server. See
`tests/test_graph_advisor.py` for the 20 unit tests covering loader,
index, scorer and the full advisor API.

### Inline reactive hints — non-blocking next-step suggestions

`cli/reactive_hints.py` hooks into the cmd2 post-command pipeline via
`register_postcmd_hook` and prints a single dim line below every command
output, before the next prompt appears:

```
  ↳ do_gobuster · do_enum4linux · do_ffuf
```

The suggestion comes from the graphify knowledge graph (same `GraphAdvisor`
used by `suggest_next`), so it is structurally grounded — not a generic list.
The hook is fully non-blocking: it returns before cmd2 renders the prompt, so
the operator can start typing the next command immediately.

**Control**

| Action | How |
|--------|-----|
| Disable hints for the session | `set enable_inline_hints false` |
| Re-enable | `set enable_inline_hints true` |
| Persist permanently | `set enable_inline_hints false` then `save` |

Commands on the skip list (`help`, `?`, `exit`, `set`, `show`, `palette`,
`dashboard`, `suggest_next`, `graph_search`, `neighbors`, `god_nodes`) never
produce a hint line — they are meta-commands where a suggestion adds noise.

When the graphify graph is absent the hook returns silently. Run
`/graphify .` once to build the graph and hints start appearing on the very
next command.

### Operator TUI dashboard — `dashboard`

`cli/dashboard_tui.py` is a full-screen [Textual](https://textual.textualize.io)
dashboard launched from the shell with:

```
dashboard
```

It blocks the shell while open (like `htop` or `lazygit`). Press **Q** or
Ctrl-C to close and return to the cmd2 prompt.

**Layout**

```
┌─ LazyOwn RedTeam Dashboard ─────────────────────────────────────────────────┐
│ TARGET 10.10.11.5  ATTACKER 10.10.14.5  DOMAIN target.htb  PHASE RECON  OS  │
├─────────────────────┬─────────────────────────────────┬─────────────────────┤
│  Kill Chain         │  Recent Commands                │  Ops                │
│  ✔ Recon            │  ● lazynmap        2026-05-11   │  Objective:         │
│  ▶ Enum             │  ● ping            2026-05-11   │  Initial Access     │
│  ○ Exploit          │  ● gobuster        2026-05-11   │                     │
│  ○ PrivEsc          │                                 │  Credentials: 0     │
│  ○ Lateral          │                                 │  Hashes: 0          │
│  ○ Exfil            │  Config                         │  Beacons: 0         │
│  ○ Report           │  Target: 10.10.11.5             │                     │
│                     │  C2 Port: 4444                  │                     │
├─────────────────────┴─────────────────────────────────┴─────────────────────┤
│  ↳ next: do_gobuster · do_enum4linux · do_ffuf · do_nikto                   │
└──────────────────────────────────── [Q] Quit  [R] Refresh  [?] Help ────────┘
```

**Data sources** (auto-refreshed every 5 seconds)

| Panel | Source |
|-------|--------|
| Target / phase / OS | `payload.json`, `sessions/world_model.json` |
| Kill chain progress | `sessions/world_model.json` → `completed_phases` |
| Recent commands | `sessions/LazyOwn_session_report.csv` |
| Objective | `sessions/world_model.json`, `sessions/tasks.json` |
| Credentials / hashes | `sessions/credentials*.txt`, `sessions/hash*.txt` |
| Beacons | `sessions/beacons.json` |
| Graph hints | `graphify-out/graph_lazyown.json` |

Requires `pip install textual` (added to `install.sh`).

### Command palette and graph-aware discovery

The `lazyown_palette` MCP tool (also reachable as the `palette` CLI command
and the `/palette` web view, with a global **Ctrl+K / Cmd+K** overlay on
every C2 page) lets agents and operators browse the 422+ `do_*` commands
without scrolling. Modes:

| Mode | Example | Description |
|------|---------|-------------|
| Overview | `palette` | Phase-by-phase command counts. |
| Phase | `palette recon` | Every command in a kill-chain phase, with a one-line summary. |
| Phase + filter | `palette enum nmap` | Phase listing narrowed by a free-text query. |
| Search | `palette --search ldap` | Fuzzy search across name and summary. |
| Detail | `palette --info do_lazynmap` | Full entry **plus graphify-derived `calls` and `related` neighbours** (which other commands share helper functions with this one). |
| Next phase | `palette --next recon` | Recommended commands in the phase that follows in the kill-chain ordering. |

The detail view's `calls` / `related` lists come from
`graphify-out/graph_lazyown.json` (re-generated by the `graphify` skill);
when that file is absent the palette degrades silently to phase data only.

---
