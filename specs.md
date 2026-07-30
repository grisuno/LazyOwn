# LazyOwn -- Specifications & Architecture

Version `release/0.2.157` -- Last updated 2026-07-30

---

## 1. Project Overview

LazyOwn is a red-team framework providing a unified CLI, C2 web dashboard, MCP
server, and autonomous agent integration. It covers the full kill chain from
reconnaissance through data exfiltration with 600+ CLI commands, 120+ aliases,
and 100+ modules.

| Component | File | Lines | Description |
|-----------|------|-------|-------------|
| CLI Shell | `lazyown.py` | ~4,500 | cmd2 shell + cmd2 CommandSets |
| C2 Server | `lazyc2.py` | ~6,400 | Flask + Socket.IO dashboard |
| MCP Server | `skills/lazyown_mcp.py` | ~10,600 | 131+ tools for AI agents |
| Utils | `utils.py` | ~3,400 | Shared config, crypto, helpers |
| DB | `modules/db.py` | ~700 | SQLite workspace isolation |
| Module Registry | `modules/module_registry.py` | ~540 | 100+ module catalog |
| Payload Factory | `modules/payload_factory.py` | ~720 | Native shellcode, PS, rev shells |
| CommandSets (active) | `cli/commands/*.py` | ~9,000 | Phase-scoped cmd2 CommandSets |
| CommandSets (pending) | `cli/commands/*_migrated.py` | ~20,900 | Dormant migration copies |
| Lab Manager | `cli/commands/lab.py` | ~200 | Docker CTF lab orchestration |
| Marketplace | `cli/commands/marketplace.py` | ~250 | Plugin/addon discovery |

---

## 2. Architecture Layers

```
+------------------+     +------------------+     +------------------+
|   CLI (cmd2)     |     |   C2 (Flask)     |     |  MCP (FastMCP)   |
|   lazyown.py     |     |   lazyc2.py      |     | lazyown_mcp.py   |
+--------+---------+     +--------+---------+     +--------+---------+
         |                        |                        |
         +------------------------+------------------------+
                         |
                    +-----v------+
                    |   utils.py  |  Config, run_command, helpers
                    +-----+------+
                          |
          +---------------+---------------+
          |               |               |
   +------v------+ +-----v------+ +------v------+
   | cli/commands/| | modules/    | | skills/     |
   | 23 CommandSets| | db, llm,    | | mcp, auto,  |
   | per-phase    | | registry,   | | hive, etc.  |
   +-------------+ +------------+ +-------------+
```

### 2.1 Shared Backend

`utils.py` exports 150+ public names: Config class, run_command wrapper,
color/format constants, crypto primitives, and re-exports of common stdlib
modules. Both CLI and C2 import from it. Wildcard imports were replaced with
66 explicit symbols (2026-06).

### 2.2 Configuration

`payload.json` (82 keys) is the single source of truth. Always read at startup;
never written except through `do_assign`, `do_set`, or `lazyown_set_config`.
Schema validated at module load by `core/config.py`.

### 2.3 CommandSet Architecture

The original monolith `lazyown.py` (~24,900 lines, 369 `do_*` methods) has been
deconstructed into `cli/commands/` CommandSet modules. Currently:

- **23 active CommandSets** registered at boot via `cli/registry.py`
- **10 migrated modules (`*_migrated.py`)** with 20,885 lines, using
  `PendingCommandSet` from `_dormancy.py`. These are dormant copies waiting for
  the originals to be deleted from `lazyown.py` before activation.

Migration phases completed: recon (12 commands), enum (10), scan, exploit (10),
postexp (8), persist (7), cred (9), lateral (8), report (8). Pending phases in
migrated files: the remaining ~200 `do_*` methods.

### 2.4 CLI CommandSet Base Class

`cli/commands/_base.py` defines `LazyOwnCommandSet(cmd2.CommandSet)`:

- **`params` property**: Returns the live `payload.json` dict.
- **`payload` property**: Returns the `Config` wrapper.
- **`__getattr__` forwarding**: Unknown attribute access (e.g., `self.run_script`,
  `self.c2_url`) is forwarded to the parent shell.

---

## 3. Data Flow

### 3.1 CLI Session

```
User input -> cmd2 parsing -> do_<name>(line) -> run_command(cmd_str)
    -> subprocess execution -> output capture -> CSV logging -> toast/stderr
```

### 3.2 C2 Session

```
Beacon -> HTTPS POST /api/beacon -> Flask -> Socket.IO event
    -> operator dashboard -> command queue -> beacon poll -> execute
```

### 3.3 MCP Session

```
AI agent -> MCP tool call -> lazyown_mcp dispatch table (O(1))
    -> lazyown_set_config / lazyown_run_command -> lazyown shell
    -> result -> JSON response
```

---

## 4. Kill Chain Phases

| # | Phase | Commands |
|---|-------|----------|
| 01 | Reconnaissance | lazynmap, dig, dnsenum, whatweb, gobuster |
| 02 | Scanning & Enumeration | nmapscript, wfuzz, dirb, sslyze |
| 03 | Exploitation | hunt, chain, exploit, searchsploit, auto_pwn |
| 04 | Post-Exploitation | linpeas, winpeas, shell, upload, download |
| 05 | Persistence | backdoor, cron, service, schtask |
| 06 | Privilege Escalation | adcs_check, dominion, getsystem |
| 07 | Credential Access | secretsdump, evil, getnpusers, hash |
| 08 | Lateral Movement | psexec, wmiexec, bloodhound, pivot |
| 09 | Data Exfiltration | exfil, zip, compress, send |
| 10 | Command & Control | srv, beaconcfg, phisher, listener |
| 11 | Reporting | lazyreport, chain report |

**Autonomous modes** -- `engage` (fixed chain) and `orchestrate` (daemon/hive/swan)
can walk the full kill chain with optional human gating.

---

## 5. Module System

### 5.1 Discovery

`modules/module_registry.py` scans five sources:
- `lazyaddons/` -- YAML tool integrations (96 entries)
- `plugins/` -- Lua + YAML plugins (60+ entries)
- `modules/` -- Python modules
- `tools/` -- pwntomate auto-jobs (72 entries)
- `marketplace` -- community plugin index (`lazyown-community-plugins`)

### 5.2 Classification

Keyword-based auto-classification maps modules to kill-chain phases. Python
modules also classified by AST docstring scanning via `_classify_module_source()`.

### 5.3 Marketplace

`cli/commands/marketplace.py` provides `marketplace list|search|install|update|info`
for discovering community plugins, lazyaddons, and tool integrations.

### 5.4 Lab Manager

`cli/commands/lab.py` provides `lab list|start|stop|status` for spinning up
Docker-based CTF practice targets (DVWA, Metasploitable2, Juice Shop, vulnerable
Tomcat, Struts2, AD lab, etc.).

---

## 6. Database Schema (SQLite)

`modules/db.py` manages campaign state with migration system (v2->v4):

- **workspaces**: Campaign isolation
- **hosts**: Discovered targets
- **services**: Port/protocol/service/version
- **vulnerabilities**: CVEs matched to services
- **credentials**: Captured creds, hashes, tokens
- **loot**: Files, screenshots, keylogs
- **notes**: Freeform operator notes
- **scan_files**: nmap XML import tracking

---

## 7. Security Architecture

### 7.1 C2 Security (`lazyc2/security/`)

- **CORS policy**: Environment-aware (DEV allows `*`, PROD enforces whitelist)
- **CSRF protection**: All state-changing endpoints; exempts `/login`, `/api/beacon`
- **HTTPS redirect**: Enforced in production
- **AES encryption**: Beacon traffic encrypted with per-session keys
- **Password validation**: Rejects blank, common defaults, or < 12 chars
- **RBAC** (optional): MFA/TOTP, multi-tenant, roles, permissions

### 7.2 Scope Enforcement

`scope_enforcement` in `payload.json` controls target restrictions:
- `off`: No enforcement
- `warn`: Log warning for out-of-scope targets
- `enforce`: Block out-of-scope operations

---

## 8. Hermes AI Integration

### 8.1 MCP Tools (131+ total)

Essential tools for AI agents:
- `lazyown_campaign_sitrep` -- Aggregate all campaign state
- `lazyown_session_init` -- Initialize session, check scans
- `lazyown_set_config` -- Set target, attacker IP
- `lazyown_run_command` -- Execute any LazyOwn command
- `lazyown_auto_populate` -- Parse nmap XML into world model
- `lazyown_facts_show` -- Display discovered services
- `lazyown_recommend_next` -- Groq-ranked next commands

### 8.2 Auto-Loop

Multiple autonomous backends:
- **engage**: Fixed kill-chain walk with human gating
- **daemon**: Objective-driven autonomous loop (local, offline)
- **hive**: Queen/drone swarm with shared memory
- **swan**: MoE+RL router that learns from outcomes

---

## 9. Code Quality Standards

1. English only -- identifiers, strings, logs, docstrings.
2. No comments -- self-explanatory names + docstrings only.
3. Docstrings on every public function/class (Args/Returns/Raises).
4. No magic numbers -- constants in Config or UPPER_SNAKE.
5. No hardcoded paths/ports -- use `payload.json`.
6. SOLID: single responsibility, open for extension.
7. Every directory gets `README.md`.
8. Explicit imports only -- no wildcards (phased out 2026-06/07).

---

## 10. Branching Model

| Branch | Purpose | Agent Access |
|--------|---------|-------------|
| `dev` | Active development, daily commits | Read/write |
| `pp` | Pre-production / staging, QA | Read-only |
| `main` | Production releases, tagged only | Read-only |

Agents operate on `dev`. Feature branches cut from `dev`. Hotfixes from `main`.
PRs from `dev` -> `pp` require human approval.

---

## 11. Key Dependencies

- **cmd2**: CLI framework
- **Flask + Socket.IO**: C2 web dashboard
- **Impacket**: Windows exploitation suite
- **libnmap**: nmap XML parsing
- **Groq**: LLM inference for recommendations
- **scapy**: Packet crafting
- **dnslib**: DNS tunneling
- **cryptography**: AES encryption
- **networkx + pyvis**: Beacon graph visualization
- **textual**: TUI dashboard and command palette

---

## 12. Deploy & Lab

- **Docker**: `lazyown-docker/` with multi-stage build, OpenVPN integration, Docker Compose
- **Kubernetes**: `deploy/k8s/lazyown-c2.yaml` for C2 deployment
- **Lab**: `lab start metasploitable` spins up Docker-based practice targets
- **Marketplace**: `marketplace install <plugin>` from community index
