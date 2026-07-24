# Deploy Directory

Deployment configurations and infrastructure-as-code for LazyOwn.

## Contents

| Path | Purpose |
|------|---------|
| `k8s/` | Kubernetes manifests for C2 and worker deployments |
| `docker/` | Docker Compose and container configurations |

## Usage

```bash
kubectl apply -f deploy/k8s/lazyown-c2.yaml
```

See `QUICKSTART.md` for full deployment guide.
