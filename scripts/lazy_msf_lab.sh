#!/bin/bash
# lazy_msf_lab.sh — Metasploitable2 smoke lab manager for LazyOwn.
#
# The lab image is operator-provided (Rapid7 license): place
# metasploitable-linux-2.0.0.zip next to this script's install dir or pass
# its path via MSF_LAB_ZIP. The script never downloads the image itself.
#
# Usage:
#   lazy_msf_lab.sh setup [zip-path]  # unzip + import guidance
#   lazy_msf_lab.sh up                # start VM headless
#   lazy_msf_lab.sh status            # VM state + guest IP
#   lazy_msf_lab.sh down              # stop VM
#   lazy_msf_lab.sh smoke [target]    # loop smoke run, prints verdict
#
# Non-interactive except setup's import guidance (operator imports once
# in VirtualBox; thereafter everything is CLI-driven).

set -u

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
LAB_DIR="$ROOT/external/.exploit/lazy_msf_lab"
ZIP_NAME="metasploitable-linux-2.0.0.zip"
ZIP_URL="https://sourceforge.net/projects/metasploitable/files/Metasploitable2/$ZIP_NAME/download"
VM_NAME="${MSF_LAB_VM:-Metasploitable2}"
TARGET="${MSF_LAB_TARGET:-}"

mkdir -p "$LAB_DIR"

case "${1:-status}" in
    setup)
        ZIP="${2:-$LAB_DIR/$ZIP_NAME}"
        if [[ ! -f "$ZIP" ]]; then
            echo "The Metasploitable2 image is ~800MB."
            read -r -p "Download $ZIP_NAME from SourceForge now? [Y] " reply
            reply="${reply:-Y}"
            if [[ ! "$reply" =~ ^[Yy] ]]; then
                echo "Place $ZIP_NAME in $LAB_DIR/ (or pass its path) and re-run setup."
                exit 0
            fi
            curl -C - -L --progress-bar -o "$LAB_DIR/$ZIP_NAME" "$ZIP_URL"
            ZIP="$LAB_DIR/$ZIP_NAME"
        fi
        echo "Unzipping lab image into $LAB_DIR/ (once)..."
        unzip -o -q "$ZIP" -d "$LAB_DIR/"
        echo "Import the VM once (VirtualBox):"
        echo "  VBoxManage import \"$LAB_DIR/Metasploitable2-Linux/Metasploitable2-Linux.ovf\" --vsys 0 --vmname $VM_NAME"
        echo "Then: bash scripts/lazy_msf_lab.sh up"
        ;;
    up)
        VBoxManage startvm "$VM_NAME" --type headless && echo "VM $VM_NAME starting..."
        sleep 15
        bash "$0" status
        ;;
    status)
        VBoxManage showvminfo "$VM_NAME" --machinereadable 2>/dev/null | grep -E "^VMState=" || echo "VM $VM_NAME not imported yet (run setup first)"
        for nic in 0 1; do
            VBoxManage guestproperty get "$VM_NAME" "/VirtualBox/GuestInfo/Net/$nic/V4/IP" 2>/dev/null
        done
        ;;
    down)
        VBoxManage controlvm "$VM_NAME" acpipowerbutton && echo "VM $VM_NAME stopping..."
        ;;
    smoke)
        TARGET="${2:-$TARGET}"
        [[ -n "$TARGET" ]] || { echo "Usage: $0 smoke <target-ip> (or set MSF_LAB_TARGET)"; exit 2; }
        echo "Smoke run against $TARGET: loop drives recon, cred spray and exploit intents."
        cd "$ROOT" && python3 - <<EOF
import json
from modules.lazy_loop import LazyLoopEngine
engine = LazyLoopEngine()
rec = engine.create_task("gain initial access on $TARGET")
tid = rec["task_id"]
engine.ensure_target(tid, "$TARGET", "msf smoke lab")
result = engine.run(tid, max_rounds=6, workers=2)
verdict = (result.get("verdict") or {})
print(json.dumps({
    "task": tid,
    "status": result.get("status"),
    "rounds": result.get("rounds"),
    "verdict": verdict.get("verdict"),
    "coverage_pct": verdict.get("coverage_pct"),
    "findings": verdict.get("findings"),
    "report": verdict.get("path"),
}, indent=2))
EOF
        ;;
    *) echo "Usage: $0 setup|up|status|down|smoke [args]"; exit 2 ;;
esac
