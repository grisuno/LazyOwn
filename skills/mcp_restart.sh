#!/usr/bin/env bash
# LazyOwn MCP reload helper
# Sends SIGHUP so the server re-execs itself with new code WITHOUT dropping
# the stdio connection to Claude Code — no /mcp needed.
# Usage: bash skills/mcp_restart.sh
#
# Falls back to SIGTERM (full restart) only if the process doesn't come back.

set -euo pipefail

MCP_SCRIPT="skills/lazyown_mcp.py"

pids=$(pgrep -f "python3.*$MCP_SCRIPT" 2>/dev/null || true)

if [ -z "$pids" ]; then
    echo "[mcp] Server is not running — Claude Code will start it on the next tool call."
    exit 0
fi

echo "[mcp] Reloading server (pid $pids) via SIGHUP..."
kill -HUP $pids

# Give it 2 s to re-exec
sleep 2

new_pids=$(pgrep -f "python3.*$MCP_SCRIPT" 2>/dev/null || true)
if [ -n "$new_pids" ]; then
    echo "[mcp] Reloaded OK (pid $new_pids). No /mcp needed."
else
    echo "[mcp] Process did not come back — Claude Code will restart it on next tool call."
fi
