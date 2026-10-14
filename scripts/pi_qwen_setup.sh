#!/bin/bash
# pi_qwen_setup.sh - idempotent bootstrap for the pi_qwen lazyaddon.
#
# Ensures the pi CLI is installed and registers the local llama.cpp Qwen
# endpoint as the "local-qwen" provider in Pi models.json, preserving any
# existing providers. Safe to run on every invocation.
#
# Usage:
#   pi_qwen_setup.sh [base_url] [model_id]
#
# Base URL defaults to the LazyOwn llama.cpp server. Model ID defaults to
# the alias that server exposes (local-model).

set -u

BASE_URL="${1:-http://127.0.0.1:8080}"
MODEL_ID="${2:-local-model}"
BASE_URL="${BASE_URL%/}"
AGENT_DIR="${PI_AGENT_DIR:-$HOME/.pi/agent}"
MODELS_JSON="$AGENT_DIR/models.json"

command -v node >/dev/null 2>&1 || { echo "ERROR: node 22.19+ required: https://nodejs.org"; exit 1; }

if ! command -v pi >/dev/null 2>&1; then
    echo "Installing pi CLI..."
    npm install -g --ignore-scripts @earendil-works/pi-coding-agent
fi
command -v pi >/dev/null 2>&1 || { echo "ERROR: pi CLI not found after install"; exit 1; }

mkdir -p "$AGENT_DIR"
if [ ! -f "$MODELS_JSON" ]; then
    echo '{"providers":{}}' > "$MODELS_JSON"
fi

PI_BASE_URL="$BASE_URL" PI_MODEL_ID="$MODEL_ID" PI_MODELS_JSON="$MODELS_JSON" python3 - <<'PYEOF'
import json
import os

path = os.environ["PI_MODELS_JSON"]
base = os.environ["PI_BASE_URL"].rstrip("/") + "/v1"
mid = os.environ["PI_MODEL_ID"]
size = os.path.getsize(path)
data = json.load(open(path)) if size else {}
if not isinstance(data, dict):
    data = {}
data.setdefault("providers", {})
data["providers"]["local-qwen"] = {
    "baseUrl": base,
    "api": "openai-completions",
    "apiKey": "local",
    "models": [{"id": mid}],
}
with open(path, "w") as fh:
    json.dump(data, fh, indent=2)
print("local-qwen -> " + base + " [" + mid + "]")
PYEOF

echo "pi ready. Run: pi --model local-qwen/$MODEL_ID --print \"...\""
