# Publishing LazyOwn MCP

## Registry entries

- Glama: submit `skills/lazyown_mcp.py` with transport stdio, env `LAZYOWN_DIR`.
- mcp.so / Smithery: same entrypoint, tag with `redteam`, `c2`, `pentest`, `mcp`.
- Claude Code: `claude mcp add lazyown python3 <repo>/skills/lazyown_mcp.py`.
- Claude Desktop: add to `claude_desktop_config.json` under `mcpServers.lazyown`.
- OpenCode: via LazyOwnOpenCodeAdapter (see README).

## Pre-publish checklist

- `bash skills/mcp_restart.sh` passes after edits.
- `lazyown_session_init(format='json')` returns structured SITREP.
- Destructive tools require `confirm=true`.
- Docs: `skills/lazyown.md` slash-command copy installed.

## Demo script (60s)

1. `claude mcp add lazyown ...` (5s).
2. `lazyown_session_init` JSON SITREP (10s).
3. `lazyown_recommend_next` ranked actions (10s).
4. `lazyown_run_command('lazynmap', dry_run=true)` preflight (15s).
5. `lazyown_campaign_sitrep` shift report (10s).
GIF: `assets/demo/mcp-ai.gif`.
