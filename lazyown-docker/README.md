# lazyown-docker

Docker configuration for running LazyOwn in an isolated container. Useful for
clean-room testing, repeatable engagements, and the sandbox mode feature
(`sandbox on` in the CLI).

## Files

| File | Purpose |
|------|---------|
| `Dockerfile` | Multi-stage image build. Installs system dependencies (nmap, gcc, make, SecLists subset), creates the virtualenv, copies the framework source, and sets the entrypoint. |
| `docker-compose.yml` | Service definition for the full stack: the LazyOwn CLI container plus an optional C2 container with port mappings for the web UI and listener ports. |
| `entrypoint.sh` | Container startup script. Checks for `payload.json`, runs `wizard` if `rhost` is unset, then launches the CLI. |
| `init.sh` | One-time initialisation: generates TLS certificates, sets default `payload.json` values, and pulls the Atomic Red Team corpus. |
| `mkdocker.sh` | Helper to build the image and start the compose stack in one command. |

## Quick start

```bash
# Build and start
bash lazyown-docker/mkdocker.sh

# Or step by step
docker build -t lazyown -f lazyown-docker/Dockerfile .
docker-compose -f lazyown-docker/docker-compose.yml up -d

# Open an interactive shell
docker exec -it lazyown_cli /bin/bash
./run
```

## Sandbox mode

The framework's `sandbox` CLI command uses Docker internally to run individual
commands in an isolated container, then streams the output back:

```
(LazyOwn) > sandbox on
(LazyOwn) > lazynmap   # runs inside Docker, output returned to the shell
```

The sandbox feature reads the image name from `payload.json` (`sandbox_image`
key). The image must be built from this Dockerfile.

## Networking

The default compose file maps:
- `<c2_port>/tcp` for the C2 HTTPS listener
- `<lport>/tcp` for the reverse-shell listener

Both ports are read from `payload.json` at container start. Override with
environment variables:

```bash
C2_PORT=8443 LPORT=4444 docker-compose up -d
```
