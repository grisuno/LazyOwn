# LazyOwn Framework — Skill

You are operating the **LazyOwn** red-team framework via its MCP tools.
LazyOwn is a penetration testing / C2 framework located at `/home/grisun0/LazyOwn`.

---

## STEP 0 — At the start of EVERY operator shift: Campaign SITREP

```python
lazyown_campaign_sitrep()
```

This single call reads **all 10 campaign state files** and returns a structured briefing:
`WORLD MODEL → SESSION JSON (creds/implants) → CRED FILES → TASKS → OBJECTIVES → CAMPAIGN → LESSONS → DAEMON → AUTO EVENTS → CSV STATS`

Use this before any decision. Never fly blind.

---

## MANDATORY: Call `lazyown_session_init` FIRST

**At the start of every session**, call `lazyown_session_init()` before anything else.
It returns a full **SITREP** (situation report):
- Active config (rhost, domain, lhost, os_id)
- OS cross-reference: what payload.json says vs what nmap actually found — flags conflicts
- Nmap scan evidence: checks `sessions/scan_{rhost}.nmap` and `sessions/vulns_{rhost}.nmap` already exist
- Pwntomate output: checks `sessions/{rhost}/{port}/{tool}/` dirs already exist
- Tasks from `sessions/tasks.json` — what's pending vs done
- Active objectives from `sessions/objectives.jsonl`
- Engagement phase from `world_model.json`
- Phase-relevant commands from bridge catalog

**Do not re-run nmap or pwntomate if the files already exist** — read them instead.

---

## Command Abstraction Model — Critical Understanding

LazyOwn CLI commands are **high-level abstractions** over real security tools.
They **automatically inject** values from `payload.json` — you NEVER write raw tool commands.

```
payload.json  ──► LazyOwn CLI command ──► real underlying tool + full optimized flags
     rhost              nmap               nmap -sC -sV -p- -T4 --script vuln 10.10.11.5
     domain             ww                 whatweb http://target.htb -a 3
     domain             dig                dig @10.10.11.5 target.htb axfr
     rhost+wordlist     gobuster           gobuster dir -u http://10.10.11.5 -w /path/wordlist
     rhost+creds        psexec             impacket-psexec user:pass@10.10.11.5
     domain+creds       bh                 bloodhound-python -d target.htb -u user ...
     rhost+creds        evil               evil-winrm -i 10.10.11.5 -u user -p pass
```

**Workflow:**
1. Set config: `lazyown_set_config(key='rhost', value='10.10.11.5')`
2. Discover commands for your phase: `lazyown_discover_commands(phase='recon')`
3. Get docs for a command: `lazyown_command_help(command='lazynmap')`
4. Run the abstract command: `lazyown_run_command('nmap')`

**Kill chain (11 phases):**
`recon → enum → exploit → postexp → persist → privesc → cred → lateral → exfil → c2 → report`

Only use commands from the CURRENT phase. Don't run post-exploitation tools during recon.

---

## Core MCP Tools (92)

### Campaign Intelligence (call at shift start)

| Tool | Purpose |
|------|---------|
| `lazyown_campaign_sitrep` | **MASTER SITREP** — aggregates world_model + tasks + objectives + creds + lessons + daemon into one briefing |
| `lazyown_credentials` | All captured creds from credentials*.txt + sessionLazyOwn.json + world_model — deduped table |
| `lazyown_c2_notes` | Read/append/clear operational notes in sessionLazyOwn.json — shift handoff commentary |
| `lazyown_report_update` | Read or update PDF report fields in static/body_report.json; `auto_fill` generates exec summary from session data |
| `lazyown_campaign_lessons` | Read tactical lessons derived from campaign milestones — avoid repeating mistakes |

### Session Init (call FIRST)

| Tool | Purpose |
|------|---------|
| `lazyown_session_init` | **CALL FIRST** — returns phase, config, phase commands, objectives, abstraction cheatsheet |

### Execution & Configuration

| Tool | Purpose |
|------|---------|
| `lazyown_run_command` | Run any LazyOwn shell command (or newline-separated list) |
| `lazyown_get_config` | Read current payload.json settings |
| `lazyown_set_config` | Write a key-value pair to payload.json |
| `lazyown_list_modules` | List modules/ contents |
| `lazyown_discover_commands` | List commands by pentest phase (use `phase='recon'`/`'enum'`/etc) OR all shell commands |
| `lazyown_command_help` | Get full docs for any command: `help <command>` |

### Target Management

| Tool | Purpose |
|------|---------|
| `lazyown_add_target` | Add/update a target with IP, domain, ports, status, notes, tags |
| `lazyown_list_targets` | List all targets (optional status filter) |
| `lazyown_set_active_target` | Activate a target — updates rhost/domain in payload.json |

### C2 / Implant Control

| Tool | Purpose |
|------|---------|
| `lazyown_c2_command` | Task a specific beacon connected to the C2 server |
| `lazyown_c2_status` | C2 health check + dashboard data |
| `lazyown_get_beacons` | List connected beacons/implants |
| `lazyown_run_api` | Execute a command on the C2 host via `/api/run` REST endpoint |
| `lazyown_c2_profile` | Show, set, or list malleable C2 profiles (sleep, jitter, HTTP headers, URIs) |
| `lazyown_c2_vuln_analysis` | Ask C2 AI (Groq) to analyse a vulnerability or CVE |
| `lazyown_c2_redop` | Ask C2 AI to plan a red team operation |
| `lazyown_c2_search_agent` | Delegate an OSINT/research query to the C2 AI search agent |
| `lazyown_c2_script` | Ask C2 AI to generate an exploit or pentest script |
| `lazyown_c2_adversary` | Emulate a MITRE ATT&CK adversary or technique via the C2 AI |

### Session Awareness

| Tool | Purpose |
|------|---------|
| `lazyown_session_status` | Live implant view: OS/user/hostname/IPs, privileged vs unprivileged, discovered hosts, campaign tasks. Reads `sessions/{client_id}.log` CSVs directly |
| `lazyown_session_state` | Aggregated state snapshot: phase, hosts, ports, creds, last command |
| `lazyown_list_sessions` | Browse files in `sessions/` |
| `lazyown_read_session_file` | Read any file from `sessions/` |

### Autonomous Loop & Policy

| Tool | Purpose |
|------|---------|
| `lazyown_auto_loop` | Autonomous attack loop: reactive → parquet → bridge → SWAN → LLM → fallback → execute → learn (max 20 steps) |
| `lazyown_policy_status` | Policy engine episode summary + next-action recommendations per target |
| `lazyown_recommend_next` | Ask Groq to recommend the best 3-5 next commands ranked by confidence |

### Reactive Intelligence

| Tool | Purpose |
|------|---------|
| `lazyown_reactive_suggest` | Parse raw output → prioritised decisions: AV/EDR evasion, privesc hints, creds, new hosts, switch-tool. Priority ≤2 auto-injected into next auto_loop step |
| `lazyown_bridge_suggest` | Query the full command catalog (347 commands, 11 phases, MITRE-mapped). Modes: single, sequence, list_all, catalog_summary. Params: phase, services, os_hint, tag_hint |

### Objectives & Planning

| Tool | Purpose |
|------|---------|
| `lazyown_inject_objective` | Inject a high-level attack objective into the queue |
| `lazyown_next_objective` | Return full frontier-model context: soul + top objective + world state + facts + timeline |
| `lazyown_soul` | Read or update `sessions/soul.md` — persona, objective, hard stops, guardrails |
| `lazyown_read_prompt` | Read `prompt.md` — full architecture reference |

### Knowledge Bases

| Tool | Purpose |
|------|---------|
| `lazyown_parquet_query` | Query Parquet knowledge base: session history, GTFOBins, LOLBas, MITRE ATT&CK. Modes: session, keyword, context, stats, list |
| `lazyown_parquet_annotate` | Annotate a session row in `session_knowledge.parquet` with actual outcome |
| `lazyown_facts_show` | Structured facts from nmap + tool output: ports, services, creds, shares, access level |
| `lazyown_cve_search` | Search NVD for CVEs matching product + optional version (cached on disk) |
| `lazyown_searchsploit` | **Multi-source vuln search** wrapping `ss` command: searchsploit+NVD+ExploitAlert+PacketStorm+Pompem+Metasploit(opt). Use after ANY service version is discovered. |
| `lazyown_rag_index` | Incrementally index all sessions/ artefacts into ChromaDB (or keyword fallback). mode: `incremental` (default) / `full`. Persists between process restarts. Install: `pip install chromadb` |
| `lazyown_rag_query` | Semantic search over indexed sessions/ (logs, scans, creds, XML, etc.). Falls back to keyword search. Used automatically by auto_loop on every step |
| `lazyown_threat_model` | Build/load the blue team threat model: assets + risk scores, MITRE TTPs, IOC registry, Sigma-lite rules, purple team mapping. actions: `build`, `load`, `ttps`, `rules`, `iocs`, `purple`, `gaps` |

### Memory & Learning

| Tool | Purpose |
|------|---------|
| `lazyown_memory_recall` | Query episodic memory for past command executions relevant to a goal |
| `lazyown_memory_store` | Explicitly save a command execution to episodic memory |
| `lazyown_eval_quality` | LLM decision quality report: success rate, top/worst MITRE tactics, confidence calibration |

### Campaign & Reporting

| Tool | Purpose |
|------|---------|
| `lazyown_campaign` | Manage a pentest campaign: multi-target engagement, CIDR scope, per-host phase tracking |
| `lazyown_campaign_tasks` | CRUD on `sessions/tasks.json` — list/add/update tasks. Status workflow: New → Refined → Started → Review → Qa → Done / Blocked |
| `lazyown_generate_report` | Auto-generate a structured Markdown pentest report from facts, events, creds, objectives, timeline |
| `lazyown_misp_export` | Export session findings as MISP-compatible event JSON (hosts, services, credentials, CVEs) |
| `lazyown_collab_publish` | Broadcast a structured event to all connected operators via SSE |
| `lazyown_timeline` | AI-written red-team timeline narrative (Groq reads all session events → prose summary) |

### Playbooks

| Tool | Purpose |
|------|---------|
| `lazyown_playbook_generate` | Generate a MITRE ATT&CK-grounded playbook from STIX2 technique data and Atomic Red Team tests |
| `lazyown_playbook_run` | Execute a playbook YAML step by step (each step dispatched as an MCP command) |

### Addons, Tools & Plugins

| Tool | Purpose |
|------|---------|
| `lazyown_list_addons` | List all YAML addons in `lazyaddons/`: name, enabled, description, repo |
| `lazyown_list_plugins` | List all Lua plugins in `plugins/`: name, enabled, description |
| `lazyown_create_addon` | Create a new YAML addon — integrates any GitHub tool into LazyOwn immediately |
| `lazyown_create_tool` | Create a new pwntomate `.tool` file — applied automatically to matching services |

### Scheduling & Automation

| Tool | Purpose |
|------|---------|
| `lazyown_cron_schedule` | Schedule any LazyOwn command at HH:MM using the built-in cron system. Acts as time-motor for autonomous activities (add/list/remove) |
| `lazyown_daemon` | Manage the unified background daemon: file watcher + event engine + heartbeat |

### AI Agents & Delegation

| Tool | Purpose |
|------|---------|
| `lazyown_run_agent` | Delegate a goal to an autonomous AI sub-agent (Groq or Ollama) |
| `lazyown_agent_status` | Check status of a running/completed sub-agent: status, iterations, last action |
| `lazyown_agent_result` | Read full result of a completed sub-agent: final answer + complete action log |
| `lazyown_list_agents` | List recent sub-agents with status, goal, backend, iteration count |
| `lazyown_llm_ask` | Ask a satellite LLM (Groq or local deepseek-r1:1.5b) to reason about a goal using LazyOwn tools |

### Event Engine

| Tool | Purpose |
|------|---------|
| `lazyown_poll_events` | Read events from the LazyOwn Event Engine (triggered by command pattern rules) |
| `lazyown_ack_event` | Mark an event as processed so it won't appear in future polls |
| `lazyown_add_rule` | Add or update an event detection rule |
| `lazyown_list_event_rules` | **List all active detection rules** — id, trigger, severity, suggest. Audit before adding new rules. |
| `lazyown_heartbeat_status` | Check whether the Heartbeat process is running (PID + event counts) |

### Hive Mind — Multi-Agent Parallel Execution

| Tool | Purpose |
|------|---------|
| `lazyown_hive_spawn` | Spawn N drones (Groq/Ollama) IN PARALLEL for a goal. Roles: recon, exploit, analyze, cred, lateral, report, generic |
| `lazyown_hive_status` | Full hive status: active drones, ChromaDB vector count, episodic memory entries |
| `lazyown_hive_recall` | Semantic + episodic + long-term memory recall from unified hive ChromaDB |
| `lazyown_hive_plan` | Queen generates task decomposition plan WITHOUT spawning drones — use for previewing |
| `lazyown_hive_result` | Get the full result of a specific hive drone by drone_id |
| `lazyown_hive_collect` | Wait for all drones to finish, return Queen's synthesized summary |
| `lazyown_hive_forget` | Prune hive episodic memory (older than N hours, optional topic filter) |

### SWAN — Mixture of Experts + Reinforcement Learning

| Tool | Purpose |
|------|---------|
| `lazyown_swan_run` | Route a task to the best expert using MoE+RL (Q-learning). Returns expert output + routing metadata |
| `lazyown_swan_route` | **Preview** expert routing WITHOUT executing — shows which expert would be chosen and why |
| `lazyown_swan_ensemble` | Run task with MULTIPLE experts in parallel then synthesize results (highest-confidence answer) |
| `lazyown_swan_status` | MoE expert weights, RL epsilon, per-expert performance EMA and history |

### Autonomous Daemon — Fully Independent Execution

| Tool | Purpose |
|------|---------|
| `lazyown_autonomous_start` | Launch the daemon: 4 asyncio roles (ObjectiveLoop, ExecutionEngine, WorldModelWatcher, DroneCoordinator) |
| `lazyown_autonomous_stop` | Terminate daemon by PID |
| `lazyown_autonomous_status` | Real-time daemon state: phase, current objective, steps completed, active drones |
| `lazyown_autonomous_inject` | Inject a new objective into the queue — daemon picks it up on the next cycle (no restart needed) |
| `lazyown_autonomous_events` | Read last N events from the `autonomous_events.jsonl` stream (STEP_START/DONE, HIGH_VALUE, PHASE_CHANGE) |

### Groq Agent + Atomic Red Team

| Tool | Purpose |
|------|---------|
| `lazyown_groq_agent` | Spawn autonomous Groq/Ollama agent with **21 native LazyOwn tools** — full ReAct loop |
| `lazyown_atomic_search` | Structured search over **1690 Atomic Red Team tests** (techniques_enriched.parquet). Filter by keyword, MITRE ID, platform, complexity |
| `lazyown_fast_run` | Launch LazyOwn full-stack HackTheBox orchestrator: nmap + C2 + auto_loop + Flask + HTTP server + VPN |

---

---

## Required Methodology — Read Before Any Action

### Rule 0 — Always read sessions/ first

**Before launching any tool**, check whether the result already exists:

```
lazyown_list_sessions()                          # full inventory of sessions/
lazyown_read_session_file("scan_<rhost>.nmap")   # read prior nmap if present
lazyown_read_session_file("vulns_<rhost>.nmap")
lazyown_read_session_file("<rhost>/<port>/<tool>/<output>.txt")
lazyown_read_session_file("logs/command_<tool>output<domain>.txt")
```

Scripts emit logs for the agent to analyse.
If a file has content, read and reason over it **before** repeating the same command.
The `sessions/` directory is the authoritative source of campaign state.

### Rule 1 — Identify the target OS before enumeration

Always run `ping` as the first step to detect the OS from the ICMP TTL:

```
lazyown_run_command("ping")   # TTL ~64 -> Linux/Unix | TTL ~128 -> Windows
```

This determines which tool chain to follow (SMB/Kerberos/AD vs SSH/web).
**Do not run AD enumeration against a Linux target. Do not run SSH brute-force against Windows.**

OS detection propagates through the full stack in this order:

1. **Autonomous daemon** (`autonomous_daemon.py`): `_detect_target_os()` probes the target
   via ICMP before the first step. Result is written to `payload.json` (`os_id`) and
   `sessions/os.json` so every fresh LazyOwn shell spawned by the runner picks it up.
2. **LazyOwn shell** (`lazyown.py`): `do_ping` now updates `self.params["os_id"]` in
   memory after writing `sessions/os.json`, so the detection persists in the running session.
   `run_lazynmap` / `do_lazynmap` check `sessions/os.json` before scanning — if OS is
   unknown, they call `ping` automatically.
3. **C2 beacon feedback** (`lazyc2.py`): when a beacon responds, the `client` field (OS
   string from the implant) is written to `sessions/os.json` and `sessions/world_model.json`
   as ground truth, overriding TTL-based heuristics.
4. **Bridge catalog**: `BridgeSelector` passes `os_hint` to `dispatcher.suggest()` so only
   OS-appropriate commands are returned from the 347-command catalog.
5. **Fallback selector**: `_FALLBACK_MAP_LINUX` and `_FALLBACK_MAP_WINDOWS` ensure that
   `linpeas` is never dispatched against Windows, and `winpeas`/`evil-winrm` never against Linux.

### Rule 2 — fast_run_as_r00t.sh runs in the background, no timeout

`fast_run_as_r00t.sh` takes **at least 333 seconds** just to start the auto-loop
(`sleep_start` in payload.json). The full run can take hours.

**Correct way to launch from the MCP:**

```bash
# Background launch — do not block, do not set a short timeout
shell nohup sudo -n bash fast_run_as_r00t.sh --no-attach --vpn 1 \
    > /tmp/fast_run.log 2>&1 &
```

- `--no-attach` prevents `tmux attach` from blocking the process
- The process runs in the tmux session `lazyown_sessions`
- Verify with: `tmux ls` or `tmux has-session -t lazyown_sessions`
- Attach manually: `tmux attach -t lazyown_sessions`

**Never** launch `fast_run_as_r00t.sh` with a timeout of 60 seconds or less.
**Never** wait for its output in a blocking call from the MCP.

### Rule 3 — Read logs generated by pwntomate and auto_loop

While `fast_run_as_r00t.sh` runs in the background, scripts produce:

- `sessions/scan_<ip>.nmap` — full TCP scan
- `sessions/scan_<ip>.nmap.xml` — parseable XML
- `sessions/vulns_<ip>.nmap` — vulnerability scripts
- `sessions/<ip>/<port>/<tool>/*.txt` — pwntomate output per port
- `sessions/logs/command_<tool>output<domain>.txt` — LazyOwn command logs
- `sessions/LazyOwn_session_report.csv` — campaign summary

**Correct cycle:**
1. `lazyown_list_sessions()` — identify files with content (> 0 bytes)
2. `lazyown_read_session_file(filepath)` — read each relevant file
3. Reason over the results — decide the next command
4. If results already answer the question — do not repeat the scan

---

## Workflows

### 1. Configure a target

```
lazyown_set_config(key="lhost", value="10.10.14.5")
lazyown_set_config(key="rhost", value="10.10.11.78")
lazyown_set_config(key="lport", value="4444")
```

### 2. Recon

OS detection must precede service scanning. The ping TTL identifies the platform
so that subsequent tool selection uses the correct OS-specific chain.

```
# Step 1 — OS detection (always first)
lazyown_run_command("ping")           # TTL ~64 -> Linux | TTL ~128 -> Windows

# Step 2 — Network scan (do not kill early, 5-30 min)
lazyown_run_command("lazynmap")       # full TCP scan
lazyown_run_command("hosts_discover")

# Step 3 — Parse findings
lazyown_facts_show(target="10.10.11.78", refresh=True)
```

The autonomous daemon performs OS detection automatically before the first
command selection step and propagates `os_hint` to all selectors.

### 3. Vulnerability Research — MANDATORY after service discovery

**Trigger**: Any time you identify a service version (from nmap, pwntomate, whatweb, wappalyzer, banner grab).
**Never skip this step.** A known CVE may give you direct RCE without further enumeration.

The `lazyown_searchsploit` tool wraps the full `ss` command and queries **9 sources simultaneously**:

| # | Source | What it finds |
|---|--------|--------------|
| 1 | ExploitDB / searchsploit | Offline local exploit database (PoC scripts, shellcode) |
| 2 | NVD (NIST) | CVE details, CVSS scores, affected versions |
| 3 | ExploitAlert | Community exploit repository |
| 4 | PacketStorm Security | Exploit archive (advisories + code) |
| 5 | Metasploit | Ready-to-use msf modules (set include_msf=True) |
| 6 | Pompem | Multi-DB exploit finder, output saved to sessions/ |
| 7 | Default Credentials (creds_py) | Default vendor credentials via DefaultCredsCheatSheet |
| 8 | Sploitus | Reference URL — community CVE/exploit aggregator |
| 9 | exploits.shodan.io | Reference URL — Shodan exploit database |

**Usage pattern — call immediately after seeing a version:**

```python
# After nmap shows: 80/tcp open http Apache httpd 2.4.49
lazyown_searchsploit(query="apache 2.4.49")

# After nmap shows: 21/tcp open ftp vsftpd 2.3.4
lazyown_searchsploit(query="vsftpd 2.3.4")

# SMB service with potential EternalBlue
lazyown_searchsploit(query="smb ms17-010", include_msf=True)

# CVE from vulns scan
lazyown_searchsploit(cve="CVE-2021-41773")

# Web app from whatweb
lazyown_searchsploit(query="Drupal 7.54")

# After whatweb finds PHP version
lazyown_searchsploit(query="php 8.1.0-dev")

# IIS server
lazyown_searchsploit(query="IIS 10.0", include_msf=True)

# OpenSSL version
lazyown_searchsploit(query="openssl 1.0.1")

# AD/Kerberos: after SMB enum finds Windows Server version
lazyown_searchsploit(query="Windows Server 2019 kerberos")
```

**After getting results → decide next step:**
- ExploitDB path found → `lazyown_run_command("ss <term>")` to get full output with file paths
- Metasploit module found → `lazyown_run_command("msfconsole")` then use the module
- CVE confirmed → `lazyown_cve_search(product="...", version="...")` for CVSS + patch info
- No public exploit → continue enumeration, deeper web app testing

**Integration into auto_loop:**
The auto_loop's `BridgeSelector` and `ReactiveSelector` know to call `ss` when service versions
are detected. But when operating manually or when the output is ambiguous, always call
`lazyown_searchsploit` yourself.

### 4. Generate a payload

```
lazyown_run_command("venom")
lazyown_run_command("payload")
```

### 4. Interact with beacons (requires C2 running)

```
lazyown_get_beacons()
lazyown_c2_command(client_id="abc123", command="whoami")
lazyown_c2_command(client_id="abc123", command="softenum")
lazyown_c2_command(client_id="abc123", command="exfil")
```

### 5. Session awareness — live implant state

```
# See all connected implants without touching lazyc2.py
lazyown_session_status()
# → [PRIVILEGED] abc123 | webserver | linux | user=root | ips=10.0.0.5
# → Privileged sessions: 1 | Unprivileged: 2
# → Discovered hosts: 10.0.0.1, 10.0.0.2, 10.0.0.3

# Filter to a specific client
lazyown_session_status(client_id="abc123", show_outputs=True)
```

### 6. Reactive loop — act on command output

```
# Parse any raw output and get prioritised next actions
lazyown_reactive_suggest(
    output="Windows Defender blocked the executable. Access denied.",
    command="meterpreter",
    platform="windows"
)
# → [escalate_evasion] priority=1
#      Command: adversary_yaml amsi
#      Reason: AMSI/Defender detected — bypass before next execution
#      MITRE: T1562

lazyown_reactive_suggest(
    output="User alice may run: (ALL) NOPASSWD: ALL",
    command="sudo -l",
    platform="linux"
)
# → [run_command] priority=1
#      Command: adversary_yaml sudo_nopasswd
#      MITRE: T1548
```

### 7. Bridge catalog — phase-aware command selection

```
# Get the best single command for a phase
lazyown_bridge_suggest(phase="enum", services=["smb", "ldap"], os_hint="windows")

# Get next 5 commands in kill-chain order
lazyown_bridge_suggest(phase="lateral", sequence=True, has_creds=True)

# Filter by technique tag
lazyown_bridge_suggest(phase="enum", tag_hint="kerberos")

# Show the full 347-command catalog summary
lazyown_bridge_suggest(catalog_summary=True)

# List all commands for a phase
lazyown_bridge_suggest(phase="postexp", list_all=True)
```

### 8. Campaign tasks — track progress beyond vulnbot

```
# List all tasks
lazyown_campaign_tasks(action="list")

# Create a task
lazyown_campaign_tasks(
    action="add",
    title="Kerberoast domain service accounts",
    description="Extract SPNs and crack offline with hashcat",
    operator="redteam1"
)
# → Task #0 created: [New] Kerberoast domain service accounts

# Move through the status workflow
lazyown_campaign_tasks(action="update", task_id=0, status="Started")
lazyown_campaign_tasks(action="update", task_id=0, status="Done")

# Filter by status
lazyown_campaign_tasks(action="list", filter_status="Blocked")
```

### 9. Cron scheduling — time-motor for autonomous activities

```
# Schedule recon every morning
lazyown_cron_schedule(action="add", time="08:00", command="lazynmap")

# Schedule a privesc check
lazyown_cron_schedule(action="add", time="14:30", command="adversary_yaml", args="linpeas")

# Schedule lateral movement attempt after recon
lazyown_cron_schedule(action="add", time="09:00", command="enum_smb")

# List scheduled jobs
lazyown_cron_schedule(action="list")

# Remove a job
lazyown_cron_schedule(action="remove", cron_id="a1b2c3d4")
```

### 10b. RAG over session artefacts

```
# Index all sessions/ artefacts incrementally (fast — run from cron)
lazyown_rag_index(mode="incremental")

# Full rebuild after wiping old index
lazyown_rag_index(mode="full")

# Semantic / keyword search over logs, scans, creds, XML, etc.
lazyown_rag_query(query="SMB credentials found", n=5)
lazyown_rag_query(query="nmap open ports 10.10.11.78", n=3)
lazyown_rag_query(query="privilege escalation sudo NOPASSWD", n=5)

# Schedule hourly re-indexing (keeps auto_loop context fresh)
lazyown_cron_schedule(action="add", time="00:30", command="rag_index")
```

Note: install ChromaDB for semantic search (`pip install chromadb`).
Without ChromaDB the fallback keyword index is persisted to
`sessions/keyword_fallback_index.json` and survives process restarts.

### 10c. Threat model — red + blue + purple spectrum

```
# Build the full threat model from LazyOwn_session_report.csv
lazyown_threat_model(action="build")

# Reload last saved model without rebuilding
lazyown_threat_model(action="load")

# List all MITRE ATT&CK TTPs observed in session history
lazyown_threat_model(action="ttps")

# Show Sigma-lite detection rules for each TTP
lazyown_threat_model(action="rules")

# IOC registry: IPs, domains, credentials, hashes
lazyown_threat_model(action="iocs")

# Purple team mapping: red (commands used) + blue (detection rule) side-by-side
lazyown_threat_model(action="purple")

# Coverage gap analysis: TTPs with no detection rule
lazyown_threat_model(action="gaps")
```

Output: `sessions/reports/threat_model.json`

The purple team view shows:
- RED side: LazyOwn commands observed, occurrences, first/last seen
- BLUE side: matching Sigma-lite rule with log_source, condition, blue team response
- GAP marker: TTPs that have no detection rule (prioritised for hardening)

### 10. Parquet knowledge base

```
# Get full context briefing for current phase
lazyown_parquet_query(mode="context", phase="enum", target="10.10.11.78")

# Find GTFOBins/LOLBas entries for a binary
lazyown_parquet_query(mode="keyword", keyword="wget")

# Show past successful commands for privesc
lazyown_parquet_query(mode="session", phase="privesc", target="10.10.11.78", success_only=True)

# List available parquets
lazyown_parquet_query(mode="list")
```

### 11. Objectives — frontier-model reasoning entry point

```
# Set the agent persona and campaign goal
lazyown_soul(action="write", content="Objective: compromise darkzero.htb AD. Priority: credential access, lateral movement. Hard stop: do not exfil PII.")

# Inject a new goal
lazyown_inject_objective(
    title="Gain foothold via SMB relay",
    description="Use responder + ntlmrelayx to relay credentials to WinRM",
    priority=1,
    mitre_tactic="T1557"
)

# Get the full context to plan the next action
lazyown_next_objective()
# → soul.md + top objective + world state + session facts + timeline
```

### 12. Full autonomous attack cycle (policy engine + reactive + parquet)

```
# Bootstrap policy from historical data (run once)
# python3 skills/lazyown_policy.py bootstrap

# Check policy recommendations
lazyown_policy_status(target="10.10.11.78")

# Launch unattended loop — 6-selector cascade per step:
#   1. ReactiveSelector  — last output patterns (AV, privesc, creds, new hosts)
#   2. ParquetSelector   — session_knowledge.parquet proven commands
#   3. BridgeSelector    — 347-command catalog (MITRE-mapped, OS-filtered)
#   4. SWANSelector      — MoE+RL expert routing (AUTO_USE_SWAN=1)
#   5. LLMSelector       — Groq/Ollama recommendation (AUTO_USE_LLM=1)
#   6. FallbackSelector  — static OS-aware maps (always returns a result)
lazyown_auto_loop(
    target="10.10.11.78",
    max_steps=10,
    stop_on_high_value_success=True,
    step_timeout_s=60,   # per command — NOT applied to lazynmap or pwntomate
    step_delay_s=5,
)
# After a successful lazynmap step, auto_loop:
#   1. Detects sessions/scan_<target>.nmap.xml
#   2. Launches pwntomate in background (parallel tools, NO timeout)
#   3. Refreshes FactStore — next commands are parameterised with real data
#   4. Runs reactive_engine on each output — injects evasion/privesc decisions

# For fully autonomous (no Claude needed between objectives):
lazyown_autonomous_start(max_steps_per_objective=15, backend="groq")
lazyown_autonomous_inject(text="Initial recon and foothold on 10.10.11.78", priority="high")
lazyown_autonomous_events(last_n=20)   # monitor progress
```

### 13. Agentic event loop

```
# Start heartbeat daemon
lazyown_daemon(action="start")
lazyown_heartbeat_status()

# Poll for new events
lazyown_poll_events()
# → [a1b2c3d4] CREDENTIALS_CAPTURED  suggest: Check sessions/credentials*.txt
# → [e5f6g7h8] AD_ENUM_STARTED        suggest: Check for domain users/groups

# Act and acknowledge
lazyown_run_command("cat sessions/credentials*.txt")
lazyown_ack_event("a1b2c3d4")

# Teach the engine new detection patterns
lazyown_add_rule({
    "id": "hash_captured",
    "description": "NTLM hash captured via responder",
    "trigger": {"command_contains": "responder", "output_contains": "NTLMv2"},
    "event_type": "HASH_CAPTURED",
    "severity": "high",
    "suggest": "Run hashcat or john on the captured hash."
})
```

### 14. AI Sub-Agents

```
lazyown_run_agent(goal="Enumerate SMB on rhost and list shares", backend="groq")
# → returns agent_id instantly

lazyown_agent_status("a1b2c3d4")   # poll progress
lazyown_agent_result("a1b2c3d4")   # full log + final answer
lazyown_list_agents()               # all past agents
```

### 15. Report generation — full pipeline

```python
# Step 1 — Get the complete campaign picture first
lazyown_campaign_sitrep()

# Step 2 — Verify all credentials captured
lazyown_credentials()

# Step 3 — Read campaign lessons for narrative
lazyown_campaign_lessons()

# Step 4 — Auto-generate Markdown report from session artefacts
lazyown_generate_report(target="10.10.11.78", include_timeline=True)

# Step 5 — Auto-fill executive summary in PDF report body
lazyown_report_update(action="auto_fill")

# Step 6 — Update specific report sections with findings
lazyown_report_update(
    action="write",
    key="executive_summary_findings",
    value="Critical: AD domain compromised via Kerberoasting. Domain Admin hash cracked. Full DA access achieved."
)
lazyown_report_update(
    action="write",
    key="appendix_a_changes",
    value="1) Created user 'backdoor_svc' on DC01 (removed after test)\n2) Modified ACL on AdminSDHolder (reverted)"
)

# Step 7 — Read what's currently in the report
lazyown_report_update(action="read")

# Step 8 — Export to MISP for threat intel sharing
lazyown_misp_export()
```

**PDF report data is at `static/body_report.json`** — fields rendered into the PDF template:
- `assessment_information` — company/team contact details
- `executive_summary_findings` — risk level, key compromises (auto-fill from session)
- `summary_vulnerability_overview` — vulnerability table with severity badges
- `appendix_a_changes` — environment changes made during test

### 16. Multi-target campaign

```
lazyown_add_target(ip="10.10.11.78", domain="darkzero.htb", tags=["AD", "windows"])
lazyown_add_target(ip="10.10.11.89", domain="solarlab.htb", tags=["web", "linux"])
lazyown_list_targets(status_filter="pending")
lazyown_set_active_target(ip="10.10.11.78", status="in_progress")
# ... attack ...
lazyown_set_active_target(ip="10.10.11.78", status="owned")
lazyown_set_active_target(ip="10.10.11.89", status="in_progress")
```

### 17. Operator shift handoff — zero-gap continuity

This workflow allows the **next operator (human or AI) to pick up exactly where the last left off** with zero manual briefing:

```python
# Outgoing operator — before ending shift:
# 1. Document what was found and what's next
lazyown_c2_notes(action="append", note="Kerberoasting complete — 3 hashes dumped. WinRM working on 10.10.11.78 as j.fleischman. Next: BloodHound to find DA path.")
# 2. Update task statuses
lazyown_campaign_tasks(action="update", task_id=2, status="Done")
lazyown_campaign_tasks(action="add", title="Run BloodHound for DA path", description="Use j.fleischman:J0elTHEM4n1990!", operator="claude_agent")
# 3. Pre-fill report executive summary
lazyown_report_update(action="auto_fill")
# 4. Inject next objectives for the autonomous daemon
lazyown_autonomous_inject(text="BloodHound collect on VariaType.htb to find DA path", priority="high")

# Incoming operator — start of shift:
lazyown_campaign_sitrep()          # full picture in one call
lazyown_c2_notes(action="read")   # read handoff notes
lazyown_campaign_lessons()         # learned patterns
lazyown_credentials()              # know what you have
lazyown_session_state()            # live phase + last commands
```

**The autonomous daemon continues working between shifts** — inject objectives and let it run.

### 17b. Hive Mind — massively parallel multi-agent analysis

```python
# 1. Let the Queen decompose a complex goal (dry-run first)
lazyown_hive_plan(goal="Fully compromise darkzero.htb Active Directory")
# → decomposition: [recon drone, exploit drone, cred drone, lateral drone]

# 2. Spawn 4 specialized drones in PARALLEL
lazyown_hive_spawn(
    goal="Enumerate all AD users and find Kerberoastable accounts on darkzero.htb",
    n_drones=4,
    roles=["recon", "exploit", "cred", "lateral"],
    backend="groq",
    wait=False       # non-blocking — returns drone IDs
)

# 3. Poll status
lazyown_hive_status()

# 4. Wait for synthesis (Queen aggregates drone results)
lazyown_hive_collect(goal="Enumerate AD users", timeout_s=120)

# 5. Semantic recall from unified ChromaDB + episodic SQLite + Parquet long-term
lazyown_hive_recall(query="kerberoast SPN hash", n=5)

# 6. Prune stale memory
lazyown_hive_forget(older_than_hours=48, topic="recon")
```

**Memory layers:**
- **Working memory**: current task context (shared via HiveBus)
- **Episodic memory**: SQLite FTS5 (`sessions/hive/episodic.db`) — events, commands, outcomes
- **Semantic memory**: ChromaDB vectors (`sessions/hive/chromadb/`) — similarity search
- **Long-term memory**: Parquet (`parquets/`) — GTFOBins, LOLBas, MITRE ATT&CK

### 17b. SWAN — Mixture of Experts with Reinforcement Learning

```python
# Route a task to the best expert (Q-learning decides which expert)
lazyown_swan_run(task_type="exploit", task="Suggest best exploit for SMB ms17-010", phase="exploit")

# Preview routing without executing
lazyown_swan_route(task_type="privesc", task="Linux privesc with sudo -l output")
# → expert_id=exploit_specialist, weight=0.72, rl_epsilon=0.12

# Ensemble: run ALL experts in parallel and synthesize
lazyown_swan_ensemble(task_type="cred", task="Enumerate credentials after BloodHound recon", phase="cred")

# See MoE health and learning state
lazyown_swan_status()
# → experts: [recon(0.68), exploit(0.72), privesc(0.65), cred(0.71), lateral(0.69)]
# → RL epsilon: 0.12 (exploitation-dominant)
```

**When to use SWAN vs Hive:**
- **SWAN**: single best expert for a specific tactical decision (fast, low overhead)
- **Hive**: N specialized agents for a complex multi-stage goal (slower, parallel, synthesized)

### 17c. Autonomous Daemon — fire-and-forget autonomous loop

```python
# Start the daemon (4 asyncio roles, runs independently of Claude)
lazyown_autonomous_start(max_steps_per_objective=15, backend="groq")

# Inject objectives — daemon picks them up in real-time
lazyown_autonomous_inject(text="Gain initial foothold via SMB on 10.10.11.78", priority="high")
lazyown_autonomous_inject(text="Escalate privileges once on host", priority="normal")

# Monitor execution in real-time
lazyown_autonomous_status()
# → phase=exploit, objective="Gain initial foothold", step=4/15, drones=2

# Read the event stream (STEP_START, STEP_DONE, HIGH_VALUE, PHASE_CHANGE, DRONE_SPAWNED)
lazyown_autonomous_events(last_n=20)

# Stop when done
lazyown_autonomous_stop()
```

**Autonomous daemon 6-selector cascade (in order):**
1. **ReactiveSelector** — parses last output for AV/EDR evasion, privesc hints, creds, new hosts. Priority ≤2 auto-injected.
2. **ParquetSelector** — queries `session_knowledge.parquet` for commands that succeeded in past sessions for this phase+target
3. **BridgeSelector** — queries the 347-command catalog (11 phases, MITRE-mapped) with OS + service hints
4. **SWANSelector** — routes to best MoE expert via Q-learning (enabled with `AUTO_USE_SWAN=1`)
5. **LLMSelector** — calls Groq/Ollama for intelligent suggestion (enabled with `AUTO_USE_LLM=1`)
6. **FallbackSelector** — OS-aware static maps (`_FALLBACK_MAP_LINUX` / `_FALLBACK_MAP_WINDOWS`)

**Env vars to enable full cascade:**
```bash
export AUTO_USE_SWAN=1      # activate SWAN expert routing
export AUTO_USE_LLM=1       # activate Groq/Ollama LLM selector
export AUTO_MAX_STEPS=20    # steps per objective (default 10)
export AUTO_STEP_TIMEOUT=90 # per-step timeout in seconds
export AUTO_HIVE_BACKEND=groq
```

### 17d. Atomic Red Team search

```python
# Search by keyword
lazyown_atomic_search(keyword="kerberoast")

# Search by MITRE technique
lazyown_atomic_search(mitre_id="T1558")

# Filter by platform and complexity
lazyown_atomic_search(keyword="credential", platform="windows", complexity="low")

# All tests for a MITRE tactic prefix
lazyown_atomic_search(mitre_id="T1547")   # all T1547.xxx subtechniques
```

Returns: technique id, name, MITRE ID, platform list, scope, complexity, prerequisites.
Source: `parquets/techniques_enriched.parquet` (1690 tests from Atomic Red Team project).

### 18. Integrate any GitHub tool on the fly

```
lazyown_list_addons()
lazyown_create_addon(
    name="subfinder",
    description="Fast passive subdomain enumeration",
    repo_url="https://github.com/projectdiscovery/subfinder.git",
    install_command="go install -v github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest",
    execute_command="subfinder -d {rhost}",
    params=[{"name": "rhost", "required": true, "description": "Target domain"}]
)
# 'subfinder' is now available in the LazyOwn shell
```

---

## Complete Data Sources Reference (26 sources)

LazyOwn aggregates **26 data sources** across 4 layers. When performing lateral thinking on a problem, consult multiple layers:

### Layer 1 — Parquet Knowledge Bases (7 sources)
Access via `lazyown_parquet_query` and `lazyown_atomic_search`

| # | Source | Parquet file | Query mode |
|---|--------|-------------|-----------|
| 1 | Session history | `session_knowledge.parquet` | `mode=session` — proven commands per phase/target |
| 2 | GTFOBins | `binarios.parquet` | `mode=keyword` — living-off-the-land Unix binaries |
| 3 | GTFOBins detail | `detalles.parquet` | `mode=keyword` — full command flags and context |
| 4 | LOLBAS index | `lolbas_index.parquet` | `mode=keyword` — Windows LOLBins index |
| 5 | LOLBAS detail | `lolbas_details.parquet` | `mode=keyword` — full Windows LOLBin commands |
| 6 | MITRE ATT&CK | `techniques.parquet` | `mode=context` — tactic/technique mapping |
| 7 | Atomic Red Team | `techniques_enriched.parquet` | `lazyown_atomic_search` — 1690 test cases |

### Layer 2 — Exploit Intelligence (9 sources)
Access via `lazyown_searchsploit` and `lazyown_cve_search`

| # | Source | Tool | Type |
|---|--------|------|------|
| 8 | ExploitDB / searchsploit | `lazyown_searchsploit` | Offline PoC database |
| 9 | NVD (NIST) | `lazyown_searchsploit`, `lazyown_cve_search` | CVE + CVSS scores |
| 10 | ExploitAlert | `lazyown_searchsploit` | Community exploits API |
| 11 | PacketStorm Security | `lazyown_searchsploit` | Exploit archive |
| 12 | Metasploit Framework | `lazyown_searchsploit` | Ready-to-use msf modules |
| 13 | Pompem | `lazyown_searchsploit` | Multi-DB exploit finder |
| 14 | Default Credentials | `lazyown_searchsploit` | DefaultCredsCheatSheet via creds_py |
| 15 | Sploitus | `lazyown_searchsploit` | Reference URL (community aggregator) |
| 16 | exploits.shodan.io | `lazyown_searchsploit` | Reference URL (Shodan exploit DB) |

### Layer 3 — Session Intelligence (8 sources)
Access via `lazyown_rag_query`, `lazyown_hive_recall`, `lazyown_facts_show`, `lazyown_campaign_sitrep`

| # | Source | Tool | Content |
|---|--------|------|---------|
| 17 | ChromaDB RAG | `lazyown_rag_query`, `lazyown_hive_recall` | Semantic search over all sessions/ artefacts |
| 18 | SQLite episodic memory | `lazyown_hive_recall`, `lazyown_memory_recall` | Per-session events, commands, outcomes (FTS5) |
| 19 | FactStore | `lazyown_facts_show` | Structured facts: ports, services, creds, shares, access level |
| 20 | sessionLazyOwn.json | `lazyown_campaign_sitrep`, `lazyown_c2_notes`, `lazyown_credentials` | Full operator session: params, creds, hashes, implants, notes, plan |
| 21 | tasks.json | `lazyown_campaign_tasks`, `lazyown_campaign_sitrep` | Task board: all objectives + status workflow |
| 22 | campaign_lessons.jsonl | `lazyown_campaign_lessons`, `lazyown_campaign_sitrep` | Derived tactical lessons from milestones |
| 23 | LazyOwn_session_report.csv | `lazyown_threat_model`, `lazyown_timeline`, `lazyown_campaign_sitrep` | Full command history with timestamps |
| 24 | body_report.json | `lazyown_report_update` | PDF report template fields (executive summary, findings, etc.) |

### Layer 4 — Adversarial Intelligence (2 sources)
Access via `lazyown_playbook_generate`, `lazyown_threat_model`

| # | Source | Tool | Content |
|---|--------|------|---------|
| 20 | STIX2 | `lazyown_playbook_generate` | MITRE ATT&CK STIX2 objects for playbook grounding |
| 21 | WorldModel | `lazyown_session_state`, `lazyown_autonomous_status` | Live host state machine + engagement phase |

### Lateral thinking query pattern — use ALL layers before deciding
```python
# START: complete campaign picture
lazyown_campaign_sitrep()                                                # L3 - all 10 state files
lazyown_credentials()                                                    # L3 - know what you have

# KNOWLEDGE: query all knowledge layers
lazyown_parquet_query(mode="context", phase="privesc", target=rhost)   # L1 - past + GTFOBins + MITRE
lazyown_searchsploit(query="<service> <version>")                       # L2 - all 9 exploit sources
lazyown_rag_query(query="<goal or technique>", n=5)                    # L3 - semantic session recall
lazyown_hive_recall(query="<credential type or technique>", n=5)       # L3 - episodic hive memory
lazyown_atomic_search(keyword="<technique>", platform="linux")         # L1 - 1690 Atomic Red Team tests
lazyown_bridge_suggest(phase="privesc", os_hint="linux", sequence=True) # catalog - next 5 commands
lazyown_campaign_lessons(topic="privesc")                               # L3 - learned patterns

# SYNTHESIZE with experts
lazyown_swan_ensemble(task_type="privesc", task="Best privesc path given: <context>", phase="privesc")
```

---

## Common LazyOwn Shell Commands

```
list                     — show all commands
set <key> <value>        — update a parameter (also writes payload.json)
payload                  — show current payload settings
lazynmap                 — full nmap recon against rhost
venom                    — generate msfvenom payload
msf                      — launch Metasploit listener
nc                       — start netcat listener
ligolo                   — set up Ligolo tunnel
chisel                   — set up chisel tunnel
adversary_yaml <name>    — run a lazyadversaries/*.yaml (amsi, linpeas, sudo_nopasswd...)
adversary <id>           — emulate MITRE ATT&CK technique
cron HH:MM <command>     — schedule a command at a specific time
report                   — generate HTML/PDF report via AI
tools list               — list custom pwntomate .tool files
```

---

## IMPORTANT — Long-running scripts (NO TIMEOUT)

### `lazynmap` / `modules/lazynmap.sh`
- Full TCP scan (`-p- --open -sS --min-rate 5000`) + per-port `-sV` + NSE scripts.
- Takes **5–30 minutes** on real targets.
- **NEVER kill early.** Do NOT set a timeout on `lazyown_run_command("lazynmap")`.
- If MCP times out, the scan continues in the background — check `sessions/scan_<rhost>.nmap`.

### `pwntomate.py`
- Reads nmap XML and launches every matching tool in parallel.
- HTTP targets: ffuf/gobuster/nikto can each run **20–60 minutes per port**.
- **NEVER set a timeout** on pwntomate. Run detached and poll `sessions/<ip>/` for output.

### Recommended pattern

```python
# 1. Recon (inform user this is long-running)
lazyown_run_command("lazynmap")

# 2. Once scan XML exists, pwntomate runs automatically via auto_loop
#    or manually: python3 pwntomate.py sessions/scan_<rhost>.nmap.xml -x -b sessions/ -t tools/

# 3. Incremental results via FactStore
lazyown_facts_show(target="<rhost>", refresh=True)
```

---

## Reactive Engine — Priority Table

| Priority | Action | Trigger |
|----------|--------|---------|
| 1 | `escalate_evasion` | AMSI / Defender / CrowdStrike detected |
| 1 | `run_command` | sudo NOPASSWD / SUID / polkit / token impersonation |
| 2 | `record_cred` | Password or NTLM hash in output |
| 3 | `add_host` | New RFC1918 IP discovered |
| 3–4 | `switch_tool` | Connection refused / auth failed / command not found |

Priority ≤ 2 decisions are auto-injected as the next `auto_loop` step.

---

## Auto-discovered tools

Discovered at server startup from `lazyaddons/`, `tools/`, and `plugins/`. Run `mcp restart` to refresh.

### Addons (`lazyown_addon_*`)

| Tool | Description |
|------|-------------|
| `lazyown_addon_adaptixc2` | Extensible post-exploitation and adversarial emulation framework |
| `lazyown_addon_agentzero` | Personal agentic framework that grows and learns with you |
| `lazyown_addon_argfuscator` | Generate obfuscated versions of common commands to bypass detection |
| `lazyown_addon_attpwn` | Adversary emulation tool aimed at MITRE ATT&CK techniques |
| `lazyown_addon_aurorapatch` | Lightweight Go tool that bypasses Windows AMSI |
| `lazyown_addon_banner_tool` | Execute banner.py from modules/ |
| `lazyown_addon_bbr` | Command-line bug bounty report generator |
| `lazyown_addon_beacon` | Next-gen framework for generating, obfuscating, and deploying beacons |
| `lazyown_addon_cgoblin_windows` | Shellcode loader for Windows (from URL) |
| `lazyown_addon_clematis` | Convert PE files (EXE/DLL) into position-independent shellcode |
| `lazyown_addon_commix2` | Detect and exploit command injection vulnerabilities |
| `lazyown_addon_cve-2022-22077` | PoC for CVE-2022-22077 (Qualcomm privilege escalation) |
| `lazyown_addon_cve_2025_24071_poc` | CVE-2025-24071: NTLM hash leak via RAR/ZIP + .library-ms |
| `lazyown_addon_demiguise` | HTA encryption tool for Red Teams |
| `lazyown_addon_ebird3` | Framework for generating and obfuscating beacons (ebird3) |
| `lazyown_addon_evilginx2` | Man-in-the-middle framework for phishing credential capture |
| `lazyown_addon_gcr` | Google Calendar RAT — C2 over Google Calendar events |
| `lazyown_addon_gemini-cli` | Gemini AI agent in your terminal |
| `lazyown_addon_gen_dll_rev` | Generate obfuscated DLL reverse shells |
| `lazyown_addon_get_reverseshell` | PowerShell reverse shell via Invoke-PSObfuscation |
| `lazyown_addon_githubot` | Create and manage GitHub repos via bot.py |
| `lazyown_addon_gomulti_loader_linux` | Multi-loader shellcode for Linux |
| `lazyown_addon_gomulti_loader_windows` | Multi-loader shellcode for Windows |
| `lazyown_addon_gopeinjection` | Golang PE injection on Windows |
| `lazyown_addon_gosearch` | Search anyone's digital footprint across 300+ websites |
| `lazyown_addon_gui` | Start the LazyOwn C2 GUI |
| `lazyown_addon_hack_browser_data` | Extract and decrypt browser data (cookies, history, passwords) |
| `lazyown_addon_hellbird` | Framework for generating obfuscated payloads (hellbird) |
| `lazyown_addon_hooka_linux_amd64` | Shellcode loader generator with multiple features (Linux AMD64) |
| `lazyown_addon_hostdiscover` | Execute hostdiscover.sh from modules/ |
| `lazyown_addon_kivi_revshell` | Kivy-based reverse shell via kivi.py |
| `lazyown_addon_laps` | Dump LAPS passwords from Active Directory |
| `lazyown_addon_lazyagentai` | Execute lazyagentAi.py from modules/ |
| `lazyown_addon_lazybinenc` | Execute lazybinenc.py — binary encoder from modules/ |
| `lazyown_addon_lazyftpsniff` | Execute lazyftpsniff.py — FTP credential sniffer |
| `lazyown_addon_lazyloader` | Stealthy Windows PE loader: fetch, decrypt, execute in memory |
| `lazyown_addon_lazymapd` | Detect open ports and save results (LazyOwn RedTeam) |
| `lazyown_addon_lazyownbt` | LazyOwn BlueTeam: detect and react to attacks, hardening |
| `lazyown_addon_lazyownexplorer` | Execute LazyOwnExplorer.py from modules/ |
| `lazyown_addon_nullgate` | Indirect syscalls library for AV/EDR bypass |
| `lazyown_addon_oniux` | Isolate any app into its own Tor network namespace |
| `lazyown_addon_orpheus` | Bypass Kerberoast detections via modified KDC options |
| `lazyown_addon_override` | Process overwrite PoC for code execution |
| `lazyown_addon_peeko` | Browser-based XSS C2 — compromised browsers as internal network proxies |
| `lazyown_addon_pretender` | MitM sidekick: DHCPv6 DNS takeover + NTLM relay |
| `lazyown_addon_ptmultitools` | Public CTF/red team multi-tool collection |
| `lazyown_addon_ptmultitools_scan` | Multi-tool collection — scanning mode |
| `lazyown_addon_pyinmemorype` | Execute PE (DLL/EXE) in memory filelessly |
| `lazyown_addon_pyrit` | Microsoft PyRIT — AI red teaming risk identification |
| `lazyown_addon_raven` | Invoke-PSObfuscation-based payload generator |
| `lazyown_addon_ridenum` | RID cycling for user enumeration bypassing Kerberoast detections |
| `lazyown_addon_setoolkit` | Social-Engineer Toolkit (TrustedSec SET) |
| `lazyown_addon_shadowlink` | Next-gen obfuscated payload framework (shadowlink) |
| `lazyown_addon_shellcode_custom_win_rev_tcp_xored` | Custom XOR-encoded Windows TCP reverse shellcode (no msfvenom) |
| `lazyown_addon_sigploit` | Signaling security testing framework for Telecom (SS7/Diameter/GTP) |
| `lazyown_addon_spoonmap` | Wrapper for nmap + masscan with unified output |
| `lazyown_addon_stratus_detonate` | Cloud adversary emulation — detonate ATT&CK techniques in AWS/Azure/GCP |
| `lazyown_addon_stratus_list` | Cloud adversary emulation — list available techniques |
| `lazyown_addon_unicorn` | PowerShell downgrade attack + shellcode injection via unicorn |
| `lazyown_addon_upxdump` | Repair corrupt UPX-packed malware p_info headers |
| `lazyown_addon_vulnbot` | Execute vuln_bot_cli.py from modules/ |
| `lazyown_addon_vulnbot_groq` | Execute vuln_bot_cli.py with Groq backend |
| `lazyown_addon_vulnhuntr` | LLM-powered automatic vulnerability discovery in source code |
| `lazyown_addon_watchguard` | WatchGuard SSO Agent Protocol client for security research |
| `lazyown_addon_wspcoerce` | Coerce Windows computer account via SMB to arbitrary target |

### Plugins (`lazyown_plugin_*`)

| Tool | Description |
|------|-------------|
| `lazyown_plugin_generate_c_reverse_shell` | Generate a reverse shell payload in C with dynamic shellcode |
| `lazyown_plugin_generate_cleanup_commands` | Generate cleanup commands for Windows or Linux post-exploitation |
| `lazyown_plugin_generate_html_payload` | Generate an HTML file that delivers a hidden encoded payload |
| `lazyown_plugin_generate_lateral_command` | Generate lateral movement commands (psexec, smbexec, wmiexec...) |
| `lazyown_plugin_generate_linux_asm_reverse_shell` | Generate NASM assembly for a Linux syscall-based reverse shell |
| `lazyown_plugin_generate_linux_raw_shellcode` | Generate raw shellcode for a Linux TCP reverse shell |
| `lazyown_plugin_generate_lolbird` | Generate XOR-encoded shellcode + 3-phase LOLbird one-liner |
| `lazyown_plugin_generate_msfvenom_loader` | Generate hex shellcode for msfvenom reverse shell on Linux |
| `lazyown_plugin_generate_msfvenom_loader_win` | Generate hex shellcode for msfvenom reverse shell on Windows |
| `lazyown_plugin_generate_reverse_shell` | Generate a Python reverse shell payload connecting back to LHOST |
| `lazyown_plugin_generate_stub` | Generate XOR-encoded shellcode + 2-phase stub one-liner |
| `lazyown_plugin_kerberos_harvest` | Harvest Kerberos tickets by querying SPNs |
| `lazyown_plugin_lolbas_bitsadmin_exe` | Use bitsadmin to download and execute an EXE (LOLBas) |
| `lazyown_plugin_lolbas_certutil_download_exec` | Use certutil to download an XOR-obfuscated DLL and execute via regsvr32 |
| `lazyown_plugin_lolbas_certutil_exe` | Download and execute EXE with certutil |
| `lazyown_plugin_lolbas_mshta_js_lua` | Download and execute JavaScript via mshta |
| `lazyown_plugin_lolbas_mshta_reverse_shell` | Generate mshta one-liner executing a JavaScript reverse shell |
| `lazyown_plugin_lolbas_rundll32_dll` | Generate rundll32 one-liner for DLL sideloading |
| `lazyown_plugin_lolbas_wmic_xsl_execution` | Execute commands via wmic + remote XSL file (T1220) |
| `lazyown_plugin_parse_nmap_with_xmlstarlet` | Extract IPs, ports, services from nmap XML using xmlstarlet |
| `lazyown_plugin_run_nuclei_on_nmap_files` | Run nuclei against IPs extracted from nmap XML files |
| `lazyown_plugin_run_python_rev_c2` | Execute a Python reverse shell payload connecting to LHOST |
| `lazyown_plugin_rundll32_sct_from_url` | Craft a rundll32.exe one-liner to execute a remote SCT payload |
| `lazyown_plugin_validate_shellcode` | Validate shellcode for bad bytes and payload integrity |
| `lazyown_plugin_visualize_network` | Generate a node graph visualization from a list of IPs |

### Tools (`lazyown_tool_*`)

Auto-applied by pwntomate when nmap detects matching services. Also callable directly as MCP tools.

| Tool | Triggers on | Description |
|------|-------------|-------------|
| `lazyown_tool_asrep_roast` | ldap, kerberos-sec | AS-REP roasting — extract hashes for accounts without pre-auth |
| `lazyown_tool_bloodhound-python` | ldap, kerberos-sec | BloodHound data collection via Python |
| `lazyown_tool_crackmapexec_ldap` | ldap, ldaps | CME LDAP enumeration |
| `lazyown_tool_crackmapexec_smb` | microsoft-ds, netbios-ssn | CME SMB enumeration and attacks |
| `lazyown_tool_dig_any` | domain | DNS ANY record lookup |
| `lazyown_tool_dig_reverse` | domain | Reverse DNS lookup |
| `lazyown_tool_dns_enum_tool` | domain | DNS enumeration (zone transfer, brute) |
| `lazyown_tool_dnsrecon_axfr` | domain | DNSrecon zone transfer attempt |
| `lazyown_tool_enum4linux_tool` | microsoft-ds, netbios | Full enum4linux enumeration |
| `lazyown_tool_enum_rpcbind` | rpcbind | RPC endpoint enumeration |
| `lazyown_tool_enum_smb` | microsoft-ds | SMB share and session enumeration |
| `lazyown_tool_evil_winrm_tool` | winrm | evil-winrm connection |
| `lazyown_tool_ffuf_enumeration` | http, https | ffuf directory/file enumeration |
| `lazyown_tool_ffuf_tool` | http, https, http-mgmt | ffuf fuzzing (extended service list) |
| `lazyown_tool_getnpusers_tool` | kerberos-sec | GetNPUsers — AS-REP roasting |
| `lazyown_tool_getuserspns_py` | kerberos-sec | GetUserSPNs.py — Kerberoasting |
| `lazyown_tool_gobuster_dns` | http, https | Gobuster DNS subdomain enumeration |
| `lazyown_tool_gobuster_http` | http, http-proxy | Gobuster web directory brute-force |
| `lazyown_tool_gobuster_web` | http, https | Gobuster web enumeration |
| `lazyown_tool_hydrardp_tool` | rdp | Hydra RDP brute-force |
| `lazyown_tool_hydrasmb` | smb | Hydra SMB brute-force |
| `lazyown_tool_kerberoasting_tool` | kerberos-sec | Kerberoasting — request TGS tickets |
| `lazyown_tool_kerbrute_tool` | kerberos-sec | Kerbrute user enumeration and brute-force |
| `lazyown_tool_kerbrute_tool_user` | kerberos-sec | Kerbrute username enumeration only |
| `lazyown_tool_ldap_domain_dump_tool` | ldap | ldapdomaindump — full AD dump |
| `lazyown_tool_ldapsearch_anon` | ldap | LDAP anonymous bind enumeration |
| `lazyown_tool_ldapsearch_tool` | ldap | Authenticated LDAP search |
| `lazyown_tool_nc_ldap_interact` | ldap | Netcat LDAP interaction |
| `lazyown_tool_nikto_host` | http, https | Nikto web server scanner |
| `lazyown_tool_nuclei_ad_http` | http, https, http-rpc | Nuclei templates for AD HTTP endpoints |
| `lazyown_tool_nxc_idap_tool` | ldap, ldaps | NetExec LDAP enumeration |
| `lazyown_tool_nxc_ldap` | ldap | NetExec LDAP (alternate template) |
| `lazyown_tool_nxc_null_session` | microsoft-ds | NetExec null session test |
| `lazyown_tool_nxc_pass_policy` | microsoft-ds | NetExec password policy enumeration |
| `lazyown_tool_nxc_rid` | microsoft-ds | NetExec RID cycling |
| `lazyown_tool_nxc_winrm` | winrm | NetExec WinRM authentication test |
| `lazyown_tool_ollama_enum` | http, https | Enumerate Ollama API endpoints |
| `lazyown_tool_rpcclient_tool` | msrpc | rpcclient enumeration (users, groups, shares) |
| `lazyown_tool_showmount_nfs` | nfs | showmount NFS export listing |
| `lazyown_tool_showmount_tool` | nfs_acl, nfs | showmount (extended) |
| `lazyown_tool_smb_ghost` | microsoft-ds | SMBGhost (CVE-2020-0796) check |
| `lazyown_tool_smb_map` | microsoft-ds | SMBMap share enumeration |
| `lazyown_tool_smbclient_list` | microsoft-ds | smbclient share listing |
| `lazyown_tool_smbclient_tool` | microsoft-ds, netbios | smbclient interactive |
| `lazyown_tool_smbmap_tool` | microsoft-ds | smbmap with credentials |
| `lazyown_tool_smbserver_tool` | microsoft-ds | Impacket smbserver (for file transfer/relay) |
| `lazyown_tool_subwfuzz_tool` | http, https, http-mgmt | Subdomain fuzzing with wfuzz |
| `lazyown_tool_swaks_smtp_test` | smtp | SMTP test via swaks |
| `lazyown_tool_userenum_tool` | microsoft-ds | SMB user enumeration |
| `lazyown_tool_vncviewer_connect` | vnc | VNC viewer connection |

---

## AI Sub-Agent Backends

| Backend | Model | Requirement | Best for |
|---------|-------|-------------|----------|
| `groq` | llama-3.3-70b-versatile | `api_key` in payload.json | Complex reasoning, multi-step recon |
| `ollama` | auto-detected | Local chat model | Offline/private tasks |

Ollama requires an instruction-tuned chat model (NOT reasoning-only):
```bash
ollama pull llama3.2:3b   # fast, recommended
ollama pull mistral        # excellent for pentesting
```

---

## Notes

- The LazyOwn shell is cmd2-based; commands are fed via stdin.
- The C2 REST API runs on `https://<lhost>:<c2_port>` (self-signed TLS).
- Configuration lives in `payload.json` — always call `lazyown_get_config` first.
- Session data (logs, exfil, screenshots) is stored under `sessions/`.
- `lazyown_addon_*`, `lazyown_plugin_*`, `lazyown_tool_*` are auto-discovered at startup. Run `mcp restart` to pick up new ones.
- **Never kill or timeout `lazynmap` or `pwntomate`** — they are intentionally long-running.
- Autonomous daemon env vars: `AUTO_USE_SWAN=1`, `AUTO_USE_LLM=1`, `AUTO_MAX_STEPS=N`, `AUTO_STEP_TIMEOUT=N`, `AUTO_HIVE_BACKEND=groq|ollama`
- Hive Mind requires ChromaDB for semantic search: `pip install chromadb`
- SWAN+LLM selectors disabled by default in auto_loop — set env vars to enable full 6-selector cascade
- 26 total data sources: 7 Parquets + 9 exploit sources + 8 session intelligence + 2 adversarial intelligence
- PDF report body at `static/body_report.json` — use `lazyown_report_update` to read/write fields
- Operator shift handoff: `lazyown_c2_notes(action="append")` then `lazyown_campaign_sitrep()` for incoming operator
- Session state files: sessionLazyOwn.json (creds+implants), tasks.json, campaign_lessons.jsonl, campaign.json








## Auto-discovered tools

Discovered at server startup. Run `mcp restart` to refresh.

| MCP Tool Name | Source | Description |
|---|---|---|
| `lazyown_addon_adaptixc2` | addon | Adaptix is an extensible post-exploitation and adversarial emulation framework m |
| `lazyown_addon_agentzero` | addon | A personal, organic agentic framework that grows and learns with you Agent Zero  |
| `lazyown_addon_argfuscator` | addon | ArgFuscator is an open-source, stand-alone web application that helps generate o |
| `lazyown_addon_attpwn` | addon | ATTPwn is a computer security tool designed to emulate adversaries. The tool aim |
| `lazyown_addon_aurorapatch` | addon | AuroraPatch is a lightweight, offensive Go tool that bypasses Windows AMSI (Anti |
| `lazyown_addon_banner_tool` | addon | Ejecuta el script banner.py que se encuentra en la carpeta modules. |
| `lazyown_addon_bbr` | addon | An open source tool to aid in command line driven generation of bug bounty repor |
| `lazyown_addon_beacon` | addon | beacon is a next-generation, automated framework for generating, obfuscating, an |
| `lazyown_addon_cgoblin_windows` | addon | cgoblin shellcode in windows and windows from an url |
| `lazyown_addon_clematis` | addon | 🛠️ A powerful tool for converting PE files (EXE/DLL) into position-independent s |
| `lazyown_addon_commix2` | addon | Detecta y explota vulnerabilidades de inyección de comandos. |
| `lazyown_addon_cve-2022-22077` | addon | CVE-2022-22077 is a high-severity vulnerability (CVSS score 7.8) affecting the R |
| `lazyown_addon_cve_2025_24071_poc` | addon | CVE-2025-24071: NTLM Hash Leak via RAR/ZIP Extraction and .library-ms File. Wind |
| `lazyown_addon_demiguise` | addon | HTA encryption tool for RedTeams |
| `lazyown_addon_ebird3` | addon | ebird3 is a next-generation, automated framework for generating, obfuscating, an |
| `lazyown_addon_evilginx2` | addon | Standalone man-in-the-middle attack framework used for phishing login credential |
| `lazyown_addon_gcr` | addon | Google Calendar RAT is a PoC of Command&Control over Google Calendar Events |
| `lazyown_addon_gemini-cli` | addon | An open-source AI agent that brings the power of Gemini directly into your termi |
| `lazyown_addon_gen_dll_rev` | addon | gen_dll_rev is a next-generation, automated framework for generating, obfuscatin |
| `lazyown_addon_get_reverseshell` | addon | Get-ReverseShell is a project that stems from the Invoke-PSObfuscation framework |
| `lazyown_addon_githubot` | addon | Ejecuta el script bot.py que se encuentra en la carpeta modules. creando un repo |
| `lazyown_addon_gomulti_loader_linux` | addon | gomulti_loader shellcode in windows and linux |
| `lazyown_addon_gomulti_loader_windows` | addon | gomulti_loader shellcode in windows and windows |
| `lazyown_addon_gopeinjection` | addon | Golang PE injection on windows |
| `lazyown_addon_gosearch` | addon | gosearch is a Search anyone's digital footprint across 300+ websites |
| `lazyown_addon_gui` | addon | Start the GUI of our C2 |
| `lazyown_addon_hack_browser_data` | addon | Extract and decrypt browser data, supporting multiple data types, runnable on va |
| `lazyown_addon_hellbird` | addon | hellbird is a next-generation, automated framework for generating, obfuscating,  |
| `lazyown_addon_hooka_linux_amd64` | addon | Shellcode loader generator with multiples features |
| `lazyown_addon_hostdiscover` | addon | Ejecuta el script hostdiscover.sh que se encuentra en la carpeta modules. |
| `lazyown_addon_kivi_revshell` | addon | Ejecuta el script kivi.py que se encuentra en la carpeta modules. para Reverse s |
| `lazyown_addon_laps` | addon | Dumping LAPS from Python |
| `lazyown_addon_lazyagentai` | addon | Ejecuta el script lazyagentAi.py que se encuentra en la carpeta modules. |
| `lazyown_addon_lazybinenc` | addon | Ejecuta el script lazybinenc.py que se encuentra en la carpeta modules. |
| `lazyown_addon_lazyftpsniff` | addon | Ejecuta el script lazyftpsniff.py que se encuentra en la carpeta modules. |
| `lazyown_addon_lazyloader` | addon | LazyLoader is A stealthy LazyLoader Windows PE loader designed to fetch, decrypt |
| `lazyown_addon_lazymapd` | addon | LAzyOwn RedTeam Framework, Detecta puertos abiertos y es capaz de guardar en un  |
| `lazyown_addon_lazyownbt` | addon | LAzyOwn BlueTeam Framework, Detecta y reacciona a ataques, haredenización, integ |
| `lazyown_addon_lazyownexplorer` | addon | Ejecuta el script LazyOwnExplorer.py que se encuentra en la carpeta modules. |
| `lazyown_addon_nullgate` | addon | Library that eases the use of indirect syscalls. Quite interesting AV/EDR bypass |
| `lazyown_addon_oniux` | addon | oniux is a tool that utilizes various Linux namespaces(7) in order to isolate an |
| `lazyown_addon_orpheus` | addon | Bypassing Kerberoast Detections with Modified KDC Options and Encryption Types |
| `lazyown_addon_override` | addon | This project provides a proof-of-concept implementation of the "Process Overwrit |
| `lazyown_addon_peeko` | addon | Browser-based XSS C2 tool that turns compromised browsers into internal network  |
| `lazyown_addon_pretender` | addon | Your MitM sidekick for relaying attacks featuring DHCPv6 DNS takeover as well as |
| `lazyown_addon_ptmultitools` | addon | This repository my public tools that I use in CTF's and real world engagements. |
| `lazyown_addon_ptmultitools_scan` | addon | This repository my public tools that I use in CTF's and real world engagements. |
| `lazyown_addon_pyinmemorype` | addon | 🛠️ Execute any PE (dll,exe) in memory filelessly usage pymemory.py < url> < TYPe |
| `lazyown_addon_pyrit` | addon | Python Risk Identification Tool for generative AI (PyRIT) by Microsoft/Azure. Em |
| `lazyown_addon_raven` | addon | raven is a project that stems from the Invoke-PSObfuscation framework, with the  |
| `lazyown_addon_ridenum` | addon | Bypassing Kerberoast Detections with Modified KDC Options and Encryption Types |
| `lazyown_addon_setoolkit` | addon | The Social-Engineer Toolkit (SET) repository from TrustedSec - All new versions  |
| `lazyown_addon_shadowlink` | addon | ShadowLink is a next-generation, automated framework for generating, obfuscating |
| `lazyown_addon_shellcode_custom_win_rev_tcp_xored` | addon | win_shellcode shellcode in windows custom (no msfvenom) and xored |
| `lazyown_addon_sigploit` | addon | SigPloit a signaling security testing framework dedicated to Telecom Security pr |
| `lazyown_addon_spoonmap` | addon | This script is simply a wrapper for NMAP and Masscan. Install them from your fav |
| `lazyown_addon_stratus_detonate` | addon | ☁️ ⚡ Granular, Actionable Adversary Emulation for the Cloud. Need an attack like |
| `lazyown_addon_stratus_list` | addon | ☁️ ⚡ Granular, Actionable Adversary Emulation for the Cloud |
| `lazyown_addon_unicorn` | addon | Unicorn is a simple tool for using a PowerShell downgrade attack and inject shel |
| `lazyown_addon_upxdump` | addon | Some C code to repair corrupt p_info header on UPX! packed malware. It fixes two |
| `lazyown_addon_vulnbot` | addon | Ejecuta el script vuln_bot_cli.py que se encuentra en la carpeta modules. |
| `lazyown_addon_vulnbot_groq` | addon | Ejecuta el script vuln_bot_cli.py que se encuentra en la carpeta modules. |
| `lazyown_addon_vulnhuntr` | addon | Vulnhuntr leverages the power of LLMs to automatically create and analyze entire |
| `lazyown_addon_watchguard` | addon | Client Implementation for the WatchGuard SSO Agent Protocol used for Security Re |
| `lazyown_addon_wspcoerce` | addon | wspcoerce coerces a Windows computer account via SMB to an arbitrary target usin |
| `lazyown_plugin_generate_c_reverse_shell` | plugin | Generates a reverse shell payload written in C, embedding dynamically crafted sh |
| `lazyown_plugin_generate_cleanup_commands` | plugin | Generates cleanup commands for Windows or Linux systems based on user-specified  |
| `lazyown_plugin_generate_html_payload` | plugin | Generates an HTML file that delivers a hidden payload file using various encodin |
| `lazyown_plugin_generate_lateral_command` | plugin | Genera comandos de movimiento lateral usando diferentes técnicas (psexec, smbexe |
| `lazyown_plugin_generate_linux_asm_reverse_shell` | plugin | Genera código ensamblador NASM para una reverse shell en Linux basada en syscall |
| `lazyown_plugin_generate_linux_raw_shellcode` | plugin | Genera shellcode en formato raw para una reverse shell TCP en Linux. No crea arc |
| `lazyown_plugin_generate_lolbird` | plugin | generate shellcode xored using the key 0x33 and craft a oneliner with 3 phases a |
| `lazyown_plugin_generate_msfvenom_loader` | plugin | Genera shellcode en formato hex para una msfvenom reverse shell TCP en Linux. Cr |
| `lazyown_plugin_generate_msfvenom_loader_win` | plugin | Genera shellcode en formato hex para una msfvenom reverse shell TCP en Windows.  |
| `lazyown_plugin_generate_reverse_shell` | plugin | Generates a Python reverse shell payload that connects back to a specified LHOST |
| `lazyown_plugin_generate_stub` | plugin | generate stub xored using the key 0x33 and craft a oneliner with 2 phases attack |
| `lazyown_plugin_kerberos_harvest` | plugin | Harvests Kerberos tickets by querying for Service Principal Names (SPNs) and req |
| `lazyown_plugin_lolbas_bitsadmin_exe` | plugin | Usa bitsadmin para descargar y ejecutar EXE |
| `lazyown_plugin_lolbas_certutil_download_exec` | plugin | Usa certutil para descargar una DLL ofuscada con XOR, la decodifica y ejecuta co |
| `lazyown_plugin_lolbas_certutil_exe` | plugin | Descarga y ejecuta EXE con certutil |
| `lazyown_plugin_lolbas_mshta_js_lua` | plugin | Descarga y ejecuta js con mshta |
| `lazyown_plugin_lolbas_mshta_reverse_shell` | plugin | Genera un one-liner con mshta que ejecuta una reverse shell en JavaScript. No re |
| `lazyown_plugin_lolbas_rundll32_dll` | plugin | Genera un one-liner con mshta que ejecuta una reverse shell en JavaScript. No re |
| `lazyown_plugin_lolbas_wmic_xsl_execution` | plugin | Usa wmic + archivo XSL remoto para ejecutar comandos. Técnica T1220. Requiere se |
| `lazyown_plugin_parse_nmap_with_xmlstarlet` | plugin | Usa xmlstarlet para extraer información útil de archivos NMAP (.xml):
 - IPs act |
| `lazyown_plugin_run_nuclei_on_nmap_files` | plugin | Ejecuta nuclei utilizando direcciones IP extraídas de archivos NMAP .xml
almacen |
| `lazyown_plugin_run_python_rev_c2` | plugin | Executes a Python reverse shell payload that connects back to a specified LHOST  |
| `lazyown_plugin_rundll32_sct_from_url` | plugin | Craft a one-liner using rundll32.exe to execute a remote SCT payload via JavaScr |
| `lazyown_plugin_validate_shellcode` | plugin | Validates shellcode data by checking for bad bytes and ensuring the payload does |
| `lazyown_plugin_visualize_network` | plugin | Reads a list of IP addresses from a file, generates a simple node graph visualiz |
| `lazyown_tool_asrep_roast` | tool | Run asrep_roast against a target. Triggers on services: ldap, kerberos-sec. Comm |
| `lazyown_tool_bloodhound-python` | tool | Run bloodhound-python against a target. Triggers on services: ldap, kerberos-sec |
| `lazyown_tool_crackmapexec_ldap` | tool | Run crackmapexec_ldap against a target. Triggers on services: ldap, ldaps. Comma |
| `lazyown_tool_crackmapexec_smb` | tool | Run crackmapexec_smb against a target. Triggers on services: microsoft-ds, netbi |
| `lazyown_tool_dig_any` | tool | Run dig_any against a target. Triggers on services: domain. Command template: di |
| `lazyown_tool_dig_reverse` | tool | Run dig_reverse against a target. Triggers on services: domain. Command template |
| `lazyown_tool_dns_enum_tool` | tool | Run dns_enum_tool against a target. Triggers on services: domain. Command templa |
| `lazyown_tool_dnsrecon_axfr` | tool | Run dnsrecon_axfr against a target. Triggers on services: domain. Command templa |
| `lazyown_tool_enum4linux_tool` | tool | Run enum4linux_tool against a target. Triggers on services: microsoft-ds, netbio |
| `lazyown_tool_enum_rpcbind` | tool | Run enum_rpcbind against a target. Triggers on services: rpcbind. Command templa |
| `lazyown_tool_enum_smb` | tool | Run enum_smb against a target. Triggers on services: microsoft-ds. Command templ |
| `lazyown_tool_evil_winrm_tool` | tool | Run evil_winrm_tool against a target. Triggers on services: winrm. Command templ |
| `lazyown_tool_ffuf_enumeration` | tool | Run ffuf_enumeration against a target. Triggers on services: http, https. Comman |
| `lazyown_tool_ffuf_tool` | tool | Run ffuf_tool against a target. Triggers on services: http, https, http-mgmt, ht |
| `lazyown_tool_getnpusers_tool` | tool | Run getNPUsers_tool against a target. Triggers on services: kerberos-sec. Comman |
| `lazyown_tool_getuserspns_py` | tool | Run GetUserSPNs.py against a target. Triggers on services: kerberos-sec. Command |
| `lazyown_tool_gobuster_dns` | tool | Run gobuster_dns against a target. Triggers on services: http, https. Command te |
| `lazyown_tool_gobuster_http` | tool | Run gobuster_http against a target. Triggers on services: http, http-proxy, http |
| `lazyown_tool_gobuster_web` | tool | Run gobuster_web against a target. Triggers on services: http, https. Command te |
| `lazyown_tool_hydrardp_tool` | tool | Run hydrardp_tool against a target. Triggers on services: rdp. Command template: |
| `lazyown_tool_hydrasmb` | tool | Run hydrasmb against a target. Triggers on services: smb. Command template: hydr |
| `lazyown_tool_kerberoasting_tool` | tool | Run kerberoasting_tool against a target. Triggers on services: kerberos-sec. Com |
| `lazyown_tool_kerbrute_tool` | tool | Run kerbrute_tool against a target. Triggers on services: kerberos-sec. Command  |
| `lazyown_tool_kerbrute_tool_user` | tool | Run kerbrute_tool_user against a target. Triggers on services: kerberos-sec. Com |
| `lazyown_tool_ldap_domain_dump_tool` | tool | Run ldap_domain_dump_tool against a target. Triggers on services: ldap. Command  |
| `lazyown_tool_ldapsearch_anon` | tool | Run ldapsearch_anon against a target. Triggers on services: ldap. Command templa |
| `lazyown_tool_ldapsearch_tool` | tool | Run ldapsearch_tool against a target. Triggers on services: ldap. Command templa |
| `lazyown_tool_nc_ldap_interact` | tool | Run nc_ldap_interact against a target. Triggers on services: ldap. Command templ |
| `lazyown_tool_nikto_host` | tool | Run nikto_host against a target. Triggers on services: http, https. Command temp |
| `lazyown_tool_nuclei_ad_http` | tool | Run nuclei_ad_http against a target. Triggers on services: http, https, http-rpc |
| `lazyown_tool_nxc_idap_tool` | tool | Run nxc_idap_tool against a target. Triggers on services: ldap, ldaps. Command t |
| `lazyown_tool_nxc_ldap` | tool | Run nxc_ldap against a target. Triggers on services: ldap. Command template: nxc |
| `lazyown_tool_nxc_null_session` | tool | Run nxc_null_session against a target. Triggers on services: microsoft-ds. Comma |
| `lazyown_tool_nxc_pass_policy` | tool | Run nxc_pass_policy against a target. Triggers on services: microsoft-ds. Comman |
| `lazyown_tool_nxc_rid` | tool | Run nxc_rid against a target. Triggers on services: microsoft-ds. Command templa |
| `lazyown_tool_nxc_winrm` | tool | Run nxc_winrm against a target. Triggers on services: winrm. Command template: n |
| `lazyown_tool_ollama_enum` | tool | Run ollama_enum against a target. Triggers on services: http, https. Command tem |
| `lazyown_tool_rpcclient_tool` | tool | Run rpcclient_tool against a target. Triggers on services: msrpc. Command templa |
| `lazyown_tool_showmount_nfs` | tool | Run showmount_nfs against a target. Triggers on services: nfs. Command template: |
| `lazyown_tool_showmount_tool` | tool | Run showmount_tool against a target. Triggers on services: nfs_acl, nfs. Command |
| `lazyown_tool_smb_ghost` | tool | Run smb_ghost against a target. Triggers on services: microsoft-ds. Command temp |
| `lazyown_tool_smb_map` | tool | Run smb_map against a target. Triggers on services: microsoft-ds. Command templa |
| `lazyown_tool_smbclient_list` | tool | Run smbclient_list against a target. Triggers on services: microsoft-ds. Command |
| `lazyown_tool_smbclient_tool` | tool | Run smbclient_tool against a target. Triggers on services: microsoft-ds, netbios |
| `lazyown_tool_smbmap_tool` | tool | Run smbmap_tool against a target. Triggers on services: microsoft-ds. Command te |
| `lazyown_tool_smbserver_tool` | tool | Run smbserver_tool against a target. Triggers on services: microsoft-ds. Command |
| `lazyown_tool_subwfuzz_tool` | tool | Run subwfuzz_tool against a target. Triggers on services: http, https, http-mgmt |
| `lazyown_tool_swaks_smtp_test` | tool | Run swaks_smtp_test against a target. Triggers on services: smtp. Command templa |
| `lazyown_tool_userenum_tool` | tool | Run userEnum_tool against a target. Triggers on services: microsoft-ds. Command  |
| `lazyown_tool_vncviewer_connect` | tool | Run vncviewer_connect against a target. Triggers on services: vnc. Command templ |

<!-- end auto-discovered -->
