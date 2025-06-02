#!/bin/bash

# LazyOwn Entrypoint Script
# Initializes LazyOwn framework in a Docker container with tmux sessions

set -e

# Configuration
SESSION="lazyown_sessions"
VENV_PATH="env"
JSON_FILE="/home/lazyown/payload.json"
OS_FILE="sessions/os.json"
CERTPASS="${CERTPASS:-LazyOwn}" # Default password, override via env
VPN="${VPN:-1}" # Default VPN mode

# Validate dependencies
for cmd in tmux jq; do
    if ! command -v $cmd &>/dev/null; then
        echo "Error: $cmd is required but not installed."
        exit 1
    fi
done

# Validate payload.json
if [ ! -f "$JSON_FILE" ]; then
    echo "Error: $JSON_FILE not found."
    exit 1
fi

# Read environment variables (set by dockerizer.sh)
: "${C2_PORT:?Missing C2_PORT}"
: "${RHOST:?Missing RHOST}"
: "${DOMAIN:?Missing DOMAIN}"
: "${C2_USER:?Missing C2_USER}"
: "${C2_PASS:?Missing C2_PASS}"
: "${SLEEP_START:?Missing SLEEP_START}"
: "${OS_ID:?Missing OS_ID}"
: "${ENABLE_TELEGRAM_C2:?Missing ENABLE_TELEGRAM_C2}"
: "${ENABLE_DISCORD_C2:?Missing ENABLE_DISCORD_C2}"
: "${ENABLE_DEEPSEEK:?Missing ENABLE_DEEPSEEK}"
: "${ENABLE_NC:?Missing ENABLE_NC}"
: "${ENABLE_CF:?Missing ENABLE_CF}"

# Initialize session file
SESSION_FILE="sessions/sessionLazyOwn.json"
mkdir -p sessions
touch "$SESSION_FILE"
chmod 600 "$SESSION_FILE"

# Start tmux session
tmux new-session -d -s "$SESSION"

# Panel 1: Main C2
tmux send-keys -t "$SESSION" "sleep 5 && ./run -c 'c2 no_priv $OS_ID' ${ENABLE_CF:+1}" C-m

# Panel 2: Network discovery
tmux split-window -v
tmux send-keys -t "$SESSION" "sleep 5 && ./modules/hostdiscover.sh" C-m

# Panel 3: Ping check
tmux split-window -v
tmux send-keys -t "$SESSION" "sleep 5 && ./run -c ping" C-m
tmux send-keys -t "$SESSION" "addhosts $DOMAIN" C-m

# Panel 4: DeepSeek (if enabled)
if [ "$ENABLE_DEEPSEEK" = "true" ]; then
    tmux split-window -v
    tmux send-keys -t "$SESSION" "sleep 5 && source '$VENV_PATH/bin/activate' && ollama run deepseek-r1:1.5b" C-m
fi

# Panel 5: Discord C2 (if enabled)
if [ "$ENABLE_DISCORD_C2" = "true" ]; then
    tmux split-window -v
    tmux send-keys -t "$SESSION" "sleep 5 && source '$VENV_PATH/bin/activate' && python3 -W ignore discord_c2.py" C-m
fi

# Panel 6: Credentials
tmux split-window -v
tmux send-keys -t "$SESSION" "sleep 5 && ./run" C-m
tmux send-keys -t "$SESSION" "createcredentials" C-m

# Panel 7: Auto mode
tmux split-window -h
tmux send-keys -t "$SESSION" "sleep $SLEEP_START && ./run" C-m
tmux send-keys -t "$SESSION" "auto" C-m

# Panel 8: LazyC2
tmux split-window -h
tmux send-keys -t "$SESSION" "sleep 5 && source '$VENV_PATH/bin/activate' && python3 -W ignore lazyc2.py $C2_PORT $C2_USER $C2_PASS" C-m
tmux send-keys -t "$SESSION" "$CERTPASS" C-m

# Panel 9: Web interface
tmux select-pane -t 0
tmux split-window -h
tmux send-keys -t "$SESSION" "./run" C-m
tmux send-keys -t "$SESSION" "www" C-m
tmux send-keys -t "$SESSION" "$CERTPASS" C-m

# Panel 10: VPN
tmux split-window -h
tmux send-keys -t "$SESSION" "./run" C-m
tmux send-keys -t "$SESSION" "vpn $VPN" C-m

# Panel 11: Netcat reverse shell (if enabled)
if [ "$ENABLE_NC" = "true" ]; then
    tmux split-window -v
    tmux send-keys -t "$SESSION" "./run" C-m
    tmux send-keys -t "$SESSION" "createrevshell" C-m
    tmux send-keys -t "$SESSION" "rnc" C-m
fi

# Panel 12: Telegram C2 (if enabled)
if [ "$ENABLE_TELEGRAM_C2" = "true" ]; then
    tmux split-window -v
    tmux send-keys -t "$SESSION" "sleep 5 && source '$VENV_PATH/bin/activate' && python3 -W ignore telegram_c2.py" C-m
fi

# Panel 13: Cloudflare tunnel (if enabled)
if [ "$ENABLE_CF" = "true" ]; then
    tmux split-window -v
    tmux send-keys -t "$SESSION" "sleep 5 && ./run" C-m
    tmux send-keys -t "$SESSION" "cloudflare_tunnel" C-m
fi

# Attach to tmux session
tmux select-pane -t 5
tmux attach -t "$SESSION"