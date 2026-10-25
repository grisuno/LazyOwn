# C2 Stack (Ephemeral)

Local ephemeral C2: `Caddy` terminates TLS with automatic Let's Encrypt
certificates, `lazyown` listens only on the internal network.

## Usage

```bash
DOMAIN=c2.example.com docker compose -f deploy/c2/docker-compose.yml up -d
DOMAIN=c2.example.com docker compose -f deploy/c2/docker-compose.yml down -v
```

Or via CLI:

```bash
infra deploy --provider local
infra destroy --provider local
```
