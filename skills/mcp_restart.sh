#!/usr/bin/env bash
# LazyOwn MCP restart helper
# Kills the running lazyown_mcp.py process so Claude Code restarts it automatically.
# Usage: bash skills/mcp_restart.sh

set -euo pipefail

MCP_SCRIPT="skills/lazyown_mcp.py"
LAZYOWN_DIR="$(cd "$(dirname "$0")/.." && pwd)"
MCP_FULL="$LAZYOWN_DIR/$MCP_SCRIPT"

pids=$(pgrep -f "python3.*$MCP_SCRIPT" 2>/dev/null || true)

if [ -z "$pids" ]; then
    echo "[mcp_restart] MCP server is not running."
    echo "[mcp_restart] Claude Code will start it automatically on the next tool call."
    exit 0
fi

echo "[mcp_restart] Stopping MCP server (pid(s): $pids)..."
kill $pids

# Wait up to 3 s for clean exit
for i in 1 2 3; do
    sleep 1
    remaining=$(pgrep -f "python3.*$MCP_SCRIPT" 2>/dev/null || true)
    if [ -z "$remaining" ]; then
        echo "[mcp_restart] Stopped cleanly."
        break
    fi
    if [ $i -eq 3 ]; then
        echo "[mcp_restart] Force-killing..."
        kill -9 $remaining 2>/dev/null || true
    fi
done

echo "[mcp_restart] Done. Claude Code will restart the MCP server on the next tool call."
echo "[mcp_restart] You can also run /mcp in the Claude Code prompt to reconnect immediately."
