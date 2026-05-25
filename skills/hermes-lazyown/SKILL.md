---
name: hermes-lazyown
description: "Use when running LazyOwn inside a Hermes agent session. Provides Hermes-optimized MCP tools with compact output, checkpoint resume, dynamic rules, and native delegation planning."
version: 1.0.0
author: LazyOwn RedTeam
platforms: [linux]
metadata:
  hermes:
    tags: [pentest, redteam, mcp, lazyown, hermes]
    homepage: https://github.com/grisuno/LazyOwn
    related_skills: [lazyown]
---

# Hermes-LazyOwn Integration

Hermes-native MCP layer for the LazyOwn red-team framework.

**Location:** `skills/hermes-lazyown/`
**Server:** `skills/hermes-lazyown/mcp_server.py`
**Purpose:** Compact, namespaced tool surface optimized for Hermes context windows.

## Architecture

```
Hermes Agent -> MCP -> skills/hermes-lazyown/mcp_server.py
                              |
                    +---------+---------+---------+
                    |         |         |         |
              config_bridge  compactor  sync     executor
                    |         |         |         |
              payload.json  sessions/  todo      lazyown.py
```

## Key Files

| File | Purpose |
|------|---------|
| `mcp_server.py` | MCP server with namespaced tools |
| `config_bridge.py` | Unified config: env -> payload.json -> defaults |
| `output_compactor.py` | Phase-aware output compaction |
| `hermes_sync.py` | Checkpoint, todo sync, delegation plans |
| `claudemd_rules.py` | Dynamic system prompt rules |
| `executor.py` | Subprocess execution with PTY fallback |
| `constants.py` | Central constants, no magic numbers |

## Essential Tools (7)

| Tool | Purpose |
|------|---------|
| `lazyown_core_session_init` | SITREP at start of every session |
| `lazyown_core_set_config` | Update payload.json |
| `lazyown_core_run_command` | Execute LazyOwn CLI commands |
| `lazyown_intel_recommend_next` | AI-ranked next commands |
| `lazyown_auto_inject_objective` | Queue attack objectives |
| `lazyown_hermes_checkpoint_write` | Save state for resume |
| `lazyown_hermes_rules_generate` | Dynamic context rules |

## Namespaces

| Prefix | Phase | Tools |
|--------|-------|-------|
| `lazyown_core_*` | All | session_init, set_config, run_command, command_help |
| `lazyown_intel_*` | Intel | facts_show, recommend_next, searchsploit |
| `lazyown_auto_*` | Autonomous | auto_loop, inject_objective |
| `lazyown_hermes_*` | Hermes | checkpoint_write/read, rules_generate, delegate_plan |
| `lazyown_c2_*` | C2 | status, get_beacons |

## Dynamic Rules

Call `lazyown_hermes_rules_generate` to inject phase-specific constraints into the system prompt.

## Checkpoints

Long engagements exceed Hermes max_turns. Write checkpoints with `lazyown_hermes_checkpoint_write` and read them at session start with `lazyown_hermes_checkpoint_read`.

## Setup

Register in Hermes config.yaml:

```yaml
mcp_servers:
  hermes-lazyown:
    command: python3
    args: ["/home/grisun0/LazyOwn/skills/hermes-lazyown/mcp_server.py"]
    env:
      LAZYOWN_DIR: "/home/grisun0/LazyOwn"
```

## Documentation

- Full MCP playbook: `skills/lazyown.md`
- LazyOwn skill: `skills/lazyown/SKILL.md`
