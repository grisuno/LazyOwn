#!/bin/bash
# fast_run_as_r00t.sh — LazyOwn full-stack orchestrator
#
# Speed-run launcher: brings up every core service in a tmux session.
#
# Fixed panes:
#   [0] Recon        — lazynmap full scan
#   [1] Network      — addhosts + ping sweep
#   [2] C2 implant   — createcredentials + c2 launch
#   [3] Auto-loop    — autonomous loop (waits SLEEP_START)
#   [4] lazyc2       — Flask C2 server (unprivileged)
#   [5] www          — HTTP file server + certs
#   [6] VPN          — tun interface
#
# Optional panes (driven by payload.json flags):
#   DeepSeek/Ollama, Discord C2, Telegram C2, Cloudflare tunnel, NC revshell

SESSION="lazyown_sessions"
VPN=1
VENV_PATH="env"
JSON_FILE="payload.json"
NO_ATTACH=0   # set to 1 by --no-attach (MCP mode — skip tmux attach at the end)
CERTPASS="LazyOwn"

# ── Read payload.json ─────────────────────────────────────────────────────────
_jq() { jq -r ".$1" "$JSON_FILE"; }

C2_PORT=$(_jq c2_port)
DOMAIN=$(_jq domain)
C2_USER=$(_jq c2_user)
C2_PASS=$(_jq c2_pass)
SLEEP_START=$(_jq sleep_start)
OS_ID=$(_jq os_id)
ENABLE_TELEGRAM_C2=$(_jq enable_telegram_c2)
ENABLE_DISCORD_C2=$(_jq enable_discord_c2)
ENABLE_DEEPSEEK=$(_jq enable_deepseek)
ENABLE_NC=$(_jq enable_nc)
ENABLE_CF=$(_jq enable_cloudflare)
TUNNEL=""

# ── Pretty-print helpers ──────────────────────────────────────────────────────
log()    { gum log --time rfc822 --level info "    [+] $*"; }
spin()   { gum spin --spinner dot --title "$*" -- sleep 0.1; }
err_box(){ gum style \
               --foreground 212 --border-foreground 212 --border double \
               --align center --width 50 --margin "1 2" --padding "2 4" \
               "$*"; }

# ── Ensure gum is installed ───────────────────────────────────────────────────
ensure_gum() {
    command -v gum &>/dev/null && return
    sudo mkdir -p /etc/apt/keyrings
    curl -fsSL https://repo.charm.sh/apt/gpg.key \
        | sudo gpg --dearmor -o /etc/apt/keyrings/charm.gpg
    echo "deb [signed-by=/etc/apt/keyrings/charm.gpg] https://repo.charm.sh/apt/ * *" \
        | sudo tee /etc/apt/sources.list.d/charm.list
    sudo apt update && sudo apt install -y gum
}

# ── Dependency check ──────────────────────────────────────────────────────────
check_deps() {
    for dep in tmux jq go; do
        command -v "$dep" &>/dev/null && continue
        err_box "Error: $dep is required but not installed."
        exit 1
    done
}

# ── Re-exec as root if needed ─────────────────────────────────────────────────
check_sudo() {
    [[ "$EUID" -eq 0 ]] && return
    err_box "[S] This script will reload as r00t ..."
    local extra_flags=""
    [[ "$NO_ATTACH" -eq 1 ]] && extra_flags="--no-attach"
    exec sudo "$0" --vpn "$VPN" $extra_flags
}

# ── CLI argument parsing ──────────────────────────────────────────────────────
parse_args() {
    while [[ "$#" -gt 0 ]]; do
        case $1 in
            --vpn)
                [[ "$2" =~ ^[0-9]+$ ]] \
                    || { err_box "Error: --vpn must be an integer."; exit 1; }
                VPN=$2; shift ;;
            --no-attach)
                NO_ATTACH=1 ;;   # MCP/automation mode: skip blocking tmux attach
            *) err_box "Error: Unknown option: $1"; exit 1 ;;
        esac
        shift
    done
}

# ── tmux helpers ──────────────────────────────────────────────────────────────

# Send one or more commands to the active tmux pane
t_send() {
    for cmd in "$@"; do tmux send-keys -t "$SESSION" "$cmd" C-m; done
}

# Open a new pane (split v or h), start LazyOwn shell with optional run flags,
# then send any follow-up commands once the shell is up.
# Usage: t_lazyown <v|h> <delay_secs> <run_flags> [cmd1] [cmd2] ...
t_lazyown() {
    local split=$1 delay=$2 flags=$3; shift 3
    tmux split-window "-${split}"
    t_send "sleep ${delay} && bash -c './run ${flags}'"
    for cmd in "$@"; do t_send "$cmd"; done
}

# Open a new pane running a command as unprivileged user 1000 (with venv).
# Usage: t_priv_user <v|h> <command_string>
t_priv_user() {
    local split=$1; shift
    tmux split-window "-${split}"
    t_send "sleep 5 && sudo -u \#1000 bash -c 'source \"${VENV_PATH}/bin/activate\" && $*'"
}

# ── Entry point ───────────────────────────────────────────────────────────────
ensure_gum
log "Start the OPSEC."

parse_args "$@"
check_deps

spin "Host discovery..."
./modules/hostdiscover.sh 2>/dev/null &

[[ "$ENABLE_CF" == "true" ]] && TUNNEL="1"

log "Checking sudo."
check_sudo

python3 key.py
log "Start the session."

touch sessions/sessionLazyOwn.json
spin "Chmod..."
chmod 777 sessions/sessionLazyOwn.json
spin "Chown..."
chown 1000:1000 . -R

# ── Build tmux workspace ──────────────────────────────────────────────────────
tmux new-session -d -s "$SESSION"

# [0] Recon — full nmap scan
t_send "sleep 5 && bash -c './run'" "nmap"

# [1] Network — add hosts to /etc/hosts + ping sweep
t_lazyown v 5 "-c ping" "addhosts $DOMAIN"

# [opt] Local LLM inference (DeepSeek via Ollama)
[[ "$ENABLE_DEEPSEEK" == "true" ]] && \
    t_priv_user v "ollama run deepseek-r1:1.5b"

# [opt] Discord C2 bot
[[ "$ENABLE_DISCORD_C2" == "true" ]] && \
    t_priv_user v "python3 -W ignore discord_c2.py"

# [2] C2 implant — generate credentials then launch implant
t_lazyown v 5 "" "createcredentials" "$(printf 'c2 no_priv %s' "$OS_ID") $TUNNEL"

# [3] Auto-loop — waits SLEEP_START seconds so C2 server is up before starting
t_lazyown h "$SLEEP_START" "" "auto"

# [4] lazyc2 — Flask C2 server (runs as unprivileged user 1000)
tmux split-window -h
t_send "sudo -u \#1000 bash -c \"sleep 5 && /bin/bash -c \
'source \\\"${VENV_PATH}/bin/activate\\\" && \
python3 -W ignore lazyc2.py ${C2_PORT} ${C2_USER} ${C2_PASS}'\"" \
    "$CERTPASS"

# Return to pane 0 to add www + vpn side by side
tmux select-pane -t 0

# [5] HTTP file server + certs (www)
tmux split-window -h
t_send "bash -c './run'" "www" "$CERTPASS"

# [6] VPN — bring up tun interface
tmux split-window -h
t_send "bash -c './run'" "vpn $VPN"

# [opt] Netcat reverse shell listener
if [[ "$ENABLE_NC" == "true" ]]; then
    t_lazyown v 0 "" "createrevshell" "rnc"
fi

# [opt] Telegram C2 bot
[[ "$ENABLE_TELEGRAM_C2" == "true" ]] && \
    t_priv_user v "python3 -W ignore telegram_c2.py"

# [opt] Cloudflare tunnel
if [[ "$ENABLE_CF" == "true" ]]; then
    tmux split-window -v
    t_send "sleep 5 && sudo -u \#1000 bash -c './run'" "cloudflare_tunnel"
fi

tmux select-pane -t 5
log "Session ready."
if [[ "$NO_ATTACH" -eq 1 ]]; then
    log "MCP mode: tmux session '$SESSION' is running — attach manually: tmux attach -t $SESSION"
else
    log "Attaching to session..."
    tmux attach -t "$SESSION"
fi
