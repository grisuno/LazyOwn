# Redirector (Disposable)

Disposable Cloudflare redirector: `cloudflared quick tunnel` -> `Caddy`
path filter -> real C2 on `127.0.0.1:4444`.

Only `/gmail/*`, `/api/*`, `/command/*`, `/s/*` are forwarded. Everything
else returns `404` to burn scanners and sandboxes.

## Usage

```bash
C2_HOST=host.docker.internal C2_PORT=4444 docker compose -f deploy/redirector/docker-compose.yml up -d --scale redirector=2
docker compose -f deploy/redirector/docker-compose.yml logs --tail 50
# copy the https://*.trycloudflare.com URL into c2_fallback_urls
docker compose -f deploy/redirector/docker-compose.yml down -v
```

`C2_HOST` defaults to `host.docker.internal` so the filter reaches a C2
running on the Docker host. Override it when the C2 lives elsewhere.

## Beacon wiring (order matters)

Tunnel URLs bake into the Go beacon at compile time. After every fresh
spawn, rebuild:

```bash
infra redirector spawn --count 2   # prints only fresh URLs
assign c2_fallback_urls <url1,url2>
c2 linux 2                         # rebuilds with redirector fallbacks
```

`infra redirector list` shows URL age and prunes entries older than 24h.
Quick-tunnel URLs die when their container stops, so never reuse URLs
from a previous spawn without rebuilding.

Or via CLI:

```bash
infra redirector spawn --count 2
infra redirector list
infra redirector kill --all
```
