# Deploy Directory

Deployment configurations and infrastructure-as-code for LazyOwn.

## Contents

| Path | Purpose |
|------|---------|
| `k8s/` | Kubernetes manifests for C2 and worker deployments |
| `docker/` | Docker Compose and container configurations |
| `redirector/` | Disposable cloudflared redirector with Caddy path filter |
| `c2/` | Ephemeral local C2 stack with automatic TLS (Caddy + Let's Encrypt) |
| `infra/providers/digitalocean/` | Terraform droplets + firewall for ephemeral cloud C2 |
| `infra/README.md` | IaC usage (`infra deploy` / `infra destroy`) |
| `range/ad-mini/` | Local vulnerable AD cyber range with fake traffic |

## Usage

```bash
infra redirector spawn --count 2
infra deploy --provider local
infra deploy --provider digitalocean --region nyc1
infra destroy --provider local
lab range start ad-mini
gen_report generate acme --with-ai
```

See `QUICKSTART.md` for full deployment guide.
