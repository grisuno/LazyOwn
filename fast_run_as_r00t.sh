#!/bin/bash

SESSION="lazyown_sessions"
COMMAND='./run -c "c2 no_priv"'
VPN=1
VENV_PATH="env"
JSON_FILE="payload.json"
OS_FILE="sessions/os.json"
C2_PORT=$(jq -r '.c2_port' "$JSON_FILE")
RHOST=$(jq -r '.rhost' "$JSON_FILE")
DOMAIN=$(jq -r '.domain' "$JSON_FILE")
C2_USER=$(jq -r '.c2_user' "$JSON_FILE")
C2_PASS=$(jq -r '.c2_pass' "$JSON_FILE")
SLEEP_START=$(jq -r '.sleep_start' "$JSON_FILE")
OS_ID=$(jq -r '.os_id' "$JSON_FILE")
ENABLE_TELEGRAM_C2=$(jq -r '.enable_telegram_c2' "$JSON_FILE")
CERTPASS="LazyOwn"
CURRENT=$PWD
check_sudo() {
    if [ "$EUID" -ne 0 ]; then
        echo "[S] This script will reload as r00t ..."
        sudo "$0" --vpn "$VPN" "${@/#--vpn*/}"
        exit
    fi
}
while [[ "$#" -gt 0 ]]; do
    case $1 in
        --vpn)
            if [[ "$2" =~ ^[0-9]+$ ]]; then
                VPN=$2
                shift
            else
                echo "Error: the value --vpn must be int nummber."
                exit 1
            fi
            ;;
        *)
            echo "Error: Not recon option $1"
            exit 1
            ;;
    esac
    shift
done

check_sudo "$@"


chown 1000:1000 sessions -R
chmod 777 sessions/temp_uploads -R
chmod 777 sessions/uploads -R
tmux new-session -d -s $SESSION
tmux send-keys -t $SESSION "sleep 5 && bash -c './run'" C-m
tmux send-keys -t $SESSION "nmap" C-m
tmux split-window -v
tmux send-keys -t $SESSION "sleep 5 && bash -c './run -c ping'" C-m
tmux send-keys -t $SESSION "addhosts $DOMAIN" C-m
tmux split-window -v
tmux send-keys -t $SESSION "sleep 5 && bash -c './run'" C-m
tmux send-keys -t $SESSION "createcredentials" C-m
tmux send-keys -t $SESSION "$(printf 'c2 no_priv %s' $OS_ID)" C-m
tmux split-window -h
tmux send-keys -t $SESSION "sleep $SLEEP_START && bash -c './run'" C-m
tmux send-keys -t $SESSION "auto" C-m
tmux split-window -h
tmux send-keys -t $SESSION "sudo -u \#1000 bash -c \"sleep 0.05 && /bin/bash -c 'source \"$VENV_PATH/bin/activate\" && python3 -W ignore lazyc2.py $C2_PORT $C2_USER $C2_PASS'\"" C-m
tmux send-keys -t $SESSION "$CERTPASS" C-m
tmux select-pane -t 0
tmux split-window -h
tmux send-keys -t $SESSION "bash -c './run'" C-m
tmux send-keys -t $SESSION "www" C-m
tmux send-keys -t $SESSION "$CERTPASS" C-m
tmux split-window -h
tmux send-keys -t $SESSION "bash -c './run'" C-m
tmux send-keys -t $SESSION "vpn $VPN" C-m
tmux split-window -v
tmux send-keys -t $SESSION "bash -c './run'" C-m
tmux send-keys -t $SESSION "createrevshell" C-m
tmux send-keys -t $SESSION "rnc" C-m
if [ "$ENABLE_TELEGRAM_C2"  == true ]; then
    tmux split-window -v
    tmux send-keys -t $SESSION "sleep 5 && sudo -u \#1000 bash -c  'source \"$VENV_PATH/bin/activate\" && python3 -W ignore tel.py'" C-m
fi
tmux select-pane -t 5
tmux attach -t $SESSION
