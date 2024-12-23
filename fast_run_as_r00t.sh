#!/bin/bash

SESSION="lazyown_sessions"
COMMAND='./run -c "c2 no_priv"'
VPN=1
VENV_PATH="env"


check_sudo() {
    if [ "$EUID" -ne 0 ]; then
        echo "[S] Este script necesita permisos de superusuario. Relanzando con sudo..."
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
                echo "Error: El valor para --vpn debe ser un número."
                exit 1
            fi
            ;;
        *)
            echo "Error: Opción no reconocida $1"
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
tmux send-keys -t $SESSION "sleep 5 && bash -c './run -c nmap'" C-m
tmux split-window -v
tmux send-keys -t $SESSION "sleep 5 && bash -c './run -c ping'" C-m
tmux send-keys -t $SESSION "c2 no_priv" C-m
tmux split-window -v
tmux send-keys -t $SESSION "sleep 99 && bash -c './run -c pyautomate'" C-m
tmux split-window -h
tmux send-keys -t $SESSION "sleep 0.05 && bash -c 'source \"$VENV_PATH/bin/activate\" && python3 -W ignore lazyc2.py 4444 LazyOwn LazyOwn'" C-m
tmux select-pane -t 0
tmux split-window -h
tmux send-keys -t $SESSION "bash -c './run -c \"vpn $VPN\"'" C-m
tmux split-window -v
tmux send-keys -t $SESSION "bash -c './run -c www'" C-m
tmux select-pane -t 3
tmux attach -t $SESSION
