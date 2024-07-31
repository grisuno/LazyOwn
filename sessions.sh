#!/bin/bash

# Nombre de la nueva sesión de tmux
SESSION_NAME="lazyown_sessions"

# Comandos a ejecutar en cada panel
COMMAND="./run --no-banner"

# Crear una nueva sesión de tmux
tmux new-session -d -s $SESSION_NAME

# Crear los primeros dos paneles (izquierda arriba e izquierda abajo)
tmux send-keys -t $SESSION_NAME "bash -c '$COMMAND'" C-m
tmux split-window -v
tmux send-keys -t $SESSION_NAME "bash -c '$COMMAND'" C-m

# Dividir el panel izquierdo (izquierda arriba) para crear los paneles derecho arriba y derecho abajo
tmux select-pane -t 0
tmux split-window -h
tmux send-keys -t $SESSION_NAME "bash -c '$COMMAND'" C-m
tmux split-window -v
tmux send-keys -t $SESSION_NAME "bash -c '$COMMAND'" C-m

# Seleccionar el primer panel
tmux select-pane -t 0

# Adjuntar a la sesión
tmux attach -t $SESSION_NAME