#!/bin/bash

SESSION="lazyown_sessions"
COMMAND='./run --no-banner'
VPN=1  
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
echo $VPN
check_sudo "$@"
echo $VPN
tmux new-session -d -s $SESSION
tmux send-keys -t $SESSION "sleep 5 && bash -c './run -c nmap'" C-m
tmux split-window -v
tmux send-keys -t $SESSION "sleep 5 && bash -c '$COMMAND'" C-m
tmux split-window -v
tmux send-keys -t $SESSION "sleep 60 && bash -c './run -c pyautomate'" C-m
tmux select-pane -t 0
tmux split-window -h
tmux send-keys -t $SESSION "bash -c './run -c \"vpn $VPN\"'" C-m
tmux split-window -v
tmux send-keys -t $SESSION "bash -c './run -c www'" C-m
tmux select-pane -t 3
tmux attach -t $SESSION
