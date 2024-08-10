#!/bin/bash

# Nombre de la nueva sesión de tmux
SESSION="lazyown_sessions"
COMMAND='./run --no-banner'
# Función para verificar y relanzar con sudo si es necesario
check_sudo() {
    if [ "$EUID" -ne 0 ]; then
        echo "[S] Este script necesita permisos de superusuario. Relanzando con sudo..."
        sudo bash "$0" "$@"
        exit
    fi
}

check_sudo

# Crear una nueva sesión de tmux
tmux new-session -d -s $SESSION

# Crear los primeros dos paneles (izquierda arriba e izquierda abajo)
tmux send-keys -t $SESSION "sleep 5 && bash -c './run -c nmap'" C-m
tmux split-window -v
tmux send-keys -t $SESSION "sleep 5 && bash -c '$COMMAND'" C-m
tmux split-window -v
tmux send-keys -t $SESSION "sleep 60 && bash -c './run -c pyautomate'" C-m
# Dividir el panel izquierdo (izquierda arriba) para crear los paneles derecho arriba y derecho abajo
tmux select-pane -t 0
tmux split-window -h

# Agregar un delay para que la VPN tenga tiempo de conectarse

tmux send-keys -t $SESSION "bash -c './run -c \"vpn 1\"'" C-m
tmux split-window -v

tmux send-keys -t $SESSION "bash -c './run -c www'" C-m
# Seleccionar el primer panel
tmux select-pane -t 3

# Adjuntar a la sesión
tmux attach -t $SESSION