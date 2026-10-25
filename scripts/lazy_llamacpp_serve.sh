#!/bin/bash
# lazy_llamacpp_serve.sh — idempotent llama.cpp server manager for LazyOwn.
#
# Usage:
#   lazy_llamacpp_serve.sh           # ensure server up, print endpoint + status
#   lazy_llamacpp_serve.sh status    # health check only (exit 0/1)
#   lazy_llamacpp_serve.sh stop      # stop the server started from this repo
#
# Env overrides: LLAMACPP_HOST (default 127.0.0.1), LLAMACPP_PORT (8080),
# LLAMACPP_MODEL (gguf path), LLAMACPP_NGL (auto: 26 with NVIDIA GPU else 0),
# LLAMACPP_THREADS (default 8), LLAMACPP_CTX (default 65536).
#
# Non-interactive: safe for addon execute_command and fast_run panes.

set -u

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ADDON_DIR="$ROOT/external/.exploit/lazy_llamacpp"
BIN="$ADDON_DIR/build/bin/llama-server"
HOST="${LLAMACPP_HOST:-127.0.0.1}"
PORT="${LLAMACPP_PORT:-8080}"
MODEL="${LLAMACPP_MODEL:-$ADDON_DIR/models/Qwen3.8-27B-GSQ-RCO-IQ2_XS.gguf}"
PIDFILE="$ADDON_DIR/llama-server.pid"

if command -v nvidia-smi &>/dev/null && nvidia-smi -L &>/dev/null; then
    GPU_LAYERS="${LLAMACPP_NGL:-26}"
else
    GPU_LAYERS="${LLAMACPP_NGL:-0}"
fi
THREADS="${LLAMACPP_THREADS:-8}"
CTX="${LLAMACPP_CTX:-65536}"

healthy() {
    curl -sf -m 5 "http://$HOST:$PORT/health" >/dev/null 2>&1 || \
    curl -sf -m 5 "http://$HOST:$PORT/v1/models" >/dev/null 2>&1
}

action="${1:-up}"
case "$action" in
    status)
        if healthy; then echo "Lazy llama.cpp server UP at http://$HOST:$PORT/v1 (model: $(basename "$MODEL"))"; exit 0; fi
        echo "Lazy llama.cpp server DOWN ($HOST:$PORT)"; exit 1
        ;;
    stop)
        if [[ -f "$PIDFILE" ]] && kill -0 "$(cat "$PIDFILE")" 2>/dev/null; then
            kill "$(cat "$PIDFILE")" && echo "Stopped llama-server (pid $(cat "$PIDFILE"))"
        else
            pkill -f "llama-server.*--port $PORT" 2>/dev/null && echo "Stopped llama-server on port $PORT" || echo "No llama-server running on port $PORT"
        fi
        rm -f "$PIDFILE"
        exit 0
        ;;
    up) ;;
    *) echo "Usage: $0 [up|status|stop]"; exit 2 ;;
esac

if healthy; then
    echo "Lazy llama.cpp server already UP at http://$HOST:$PORT/v1 (model: $(basename "$MODEL"))"
    exit 0
fi

[[ -x "$BIN" ]] || { echo "ERROR: $BIN missing. Build first with: bash scripts/lazy_llamacpp_setup.sh"; exit 1; }
[[ -f "$MODEL" ]] || { echo "ERROR: model missing: $MODEL. Run: bash scripts/lazy_llamacpp_setup.sh"; exit 1; }

echo "Starting llama-server ($HOST:$PORT, ngl=$GPU_LAYERS, ctx=$CTX)..."
nohup "$BIN" --jinja -fa on --alias local-model \
    -m "$MODEL" -ngl "$GPU_LAYERS" -np 1 -c "$CTX" \
    --cache-type-k q4_0 --cache-type-v q4_0 \
    -t "$THREADS" -b 512 -ub 512 \
    --port "$PORT" --host "$HOST" \
    > "$ADDON_DIR/llama-server.log" 2>&1 &
echo $! > "$PIDFILE"

for _ in $(seq 1 60); do
    sleep 2
    healthy && { echo "Lazy llama.cpp server UP at http://$HOST:$PORT/v1 (model: $(basename "$MODEL"))"; exit 0; }
done
echo "ERROR: server did not become healthy in 120s. See $ADDON_DIR/llama-server.log"
exit 1
