#!/usr/bin/env bash
# LazyOwn MCP restart helper
# Sends SIGHUP for a clean exit. Claude Code auto-restarts the server on
# the next tool call — no /mcp needed.
# Usage: bash skills/mcp_restart.sh

set -euo pipefail

MCP_SCRIPT="skills/lazyown_mcp.py"

pids=$(pgrep -f "python3.*$MCP_SCRIPT" 2>/dev/null || true)

if [ -z "$pids" ]; then
    echo "[mcp] Server is not running — Claude Code starts it automatically on next tool call."
    exit 0
fi

echo "[mcp] Stopping server (pid $pids)..."
kill -HUP $pids 2>/dev/null || kill $pids 2>/dev/null || true

sleep 1
echo "[mcp] Done. Claude Code will restart the server automatically on the next tool call."
