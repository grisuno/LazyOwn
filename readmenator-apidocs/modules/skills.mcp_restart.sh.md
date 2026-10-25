# `skills/mcp_restart.sh`

> Source: [skills/mcp_restart.sh:1](../../skills/mcp_restart.sh#L1) | language `sh` | coverage 100.0% | [API index](../index.md)

LazyOwn MCP restart helper  Kills ALL lazyown_mcp instances (stdio + SSE) and relaunches the SSE daemon.

After running this script: - The stdio server (lazyown) will be dead — Claude Code requires /mcp to reconnect. - The SSE daemon (lazyown-sse) will be running on http://127.0.0.1:PORT/sse  NOTE: The comment "Claude Code reconnects automatically" was WRONG. For stdio transport, reconnect is MANUAL via /mcp. For SSE transport (lazyown-sse), Claude Code reconnects automatically.  Usage: bash skills/mcp_restart.sh [PORT]
