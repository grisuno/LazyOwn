# lazyown-docker

> **Note:** the primary container path is the root [`Dockerfile`](../Dockerfile),
> published as `ghcr.io/grisuno/lazyown:latest` (`docker run -it
> ghcr.io/grisuno/lazyown:latest`). This directory holds the legacy
> full-stack compose variant (tmux-orchestrated) kept for reference.

Docker support for running LazyOwn in an isolated container. Built and tested on Python 3.12 (slim-bookworm).

## Directory structure

| File | Purpose |
|------|---------|
| `Dockerfile` | Multi-stage build. Builder stage installs system deps (git, go, gcc), creates a Python venv, pins all dependencies via `requirements.txt`. Runtime stage copies the framework + venv and adds runtime tools (nmap, tmux, iproute2, net-tools, parallel). |
| `docker-compose.yml` | Quick launcher with port mappings, payload volume mount, and environment variables. |  
| `entrypoint.sh` | Container startup script. Reads `payload.json`, creates tmux session with panels for C2, recon, VPN, web interface, and optional services (Telegram/Discord bots, DeepSeek, Cloudflare tunnel). |
| `init.sh` | One-liner to install jq, build image, and run. |
| `mkdocker.sh` | CLI helper: `./mkdocker.sh build`, `./mkdocker.sh run --vpn 1`, `./mkdocker.sh stop`, `./mkdocker.sh clean`. |

## Quick start

```bash
cd lazyown-docker

# Build the image
./mkdocker.sh build

# Or manually:
docker build --build-arg REPO_URL=https://github.com/grisuno/LazyOwn.git --build-arg REPO_COMMIT=main -t lazyown -f Dockerfile .

# Run (interactive tmux session)
./mkdocker.sh run --vpn 1

# Run a quick sanity check
docker run --rm -v $(pwd)/../payload.json:/home/lazyown/payload.json:ro -e C2_PORT=4444 -e RHOST=10.0.0.1 -e DOMAIN=test.local -e C2_USER=admin -e C2_PASS=test123 -e SLEEP_START=5 -e OS_ID=linux -e ENABLE_TELEGRAM_C2=false -e ENABLE_DISCORD_C2=false -e ENABLE_DEEPSEEK=false -e ENABLE_NC=false -e ENABLE_CF=false lazyown /bin/bash -c 'cd /home/lazyown/LazyOwn && source env/bin/activate && echo -e "help\nexit" | timeout 10 python3 -W ignore lazyown.py'
```

## Networking

Ports are read from `payload.json` (`ports` array) and mapped to the host. Defaults: 80, 443, 4444, 5555, 6666, 7777, 8888, 31337.

The following environment variables are consumed by the entrypoint:

| Variable | Source | Default |
|----------|--------|---------|
| `C2_PORT` | payload.json | 4444 |
| `RHOST` | payload.json | — |
| `DOMAIN` | payload.json | — |
| `C2_USER` | payload.json | admin |
| `C2_PASS` | payload.json | LazyOwn |
| `SLEEP_START` | payload.json | 5 |
| `OS_ID` | payload.json | linux |
| `VPN` | mkdocker.sh --vpn | 1 |
| `TERM` | hardcoded | xterm |

## Known issues & fixes applied

- **repo.charm.sh offline** — replaced with direct GitHub download of gum v0.14.5 `.deb`.
- **Python < 3.12** — base image changed from `debian:bookworm-slim` to `python:3.12-slim-bookworm` to satisfy `certipy-ad==5.0.4`.
- **Dependency conflicts** — packages are installed with `--no-deps` (batched via `xargs -n 50`) to bypass pip's version solver. Conflicting packages (`certipy-ad`) are installed separately.
- **Missing runtime binaries** — added `iproute2`, `iputils-ping`, `net-tools`, `parallel` to the runtime stage.
- **Missing Python modules** — `bleach` installed separately (transitive dep, not listed in `requirements.txt`).
- **payload.json path** — symlink `/home/lazyown/LazyOwn/payload.json` -> `/home/lazyown/payload.json` so scripts using relative paths work.
- **tmux without TTY** — container started with `-dt` flag and `TERM=xterm` to give tmux a pseudo-terminal.
