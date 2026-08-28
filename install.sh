#!/usr/bin/env bash
#
# LazyOwn installer.
#
# Provisions system packages (Debian/Kali via apt), a Python virtualenv with the
# pinned dependency lock, external storage and encoder modules, and self-signed
# TLS certs. The default install is intentionally light; heavy extras are
# opt-in via flags.
#
# Dependencies are declared once in pyproject.toml and pinned in
# requirements.txt / requirements-ml.txt. This script never duplicates the list.
#
# Usage:
#   bash install.sh [--with-ml] [--with-ollama] [--with-tools] [--no-ml] [--no-ollama] [--help]
#
#   --with-ml       Also install the heavy, platform-specific ML stack
#                   (torch/CUDA, sklearn ~2 GB). Skipped by default.
#   --with-ollama   Also install the local Ollama runtime. Skipped by default.
#   --with-tools    Also apt-install the common external pentest tools
#                   (gobuster, ffuf, enum4linux, seclists, responder, ...).
#   --no-ml         Accepted for backwards compatibility (ML is off by default).
#   --no-ollama     Accepted for backwards compatibility (Ollama is off by default).
#   --help          Show this help and exit.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

VENV_DIR="$SCRIPT_DIR/env"
WITH_ML=0
WITH_OLLAMA=0
WITH_TOOLS=0

usage() {
    grep '^#' "$0" | grep -v '^#!' | sed 's/^# \{0,1\}//'
}

for arg in "$@"; do
    case "$arg" in
        --with-ml) WITH_ML=1 ;;
        --with-ollama) WITH_OLLAMA=1 ;;
        --with-tools) WITH_TOOLS=1 ;;
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
        log warn "apt-get not found; skipping system packages. Install manually: golang nmap xsltproc moreutils ltrace rlwrap python3-venv gum"
        return 0
    fi
    sudo apt-get update
    sudo apt-get install -y golang rlwrap
    ensure_gum
    sudo apt-get install -y ltrace python3-xyzservices python3-venv nmap xsltproc moreutils golang rlwrap
}

install_external_tools() {
    if [[ "$WITH_TOOLS" -eq 0 ]]; then
        return 0
    fi
    if ! command -v apt-get >/dev/null 2>&1; then
        log warn "apt-get not found; skipping external tools. Run 'doctor' inside the shell to see what is missing."
        return 0
    fi
    log info "Installing common external pentest tools (--with-tools)."
    sudo apt-get install -y \
        gobuster ffuf feroxbuster enum4linux seclists responder nikto \
        hydra john hashcat smbclient exploitdb tmux \
        || log warn "Some external tools failed to install; run 'doctor' to audit them."
}

install_python_environment() {
    # Recreate venv if broken (no pip, wrong python version, etc.)
    if [[ -d "$VENV_DIR" ]]; then
        if ! "$VENV_DIR/bin/pip" --version >/dev/null 2>&1; then
            log warn "Virtualenv is broken (pip missing). Recreating..."
            rm -rf "$VENV_DIR"
        fi
    fi
    if [[ ! -d "$VENV_DIR" ]]; then
        python3 -m venv --system-site-packages "$VENV_DIR"
        log info "Created fresh virtualenv at $VENV_DIR (with --system-site-packages)"
    fi
    local pip="$VENV_DIR/bin/pip"
    "$pip" install --upgrade pip setuptools wheel
    mkdir -p "$SCRIPT_DIR/vpn" "$SCRIPT_DIR/banners" "$SCRIPT_DIR/sessions/logs"
    "$pip" install -r "$SCRIPT_DIR/requirements.txt" --resolver=backtrack || {
        log warn "Full install failed; installing core packages only..."
        "$pip" install \
            cmd2 pyyaml requests beautifulsoup4 rich tabulate psutil watchdog \
            defusedxml lupa Pillow textual flask flask-socketio flask-login \
            flask-limiter flask-sock flask-unsign markupsafe jinja2 werkzeug \
            itsdangerous click blinker pycryptodome pycryptodomex \
            impacket scapy netaddr pyotp pyopenssl paramiko bcrypt \
            lxml pyarrow pandas numpy groq netifaces \
            simplejson jsonpickle websocket-client mcp mcp-types seaborn \
            markdown yagmail dnslib validators bleach \
            && log info "Core packages installed successfully."
    }
    if [[ "$WITH_ML" -eq 1 ]]; then
        "$pip" install -r "$SCRIPT_DIR/requirements-ml.txt" || log warn "ML install failed; non-critical."
    else
        log info "Skipping machine-learning dependencies (default; use --with-ml to include)."
    fi
    "$pip" install -e "$SCRIPT_DIR" --no-deps || log warn "Editable install of the lazyown entry point failed; ./run still works."
}

install_ollama() {
    if [[ "$WITH_OLLAMA" -eq 0 ]]; then
        log info "Skipping Ollama install (default; use --with-ollama to include)."
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

install_lazyownbt() {
    local bt_dir="$SCRIPT_DIR/external/.exploit/LazyOwnBT"
    if [[ -d "$bt_dir/.git" ]]; then
        log info "LazyOwnBT present; updating."
        git -C "$bt_dir" pull --ff-only || log warn "Could not update LazyOwnBT."
    else
        log info "Cloning LazyOwnBT..."
        mkdir -p "$SCRIPT_DIR/external/.exploit"
        git clone https://github.com/grisuno/LazyOwnBT.git "$bt_dir" || {
            log warn "Could not clone LazyOwnBT; purple team features will be unavailable."
            return 0
        }
    fi
    if [[ -f "$bt_dir/requirements.txt" ]]; then
        "$VENV_DIR/bin/pip" install -r "$bt_dir/requirements.txt" --resolver=backtrack || \
            log warn "LazyOwnBT dependencies had conflicts; install manually if needed."
    fi
    log info "LazyOwnBT installed at $bt_dir"
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

seed_payload_config() {
    if [[ -f "$SCRIPT_DIR/payload.json" ]]; then
        log info "payload.json already present; keeping existing configuration."
        return 0
    fi
    if [[ -f "$SCRIPT_DIR/payload.example.json" ]]; then
        cp "$SCRIPT_DIR/payload.example.json" "$SCRIPT_DIR/payload.json"
        log info "Seeded payload.json from payload.example.json"
    else
        log warn "payload.example.json not found; the CLI will fall back to built-in defaults."
    fi
}

verify_installation() {
    "$VENV_DIR/bin/python" - <<'PYCHECK'
import importlib.util
import sys

required = ["cmd2", "flask", "rich", "scapy", "impacket", "yaml", "psutil",
            "defusedxml", "lupa", "PIL", "requests", "bs4", "tabulate",
            "markdown", "yagmail", "dnslib", "validators"]
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
    install_external_tools
    install_python_environment
    install_ollama
    install_external_storage
    install_lazyownbt
    install_encoder_module
    generate_certificates
    seed_payload_config
    verify_installation
    log info "[+] Installation complete. Next steps: ./run  then 'doctor'  then 'wizard'."
}

main "$@"
