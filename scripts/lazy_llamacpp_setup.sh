#!/bin/bash
# lazy_llamacpp_setup.sh — one-time local LLM setup for LazyOwn users.
#
# Interactively (or via flags) it:
#   1. builds llama.cpp from the lazy_llamacpp addon clone (CUDA when present),
#   2. downloads the Qwen 27B GGUF model (~8GB, asks first),
#   3. starts the server through lazy_llamacpp_serve.sh,
#   4. optionally patches opencode (~/.config/opencode/opencode.json),
#   5. optionally patches hermes (~/.hermes/config.yaml),
#   6. optionally sets payload.json local_llm so fast_run uses it.
#
# Flags (all default to asking):
#   --yes            accept every default without prompting
#   --no-download    skip the model download (reuse existing models/*.gguf)
#   --no-opencode    skip opencode config patch
#   --no-hermes      skip hermes config patch
#   --no-payload     skip payload.json local_llm change
#
# The operator's existing setup is never touched without an explicit yes.

set -u

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ADDON_DIR="$ROOT/external/.exploit/lazy_llamacpp"
MODEL_FILE="Qwen3.8-27B-GSQ-RCO-IQ2_XS.gguf"
MODEL_URL="https://huggingface.co/ISTA-DASLab/Qwen3.8-27B-GSQ-RCO-GGUF/resolve/main/$MODEL_FILE"
YES=0; NO_DOWNLOAD=0; NO_OPENCODE=0; NO_HERMES=0; NO_PAYLOAD=0

for arg in "$@"; do
    case "$arg" in
        --yes) YES=1 ;;
        --no-download) NO_DOWNLOAD=1 ;;
        --no-opencode) NO_OPENCODE=1 ;;
        --no-hermes) NO_HERMES=1 ;;
        --no-payload) NO_PAYLOAD=1 ;;
        *) echo "Unknown flag: $arg"; exit 2 ;;
    esac
done

ask() {
    # ask <question> <default:Y|N> -> 0=yes
    local prompt="$1" default="$2" reply
    if [[ "$YES" == "1" ]]; then [[ "$default" == "Y" ]]; return; fi
    read -r -p "$prompt [$default] " reply
    reply="${reply:-$default}"
    [[ "$reply" =~ ^[Yy] ]]
}

if [[ ! -x "$ADDON_DIR/build/bin/llama-server" ]]; then
    echo "[1/6] Building llama.cpp (takes several minutes)..."
    [[ -d "$ADDON_DIR/.git" ]] || git clone --depth 1 https://github.com/ggml-org/llama.cpp.git "$ADDON_DIR"
    if command -v nvcc &>/dev/null || (command -v nvidia-smi &>/dev/null && nvidia-smi -L &>/dev/null); then
        cmake -B "$ADDON_DIR/build" -DGGML_CUDA=ON "$ADDON_DIR"
    else
        echo "No NVIDIA GPU detected: CPU-only build."
        cmake -B "$ADDON_DIR/build" "$ADDON_DIR"
    fi
    cmake --build "$ADDON_DIR/build" --config Release -j "$(nproc)"
else
    echo "[1/6] llama-server binary already built, skipping."
fi

mkdir -p "$ADDON_DIR/models"
if ls "$ADDON_DIR"/models/*.gguf >/dev/null 2>&1; then
    echo "[2/6] Model already present: $(ls "$ADDON_DIR"/models/*.gguf | head -1)"
elif [[ "$NO_DOWNLOAD" == "1" ]]; then
    echo "[2/6] Skipped download (--no-download); server start will fail until a model lands in $ADDON_DIR/models/"
else
    echo "[2/6] The Qwen 27B model is ~8GB on disk."
    if ask "Download $MODEL_FILE now?" Y; then
        if command -v huggingface-cli &>/dev/null; then
            huggingface-cli download "ISTA-DASLab/Qwen3.8-27B-GSQ-RCO-GGUF" "$MODEL_FILE" \
                --local-dir "$ADDON_DIR/models" --local-dir-use-symlinks False
        else
            curl -C - -L --progress-bar -o "$ADDON_DIR/models/$MODEL_FILE" "$MODEL_URL"
        fi
    else
        echo "Skipped. Place any GGUF in $ADDON_DIR/models/ later (or set LLAMACPP_MODEL)."
    fi
fi

echo "[3/6] Starting server..."
bash "$ROOT/scripts/lazy_llamacpp_serve.sh" || echo "Server not started (missing model?). Continuing with config steps."

if [[ "$NO_OPENCODE" == "1" ]]; then
    echo "[4/6] Skipped opencode patch."
else
    echo "[4/6] opencode (~/.config/opencode/opencode.json) can gain the llamacpp provider + local-model (backup .bak first)."
    if ask "Patch opencode config?" Y; then
        python3 "$ROOT/scripts/lazy_opencode_config.py" --target opencode --add-llamacpp
    fi
fi

if [[ "$NO_HERMES" == "1" ]]; then
    echo "[5/6] Skipped hermes patch."
else
    echo "[5/6] hermes (~/.hermes/config.yaml) can point its model at the local server (backup first)."
    if ask "Patch hermes config?" Y; then
        python3 "$ROOT/scripts/lazy_opencode_config.py" --target hermes --add-llamacpp
    fi
fi

if [[ "$NO_PAYLOAD" == "1" ]]; then
    echo "[6/6] Skipped payload.json change."
else
    echo "[6/6] payload.json local_llm controls fast_run panes (ollama|llamacpp|both|none)."
    if ask "Set local_llm=llamacpp in payload.json?" N; then
        python3 -c "
import json
p = '$ROOT/payload.json'
d = json.load(open(p))
d['local_llm'] = 'llamacpp'
json.dump(d, open(p, 'w'), indent=2)
print('local_llm=llamacpp')
"
    fi
fi

echo "Done. Verify: curl http://127.0.0.1:8080/health"
