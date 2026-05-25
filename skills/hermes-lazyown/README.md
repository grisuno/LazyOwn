# Hermes-LazyOwn Integration Layer

Hermes-native MCP server and support modules for the LazyOwn red-team framework.

## Purpose

The main LazyOwn MCP server (`skills/lazyown_mcp.py`) exposes ~131 tools. This integration layer provides a compact, namespaced subset optimized for Hermes agent context windows and production reliability.

## Design Principles

- **SOLID**: single responsibility per module, small interfaces, dependency on abstractions
- **No hardcoded values**: all paths, ports, timeouts from `payload.json` or environment variables
- **Graceful degradation**: every external dependency is optional with informative fallback
- **Phase-aware compaction**: verbose tool output is reduced based on the current engagement phase
- **Hermes-native**: checkpoint resume, todo sync, and delegation planning integrate with Hermes primitives

## Modules

### constants.py
Central constants, configuration keys, and path resolution. No magic numbers.

### config_bridge.py
Unified configuration adapter. Reads from (highest priority first):
1. Environment variables (`LAZYOWN_*`, `HERMES_*`)
2. `payload.json`
3. Built-in defaults

### output_compactor.py
Phase-aware output compaction using the Strategy pattern.

| Phase | Strategy |
|-------|----------|
| recon | Keep open ports, services, OS guesses only |
| enum  | Keep findings, deduplicate against known state |
| exploit | Keep success/failure and access level only |
| privesc | Keep vectors found and commands executed |

### hermes_sync.py
- `CheckpointSerializer`: save/load engagement state for resume across turns
- `ObjectiveTodoSync`: bidirectional sync between `objectives.jsonl` and Hermes todo items
- `DelegationPlanner`: generate parallel task descriptors for `delegate_task`

### claudemd_rules.py
Dynamic rule generation for the Hermes system prompt. Builds markdown constraints based on current phase, discovered services, and credential state.

### executor.py
LazyOwn CLI execution via subprocess with PTY support and timeout handling.

### mcp_server.py
The MCP server entry point. Exposes namespaced tools:

- `lazyown_core_*` - Session management and command execution
- `lazyown_intel_*` - Intelligence gathering and recommendations
- `lazyown_auto_*` - Autonomous loop and objective injection
- `lazyown_hermes_*` - Hermes-native integration primitives
- `lazyown_c2_*` - C2 status and beacon enumeration

## Registration

Add to `~/.hermes/config.yaml`:

```yaml
mcp_servers:
  hermes-lazyown:
    command: python3
    args:
      - /home/grisun0/LazyOwn/skills/hermes-lazyown/mcp_server.py
    env:
      LAZYOWN_DIR: /home/grisun0/LazyOwn
      HERMES_MAX_OUTPUT_LINES: "2000"
      HERMES_CMD_TIMEOUT: "60"
```

Then reload MCP tools in Hermes with `/reload-mcp`.

## Testing

Run the server standalone for smoke testing:

```bash
cd /home/grisun0/LazyOwn
python3 skills/hermes-lazyown/mcp_server.py
```

It expects JSON-RPC over stdio as per the MCP protocol.

## Relationship to LazyOwn

This layer is additive. The original `skills/lazyown_mcp.py` remains the canonical full-featured MCP server. Use this layer when:

- Hermes context window is constrained
- You need checkpoint/resume across long engagements
- You want dynamic rule injection based on phase
- You want Hermes-native delegation plans
