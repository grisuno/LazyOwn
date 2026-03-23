# LazyOwn Skills — MCP Integration

Connect Claude Code (and Claude web) to the full LazyOwn framework via the Model Context Protocol.

## Files

| File | Purpose |
|------|---------|
| `lazyown_mcp.py` | MCP server — exposes 67 LazyOwn tools to Claude |
| `lazyown.md` | Claude Code skill / slash-command documentation |
| `lazyown_policy.py` | Reward-based policy engine for the auto_loop |
| `lazyown_facts.py` | Structured fact extraction from nmap XML and tool output |
| `lazyown_objective.py` | Objective queue + soul.md management |
| `lazyown_llm.py` | LLM bridge: Groq native tool-call + Ollama ReAct |
| `lazyown_automapper.py` | Auto-discovery of addons/tools/plugins as dynamic MCP tools |
| `lazyown_parquet_db.py` | Parquet knowledge base: session history + GTFOBins + LOLBas + ATT&CK |
| `lazyown_campaign.py` | Campaign store: multi-target engagement tracking |
| `mcp_restart.sh` | Restart helper for the MCP server process |

---

## Quick Start

### 1. Register the MCP server in Claude Code

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

### 2. Install the slash command (optional)

```bash
cp skills/lazyown.md ~/.claude/commands/lazyown.md
```

### 3. Use from Claude Code

After restarting Claude Code, all `lazyown_*` tools are available.
Type `/lazyown` to load the full skill prompt.

```
You: set target to 10.10.11.78 and start the autonomous loop
Claude: [calls lazyown_set_config → lazyown_auto_loop]
```

---

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `LAZYOWN_DIR` | parent of `skills/` | LazyOwn root directory |
| `LAZYOWN_C2_HOST` | `payload.json lhost` | C2 server address |
| `LAZYOWN_C2_PORT` | `payload.json c2_port` | C2 server port |
| `LAZYOWN_C2_USER` | `payload.json c2_user` | C2 username |
| `LAZYOWN_C2_PASS` | `payload.json c2_pass` | C2 password |

---

## All MCP Tools (67)

Tools are grouped by function. All names are prefixed `lazyown_`.

### Core Execution

| Tool | Description |
|------|-------------|
| `run_command` | Execute any LazyOwn shell command (or newline-separated list of commands) |
| `get_config` | Read the current payload.json configuration |
| `set_config` | Write a single key-value pair to payload.json |
| `list_modules` | List all modules and scripts in `modules/` |
| `discover_commands` | Discover all commands available in the LazyOwn shell (builtins, plugins, addons, adversaries) |
| `command_help` | Get full documentation for any LazyOwn command: `help <command>` |

### Target Management

| Tool | Description |
|------|-------------|
| `add_target` | Add or update a target in payload.json's `targets` list |
| `list_targets` | List all targets with IP, domain, ports, status, tags, and notes |
| `set_active_target` | Set a target from the list as active — updates `rhost`, `domain`, and related fields |

### C2 / Implant Control

| Tool | Description |
|------|-------------|
| `c2_command` | Task a beacon connected to the LazyOwn C2 server |
| `c2_status` | C2 health check + dashboard data |
| `get_beacons` | List connected beacons/implants |
| `run_api` | Execute a shell command on the C2 host via `/api/run` REST endpoint |
| `c2_profile` | Show, set, or list malleable C2 profiles (sleep, jitter, HTTP headers, URI paths) |
| `c2_vuln_analysis` | Ask the C2 AI (Groq) to analyse a vulnerability or CVE |
| `c2_redop` | Ask the C2 AI (Groq) to plan a red team operation |
| `c2_search_agent` | Delegate a research query to the C2 AI search agent (OSINT, technique lookup) |
| `c2_script` | Ask the C2 AI (Groq) to generate an exploit or pentest script |
| `c2_adversary` | Emulate a MITRE ATT&CK adversary or technique via the C2 AI |

### Session Awareness (C2 Implant State)

| Tool | Description |
|------|-------------|
| `session_status` | Live C2 implant view: OS/user/hostname/IPs, privileged vs unprivileged, discovered hosts, campaign tasks. Reads `sessions/{client_id}.log` CSVs directly — no lazyc2.py dependency |
| `list_sessions` | Browse files in `sessions/` directory |
| `read_session_file` | Read any file in `sessions/` |
| `session_state` | Aggregated session state: phase, discovered hosts, ports, credentials, last command |

### Autonomous Loop & Policy

| Tool | Description |
|------|-------------|
| `auto_loop` | Autonomous attack loop: policy recommendation → command resolution → execute → observe → repeat. Supports reactive injection, bridge catalog, LLM fallback, parquet history |
| `policy_status` | Policy engine episode summary: accumulated reward, phase, next-action recommendations per target |
| `recommend_next` | Ask Groq to recommend the best 3-5 next commands ranked by confidence |

### Reactive Intelligence

| Tool | Description |
|------|-------------|
| `reactive_suggest` | Parse raw command output → prioritised reactive decisions. Detects: AV/EDR blocks (evasion via amsi.yaml/darkarmour), privesc hints (SUID/sudo/polkit → adversary_yaml/lazypwn), credentials, new hosts, service versions, shell errors |
| `bridge_suggest` | Query the full LazyOwn command catalog (347 commands, 11 kill-chain phases, MITRE-mapped) for the best command given phase, services, OS, tags. Supports single suggestion, sequence (next 5), list_all, catalog_summary |

### Objectives & Planning

| Tool | Description |
|------|-------------|
| `inject_objective` | Inject a high-level attack objective into the queue. Primary reasoning entry point for the frontier model |
| `next_objective` | Return the full frontier-model context: soul.md + top objective + world state + session facts + timeline |
| `soul` | Read or update `sessions/soul.md` — agent persona, campaign objective, priority order, hard stops |
| `read_prompt` | Read `prompt.md` — full architecture reference for the developer |

### Knowledge Bases

| Tool | Description |
|------|-------------|
| `parquet_query` | Query the Parquet knowledge base: session history, GTFOBins, LOLBas, MITRE ATT&CK techniques. Modes: `session`, `keyword`, `context`, `stats`, `list` |
| `parquet_annotate` | Annotate a session row in `session_knowledge.parquet` with actual outcome after execution |
| `facts_show` | Show structured facts extracted from nmap XML and tool output: open ports, services, credentials, access level. Optionally re-parse sessions/ |
| `cve_search` | Search NVD for CVEs matching product + optional version. Results cached on disk |
| `searchsploit` | Search public exploits by CVE ID or service/version. Uses searchsploit CLI, falls back to ExploitDB API |
| `rag_index` | Incrementally index all sessions/ artefacts into ChromaDB (falls back to keyword search). mode: `incremental` (default) or `full`. Returns file/chunk counts. Install: `pip install chromadb` |
| `rag_query` | Semantic search over indexed sessions/ artefacts (logs, scans, credentials, XMLs, etc.). Falls back to keyword search when ChromaDB is unavailable. Enriches auto_loop thought prompts |
| `threat_model` | Build or load the blue team threat model from session data. Maps commands to MITRE ATT&CK, scores assets by risk, produces IOC registry and Sigma-lite detection rules. Saved to `sessions/reports/threat_model.json` |

### Memory & Learning

| Tool | Description |
|------|-------------|
| `memory_recall` | Query episodic memory for past command executions relevant to a goal |
| `memory_store` | Explicitly save a command execution to episodic memory (auto_loop saves automatically) |
| `eval_quality` | LLM decision quality report: success rate, top/worst MITRE tactics, confidence calibration |

### Campaign & Reporting

| Tool | Description |
|------|-------------|
| `campaign` | Manage a pentest campaign: group targets under a named engagement, CIDR scope, per-host phase tracking, export |
| `campaign_tasks` | CRUD on `sessions/tasks.json` — list/add/update tasks with status workflow: New → Refined → Started → Review → Qa → Done / Blocked |
| `generate_report` | Auto-generate a structured Markdown pentest report from facts, events, credentials, objectives, and timeline |
| `misp_export` | Export session findings as a MISP-compatible event JSON (WorldModel hosts, services, credentials, CVEs) |
| `collab_publish` | Broadcast a structured event to all connected operators via SSE (shared team awareness) |
| `timeline` | Generate or return the AI-written red-team timeline narrative (Groq reads all session events → prose summary) |

### Playbooks

| Tool | Description |
|------|-------------|
| `playbook_generate` | Generate a MITRE ATT&CK-grounded playbook from STIX2 technique data and Atomic Red Team tests |
| `playbook_run` | Execute a playbook YAML against the target step by step (dispatches each step as an MCP command) |

### Addons, Tools & Plugins

| Tool | Description |
|------|-------------|
| `list_addons` | List all YAML addons in `lazyaddons/`: name, enabled, description, repo URL |
| `list_plugins` | List all Lua plugins in `plugins/`: name, enabled, description |
| `create_addon` | Create a new YAML addon — integrates any GitHub tool into LazyOwn immediately |
| `create_tool` | Create a new pwntomate `.tool` file — applied automatically to matching services on future scans |

### Scheduling & Automation

| Tool | Description |
|------|-------------|
| `cron_schedule` | Schedule any LazyOwn command at HH:MM using the built-in cron system. Acts as a time-motor for autonomous activities (add/list/remove) |
| `daemon` | Manage the unified background daemon: file watcher + event engine + heartbeat in a single process |

### AI Agents & Delegation

| Tool | Description |
|------|-------------|
| `run_agent` | Delegate a goal to an autonomous AI sub-agent (Groq or Ollama) that runs LazyOwn commands independently until complete |
| `agent_status` | Check status of a running or completed sub-agent: status, iterations, last action |
| `agent_result` | Read the full result of a completed sub-agent: final answer + complete action log |
| `list_agents` | List recent sub-agents with status, goal, backend, and iteration count |
| `llm_ask` | Ask a satellite LLM (Groq or local deepseek-r1:1.5b) to reason about a goal using LazyOwn tools |

### Event Engine

| Tool | Description |
|------|-------------|
| `poll_events` | Read events from the LazyOwn Event Engine (generated when command patterns match detection rules) |
| `ack_event` | Mark an event as processed so it won't appear in future polls |
| `add_rule` | Add or update an event detection rule (define what patterns trigger which events) |
| `heartbeat_status` | Check whether the LazyOwn Heartbeat process is running (PID + event counts) |

---

## Architecture

```
Claude (frontier model)
       |
       | MCP protocol
       v
lazyown_mcp.py  ──────────────────────────────────────────────────────┐
  auto_loop                                                            │
    ├── OS detection gate (ping TTL -> os_id -> payload.json)         │
    │     linux: TTL<=64  |  windows: TTL<=128  |  unknown: skip      │
    ├── policy engine (lazyown_policy.py)                             │
    ├── reactive engine (modules/reactive_engine.py)                  │
    │     detects AV/EDR, privesc hints, creds, new hosts             │
    ├── bridge catalog (modules/lazyown_bridge.py)                    │
    │     347 commands × 11 phases × MITRE mapping × os_hint filter   │
    ├── parquet knowledge (lazyown_parquet_db.py)                     │
    │     session history + GTFOBins + LOLBas + ATT&CK techniques     │
    ├── LLM recommender (lazyown_llm.py — Groq / Ollama)             │
    └── session reader (modules/session_reader.py)                    │
          reads sessions/{client_id}.log CSVs from lazyc2.py          │
                                                                       │
LazyOwn framework ─────────────────────────────────────────────────────┘
  lazyown.py (shell)         pwntomate.py (parallel service exploitation)
    do_ping -> sessions/os.json -> self.params["os_id"]               │
    run_lazynmap -> gates on sessions/os.json, runs ping if unknown   │
  lazyc2.py (C2 server)                                               │
    beacon POST -> client (OS string) -> sessions/os.json             │
                                      -> sessions/world_model.json    │
  autonomous_daemon.py                                                 │
    _detect_target_os() -> payload.json os_id                         │
                        -> sessions/os.json (same format as do_ping)  │
                        -> world_model.os_hint                        │
  lazyaddons/ (YAML tools)  lazyadversaries/ (privesc YAML)
  plugins/ (Lua)            modules/ (Python modules)
  parquets/ (techniques, binarios, lolbas_index)
  sessions/ (implant CSVs, task board, discovered hosts, os.json)
```

### Kill-chain phase order (bridge catalog)

```
os_detect → recon → enum → exploit → postexp → cred → lateral → privesc → persist → exfil → c2 → report
```

### OS detection (pre-recon)

The autonomous daemon probes the target with a single ICMP packet before any tool
selection occurs. The TTL value determines the platform:

| TTL range | Inferred OS |
|-----------|-------------|
| <= 64 | Linux / Unix / macOS |
| 65 – 128 | Windows |
| > 128 | Unknown / network device |

The result is written to `world_model.json` as `os_hint` and propagated to the
bridge catalog (`os_hint` filter), fallback selector (OS-specific tool map), and
reactive engine (platform argument). Commands such as `winpeas`, `evil-winrm`,
and Kerberos tooling are never dispatched against Linux targets, and vice-versa.

### Reactive decision priority

| Priority | Action | Trigger |
|----------|--------|---------|
| 1 | `escalate_evasion` | AMSI / Defender / CrowdStrike detected in output |
| 1 | `run_command` | sudo NOPASSWD / SUID / polkit / token impersonation found |
| 2 | `record_cred` | Password or NTLM hash extracted from output |
| 3 | `add_host` | New RFC1918 IP discovered in output |
| 3–4 | `switch_tool` | Connection refused / auth failed / command not found |

---

## Supported Modules (modules/)

| Module | Role |
|--------|------|
| `obs_parser.py` | Parse tool output into typed findings (SERVICE_VERSION, CVE, PATH, CRED, ERROR) |
| `world_model.py` | Track engagement state: hosts, services, credentials, phase |
| `reactive_engine.py` | Signal detection + reactive decision generation |
| `session_reader.py` | Read C2 implant CSVs, task board, discovered hosts |
| `lazyown_bridge.py` | Full command catalog with phase/service/OS/tag/MITRE metadata |
| `event_engine.py` | Rule-based event detection over LazyOwn command output |
| `recommender.py` | Groq/Ollama command recommendation |
| `timeline_narrator.py` | AI-written timeline narration |
| `session_state.py` | Aggregated session state snapshot |
| `session_rag.py` | ChromaDB/keyword RAG over sessions/ artefacts — incremental indexing, semantic search, auto_loop context injection |
| `threat_model.py` | Blue team threat model builder: assets × risk scores, MITRE TTPs, IOC registry, Sigma-lite detection rules |

---

## Running Tests

```bash
python3 -m pytest tests/test_core_modules.py -v
# Expected: 60 tests passing
```
