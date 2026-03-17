# LazyOwn Skills — MCP Integration

Connect Claude Code (and Claude web) to the LazyOwn framework.

## Files

| File | Purpose |
|------|---------|
| `lazyown_mcp.py` | MCP server — exposes LazyOwn as 10 Claude tools |
| `lazyown.md` | Claude Code skill / slash-command documentation |

## Quick Start

### 1. Register the MCP server in Claude Code

Add this to `~/.claude/claude_desktop_config.json` (or `~/.config/claude/claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "lazyown": {
      "command": "python3",
      "args": ["~/LazyOwn/skills/lazyown_mcp.py"],
      "env": {
        "LAZYOWN_DIR": "~/LazyOwn"
      }
    }
  }
}
```

Or register via the CLI:

```bash
claude mcp add lazyown python3 /home/grisun0/LazyOwn/skills/lazyown_mcp.py
```

### 2. Install the skill (optional, for /lazyown slash command)

```bash
cp skills/lazyown.md ~/.claude/commands/lazyown.md
```

### 3. Use from Claude Code

After restarting Claude Code, the `lazyown_*` tools are available automatically.
Type `/lazyown` to load the skill prompt.

```
You: set the target to 10.10.11.78 and run an nmap scan
Claude: [calls lazyown_set_config then lazyown_run_command("lazynmap")]
```

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `LAZYOWN_DIR` | parent of skills/ | LazyOwn root directory |
| `LAZYOWN_C2_HOST` | payload.json `lhost` | C2 server address |
| `LAZYOWN_C2_PORT` | payload.json `c2_port` | C2 server port |
| `LAZYOWN_C2_USER` | payload.json `c2_user` | C2 username |
| `LAZYOWN_C2_PASS` | payload.json `c2_pass` | C2 password |

## Exposed Tools

| MCP Tool | Description |
|----------|-------------|
| `lazyown_run_command` | Run any LazyOwn shell command |
| `lazyown_get_config` | Read payload.json |
| `lazyown_set_config` | Write payload.json |
| `lazyown_list_modules` | List modules/ contents |
| `lazyown_get_beacons` | List connected C2 beacons |
| `lazyown_c2_command` | Task a beacon |
| `lazyown_run_api` | Execute command via C2 REST API |
| `lazyown_list_sessions` | Browse sessions/ directory |
| `lazyown_read_session_file` | Read a session file |
| `lazyown_c2_status` | C2 health check + dashboard data |
