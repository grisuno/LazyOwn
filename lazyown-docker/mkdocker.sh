#!/bin/bash

# LazyOwn Dockerizer Script
# Builds, runs, and manages Docker containers for LazyOwn red teaming framework

set -e

# Configuration
IMAGE_NAME="lazyown"
CONTAINER_NAME="lazyown-container"
REPO_URL="https://github.com/grisuno/LazyOwn.git"
REPO_COMMIT="abcdef123456" # Replace with specific commit hash
CURRENT_DIR=$(pwd)
PAYLOAD_JSON="${CURRENT_DIR}/payload.json"
DOCKERFILE="${CURRENT_DIR}/Dockerfile.dockerfile"
LOG_FILE="${CURRENT_DIR}/lazyown_docker.log"

# Default ports (fallback if payload.json ports are missing)
DEFAULT_PORTS=("80" "443" "4444" "5555" "6666" "7777" "8888" "31337")

# Help message
usage() {
    echo "Usage: $0 {build|run|stop|clean} [--vpn <number>]"
    echo "Commands:"
    echo "  build    Build the LazyOwn Docker image"
    echo "  run      Run a LazyOwn container"
    echo "  stop     Stop the running LazyOwn container"
    echo "  clean    Remove the LazyOwn container and image"
    echo "Options:"
    echo "  --vpn    VPN mode (1 for OpenVPN, 2 for WireGuard, default: 1)"
    exit 1
}

# Log function
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

# Check if Docker is running
check_docker() {
    if ! docker info >/dev/null 2>&1; then
        log "Error: Docker daemon is not running."
        exit 1
    fi
}

# Check if file exists
check_file() {
    if [ ! -f "$1" ]; then
        log "Error: $1 not found."
        exit 1
    fi
}

# Validate payload.json
validate_payload() {
    check_file "$PAYLOAD_JSON"
    required_fields=("c2_port" "rhost" "domain" "c2_user" "c2_pass" "sleep_start" "os_id" "enable_telegram_c2" "enable_discord_c2" "enable_deepseek" "enable_nc" "enable_cloudflare")
    for field in "${required_fields[@]}"; do
        if ! jq -e ".${field}" "$PAYLOAD_JSON" >/dev/null 2>&1; then
            log "Error: Missing or invalid field '${field}' in payload.json."
            exit 1
        fi
    done
}

# Check if container exists
container_exists() {
    docker ps -a --format '{{.Names}}' | grep -q "^${1}$"
}

# Check if image exists
image_exists() {
    docker images --format '{{.Repository}}' | grep -q "^${1}$"
}

# Get ports from payload.json
get_ports() {
    local ports=()
    local seen_ports=()
    if jq -e '.ports' "$PAYLOAD_JSON" >/dev/null 2>&1; then
        while IFS= read -r port; do
            if [[ "$port" =~ ^[0-9]+$ && "$port" -ge 1 && "$port" -le 65535 ]]; then
                if [[ ! " ${seen_ports[*]} " =~ " ${port} " ]]; then
                    ports+=("$port")
                    seen_ports+=("$port")
                else
                    log "Warning: Duplicate port '$port' in payload.json. Skipping."
                fi
            else
                log "Warning: Invalid port '$port' in payload.json. Skipping."
            fi
        done < <(jq -r '.ports[]' "$PAYLOAD_JSON")
    fi
    if [ ${#ports[@]} -eq 0 ]; then
        ports=("${DEFAULT_PORTS[@]}")
        log "Using default ports: ${ports[*]}"
    fi
    echo "${ports[@]}"
}

# Build Docker image
build_image() {
    log "Building LazyOwn Docker image..."
    check_file "$DOCKERFILE"
    validate_payload
    docker build -t "$IMAGE_NAME" --build-arg REPO_URL="$REPO_URL" --build-arg REPO_COMMIT="$REPO_COMMIT" -f "$DOCKERFILE" .
    if [ $? -eq 0 ]; then
        log "Image '$IMAGE_NAME' built successfully."
    else
        log "Failed to build image."
        exit 1
    fi
}

# Run container
run_container() {
    local vpn_mode="$1"
    log "Starting LazyOwn container..."
    validate_payload
    if ! command -v jq &>/dev/null; then
        log "Error: jq is required but not installed."
        exit 1
    fi

    # Parse payload.json
    C2_PORT=$(jq -r '.c2_port' "$PAYLOAD_JSON")
    RHOST=$(jq -r '.rhost' "$PAYLOAD_JSON")
    DOMAIN=$(jq -r '.domain' "$PAYLOAD_JSON")
    C2_USER=$(jq -r '.c2_user' "$PAYLOAD_JSON")
    C2_PASS=$(jq -r '.c2_pass' "$PAYLOAD_JSON")
    SLEEP_START=$(jq -r '.sleep_start' "$PAYLOAD_JSON")
    OS_ID=$(jq -r '.os_id' "$PAYLOAD_JSON")
    ENABLE_TELEGRAM_C2=$(jq -r '.enable_telegram_c2' "$PAYLOAD_JSON")
    ENABLE_DISCORD_C2=$(jq -r '.enable_discord_c2' "$PAYLOAD_JSON")
    ENABLE_DEEPSEEK=$(jq -r '.enable_deepseek' "$PAYLOAD_JSON")
    ENABLE_NC=$(jq -r '.enable_nc' "$PAYLOAD_JSON")
    ENABLE_CF=$(jq -r '.enable_cloudflare' "$PAYLOAD_JSON")

    # Get ports
    PORTS=($(get_ports))
    PORT_MAPPINGS=""
    for port in "${PORTS[@]}"; do
        PORT_MAPPINGS="$PORT_MAPPINGS -p $port:$port"
    done

    if container_exists "$CONTAINER_NAME"; then
        log "Container '$CONTAINER_NAME' already exists. Starting it..."
        docker start "$CONTAINER_NAME"
        docker exec -it "$CONTAINER_NAME" bash -c "/home/lazyown/entrypoint.sh --vpn $vpn_mode"
    else
        if ! image_exists "$IMAGE_NAME"; then
            build_image
        fi
        log "Creating and running container '$CONTAINER_NAME'..."
        docker run -d --name "$CONTAINER_NAME" \
            --cap-drop=ALL \
            --security-opt=no-new-privileges \
            --read-only \
            --tmpfs /tmp \
            --tmpfs /var/log \
            $PORT_MAPPINGS \
            -v "$CURRENT_DIR/payload.json:/home/lazyown/payload.json:ro" \
            -e C2_PORT="$C2_PORT" \
            -e RHOST="$RHOST" \
            -e DOMAIN="$DOMAIN" \
            -e C2_USER="$C2_USER" \
            -e C2_PASS="$C2_PASS" \
            -e SLEEP_START="$SLEEP_START" \
            -e OS_ID="$OS_ID" \
            -e ENABLE_TELEGRAM_C2="$ENABLE_TELEGRAM_C2" \
            -e ENABLE_DISCORD_C2="$ENABLE_DISCORD_C2" \
            -e ENABLE_DEEPSEEK="$ENABLE_DEEPSEEK" \
            -e ENABLE_NC="$ENABLE_NC" \
            -e ENABLE_CF="$ENABLE_CF" \
            "$IMAGE_NAME"
        docker exec -it "$CONTAINER_NAME" bash -c "/home/lazyown/entrypoint.sh --vpn $vpn_mode"
    fi
}

# Stop container
stop_container() {
    if container_exists "$CONTAINER_NAME"; then
        log "Stopping container '$CONTAINER_NAME'..."
        docker stop "$CONTAINER_NAME"
    else
        log "Container '$CONTAINER_NAME' does not exist."
    fi
}

# Clean container and image
clean_container_and_image() {
    stop_container
    if container_exists "$CONTAINER_NAME"; then
        log "Removing container '$CONTAINER_NAME'..."
        docker rm "$CONTAINER_NAME"
    fi
    if image_exists "$IMAGE_NAME"; then
        log "Removing image '$IMAGE_NAME'..."
        docker rmi "$IMAGE_NAME"
    else
        log "Image '$IMAGE_NAME' does not exist."
    fi
}

# Parse arguments
VPN_MODE=1
COMMAND=""
while [[ "$#" -gt 0 ]]; do
    case $1 in
        build|run|stop|clean)
            COMMAND="$1"
            ;;
        --vpn)
            if [[ "$2" =~ ^[0-9]+$ ]]; then
                VPN_MODE="$2"
                shift
            else
                log "Error: --vpn value must be an integer."
                exit 1
            fi
            ;;
        *)
            usage
            ;;
    esac
    shift
done

# Execute command
check_docker
case "$COMMAND" in
    build)
        build_image
        ;;
    run)
        run_container "$VPN_MODE"
        ;;
    stop)
        stop_container
        ;;
    clean)
        clean_container_and_image
        ;;
    *)
        usage
        ;;
esac