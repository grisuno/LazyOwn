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
