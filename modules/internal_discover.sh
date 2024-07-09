#!/bin/bash

for i in $(seq 1 254); do
    timeout 1 bash -c "ping -c 1 10.10.0.$i" &> /dev/null && echo "[+] host 10.10.0.$i is ACTIVE" &
done; wait