#!/usr/bin/env bash
#
# LazyOwn installer.
#
# Provisions system packages (Debian/Kali via apt), a Python virtualenv with the
# pinned dependency lock, optional machine-learning extras, the local Ollama
# runtime, external storage and encoder modules, and self-signed TLS certs.
#
# Dependencies are declared once in pyproject.toml and pinned in
# requirements.txt / requirements-ml.txt. This script never duplicates the list.
#
# Usage:
#   bash install.sh [--no-ml] [--no-ollama] [--help]
#
#   --no-ml       Skip the heavy, platform-specific ML stack (torch/CUDA, sklearn).
#                 ML-backed features degrade gracefully when absent.
#   --no-ollama   Skip the local Ollama runtime install.
#   --help        Show this help and exit.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

VENV_DIR="$SCRIPT_DIR/env"
WITH_ML=1
WITH_OLLAMA=1

usage() {
    grep '^#' "$0" | grep -v '^#!' | sed 's/^# \{0,1\}//'
}

for arg in "$@"; do
    case "$arg" in
        --no-ml) WITH_ML=0 ;;
        --no-ollama) WITH_OLLAMA=0 ;;
        -h | --help)
            usage
            exit 0
            ;;
        *)
            echo "[!] Unknown option: $arg" >&2
            usage >&2
            exit 2
            ;;
    esac
done

log() {
    local level="$1"
    shift
    if command -v gum >/dev/null 2>&1; then
        gum log --time rfc822 --level "$level" "$*"
    else
        echo "[${level}] $*"
    fi
}

ensure_gum() {
    if command -v gum >/dev/null 2>&1; then
        return 0
    fi
    sudo mkdir -p /etc/apt/keyrings
    curl -fsSL https://repo.charm.sh/apt/gpg.key | sudo gpg --dearmor -o /etc/apt/keyrings/charm.gpg
    echo "deb [signed-by=/etc/apt/keyrings/charm.gpg] https://repo.charm.sh/apt/ * *" | sudo tee /etc/apt/sources.list.d/charm.list >/dev/null
    sudo apt-get update
    sudo apt-get install -y gum
}

install_system_packages() {
    if ! command -v apt-get >/dev/null 2>&1; then
        log warn "apt-get not found; skipping system packages. Install manually: golang nmap xsltproc moreutils ltrace python3-venv gum"
        return 0
    fi
    sudo apt-get update
    sudo apt-get install -y golang
    ensure_gum
    sudo apt-get install -y ltrace python3-xyzservices python3-venv nmap xsltproc moreutils golang
}

install_python_environment() {
    if [[ ! -d "$VENV_DIR" ]]; then
        python3 -m venv "$VENV_DIR"
    fi
    local pip="$VENV_DIR/bin/pip"
    "$pip" install --upgrade pip
    mkdir -p "$SCRIPT_DIR/vpn" "$SCRIPT_DIR/banners" "$SCRIPT_DIR/sessions/logs"
    "$pip" install -r "$SCRIPT_DIR/requirements.txt"
    if [[ "$WITH_ML" -eq 1 ]]; then
        "$pip" install -r "$SCRIPT_DIR/requirements-ml.txt"
    else
        log info "Skipping machine-learning dependencies (--no-ml)."
    fi
    "$pip" install -e "$SCRIPT_DIR" --no-deps || log warn "Editable install of the lazyown entry point failed; ./run still works."
}

install_ollama() {
    if [[ "$WITH_OLLAMA" -eq 0 ]]; then
        log info "Skipping Ollama install (--no-ollama)."
        return 0
    fi
    if command -v ollama >/dev/null 2>&1; then
        log info "Ollama already installed; skipping."
        return 0
    fi
    curl -fsSL https://ollama.com/install.sh | sh
}

install_external_storage() {
    local ext_dir="$SCRIPT_DIR/modules_ext/lazyown_infinitestorage"
    if [[ -d "$ext_dir/.git" ]]; then
        log info "LazyOwnInfiniteStorage present; updating."
        git -C "$ext_dir" pull --ff-only || log warn "Could not update LazyOwnInfiniteStorage."
    else
        git clone https://github.com/grisuno/LazyOwnInfiniteStorage.git "$ext_dir"
    fi
    if [[ -f "$ext_dir/install.sh" ]]; then
        chmod +x "$ext_dir/install.sh"
    fi
}

download_file() {
    local url="$1" dest="$2"
    if command -v curl >/dev/null 2>&1; then
        curl -fsSL -o "$dest" "$url"
    elif command -v wget >/dev/null 2>&1; then
        wget -qO "$dest" "$url"
    else
        log error "Neither curl nor wget is installed; cannot download $dest."
        return 1
    fi
}

install_encoder_module() {
    local url="https://raw.githubusercontent.com/grisuno/LazyOwnEncoderDecoder/main/lazyencoder_decoder.py"
    local dest="$SCRIPT_DIR/modules/lazyencoder_decoder.py"
    download_file "$url" "$dest"
    if [[ ! -s "$dest" ]]; then
        log error "Failed to download $dest"
        exit 1
    fi
    log info "Downloaded $dest"
}

generate_certificates() {
    bash "$SCRIPT_DIR/gen_cert.sh"
}

verify_installation() {
    "$VENV_DIR/bin/python" - <<'PYCHECK'
import importlib.util
import sys

required = ["cmd2", "flask", "rich", "scapy", "impacket"]
missing = [name for name in required if importlib.util.find_spec(name) is None]
if missing:
    print("[!] Missing core modules: " + ", ".join(missing))
    sys.exit(1)
print("[+] Core imports OK")
PYCHECK
}

main() {
    log info "[+] Starting the installation."
    install_system_packages
    install_python_environment
    install_ollama
    install_external_storage
    install_encoder_module
    generate_certificates
    verify_installation
    log info "[+] Installation complete. Next: ./run   then run 'doctor' for a health check."
}

main "$@"
