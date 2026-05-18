#!/usr/bin/env bash
##
## fast_run_service.sh
##
## LazyOwn service-mode orchestrator. Boots the framework's long-running
## components (C2 server, HTTP file server, VPN tunnel, optional bots and
## tunnels) as detached background processes for MCP and single-instance
## deployments where no operator tmux session is available.
##
## Lifecycle: start | stop | restart | status | logs <name> | chown-now.
##
## Differs from fast_run_as_r00t.sh in that it does not allocate tmux panes,
## does not invoke interactive workflow commands (lazynmap / auto-loop /
## createcredentials), and is safe to run from systemd, OpenRC, supervisord,
## or a Claude MCP server.
##

set -Eeuo pipefail

##
## Config block. Every tunable value lives here; nothing is hardcoded below.
##
readonly SCRIPT_NAME="$(basename "$0")"
readonly SCRIPT_DIR="$(cd "$(dirname "$(readlink -f "$0")")" && pwd)"
readonly PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
readonly JSON_FILE="${PROJECT_ROOT}/payload.json"
readonly VENV_PATH="${PROJECT_ROOT}/env"
readonly SESSIONS_DIR="${PROJECT_ROOT}/sessions"
readonly RUN_DIR="${SESSIONS_DIR}/service/run"
readonly LOG_DIR="${SESSIONS_DIR}/service/log"

readonly TARGET_UID=1000
readonly TARGET_GID=1000
readonly CHOWN_INTERVAL_SECONDS=30
readonly STARTUP_DELAY_SECONDS=2
readonly SHUTDOWN_GRACE_SECONDS=15
readonly STATUS_POLL_INTERVAL_SECONDS=1
readonly CERT_PASSPHRASE="LazyOwn"

readonly OLLAMA_MODEL="deepseek-r1:1.5b"

readonly SVC_CHOWN="chown_watcher"
readonly SVC_C2="lazyc2"
readonly SVC_WWW="www"
readonly SVC_VPN="vpn"
readonly SVC_DISCORD="discord_c2"
readonly SVC_TELEGRAM="telegram_c2"
readonly SVC_CLOUDFLARE="cloudflare_tunnel"
readonly SVC_OLLAMA="ollama_deepseek"

readonly DIR_MODE="0755"
readonly LOG_MODE="0644"
readonly PID_MODE="0644"

readonly STATE_RUNNING="running"
readonly STATE_STOPPED="stopped"
readonly STATE_STALE="stale"

readonly EXIT_OK=0
readonly EXIT_USAGE=64
readonly EXIT_MISCONFIG=78
readonly EXIT_PERMISSION=77
readonly EXIT_RUNTIME=70

##
## Logging primitives. Single-responsibility wrappers around printf so all
## log lines share a uniform ISO-8601 timestamp prefix.
##
log_timestamp() {
    date '+%Y-%m-%dT%H:%M:%S%z'
}

log_info() {
    printf '[%s] [INFO]  %s\n' "$(log_timestamp)" "$*"
}

log_warn() {
    printf '[%s] [WARN]  %s\n' "$(log_timestamp)" "$*" >&2
}

log_error() {
    printf '[%s] [ERROR] %s\n' "$(log_timestamp)" "$*" >&2
}

##
## Pre-flight checks. Each function performs one verification and returns
## non-zero on failure so the caller can decide how to surface it.
##
require_root() {
    ## Re-execute the script under sudo if invoked as a non-root user.
    ## Preserves the original argv via "$@" so subcommand routing is intact.
    if [[ $EUID -ne 0 ]]; then
        exec sudo -E "$0" "$@"
    fi
}

require_deps() {
    ## Verify the external binaries the orchestrator depends on.
    local deps=("jq" "python3" "sudo" "kill" "ps" "install" "tail")
    local missing=()
    local dep
    for dep in "${deps[@]}"; do
        if ! command -v "$dep" >/dev/null 2>&1; then
            missing+=("$dep")
        fi
    done
    if [[ ${#missing[@]} -gt 0 ]]; then
        log_error "Missing required binaries: ${missing[*]}"
        return "$EXIT_MISCONFIG"
    fi
}

require_paths() {
    ## Ensure the project payload and virtualenv exist before any service
    ## tries to load them. Failure here is a hard misconfiguration.
    if [[ ! -f "$JSON_FILE" ]]; then
        log_error "payload.json not found at ${JSON_FILE}"
        return "$EXIT_MISCONFIG"
    fi
    if [[ ! -d "$VENV_PATH" ]]; then
        log_error "Virtualenv not found at ${VENV_PATH}"
        return "$EXIT_MISCONFIG"
    fi
}

prepare_runtime_dirs() {
    ## Create the run/log directories owned by the operator user so the
    ## unprivileged child processes can write into them without escalation.
    install -d -m "$DIR_MODE" -o "$TARGET_UID" -g "$TARGET_GID" "$RUN_DIR"
    install -d -m "$DIR_MODE" -o "$TARGET_UID" -g "$TARGET_GID" "$LOG_DIR"
}

##
## Config loader. Reads payload.json once into a typed associative array so
## subsequent service starts work from a consistent snapshot.
##
declare -A CONFIG

load_config() {
    ## Populate CONFIG[] from payload.json. Missing keys become empty
    ## strings; consumers must validate the keys they actually need.
    local keys=(
        c2_port c2_user c2_pass
        domain sleep_start os_id
        enable_telegram_c2 enable_discord_c2 enable_deepseek
        enable_cloudflare enable_service_vpn
        service_vpn_index lhost
    )
    local key
    for key in "${keys[@]}"; do
        CONFIG[$key]="$(jq -r --arg k "$key" '.[$k] // empty' "$JSON_FILE")"
    done
}

config_truthy() {
    ## Return 0 if the named CONFIG entry equals 'true' (JSON boolean) or
    ## the case-insensitive string 'true'. Used for optional service gates.
    local value="${CONFIG[$1]:-}"
    [[ "${value,,}" == "true" ]]
}

##
## PID-file primitives. Encapsulate the per-service filesystem contract so
## lifecycle commands never touch paths directly.
##
pid_file_for() {
    ## Echo the canonical PID file path for a named service.
    printf '%s/%s.pid' "$RUN_DIR" "$1"
}

log_file_for() {
    ## Echo the canonical log file path for a named service.
    printf '%s/%s.log' "$LOG_DIR" "$1"
}

read_pid_value() {
    ## Echo the integer PID stored on disk for the named service, or empty.
    local pid_file
    pid_file="$(pid_file_for "$1")"
    if [[ -f "$pid_file" ]]; then
        local pid
        pid="$(<"$pid_file")"
        if [[ "$pid" =~ ^[0-9]+$ ]]; then
            printf '%s' "$pid"
        fi
    fi
}

is_pid_alive() {
    ## Return 0 if the given PID corresponds to a live process.
    [[ -n "${1:-}" ]] && kill -0 "$1" 2>/dev/null
}

is_service_running() {
    ## Return 0 if the named service has a recorded, live PID.
    local pid
    pid="$(read_pid_value "$1")"
    is_pid_alive "$pid"
}

write_pid_file() {
    ## Persist a PID to the named service's PID file with operator ownership.
    local name="$1" pid="$2"
    local pid_file
    pid_file="$(pid_file_for "$name")"
    printf '%s\n' "$pid" >"$pid_file"
    chown "${TARGET_UID}:${TARGET_GID}" "$pid_file"
    chmod "$PID_MODE" "$pid_file"
}

ensure_log_file() {
    ## Create the log file (truncated) with operator ownership before a
    ## service spawn so the child can append without privilege escalation.
    local name="$1"
    local log_file
    log_file="$(log_file_for "$name")"
    : >"$log_file"
    chown "${TARGET_UID}:${TARGET_GID}" "$log_file"
    chmod "$LOG_MODE" "$log_file"
    printf '%s' "$log_file"
}

##
## Process spawn primitives. One pair of helpers covers every service:
## spawn_as_target_user for unprivileged components, spawn_as_root for
## components that need root (e.g. VPN tun device).
##
spawn_as_target_user() {
    ## Run a command as the operator UID, redirecting all I/O to its log.
    ## Returns 0 if the spawn completed or the service was already up.
    local name="$1"; shift
    local payload="$1"; shift
    if is_service_running "$name"; then
        log_warn "Service '${name}' is already running (PID $(read_pid_value "$name"))."
        return "$EXIT_OK"
    fi
    local log_file
    log_file="$(ensure_log_file "$name")"
    setsid sudo -u "#${TARGET_UID}" -g "#${TARGET_GID}" -- \
        bash -lc "${payload}" \
        >>"$log_file" 2>&1 </dev/null &
    local pid=$!
    write_pid_file "$name" "$pid"
    log_info "Started '${name}' as UID ${TARGET_UID} (PID ${pid})."
}

spawn_as_root() {
    ## Run a command as root in its own session and persist the PID.
    local name="$1"; shift
    local payload="$1"; shift
    if is_service_running "$name"; then
        log_warn "Service '${name}' is already running (PID $(read_pid_value "$name"))."
        return "$EXIT_OK"
    fi
    local log_file
    log_file="$(ensure_log_file "$name")"
    setsid bash -lc "${payload}" \
        >>"$log_file" 2>&1 </dev/null &
    local pid=$!
    write_pid_file "$name" "$pid"
    log_info "Started '${name}' as root (PID ${pid})."
}

terminate_pid_tree() {
    ## Send SIGTERM to the process group, wait up to the grace window, then
    ## escalate to SIGKILL if the process is still alive.
    local pid="$1"
    [[ -z "$pid" ]] && return 0
    is_pid_alive "$pid" || return 0
    local pgid
    pgid="$(ps -o pgid= "$pid" 2>/dev/null | tr -d ' ')"
    if [[ -n "$pgid" ]]; then
        kill -TERM "-${pgid}" 2>/dev/null || true
    else
        kill -TERM "$pid" 2>/dev/null || true
    fi
    local waited=0
    while is_pid_alive "$pid" && (( waited < SHUTDOWN_GRACE_SECONDS )); do
        sleep "$STATUS_POLL_INTERVAL_SECONDS"
        waited=$(( waited + STATUS_POLL_INTERVAL_SECONDS ))
    done
    if is_pid_alive "$pid"; then
        log_warn "PID ${pid} did not exit within ${SHUTDOWN_GRACE_SECONDS}s, sending SIGKILL."
        if [[ -n "$pgid" ]]; then
            kill -KILL "-${pgid}" 2>/dev/null || true
        else
            kill -KILL "$pid" 2>/dev/null || true
        fi
    fi
}

stop_named_service() {
    ## Idempotently stop the named service and remove its PID file.
    local name="$1"
    local pid pid_file
    pid="$(read_pid_value "$name")"
    pid_file="$(pid_file_for "$name")"
    if is_pid_alive "$pid"; then
        log_info "Stopping '${name}' (PID ${pid})..."
        terminate_pid_tree "$pid"
    fi
    rm -f "$pid_file"
}

##
## Ownership maintenance. Both an on-demand restore and a background loop
## tied to the chown_watcher pseudo-service so root-owned writes from any
## service never leave files the operator user cannot read.
##
chown_project_tree() {
    ## Restore ownership of the project root to the operator UID/GID.
    chown -R "${TARGET_UID}:${TARGET_GID}" "$PROJECT_ROOT" 2>/dev/null || true
}

start_chown_watcher() {
    ## Spawn the periodic chown loop as a detached background process.
    local name="$SVC_CHOWN"
    if is_service_running "$name"; then
        log_warn "Chown watcher already running."
        return "$EXIT_OK"
    fi
    local log_file
    log_file="$(ensure_log_file "$name")"
    local uid="$TARGET_UID" gid="$TARGET_GID"
    local interval="$CHOWN_INTERVAL_SECONDS" root="$PROJECT_ROOT"
    setsid bash -lc "
        trap 'chown -R ${uid}:${gid} \"${root}\" 2>/dev/null; exit 0' TERM INT
        while true; do
            chown -R ${uid}:${gid} '${root}' 2>/dev/null
            sleep ${interval}
        done
    " >>"$log_file" 2>&1 </dev/null &
    local pid=$!
    write_pid_file "$name" "$pid"
    log_info "Started chown watcher (PID ${pid}, interval ${CHOWN_INTERVAL_SECONDS}s)."
}

##
## Concrete service launchers. Each function knows how to start exactly one
## component and decides whether it should run based on payload.json flags.
##
start_lazyc2_service() {
    ## Launch the Flask C2 server with cert passphrase pre-fed on stdin.
    local port="${CONFIG[c2_port]}"
    local user="${CONFIG[c2_user]}"
    local pass="${CONFIG[c2_pass]}"
    if [[ -z "$port" || -z "$user" || -z "$pass" ]]; then
        log_error "payload.json is missing c2_port, c2_user, or c2_pass."
        return "$EXIT_MISCONFIG"
    fi
    local payload
    payload="cd '${PROJECT_ROOT}' && source '${VENV_PATH}/bin/activate' && exec python3 -W ignore lazyc2.py '${port}' '${user}' '${pass}' <<<'${CERT_PASSPHRASE}'"
    spawn_as_target_user "$SVC_C2" "$payload"
}

start_www_service() {
    ## Launch the LazyOwn HTTP file/cert server via the ./run -c entry point.
    local payload
    payload="cd '${PROJECT_ROOT}' && exec ./run --no-banner -c 'www ${CERT_PASSPHRASE}'"
    spawn_as_target_user "$SVC_WWW" "$payload"
}

start_vpn_service() {
    ## Bring up the configured VPN tunnel as root. Disabled unless
    ## enable_service_vpn is true and service_vpn_index is a positive int.
    if ! config_truthy enable_service_vpn; then
        log_info "VPN service disabled (enable_service_vpn != true)."
        return "$EXIT_OK"
    fi
    local idx="${CONFIG[service_vpn_index]:-}"
    if [[ ! "$idx" =~ ^[1-9][0-9]*$ ]]; then
        log_warn "VPN service requested but service_vpn_index is invalid: '${idx}'."
        return "$EXIT_OK"
    fi
    local payload
    payload="cd '${PROJECT_ROOT}' && exec ./run --no-banner -c 'vpn ${idx}'"
    spawn_as_root "$SVC_VPN" "$payload"
}

start_discord_service() {
    ## Optionally launch the Discord C2 bot.
    if ! config_truthy enable_discord_c2; then
        return "$EXIT_OK"
    fi
    local payload
    payload="cd '${PROJECT_ROOT}' && source '${VENV_PATH}/bin/activate' && exec python3 -W ignore discord_c2.py"
    spawn_as_target_user "$SVC_DISCORD" "$payload"
}

start_telegram_service() {
    ## Optionally launch the Telegram C2 bot.
    if ! config_truthy enable_telegram_c2; then
        return "$EXIT_OK"
    fi
    local payload
    payload="cd '${PROJECT_ROOT}' && source '${VENV_PATH}/bin/activate' && exec python3 -W ignore telegram_c2.py"
    spawn_as_target_user "$SVC_TELEGRAM" "$payload"
}

start_cloudflare_service() {
    ## Optionally launch the cloudflared tunnel via ./run.
    if ! config_truthy enable_cloudflare; then
        return "$EXIT_OK"
    fi
    local payload
    payload="cd '${PROJECT_ROOT}' && exec ./run --no-banner -c 'cloudflare_tunnel'"
    spawn_as_target_user "$SVC_CLOUDFLARE" "$payload"
}

start_ollama_service() {
    ## Optionally launch a local Ollama inference server for the configured
    ## model. Skipped if the ollama binary is not installed.
    if ! config_truthy enable_deepseek; then
        return "$EXIT_OK"
    fi
    if ! command -v ollama >/dev/null 2>&1; then
        log_warn "enable_deepseek=true but 'ollama' is not installed; skipping."
        return "$EXIT_OK"
    fi
    local payload
    payload="exec ollama run '${OLLAMA_MODEL}'"
    spawn_as_target_user "$SVC_OLLAMA" "$payload"
}

##
## Service registry. The single ordered list of services this script owns.
## Startup order matches this array; shutdown order is its reverse.
##
managed_services_in_order() {
    ## Echo the canonical service order, one name per line.
    printf '%s\n' \
        "$SVC_CHOWN" \
        "$SVC_C2" \
        "$SVC_WWW" \
        "$SVC_VPN" \
        "$SVC_DISCORD" \
        "$SVC_TELEGRAM" \
        "$SVC_CLOUDFLARE" \
        "$SVC_OLLAMA"
}

##
## Lifecycle commands. These are the only entry points called from main().
##
cmd_start() {
    ## Bring up every enabled service in canonical order. Idempotent.
    require_deps
    require_paths
    prepare_runtime_dirs
    load_config
    log_info "Service bring-up begins."
    chown_project_tree
    start_chown_watcher
    start_lazyc2_service
    sleep "$STARTUP_DELAY_SECONDS"
    start_www_service
    start_vpn_service
    start_discord_service
    start_telegram_service
    start_cloudflare_service
    start_ollama_service
    log_info "Service bring-up complete. State directory: ${RUN_DIR}"
}

cmd_stop() {
    ## Tear down every managed service in reverse order, then run a final
    ## chown so the operator user owns whatever was written during the run.
    prepare_runtime_dirs
    log_info "Service tear-down begins."
    local services=()
    mapfile -t services < <(managed_services_in_order)
    local i
    for (( i=${#services[@]}-1; i>=0; i-- )); do
        stop_named_service "${services[i]}"
    done
    chown_project_tree
    log_info "Service tear-down complete."
}

cmd_restart() {
    ## Stop then start, preserving idempotence.
    cmd_stop
    cmd_start
}

cmd_status() {
    ## Print a fixed-width status table for every managed service.
    prepare_runtime_dirs
    printf '%-22s %-9s %-8s %s\n' "SERVICE" "STATE" "PID" "LOG"
    local name pid state
    while IFS= read -r name; do
        pid="$(read_pid_value "$name")"
        if is_pid_alive "$pid"; then
            state="$STATE_RUNNING"
        elif [[ -n "$pid" ]]; then
            state="$STATE_STALE"
        else
            state="$STATE_STOPPED"
        fi
        printf '%-22s %-9s %-8s %s\n' \
            "$name" "$state" "${pid:--}" "$(log_file_for "$name")"
    done < <(managed_services_in_order)
}

cmd_logs() {
    ## Tail the log file of a named service. Follows the file forever.
    local name="${1:-}"
    if [[ -z "$name" ]]; then
        log_error "Usage: ${SCRIPT_NAME} logs <service-name>"
        return "$EXIT_USAGE"
    fi
    local file
    file="$(log_file_for "$name")"
    if [[ ! -f "$file" ]]; then
        log_error "No log file for service '${name}': ${file}"
        return "$EXIT_RUNTIME"
    fi
    exec tail -F "$file"
}

cmd_chown_now() {
    ## Run an immediate ownership restoration on demand.
    log_info "Restoring ownership to ${TARGET_UID}:${TARGET_GID} on ${PROJECT_ROOT}..."
    chown_project_tree
    log_info "Ownership restored."
}

usage() {
    ## Print human-readable help for the CLI surface.
    cat <<EOF
Usage: ${SCRIPT_NAME} <command> [args]

Commands:
  start             Start every enabled service in the background.
  stop              Stop every managed service in reverse order.
  restart           Equivalent to: stop && start.
  status            Show per-service state, PID, and log path.
  logs <service>    Tail the log file for a single service.
  chown-now         Run an immediate ownership restoration to ${TARGET_UID}:${TARGET_GID}.
  help              Show this message.

Managed services (in startup order):
$(managed_services_in_order | sed 's/^/  /')

Paths:
  payload   ${JSON_FILE}
  venv      ${VENV_PATH}
  run dir   ${RUN_DIR}
  log dir   ${LOG_DIR}
EOF
}

##
## Entry point. require_root re-executes under sudo and never returns there;
## the case-arm dispatch is reached only when we are already root.
##
main() {
    local cmd="${1:-status}"
    case "$cmd" in
        help|-h|--help) usage; exit "$EXIT_OK" ;;
    esac
    require_root "$@"
    if [[ $# -gt 0 ]]; then
        shift
    fi
    case "$cmd" in
        start)         cmd_start "$@" ;;
        stop)          cmd_stop "$@" ;;
        restart)       cmd_restart "$@" ;;
        status)        cmd_status "$@" ;;
        logs)          cmd_logs "$@" ;;
        chown-now)     cmd_chown_now "$@" ;;
        *)             usage; exit "$EXIT_USAGE" ;;
    esac
}

main "$@"
