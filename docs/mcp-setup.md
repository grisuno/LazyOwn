## MCP Quick Start

LazyOwn exposes its full framework via the Model Context Protocol (MCP). The same server works with Claude Code, Claude Desktop, Hermes Agent, and OpenCode — pick the integration that matches your environment.

### Claude Code

```bash
bash scripts/setup_hermes_mcp.sh
```

Or copy `.mcp.example.json` to `.mcp.json` and set `LAZYOWN_DIR` to the
absolute path of this checkout:

```json
{
  "mcpServers": {
    "lazyown": {
      "command": "python3",
      "args": ["${LAZYOWN_DIR}/skills/lazyown_mcp.py"],
      "env": {
        "LAZYOWN_DIR": "${LAZYOWN_DIR}"
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
    args: ["${LAZYOWN_DIR}/skills/hermes-lazyown/mcp_server.py"]
    env:
      LAZYOWN_DIR: "${LAZYOWN_DIR}"
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

## MCP Tool Groups (153 tools)

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
