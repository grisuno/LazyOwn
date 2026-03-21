#!/bin/bash
# gui_askpass.sh — SUDO_ASKPASS helper for LazyOwn MCP
#
# Used by: sudo -A <script>  (set SUDO_ASKPASS to this file's path)
#
# Tries GUI backends in order of preference.
# Outputs the password to stdout (as required by SUDO_ASKPASS protocol).
# On cancel / error: exits non-zero so sudo aborts cleanly.
#
# Backend priority:
#   1. zenity        (GTK, GNOME)
#   2. yad           (GTK, modern)
#   3. ssh-askpass   (any X11)
#   4. kdialog       (KDE/Qt)
#   5. xterm -e read (fallback — last resort X11)

set -euo pipefail

PROMPT="${SUDO_PROMPT:-[sudo] LazyOwn fast-run password: }"

# ── helpers ───────────────────────────────────────────────────────────────────
has() { command -v "$1" &>/dev/null; }

try_zenity() {
    zenity --password --title="LazyOwn sudo" --text="$PROMPT" 2>/dev/null
}

try_yad() {
    yad --title="LazyOwn sudo" --text="$PROMPT" \
        --entry --hide-text --button=OK:0 --button=Cancel:1 2>/dev/null
}

try_ssh_askpass() {
    # ssh-askpass reads SUDO_PROMPT / SSH_ASKPASS_PROMPT if set
    SSH_ASKPASS_PROMPT="confirm"
    export SSH_ASKPASS_PROMPT
    "$SSH_ASKPASS_BIN" "$PROMPT" 2>/dev/null
}

try_kdialog() {
    kdialog --title "LazyOwn sudo" --password "$PROMPT" 2>/dev/null
}

# ── main ──────────────────────────────────────────────────────────────────────
if [[ -z "${DISPLAY:-}" && -z "${WAYLAND_DISPLAY:-}" ]]; then
    echo "gui_askpass: no display available" >&2
    exit 1
fi

if has zenity; then
    try_zenity
elif has yad; then
    try_yad
elif SSH_ASKPASS_BIN="$(command -v ssh-askpass 2>/dev/null)"; then
    try_ssh_askpass
elif [[ -x "/usr/bin/ssh-askpass" ]]; then
    SSH_ASKPASS_BIN="/usr/bin/ssh-askpass"
    try_ssh_askpass
elif has kdialog; then
    try_kdialog
else
    echo "gui_askpass: no GUI password dialog found (install zenity or ssh-askpass)" >&2
    exit 1
fi
