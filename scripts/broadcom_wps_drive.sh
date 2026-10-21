#!/bin/bash
# broadcom_wps_drive.sh - operator-side driver for the Broadcom 802.11 SDK detection toolkit.
#
# The upstream project ships two detectors: a live fingerprinter that tells
# Broadcom's vulnerable wps_monitor apart from a patched hostapd, and YARA
# rules for extracted firmware. The live path needs a monitor-mode adapter,
# root privileges and scapy, and it leaves the adapter in monitor mode.
# This driver owns that operational overhead:
#
#   doctor       report the toolchain, the adapter and the configured SSID
#   monitor      put the adapter in monitor mode
#   unmonitor    restore the adapter to managed mode
#   fingerprint  run the live detector and archive the verdict
#   yara         run the upstream rules against an extracted firmware tree
#   status       report the current state without touching the radio
#
# Usage:
#   broadcom_wps_drive.sh doctor
#   broadcom_wps_drive.sh monitor
#   broadcom_wps_drive.sh unmonitor
#   broadcom_wps_drive.sh fingerprint
#   broadcom_wps_drive.sh yara <firmware-dir>
#   broadcom_wps_drive.sh status
#
# Flags (after the action):
#   --ssid <ssid>        access point to fingerprint
#   --interface <iface>  wireless adapter to use
#   --target <dir>       firmware tree for the YARA pass
#   --keep-monitor       leave the adapter in monitor mode after the run
#   --debug-assoc        log 802.11 auth status codes (passed to the tool)
#
# Environment:
#   BROADCOM_SSID        access point to fingerprint (default: unset)
#   BROADCOM_INTERFACE   wireless adapter (default: first wireless interface)
#   BROADCOM_TARGET      firmware tree for the YARA pass (default: unset)
#   BROADCOM_SRC         upstream checkout (default: external/.exploit/broadcom_wps)
#   BROADCOM_OUT         artefact directory (default: sessions/broadcom_wps)

set -u

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SRC="${BROADCOM_SRC:-$ROOT/external/.exploit/broadcom_wps}"
OUT="${BROADCOM_OUT:-$ROOT/sessions/broadcom_wps}"
SSID="${BROADCOM_SSID:-}"
TARGET="${BROADCOM_TARGET:-}"
INTERFACE="${BROADCOM_INTERFACE:-}"
KEEP_MONITOR=0
DEBUG_ASSOC=0
POSITIONAL=()
FINGERPRINT_SCRIPT="broadcom_fingerprint.py"
YARA_RULES="broadcom_wps_monitor.yar"

log() { printf '%s\n' "$*"; }
warn() { printf '[!] %s\n' "$*" >&2; }
die() { warn "$*"; exit 1; }

usage() {
    awk 'NR == 1 { next } /^#/ { sub(/^# ?/, ""); print; next } { exit }' "${BASH_SOURCE[0]}"
}

payload_value() {
    local key="$1" value
    [[ -f "$ROOT/payload.json" ]] || return 0
    value="$(python3 - "$ROOT/payload.json" "$key" <<'PY' 2>/dev/null
import json
import sys

try:
    with open(sys.argv[1], encoding="utf-8") as handle:
        document = json.load(handle)
except Exception:
    sys.exit(0)
value = document.get(sys.argv[2], "")
if isinstance(value, str):
    sys.stdout.write(value.replace("\n", " "))
PY
)"
    printf '%s' "$value"
}

parse_flags() {
    while [[ ${#ARGS[@]} -gt 0 ]]; do
        case "${ARGS[0]}" in
            --ssid)
                SSID="${ARGS[1]:-}"
                ARGS=("${ARGS[@]:2}")
                ;;
            --ssid=*)
                SSID="${ARGS[0]#*=}"
                ARGS=("${ARGS[@]:1}")
                ;;
            --interface)
                INTERFACE="${ARGS[1]:-}"
                ARGS=("${ARGS[@]:2}")
                ;;
            --interface=*)
                INTERFACE="${ARGS[0]#*=}"
                ARGS=("${ARGS[@]:1}")
                ;;
            --target)
                TARGET="${ARGS[1]:-}"
                ARGS=("${ARGS[@]:2}")
                ;;
            --target=*)
                TARGET="${ARGS[0]#*=}"
                ARGS=("${ARGS[@]:1}")
                ;;
            --keep-monitor)
                KEEP_MONITOR=1
                ARGS=("${ARGS[@]:1}")
                ;;
            --debug-assoc)
                DEBUG_ASSOC=1
                ARGS=("${ARGS[@]:1}")
                ;;
            -*)
                warn "unknown flag: ${ARGS[0]}"
                ARGS=("${ARGS[@]:1}")
                ;;
            *)
                break
                ;;
        esac
    done
}

ARGS=("$@")
parse_flags
ACTION=""
if [[ ${#ARGS[@]} -gt 0 ]]; then
    ACTION="${ARGS[0]}"
    ARGS=("${ARGS[@]:1}")
fi
parse_flags
while [[ ${#ARGS[@]} -gt 0 ]]; do
    POSITIONAL+=("${ARGS[0]}")
    ARGS=("${ARGS[@]:1}")
done
ACTION="${ACTION:-fingerprint}"

if [[ -z "$SSID" ]]; then
    SSID="$(payload_value wifi_ssid)"
fi
if [[ -z "$TARGET" ]]; then
    TARGET="$(payload_value target_path)"
fi
if [[ -z "$INTERFACE" ]]; then
    INTERFACE="$(payload_value device)"
fi

detect_interface() {
    local candidate
    for candidate in /sys/class/net/*/wireless; do
        if [[ -d "$candidate" ]]; then
            basename "$(dirname "$candidate")"
            return 0
        fi
    done
    printf ''
}

is_wireless() {
    [[ -d "/sys/class/net/$1/wireless" ]]
}

apply_interface() {
    INTERFACE="$(resolve_interface)"
}

resolve_interface() {
    local detected
    if [[ -n "$INTERFACE" ]]; then
        if is_wireless "$INTERFACE"; then
            printf '%s' "$INTERFACE"
            return 0
        fi
        detected="$(detect_interface)"
        if [[ -n "$detected" && "$detected" != "$INTERFACE" ]]; then
            warn "$INTERFACE is not a wireless adapter - using $detected"
            INTERFACE="$detected"
        fi
        printf '%s' "$INTERFACE"
        return 0
    fi
    detected="$(detect_interface)"
    INTERFACE="${detected:-wlan0}"
    printf '%s' "$INTERFACE"
}

is_root() {
    [[ "$(id -u)" == "0" ]]
}

have_sudo() {
    is_root && return 0
    command -v sudo >/dev/null 2>&1 || return 1
    sudo -n true >/dev/null 2>&1
}

elevate() {
    if is_root; then
        "$@"
    elif have_sudo; then
        sudo -n "$@"
    else
        die "root privileges required - configure passwordless sudo or run as root"
    fi
}

interface_mode() {
    local iface="$1" mode
    mode="$(iw dev "$iface" info 2>/dev/null | awk '/^\s*type/ {print $2; exit}')"
    printf '%s' "${mode:-unknown}"
}

interface_up() {
    local iface="$1" flags
    flags="$(cat "/sys/class/net/$iface/flags" 2>/dev/null || echo 0)"
    flags="${flags#0x}"
    if [[ $(( 16#$flags & 1 )) -eq 1 ]]; then
        printf 'yes'
    else
        printf 'no'
    fi
}

python_bin() {
    command -v python3 2>/dev/null || printf 'python3'
}

has_scapy() {
    "$(python_bin)" -c "import scapy" >/dev/null 2>&1
}

do_monitor() {
    local iface
    apply_interface
    iface="$INTERFACE"
    command -v iw >/dev/null 2>&1 || die "iw not found - install the iw package"
    log "[*] Putting $iface in monitor mode..."
    elevate ip link set dev "$iface" down
    elevate iw dev "$iface" set monitor none
    elevate ip link set dev "$iface" up
    log "[*] $iface is now in monitor mode (mode=$(interface_mode "$iface"), up=$(interface_up "$iface"))"
}

do_unmonitor() {
    local iface
    apply_interface
    iface="$INTERFACE"
    command -v iw >/dev/null 2>&1 || die "iw not found - install the iw package"
    log "[*] Restoring $iface to managed mode..."
    elevate ip link set dev "$iface" down
    elevate iw dev "$iface" set type managed
    elevate ip link set dev "$iface" up
    log "[*] $iface is back in managed mode"
}

ensure_monitor_mode() {
    local iface="$1" mode
    mode="$(interface_mode "$iface")"
    if [[ "$mode" != "monitor" ]]; then
        log "[*] $iface is in $mode mode, switching to monitor..."
        do_monitor
    fi
}

run_fingerprint() {
    local iface python_bin_path status result_dir
    apply_interface
    iface="$INTERFACE"
    if [[ -z "$SSID" ]]; then
        warn "no SSID configured"
        log "  assign wifi_ssid \"MyAccessPoint\"     # persists in the shell"
        log "  broadcom_wps --ssid \"MyAccessPoint\"   # or pass it as a free arg"
        do_status
        return 2
    fi
    [[ -f "$SRC/$FINGERPRINT_SCRIPT" ]] || die "fingerprint script missing at $SRC/$FINGERPRINT_SCRIPT"
    has_scapy || die "scapy is not importable - run 'pip install scapy' first"
    python_bin_path="$(python_bin)"
    mkdir -p "$OUT"
    ensure_monitor_mode "$iface"
    log "[*] Fingerprinting SSID '$SSID' on $iface (results in $OUT)..."
    set +e
    (cd "$OUT" && elevate "$python_bin_path" "$SRC/$FINGERPRINT_SCRIPT" --interface "$iface" --ssid "$SSID")
    status=$?
    set -e
    if [[ "$KEEP_MONITOR" -eq 0 ]]; then
        do_unmonitor
    fi
    result_dir="$(find "$OUT" -maxdepth 1 -type d -name 'broadcom-fingerprint-*' 2>/dev/null | sort | tail -n 1)"
    if [[ -n "$result_dir" && -f "$result_dir/result.json" ]]; then
        cp -f "$result_dir/result.json" "$OUT/broadcom_wps_result.json"
        log "[*] Verdict: $OUT/broadcom_wps_result.json"
        log "[*] Evidence: $result_dir"
    else
        warn "no result.json produced"
    fi
    case "$status" in
        0) log "[*] Assessment complete" ;;
        1) warn "assessment inconclusive - the AP does not advertise WPS or the adapter saw nothing" ;;
        *) warn "fingerprint run failed (exit $status)" ;;
    esac
    return "$status"
}

run_yara() {
    local stamp rules
    if [[ -z "$TARGET" && ${#POSITIONAL[@]} -gt 0 ]]; then
        TARGET="${POSITIONAL[0]}"
    fi
    [[ -n "$TARGET" ]] || die "no firmware directory - pass --target <dir> or set BROADCOM_TARGET"
    [[ -d "$TARGET" ]] || die "firmware directory not found: $TARGET"
    rules="$SRC/$YARA_RULES"
    [[ -f "$rules" ]] || die "YARA rules missing at $rules"
    command -v yara >/dev/null 2>&1 || die "yara not found - install the yara package"
    mkdir -p "$OUT"
    stamp="$(date -u +%Y%m%dT%H%M%SZ)"
    log "[*] Scanning $TARGET with $rules..."
    yara -w -r "$rules" "$TARGET" | tee "$OUT/yara_${stamp}.txt"
    log "[*] Matches written to $OUT/yara_${stamp}.txt"
}

do_status() {
    local iface mode result
    apply_interface
    iface="$INTERFACE"
    mode="$(interface_mode "$iface")"
    log "Broadcom WPS status"
    log "  interface      : $iface (mode=$mode, up=$(interface_up "$iface"))"
    log "  ssid           : ${SSID:-<unset>}"
    log "  firmware target: ${TARGET:-<unset>}"
    log "  checkout       : $SRC$([[ -f "$SRC/$FINGERPRINT_SCRIPT" ]] && echo ' (present)' || echo ' (missing)')"
    log "  artefacts      : $OUT"
    log "  scapy          : $(has_scapy && echo present || echo missing)"
    log "  yara           : $(command -v yara >/dev/null 2>&1 && echo present || echo missing)"
    log "  iw             : $(command -v iw >/dev/null 2>&1 && echo present || echo missing)"
    log "  privileges     : $(is_root && echo root || { have_sudo && echo "sudo (passwordless)" || echo "no passwordless sudo"; })"
    result="$OUT/broadcom_wps_result.json"
    if [[ -f "$result" ]]; then
        log "  last verdict   : $result"
    else
        log "  last verdict   : none yet"
    fi
}

do_doctor() {
    local missing=0 iface mode
    apply_interface
    iface="$INTERFACE"
    mode="$(interface_mode "$iface")"
    log "Broadcom WPS doctor"
    if command -v iw >/dev/null 2>&1; then
        log "  iw             : $(command -v iw)"
    else
        warn "  iw             : missing - install the iw package"
        missing=1
    fi
    if has_scapy; then
        log "  scapy          : present"
    else
        warn "  scapy          : missing - run 'python3 -m pip install scapy'"
        missing=1
    fi
    if command -v yara >/dev/null 2>&1; then
        log "  yara           : $(command -v yara)"
    else
        warn "  yara           : missing - install the yara package (needed for the static pass)"
    fi
    if is_root; then
        log "  privileges     : root"
    elif have_sudo; then
        log "  privileges     : passwordless sudo"
    else
        warn "  privileges     : no passwordless sudo - configure it or run as root"
        missing=1
    fi
    log "  interface      : $iface (mode=$mode, up=$(interface_up "$iface"))"
    if [[ "$mode" != "monitor" ]]; then
        warn "  adapter        : not in monitor mode - run 'broadcom_wps monitor' first"
    else
        log "  adapter        : monitor mode"
    fi
    if [[ -f "$SRC/$FINGERPRINT_SCRIPT" ]]; then
        log "  checkout       : $SRC"
    else
        warn "  checkout       : missing at $SRC - run the addon once to clone it"
        missing=1
    fi
    if [[ -n "$SSID" ]]; then
        log "  ssid           : $SSID"
    else
        warn "  ssid           : unset - assign wifi_ssid or pass --ssid"
    fi
    if [[ "$missing" -eq 0 ]]; then
        log "  verdict        : ready"
        return 0
    fi
    log "  verdict        : missing prerequisites (see above)"
    return 1
}

main() {
    case "$ACTION" in
        doctor) do_doctor ;;
        monitor) do_monitor ;;
        unmonitor) do_unmonitor ;;
        fingerprint) run_fingerprint ;;
        yara) run_yara ;;
        status) do_status ;;
        help|-h|--help) usage ;;
        *)
            warn "unknown action: $ACTION"
            usage
            return 2
            ;;
    esac
}

main "$@"
