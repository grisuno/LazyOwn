#!/bin/bash

SESSION="lazyown_sessions"
COMMAND='./run --no-banner'


tmux new-session -d -s $SESSION
tmux send-keys -t $SESSION "bash -c '$COMMAND'" C-m
tmux split-window -v
tmux send-keys -t $SESSION "bash -c '$COMMAND'" C-m
tmux select-pane -t 1
tmux attach -t $SESSION

