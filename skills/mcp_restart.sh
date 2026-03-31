#!/usr/bin/env bash
# LazyOwn MCP restart helper
#
# Kills any running instance and relaunches in SSE daemon mode (port 9871).
# Claude Code connects via:  http://127.0.0.1:9871/sse  (lazyown-sse server)
# The stdio server (lazyown) is still managed by Claude Code automatically.
#
# Usage: bash skills/mcp_restart.sh [PORT]

set -euo pipefail

PORT="${1:-9871}"
MCP_SCRIPT="/home/grisun0/LazyOwn/skills/lazyown_mcp.py"
PYTHON="/home/grisun0/LazyOwn/env/bin/python3"
[ -x "$PYTHON" ] || PYTHON="python3"
LOG="/tmp/lazyown_mcp_sse.log"

# Kill existing instances (stdio + SSE)
pids=$(pgrep -f "python3.*lazyown_mcp" 2>/dev/null || true)
if [ -n "$pids" ]; then
    echo "[mcp] Stopping existing server(s): $pids"
    kill $pids 2>/dev/null || true
    sleep 1
fi

# Launch SSE daemon
echo "[mcp] Starting SSE daemon on http://127.0.0.1:$PORT/sse ..."
nohup "$PYTHON" "$MCP_SCRIPT" --sse "$PORT" \
    </dev/null >>"$LOG" 2>&1 &
NEW_PID=$!
sleep 2

if kill -0 "$NEW_PID" 2>/dev/null; then
    echo "[mcp] SSE server running (PID $NEW_PID). Log: $LOG"
    echo "[mcp] Claude Code reconnects automatically on next /mcp or tool call."
else
    echo "[mcp] ERROR: server failed to start. Check $LOG"
    tail -20 "$LOG"
    exit 1
fi
