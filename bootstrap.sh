#!/usr/bin/env bash
#
# LazyOwn bootstrap installer (one-liner entry point).
#
# Clones the repository into a target directory (default: $HOME/LazyOwn),
# runs install.sh, then asks whether to launch a normal session (./run)
# or the full stack as root (fast_run_as_r00t.sh).
#
# One-liner (download first, then run — immune to pipe stalls and CDN cache):
#   curl -fsSL https://raw.githubusercontent.com/grisuno/LazyOwn/main/bootstrap.sh -o /tmp/bootstrap.sh \
#     && bash /tmp/bootstrap.sh
#
# Pipe alternative (same result, single command):
#   curl -fsSL https://raw.githubusercontent.com/grisuno/LazyOwn/main/bootstrap.sh | bash
#
# With options (append after the script path, or use bash -s through the pipe):
#   bash /tmp/bootstrap.sh -- --with-tools --dir ~/pentest/LazyOwn
#   curl -fsSL https://raw.githubusercontent.com/grisuno/LazyOwn/main/bootstrap.sh | bash -s -- --with-tools --dir ~/pentest/LazyOwn
#
# If the target directory already holds a LazyOwn checkout, the installer
# asks what to do: update in place (git pull + reinstall), clean install
# (delete everything and clone fresh), install into a different directory,
# or abort. Set --existing to skip the question in scripts.
#
# Options:
#   --dir <path>     Install directory (default: $HOME/LazyOwn, or $LAZYOWN_DIR).
#   --branch <name>  Git branch to clone (default: main, or $LAZYOWN_BRANCH).
#   --with-ml        Also install the heavy ML stack (forwarded to install.sh).
#   --with-ollama    Also install the Ollama runtime (forwarded to install.sh).
#   --with-tools     Also apt-install common external pentest tools.
#   --profile <name> Install profile, forwarded to install.sh: full (default)
#                    or light (shell + C2 + recon core, no analytics/AI stack).
#   --existing <m>   Existing-checkout policy without prompting:
#                    update | clean | abort (default: ask interactively).
#   --run-mode <m>   Launch mode without prompting: normal | fast | none.
#   --no-run         Do not launch anything after install (same as --run-mode none).
#   -y, --yes        Non-interactive: assume defaults, skip every prompt.
#   --debug          Print every executed command (diagnostics for stuck runs).
#   -h, --help       Show this help and exit.
#
# Environment overrides: LAZYOWN_DIR, LAZYOWN_BRANCH, LAZYOWN_REPO, LAZYOWN_BACKUP_DIR, NO_COLOR.

set -euo pipefail

LAZYOWN_REPO="${LAZYOWN_REPO:-https://github.com/grisuno/LazyOwn.git}"
LAZYOWN_DIR="${LAZYOWN_DIR:-$HOME/LazyOwn}"
LAZYOWN_BRANCH="${LAZYOWN_BRANCH:-main}"
EXISTING_MODE="ask"
RUN_MODE="ask"
ASSUME_YES=0
DEBUG=0
INSTALL_ARGS=()

if [[ -z "${NO_COLOR:-}" && "${TERM:-dumb}" != "dumb" ]]; then
    C_RESET='\033[0m'
    C_BOLD='\033[1m'
    C_RED='\033[31m'
    C_GREEN='\033[32m'
    C_YELLOW='\033[33m'
    C_CYAN='\033[36m'
else
    C_RESET=''
    C_BOLD=''
    C_RED=''
    C_GREEN=''
    C_YELLOW=''
    C_CYAN=''
fi

usage() {
    grep '^#' "$0" | grep -v '^#!' | sed 's/^# \{0,1\}//'
}

log() {
    local level="$1"
    shift
    local text="$*"
    local prefix
    case "$level" in
        INFO) prefix="${C_CYAN}[*]${C_RESET}" ;;
        OK) prefix="${C_GREEN}[+]${C_RESET}" ;;
        WARN) prefix="${C_YELLOW}[!]${C_RESET}" ;;
        ERROR) prefix="${C_RED}[ERROR]${C_RESET}" ;;
    esac
    if [[ "$level" == "WARN" || "$level" == "ERROR" ]]; then
        printf '%b %s\n' "$prefix" "$text" >&2
    else
        printf '%b %s\n' "$prefix" "$text"
    fi
}

fail() {
    log ERROR "$1" >&2
    exit 1
}

spin_run() {
    local message="$1"
    shift
    local log_file
    log_file="$(mktemp /tmp/lazyown-bootstrap-XXXXXX.log)"
    log INFO "$message"
    log INFO "Detail log: $log_file (run 'tail -f $log_file' in another terminal to watch progress)"
    "$@" >"$log_file" 2>&1 &
    local pid=$!
    if [[ -t 1 ]]; then
        local frames="|/-\\"
        local i=0
        while kill -0 "$pid" 2>/dev/null; do
            printf '\r%b working %s' "${C_CYAN}[*]${C_RESET}" "${frames:$i:1}"
            i=$(( (i + 1) % 4 ))
            sleep 0.25
        done
        printf '\r%60s\r' ""
    fi
    local rc=0
    wait "$pid" || rc=$?
    if [[ "$rc" -eq 0 ]]; then
        log OK "$message finished."
    else
        log ERROR "$message failed (exit $rc). Last output:"
        tail -n 25 "$log_file" >&2
    fi
    return "$rc"
}

while [[ "$#" -gt 0 ]]; do
    case "$1" in
        --dir)
            [[ "$#" -ge 2 ]] || fail "--dir requires a path argument."
            LAZYOWN_DIR="$2"
            shift 2
            ;;
        --dir=*)
            LAZYOWN_DIR="${1#--dir=}"
            shift
            ;;
        --branch)
            [[ "$#" -ge 2 ]] || fail "--branch requires a name argument."
            LAZYOWN_BRANCH="$2"
            shift 2
            ;;
        --branch=*)
            LAZYOWN_BRANCH="${1#--branch=}"
            shift
            ;;
        --with-ml | --with-ollama | --with-tools)
            INSTALL_ARGS+=("$1")
            shift
            ;;
        --profile)
            [[ "$#" -ge 2 ]] || fail "--profile requires one of: light, full."
            INSTALL_ARGS+=("--profile" "$2")
            shift 2
            ;;
        --profile=*)
            INSTALL_ARGS+=("$1")
            shift
            ;;
        --existing)
            [[ "$#" -ge 2 ]] || fail "--existing requires one of: update, clean, abort."
            EXISTING_MODE="$2"
            shift 2
            ;;
        --existing=*)
            EXISTING_MODE="${1#--existing=}"
            shift
            ;;
        --run-mode)
            [[ "$#" -ge 2 ]] || fail "--run-mode requires one of: normal, fast, none."
            RUN_MODE="$2"
            shift 2
            ;;
        --run-mode=*)
            RUN_MODE="${1#--run-mode=}"
            shift
            ;;
        --no-run)
            RUN_MODE="none"
            shift
            ;;
        -y | --yes)
            ASSUME_YES=1
            shift
            ;;
        --)
            shift
            break
            ;;
        --debug)
            DEBUG=1
            shift
            ;;
        -h | --help)
            usage
            exit 0
            ;;
        *)
            fail "Unknown option: $1 (see --help)."
            ;;
    esac
done

case "$EXISTING_MODE" in
    ask | update | clean | abort) ;;
    *) fail "--existing must be one of: update, clean, abort." ;;
esac

case "$RUN_MODE" in
    ask | normal | fast | none) ;;
    *) fail "--run-mode must be one of: normal, fast, none." ;;
esac

  # Expand a leading ~ in --dir without relying on eval.
  expand_tilde() {
    local path="$1"
    if [[ "$path" == "~"* ]]; then
        printf '%s' "$HOME${path:1}"
    else
        printf '%s' "$path"
    fi
}

LAZYOWN_DIR="$(expand_tilde "$LAZYOWN_DIR")"

if [[ "$DEBUG" -eq 1 ]]; then
    log INFO "Debug mode on: printing every command."
    set -x
fi

command -v git >/dev/null 2>&1 || fail "git is required. Install it first (Debian/Kali: sudo apt-get install -y git) and retry."
command -v python3 >/dev/null 2>&1 || fail "python3 is required. Install it first (sudo apt-get install -y python3) and retry."
command -v curl >/dev/null 2>&1 || command -v wget >/dev/null 2>&1 || fail "curl or wget is required. Install one and retry."

log INFO "LazyOwn bootstrap installer working."
log INFO "Install target: $LAZYOWN_DIR (branch $LAZYOWN_BRANCH)."
log INFO "A fresh install takes several minutes. You may be asked for your sudo password."

can_prompt() {
    [[ "$ASSUME_YES" -eq 0 ]] || return 1
    if command -v timeout >/dev/null 2>&1; then
        timeout 10 bash -c ': < /dev/tty' >/dev/null 2>&1
    else
        { : < /dev/tty; } >/dev/null 2>&1
    fi
}

ASK_ANSWER=""

ask() {
    printf '%b' "$1"
    if { : < /dev/tty; } >/dev/null 2>&1; then
        read -t 120 -r ASK_ANSWER < /dev/tty || ASK_ANSWER=""
    else
        read -r ASK_ANSWER || ASK_ANSWER=""
    fi
}

update_checkout() {
    log INFO "Updating existing checkout at $LAZYOWN_DIR (branch $LAZYOWN_BRANCH)."
    spin_run "Fetching updates from origin" git -C "$LAZYOWN_DIR" fetch origin "$LAZYOWN_BRANCH" \
        || fail "Could not fetch from origin."
    git -C "$LAZYOWN_DIR" checkout "$LAZYOWN_BRANCH" || fail "Could not check out $LAZYOWN_BRANCH."
    spin_run "Fast-forwarding checkout" git -C "$LAZYOWN_DIR" pull --ff-only origin "$LAZYOWN_BRANCH" \
        || log WARN "Could not fast-forward; keeping local state."
}

backup_payload() {
    if [[ -f "$LAZYOWN_DIR/payload.json" ]]; then
        local backup_dir="${LAZYOWN_BACKUP_DIR:-/tmp}"
        local backup="$backup_dir/lazyown-payload-backup-$(date +%Y%m%d-%H%M%S).json"
        if cp "$LAZYOWN_DIR/payload.json" "$backup" 2>/dev/null; then
            log OK "Backed up payload.json to $backup"
        else
            log WARN "Could not back up payload.json; continuing anyway."
        fi
    fi
}

clone_fresh() {
    spin_run "Cloning LazyOwn ($LAZYOWN_BRANCH) into $LAZYOWN_DIR" \
        git clone --branch "$LAZYOWN_BRANCH" --depth 1 "$LAZYOWN_REPO" "$LAZYOWN_DIR" \
        || fail "Clone failed. Check the URL and your network connection."
}

clean_checkout() {
    backup_payload
    log WARN "Removing everything in $LAZYOWN_DIR"
    rm -rf "$LAZYOWN_DIR"
    clone_fresh
}

confirm_clean() {
    local answer=""
    printf "${C_RED}${C_BOLD}WARNING:${C_RESET}${C_RED} this will permanently delete everything in\n"
    printf "  %s\n" "$LAZYOWN_DIR"
    printf "including payload.json and sessions/.${C_RESET}\n"
    ask "Type DELETE to confirm, or anything else to go back: "
    answer="$ASK_ANSWER"
    [[ "$answer" == "DELETE" ]]
}

ask_new_dir() {
    local suggestion="${LAZYOWN_DIR}-new"
    local answer=""
    ask "Enter installation directory (default: ${C_BOLD}$suggestion${C_RESET}, empty aborts): "
    answer="$ASK_ANSWER"
    if [[ -z "$answer" ]]; then
        return 1
    fi
    LAZYOWN_DIR="$(expand_tilde "$answer")"
    return 0
}

ask_existing_checkout_action() {
    local answer=""
    printf "\n${C_BOLD}${C_CYAN}Existing installation detected at $LAZYOWN_DIR (branch $LAZYOWN_BRANCH).${C_RESET}\n"
    echo "How do you want to proceed?"
    echo "  [1] Update in place (git pull + reinstall over it)"
    echo "  [2] Clean install (delete everything and clone fresh)"
    echo "  [3] Install into a different directory"
    echo "  [4] Abort installation"
    while true; do
        ask "Select [1/2/3/4] (default 1): "
        answer="${ASK_ANSWER:-1}"
        case "$answer" in
            1 | update) echo "update"; return 0 ;;
            2 | clean) echo "clean"; return 0 ;;
            3 | newdir) echo "newdir"; return 0 ;;
            4 | abort) echo "abort"; return 0 ;;
            *) echo "Please answer 1, 2, 3 or 4." ;;
        esac
    done
}

ask_existing_path_action() {
    local answer=""
    printf "\n${C_BOLD}${C_YELLOW}Path $LAZYOWN_DIR exists and is not a LazyOwn checkout.${C_RESET}\n"
    echo "How do you want to proceed?"
    echo "  [1] Install into a different directory (default)"
    echo "  [2] Delete it and install here (requires confirmation)"
    echo "  [3] Abort installation"
    while true; do
        ask "Select [1/2/3] (default 1): "
        answer="${ASK_ANSWER:-1}"
        case "$answer" in
            1 | newdir) echo "newdir"; return 0 ;;
            2 | delete) echo "delete"; return 0 ;;
            3 | abort) echo "abort"; return 0 ;;
            *) echo "Please answer 1, 2 or 3." ;;
        esac
    done
}

resolve_target_dir() {
    log INFO "Checking for an existing install at $LAZYOWN_DIR ..."
    while true; do
        if [[ -d "$LAZYOWN_DIR/.git" ]]; then
            log INFO "Found an existing LazyOwn checkout."
            local action="$EXISTING_MODE"
            if [[ "$action" == "ask" ]]; then
                if can_prompt; then
                    action="$(ask_existing_checkout_action)"
                else
                    log WARN "Existing checkout at $LAZYOWN_DIR; non-interactive session, updating in place."
                    action="update"
                fi
            fi
            case "$action" in
                update)
                    update_checkout
                    return 0
                    ;;
                clean)
                    if [[ "$EXISTING_MODE" == "clean" ]] || confirm_clean; then
                        clean_checkout
                        return 0
                    fi
                    ;;
                newdir)
                    if [[ "$EXISTING_MODE" == "ask" ]] && can_prompt; then
                        ask_new_dir || { log INFO "Aborted by user."; exit 0; }
                    else
                        fail "Cannot ask for a new directory in non-interactive mode; pass --dir <path>."
                    fi
                    ;;
                abort)
                    log INFO "Aborted by user. Nothing was changed."
                    exit 0
                    ;;
            esac
        elif [[ -e "$LAZYOWN_DIR" ]]; then
            log INFO "Path exists but is not a LazyOwn checkout."
            local action="abort"
            if can_prompt; then
                action="$(ask_existing_path_action)"
            else
                fail "$LAZYOWN_DIR exists and is not a git checkout. Remove it or pick another directory with --dir."
            fi
            case "$action" in
                newdir)
                    ask_new_dir || { log INFO "Aborted by user."; exit 0; }
                    ;;
                delete)
                    if confirm_clean; then
                        rm -rf "$LAZYOWN_DIR"
                        clone_fresh
                        return 0
                    fi
                    ;;
                abort)
                    log INFO "Aborted by user. Nothing was changed."
                    exit 0
                    ;;
            esac
        else
            log INFO "No existing install found. Doing a fresh clone."
            clone_fresh
            return 0
        fi
    done
}

resolve_target_dir

cd "$LAZYOWN_DIR"
chmod +x bootstrap.sh install.sh run fast_run_as_r00t.sh 2>/dev/null || true

log INFO "Running install.sh ${INSTALL_ARGS[*]:-"(defaults)"}."
bash install.sh "${INSTALL_ARGS[@]}"

ask_launch_mode() {
    local answer=""
    echo ""
    printf "${C_BOLD}${C_CYAN}Installation finished. How do you want to start LazyOwn?${C_RESET}\n"
    echo "  [1] Normal session (./run)"
    echo "  [2] Full stack as root (fast_run_as_r00t.sh: C2, VPN, tmux services)"
    echo "  [3] Exit without starting"
    while true; do
        ask "Select [1/2/3] (default 1): "
        answer="${ASK_ANSWER:-1}"
        case "$answer" in
            1 | normal | run) echo "normal"; return 0 ;;
            2 | fast | root) echo "fast"; return 0 ;;
            3 | none | exit | quit | n) echo "none"; return 0 ;;
            *) echo "Please answer 1, 2 or 3." ;;
        esac
    done
}

if [[ "$RUN_MODE" == "ask" && "$ASSUME_YES" -eq 1 ]]; then
    RUN_MODE="none"
fi

if [[ "$RUN_MODE" == "ask" ]]; then
    if can_prompt; then
        RUN_MODE="$(ask_launch_mode)"
    else
        log INFO "Non-interactive session detected; skipping launch prompt. Start later with ./run."
        RUN_MODE="none"
    fi
fi

case "$RUN_MODE" in
    normal)
        log OK "Starting normal session (./run). Press Ctrl-D or type exit to quit."
        exec ./run
        ;;
    fast)
        log OK "Starting full stack (fast_run_as_r00t.sh). It re-executes with sudo when needed."
        exec bash fast_run_as_r00t.sh
        ;;
    none)
        log OK "Done. Next steps: cd $LAZYOWN_DIR && ./run  (full stack: sudo ./fast_run_as_r00t.sh)."
        ;;
esac
