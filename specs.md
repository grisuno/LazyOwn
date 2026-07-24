# LazyOwn — Specifications & Architecture

Version `release/0.2.156` — Last updated 2026-07-24

---

## 1. Project Overview

LazyOwn is a red-team framework providing a unified CLI, C2 web dashboard, MCP
server, and autonomous agent integration. It covers the full kill chain from
reconnaissance through data exfiltration with 360+ CLI commands, 200+ aliases,
and 120+ modules.

| Component | File | Lines | Description |
|-----------|------|-------|-------------|
| CLI Shell | `lazyown.py` | ~24,900 | cmd2 shell with all commands |
| C2 Server | `lazyc2.py` | ~6,360 | Flask + Socket.IO dashboard |
| MCP Server | `skills/lazyown_mcp.py` | ~10,140 | 131 tools for AI agents |
| Utils | `utils.py` | ~3,330 | Shared config, crypto, helpers |
| DB | `modules/db.py` | SQLite | Workspaces, hosts, services |
| Module Registry | `modules/module_registry.py` | ~540 | 120+ module catalog |
| Payload Factory | `modules/payload_factory.py` | Native | Shellcode, PS, rev shells |

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
   | modules/     | | cli/        | | skills/     |
   | db, llm,     | | commands/,  | | mcp, auto,  |
   | registry,    | | aliases,    | | hive, etc.  |
   | payload      | | registry    | |             |
   +-------------+ +------------+ +-------------+
```

### 2.1 Shared Backend

`utils.py` exports 292 public names: Config class, run_command wrapper,
color/format constants, crypto primitives, and re-exports of common stdlib
modules (os, sys, json, re, subprocess, etc.). Both CLI and C2 import from it.

### 2.2 Configuration

`payload.json` (82 keys) is the single source of truth. Always read at startup;
never written except through `do_assign`, `do_set`, or `lazyown_set_config`.
Schema is validated at module load by `core/config.py`.

### 2.3 CommandSet Deconstruction

The monolith `lazyown.py` (~24,900 lines, 369 `do_*` methods) is being
deconstructed into `cli/commands/` CommandSet modules:

| Phase | Migrated | Active | Total |
|-------|----------|--------|-------|
| Recon | 28 | 12 | 40 |
| Scan | 45 | 16 | 61 |
| Enumeration | - | 10 | 10 |
| Exploitation | 47 | 10 | 57 |
| Post-exploitation | 35 | 8 | 43 |
| Persistence | 23 | 6 | 29 |
| Credential access | 22 | 9 | 31 |
| Lateral movement | 20 | 8 | 28 |
| Reporting | 16 | 8 | 24 |
| C2 | 22 | 6 | 28 |
| Exfiltration | - | 18 | 18 |
| Misc / AI / Cloud / DB | 101 | 42 | 143 |

**Migration mechanism**: Migrated copies live in `*_migrated.py` files inheriting
from `PendingCommandSet` (dormant). When originals are deleted from
`lazyown.py`, the base class is swapped to `LazyOwnCommandSet`. This is tracked
by `cli/commands/_dormancy.py` and `cli/registry.py`.

**Remaining work**: 359 methods are copied but still dormant; 10 commands
(cloud_enum, adcs_check, dominion, hunt, phisher, lazyreport, evasive, chain,
beaconcfg, yara_scan) were added after the last auto-migration and are staged in
`cli/commands/unmigrated_batch.py`. Delete originals + swap base class to
activate.

### 2.4 CLI CommandSet Base Class

`cli/commands/_base.py` defines `LazyOwnCommandSet(cmd2.CommandSet)`:

- **`params` property**: Returns the live `payload.json` dict.
- **`payload` property**: Returns the `Config` wrapper.
- **`__getattr__` forwarding**: Unknown attribute access (e.g., `self.run_script`,
  `self.c2_url`) is forwarded to the parent shell. This lets migrated methods run
  verbatim without rewriting call sites.

---

## 3. Data Flow

### 3.1 CLI Session

```
User input → cmd2 parsing → do_<name>(line) → run_command(cmd_str)
    → subprocess execution → output capture → CSV logging → toast/stderr
```

### 3.2 C2 Session

```
Beacon → HTTPS POST /api/beacon → Flask → Socket.IO event
    → operator dashboard → command queue → beacon poll → execute
```

### 3.3 MCP Session

```
AI agent → MCP tool call → lazyown_mcp dispatch table (O(1))
    → lazyown_set_config / lazyown_run_command → lazyown shell
    → result → JSON response
```

---

## 4. Kill Chain Phases

| # | Phase | Commands |
|---|-------|----------|
| 01 | Reconnaissance | lazynmap, dig, dnsenum, whatweb, gobuster |
| 02 | Scanning & Enumeration | nmapscript, wfuzz, dirb, sslyze |
| 03 | Exploitation | hunt, chain, exploit, searchsploit |
| 04 | Post-Exploitation | linpeas, winpeas, shell, upload, download |
| 05 | Persistence | backdoor, cron, service, schtask |
| 06 | Privilege Escalation | adcs_check, dominion, getsystem |
| 07 | Credential Access | secretsdump, evil, getnpusers, hash |
| 08 | Lateral Movement | psexec, wmiexec, bloodhound, pivot |
| 09 | Data Exfiltration | exfil, zip, compress, send |
| 10 | Command & Control | srv, beaconcfg, phisher, listener |
| 11 | Reporting | lazyreport, chain report |

---

## 5. Module System

### 5.1 Discovery

`modules/module_registry.py` scans five sources:
- `lazyaddons/` — YAML tool integrations (76 entries)
- `plugins/` — Lua + YAML plugins
- `modules/` — Python modules
- `tools/` — pwntomate auto-jobs
- `playbooks/` — Playbook definitions

### 5.2 Classification

Keyword-based auto-classification maps modules to kill-chain phases. Python
modules are also classified by AST docstring scanning via
`_classify_module_source()`.

---

## 6. Database Schema (SQLite)

`modules/db.py` manages campaign state with migration system (v2→v4):

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

### 8.1 MCP Tools (131 total)

Essential tools for AI agents:
- `lazyown_campaign_sitrep` — Aggregate all campaign state
- `lazyown_session_init` — Initialize session, check scans
- `lazyown_set_config` — Set target, attacker IP
- `lazyown_run_command` — Execute any LazyOwn command
- `lazyown_auto_populate` — Parse nmap XML into world model
- `lazyown_facts_show` — Display discovered services
- `lazyown_recommend_next` — Groq-ranked next commands

### 8.2 Auto-Loop

`lazyown_auto_loop()` runs autonomous kill-chain progression: recon → scan →
auto_populate → recommend → execute → repeat. Self-healing recovers from stuck
loops.

---

## 9. Code Quality Standards

1. English only — identifiers, strings, logs, docstrings.
2. No comments — self-explanatory names + docstrings only.
3. Docstrings on every public function/class (Args/Returns/Raises).
4. No magic numbers — constants in Config or UPPER_SNAKE.
5. No hardcoded paths/ports — use `payload.json`.
6. SOLID: single responsibility, open for extension.
7. Every directory gets `README.md`.
8. Explicit imports only — no wildcards (`from utils import *` removed 2026-07-24).

---

## 10. Branching Model

| Branch | Purpose | Agent Access |
|--------|---------|-------------|
| `dev` | Active development, daily commits | Read/write |
| `pp` | Pre-production / staging, QA | Read-only |
| `main` | Production releases, tagged only | Read-only |

Agents operate on `dev`. Feature branches cut from `dev`. Hotfixes from `main`.
PRs from `dev` → `pp` require human approval.

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
